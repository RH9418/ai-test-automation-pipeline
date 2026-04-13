
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
    script_name = "BBU_By_Customer_Daily"
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
SCREENSHOT_DIR = r"Test_Screenshots/BBU_By_Customer_Daily"
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
    safe_action(page, page, 'goto', 'Navigate to https://stage.bbu.esp.antuit.ai/dp/demand-planning/executive-dashboard?workbookId=4&tabIndex=5', 'https://stage.bbu.esp.antuit.ai/dp/demand-planning/executive-dashboard?workbookId=4&tabIndex=5')

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
    safe_action(page, page.get_by_text("Customer Total columns (0)"), 'click', "get_by_text(\"Customer Total columns (0)\")", )
    safe_action(page, page.get_by_text("Customer Total"), 'click', "get_by_text(\"Customer Total\")", )
    safe_action(page, page.locator("esp-card-component").filter(has_text="Customer Total columns (0)").get_by_role("button"), 'click', "locator(\"esp-card-component\").filter(has_text=\"Customer Total columns (0)\").get_by_role(\"button\")", )
    safe_action(page, page.get_by_role("textbox", name="Filter Columns Input"), 'click', "get_by_role(\"textbox\", name=\"Filter Columns Input\")", )
    safe_action(page, page.get_by_role("textbox", name="Filter Columns Input"), 'fill', "get_by_role(\"textbox\", name=\"Filter Columns Input\")", "System")
    safe_action(page, page.get_by_role("textbox", name="Filter Columns Input"), 'press', "get_by_role(\"textbox\", name=\"Filter Columns Input\")", "Enter")
    safe_action(page, page.locator(".ag-column-select-column").first, 'click', "locator(\".ag-column-select-column\").first", )
    safe_action(page, page.get_by_role("treeitem", name="System Forecast Base (Plan").get_by_label("Press SPACE to toggle"), 'check', "get_by_role(\"treeitem\", name=\"System Forecast Base (Plan\").get_by_label(\"Press SPACE to toggle\")", )
    safe_action(page, page.locator("div:nth-child(3) > .ag-column-select-column"), 'click', "locator(\"div:nth-child(3) > .ag-column-select-column\")", )
    safe_action(page, page.get_by_role("textbox", name="Filter Columns Input"), 'click', "get_by_role(\"textbox\", name=\"Filter Columns Input\")", )
    safe_action(page, page.get_by_role("textbox", name="Filter Columns Input"), 'fill', "get_by_role(\"textbox\", name=\"Filter Columns Input\")", "")
    safe_action(page, page.get_by_role("textbox", name="Filter Columns Input"), 'press', "get_by_role(\"textbox\", name=\"Filter Columns Input\")", "Enter")
    safe_action(page, page.get_by_label("System Forecast Promotion (").get_by_text("System Forecast Promotion ("), 'click', "get_by_label(\"System Forecast Promotion (\").get_by_text(\"System Forecast Promotion (\")", )
    safe_action(page, page.get_by_label("System Forecast Total (Plan+1").get_by_text("System Forecast Total (Plan+1"), 'click', "get_by_label(\"System Forecast Total (Plan+1\").get_by_text(\"System Forecast Total (Plan+1\")", )
    safe_action(page, page.get_by_label("System Forecast Base (Plan+1").get_by_text("System Forecast Base (Plan+1"), 'click', "get_by_label(\"System Forecast Base (Plan+1\").get_by_text(\"System Forecast Base (Plan+1\")", )
    safe_action(page, page.get_by_label("System Forecast Promotion (").get_by_text("System Forecast Promotion ("), 'click', "get_by_label(\"System Forecast Promotion (\").get_by_text(\"System Forecast Promotion (\")", )
    safe_action(page, page.get_by_label("6 Week Gross Units Average").get_by_text("Week Gross Units Average"), 'click', "get_by_label(\"6 Week Gross Units Average\").get_by_text(\"Week Gross Units Average\")", )
    safe_action(page, page.get_by_label("6 Week Aged Net Units Average Column", exact=True).get_by_text("Week Aged Net Units Average"), 'click', "get_by_label(\"6 Week Aged Net Units Average Column\", exact=True).get_by_text(\"Week Aged Net Units Average\")", )
    safe_action(page, page.get_by_label("LY 6 Week Aged Net Units").get_by_text("LY 6 Week Aged Net Units"), 'click', "get_by_label(\"LY 6 Week Aged Net Units\").get_by_text(\"LY 6 Week Aged Net Units\")", )
    safe_action(page, page.get_by_label("% Change 6 Week Aged Net").get_by_text("% Change 6 Week Aged Net"), 'click', "get_by_label(\"% Change 6 Week Aged Net\").get_by_text(\"% Change 6 Week Aged Net\")", )
    safe_action(page, page.get_by_label("6 Week Scan Units Average Column", exact=True).get_by_text("Week Scan Units Average"), 'click', "get_by_label(\"6 Week Scan Units Average Column\", exact=True).get_by_text(\"Week Scan Units Average\")", )
    safe_action(page, page.get_by_label("LY 6 Week Scan Units Average").get_by_text("LY 6 Week Scan Units Average"), 'click', "get_by_label(\"LY 6 Week Scan Units Average\").get_by_text(\"LY 6 Week Scan Units Average\")", )
    safe_action(page, page.get_by_label("% Change 6 Week Scan Units").get_by_text("% Change 6 Week Scan Units"), 'click', "get_by_label(\"% Change 6 Week Scan Units\").get_by_text(\"% Change 6 Week Scan Units\")", )
    safe_action(page, page.get_by_label("Freshness (6 Week Average)").get_by_text("Freshness (6 Week Average)"), 'click', "get_by_label(\"Freshness (6 Week Average)\").get_by_text(\"Freshness (6 Week Average)\")", )
    safe_action(page, page.get_by_label("6 Week Aged Returns Units").get_by_text("6 Week Aged Returns Units"), 'click', "get_by_label(\"6 Week Aged Returns Units\").get_by_text(\"6 Week Aged Returns Units\")", )
    safe_action(page, page.locator("#ag-169").get_by_text("System Forecast Total (Plan Week)"), 'click', "locator(\"#ag-169\").get_by_text(\"System Forecast Total (Plan Week)\")", )
    safe_action(page, page.get_by_label("System Forecast Base (Plan").get_by_text("System Forecast Base (Plan"), 'click', "get_by_label(\"System Forecast Base (Plan\").get_by_text(\"System Forecast Base (Plan\")", )
    safe_action(page, page.locator("esp-card-component").filter(has_text="Customer Total columns (0)").get_by_role("button"), 'click', "locator(\"esp-card-component\").filter(has_text=\"Customer Total columns (0)\").get_by_role(\"button\")", )
    with safe_download(page) as download_info:
        safe_action(page, page.locator("esp-grid-icons-component").filter(has_text="Export").locator("#export-iconId"), 'click', "locator(\"esp-grid-icons-component\").filter(has_text=\"Export\").locator(\"#export-iconId\")", )
    download = download_info.value
    safe_action(page, page.locator(".pointer.zeb-adjustments").first, 'click', "locator(\".pointer.zeb-adjustments\").first", )
    safe_action(page, page.get_by_text("Save Preference"), 'click', "get_by_text(\"Save Preference\")", )
    safe_action(page, page.locator(".pointer.zeb-adjustments").first, 'click', "locator(\".pointer.zeb-adjustments\").first", )
    safe_action(page, page.get_by_text("Reset Preference"), 'click', "get_by_text(\"Reset Preference\")", )
    safe_action(page, page.locator(".ag-body-horizontal-scroll-container").first, 'click', "locator(\".ag-body-horizontal-scroll-container\").first", )
    safe_action(page, page.get_by_text("Customers columns (0)"), 'click', "get_by_text(\"Customers columns (0)\")", )
    safe_action(page, page.get_by_text("Customers"), 'click', "get_by_text(\"Customers\")", )
    safe_action(page, page.get_by_text("Customers columns (0)"), 'click', "get_by_text(\"Customers columns (0)\")", )
    safe_action(page, page.locator("esp-card-component").filter(has_text="Customers columns (0)").get_by_role("button"), 'click', "locator(\"esp-card-component\").filter(has_text=\"Customers columns (0)\").get_by_role(\"button\")", )
    safe_action(page, page.locator("#ag-87 > .ag-column-panel > .ag-column-select > .ag-column-select-header"), 'click', "locator(\"#ag-87 > .ag-column-panel > .ag-column-select > .ag-column-select-header\")", )
    safe_action(page, page.get_by_role("textbox", name="Filter Columns Input"), 'fill', "get_by_role(\"textbox\", name=\"Filter Columns Input\")", "Fresh")
    safe_action(page, page.get_by_role("textbox", name="Filter Columns Input"), 'press', "get_by_role(\"textbox\", name=\"Filter Columns Input\")", "Enter")
    safe_action(page, page.get_by_role("checkbox", name="Press SPACE to toggle visibility (hidden)"), 'check', "get_by_role(\"checkbox\", name=\"Press SPACE to toggle visibility (hidden)\")", )
    safe_action(page, page.get_by_role("checkbox", name="Toggle All Columns Visibility"), 'uncheck', "get_by_role(\"checkbox\", name=\"Toggle All Columns Visibility\")", )
    safe_action(page, page.get_by_role("textbox", name="Filter Columns Input"), 'click', "get_by_role(\"textbox\", name=\"Filter Columns Input\")", )
    safe_action(page, page.get_by_role("textbox", name="Filter Columns Input"), 'fill', "get_by_role(\"textbox\", name=\"Filter Columns Input\")", "")
    safe_action(page, page.get_by_role("textbox", name="Filter Columns Input"), 'press', "get_by_role(\"textbox\", name=\"Filter Columns Input\")", "Enter")
    safe_action(page, page.locator("#ag-87").get_by_text("System Forecast Total (Plan Week)"), 'click', "locator(\"#ag-87\").get_by_text(\"System Forecast Total (Plan Week)\")", )
    safe_action(page, page.get_by_label("System Forecast Base (Plan Week) Column").get_by_text("System Forecast Base (Plan"), 'click', "get_by_label(\"System Forecast Base (Plan Week) Column\").get_by_text(\"System Forecast Base (Plan\")", )
    safe_action(page, page.get_by_label("System Forecast Promotion (Plan Week) Column").get_by_text("System Forecast Promotion ("), 'click', "get_by_label(\"System Forecast Promotion (Plan Week) Column\").get_by_text(\"System Forecast Promotion (\")", )
    safe_action(page, page.get_by_label("System Forecast Total (Plan+1").get_by_text("System Forecast Total (Plan+1"), 'click', "get_by_label(\"System Forecast Total (Plan+1\").get_by_text(\"System Forecast Total (Plan+1\")", )
    safe_action(page, page.get_by_label("System Forecast Base (Plan+1").get_by_text("System Forecast Base (Plan+1"), 'click', "get_by_label(\"System Forecast Base (Plan+1\").get_by_text(\"System Forecast Base (Plan+1\")", )
    safe_action(page, page.get_by_label("System Forecast Promotion (Plan+1 Week) Column").get_by_text("System Forecast Promotion ("), 'click', "get_by_label(\"System Forecast Promotion (Plan+1 Week) Column\").get_by_text(\"System Forecast Promotion (\")", )
    safe_action(page, page.get_by_label("6 Week Gross Units Average").get_by_text("Week Gross Units Average"), 'click', "get_by_label(\"6 Week Gross Units Average\").get_by_text(\"Week Gross Units Average\")", )
    safe_action(page, page.get_by_label("6 Week Aged Net Units Average Column", exact=True).get_by_text("6 Week Aged Net Units Average", exact=True), 'click', "get_by_label(\"6 Week Aged Net Units Average Column\", exact=True).get_by_text(\"6 Week Aged Net Units Average\", exact=True)", )
    safe_action(page, page.get_by_label("LY 6 Week Aged Net Units").get_by_text("LY 6 Week Aged Net Units"), 'click', "get_by_label(\"LY 6 Week Aged Net Units\").get_by_text(\"LY 6 Week Aged Net Units\")", )
    safe_action(page, page.get_by_label("% Change 6 Week Aged Net").get_by_text("% Change 6 Week Aged Net"), 'click', "get_by_label(\"% Change 6 Week Aged Net\").get_by_text(\"% Change 6 Week Aged Net\")", )
    safe_action(page, page.get_by_label("LY 6 Week Scan Units Average").get_by_text("LY 6 Week Scan Units Average"), 'click', "get_by_label(\"LY 6 Week Scan Units Average\").get_by_text(\"LY 6 Week Scan Units Average\")", )
    safe_action(page, page.get_by_label("6 Week Scan Units Average Column", exact=True).get_by_text("Week Scan Units Average"), 'click', "get_by_label(\"6 Week Scan Units Average Column\", exact=True).get_by_text(\"Week Scan Units Average\")", )
    safe_action(page, page.get_by_label("% Change 6 Week Scan Units").get_by_text("% Change 6 Week Scan Units"), 'click', "get_by_label(\"% Change 6 Week Scan Units\").get_by_text(\"% Change 6 Week Scan Units\")", )
    safe_action(page, page.get_by_label("Freshness (6 Week Average)").get_by_text("Freshness (6 Week Average)"), 'click', "get_by_label(\"Freshness (6 Week Average)\").get_by_text(\"Freshness (6 Week Average)\")", )
    safe_action(page, page.get_by_label("6 Week Aged Returns Units").get_by_text("6 Week Aged Returns Units"), 'click', "get_by_label(\"6 Week Aged Returns Units\").get_by_text(\"6 Week Aged Returns Units\")", )
    safe_action(page, page.locator("esp-card-component").filter(has_text="Customers columns (0)").get_by_role("button"), 'click', "locator(\"esp-card-component\").filter(has_text=\"Customers columns (0)\").get_by_role(\"button\")", )
    with safe_download(page) as download1_info:
        safe_action(page, page.locator("div:nth-child(2) > #export-iconId > .icon-color-toolbar-active"), 'click', "locator(\"div:nth-child(2) > #export-iconId > .icon-color-toolbar-active\")", )
    download1 = download1_info.value
    safe_action(page, page.locator("div:nth-child(3) > #preference-iconId > .legend-font > .multiselect-dropdown > .pointer"), 'click', "locator(\"div:nth-child(3) > #preference-iconId > .legend-font > .multiselect-dropdown > .pointer\")", )
    safe_action(page, page.get_by_text("Save Preference"), 'click', "get_by_text(\"Save Preference\")", )
    safe_action(page, page.locator("div:nth-child(3) > #preference-iconId > .legend-font > .multiselect-dropdown > .pointer"), 'click', "locator(\"div:nth-child(3) > #preference-iconId > .legend-font > .multiselect-dropdown > .pointer\")", )
    safe_action(page, page.get_by_text("Reset Preference"), 'click', "get_by_text(\"Reset Preference\")", )
    safe_action(page, page.locator("esp-row-dimentional-grid").get_by_text("Customer"), 'click', "locator(\"esp-row-dimentional-grid\").get_by_text(\"Customer\")", )
    safe_action(page, page.locator(".ag-icon.ag-icon-desc").first, 'click', "locator(\".ag-icon.ag-icon-desc\").first", )
    safe_action(page, page.locator(".ag-icon.ag-icon-desc").first, 'click', "locator(\".ag-icon.ag-icon-desc\").first", )
    safe_action(page, page.locator(".ag-filter-body-wrapper"), 'click', "locator(\".ag-filter-body-wrapper\")", )
    safe_action(page, page.get_by_text("Contains"), 'click', "get_by_text(\"Contains\")", )
    safe_action(page, page.get_by_label("Select Field").get_by_text("Contains"), 'click', "get_by_label(\"Select Field\").get_by_text(\"Contains\")", )
    safe_action(page, page.get_by_text("Contains"), 'click', "get_by_text(\"Contains\")", )
    safe_action(page, page.get_by_text("Does not contain"), 'click', "get_by_text(\"Does not contain\")", )
    safe_action(page, page.get_by_text("Does not contain"), 'click', "get_by_text(\"Does not contain\")", )
    safe_action(page, page.get_by_role("option", name="Equals"), 'click', "get_by_role(\"option\", name=\"Equals\")", )
    safe_action(page, page.get_by_text("Equals"), 'click', "get_by_text(\"Equals\")", )
    safe_action(page, page.get_by_role("option", name="Does not equal"), 'click', "get_by_role(\"option\", name=\"Does not equal\")", )
    safe_action(page, page.get_by_text("Does not equal"), 'click', "get_by_text(\"Does not equal\")", )
    safe_action(page, page.get_by_role("option", name="Begins with"), 'click', "get_by_role(\"option\", name=\"Begins with\")", )
    safe_action(page, page.get_by_role("combobox", name="Filtering operator"), 'click', "get_by_role(\"combobox\", name=\"Filtering operator\")", )
    safe_action(page, page.get_by_role("option", name="Ends with"), 'click', "get_by_role(\"option\", name=\"Ends with\")", )
    safe_action(page, page.get_by_text("Ends with"), 'click', "get_by_text(\"Ends with\")", )
    safe_action(page, page.get_by_role("option", name="Blank", exact=True), 'click', "get_by_role(\"option\", name=\"Blank\", exact=True)", )
    safe_action(page, page.get_by_text("Blank"), 'click', "get_by_text(\"Blank\")", )
    safe_action(page, page.get_by_role("option", name="Not blank"), 'click', "get_by_role(\"option\", name=\"Not blank\")", )
    safe_action(page, page.get_by_text("AND", exact=True), 'click', "get_by_text(\"AND\", exact=True)", )
    safe_action(page, page.get_by_text("OR", exact=True), 'click', "get_by_text(\"OR\", exact=True)", )
    safe_action(page, page.get_by_text("Contains"), 'click', "get_by_text(\"Contains\")", )
    safe_action(page, page.get_by_label("Column Filter").get_by_text("Contains"), 'click', "get_by_label(\"Column Filter\").get_by_text(\"Contains\")", )
    safe_action(page, page.get_by_role("textbox", name="Filter Value"), 'click', "get_by_role(\"textbox\", name=\"Filter Value\")", )
    safe_action(page, page.get_by_role("button", name="Clear"), 'click', "get_by_role(\"button\", name=\"Clear\")", )
    safe_action(page, page.get_by_role("button", name="Reset"), 'click', "get_by_role(\"button\", name=\"Reset\")", )
    safe_action(page, page.locator(".ag-header-icon.ag-header-cell-filter-button > .ag-icon").first, 'click', "locator(\".ag-header-icon.ag-header-cell-filter-button > .ag-icon\").first", )
    safe_action(page, page.get_by_role("button", name="Apply"), 'click', "get_by_role(\"button\", name=\"Apply\")", )
    safe_action(page, page.locator("span").filter(has_text="3RD PARTY DISTRIB").first, 'click', "locator(\"span\").filter(has_text=\"3RD PARTY DISTRIB\").first", )
    safe_action(page, page.get_by_text("3RD PARTY DISTRIB"), 'click', "get_by_text(\"3RD PARTY DISTRIB\")", )
    safe_action(page, page.locator(".ag-group-checkbox").first, 'click', "locator(\".ag-group-checkbox\").first", )
    safe_action(page, page.get_by_role("gridcell", name="Press Space to toggle row selection (unchecked)  99 CENT").get_by_label("Press Space to toggle row"), 'check', "get_by_role(\"gridcell\", name=\"Press Space to toggle row selection (unchecked)  99 CENT\").get_by_label(\"Press Space to toggle row\")", )
    safe_action(page, page.get_by_text("System Forecast Total (Plan").nth(2), 'click', "get_by_text(\"System Forecast Total (Plan\").nth(2)", )
    safe_action(page, page.locator(".ag-cell-label-container.ag-header-cell-sorted-desc > .ag-header-icon > .ag-icon"), 'click', "locator(\".ag-cell-label-container.ag-header-cell-sorted-desc > .ag-header-icon > .ag-icon\")", )
    safe_action(page, page.locator(".ag-filter-body-wrapper"), 'click', "locator(\".ag-filter-body-wrapper\")", )
    safe_action(page, page.get_by_text("Equals"), 'click', "get_by_text(\"Equals\")", )
    safe_action(page, page.get_by_label("Select Field").get_by_text("Equals"), 'click', "get_by_label(\"Select Field\").get_by_text(\"Equals\")", )
    safe_action(page, page.get_by_text("Equals"), 'click', "get_by_text(\"Equals\")", )
    safe_action(page, page.get_by_text("Does not equal"), 'click', "get_by_text(\"Does not equal\")", )
    safe_action(page, page.get_by_text("Does not equal"), 'click', "get_by_text(\"Does not equal\")", )
    safe_action(page, page.get_by_text("Greater than", exact=True), 'click', "get_by_text(\"Greater than\", exact=True)", )
    safe_action(page, page.get_by_text("Greater than"), 'click', "get_by_text(\"Greater than\")", )
    safe_action(page, page.get_by_text("Greater than or equal to"), 'click', "get_by_text(\"Greater than or equal to\")", )
    safe_action(page, page.get_by_text("Greater than or equal to"), 'click', "get_by_text(\"Greater than or equal to\")", )
    safe_action(page, page.get_by_role("option", name="Less than", exact=True), 'click', "get_by_role(\"option\", name=\"Less than\", exact=True)", )
    safe_action(page, page.get_by_text("Less than"), 'click', "get_by_text(\"Less than\")", )
    safe_action(page, page.get_by_text("Less than or equal to"), 'click', "get_by_text(\"Less than or equal to\")", )
    safe_action(page, page.get_by_text("Less than or equal to"), 'click', "get_by_text(\"Less than or equal to\")", )
    safe_action(page, page.get_by_role("option", name="Between"), 'click', "get_by_role(\"option\", name=\"Between\")", )
    safe_action(page, page.get_by_text("Between"), 'click', "get_by_text(\"Between\")", )
    safe_action(page, page.get_by_role("option", name="Blank", exact=True), 'click', "get_by_role(\"option\", name=\"Blank\", exact=True)", )
    safe_action(page, page.get_by_text("Blank"), 'click', "get_by_text(\"Blank\")", )
    safe_action(page, page.get_by_role("option", name="Not blank"), 'click', "get_by_role(\"option\", name=\"Not blank\")", )
    safe_action(page, page.get_by_role("button", name="Clear"), 'click', "get_by_role(\"button\", name=\"Clear\")", )
    safe_action(page, page.get_by_role("button", name="Reset"), 'click', "get_by_role(\"button\", name=\"Reset\")", )
    safe_action(page, page.locator(".ag-cell-label-container.ag-header-cell-sorted-desc > .ag-header-icon > .ag-icon"), 'click', "locator(\".ag-cell-label-container.ag-header-cell-sorted-desc > .ag-header-icon > .ag-icon\")", )
    safe_action(page, page.get_by_role("button", name="Apply"), 'click', "get_by_role(\"button\", name=\"Apply\")", )
    safe_action(page, page.locator(".ag-cell-label-container.ag-header-cell-sorted-desc > .ag-header-cell-label > .ag-sort-indicator-container > .ag-sort-indicator-icon.ag-sort-descending-icon > .ag-icon"), 'click', "locator(\".ag-cell-label-container.ag-header-cell-sorted-desc > .ag-header-cell-label > .ag-sort-indicator-container > .ag-sort-indicator-icon.ag-sort-descending-icon > .ag-icon\")", )
    safe_action(page, page.locator(".ag-cell-label-container.ag-header-cell-sorted-asc > .ag-header-cell-label > .ag-sort-indicator-container > .ag-sort-indicator-icon.ag-sort-ascending-icon > .ag-icon"), 'click', "locator(\".ag-cell-label-container.ag-header-cell-sorted-asc > .ag-header-cell-label > .ag-sort-indicator-container > .ag-sort-indicator-icon.ag-sort-ascending-icon > .ag-icon\")", )
    safe_action(page, page.get_by_text("System Forecast Base (Plan Week)"), 'click', "get_by_text(\"System Forecast Base (Plan Week)\")", )
    safe_action(page, page.locator(".ag-cell-label-container.ag-header-cell-sorted-desc > .ag-header-cell-label > .ag-sort-indicator-container > .ag-sort-indicator-icon.ag-sort-descending-icon > .ag-icon"), 'click', "locator(\".ag-cell-label-container.ag-header-cell-sorted-desc > .ag-header-cell-label > .ag-sort-indicator-container > .ag-sort-indicator-icon.ag-sort-descending-icon > .ag-icon\")", )
    safe_action(page, page.locator(".ag-cell-label-container.ag-header-cell-sorted-desc > .ag-header-cell-label > .ag-sort-indicator-container > .ag-sort-indicator-icon.ag-sort-descending-icon > .ag-icon"), 'click', "locator(\".ag-cell-label-container.ag-header-cell-sorted-desc > .ag-header-cell-label > .ag-sort-indicator-container > .ag-sort-indicator-icon.ag-sort-descending-icon > .ag-icon\")", )
    safe_action(page, page.locator(".ag-header-icon.ag-header-cell-filter-button.ag-has-popup-positioned-under > .ag-icon"), 'click', "locator(\".ag-header-icon.ag-header-cell-filter-button.ag-has-popup-positioned-under > .ag-icon\")", )
    safe_action(page, page.locator(".ag-filter-body-wrapper"), 'click', "locator(\".ag-filter-body-wrapper\")", )
    safe_action(page, page.get_by_role("combobox", name="Filtering operator"), 'click', "get_by_role(\"combobox\", name=\"Filtering operator\")", )
    safe_action(page, page.get_by_label("Select Field").get_by_text("Equals"), 'click', "get_by_label(\"Select Field\").get_by_text(\"Equals\")", )
    safe_action(page, page.get_by_text("Equals"), 'click', "get_by_text(\"Equals\")", )
    safe_action(page, page.get_by_text("Does not equal"), 'click', "get_by_text(\"Does not equal\")", )
    safe_action(page, page.get_by_text("Does not equal"), 'click', "get_by_text(\"Does not equal\")", )
    safe_action(page, page.get_by_role("option", name="Greater than", exact=True), 'click', "get_by_role(\"option\", name=\"Greater than\", exact=True)", )
    safe_action(page, page.get_by_text("Greater than"), 'click', "get_by_text(\"Greater than\")", )
    safe_action(page, page.get_by_role("option", name="Less than", exact=True), 'click', "get_by_role(\"option\", name=\"Less than\", exact=True)", )
    safe_action(page, page.get_by_text("Less than"), 'click', "get_by_text(\"Less than\")", )
    safe_action(page, page.get_by_text("Greater than or equal to"), 'click', "get_by_text(\"Greater than or equal to\")", )
    safe_action(page, page.get_by_text("Greater than or equal to"), 'click', "get_by_text(\"Greater than or equal to\")", )
    safe_action(page, page.get_by_role("option", name="Less than or equal to"), 'click', "get_by_role(\"option\", name=\"Less than or equal to\")", )
    safe_action(page, page.get_by_text("Less than or equal to"), 'click', "get_by_text(\"Less than or equal to\")", )
    safe_action(page, page.get_by_role("option", name="Between"), 'click', "get_by_role(\"option\", name=\"Between\")", )
    safe_action(page, page.get_by_text("Between"), 'click', "get_by_text(\"Between\")", )
    safe_action(page, page.get_by_role("option", name="Blank", exact=True), 'click', "get_by_role(\"option\", name=\"Blank\", exact=True)", )
    safe_action(page, page.get_by_text("Blank"), 'click', "get_by_text(\"Blank\")", )
    safe_action(page, page.get_by_role("option", name="Not blank"), 'click', "get_by_role(\"option\", name=\"Not blank\")", )
    safe_action(page, page.locator(".ag-labeled.ag-label-align-right.ag-radio-button").first, 'click', "locator(\".ag-labeled.ag-label-align-right.ag-radio-button\").first", )
    safe_action(page, page.locator(".ag-labeled.ag-label-align-right.ag-radio-button.ag-input-field.ag-filter-condition-operator.ag-filter-condition-operator-or"), 'click', "locator(\".ag-labeled.ag-label-align-right.ag-radio-button.ag-input-field.ag-filter-condition-operator.ag-filter-condition-operator-or\")", )
    safe_action(page, page.get_by_role("spinbutton", name="Filter Value"), 'click', "get_by_role(\"spinbutton\", name=\"Filter Value\")", )
    safe_action(page, page.get_by_role("spinbutton", name="Filter Value"), 'fill', "get_by_role(\"spinbutton\", name=\"Filter Value\")", "2")
    safe_action(page, page.get_by_role("spinbutton", name="Filter Value"), 'press', "get_by_role(\"spinbutton\", name=\"Filter Value\")", "Enter")
    safe_action(page, page.get_by_role("spinbutton", name="Filter Value"), 'click', "get_by_role(\"spinbutton\", name=\"Filter Value\")", )
    safe_action(page, page.get_by_role("button", name="Apply"), 'click', "get_by_role(\"button\", name=\"Apply\")", )
    safe_action(page, page.locator(".ag-header-icon.ag-header-cell-filter-button.ag-filter-active > .ag-icon"), 'click', "locator(\".ag-header-icon.ag-header-cell-filter-button.ag-filter-active > .ag-icon\")", )
    safe_action(page, page.get_by_role("button", name="Reset"), 'click', "get_by_role(\"button\", name=\"Reset\")", )
    safe_action(page, page.locator(".ag-header-cell.ag-header-parent-hidden.ag-header-cell-sortable.ag-header-background.ag-focus-managed.ag-header-active > .ag-header-cell-comp-wrapper > .ag-cell-label-container > .ag-header-icon > .ag-icon"), 'click', "locator(\".ag-header-cell.ag-header-parent-hidden.ag-header-cell-sortable.ag-header-background.ag-focus-managed.ag-header-active > .ag-header-cell-comp-wrapper > .ag-cell-label-container > .ag-header-icon > .ag-icon\")", )
    safe_action(page, page.get_by_role("button", name="Clear"), 'click', "get_by_role(\"button\", name=\"Clear\")", )
    safe_action(page, page.get_by_text("Customers columns (0)"), 'click', "get_by_text(\"Customers columns (0)\")", )
    safe_action(page, page.locator("esp-row-dimentional-grid #paginationId"), 'click', "locator(\"esp-row-dimentional-grid #paginationId\")", )
    safe_action(page, page.get_by_text("Showing 10 out of"), 'click', "get_by_text(\"Showing 10 out of\")", )
    safe_action(page, page.get_by_text("Showing 10 out of 138 12345"), 'click', "get_by_text(\"Showing 10 out of 138 12345\")", )
    safe_action(page, page.get_by_text("View 10 row(s)").first, 'click', "get_by_text(\"View 10 row(s)\").first", )
    safe_action(page, page.locator("span").filter(has_text=re.compile(r"^View 10 row\(s\)$")), 'click', "locator(\"span\").filter(has_text=re.compile(r\"^View 10 row\\(s\\)$\"))", )
    safe_action(page, page.get_by_text("Rows per page"), 'click', "get_by_text(\"Rows per page\")", )
    safe_action(page, page.get_by_text("Showing 10 out of 138 12345"), 'click', "get_by_text(\"Showing 10 out of 138 12345\")", )
    safe_action(page, page.get_by_role("listitem").filter(has_text=re.compile(r"^1$")), 'click', "get_by_role(\"listitem\").filter(has_text=re.compile(r\"^1$\"))", )
    safe_action(page, page.locator("a").filter(has_text="2"), 'click', "locator(\"a\").filter(has_text=\"2\")", )
    safe_action(page, page.locator(".zeb-chevron-left"), 'click', "locator(\".zeb-chevron-left\")", )
    safe_action(page, page.get_by_text("12345...14"), 'click', "get_by_text(\"12345...14\")", )
    safe_action(page, page.get_by_text("12345...14"), 'click', "get_by_text(\"12345...14\")", )
    safe_action(page, page.locator(".pagination-next > .zeb-chevron-right"), 'click', "locator(\".pagination-next > .zeb-chevron-right\")", )
    safe_action(page, page.locator(".zeb-nav-to-last"), 'click', "locator(\".zeb-nav-to-last\")", )
    safe_action(page, page.locator(".w-100.p-h-16"), 'click', "locator(\".w-100.p-h-16\")", )
    safe_action(page, page.locator("div").filter(has_text=re.compile(r"^View 20 row\(s\)$")).first, 'click', "locator(\"div\").filter(has_text=re.compile(r\"^View 20 row\\(s\\)$\")).first", )
    safe_action(page, page.get_by_text("Showing 20 out of"), 'click', "get_by_text(\"Showing 20 out of\")", )
    safe_action(page, page.get_by_role("gridcell", name="Press Space to toggle row selection (unchecked)  3RD PARTY DISTRIB").get_by_label("Press Space to toggle row"), 'check', "get_by_role(\"gridcell\", name=\"Press Space to toggle row selection (unchecked)  3RD PARTY DISTRIB\").get_by_label(\"Press Space to toggle row\")", )
    safe_action(page, page.get_by_text("FilterTime Latest Order &"), 'click', "get_by_text(\"FilterTime Latest Order &\")", )
    safe_action(page, page.locator("div").filter(has_text=re.compile(r"^Filter$")), 'click', "locator(\"div\").filter(has_text=re.compile(r\"^Filter$\"))", )
    safe_action(page, page.get_by_text("Time"), 'click', "get_by_text(\"Time\")", )
    safe_action(page, page.locator(".w-100.p-h-16.p-v-8.dropdown-label.background-white"), 'click', "locator(\".w-100.p-h-16.p-v-8.dropdown-label.background-white\")", )
    safe_action(page, page.locator("span").filter(has_text="Latest Order & Plan Week"), 'click', "locator(\"span\").filter(has_text=\"Latest Order & Plan Week\")", )
    safe_action(page, page.get_by_text("FilterTime Latest Order &"), 'click', "get_by_text(\"FilterTime Latest Order &\")", )
    safe_action(page, page.get_by_text("Daily Summary Customer:3RD"), 'click', "get_by_text(\"Daily Summary Customer:3RD\")", )
    safe_action(page, page.get_by_text("Daily Summary"), 'click', "get_by_text(\"Daily Summary\")", )
    safe_action(page, page.get_by_text("Customer", exact=True).nth(2), 'click', "get_by_text(\"Customer\", exact=True).nth(2)", )
    safe_action(page, page.get_by_text("Customer:3RD PARTY DISTRIB").first, 'click', "get_by_text(\"Customer:3RD PARTY DISTRIB\").first", )
    safe_action(page, page.get_by_text("3RD PARTY DISTRIB").nth(1), 'click', "get_by_text(\"3RD PARTY DISTRIB\").nth(1)", )
    safe_action(page, page.locator(".wr-20.font-weight-normal > esp-multiselect-dropdown > .multiselect-dropdown > div > .w-100"), 'click', "locator(\".wr-20.font-weight-normal > esp-multiselect-dropdown > .multiselect-dropdown > div > .w-100\")", )
    safe_action(page, page.locator(".d-flex.dropdown-option").first, 'click', "locator(\".d-flex.dropdown-option\").first", )
    safe_action(page, page.locator(".d-flex.dropdown-option").first, 'click', "locator(\".d-flex.dropdown-option\").first", )
    safe_action(page, page.locator(".d-flex.dropdown-option.align-items-center.p-v-5.p-l-32 > .d-flex").first, 'click', "locator(\".d-flex.dropdown-option.align-items-center.p-v-5.p-l-32 > .d-flex\").first", )
    safe_action(page, page.locator(".d-flex.flex-column.justify-content-center.font-size-10.align-items-center.checkbox-v2.m-r-10.zeb-check").first, 'click', "locator(\".d-flex.flex-column.justify-content-center.font-size-10.align-items-center.checkbox-v2.m-r-10.zeb-check\").first", )
    safe_action(page, page.locator(".d-flex.flex-column.justify-content-center.font-size-10.align-items-center.checkbox-v2.m-r-10.zeb-check").first, 'click', "locator(\".d-flex.flex-column.justify-content-center.font-size-10.align-items-center.checkbox-v2.m-r-10.zeb-check\").first", )
    safe_action(page, page.locator(".d-flex.flex-column.justify-content-center.font-size-10.align-items-center.checkbox-v2.m-r-10.zeb-check").first, 'click', "locator(\".d-flex.flex-column.justify-content-center.font-size-10.align-items-center.checkbox-v2.m-r-10.zeb-check\").first", )
    safe_action(page, page.locator(".d-flex.flex-column.justify-content-center.font-size-10.align-items-center.checkbox-v2.m-r-10.zeb-check").first, 'click', "locator(\".d-flex.flex-column.justify-content-center.font-size-10.align-items-center.checkbox-v2.m-r-10.zeb-check\").first", )
    safe_action(page, page.locator(".d-flex.flex-column.justify-content-center.font-size-10.align-items-center.checkbox-v2.m-r-10.zeb-check").first, 'click', "locator(\".d-flex.flex-column.justify-content-center.font-size-10.align-items-center.checkbox-v2.m-r-10.zeb-check\").first", )
    safe_action(page, page.locator(".d-flex.flex-column.justify-content-center.font-size-10.align-items-center.checkbox-v2.m-r-10.zeb-check").first, 'click', "locator(\".d-flex.flex-column.justify-content-center.font-size-10.align-items-center.checkbox-v2.m-r-10.zeb-check\").first", )
    safe_action(page, page.locator(".d-flex.flex-column.justify-content-center.font-size-10.align-items-center.checkbox-v2.m-r-10.zeb-check").first, 'click', "locator(\".d-flex.flex-column.justify-content-center.font-size-10.align-items-center.checkbox-v2.m-r-10.zeb-check\").first", )
    safe_action(page, page.locator(".d-flex.flex-column.justify-content-center.font-size-10.align-items-center.checkbox-v2.m-r-10.zeb-check").first, 'click', "locator(\".d-flex.flex-column.justify-content-center.font-size-10.align-items-center.checkbox-v2.m-r-10.zeb-check\").first", )
    safe_action(page, page.locator(".d-flex.flex-column.justify-content-center.font-size-10.align-items-center.checkbox-v2.m-r-10.zeb-check").first, 'click', "locator(\".d-flex.flex-column.justify-content-center.font-size-10.align-items-center.checkbox-v2.m-r-10.zeb-check\").first", )
    safe_action(page, page.locator(".d-flex.flex-column.justify-content-center.font-size-10.align-items-center.checkbox-v2.m-r-10.zeb-check").first, 'click', "locator(\".d-flex.flex-column.justify-content-center.font-size-10.align-items-center.checkbox-v2.m-r-10.zeb-check\").first", )
    safe_action(page, page.locator(".d-flex.flex-column.justify-content-center.font-size-10.align-items-center.checkbox-v2.m-r-10.zeb-check").first, 'click', "locator(\".d-flex.flex-column.justify-content-center.font-size-10.align-items-center.checkbox-v2.m-r-10.zeb-check\").first", )
    safe_action(page, page.locator(".d-flex.flex-column.justify-content-center.font-size-10.align-items-center.checkbox-v2.m-r-10.zeb-check").first, 'click', "locator(\".d-flex.flex-column.justify-content-center.font-size-10.align-items-center.checkbox-v2.m-r-10.zeb-check\").first", )
    safe_action(page, page.locator(".d-flex.flex-column.justify-content-center.font-size-10.align-items-center.checkbox-v2.m-r-10.zeb-check").first, 'click', "locator(\".d-flex.flex-column.justify-content-center.font-size-10.align-items-center.checkbox-v2.m-r-10.zeb-check\").first", )
    safe_action(page, page.locator(".d-flex.dropdown-option.align-items-center.p-v-5.p-l-32.p-r-16.selected").first, 'click', "locator(\".d-flex.dropdown-option.align-items-center.p-v-5.p-l-32.p-r-16.selected\").first", )
    safe_action(page, page.get_by_text("Aged Net Units (CW-5)", exact=True), 'click', "get_by_text(\"Aged Net Units (CW-5)\", exact=True)", )
    safe_action(page, page.get_by_text("Aged Net Units (CW-6)", exact=True), 'click', "get_by_text(\"Aged Net Units (CW-6)\", exact=True)", )
    safe_action(page, page.get_by_text("Scan Units (CW-4)", exact=True), 'click', "get_by_text(\"Scan Units (CW-4)\", exact=True)", )
    safe_action(page, page.get_by_text("Scan Units (CW-3)").nth(1), 'click', "get_by_text(\"Scan Units (CW-3)\").nth(1)", )
    safe_action(page, page.get_by_text("Scan Units (CW-5)", exact=True), 'click', "get_by_text(\"Scan Units (CW-5)\", exact=True)", )
    safe_action(page, page.locator("span").filter(has_text="Scan Units (CW-6)"), 'click', "locator(\"span\").filter(has_text=\"Scan Units (CW-6)\")", )
    safe_action(page, page.get_by_text("Daily Summary Customer:3RD"), 'click', "get_by_text(\"Daily Summary Customer:3RD\")", )
    safe_action(page, page.locator("esp-card-component").filter(has_text="Daily Summary Customer:3RD").get_by_role("button"), 'click', "locator(\"esp-card-component\").filter(has_text=\"Daily Summary Customer:3RD\").get_by_role(\"button\")", )
    safe_action(page, page.get_by_role("textbox", name="Filter Columns Input"), 'click', "get_by_role(\"textbox\", name=\"Filter Columns Input\")", )
    safe_action(page, page.get_by_role("checkbox", name="Toggle All Columns Visibility"), 'uncheck', "get_by_role(\"checkbox\", name=\"Toggle All Columns Visibility\")", )
    safe_action(page, page.get_by_role("checkbox", name="Toggle All Columns Visibility"), 'check', "get_by_role(\"checkbox\", name=\"Toggle All Columns Visibility\")", )
    safe_action(page, page.get_by_label("/01(Sun) Column").get_by_text("/01(Sun)"), 'click', "get_by_label(\"/01(Sun) Column\").get_by_text(\"/01(Sun)\")", )
    safe_action(page, page.get_by_label("/02(Mon) Column").get_by_text("/02(Mon)"), 'click', "get_by_label(\"/02(Mon) Column\").get_by_text(\"/02(Mon)\")", )
    safe_action(page, page.get_by_role("treeitem", name="/03(Tue) Column").get_by_label("Press SPACE to toggle visibility (visible)"), 'uncheck', "get_by_role(\"treeitem\", name=\"/03(Tue) Column\").get_by_label(\"Press SPACE to toggle visibility (visible)\")", )
    safe_action(page, page.get_by_role("treeitem", name="/05(Thu) Column").get_by_label("Press SPACE to toggle visibility (visible)"), 'uncheck', "get_by_role(\"treeitem\", name=\"/05(Thu) Column\").get_by_label(\"Press SPACE to toggle visibility (visible)\")", )
    safe_action(page, page.get_by_role("treeitem", name="/04(Wed) Column").get_by_label("Press SPACE to toggle visibility (visible)"), 'uncheck', "get_by_role(\"treeitem\", name=\"/04(Wed) Column\").get_by_label(\"Press SPACE to toggle visibility (visible)\")", )
    with safe_download(page) as download2_info:
        safe_action(page, page.locator("span:nth-child(6) > esp-grid-icons-component > .display-grid-icons > div:nth-child(2) > #export-iconId > .icon-color-toolbar-active"), 'click', "locator(\"span:nth-child(6) > esp-grid-icons-component > .display-grid-icons > div:nth-child(2) > #export-iconId > .icon-color-toolbar-active\")", )
    download2 = download2_info.value
    safe_action(page, page.locator("span:nth-child(6) > esp-grid-icons-component > .display-grid-icons > div:nth-child(3) > #preference-iconId > .legend-font > .multiselect-dropdown > .pointer"), 'click', "locator(\"span:nth-child(6) > esp-grid-icons-component > .display-grid-icons > div:nth-child(3) > #preference-iconId > .legend-font > .multiselect-dropdown > .pointer\")", )
    safe_action(page, page.get_by_text("Save Preference"), 'click', "get_by_text(\"Save Preference\")", )
    safe_action(page, page.locator("span:nth-child(6) > esp-grid-icons-component > .display-grid-icons > div:nth-child(3) > #preference-iconId > .legend-font > .multiselect-dropdown > .pointer"), 'click', "locator(\"span:nth-child(6) > esp-grid-icons-component > .display-grid-icons > div:nth-child(3) > #preference-iconId > .legend-font > .multiselect-dropdown > .pointer\")", )
    safe_action(page, page.get_by_text("Reset Preference"), 'click', "get_by_text(\"Reset Preference\")", )
    safe_action(page, page.locator("span:nth-child(6) > esp-grid-icons-component > .display-grid-icons > div:nth-child(3) > #preference-iconId > .legend-font > .multiselect-dropdown > .pointer"), 'click', "locator(\"span:nth-child(6) > esp-grid-icons-component > .display-grid-icons > div:nth-child(3) > #preference-iconId > .legend-font > .multiselect-dropdown > .pointer\")", )
    safe_action(page, page.locator("esp-card-component").filter(has_text="Daily Summary Customer:3RD").get_by_role("button"), 'click', "locator(\"esp-card-component\").filter(has_text=\"Daily Summary Customer:3RD\").get_by_role(\"button\")", )
    safe_action(page, page.locator(".wr-20.font-weight-normal > esp-multiselect-dropdown > .multiselect-dropdown > div > .w-100"), 'click', "locator(\".wr-20.font-weight-normal > esp-multiselect-dropdown > .multiselect-dropdown > div > .w-100\")", )
    safe_action(page, page.get_by_text("Select All"), 'click', "get_by_text(\"Select All\")", )
    safe_action(page, page.get_by_text("Daily Summary Customer:3RD"), 'click', "get_by_text(\"Daily Summary Customer:3RD\")", )
    safe_action(page, page.locator(".ag-header-cell.ag-column-first.ag-header-parent-hidden.ag-header-background.ag-focus-managed.ag-header-active > .ag-header-cell-comp-wrapper > .ag-cell-label-container > .ag-header-cell-label"), 'click', "locator(\".ag-header-cell.ag-column-first.ag-header-parent-hidden.ag-header-background.ag-focus-managed.ag-header-active > .ag-header-cell-comp-wrapper > .ag-cell-label-container > .ag-header-cell-label\")", )
    safe_action(page, page.get_by_text("User Suggested Order Total"), 'click', "get_by_text(\"User Suggested Order Total\")", )
    safe_action(page, page.locator("i").first, 'click', "locator(\"i\").first", )
    safe_action(page, page.get_by_text("User Override Total"), 'click', "get_by_text(\"User Override Total\")", )
    safe_action(page, page.locator("i").nth(2), 'click', "locator(\"i\").nth(2)", )
    safe_action(page, page.locator("esp-column-dimentional-grid").get_by_text("Gross Units (CW-3)"), 'click', "locator(\"esp-column-dimentional-grid\").get_by_text(\"Gross Units (CW-3)\")", )
    safe_action(page, page.locator("span").filter(has_text="Gross Units (CW-3)").first, 'click', "locator(\"span\").filter(has_text=\"Gross Units (CW-3)\").first", )
    safe_action(page, page.locator("i").nth(5), 'click', "locator(\"i\").nth(5)", )
    safe_action(page, page.locator("esp-column-dimentional-grid").get_by_text("Aged Net Units (CW-3)"), 'click', "locator(\"esp-column-dimentional-grid\").get_by_text(\"Aged Net Units (CW-3)\")", )
    safe_action(page, page.locator(".ag-cell-value.ag-cell.ag-cell-not-inline-editing.ag-cell-normal-height.ag-cell-last-left-pinned.ag-column-first.ag-cell-override-normal.notosans-overwrite.no-border.ag-cell-focus > .ag-cell-wrapper > .ag-group-contracted > .zeb-chevron-right"), 'click', "locator(\".ag-cell-value.ag-cell.ag-cell-not-inline-editing.ag-cell-normal-height.ag-cell-last-left-pinned.ag-column-first.ag-cell-override-normal.notosans-overwrite.no-border.ag-cell-focus > .ag-cell-wrapper > .ag-group-contracted > .zeb-chevron-right\")", )
    safe_action(page, page.locator(".ag-row-no-focus.ag-row-not-inline-editing.ag-row.ag-row-level-0.ag-row-group.ag-row-group-contracted.ag-row-position-absolute.ag-row-even.ag-row-hover > .ag-cell-value > .ag-cell-wrapper > .ag-group-contracted > .zeb-chevron-right"), 'click', "locator(\".ag-row-no-focus.ag-row-not-inline-editing.ag-row.ag-row-level-0.ag-row-group.ag-row-group-contracted.ag-row-position-absolute.ag-row-even.ag-row-hover > .ag-cell-value > .ag-cell-wrapper > .ag-group-contracted > .zeb-chevron-right\")", )
    safe_action(page, page.locator("esp-column-dimentional-grid").get_by_text("Scan Units (CW-3)"), 'click', "locator(\"esp-column-dimentional-grid\").get_by_text(\"Scan Units (CW-3)\")", )
    safe_action(page, page.get_by_text("Daily Trend Customer:3RD"), 'click', "get_by_text(\"Daily Trend Customer:3RD\")", )
    safe_action(page, page.locator("svg"), 'click', "locator(\"svg\")", )
    safe_action(page, page.locator(".title.d-flex.align-items-center.font-size-16.font-weight-bold.nunito.title-color > .p-l-40"), 'click', "locator(\".title.d-flex.align-items-center.font-size-16.font-weight-bold.nunito.title-color > .p-l-40\")", )
    safe_action(page, page.locator("dp-line-bar-chart").get_by_text("Customer", exact=True), 'click', "locator(\"dp-line-bar-chart\").get_by_text(\"Customer\", exact=True)", )
    safe_action(page, page.locator("dp-line-bar-chart").get_by_text("Customer:3RD PARTY DISTRIB"), 'click', "locator(\"dp-line-bar-chart\").get_by_text(\"Customer:3RD PARTY DISTRIB\")", )
    safe_action(page, page.locator("path:nth-child(79)"), 'click', "locator(\"path:nth-child(79)\")", )
    safe_action(page, page.get_by_text("User Suggested Order Base,").first, 'click', "get_by_text(\"User Suggested Order Base,\").first", )
    safe_action(page, page.locator("span").filter(has_text="User Suggested Order Base"), 'click', "locator(\"span\").filter(has_text=\"User Suggested Order Base\")", )
    safe_action(page, page.locator("span").filter(has_text="User Suggested Order Promotion"), 'click', "locator(\"span\").filter(has_text=\"User Suggested Order Promotion\")", )
    safe_action(page, page.locator("span").filter(has_text="User Override Base"), 'click', "locator(\"span\").filter(has_text=\"User Override Base\")", )
    safe_action(page, page.locator("span").filter(has_text="User Override Promotion"), 'click', "locator(\"span\").filter(has_text=\"User Override Promotion\")", )
    safe_action(page, page.locator("dp-line-bar-chart span").filter(has_text="Gross Units (CW-3)"), 'click', "locator(\"dp-line-bar-chart span\").filter(has_text=\"Gross Units (CW-3)\")", )
    safe_action(page, page.locator("dp-line-bar-chart").get_by_text("Gross Units (CW-4)"), 'click', "locator(\"dp-line-bar-chart\").get_by_text(\"Gross Units (CW-4)\")", )
    safe_action(page, page.locator(".overflow-auto > div:nth-child(7)"), 'click', "locator(\".overflow-auto > div:nth-child(7)\")", )
    safe_action(page, page.locator("div:nth-child(8) > .d-flex"), 'click', "locator(\"div:nth-child(8) > .d-flex\")", )
    safe_action(page, page.locator(".overflow-auto > div:nth-child(9)"), 'click', "locator(\".overflow-auto > div:nth-child(9)\")", )
    safe_action(page, page.locator("div:nth-child(10) > .d-flex"), 'click', "locator(\"div:nth-child(10) > .d-flex\")", )
    safe_action(page, page.locator("dp-line-bar-chart").get_by_text("Aged Net Units (CW-5)"), 'click', "locator(\"dp-line-bar-chart\").get_by_text(\"Aged Net Units (CW-5)\")", )
    safe_action(page, page.locator("dp-line-bar-chart").get_by_text("Aged Net Units (CW-6)"), 'click', "locator(\"dp-line-bar-chart\").get_by_text(\"Aged Net Units (CW-6)\")", )
    safe_action(page, page.locator("dp-line-bar-chart span").filter(has_text="Scan Units (CW-3)"), 'click', "locator(\"dp-line-bar-chart span\").filter(has_text=\"Scan Units (CW-3)\")", )
    safe_action(page, page.locator("dp-line-bar-chart").get_by_text("Scan Units (CW-4)"), 'click', "locator(\"dp-line-bar-chart\").get_by_text(\"Scan Units (CW-4)\")", )
    safe_action(page, page.locator(".overflow-auto > div:nth-child(15)"), 'click', "locator(\".overflow-auto > div:nth-child(15)\")", )
    safe_action(page, page.locator("dp-line-bar-chart").get_by_text("Scan Units (CW-6)"), 'click', "locator(\"dp-line-bar-chart\").get_by_text(\"Scan Units (CW-6)\")", )
    safe_action(page, page.locator(".ellipses > esp-multiselect-dropdown > .multiselect-dropdown > div > .w-100"), 'click', "locator(\".ellipses > esp-multiselect-dropdown > .multiselect-dropdown > div > .w-100\")", )
    safe_action(page, page.get_by_text("Daily Trend Customer:3RD"), 'click', "get_by_text(\"Daily Trend Customer:3RD\")", )
    safe_action(page, page.locator(".title.d-flex.align-items-center.font-size-16.font-weight-bold.nunito.title-color > .grid-icons-container > esp-grid-icons-component > .display-grid-icons > div > #preference-iconId > .legend-font > .multiselect-dropdown > .pointer"), 'click', "locator(\".title.d-flex.align-items-center.font-size-16.font-weight-bold.nunito.title-color > .grid-icons-container > esp-grid-icons-component > .display-grid-icons > div > #preference-iconId > .legend-font > .multiselect-dropdown > .pointer\")", )
    safe_action(page, page.get_by_text("Save Preference"), 'click', "get_by_text(\"Save Preference\")", )
    safe_action(page, page.locator(".title.d-flex.align-items-center.font-size-16.font-weight-bold.nunito.title-color > .grid-icons-container > esp-grid-icons-component > .display-grid-icons > div > #preference-iconId > .legend-font > .multiselect-dropdown > .pointer"), 'click', "locator(\".title.d-flex.align-items-center.font-size-16.font-weight-bold.nunito.title-color > .grid-icons-container > esp-grid-icons-component > .display-grid-icons > div > #preference-iconId > .legend-font > .multiselect-dropdown > .pointer\")", )
    safe_action(page, page.get_by_text("Reset Preference"), 'click', "get_by_text(\"Reset Preference\")", )
    safe_action(page, page.locator("svg"), 'click', "locator(\"svg\")", )
    safe_action(page, page.locator("svg").get_by_text("02/01/"), 'click', "locator(\"svg\").get_by_text(\"02/01/\")", )
    safe_action(page, page.get_by_text("02/02/"), 'click', "get_by_text(\"02/02/\")", )
    safe_action(page, page.get_by_text("02/03/"), 'click', "get_by_text(\"02/03/\")", )
    safe_action(page, page.locator("svg"), 'click', "locator(\"svg\")", )
    safe_action(page, page.locator("path:nth-child(67)"), 'click', "locator(\"path:nth-child(67)\")", )
    safe_action(page, page.get_by_text("User Override Promotion", exact=True), 'click', "get_by_text(\"User Override Promotion\", exact=True)", )
    safe_action(page, page.get_by_text("User Override Base", exact=True), 'click', "get_by_text(\"User Override Base\", exact=True)", )
    safe_action(page, page.locator("path:nth-child(79)"), 'click', "locator(\"path:nth-child(79)\")", )
    safe_action(page, page.locator("path:nth-child(96)"), 'click', "locator(\"path:nth-child(96)\")", )
    safe_action(page, page.locator("path:nth-child(102)"), 'click', "locator(\"path:nth-child(102)\")", )
    safe_action(page, page.locator("svg"), 'click', "locator(\"svg\")", )
    safe_action(page, page.locator("path:nth-child(102)"), 'click', "locator(\"path:nth-child(102)\")", )

    # ---------------------
    context.close()
    browser.close()


with sync_playwright() as playwright:
    run(playwright)
