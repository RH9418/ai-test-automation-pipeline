
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
    script_name = "BBU_Export"
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

# Register the report to generate automatically when the script finishes or exits
atexit.register(_generate_execution_report)

# --- Screenshot Directory Setup ---
SCREENSHOT_DIR = r"Test_Screenshots/BBU_Export"
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

# 🔴 FIX: Safe Download Context Manager
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
        # Pre-Fill Intervention
        if action_name == 'fill':
            print(f"\n⏸️ PAUSING FOR INPUT: About to fill '{description}'.")
            input("   └── Perform input manually in browser, then PRESS [ENTER] to continue...")
            page.wait_for_load_state('networkidle', timeout=5000)
            
            # Manual fills are considered successful since the user executes them
            _successful_actions.append(full_desc + " (Manual Fill)")
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
            _successful_actions.append(full_desc)
            return
            
        if locator != page:
            capture_annotated_screenshot(page, locator, full_desc)
            
        # Execution
        action_func = getattr(locator, action_name)
        action_func(*action_args, **action_kwargs)
        
        print(f"✅ SUCCESS: {description}")
        _successful_actions.append(full_desc) # Track success
        
    except Exception as e:
        print(f"❌ ERROR: Failed {action_name} on '{description}'.")
        _failed_actions.append(full_desc) # Track failure
        
        while True:
            print("\n" + "="*80 + "\n ACTION REQUIRED: Script Error\n" + "="*80)
            print(f" Failed: {full_desc}")
            choice = input(" Did you perform this manually? (y/n): ").lower().strip()
            if choice == 'y': break
            elif choice == 'n': sys.exit(0)
    finally:
        try: page.wait_for_load_state('networkidle', timeout=3000)
        except: time.sleep(1)


def run(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    safe_action(page, page, 'goto', 'Navigate to https://stage.bbu.esp.antuit.ai/dp/demand-planning/executive-dashboard?workbookId=4&tabIndex=7', 'https://stage.bbu.esp.antuit.ai/dp/demand-planning/executive-dashboard?workbookId=4&tabIndex=7')

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
    safe_action(page, page.get_by_text("FilterStart Week 01/25/2026"), 'click', "get_by_text(\"FilterStart Week 01/25/2026\")", )
    safe_action(page, page.get_by_text("Filter"), 'click', "get_by_text(\"Filter\")", )
    safe_action(page, page.get_by_text("Start Week / End Week"), 'click', "get_by_text(\"Start Week / End Week\")", )
    safe_action(page, page.locator("#Datepick"), 'click', "locator(\"#Datepick\")", )
    safe_action(page, page.locator("div").filter(has_text="‹ January 2026 ›").nth(4), 'click', "locator(\"div\").filter(has_text=\"‹ January 2026 ›\").nth(4)", )
    safe_action(page, page.get_by_text("4").first, 'click', "get_by_text(\"4\").first", )
    safe_action(page, page.get_by_role("button", name="January"), 'click', "get_by_role(\"button\", name=\"January\")", )
    safe_action(page, page.get_by_text("February").first, 'click', "get_by_text(\"February\").first", )
    safe_action(page, page.get_by_role("button", name="2026").first, 'click', "get_by_role(\"button\", name=\"2026\").first", )
    safe_action(page, page.get_by_role("gridcell", name="2025"), 'click', "get_by_role(\"gridcell\", name=\"2025\")", )
    safe_action(page, page.get_by_role("button", name="2026"), 'click', "get_by_role(\"button\", name=\"2026\")", )
    safe_action(page, page.get_by_role("gridcell", name="2024"), 'click', "get_by_role(\"gridcell\", name=\"2024\")", )
    safe_action(page, page.get_by_role("gridcell", name="January").nth(1), 'click', "get_by_role(\"gridcell\", name=\"January\").nth(1)", )
    safe_action(page, page.get_by_text("2", exact=True).nth(2), 'click', "get_by_text(\"2\", exact=True).nth(2)", )
    safe_action(page, page.get_by_text("Start Week 01/25/2026 End"), 'click', "get_by_text(\"Start Week 01/25/2026 End\")", )
    safe_action(page, page.get_by_text("Total ByProduct Level None"), 'click', "get_by_text(\"Total ByProduct Level None\")", )
    safe_action(page, page.get_by_text("Total By"), 'click', "get_by_text(\"Total By\")", )
    safe_action(page, page.get_by_text("Product Level None Location"), 'click', "get_by_text(\"Product Level None Location\")", )
    safe_action(page, page.get_by_text("Product Level"), 'click', "get_by_text(\"Product Level\")", )
    safe_action(page, page.get_by_text("None").first, 'click', "get_by_text(\"None\").first", )
    safe_action(page, page.get_by_text("Select All"), 'click', "get_by_text(\"Select All\")", )
    safe_action(page, page.locator(".d-flex.flex-column.justify-content-center").first, 'click', "locator(\".d-flex.flex-column.justify-content-center\").first", )
    safe_action(page, page.get_by_text("Brand Level 4"), 'click', "get_by_text(\"Brand Level 4\")", )
    safe_action(page, page.get_by_text("Brand Level 3"), 'click', "get_by_text(\"Brand Level 3\")", )
    safe_action(page, page.get_by_text("Brand Level 2"), 'click', "get_by_text(\"Brand Level 2\")", )
    safe_action(page, page.locator(".overflow-auto > div:nth-child(3)"), 'click', "locator(\".overflow-auto > div:nth-child(3)\")", )
    safe_action(page, page.get_by_text("UPC"), 'click', "get_by_text(\"UPC\")", )
    safe_action(page, page.get_by_text("Product Level 4"), 'click', "get_by_text(\"Product Level 4\")", )
    safe_action(page, page.get_by_text("Product Level 3"), 'click', "get_by_text(\"Product Level 3\")", )
    safe_action(page, page.get_by_text("Product Level 2"), 'click', "get_by_text(\"Product Level 2\")", )
    safe_action(page, page.get_by_text("Location Level"), 'click', "get_by_text(\"Location Level\")", )
    safe_action(page, page.get_by_text("None").first, 'click', "get_by_text(\"None\").first", )
    safe_action(page, page.get_by_text("Select All"), 'click', "get_by_text(\"Select All\")", )
    safe_action(page, page.get_by_text("Sales Level 6"), 'click', "get_by_text(\"Sales Level 6\")", )
    safe_action(page, page.get_by_text("Sales Level 5", exact=True), 'click', "get_by_text(\"Sales Level 5\", exact=True)", )
    safe_action(page, page.get_by_text("Sales Level 4", exact=True), 'click', "get_by_text(\"Sales Level 4\", exact=True)", )
    safe_action(page, page.locator("div:nth-child(8)"), 'click', "locator(\"div:nth-child(8)\")", )
    safe_action(page, page.get_by_text("Sales Level 1", exact=True), 'click', "get_by_text(\"Sales Level 1\", exact=True)", )
    safe_action(page, page.locator(".overflow-auto > div:nth-child(5)"), 'click', "locator(\".overflow-auto > div:nth-child(5)\")", )
    safe_action(page, page.locator("div:nth-child(7)"), 'click', "locator(\"div:nth-child(7)\")", )
    safe_action(page, page.get_by_text("Depot", exact=True), 'click', "get_by_text(\"Depot\", exact=True)", )
    safe_action(page, page.get_by_text("Sales Level 3", exact=True), 'click', "get_by_text(\"Sales Level 3\", exact=True)", )
    safe_action(page, page.get_by_text("BUSS Environment", exact=True), 'click', "get_by_text(\"BUSS Environment\", exact=True)", )
    safe_action(page, page.locator("span").filter(has_text="BUSS Route ID"), 'click', "locator(\"span\").filter(has_text=\"BUSS Route ID\")", )
    safe_action(page, page.locator("div:nth-child(2) > esp-multiselect-dropdown > .multiselect-dropdown > div > .w-100"), 'click', "locator(\"div:nth-child(2) > esp-multiselect-dropdown > .multiselect-dropdown > div > .w-100\")", )
    safe_action(page, page.get_by_text("Customer Level"), 'click', "get_by_text(\"Customer Level\")", )
    safe_action(page, page.locator("div:nth-child(3) > esp-multiselect-dropdown > .multiselect-dropdown > div > .w-100"), 'click', "locator(\"div:nth-child(3) > esp-multiselect-dropdown > .multiselect-dropdown > div > .w-100\")", )
    safe_action(page, page.get_by_text("Select All"), 'click', "get_by_text(\"Select All\")", )
    safe_action(page, page.get_by_text("All").nth(3), 'click', "get_by_text(\"All\").nth(3)", )
    safe_action(page, page.get_by_text("Time"), 'click', "get_by_text(\"Time\")", )
    safe_action(page, page.get_by_text("None").nth(1), 'click', "get_by_text(\"None\").nth(1)", )
    safe_action(page, page.locator("div").filter(has_text=re.compile(r"^Weekly$")).nth(3), 'click', "locator(\"div\").filter(has_text=re.compile(r\"^Weekly$\")).nth(3)", )
    safe_action(page, page.get_by_text("Measures", exact=True), 'click', "get_by_text(\"Measures\", exact=True)", )
    safe_action(page, page.locator(".measure-filter-list"), 'click', "locator(\".measure-filter-list\")", )
    safe_action(page, page.get_by_text("Measure", exact=True), 'click', "get_by_text(\"Measure\", exact=True)", )
    safe_action(page, page.get_by_text("All Measures").first, 'click', "get_by_text(\"All Measures\").first", )
    safe_action(page, page.get_by_text("Select All Measures"), 'click', "get_by_text(\"Select All Measures\")", )
    safe_action(page, page.get_by_text("Select All Measures"), 'click', "get_by_text(\"Select All Measures\")", )
    safe_action(page, page.get_by_text("User Forecast Total"), 'click', "get_by_text(\"User Forecast Total\")", )
    safe_action(page, page.locator(".d-flex.dropdown-option.align-items-center.p-v-5.p-l-32").first, 'click', "locator(\".d-flex.dropdown-option.align-items-center.p-v-5.p-l-32\").first", )
    safe_action(page, page.get_by_text("User Forecast Base"), 'click', "get_by_text(\"User Forecast Base\")", )
    safe_action(page, page.locator(".overflow-auto > div:nth-child(3)"), 'click', "locator(\".overflow-auto > div:nth-child(3)\")", )
    safe_action(page, page.locator(".overflow-auto > div:nth-child(5)"), 'click', "locator(\".overflow-auto > div:nth-child(5)\")", )
    safe_action(page, page.get_by_text("Select All Measures"), 'click', "get_by_text(\"Select All Measures\")", )
    safe_action(page, page.get_by_text("Measure", exact=True), 'click', "get_by_text(\"Measure\", exact=True)", )
    safe_action(page, page.get_by_role("button", name="Download"), 'click', "get_by_role(\"button\", name=\"Download\")", )
    safe_action(page, page.get_by_text("Please note that a maximum of"), 'click', "get_by_text(\"Please note that a maximum of\")", )
    safe_action(page, page.get_by_role("button", name="Reset"), 'click', "get_by_role(\"button\", name=\"Reset\")", )
    safe_action(page, page.get_by_role("button", name="Reset"), 'click', "get_by_role(\"button\", name=\"Reset\")", )

    # ---------------------
    context.close()
    browser.close()


with sync_playwright() as playwright:
    run(playwright)
