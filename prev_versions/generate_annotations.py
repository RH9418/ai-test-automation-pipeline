# import os
# import json
# import base64
# import glob
# from typing import TypedDict, List, Dict, Any
# from dotenv import load_dotenv

# from langchain_openai import AzureChatOpenAI
# from langchain_core.messages import HumanMessage, SystemMessage
# from langgraph.graph import StateGraph, END

# # Load environment variables
# load_dotenv()

# # --- State Definition ---
# class AgentState(TypedDict):
#     script_name: str
#     raw_code: str
#     numbered_code: str
#     screenshot_paths: List[str]
#     sections: List[Dict[str, Any]]  # Output from the Planner
#     comments: List[Dict[str, Any]]  # Output from the Worker
#     output_path: str

# # --- Helper Functions ---
# def encode_image(image_path: str) -> str:
#     with open(image_path, "rb") as image_file:
#         return base64.b64encode(image_file.read()).decode("utf-8")

# # --- Node 1: File Loader ---
# def load_files(state: AgentState) -> dict:
#     script_path = os.path.join("Codegen_Logs", state["script_name"])
    
#     with open(script_path, "r", encoding="utf-8") as f:
#         raw_code = f.read()

#     # Add line numbers to the code
#     numbered_code = "\n".join([f"{i+1}: {line}" for i, line in enumerate(raw_code.split('\n'))])

#     # Load all screenshots chronologically
#     screenshot_paths = sorted(glob.glob("Test_Screenshots/*.png"))
    
#     print(f"Loaded script: {state['script_name']} | Total Images found: {len(screenshot_paths)}")
    
#     return {
#         "raw_code": raw_code,
#         "numbered_code": numbered_code,
#         "screenshot_paths": screenshot_paths,
#         "comments": [] # Initialize empty list
#     }

# # --- Node 2: The Planner (Text-Only Semantic Chunker) ---
# def plan_semantic_sections(state: AgentState) -> dict:
#     print("Planning semantic sections...")
    
#     llm = AzureChatOpenAI(
#         api_key=os.environ.get("AZURE_API_KEY"),
#         azure_endpoint=os.environ.get("AZURE_ENDPOINT"),
#         api_version=os.environ.get("AZURE_API_VERSION"),
#         azure_deployment=os.environ.get("AZURE_DEPLOYMENT_NAME"),
#         temperature=0.0, # Zero temp for strict JSON adherence
#     ).bind(response_format={"type": "json_object"})

#     # Extract just the filenames to pass as text context
#     filenames = [os.path.basename(p) for p in state["screenshot_paths"]]

#     system_prompt = (
#         "You are an Expert QA Architect. Your job is to semantically divide a Playwright script into logical sections.\n"
#         "I will provide the numbered code and a chronological list of screenshot filenames (which contain locator hints).\n\n"
#         "INSTRUCTIONS:\n"
#         "1. Break the code into 5 to 10 logical sections (e.g., 'Initial Navigation', 'Fill Promotion Details', 'Hierarchy Selection', etc.).\n"
#         "2. For each section, provide the `start_line` and `end_line`.\n"
#         "3. Select exactly ONE `image_filename` from the provided list that best visually represents the START of this section. If none fit well, use the closest chronological one.\n"
#         "4. Return ONLY a JSON object."
#     )

#     message_content = (
#         f"Numbered Code:\n{state['numbered_code']}\n\n"
#         f"Available Screenshot Filenames (Chronological):\n{json.dumps(filenames, indent=2)}\n\n"
#         "EXPECTED JSON FORMAT:\n"
#         "{\n"
#         '  "sections": [\n'
#         '    {"name": "Initial Navigation", "start_line": 1, "end_line": 12, "image_filename": "12-14-31_02_click_...png"}\n'
#         "  ]\n"
#         "}"
#     )

#     response = llm.invoke([SystemMessage(content=system_prompt), HumanMessage(content=message_content)])
    
#     try:
#         sections = json.loads(response.content)["sections"]
#         print(f"Divided code into {len(sections)} semantic sections.")
#         return {"sections": sections}
#     except Exception as e:
#         print(f"Failed to parse Planner JSON: {e}")
#         return {"sections": []}

# # --- Node 3: The Worker (Multimodal Annotator) ---
# def annotate_sections(state: AgentState) -> dict:
#     llm = AzureChatOpenAI(
#         api_key=os.environ.get("AZURE_API_KEY"),
#         azure_endpoint=os.environ.get("AZURE_ENDPOINT"),
#         api_version=os.environ.get("AZURE_API_VERSION"),
#         azure_deployment=os.environ.get("AZURE_DEPLOYMENT_NAME"),
#         temperature=0.1, 
#     ).bind(response_format={"type": "json_object"})

#     all_comments = []
#     raw_lines = state["numbered_code"].split('\n')

#     # Iterate through one semantic section at a time
#     for i, section in enumerate(state["sections"]):
#         print(f"Annotating Section {i+1}/{len(state['sections'])}: {section['name']}...")
        
#         # Extract the specific snippet of code for this section
#         start_idx = max(0, section["start_line"] - 1)
#         end_idx = min(len(raw_lines), section["end_line"])
#         snippet = "\n".join(raw_lines[start_idx:end_idx])

#         # Find the full path for the selected image
#         selected_image_path = None
#         for path in state["screenshot_paths"]:
#             if os.path.basename(path) == section["image_filename"]:
#                 selected_image_path = path
#                 break
        
#         system_prompt = (
#             f"You are an Expert QA Automation Engineer. You are annotating a specific section of code titled: '{section['name']}'.\n"
#             "Analyze the numbered code snippet and the single provided screenshot showing the UI state for this section.\n"
#             "Return a JSON object mapping the EXACT line numbers to business-logic comments.\n\n"
#             "EXPECTED JSON FORMAT:\n"
#             "{\n"
#             '  "comments": [\n'
#             '    {"line": 15, "comment": "Click on \'New Promotion\' to initiate creation"}\n'
#             "  ]\n"
#             "}"
#         )

#         message_content = [{"type": "text", "text": f"Code Snippet:\n\n{snippet}"}]

#         # Attach the single image if found
#         if selected_image_path:
#             base64_img = encode_image(selected_image_path)
#             message_content.append({"type": "text", "text": f"\n--- Section Context Image: {section['image_filename']} ---\n"})
#             message_content.append({
#                 "type": "image_url",
#                 "image_url": {"url": f"data:image/png;base64,{base64_img}", "detail": "low"}
#             })

#         response = llm.invoke([SystemMessage(content=system_prompt), HumanMessage(content=message_content)])
        
#         try:
#             chunk_comments = json.loads(response.content).get("comments", [])
#             all_comments.extend(chunk_comments)
#         except Exception as e:
#             print(f"Failed to parse Worker JSON for section {section['name']}: {e}")

#     return {"comments": all_comments}

# # --- Node 4: File Saver (Code Injection) ---
# def save_annotated_code(state: AgentState) -> dict:
#     os.makedirs("Annotated_Logs", exist_ok=True)
#     out_path = os.path.join("Annotated_Logs", state["script_name"])
    
#     raw_lines = state["raw_code"].split('\n')
#     comments_dict = {int(item["line"]): item["comment"] for item in state["comments"]}
#     annotated_lines = []
    
#     for i, line in enumerate(raw_lines):
#         line_num = i + 1 
#         if line_num in comments_dict:
#             # Maintain indentation
#             indent = len(line) - len(line.lstrip())
#             annotated_lines.append(f"{' ' * indent}# {comments_dict[line_num]}")
#         annotated_lines.append(line)
        
#     final_code = "\n".join(annotated_lines)
    
#     with open(out_path, "w", encoding="utf-8") as f:
#         f.write(final_code)
        
#     print(f"✅ Successfully injected {len(comments_dict)} comments and saved to: {out_path}")
#     return {"output_path": out_path}

# # --- Build the LangGraph Workflow ---
# workflow = StateGraph(AgentState)

# workflow.add_node("load_files", load_files)
# workflow.add_node("plan_semantic_sections", plan_semantic_sections)
# workflow.add_node("annotate_sections", annotate_sections)
# workflow.add_node("save_annotated_code", save_annotated_code)

# workflow.set_entry_point("load_files")
# workflow.add_edge("load_files", "plan_semantic_sections")
# workflow.add_edge("plan_semantic_sections", "annotate_sections")
# workflow.add_edge("annotate_sections", "save_annotated_code")
# workflow.add_edge("save_annotated_code", END)

# annotator_app = workflow.compile()

# # --- Execution Entry Point ---
# if __name__ == "__main__":
#     os.makedirs("Codegen_Logs", exist_ok=True)
#     os.makedirs("Test_Screenshots", exist_ok=True)
    
#     scripts_to_process = [f for f in os.listdir("Codegen_Logs") if f.endswith(".py")]
    
#     if not scripts_to_process:
#         print("No Python scripts found in the Codegen_Logs directory to process.")
#     else:
#         for script in scripts_to_process:
#             print(f"\n--- Starting workflow for {script} ---")
#             initial_state = {"script_name": script}
#             result = annotator_app.invoke(initial_state)
















import os
import sys
import json
import base64
import glob
import argparse
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
    # 1. Read pure, raw code from Codegen_Logs
    script_path = os.path.join("Codegen_Logs", state["script_name"])
    
    with open(script_path, "r", encoding="utf-8") as f:
        raw_code = f.read()

    # Add line numbers to the code so the LLM can reference exactly where to put comments
    numbered_code = "\n".join([f"{i+1}: {line}" for i, line in enumerate(raw_code.split('\n'))])
    
    # 2. Dynamically map to the specific screenshot subdirectory
    # e.g., 'wba_Alerts.py' -> 'Test_Screenshots/wba_Alerts/*.png'
    script_base_name = state["script_name"].replace(".py", "")
    target_screenshot_dir = f"Test_Screenshots/{script_base_name}"
    
    # Load all screenshots chronologically from that specific subdirectory
    screenshot_paths = sorted(glob.glob(f"{target_screenshot_dir}/*.png"))
    
    print(f"\nLoaded script: {state['script_name']} | Total Images found in {target_screenshot_dir}: {len(screenshot_paths)}")
    
    return {
        "raw_code": raw_code,
        "numbered_code": numbered_code,
        "screenshot_paths": screenshot_paths,
        "comments": [] # Initialize empty list
    }

# --- Node 2: The Planner (Text-Only Semantic Chunker) ---
def plan_semantic_sections(state: AgentState) -> dict:
    print("🧠 Planning semantic sections based on user flows...")
    
    llm = AzureChatOpenAI(
        api_key=os.environ.get("AZURE_API_KEY"),
        azure_endpoint=os.environ.get("AZURE_ENDPOINT"),
        api_version=os.environ.get("AZURE_API_VERSION"),
        azure_deployment=os.environ.get("AZURE_DEPLOYMENT_NAME"),
        temperature=0.0, # Zero temp for strict analytical adherence
    ).bind(response_format={"type": "json_object"})

    filenames = [os.path.basename(p) for p in state["screenshot_paths"]]
    
    system_prompt = (
        "You are an Expert QA Architect. Your job is to semantically divide a Playwright script into cohesive, logical sections.\n"
        "CRITICAL INSTRUCTIONS:\n"
        "1. Break the entire script into non-overlapping semantic sections.\n"
        "2. EXHAUSTIVE MAPPING: Every single line of code MUST belong to exactly one section. Do not leave gaps.\n"
        "3. Provide the `start_line` and `end_line`.\n"
        "4. ALIGNING IMAGES: Select ALL `image_filenames` from the provided list that correspond to the actions within this specific section's line range. Return them as a list of strings. If none apply, return an empty list [].\n"
        "5. Return ONLY a JSON object."
    )
    
    message_content = (
        f"Numbered Code:\n{state['numbered_code']}\n\n"
        f"Available Screenshot Filenames (Chronological):\n{json.dumps(filenames, indent=2)}\n\n"
        "EXPECTED JSON FORMAT:\n"
        "{\n"
        '  "sections": [\n'
        '    {\n'
        '      "name": "Initial Setup & Navigation",\n'
        '      "start_line": 1,\n'
        '      "end_line": 12,\n'
        '      "image_filenames": ["12-14-31_02_click__...png", "12-14-35_03_click__...png"]\n'
        '    }\n'
        "  ]\n"
        "}"
    )
    
    response = llm.invoke([SystemMessage(content=system_prompt), HumanMessage(content=message_content)])
    
    try:
        sections = json.loads(response.content).get("sections", [])
        print(f"✅ Divided code into {len(sections)} semantic sections.")
        return {"sections": sections}
    except Exception as e:
        print(f"❌ Failed to parse Planner JSON: {e}")
        return {"sections": []}

# --- Node 3: The Worker (Multimodal Annotator) ---
def annotate_sections(state: AgentState) -> dict:
    llm = AzureChatOpenAI(
        api_key=os.environ.get("AZURE_API_KEY"),
        azure_endpoint=os.environ.get("AZURE_ENDPOINT"),
        api_version=os.environ.get("AZURE_API_VERSION"),
        azure_deployment=os.environ.get("AZURE_DEPLOYMENT_NAME"),
        temperature=0.0, # 0.0 Temperature to kill hallucinations
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
            "1. DO NOT GUESS. If a locator is abstract (e.g., `div:nth-child(8)`) and the screenshot does not clearly explain what it is, describe the action literally (e.g., 'Click the 8th div element').\n"
            "2. DO NOT invent business rules, feature names, or product names that are not explicitly visible in the code or the screenshots.\n"
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
        
        # Attach ALL images assigned to this section to prevent LLM from guessing
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
            # Maintain the original indentation level of the code
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
    parser.add_argument('--files', nargs='*', help="Specific script names to process (e.g., promo_main.py). If omitted, processes all files.")
    args = parser.parse_args()
    
    # Use Codegen_Logs as the source directory for pure scripts
    codegen_dir = "Codegen_Logs"
    
    os.makedirs(codegen_dir, exist_ok=True)
    
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
