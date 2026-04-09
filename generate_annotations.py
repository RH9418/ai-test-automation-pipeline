import os
import sys
import json
import base64
import glob
import argparse
import time
from typing import TypedDict, List, Dict, Any
from dotenv import load_dotenv

from langchain_openai import AzureChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
from langgraph.graph import StateGraph, END

# Load environment variables
load_dotenv()

# --- State Definition ---
class AgentState(TypedDict):
    script_name: str
    raw_code: str
    numbered_code: str
    screenshot_paths: List[str]
    sections: List[Dict[str, Any]]  # Output from the Planner
    comments: List[Dict[str, Any]]  # Output from the Worker
    output_path: str

# --- Helper Functions ---
def encode_image(image_path: str) -> str:
    """Encodes an image to Base64 to be sent to GPT-4o."""
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")

# --- Node 1: File Loader ---
def load_files(state: AgentState) -> dict:
    # 🔴 STRICTLY READ FROM Codegen_Logs
    script_path = os.path.join("Codegen_Logs", state["script_name"])
    
    with open(script_path, "r", encoding="utf-8") as f:
        raw_code = f.read()

    # 🔴 SAFETY CHECK: Ensure we aren't reading an Enhanced Log by mistake
    if "def safe_action" in raw_code or "capture_annotated_screenshot" in raw_code:
        print("\n" + "!"*80)
        print(f"🚨 CRITICAL WARNING 🚨")
        print(f"The file {script_path} contains 'safe_action' or boilerplate code!")
        print(f"You must use the RAW Playwright recording. Please fix the file in Codegen_Logs.")
        print("!"*80 + "\n")

    # Add line numbers to the code
    numbered_code = "\n".join([f"{i+1}: {line}" for i, line in enumerate(raw_code.split('\n'))])
    
    # Safely map to the specific screenshot subdirectory using os.path.join
    script_base_name = state["script_name"].replace(".py", "").replace("_enhanced", "")
    target_screenshot_dir = os.path.join("Test_Screenshots", script_base_name)
    
    # Use os.listdir to avoid glob bugs on Windows
    if not os.path.exists(target_screenshot_dir):
        print(f"⚠️ Warning: No screenshot directory found at {target_screenshot_dir}")
        screenshot_paths = []
    else:
        screenshot_paths = [
            os.path.join(target_screenshot_dir, f) 
            for f in os.listdir(target_screenshot_dir) 
            if f.endswith('.png')
        ]
        screenshot_paths.sort()
    
    print(f"\nLoaded script: {state['script_name']} | Total Images found: {len(screenshot_paths)}")
    
    return {
        "raw_code": raw_code,
        "numbered_code": numbered_code,
        "screenshot_paths": screenshot_paths,
        "comments": [] 
    }

# --- Node 2: The Planner (Overlap Sliding Window) ---
def plan_semantic_sections(state: AgentState) -> dict:
    print("🧠 Planning semantic sections using Overlap Sliding Window...")
    
    llm = AzureChatOpenAI(
        api_key=os.environ.get("AZURE_API_KEY"),
        azure_endpoint=os.environ.get("AZURE_ENDPOINT"),
        api_version=os.environ.get("AZURE_API_VERSION"),
        azure_deployment=os.environ.get("AZURE_DEPLOYMENT_NAME"),
        temperature=0.0, 
    ).bind(response_format={"type": "json_object"})

    filenames = [os.path.basename(p) for p in state["screenshot_paths"]]
    raw_lines = state["raw_code"].split('\n')
    total_lines = len(raw_lines)
    
    WINDOW_SIZE = 150
    OVERLAP = 20
    
    all_sections = []
    last_processed_line = 0
    start_idx = 0
    
    while start_idx < total_lines:
        end_idx = min(start_idx + WINDOW_SIZE, total_lines)
        
        # Extract the chunk and number it globally
        chunk_lines = raw_lines[start_idx:end_idx]
        numbered_chunk = "\n".join([f"{start_idx + i + 1}: {line}" for i, line in enumerate(chunk_lines)])
        
        print(f"   └── Planning window: Lines {start_idx + 1} to {end_idx}...")
        
        system_prompt = (
            "You are an Expert QA Architect. Your job is to semantically divide a portion of a Playwright script into cohesive, logical sections.\n"
            "CRITICAL INSTRUCTIONS:\n"
            f"1. You MUST start planning from line {last_processed_line + 1}. Do not plan sections for lines before this.\n"
            "2. Break the code into non-overlapping semantic sections (e.g., 'Initial Navigation', 'Applying Filters').\n"
            "3. EXHAUSTIVE MAPPING: Every line from your starting point must belong to a section. Do not leave gaps.\n"
            "4. THE OVERLAP RULE: If a logical user flow starts near the end of this snippet but seems incomplete, DO NOT include it in your final section. Stop your planning at the end of the last complete flow. Another agent will handle the rest of the file.\n"
            "5. Provide the `start_line` and `end_line` using the EXACT line numbers shown in the text.\n"
            "6. ALIGNING IMAGES: Select ALL `image_filenames` from the provided list that correspond to the actions in the section. Return them as a list of strings.\n"
            "7. Return ONLY a JSON object."
        )
        
        message_content = (
            f"Numbered Code Snippet:\n{numbered_chunk}\n\n"
            f"Available Screenshot Filenames (Chronological):\n{json.dumps(filenames, indent=2)}\n\n"
            "EXPECTED JSON FORMAT:\n"
            "{\n"
            '  "sections": [\n'
            '    {\n'
            '      "name": "Columns Configuration",\n'
            f'      "start_line": {max(start_idx + 1, last_processed_line + 1)},\n'
            f'      "end_line": {start_idx + 12},\n'
            '      "image_filenames": ["12-14-31_02_click__...png"]\n'
            '    }\n'
            "  ]\n"
            "}"
        )
        
        response = llm.invoke([SystemMessage(content=system_prompt), HumanMessage(content=message_content)])
        
        try:
            chunk_sections = json.loads(response.content).get("sections", [])
            
            if chunk_sections:
                all_sections.extend(chunk_sections)
                last_processed_line = chunk_sections[-1]["end_line"]
                print(f"       ✅ Found {len(chunk_sections)} sections. Processed up to line {last_processed_line}.")
                start_idx = last_processed_line
            else:
                print("       ⚠️ LLM returned no sections for this window. Forcing window forward.")
                start_idx += WINDOW_SIZE - OVERLAP
                
            time.sleep(2) # Prevent rate limits
            
        except Exception as e:
            print(f"       ❌ Failed to parse Planner JSON for window {start_idx + 1}-{end_idx}: {e}")
            start_idx += WINDOW_SIZE - OVERLAP

        if last_processed_line >= total_lines - 5: 
            break

    print(f"✅ Total script divided into {len(all_sections)} continuous semantic sections.")
    return {"sections": all_sections}

# --- Node 3: The Worker (Multimodal Annotator) ---
def annotate_sections(state: AgentState) -> dict:
    llm = AzureChatOpenAI(
        api_key=os.environ.get("AZURE_API_KEY"),
        azure_endpoint=os.environ.get("AZURE_ENDPOINT"),
        api_version=os.environ.get("AZURE_API_VERSION"),
        azure_deployment=os.environ.get("AZURE_DEPLOYMENT_NAME"),
        temperature=0.0, 
    ).bind(response_format={"type": "json_object"})
    
    all_comments = []
    raw_lines = state["numbered_code"].split('\n')
    prev_context = "None. This is the first section."
    
    for i, section in enumerate(state["sections"]):
        print(f"   └── 📝 Annotating Section {i+1}/{len(state['sections'])}: {section['name']}...")
        
        start_idx = max(0, section["start_line"] - 1)
        end_idx = min(len(raw_lines), section["end_line"])
        snippet = "\n".join(raw_lines[start_idx:end_idx])
        
        system_prompt = (
            f"You are an Expert QA Automation Engineer. You are annotating a specific section of a script titled: '{section['name']}'.\n"
            "Analyze the numbered code snippet. I am providing the chronological sequence of screenshots for this specific flow.\n\n"
            "ANTI-HALLUCINATION RULES (CRITICAL):\n"
            "1. DO NOT GUESS. If a locator is abstract and the screenshot does not clearly explain what it is, describe the action literally.\n"
            "2. DO NOT invent business rules or feature names that are not explicitly visible in the code or screenshots.\n"
            "3. Group related actions. If 3 lines fill out a single form, place ONE detailed comment above the first line.\n"
            "4. The line number you provide MUST match a line inside the provided snippet exactly.\n\n"
            "EXPECTED JSON FORMAT:\n"
            "{\n"
            '  "comments": [\n'
            '    {"line": 15, "comment": "Click on \'New Promotion\' to initiate creation"}\n'
            "  ]\n"
            "}"
        )
        
        message_content = [
            {"type": "text", "text": f"Context from Previous Section:\n{prev_context}\n\nCode Snippet for {section['name']}:\n\n{snippet}"}
        ]
        
        # Attach ALL images assigned to this section
        for img_name in section.get("image_filenames", []):
            img_path = next((p for p in state["screenshot_paths"] if os.path.basename(p) == img_name), None)
            if img_path:
                base64_img = encode_image(img_path)
                message_content.append({"type": "text", "text": f"\n--- Visual State: {img_name} ---\n"})
                message_content.append({
                    "type": "image_url",
                    "image_url": {"url": f"data:image/png;base64,{base64_img}", "detail": "low"}
                })
                
        response = llm.invoke([SystemMessage(content=system_prompt), HumanMessage(content=message_content)])
        
        try:
            chunk_comments = json.loads(response.content).get("comments", [])
            all_comments.extend(chunk_comments)
            prev_context = json.dumps(chunk_comments)
        except Exception as e:
            print(f"❌ Failed to parse Worker JSON for section {section['name']}: {e}")
            
    return {"comments": all_comments}

# --- Node 4: File Saver (Code Injection) ---
def save_annotated_code(state: AgentState) -> dict:
    os.makedirs("Annotated_Logs", exist_ok=True)
    out_path = os.path.join("Annotated_Logs", state["script_name"])
    
    raw_lines = state["raw_code"].split('\n')
    comments_dict = {int(item["line"]): item["comment"] for item in state["comments"]}
    annotated_lines = []
    
    for i, line in enumerate(raw_lines):
        line_num = i + 1
        if line_num in comments_dict:
            indent = len(line) - len(line.lstrip())
            annotated_lines.append(f"{' ' * indent}# {comments_dict[line_num]}")
        annotated_lines.append(line)
        
    final_code = "\n".join(annotated_lines)
    
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(final_code)
        
    print(f"✅ Successfully injected {len(comments_dict)} semantic comments and saved to: {out_path}\n")
    return {"output_path": out_path}

# --- Build the LangGraph Workflow ---
workflow = StateGraph(AgentState)
workflow.add_node("load_files", load_files)
workflow.add_node("plan_semantic_sections", plan_semantic_sections)
workflow.add_node("annotate_sections", annotate_sections)
workflow.add_node("save_annotated_code", save_annotated_code)
workflow.set_entry_point("load_files")
workflow.add_edge("load_files", "plan_semantic_sections")
workflow.add_edge("plan_semantic_sections", "annotate_sections")
workflow.add_edge("annotate_sections", "save_annotated_code")
workflow.add_edge("save_annotated_code", END)
annotator_app = workflow.compile()

# --- Execution Entry Point ---
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Semantically chunk and annotate Playwright logs.")
    parser.add_argument('--files', nargs='*', help="Specific script names to process. If omitted, processes all files in Codegen_Logs.")
    args = parser.parse_args()
    
    # 🔴 STRICTLY SET TO Codegen_Logs
    codegen_dir = "Codegen_Logs"
    screenshot_dir = "Test_Screenshots"
    
    os.makedirs(codegen_dir, exist_ok=True)
    os.makedirs(screenshot_dir, exist_ok=True)
    
    if args.files:
        available_files = os.listdir(codegen_dir)
        scripts_to_process = [f for f in args.files if f in available_files]
        missing_files = [f for f in args.files if f not in available_files]
        if missing_files:
            print(f"⚠️ Warning: The following specified files were not found in {codegen_dir}: {missing_files}")
    else:
        scripts_to_process = [f for f in os.listdir(codegen_dir) if f.endswith(".py")]
    
    if not scripts_to_process:
        print(f"No Python scripts found in {codegen_dir} to process.")
        sys.exit(0)
        
    print(f"{'='*60}\n🚀 Starting Playwright Log Annotator Pipeline\n{'='*60}")
    for script in scripts_to_process:
        initial_state = {"script_name": script}
        result = annotator_app.invoke(initial_state)
