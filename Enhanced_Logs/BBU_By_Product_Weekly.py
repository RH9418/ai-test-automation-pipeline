
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
    script_name = "BBU_By_Product_Weekly"
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
SCREENSHOT_DIR = r"Test_Screenshots/BBU_By_Product_Weekly"
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


def run(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    safe_action(page, page, 'goto', 'Navigate to https://stage.bbu.esp.antuit.ai/dp/demand-planning/executive-dashboard?workbookId=4&tabIndex=2', 'https://stage.bbu.esp.antuit.ai/dp/demand-planning/executive-dashboard?workbookId=4&tabIndex=2')

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
    safe_action(page, page.locator("esp-card-component").filter(has_text="Product Total columns (0)").get_by_role("button"), 'click', "locator(\"esp-card-component\").filter(has_text=\"Product Total columns (0)\").get_by_role(\"button\")", )
    safe_action(page, page.get_by_role("treeitem", name="System Forecast Total (Plan Week) Column").get_by_label("Press SPACE to toggle"), 'uncheck', "get_by_role(\"treeitem\", name=\"System Forecast Total (Plan Week) Column\").get_by_label(\"Press SPACE to toggle\")", )
    safe_action(page, page.get_by_role("treeitem", name="System Forecast Base (Plan").get_by_label("Press SPACE to toggle"), 'uncheck', "get_by_role(\"treeitem\", name=\"System Forecast Base (Plan\").get_by_label(\"Press SPACE to toggle\")", )
    safe_action(page, page.get_by_role("treeitem", name="System Forecast Promotion (").get_by_label("Press SPACE to toggle"), 'uncheck', "get_by_role(\"treeitem\", name=\"System Forecast Promotion (\").get_by_label(\"Press SPACE to toggle\")", )
    safe_action(page, page.locator("div:nth-child(3) > .ag-column-select-column"), 'click', "locator(\"div:nth-child(3) > .ag-column-select-column\")", )
    safe_action(page, page.get_by_role("treeitem", name="System Forecast Promotion (").get_by_label("Press SPACE to toggle"), 'uncheck', "get_by_role(\"treeitem\", name=\"System Forecast Promotion (\").get_by_label(\"Press SPACE to toggle\")", )
    safe_action(page, page.get_by_role("checkbox", name="Toggle All Columns Visibility"), 'check', "get_by_role(\"checkbox\", name=\"Toggle All Columns Visibility\")", )
    safe_action(page, page.locator(".pointer.zeb-adjustments").first, 'click', "locator(\".pointer.zeb-adjustments\").first", )
    safe_action(page, page.locator("div").filter(has_text=re.compile(r"^Save Preference$")).nth(1), 'click', "locator(\"div\").filter(has_text=re.compile(r\"^Save Preference$\")).nth(1)", )
    with safe_download(page) as download_info:
        safe_action(page, page.locator(".icon-color-toolbar-active.zeb-download-underline").first, 'click', "locator(\".icon-color-toolbar-active.zeb-download-underline\").first", )
    download = download_info.value
    safe_action(page, page.locator(".pointer.zeb-adjustments").first, 'click', "locator(\".pointer.zeb-adjustments\").first", )
    safe_action(page, page.get_by_text("Reset Preference"), 'click', "get_by_text(\"Reset Preference\")", )
    safe_action(page, page.get_by_text("Products"), 'click', "get_by_text(\"Products\")", )
    safe_action(page, page.locator("esp-card-component").filter(has_text="Products columns (0)").get_by_role("button"), 'click', "locator(\"esp-card-component\").filter(has_text=\"Products columns (0)\").get_by_role(\"button\")", )
    safe_action(page, page.get_by_role("checkbox", name="Toggle All Columns Visibility"), 'uncheck', "get_by_role(\"checkbox\", name=\"Toggle All Columns Visibility\")", )
    safe_action(page, page.get_by_role("treeitem", name="System Forecast Total (Plan Week) Column").get_by_label("Press SPACE to toggle visibility (hidden)"), 'check', "get_by_role(\"treeitem\", name=\"System Forecast Total (Plan Week) Column\").get_by_label(\"Press SPACE to toggle visibility (hidden)\")", )
    safe_action(page, page.get_by_role("treeitem", name="System Forecast Base (Plan Week) Column").get_by_label("Press SPACE to toggle visibility (hidden)"), 'check', "get_by_role(\"treeitem\", name=\"System Forecast Base (Plan Week) Column\").get_by_label(\"Press SPACE to toggle visibility (hidden)\")", )
    safe_action(page, page.get_by_role("treeitem", name="System Forecast Promotion (Plan Week) Column").get_by_label("Press SPACE to toggle visibility (hidden)"), 'check', "get_by_role(\"treeitem\", name=\"System Forecast Promotion (Plan Week) Column\").get_by_label(\"Press SPACE to toggle visibility (hidden)\")", )
    safe_action(page, page.get_by_role("treeitem", name="System Forecast Total (Plan+1").get_by_label("Press SPACE to toggle visibility (hidden)"), 'check', "get_by_role(\"treeitem\", name=\"System Forecast Total (Plan+1\").get_by_label(\"Press SPACE to toggle visibility (hidden)\")", )
    safe_action(page, page.get_by_role("treeitem", name="System Forecast Base (Plan+1").get_by_label("Press SPACE to toggle visibility (hidden)"), 'check', "get_by_role(\"treeitem\", name=\"System Forecast Base (Plan+1\").get_by_label(\"Press SPACE to toggle visibility (hidden)\")", )
    safe_action(page, page.get_by_role("treeitem", name="System Forecast Promotion (Plan+1 Week) Column").get_by_label("Press SPACE to toggle visibility (hidden)"), 'check', "get_by_role(\"treeitem\", name=\"System Forecast Promotion (Plan+1 Week) Column\").get_by_label(\"Press SPACE to toggle visibility (hidden)\")", )
    safe_action(page, page.get_by_role("treeitem", name="Week Gross Units Average Column").get_by_label("Press SPACE to toggle visibility (hidden)"), 'check', "get_by_role(\"treeitem\", name=\"Week Gross Units Average Column\").get_by_label(\"Press SPACE to toggle visibility (hidden)\")", )
    safe_action(page, page.get_by_role("treeitem", name="6 Week Aged Net Units Average Column", exact=True).get_by_label("Press SPACE to toggle visibility (hidden)"), 'check', "get_by_role(\"treeitem\", name=\"6 Week Aged Net Units Average Column\", exact=True).get_by_label(\"Press SPACE to toggle visibility (hidden)\")", )
    safe_action(page, page.get_by_role("checkbox", name="Toggle All Columns Visibility"), 'check', "get_by_role(\"checkbox\", name=\"Toggle All Columns Visibility\")", )
    safe_action(page, page.locator("div:nth-child(3) > #preference-iconId > .legend-font > .multiselect-dropdown > .pointer"), 'click', "locator(\"div:nth-child(3) > #preference-iconId > .legend-font > .multiselect-dropdown > .pointer\")", )
    safe_action(page, page.locator("div").filter(has_text=re.compile(r"^Save Preference$")).nth(1), 'click', "locator(\"div\").filter(has_text=re.compile(r\"^Save Preference$\")).nth(1)", )
    safe_action(page, page.locator("div:nth-child(3) > #preference-iconId > .legend-font > .multiselect-dropdown > .pointer"), 'click', "locator(\"div:nth-child(3) > #preference-iconId > .legend-font > .multiselect-dropdown > .pointer\")", )
    safe_action(page, page.get_by_text("Reset Preference"), 'click', "get_by_text(\"Reset Preference\")", )
    safe_action(page, page.locator(".ag-header-icon.ag-header-cell-filter-button > .ag-icon").first, 'click', "locator(\".ag-header-icon.ag-header-cell-filter-button > .ag-icon\").first", )
    safe_action(page, page.get_by_role("textbox", name="Filter Value"), 'fill', "get_by_role(\"textbox\", name=\"Filter Value\")", "BARCEL")
    safe_action(page, page.get_by_role("button", name="Apply"), 'click', "get_by_role(\"button\", name=\"Apply\")", )
    safe_action(page, page.locator(".ag-header-icon.ag-header-cell-filter-button > .ag-icon").first, 'click', "locator(\".ag-header-icon.ag-header-cell-filter-button > .ag-icon\").first", )
    safe_action(page, page.get_by_role("button", name="Reset"), 'click', "get_by_role(\"button\", name=\"Reset\")", )
    safe_action(page, page.get_by_role("gridcell", name="Press Space to toggle row selection (unchecked)  ARNOLD-BRWNBRY-OROWT").get_by_label("Press Space to toggle row"), 'check', "get_by_role(\"gridcell\", name=\"Press Space to toggle row selection (unchecked)  ARNOLD-BRWNBRY-OROWT\").get_by_label(\"Press Space to toggle row\")", )
    safe_action(page, page.locator("a").filter(has_text="2"), 'click', "locator(\"a\").filter(has_text=\"2\")", )
    safe_action(page, page.locator("a").filter(has_text="3"), 'click', "locator(\"a\").filter(has_text=\"3\")", )
    safe_action(page, page.get_by_role("listitem").filter(has_text=re.compile(r"^$")).nth(4), 'click', "get_by_role(\"listitem\").filter(has_text=re.compile(r\"^$\")).nth(4)", )
    safe_action(page, page.locator(".dropdown-caret.p-l-16").first, 'click', "locator(\".dropdown-caret.p-l-16\").first", )
    safe_action(page, page.locator("div").filter(has_text=re.compile(r"^View 20 row\(s\)$")).nth(1), 'click', "locator(\"div\").filter(has_text=re.compile(r\"^View 20 row\\(s\\)$\")).nth(1)", )
    safe_action(page, page.get_by_text("Filter"), 'click', "get_by_text(\"Filter\")", )
    safe_action(page, page.locator(".w-100.p-h-16.p-v-8.dropdown-label.background-white > .d-flex.align-items-center > .dropdown-caret"), 'click', "locator(\".w-100.p-h-16.p-v-8.dropdown-label.background-white > .d-flex.align-items-center > .dropdown-caret\")", )
    safe_action(page, page.locator("div").filter(has_text=re.compile(r"^Latest 5 Next 4$")).nth(1), 'click', "locator(\"div\").filter(has_text=re.compile(r\"^Latest 5 Next 4$\")).nth(1)", )
    safe_action(page, page.locator(".w-100.p-h-16.p-v-8.dropdown-label.background-white > .d-flex.align-items-center > .dropdown-caret"), 'click', "locator(\".w-100.p-h-16.p-v-8.dropdown-label.background-white > .d-flex.align-items-center > .dropdown-caret\")", )
    safe_action(page, page.locator("div").filter(has_text=re.compile(r"^Latest 5 Next 12$")).nth(1), 'click', "locator(\"div\").filter(has_text=re.compile(r\"^Latest 5 Next 12$\")).nth(1)", )
    safe_action(page, page.locator(".w-100.p-h-16.p-v-8.dropdown-label.background-white > .d-flex.align-items-center > .dropdown-caret"), 'click', "locator(\".w-100.p-h-16.p-v-8.dropdown-label.background-white > .d-flex.align-items-center > .dropdown-caret\")", )
    safe_action(page, page.locator("div").filter(has_text=re.compile(r"^Latest 13 Next 4$")).nth(1), 'click', "locator(\"div\").filter(has_text=re.compile(r\"^Latest 13 Next 4$\")).nth(1)", )
    safe_action(page, page.locator(".w-100.p-h-16.p-v-8.dropdown-label.background-white > .d-flex.align-items-center > .dropdown-caret"), 'click', "locator(\".w-100.p-h-16.p-v-8.dropdown-label.background-white > .d-flex.align-items-center > .dropdown-caret\")", )
    safe_action(page, page.locator("div").filter(has_text=re.compile(r"^Latest 13 Next 12$")).nth(1), 'click', "locator(\"div\").filter(has_text=re.compile(r\"^Latest 13 Next 12$\")).nth(1)", )
    safe_action(page, page.locator(".wr-20.font-weight-normal > esp-multiselect-dropdown > .multiselect-dropdown > div > .w-100 > .d-flex.align-items-center > .dropdown-caret"), 'click', "locator(\".wr-20.font-weight-normal > esp-multiselect-dropdown > .multiselect-dropdown > div > .w-100 > .d-flex.align-items-center > .dropdown-caret\")", )
    safe_action(page, page.locator(".d-flex.flex-column.justify-content-center").first, 'click', "locator(\".d-flex.flex-column.justify-content-center\").first", )
    safe_action(page, page.locator(".d-flex.dropdown-option.align-items-center.p-v-5.p-l-32 > .d-flex").first, 'click', "locator(\".d-flex.dropdown-option.align-items-center.p-v-5.p-l-32 > .d-flex\").first", )
    safe_action(page, page.locator(".overflow-auto > div:nth-child(2) > .d-flex"), 'click', "locator(\".overflow-auto > div:nth-child(2) > .d-flex\")", )
    safe_action(page, page.locator(".overflow-auto > div:nth-child(3) > .d-flex"), 'click', "locator(\".overflow-auto > div:nth-child(3) > .d-flex\")", )
    safe_action(page, page.locator(".overflow-auto > div:nth-child(4)"), 'click', "locator(\".overflow-auto > div:nth-child(4)\")", )
    safe_action(page, page.locator(".overflow-auto > div:nth-child(5)"), 'click', "locator(\".overflow-auto > div:nth-child(5)\")", )
    safe_action(page, page.locator(".overflow-auto > div:nth-child(6)"), 'click', "locator(\".overflow-auto > div:nth-child(6)\")", )
    safe_action(page, page.locator(".d-flex.flex-column.justify-content-center").first, 'click', "locator(\".d-flex.flex-column.justify-content-center\").first", )
    safe_action(page, page.locator(".wr-20.font-weight-normal > esp-multiselect-dropdown > .multiselect-dropdown > div > .w-100 > .d-flex.align-items-center > .dropdown-caret"), 'click', "locator(\".wr-20.font-weight-normal > esp-multiselect-dropdown > .multiselect-dropdown > div > .w-100 > .d-flex.align-items-center > .dropdown-caret\")", )
    safe_action(page, page.locator("esp-card-component").filter(has_text="Weekly Summary Product:ARNOLD").get_by_role("button"), 'click', "locator(\"esp-card-component\").filter(has_text=\"Weekly Summary Product:ARNOLD\").get_by_role(\"button\")", )
    safe_action(page, page.get_by_role("checkbox", name="Toggle All Columns Visibility"), 'uncheck', "get_by_role(\"checkbox\", name=\"Toggle All Columns Visibility\")", )
    safe_action(page, page.get_by_role("treeitem", name="-10-26 (44) Column").get_by_label("Press SPACE to toggle visibility (hidden)"), 'check', "get_by_role(\"treeitem\", name=\"-10-26 (44) Column\").get_by_label(\"Press SPACE to toggle visibility (hidden)\")", )
    safe_action(page, page.get_by_role("treeitem", name="-11-02 (45) Column").get_by_label("Press SPACE to toggle visibility (hidden)"), 'check', "get_by_role(\"treeitem\", name=\"-11-02 (45) Column\").get_by_label(\"Press SPACE to toggle visibility (hidden)\")", )
    safe_action(page, page.get_by_role("treeitem", name="-11-09 (46) Column").get_by_label("Press SPACE to toggle visibility (hidden)"), 'check', "get_by_role(\"treeitem\", name=\"-11-09 (46) Column\").get_by_label(\"Press SPACE to toggle visibility (hidden)\")", )
    safe_action(page, page.get_by_role("treeitem", name="-11-16 (47) Column").get_by_label("Press SPACE to toggle visibility (hidden)"), 'check', "get_by_role(\"treeitem\", name=\"-11-16 (47) Column\").get_by_label(\"Press SPACE to toggle visibility (hidden)\")", )
    safe_action(page, page.get_by_role("checkbox", name="Toggle All Columns Visibility"), 'check', "get_by_role(\"checkbox\", name=\"Toggle All Columns Visibility\")", )
    safe_action(page, page.locator("esp-card-component").filter(has_text="Weekly Summary Product:ARNOLD").get_by_role("button"), 'click', "locator(\"esp-card-component\").filter(has_text=\"Weekly Summary Product:ARNOLD\").get_by_role(\"button\")", )
    safe_action(page, page.locator("div:nth-child(4) > #preference-iconId > .legend-font > .multiselect-dropdown > .pointer"), 'click', "locator(\"div:nth-child(4) > #preference-iconId > .legend-font > .multiselect-dropdown > .pointer\")", )
    safe_action(page, page.get_by_text("Save Preference"), 'click', "get_by_text(\"Save Preference\")", )
    with safe_download(page) as download1_info:
        safe_action(page, page.locator("div:nth-child(3) > #export-iconId > .icon-color-toolbar-active"), 'click', "locator(\"div:nth-child(3) > #export-iconId > .icon-color-toolbar-active\")", )
    download1 = download1_info.value
    safe_action(page, page.locator("div:nth-child(4) > #preference-iconId > .legend-font > .multiselect-dropdown > .pointer"), 'click', "locator(\"div:nth-child(4) > #preference-iconId > .legend-font > .multiselect-dropdown > .pointer\")", )
    safe_action(page, page.get_by_text("Reset Preference"), 'click', "get_by_text(\"Reset Preference\")", )
    safe_action(page, page.get_by_text("-02-15 (08)"), 'click', "get_by_text(\"-02-15 (08)\")", )
    safe_action(page, page.get_by_role("img").nth(5), 'click', "get_by_role(\"img\").nth(5)", )
    safe_action(page, page.locator("esp-card-component").filter(has_text="Event Details columns (0)").get_by_role("button"), 'click', "locator(\"esp-card-component\").filter(has_text=\"Event Details columns (0)\").get_by_role(\"button\")", )
    safe_action(page, page.get_by_role("treeitem", name="Event Column").get_by_label("Press SPACE to toggle visibility (visible)"), 'uncheck', "get_by_role(\"treeitem\", name=\"Event Column\").get_by_label(\"Press SPACE to toggle visibility (visible)\")", )
    safe_action(page, page.get_by_role("treeitem", name="UPC 12 Column").get_by_label("Press SPACE to toggle visibility (visible)"), 'uncheck', "get_by_role(\"treeitem\", name=\"UPC 12 Column\").get_by_label(\"Press SPACE to toggle visibility (visible)\")", )
    safe_action(page, page.get_by_role("treeitem", name="Customer Level 2 Column").get_by_label("Press SPACE to toggle visibility (visible)"), 'uncheck', "get_by_role(\"treeitem\", name=\"Customer Level 2 Column\").get_by_label(\"Press SPACE to toggle visibility (visible)\")", )
    safe_action(page, page.get_by_role("treeitem", name="Start Date Column").get_by_label("Press SPACE to toggle visibility (visible)"), 'uncheck', "get_by_role(\"treeitem\", name=\"Start Date Column\").get_by_label(\"Press SPACE to toggle visibility (visible)\")", )
    safe_action(page, page.get_by_role("treeitem", name="End Date Column").get_by_label("Press SPACE to toggle visibility (visible)"), 'uncheck', "get_by_role(\"treeitem\", name=\"End Date Column\").get_by_label(\"Press SPACE to toggle visibility (visible)\")", )
    safe_action(page, page.get_by_role("checkbox", name="Toggle All Columns Visibility"), 'check', "get_by_role(\"checkbox\", name=\"Toggle All Columns Visibility\")", )
    safe_action(page, page.locator(".col-12.m-t-16 > div > esp-grid-container > esp-card-component > .card-container > .title > .grid-icons-container > esp-grid-icons-component > .display-grid-icons > div:nth-child(2) > #preference-iconId > .legend-font > .multiselect-dropdown > .pointer"), 'click', "locator(\".col-12.m-t-16 > div > esp-grid-container > esp-card-component > .card-container > .title > .grid-icons-container > esp-grid-icons-component > .display-grid-icons > div:nth-child(2) > #preference-iconId > .legend-font > .multiselect-dropdown > .pointer\")", )
    safe_action(page, page.get_by_text("Save Preference"), 'click', "get_by_text(\"Save Preference\")", )
    with safe_download(page) as download2_info:
        safe_action(page, page.locator("div:nth-child(6) > div > esp-grid-container > esp-card-component > .card-container > .title > .grid-icons-container > esp-grid-icons-component > .display-grid-icons > div > #export-iconId > .icon-color-toolbar-active"), 'click', "locator(\"div:nth-child(6) > div > esp-grid-container > esp-card-component > .card-container > .title > .grid-icons-container > esp-grid-icons-component > .display-grid-icons > div > #export-iconId > .icon-color-toolbar-active\")", )
    download2 = download2_info.value
    safe_action(page, page.locator(".col-12.m-t-16 > div > esp-grid-container > esp-card-component > .card-container > .title > .grid-icons-container > esp-grid-icons-component > .display-grid-icons > div:nth-child(2) > #preference-iconId > .legend-font > .multiselect-dropdown > .pointer"), 'click', "locator(\".col-12.m-t-16 > div > esp-grid-container > esp-card-component > .card-container > .title > .grid-icons-container > esp-grid-icons-component > .display-grid-icons > div:nth-child(2) > #preference-iconId > .legend-font > .multiselect-dropdown > .pointer\")", )
    safe_action(page, page.get_by_text("Reset Preference"), 'click', "get_by_text(\"Reset Preference\")", )
    safe_action(page, page.locator(".ag-header-cell.ag-header-parent-hidden.ag-header-cell-sortable.ag-header-background.ag-focus-managed.ag-header-active > .ag-header-cell-comp-wrapper > .ag-cell-label-container > .ag-header-icon > .ag-icon"), 'click', "locator(\".ag-header-cell.ag-header-parent-hidden.ag-header-cell-sortable.ag-header-background.ag-focus-managed.ag-header-active > .ag-header-cell-comp-wrapper > .ag-cell-label-container > .ag-header-icon > .ag-icon\")", )
    safe_action(page, page.get_by_role("textbox", name="Filter Value"), 'fill', "get_by_role(\"textbox\", name=\"Filter Value\")", "Scan Track")
    safe_action(page, page.get_by_role("button", name="Apply"), 'click', "get_by_role(\"button\", name=\"Apply\")", )
    safe_action(page, page.locator(".ag-header-icon.ag-header-cell-filter-button.ag-filter-active > .ag-icon"), 'click', "locator(\".ag-header-icon.ag-header-cell-filter-button.ag-filter-active > .ag-icon\")", )
    safe_action(page, page.get_by_role("button", name="Reset"), 'click', "get_by_role(\"button\", name=\"Reset\")", )
    safe_action(page, page.get_by_text("Products"), 'click', "get_by_text(\"Products\")", )
    safe_action(page, page.locator("span").filter(has_text="ARNOLD-BRWNBRY-OROWT").first, 'dblclick', "locator(\"span\").filter(has_text=\"ARNOLD-BRWNBRY-OROWT\").first", )
    safe_action(page, page.locator("span").filter(has_text="ABO COUNTRY").first, 'dblclick', "locator(\"span\").filter(has_text=\"ABO COUNTRY\").first", )
    safe_action(page, page.locator("span").filter(has_text="ABO COUNTRY").first, 'click', "locator(\"span\").filter(has_text=\"ABO COUNTRY\").first", )
    safe_action(page, page.get_by_text("ABO COUNTRY").nth(1), 'dblclick', "get_by_text(\"ABO COUNTRY\").nth(1)", )
    safe_action(page, page.locator("span").filter(has_text=re.compile(r"^OR CTY BTRMK WP 24Z-731300012500$")), 'click', "locator(\"span\").filter(has_text=re.compile(r\"^OR CTY BTRMK WP 24Z-731300012500$\"))", button="right")
    safe_action(page, page.get_by_text("Drill up"), 'click', "get_by_text(\"Drill up\")", )
    safe_action(page, page.locator("span").filter(has_text="ABO COUNTRY").first, 'click', "locator(\"span\").filter(has_text=\"ABO COUNTRY\").first", button="right")
    safe_action(page, page.get_by_text("Drill up"), 'click', "get_by_text(\"Drill up\")", )
    safe_action(page, page.locator("span").filter(has_text="ABO COUNTRY").first, 'click', "locator(\"span\").filter(has_text=\"ABO COUNTRY\").first", button="right")
    safe_action(page, page.get_by_text("Drill up"), 'click', "get_by_text(\"Drill up\")", )
    safe_action(page, page.get_by_role("gridcell", name="Press Space to toggle row selection (unchecked)  ARNOLD-BRWNBRY-OROWT").get_by_label("Press Space to toggle row"), 'check', "get_by_role(\"gridcell\", name=\"Press Space to toggle row selection (unchecked)  ARNOLD-BRWNBRY-OROWT\").get_by_label(\"Press Space to toggle row\")", )
    page.close()

    # ---------------------
    context.close()
    browser.close()


with sync_playwright() as playwright:
    run(playwright)
