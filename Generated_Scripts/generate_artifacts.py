import os
import sys
import yaml
import argparse
import re
from datetime import datetime

# --- 1. Fix the SSL Telemetry Error ---
os.environ['CREWAI_DISABLE_TELEMETRY'] = 'True'
os.environ['OTEL_SDK_DISABLED'] = 'true'

from dotenv import load_dotenv
from crewai import Agent, Task, Crew, Process, LLM

# Load environment variables
load_dotenv()

# --- Configuration Loader ---
def load_yaml(file_path: str) -> dict:
    with open(file_path, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)

# --- Azure OpenAI LLM Configuration ---
azure_llm = LLM(
    model=f"azure/{os.environ.get('AZURE_DEPLOYMENT_NAME')}", 
    api_key=os.environ.get("AZURE_API_KEY"),
    base_url=os.environ.get("AZURE_ENDPOINT"),
    api_version=os.environ.get("AZURE_API_VERSION"),
    temperature=0.0, 
    max_tokens=8000  
)

# ====================================================================
# USER'S FALLBACK BLOCK (Injected at the top of generated Pytest files)
# ====================================================================
FALLBACK_INJECTION_BLOCK = r"""
import os
import sys
import time
import re
from datetime import datetime
import pytest
from playwright.sync_api import sync_playwright, Page, expect, TimeoutError

# --- Screenshot Directory Setup ---
SCREENSHOT_DIR = "Test_Screenshots"
if not os.path.exists(SCREENSHOT_DIR):
    os.makedirs(SCREENSHOT_DIR)
screenshot_counter = 0

def capture_annotated_screenshot(page: Page, locator, full_action_description: str):
    '''Highlights element with a thick red box and glow, then captures screenshot.'''
    global screenshot_counter
    screenshot_counter += 1
    try:
        locator.scroll_into_view_if_needed()
        locator.wait_for(state='visible', timeout=5000)
        box = locator.bounding_box()
        if not box:
            print(f"   └── ⚠️ Screenshot Warning: Bounding box null for '{full_action_description}'.")
            return
            
        js_description = full_action_description.replace("'", "\\'")
        page.evaluate(f'''(params) => {{
            const {{ box, desc }} = params;
            const div = document.createElement('div');
            div.id = 'ge-spotlight-box';
            div.style.position = 'absolute';
            div.style.left = `${{box.x}}px`;
            div.style.top = `${{box.y}}px`;
            div.style.width = `${{box.width}}px`;
            div.style.height = `${{box.height}}px`;
            div.style.border = '5px solid #FF0000';
            div.style.boxShadow = '0 0 15px 5px rgba(255, 0, 0, 0.7)';
            div.style.boxSizing = 'border-box';
            div.style.zIndex = '2147483647';
            div.style.pointerEvents = 'none';
            
            const label = document.createElement('div');
            label.id = 'ge-spotlight-label';
            label.textContent = desc;
            label.style.position = 'absolute';
            label.style.left = `${{box.x}}px`;
            label.style.top = `${{box.y - 40 > 0 ? box.y - 40 : box.y + box.height + 10}}px`;
            label.style.backgroundColor = '#FF0000';
            label.style.color = '#FFFFFF';
            label.style.padding = '8px 12px';
            label.style.fontSize = '16px';
            label.style.fontWeight = 'bold';
            label.style.borderRadius = '4px';
            label.style.zIndex = '2147483647';
            document.body.appendChild(div);
            document.body.appendChild(label);
        }}''', {'box': box, 'desc': js_description})
        
        time.sleep(0.2)
        timestamp = datetime.now().strftime("%H-%M-%S")
        safe_filename = re.sub(r'[^a-z0-9]', '_', full_action_description.lower())[:40]
        filename = f"{timestamp}_{screenshot_counter:02d}_{safe_filename}.png"
        path = os.path.join(SCREENSHOT_DIR, filename)
        
        page.screenshot(path=path, full_page=False)
        print(f"   └── 📸 Screenshot saved: {path}")
        
        page.evaluate("() => { document.getElementById('ge-spotlight-box')?.remove(); document.getElementById('ge-spotlight-label')?.remove(); }")
    except Exception as e:
        print(f"   └── ⚠️ Screenshot Error: {e}")

def safe_action(page: Page, locator, action_name: str, description: str, *action_args):
    '''Performs action with spotlight screenshots and manual fallbacks.'''
    full_desc = f"{action_name.capitalize()}: {description}"
    if action_name == 'fill':
        full_desc += f" with '{action_args[0] if action_args else ''}'"
        
    try:
        if action_name == 'fill':
            print(f"\n⏸️ PAUSING FOR INPUT: About to fill '{description}'.")
            input("   └── Perform input manually in browser, then PRESS [ENTER] to continue...")
            page.wait_for_load_state('networkidle', timeout=5000)
            return

        if action_name in ['click', 'dblclick', 'check', 'uncheck', 'hover']:
            try:
                locator.hover(timeout=2000)
                time.sleep(0.3)
            except: pass
            
        # --- BULLETPROOF TEARDOWN FIX ---
        if action_name == 'close':
            try: locator.close()
            except: pass
            print(f"✅ SUCCESS: {description} (Teardown handled by Pytest)")
            return

        if locator != page: # Don't try to draw a box around the entire page object
            capture_annotated_screenshot(page, locator, full_desc)
            action_func = getattr(locator, action_name)
            action_func(*action_args)
        else:
            if action_name == 'goto':
                page.goto(*action_args)
                
        print(f"✅ SUCCESS: {description}")
    except Exception as e:
        print(f"❌ ERROR: Failed {action_name} on '{description}'.")
        while True:
            print("\n" + "="*80 + "\n ACTION REQUIRED: Script Error\n" + "="*80)
            print(f" Failed: {full_desc}")
            choice = input(" Did you perform this manually? (y/n): ").lower().strip()
            if choice == 'y': break
            elif choice == 'n': sys.exit(0)
    finally:
        try: page.wait_for_load_state('networkidle', timeout=3000)
        except: time.sleep(1)
"""

# ====================================================================
# PHASE 1: Generate Feature Documentation
# ====================================================================
def process_annotated_script_to_docs(script_path: str, feature_name: str, tab_name: str) -> str:
    print(f"\n--- [PHASE 1] Generating Markdown Documentation for {os.path.basename(script_path)} ---")
    
    agents_config = load_yaml('configs/agents.yaml')['agents']
    tasks_config = load_yaml('configs/tasks.yaml')['tasks']
    with open(script_path, 'r', encoding='utf-8') as f:
        annotated_code = f.read()

    doc_agent = Agent(
        role=agents_config['feature_documentarian_agent']['role'],
        goal=agents_config['feature_documentarian_agent']['goal'],
        backstory=agents_config['feature_documentarian_agent']['backstory'],
        allow_delegation=False,
        llm=azure_llm
    )
    expander_agent = Agent(
        role=agents_config['detail_expander_agent']['role'],
        goal=agents_config['detail_expander_agent']['goal'],
        backstory=agents_config['detail_expander_agent']['backstory'],
        allow_delegation=False,
        llm=azure_llm
    )
    
    draft_task = Task(
        description=tasks_config['draft_high_level_task']['description'],
        expected_output=tasks_config['draft_high_level_task']['expected_output'],
        agent=doc_agent
    )
    expand_task = Task(
        description=tasks_config['expand_details_task']['description'],
        expected_output=tasks_config['expand_details_task']['expected_output'],
        agent=expander_agent
    )

    pipeline_crew = Crew(agents=[doc_agent, expander_agent], tasks=[draft_task, expand_task], process=Process.sequential)
    return str(pipeline_crew.kickoff(inputs={
        'feature_name': feature_name,
        'tab_name': tab_name,
        'codegen_script_content': annotated_code
    }))



def verify_script_completeness(raw_script_path: str, generated_script_path: str):
    print(f"\n--- Verifying Script Completeness ---")
    
    # 1. Read the raw log
    with open(raw_script_path, 'r', encoding='utf-8') as f:
        raw_lines = f.readlines()
        
    # Count actionable Playwright commands in the raw log
    # Matches .click(, .fill(, .check(, .goto(, .press(, .hover(
    action_regex = re.compile(r"\.(click|fill|check|uncheck|press|hover|goto)\(")
    raw_action_count = 0
    for line in raw_lines:
        # Ignore comments and browser teardown/setup
        if not line.strip().startswith("#") and action_regex.search(line):
            if "close()" not in line and "chromium.launch" not in line and "new_context" not in line and "new_page" not in line:
                raw_action_count += 1

    # 2. Read the generated script
    with open(generated_script_path, 'r', encoding='utf-8') as f:
        gen_content = f.read()
        
    # Count how many times safe_action was called
    safe_action_count = gen_content.count("safe_action(")

    print(f"   └── Found {raw_action_count} Playwright actions in the raw log.")
    print(f"   └── Found {safe_action_count} safe_action calls in the generated script.")

    # 3. Evaluate Completeness
    if safe_action_count < raw_action_count:
        print(f"❌ WARNING: The LLM dropped {raw_action_count - safe_action_count} actions! The generated script is incomplete.")
    elif safe_action_count > raw_action_count:
        print(f"⚠️ NOTE: The generated script has {safe_action_count - raw_action_count} more actions than the raw log. (Likely extra setup steps).")
    else:
        print(f"✅ VERIFICATION PASSED: Every action from the raw log is accounted for in the generated script.")

# ====================================================================
# PHASE 2: Generate Pytest Scripts with Fallbacks
# ====================================================================
# ====================================================================
# PHASE 2: Generate Pytest Scripts with Fallbacks
# ====================================================================
def process_docs_to_pytest(uat_doc_path: str, original_script_path: str, output_pytest_path: str):
    print(f"\n--- [PHASE 2] Generating Smart Pytest Scripts for {os.path.basename(uat_doc_path)} ---")
    
    agents_config = load_yaml('configs/agents.yaml')['agents']
    
    with open(uat_doc_path, 'r', encoding='utf-8') as f: uat_content = f.read()
    with open(original_script_path, 'r', encoding='utf-8') as f: raw_code_content = f.read()

    # --- Pre-Count the Exact Number of Actions Needed ---
    action_regex = re.compile(r"\.(click|fill|check|uncheck|press|hover|goto)\(")
    expected_action_count = 0
    for line in raw_code_content.split('\n'):
        if not line.strip().startswith("#") and action_regex.search(line):
            if "close()" not in line and "chromium.launch" not in line and "new_context" not in line and "new_page" not in line:
                expected_action_count += 1

    automation_agent = Agent(
        role=agents_config['automation_agent']['role'],
        goal=agents_config['automation_agent']['goal'],
        backstory=agents_config['automation_agent']['backstory'],
        allow_delegation=False,
        llm=azure_llm
    )

    pytest_task = Task(
        description=(
            "You are an Expert SDET. Your job is to convert a UAT Markdown Table into a fully functional Pytest script.\n\n"
            "CRITICAL RULES (FAILURE TO FOLLOW WILL CAUSE PIPELINE ERRORS):\n"
            "1. NO LAZINESS (EXHAUSTIVE MAPPING): You MUST process EVERY SINGLE ROW from the UAT document. Do NOT stop halfway. I have allocated 8000 tokens for this.\n"
            "2. NO FIXTURES: DO NOT create a `@pytest.fixture` for `shared_page`. The test environment provides it automatically.\n"
            "3. IGNORE TEARDOWN: You MUST completely ignore and omit any `close()` actions for the page, context, or browser.\n"
            "4. INJECT THE FALLBACK BLOCK: You MUST place the exact provided python block at the very top of your output file.\n"
            "5. TEST FUNCTIONS: Group the logic into sequential Pytest functions.\n"
            "6. NO RAW PLAYWRIGHT: You are STRICTLY FORBIDDEN from using raw `click()`, `fill()`, or `check()` commands. You MUST wrap every single UI interaction using the `safe_action(page, locator, action_name, description, *args)` paradigm.\n"
            f"7. STRICT COUNT ENFORCEMENT: The original script contains EXACTLY {expected_action_count} UI actions. Your generated script MUST contain EXACTLY {expected_action_count} `safe_action(...)` calls. You MUST not drop a single one.\n\n"
            "SYNTAX EXAMPLES:\n"
            "Raw: `page.get_by_test_id('promo-button').click()`\n"
            "Correct: `safe_action(shared_page, shared_page.get_by_test_id('promo-button'), 'click', 'Click the promotions button')`\n\n"
            "Raw: `page.get_by_test_id('promo-name').fill('TEST')`\n"
            "Correct: `safe_action(shared_page, shared_page.get_by_test_id('promo-name'), 'fill', 'Fill promotion name', 'TEST')`\n\n"
            "FALLBACK BLOCK TO INJECT:\n"
            "```python\n"
            f"{FALLBACK_INJECTION_BLOCK}\n"
            "```\n\n"
            "SOURCE MATERIAL:\n"
            f"UAT Document:\n{uat_content}\n\n"
            f"Original Annotated Code:\n{raw_code_content}"
        ),
        expected_output="A single, complete Python file containing the fallback block and all Pytest test functions. Output ONLY the raw python code without markdown backticks.",
        agent=automation_agent
    )

    script_crew = Crew(agents=[automation_agent], tasks=[pytest_task], process=Process.sequential)
    result = str(script_crew.kickoff())
    
    cleaned_code = result.strip()
    if cleaned_code.startswith("```python"): cleaned_code = cleaned_code[9:]
    elif cleaned_code.startswith("```"): cleaned_code = cleaned_code[3:]
    if cleaned_code.endswith("```"): cleaned_code = cleaned_code[:-3]

    with open(output_pytest_path, 'w', encoding='utf-8') as f:
        f.write(cleaned_code.strip())
        
    print(f"✅ Successfully generated robust Pytest script: {output_pytest_path}")
    verify_script_completeness(original_script_path, output_pytest_path)


# --- Execution Entry Point ---
if __name__ == "__main__":
    # --- Parse Command Line Arguments ---
    parser = argparse.ArgumentParser(description="Orchestrate CrewAI generation of Docs and Pytest scripts.")
    parser.add_argument('--step', type=int, choices=[1, 2], help="Phase to run (1 for Docs, 2 for Scripts). If omitted, runs both sequentially.")
    parser.add_argument('--files', nargs='*', help="Specific annotated script names to process (e.g., promo_main.py). If omitted, processes all in Annotated_Logs.")
    args = parser.parse_args()

    annotated_logs_dir = "Annotated_Logs"
    output_docs_dir = "Generated_Documentation"
    output_pytest_dir = "Generated_Scripts"
    
    os.makedirs(output_docs_dir, exist_ok=True)
    os.makedirs(output_pytest_dir, exist_ok=True)
    
    # --- Determine which files to process ---
    if args.files:
        available_files = os.listdir(annotated_logs_dir)
        scripts_to_process = [f for f in args.files if f in available_files]
        missing_files = [f for f in args.files if f not in available_files]
        if missing_files:
            print(f"⚠️ Warning: The following specified files were not found in {annotated_logs_dir}: {missing_files}")
    else:
        scripts_to_process = [f for f in os.listdir(annotated_logs_dir) if f.endswith(".py")]
    
    if not scripts_to_process:
        print(f"No annotated scripts found to process.")
        sys.exit(0)

    # --- Determine which steps to run ---
    run_step_1 = args.step is None or args.step == 1
    run_step_2 = args.step is None or args.step == 2

    # --- Process the Pipeline ---
    for script_name in scripts_to_process:
        print(f"\n{'='*60}\n🚀 Processing: {script_name}\n{'='*60}")
        script_path = os.path.join(annotated_logs_dir, script_name)
        feature_name_derived = script_name.replace(".py", "").replace("_", " ").title()
        
        doc_output_path = os.path.join(output_docs_dir, f"{feature_name_derived}_UAT.md")
        pytest_output_path = os.path.join(output_pytest_dir, f"test_{script_name}")
        
        # --- PHASE 1 (Docs) ---
        if run_step_1:
            if not os.path.exists(doc_output_path):
                md_result = process_annotated_script_to_docs(script_path, feature_name_derived, "Main Workspace")
                with open(doc_output_path, 'w', encoding='utf-8') as f:
                    f.write(md_result)
                print(f"✅ Generated Docs: {doc_output_path}")
            else:
                print(f"⏭️ Skipping Phase 1: {os.path.basename(doc_output_path)} already exists.")
        
        # --- PHASE 2 (Pytest) ---
        if run_step_2:
            if not os.path.exists(doc_output_path):
                print(f"❌ Error: Cannot run Phase 2. The required UAT document ({os.path.basename(doc_output_path)}) is missing.")
                print(f"Please run without `--step` or with `--step 1` first to generate the documentation.")
            else:
                process_docs_to_pytest(doc_output_path, script_path, pytest_output_path)
