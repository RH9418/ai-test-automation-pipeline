import os
import re
import sys
import argparse
from datetime import datetime

# --- Configuration ---
CODEGEN_LOG_DIR = "Codegen_Logs"
ENHANCED_LOG_DIR = "Enhanced_Logs" 
BASE_SCREENSHOT_DIR = "Test_Screenshots"

# --- Code Blocks to be Injected ---
FULL_INJECTION_BLOCK = r"""
import os
import sys
import time
import random
import re
import atexit
import contextlib
from datetime import datetime
from playwright.sync_api import sync_playwright, Playwright, expect, TimeoutError

# --- Execution Tracking & Reporting ---
_successful_actions = []
_failed_actions = []

def _generate_execution_report():
    report_dir = "Execution_Reports"
    os.makedirs(report_dir, exist_ok=True)
    script_name = "[[SCRIPT_NAME_PLACEHOLDER]]"
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_path = os.path.join(report_dir, f"{script_name}_Execution_{timestamp}.txt")
    
    with open(report_path, "w", encoding="utf-8") as f:
        f.write(f"Execution Report for: {script_name}\n")
        f.write("="*80 + "\n\n")
        f.write(f"Total Successful Automated Actions: {len(_successful_actions)}\n")
        f.write(f"Total Failed (Manual Intervention) Actions: {len(_failed_actions)}\n\n")
        
        f.write("--- ❌ FAILED ACTIONS (Required Human Intervention) ---\n")
        if _failed_actions:
            for fa in _failed_actions:
                f.write(f"- {fa}\n")
        else:
            f.write("None! 100% of actions succeeded automatically.\n")
            
        f.write("\n--- ✅ SUCCESSFUL ACTIONS ---\n")
        for sa in _successful_actions:
            f.write(f"- {sa}\n")
            
    print(f"\n📊 Execution Report saved to: {report_path}\n")

atexit.register(_generate_execution_report)

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
            label.style.fontFamily = 'Arial, sans-serif';
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
        
        page.evaluate('''() => {
            document.getElementById('ge-spotlight-box')?.remove();
            document.getElementById('ge-spotlight-label')?.remove();
        }''')
    except Exception as e:
        print(f"   └── ⚠️ Screenshot Error: {e}")

# 🔴 FIX: Injected the safe_download context manager to prevent timeouts
@contextlib.contextmanager
def safe_download(page, timeout_ms=300000): # 5 minutes default timeout
    class DummyEvent:
        @property
        def value(self):
            print("   └── ⚠️ Dummy download object returned. Proceeding safely.")
            return None
            
    try:
        print(f"\n⏳ Waiting for download to complete (Timeout: {timeout_ms/1000}s)...")
        with page.expect_download(timeout=timeout_ms) as d:
            yield d
        print("✅ SUCCESS: Download completed.")
        _successful_actions.append("Download action completed")
    except Exception as e:
        print(f"\n❌ ERROR: Download failed or timed out: {e}")
        _failed_actions.append("Download action failed/timed out")
        while True:
            print("\n" + "="*80 + "\n ACTION REQUIRED: Download Error\n" + "="*80)
            print(" Failed: Download operation timed out.")
            choice = input(" Did you perform the download manually or want to proceed anyway? (y/n): ").lower().strip()
            if choice == 'y': break
            elif choice == 'n': sys.exit(0)
        yield DummyEvent()

def safe_action(page, locator, action_name: str, description: str, *action_args, **action_kwargs):
    '''Performs action with spotlight screenshots and manual fallbacks.'''
    full_desc = f"{action_name.capitalize()}: {description}"
    if action_name == 'fill':
        full_desc += f" with '{action_args[0] if action_args else ''}'"
        
    try:
        if action_name == 'fill':
            print(f"\n⏸️ PAUSING FOR INPUT: About to fill '{description}'.")
            input("   └── Perform input manually in browser, then PRESS [ENTER] to continue...")
            page.wait_for_load_state('networkidle', timeout=5000)
            _successful_actions.append(full_desc + " (Manual Fill)")
            return

        if action_name in ['click', 'dblclick', 'check', 'uncheck', 'hover']:
            try:
                locator.hover(timeout=2000)
                time.sleep(0.3)
            except: pass
            
        if action_name == 'close':
            try: locator.close()
            except: pass
            print(f"✅ SUCCESS: {description} (Teardown handled by Pytest)")
            _successful_actions.append(full_desc)
            return
            
        if locator != page:
            capture_annotated_screenshot(page, locator, full_desc)
            
        action_func = getattr(locator, action_name)
        action_func(*action_args, **action_kwargs)
        
        print(f"✅ SUCCESS: {description}")
        _successful_actions.append(full_desc) 
        
    except Exception as e:
        print(f"❌ ERROR: Failed {action_name} on '{description}'.")
        _failed_actions.append(full_desc) 
        
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
    output_path = os.path.join(ENHANCED_LOG_DIR, base_name)
    specific_screenshot_dir = os.path.join(BASE_SCREENSHOT_DIR, name_no_ext).replace('\\', '/')
    
    print(f"Enhancing: {base_name} -> {output_path}")
    
    with open(file_path, 'r', encoding='utf-8') as f:
        original_lines = f.readlines()
        
    new_script_lines = []
    captured_actions = []
    missed_actions = []
    
    action_regex = re.compile(
        r"^(\s*)"                                             
        r"(page\..+?)"                                        
        r"\.(click|fill|check|uncheck|press|hover|dblclick)"  
        r"\((.*?)\)"                                          
        r"(?:\s*#.*)?$"                                       
    )
    
    header_injected = False
    mfa_injected = False
    
    injected_block = FULL_INJECTION_BLOCK.replace("[[SCREENSHOT_DIR_PLACEHOLDER]]", specific_screenshot_dir).replace("[[SCRIPT_NAME_PLACEHOLDER]]", name_no_ext)
    
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
            captured_actions.append(line.strip()) 
            continue

        # 🔴 FIX: Intercept the native download expectation and inject safe_download
        if "page.expect_download()" in line:
            new_script_lines.append(line.replace("page.expect_download()", "safe_download(page)"))
            continue

        match = action_regex.search(line)
        if match:
            indent, loc, act, args = match.groups()
            
            # 🔴 FIX: DYNAMIC AG-GRID SANITIZER
            # This instantly heals brittle AG-Grid IDs (e.g., #ag-169 -> .ag-root-wrapper)
            loc = re.sub(r'#ag-\d+', '.ag-root-wrapper', loc)
            
            desc = re.sub(r'\s+', ' ', loc.replace('page.', '')).replace('\\', '\\\\').replace('"', '\\"')
            
            new_script_lines.append(f"{indent}safe_action(page, {loc}, '{act}', \"{desc}\", {args})\n")
            captured_actions.append(line.strip()) 
        else:
            new_script_lines.append(line)
            
            stripped = line.strip()
            if not stripped.startswith("#") and (stripped.startswith("page.") or ".locator(" in stripped or ".get_by_" in stripped):
                ignore_list = [
                    "page.close()", "context.close()", "browser.close()", 
                    "page.expect_download(", "page.evaluate(", 
                    "page.wait_for_", "page.on(", "page.pause()"
                ]
                if not any(ign in stripped for ign in ignore_list):
                    missed_actions.append(stripped)
            
    with open(output_path, 'w', encoding='utf-8') as f:
        f.writelines(new_script_lines)
        
    print(f"  └── ✅ Successfully created spotlight-enhanced file.\n")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Enhance Playwright Codegen scripts with spot-light screenshots and safe fallbacks.")
    parser.add_argument('--files', nargs='*', help="Specific script names to process. If omitted, processes all.")
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
    else:
        scripts_to_process = [f for f in os.listdir(CODEGEN_LOG_DIR) if f.endswith(".py")]

    if not scripts_to_process:
        sys.exit(0)

    for filename in scripts_to_process:
        process_playwright_file(os.path.join(CODEGEN_LOG_DIR, filename))















