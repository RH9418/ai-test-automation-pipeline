# import os
# import re

# # --- Configuration ---
# CODEGEN_LOG_DIR = "Codegen_Logs"

# # --- Code Blocks to be Injected ---

# SAFE_ACTION_FUNC = """
# import time
# from playwright.sync_api import TimeoutError

# def safe_action(page, action, description: str):
#     \"\"\"
#     Wraps a Playwright action in a try-except block and adds a smart wait.
#     It waits for the network to be idle after each action.
    
#     Args:
#         page: The Playwright page object.
#         action: A lambda function containing the Playwright action to perform.
#         description: A human-readable description of the action for logging.
#     \"\"\"
#     try:
#         action()
#         print(f"✅ SUCCESS: {description}")
#     except Exception as e:
#         print(f"❌ ERROR: Failed to {description}.")
#         # To see the detailed error from Playwright, uncomment the line below
#         # print(f"   └── Details: {e}")
#     finally:
#         # After every action, wait for the page's network to be idle.
#         try:
#             print("   └── Waiting for page network to be idle...")
#             # Wait up to 5 seconds for the network to be quiet
#             page.wait_for_load_state('networkidle', timeout=5000)
#             print("   └── Network is idle. Proceeding.")
#         except TimeoutError:
#             # If the network is still busy after 5s, print a warning and wait a bit longer.
#             print("   └── WARNING: Network still active after 5s. Forcing a 3s pause.")
#             time.sleep(3)
# """

# MFA_WAIT_BLOCK = """
#     mfa_message = \"\"\"
# ================================================================================
#   ACTION REQUIRED: MANUAL LOGIN & MFA
# --------------------------------------------------------------------------------
#   The script is now paused. Please complete the following in the browser window:
#   1. Log in with your credentials.
#   2. Complete the Multi-Factor Authentication (MFA) step.
#   3. Wait for the application's main dashboard or landing page to fully load.

#   ---> PRESS [ENTER] IN THIS TERMINAL WHEN YOU ARE READY TO PROCEED <---
# ================================================================================
# \"\"\"
#     print(mfa_message)
#     input()
#     print("\\n🚀 Starting automated actions...")
# """

# def process_playwright_file(file_path):
#     """
#     Reads a raw Playwright script, injects helper code, and wraps actions.
#     """
#     print(f"Processing file: {file_path}...")

#     with open(file_path, 'r', encoding='utf-8') as f:
#         lines = f.readlines()

#     if any("def safe_action(" in line for line in lines):
#         print("   -> Skipping: File has already been enhanced.")
#         return

#     new_lines = []
#     action_regex = re.compile(r"(\s*)(page\..*?\.(?:click|fill|check|press|goto|check|uncheck|select_option|dispatch_event|locator.*?(?:click|fill|check|press))\(.*\))")
#     safe_action_injected = False
#     mfa_block_injected = False

#     for line in lines:
#         # Inject the safe_action function definition right after imports
#         if "from playwright.sync_api" in line and not safe_action_injected:
#             new_lines.append(line)
#             new_lines.append(SAFE_ACTION_FUNC)
#             safe_action_injected = True
#             continue

#         # Inject the MFA wait block right after the first page.goto()
#         if "page.goto(" in line and not mfa_block_injected:
#             match = action_regex.match(line)
#             if match:
#                 indentation = match.group(1)
#                 action_call = match.group(2)
#                 description = action_call.replace('page.', '').replace('("', ' "').replace('")', '"')
#                 # Note the 'page' argument is added here
#                 wrapped_line = f"{indentation}safe_action(page, lambda: {action_call}, \"{description}\")\n"
#                 new_lines.append(wrapped_line)
#             else:
#                  new_lines.append(line)
            
#             new_lines.append(MFA_WAIT_BLOCK)
#             mfa_block_injected = True
#             continue

#         # Wrap all other Playwright actions with safe_action
#         match = action_regex.match(line)
#         if match:
#             indentation = match.group(1)
#             action_call = match.group(2)
#             description = action_call.replace('page.', '').replace('"', '\\"')
#             # Note the 'page' argument is added here
#             wrapped_line = f"{indentation}safe_action(page, lambda: {action_call}, \"{description}\")\n"
#             new_lines.append(wrapped_line)
#         else:
#             new_lines.append(line)

#     with open(file_path, 'w', encoding='utf-8') as f:
#         f.writelines(new_lines)

#     print(f"   -> Successfully enhanced with smart-waiting and saved.")


# if __name__ == "__main__":
#     if not os.path.exists(CODEGEN_LOG_DIR):
#         print(f"Error: Directory '{CODEGEN_LOG_DIR}' not found.")
#         print("Please create it and place your Playwright Codegen scripts inside.")
#     else:
#         print(f"--- Starting Playwright Script Enhancer ---")
#         print(f"Looking for .py files in '{CODEGEN_LOG_DIR}' directory...")
        
#         file_count = 0
#         for filename in os.listdir(CODEGEN_LOG_DIR):
#             if filename.endswith(".py"):
#                 file_path = os.path.join(CODEGEN_LOG_DIR, filename)
#                 process_playwright_file(file_path)
#                 file_count += 1
        
#         if file_count == 0:
#             print("No Python files found to process.")
#         else:
#             print(f"\n--- Enhancement complete. Processed {file_count} files. ---")















import os
import re
import sys
import argparse
from datetime import datetime

# --- Configuration ---
CODEGEN_LOG_DIR = "Codegen_Logs"
ENHANCED_LOG_DIR = "Enhanced_Logs" # New dedicated output directory
BASE_SCREENSHOT_DIR = "Test_Screenshots"

# --- Code Blocks to be Injected ---
# NOTICE THE 'r' PREFIX HERE. THIS IS CRITICAL FOR PREVENTING SYNTAX ERRORS!
FULL_INJECTION_BLOCK = r"""
import os
import sys
import time
import random
import re
from datetime import datetime
from playwright.sync_api import sync_playwright, Playwright, expect, TimeoutError

# --- Screenshot Directory Setup ---
SCREENSHOT_DIR = r"[[SCREENSHOT_DIR_PLACEHOLDER]]"
if not os.path.exists(SCREENSHOT_DIR):
    os.makedirs(SCREENSHOT_DIR)
screenshot_counter = 0

def capture_annotated_screenshot(page, locator, full_action_description: str):
    '''Highlights element with a thick red box and glow, then captures screenshot.'''
    global screenshot_counter
    screenshot_counter += 1
    
    try:
        # 1. Force element into view so the agent can see it
        locator.scroll_into_view_if_needed()
        locator.wait_for(state='visible', timeout=5000)
        
        box = locator.bounding_box()
        if not box:
            print(f"   └── ⚠️ Screenshot Warning: Bounding box null for '{full_action_description}'.")
            return
            
        js_description = full_action_description.replace("'", "\\'")
        # 2. Inject a high-visibility "Spotlight" annotation
        page.evaluate(f'''(params) => {{
            const {{ box, desc }} = params;
            
            // Create High-Visibility Box
            const div = document.createElement('div');
            div.id = 'ge-spotlight-box';
            div.style.position = 'absolute';
            div.style.left = `${{box.x}}px`;
            div.style.top = `${{box.y}}px`;
            div.style.width = `${{box.width}}px`;
            div.style.height = `${{box.height}}px`;
            div.style.border = '5px solid #FF0000'; // Thick Red
            div.style.boxShadow = '0 0 15px 5px rgba(255, 0, 0, 0.7)'; // Red Glow
            div.style.boxSizing = 'border-box';
            div.style.zIndex = '2147483647';
            div.style.pointerEvents = 'none'; // Don't interfere with clicks
            
            // Create High-Contrast Label
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
            label.style.fontFamily = 'Arial, sans-serif';
            document.body.appendChild(div);
            document.body.appendChild(label);
        }}''', {'box': box, 'desc': js_description})
        
        # 3. Small sleep to allow the browser to 'paint' the red box
        time.sleep(0.2)
        timestamp = datetime.now().strftime("%H-%M-%S")
        safe_filename = re.sub(r'[^a-z0-9]', '_', full_action_description.lower())[:40]
        filename = f"{timestamp}_{screenshot_counter:02d}_{safe_filename}.png"
        path = os.path.join(SCREENSHOT_DIR, filename)
        
        # Capture the screen
        page.screenshot(path=path, full_page=False) # Full page can sometimes blur annotations
        print(f"   └── 📸 Screenshot saved: {path}")
        
        # 4. Clean up
        page.evaluate('''() => {
            document.getElementById('ge-spotlight-box')?.remove();
            document.getElementById('ge-spotlight-label')?.remove();
        }''')
    except Exception as e:
        print(f"   └── ⚠️ Screenshot Error: {e}")

def safe_action(page, locator, action_name: str, description: str, *action_args, **action_kwargs):
    '''Performs action with spotlight screenshots and manual fallbacks.'''
    full_desc = f"{action_name.capitalize()}: {description}"
    if action_name == 'fill':
        full_desc += f" with '{action_args[0] if action_args else ''}'"
        
    try:
        # Pre-Fill Intervention
        if action_name == 'fill':
            print(f"\n⏸️ PAUSING FOR INPUT: About to fill '{description}'.")
            input("   └── Perform input manually in browser, then PRESS [ENTER] to continue...")
            page.wait_for_load_state('networkidle', timeout=5000)
            return

        # Screenshot Logic
        if action_name in ['click', 'dblclick', 'check', 'uncheck', 'hover']:
            try:
                locator.hover(timeout=2000)
                time.sleep(0.3)
            except: pass
            
        if action_name == 'close':
            try: locator.close()
            except: pass
            print(f"✅ SUCCESS: {description} (Teardown handled by Pytest)")
            return
            
        if locator != page:
            capture_annotated_screenshot(page, locator, full_desc)
            
        # Execution
        action_func = getattr(locator, action_name)
        action_func(*action_args, **action_kwargs)
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

# NOTICE THE 'r' PREFIX HERE AS WELL
MFA_WAIT_BLOCK = r"""
    print('''
================================================================================
  ACTION REQUIRED: MANUAL LOGIN & MFA
--------------------------------------------------------------------------------
  1. Log in manually. 2. Complete MFA. 3. Wait for dashboard to load.
  ---> PRESS [ENTER] IN THIS TERMINAL WHEN READY <---
================================================================================
''')
    input()
    print("\n🚀 Starting automated actions...")
"""

def process_playwright_file(file_path):
    base_name = os.path.basename(file_path)
    name_no_ext, ext = os.path.splitext(base_name)
    
    # Save directly to the Enhanced_Logs directory using the original filename
    output_path = os.path.join(ENHANCED_LOG_DIR, base_name)
    
    # Create a specific screenshot directory for this file
    specific_screenshot_dir = os.path.join(BASE_SCREENSHOT_DIR, name_no_ext).replace('\\', '/')
    
    print(f"Enhancing: {base_name} -> {output_path}")
    print(f"  └── Targeting Screenshots to: {specific_screenshot_dir}")
    
    with open(file_path, 'r', encoding='utf-8') as f:
        original_lines = f.readlines()
        
    new_script_lines = []
    
    action_regex = re.compile(
        r"^(\s*)"                                             # Group 1: Indentation
        r"(page\..+?)"                                        # Group 2: The full locator
        r"\.(click|fill|check|uncheck|press|hover|dblclick)"  # Group 3: The action
        r"\((.*?)\)"                                          # Group 4: Arguments
        r"(?:\s*#.*)?$"                                       # Allow optional inline comments
    )
    
    header_injected = False
    mfa_injected = False
    
    # Inject the specific folder path into the code block
    injected_block = FULL_INJECTION_BLOCK.replace("[[SCREENSHOT_DIR_PLACEHOLDER]]", specific_screenshot_dir)
    
    for line in original_lines:
        if line.strip().startswith(("import ", "from ")):
            if not header_injected:
                new_script_lines.append(injected_block)
                header_injected = True
            continue
            
        if "page.goto(" in line and not mfa_injected:
            url = line.strip().split('"')[1]
            new_script_lines.append(f"    safe_action(page, page, 'goto', 'Navigate to {url}', '{url}')\n")
            new_script_lines.append(MFA_WAIT_BLOCK)
            mfa_injected = True
            continue

        match = action_regex.search(line)
        if match:
            indent, loc, act, args = match.groups()
            
            # Safely escape backslashes and double quotes for the description string
            desc = re.sub(r'\s+', ' ', loc.replace('page.', '')).replace('\\', '\\\\').replace('"', '\\"')
            
            new_script_lines.append(f"{indent}safe_action(page, {loc}, '{act}', \"{desc}\", {args})\n")
        else:
            new_script_lines.append(line)
            
    with open(output_path, 'w', encoding='utf-8') as f:
        f.writelines(new_script_lines)
    print(f"  └── ✅ Successfully created spotlight-enhanced file.\n")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Enhance Playwright Codegen scripts with spot-light screenshots and safe fallbacks.")
    parser.add_argument('--files', nargs='*', help="Specific script names to process (e.g., promo_main.py). If omitted, processes all.")
    args = parser.parse_args()

    if not os.path.exists(CODEGEN_LOG_DIR):
        print(f"Error: {CODEGEN_LOG_DIR} not found.")
        sys.exit(1)
        
    os.makedirs(ENHANCED_LOG_DIR, exist_ok=True)
    os.makedirs(BASE_SCREENSHOT_DIR, exist_ok=True)

    print(f"{'='*60}\n🚀 Starting Playwright Script Enhancer Pipeline\n{'='*60}")

    if args.files:
        available_files = os.listdir(CODEGEN_LOG_DIR)
        scripts_to_process = [f for f in args.files if f in available_files]
        missing_files = [f for f in args.files if f not in available_files]
        if missing_files:
            print(f"⚠️ Warning: The following specified files were not found in {CODEGEN_LOG_DIR}: {missing_files}\n")
    else:
        scripts_to_process = [f for f in os.listdir(CODEGEN_LOG_DIR) if f.endswith(".py")]

    if not scripts_to_process:
        print("No valid Python scripts found to process.")
        sys.exit(0)

    for filename in scripts_to_process:
        process_playwright_file(os.path.join(CODEGEN_LOG_DIR, filename))
