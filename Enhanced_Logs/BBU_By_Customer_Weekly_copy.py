
import os
import sys
import time
import random
import re
import atexit
import contextlib
from datetime import datetime
from playwright.sync_api import sync_playwright, Playwright, Page, expect, TimeoutError


# --- Execution Tracking & Reporting ---
_successful_actions = []
_failed_actions = []

def _generate_execution_report():
    report_dir = "Execution_Reports"
    os.makedirs(report_dir, exist_ok=True)
    script_name = "BBU_By_Customer_Weekly_copy"
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
SCREENSHOT_DIR = r"Test_Screenshots/BBU_By_Customer_Weekly_copy"
if not os.path.exists(SCREENSHOT_DIR):
    os.makedirs(SCREENSHOT_DIR)
screenshot_counter = 0

def capture_annotated_screenshot(page: Page, locator, full_action_description: str):
    '''Highlights element with a thick red box and glow, then captures screenshot.'''
    global screenshot_counter
    screenshot_counter += 1
    
    timestamp = datetime.now().strftime("%H-%M-%S")
    safe_filename = re.sub(r'[^a-z0-9]', '_', full_action_description.lower())[:40]
    filename = f"{timestamp}_{screenshot_counter:02d}_{safe_filename}.png"
    path = os.path.join(SCREENSHOT_DIR, filename)

    try:
        # 🔴 FIX 1: Lightning fast visibility check (1 second max)
        locator.wait_for(state='visible', timeout=1000)
        locator.scroll_into_view_if_needed(timeout=1000)
        
        box = locator.bounding_box()
        if box:
            js_description = full_action_description.replace("'", "\\'")
            page.evaluate(f'''(params) => {{
                const {{ box, desc }} = params;
                const div = document.createElement('div');
                div.id = 'ge-spotlight-box'; div.style.position = 'absolute';
                div.style.left = `${{box.x}}px`; div.style.top = `${{box.y}}px`;
                div.style.width = `${{box.width}}px`; div.style.height = `${{box.height}}px`;
                div.style.border = '5px solid #FF0000'; div.style.boxShadow = '0 0 15px 5px rgba(255, 0, 0, 0.7)';
                div.style.boxSizing = 'border-box'; div.style.zIndex = '2147483647'; div.style.pointerEvents = 'none';
                
                const label = document.createElement('div');
                label.id = 'ge-spotlight-label'; label.textContent = desc; label.style.position = 'absolute';
                label.style.left = `${{box.x}}px`; label.style.top = `${{box.y - 40 > 0 ? box.y - 40 : box.y + box.height + 10}}px`;
                label.style.backgroundColor = '#FF0000'; label.style.color = '#FFFFFF'; label.style.padding = '8px 12px';
                label.style.fontSize = '16px'; label.style.fontWeight = 'bold'; label.style.borderRadius = '4px';
                label.style.zIndex = '2147483647';
                document.body.appendChild(div); document.body.appendChild(label);
            }}''', {'box': box, 'desc': js_description})
            
            # 🔴 FIX 2: 4x faster screenshot processing
            time.sleep(0.05) 
            page.screenshot(path=path, full_page=False)
            print(f"   └── 📸 Screenshot saved: {path}")
            
            page.evaluate('''() => {
                document.getElementById('ge-spotlight-box')?.remove();
                document.getElementById('ge-spotlight-label')?.remove();
            }''')
            return
            
    except Exception:
        pass # Element was transient/hidden. Fall back to clean screenshot!

    # 🔴 FIX 3: The Fallback Guarantee. If the box fails, take a context screenshot anyway!
    try:
        page.screenshot(path=path, full_page=False)
        print(f"   └── 📸 Context Screenshot saved (Element was transient): {path}")
    except Exception as e:
        print(f"   └── ⚠️ Total Screenshot Failure: {e}")

@contextlib.contextmanager
def safe_download(page, timeout_ms=300000): # 5 minutes default timeout
    class DummyEvent:
        @property
        def value(self):
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

def safe_action(page: Page, locator, action_name: str, description: str, *action_args, **action_kwargs):
    '''Performs action with spotlight screenshots and manual fallbacks.'''
    full_desc = f"{action_name.capitalize()}: {description}"
    if action_name == 'fill': full_desc += f" with '{action_args[0] if action_args else ''}'"
        
    try:
        if action_name == 'fill':
            print(f"\n⏸️ PAUSING FOR INPUT: About to fill '{description}'.")
            input("   └── Perform input manually in browser, then PRESS [ENTER] to continue...")
            page.wait_for_load_state('networkidle', timeout=5000)
            _successful_actions.append(full_desc + " (Manual Fill)")
            return
            
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
    safe_action(page, page, 'goto', 'Navigate to https://stage.bbu.esp.antuit.ai/dp/demand-planning/executive-dashboard?workbookId=4&tabIndex=4', 'https://stage.bbu.esp.antuit.ai/dp/demand-planning/executive-dashboard?workbookId=4&tabIndex=4')

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
    safe_action(page, page.get_by_role("checkbox", name="Toggle All Columns Visibility"), 'uncheck', "get_by_role(\"checkbox\", name=\"Toggle All Columns Visibility\")", )
    safe_action(page, page.get_by_role("textbox", name="Filter Columns Input"), 'click', "get_by_role(\"textbox\", name=\"Filter Columns Input\")", )
    safe_action(page, page.get_by_role("checkbox", name="Toggle All Columns Visibility"), 'check', "get_by_role(\"checkbox\", name=\"Toggle All Columns Visibility\")", )
    safe_action(page, page.get_by_role("textbox", name="Filter Columns Input"), 'click', "get_by_role(\"textbox\", name=\"Filter Columns Input\")", )
    safe_action(page, page.get_by_role("textbox", name="Filter Columns Input"), 'fill', "get_by_role(\"textbox\", name=\"Filter Columns Input\")", "System Forecast")
    safe_action(page, page.get_by_role("textbox", name="Filter Columns Input"), 'press', "get_by_role(\"textbox\", name=\"Filter Columns Input\")", "Enter")
    safe_action(page, page.locator(".ag-column-select-column").first, 'click', "locator(\".ag-column-select-column\").first", )
    safe_action(page, page.get_by_role("treeitem", name="System Forecast Base (Plan").get_by_label("Press SPACE to toggle"), 'check', "get_by_role(\"treeitem\", name=\"System Forecast Base (Plan\").get_by_label(\"Press SPACE to toggle\")", )
    safe_action(page, page.get_by_role("textbox", name="Filter Columns Input"), 'click', "get_by_role(\"textbox\", name=\"Filter Columns Input\")", )
    safe_action(page, page.get_by_role("textbox", name="Filter Columns Input"), 'fill', "get_by_role(\"textbox\", name=\"Filter Columns Input\")", "")
    safe_action(page, page.get_by_role("textbox", name="Filter Columns Input"), 'press', "get_by_role(\"textbox\", name=\"Filter Columns Input\")", "Enter")
    safe_action(page, page.locator(".ag-root-wrapper").get_by_text("System Forecast Total (Plan Week)"), 'click', "locator(\".ag-root-wrapper\").get_by_text(\"System Forecast Total (Plan Week)\")", )
    safe_action(page, page.get_by_label("System Forecast Base").get_by_text("System Forecast Base"), 'click', "get_by_label(\"System Forecast Base\").get_by_text(\"System Forecast Base\")", )
    safe_action(page, page.get_by_label("System Forecast Promotion").get_by_text("System Forecast Promotion"), 'click', "get_by_label(\"System Forecast Promotion\").get_by_text(\"System Forecast Promotion\")", )
    safe_action(page, page.get_by_label("System Forecast Total").get_by_text("System Forecast Total"), 'click', "get_by_label(\"System Forecast Total\").get_by_text(\"System Forecast Total\")", )
    safe_action(page, page.get_by_label("System Forecast Base").get_by_text("System Forecast Base"), 'click', "get_by_label(\"System Forecast Base\").get_by_text(\"System Forecast Base\")", )
    safe_action(page, page.get_by_label("System Forecast Base").get_by_text("System Forecast Base"), 'click', "get_by_label(\"System Forecast Base\").get_by_text(\"System Forecast Base\")", )
    safe_action(page, page.get_by_label("LY 6 Week Aged Net Units").get_by_text("LY 6 Week Aged Net Units"), 'click', "get_by_label(\"LY 6 Week Aged Net Units\").get_by_text(\"LY 6 Week Aged Net Units\")", )
    safe_action(page, page.get_by_label("% Change 6 Week Aged Net").get_by_text("% Change 6 Week Aged Net"), 'click', "get_by_label(\"% Change 6 Week Aged Net\").get_by_text(\"% Change 6 Week Aged Net\")", )
    safe_action(page, page.get_by_label("6 Week Scan Units Average Column", exact=True).get_by_text("Week Scan Units Average"), 'click', "get_by_label(\"6 Week Scan Units Average Column\", exact=True).get_by_text(\"Week Scan Units Average\")", )
    safe_action(page, page.get_by_label("LY 6 Week Scan Units Average").get_by_text("LY 6 Week Scan Units Average"), 'click', "get_by_label(\"LY 6 Week Scan Units Average\").get_by_text(\"LY 6 Week Scan Units Average\")", )
    safe_action(page, page.get_by_label("% Change 6 Week Scan Units").get_by_text("% Change 6 Week Scan Units"), 'click', "get_by_label(\"% Change 6 Week Scan Units\").get_by_text(\"% Change 6 Week Scan Units\")", )
    safe_action(page, page.get_by_label("Freshness (6 Week Average)").get_by_text("Freshness (6 Week Average)"), 'click', "get_by_label(\"Freshness (6 Week Average)\").get_by_text(\"Freshness (6 Week Average)\")", )
    safe_action(page, page.get_by_role("checkbox", name="Press SPACE to toggle visibility (visible)"), 'uncheck', "get_by_role(\"checkbox\", name=\"Press SPACE to toggle visibility (visible)\")", )
    safe_action(page, page.get_by_role("checkbox", name="Toggle All Columns Visibility"), 'check', "get_by_role(\"checkbox\", name=\"Toggle All Columns Visibility\")", )
    safe_action(page, page.locator("esp-card-component").filter(has_text="Customer Total columns (0)").get_by_role("button"), 'click', "locator(\"esp-card-component\").filter(has_text=\"Customer Total columns (0)\").get_by_role(\"button\")", )
    with safe_download(page) as download_info:
        safe_action(page, page.locator(".icon-color-toolbar-active.zeb-download-underline").first, 'click', "locator(\".icon-color-toolbar-active.zeb-download-underline\").first", )
    download = download_info.value
    safe_action(page, page.locator(".pointer.zeb-adjustments").first, 'click', "locator(\".pointer.zeb-adjustments\").first", )
    safe_action(page, page.locator("div").filter(has_text=re.compile(r"^Save Preference$")).first, 'click', "locator(\"div\").filter(has_text=re.compile(r\"^Save Preference$\")).first", )
    safe_action(page, page.locator(".pointer.zeb-adjustments").first, 'click', "locator(\".pointer.zeb-adjustments\").first", )
    safe_action(page, page.get_by_text("Reset Preference"), 'click', "get_by_text(\"Reset Preference\")", )
    safe_action(page, page.locator(".ag-body-horizontal-scroll-container").first, 'click', "locator(\".ag-body-horizontal-scroll-container\").first", )
    safe_action(page, page.get_by_text("Customers columns (0)"), 'click', "get_by_text(\"Customers columns (0)\")", )
    safe_action(page, page.get_by_text("Customers"), 'click', "get_by_text(\"Customers\")", )
    safe_action(page, page.locator("esp-card-component").filter(has_text="Customers columns (0)").get_by_role("button"), 'click', "locator(\"esp-card-component\").filter(has_text=\"Customers columns (0)\").get_by_role(\"button\")", )
    safe_action(page, page.get_by_role("textbox", name="Filter Columns Input"), 'click', "get_by_role(\"textbox\", name=\"Filter Columns Input\")", )
    safe_action(page, page.get_by_role("checkbox", name="Toggle All Columns Visibility"), 'uncheck', "get_by_role(\"checkbox\", name=\"Toggle All Columns Visibility\")", )
    safe_action(page, page.get_by_role("checkbox", name="Toggle All Columns Visibility"), 'check', "get_by_role(\"checkbox\", name=\"Toggle All Columns Visibility\")", )
    safe_action(page, page.get_by_role("textbox", name="Filter Columns Input"), 'click', "get_by_role(\"textbox\", name=\"Filter Columns Input\")", )
    safe_action(page, page.get_by_role("textbox", name="Filter Columns Input"), 'fill', "get_by_role(\"textbox\", name=\"Filter Columns Input\")", "6")
    safe_action(page, page.get_by_role("textbox", name="Filter Columns Input"), 'press', "get_by_role(\"textbox\", name=\"Filter Columns Input\")", "Enter")
    safe_action(page, page.get_by_role("treeitem", name="Week Gross Units Average Column").get_by_label("Press SPACE to toggle visibility (hidden)"), 'check', "get_by_role(\"treeitem\", name=\"Week Gross Units Average Column\").get_by_label(\"Press SPACE to toggle visibility (hidden)\")", )
    safe_action(page, page.get_by_role("treeitem", name="6 Week Aged Net Units Average Column", exact=True).get_by_label("Press SPACE to toggle visibility (hidden)"), 'check', "get_by_role(\"treeitem\", name=\"6 Week Aged Net Units Average Column\", exact=True).get_by_label(\"Press SPACE to toggle visibility (hidden)\")", )
    safe_action(page, page.get_by_role("treeitem", name="LY 6 Week Aged Net Units").get_by_label("Press SPACE to toggle visibility (hidden)"), 'check', "get_by_role(\"treeitem\", name=\"LY 6 Week Aged Net Units\").get_by_label(\"Press SPACE to toggle visibility (hidden)\")", )
    safe_action(page, page.get_by_role("treeitem", name="% Change 6 Week Aged Net").get_by_label("Press SPACE to toggle visibility (hidden)"), 'check', "get_by_role(\"treeitem\", name=\"% Change 6 Week Aged Net\").get_by_label(\"Press SPACE to toggle visibility (hidden)\")", )
    safe_action(page, page.get_by_label("Column List 9 Columns").get_by_text("6 Week Scan Units Average", exact=True), 'click', "get_by_label(\"Column List 9 Columns\").get_by_text(\"6 Week Scan Units Average\", exact=True)", )
    safe_action(page, page.get_by_label("LY 6 Week Scan Units Average").get_by_text("LY 6 Week Scan Units Average"), 'click', "get_by_label(\"LY 6 Week Scan Units Average\").get_by_text(\"LY 6 Week Scan Units Average\")", )
    safe_action(page, page.get_by_label("% Change 6 Week Scan Units").get_by_text("% Change 6 Week Scan Units"), 'click', "get_by_label(\"% Change 6 Week Scan Units\").get_by_text(\"% Change 6 Week Scan Units\")", )
    safe_action(page, page.get_by_label("6 Week Aged Returns Units").get_by_text("6 Week Aged Returns Units"), 'click', "get_by_label(\"6 Week Aged Returns Units\").get_by_text(\"6 Week Aged Returns Units\")", )
    safe_action(page, page.get_by_role("textbox", name="Filter Columns Input"), 'click', "get_by_role(\"textbox\", name=\"Filter Columns Input\")", )
    safe_action(page, page.get_by_role("textbox", name="Filter Columns Input"), 'fill', "get_by_role(\"textbox\", name=\"Filter Columns Input\")", "")
    safe_action(page, page.get_by_role("textbox", name="Filter Columns Input"), 'press', "get_by_role(\"textbox\", name=\"Filter Columns Input\")", "Enter")
    safe_action(page, page.locator(".ag-column-panel > .ag-column-select > .ag-column-select-list > .ag-virtual-list-viewport > .ag-virtual-list-container > div > .ag-column-select-column").first, 'click', "locator(\".ag-column-panel > .ag-column-select > .ag-column-select-list > .ag-virtual-list-viewport > .ag-virtual-list-container > div > .ag-column-select-column\").first", )
    safe_action(page, page.get_by_label("System Forecast Base (Plan Week) Column").get_by_text("System Forecast Base"), 'click', "get_by_label(\"System Forecast Base (Plan Week) Column\").get_by_text(\"System Forecast Base\")", )
    safe_action(page, page.get_by_label("System Forecast Promotion (Plan Week) Column").get_by_text("System Forecast Promotion"), 'click', "get_by_label(\"System Forecast Promotion (Plan Week) Column\").get_by_text(\"System Forecast Promotion\")", )
    safe_action(page, page.get_by_label("System Forecast Total").get_by_text("System Forecast Total"), 'click', "get_by_label(\"System Forecast Total\").get_by_text(\"System Forecast Total\")", )
    safe_action(page, page.get_by_label("System Forecast Base").get_by_text("System Forecast Base"), 'click', "get_by_label(\"System Forecast Base\").get_by_text(\"System Forecast Base\")", )
    safe_action(page, page.get_by_label("System Forecast Promotion (Plan+1 Week) Column").get_by_text("System Forecast Promotion"), 'click', "get_by_label(\"System Forecast Promotion (Plan+1 Week) Column\").get_by_text(\"System Forecast Promotion\")", )
    safe_action(page, page.get_by_label("6 Week Gross Units Average").get_by_text("Week Gross Units Average"), 'click', "get_by_label(\"6 Week Gross Units Average\").get_by_text(\"Week Gross Units Average\")", )
    safe_action(page, page.get_by_label("6 Week Aged Net Units Average Column", exact=True).get_by_text("6 Week Aged Net Units Average", exact=True), 'click', "get_by_label(\"6 Week Aged Net Units Average Column\", exact=True).get_by_text(\"6 Week Aged Net Units Average\", exact=True)", )
    safe_action(page, page.get_by_label("LY 6 Week Aged Net Units").get_by_text("LY 6 Week Aged Net Units"), 'click', "get_by_label(\"LY 6 Week Aged Net Units\").get_by_text(\"LY 6 Week Aged Net Units\")", )
    safe_action(page, page.get_by_label("% Change 6 Week Aged Net").get_by_text("% Change 6 Week Aged Net"), 'click', "get_by_label(\"% Change 6 Week Aged Net\").get_by_text(\"% Change 6 Week Aged Net\")", )
    safe_action(page, page.get_by_label("6 Week Scan Units Average Column", exact=True).get_by_text("6 Week Scan Units Average", exact=True), 'click', "get_by_label(\"6 Week Scan Units Average Column\", exact=True).get_by_text(\"6 Week Scan Units Average\", exact=True)", )
    safe_action(page, page.get_by_label("LY 6 Week Scan Units Average").get_by_text("LY 6 Week Scan Units Average"), 'click', "get_by_label(\"LY 6 Week Scan Units Average\").get_by_text(\"LY 6 Week Scan Units Average\")", )
    safe_action(page, page.get_by_label("% Change 6 Week Scan Units").get_by_text("% Change 6 Week Scan Units"), 'click', "get_by_label(\"% Change 6 Week Scan Units\").get_by_text(\"% Change 6 Week Scan Units\")", )
    safe_action(page, page.get_by_label("Freshness (6 Week Average)").get_by_text("Freshness (6 Week Average)"), 'click', "get_by_label(\"Freshness (6 Week Average)\").get_by_text(\"Freshness (6 Week Average)\")", )
    safe_action(page, page.get_by_label("6 Week Aged Returns Units").get_by_text("6 Week Aged Returns Units"), 'click', "get_by_label(\"6 Week Aged Returns Units\").get_by_text(\"6 Week Aged Returns Units\")", )
    safe_action(page, page.get_by_role("checkbox", name="Toggle All Columns Visibility"), 'check', "get_by_role(\"checkbox\", name=\"Toggle All Columns Visibility\")", )
    with safe_download(page) as download1_info:
        safe_action(page, page.locator("esp-grid-icons-component").filter(has_text="Export").locator("#export-iconId"), 'click', "locator(\"esp-grid-icons-component\").filter(has_text=\"Export\").locator(\"#export-iconId\")", )
    download1 = download1_info.value
    safe_action(page, page.locator("esp-card-component").filter(has_text="Customers columns (0)").locator("#preference-iconId"), 'click', "locator(\"esp-card-component\").filter(has_text=\"Customers columns (0)\").locator(\"#preference-iconId\")", )
    safe_action(page, page.locator("div").filter(has_text=re.compile(r"^Reset Preference$")).first, 'click', "locator(\"div\").filter(has_text=re.compile(r\"^Reset Preference$\")).first", )
    safe_action(page, page.locator(".ag-header-cell.ag-column-first > .ag-header-cell-comp-wrapper > .ag-cell-label-container > .ag-header-cell-label"), 'click', "locator(\".ag-header-cell.ag-column-first > .ag-header-cell-comp-wrapper > .ag-cell-label-container > .ag-header-cell-label\")", )
    safe_action(page, page.locator(".ag-icon.ag-icon-desc").first, 'click', "locator(\".ag-icon.ag-icon-desc\").first", )
    safe_action(page, page.locator(".ag-icon.ag-icon-asc").first, 'click', "locator(\".ag-icon.ag-icon-asc\").first", )
    safe_action(page, page.get_by_text("3RD PARTY DISTRIB"), 'click', "get_by_text(\"3RD PARTY DISTRIB\")", )
    safe_action(page, page.locator(".ag-group-checkbox").first, 'click', "locator(\".ag-group-checkbox\").first", )
    safe_action(page, page.locator("esp-row-dimentional-grid span").filter(has_text=re.compile(r"^3RD PARTY DISTRIB$")), 'click', "locator(\"esp-row-dimentional-grid span\").filter(has_text=re.compile(r\"^3RD PARTY DISTRIB$\"))", button="right")
    safe_action(page, page.locator("esp-row-dimentional-grid").get_by_text("3RD PARTY DISTRIB"), 'click', "locator(\"esp-row-dimentional-grid\").get_by_text(\"3RD PARTY DISTRIB\")", )
    safe_action(page, page.locator(".ag-header-icon.ag-header-cell-filter-button > .ag-icon").first, 'click', "locator(\".ag-header-icon.ag-header-cell-filter-button > .ag-icon\").first", )
    safe_action(page, page.locator(".ag-filter-body-wrapper"), 'click', "locator(\".ag-filter-body-wrapper\")", )
    safe_action(page, page.get_by_text("Contains"), 'click', "get_by_text(\"Contains\")", )
    safe_action(page, page.get_by_role("option", name="Contains"), 'click', "get_by_role(\"option\", name=\"Contains\")", )
    safe_action(page, page.get_by_text("Contains"), 'click', "get_by_text(\"Contains\")", )
    safe_action(page, page.get_by_text("Does not contain"), 'click', "get_by_text(\"Does not contain\")", )
    safe_action(page, page.get_by_text("Does not contain"), 'click', "get_by_text(\"Does not contain\")", )
    safe_action(page, page.get_by_role("option", name="Equals"), 'click', "get_by_role(\"option\", name=\"Equals\")", )
    safe_action(page, page.get_by_text("Equals"), 'click', "get_by_text(\"Equals\")", )
    safe_action(page, page.get_by_role("option", name="Does not equal"), 'click', "get_by_role(\"option\", name=\"Does not equal\")", )
    safe_action(page, page.get_by_text("Does not equal"), 'click', "get_by_text(\"Does not equal\")", )
    safe_action(page, page.get_by_role("option", name="Begins with"), 'click', "get_by_role(\"option\", name=\"Begins with\")", )
    safe_action(page, page.get_by_text("Begins with"), 'click', "get_by_text(\"Begins with\")", )
    safe_action(page, page.get_by_role("option", name="Ends with"), 'click', "get_by_role(\"option\", name=\"Ends with\")", )
    safe_action(page, page.get_by_text("Ends with"), 'click', "get_by_text(\"Ends with\")", )
    safe_action(page, page.get_by_role("option", name="Blank", exact=True), 'click', "get_by_role(\"option\", name=\"Blank\", exact=True)", )
    safe_action(page, page.get_by_text("AND", exact=True), 'click', "get_by_text(\"AND\", exact=True)", )
    safe_action(page, page.locator(".ag-labeled.ag-label-align-right.ag-radio-button.ag-input-field.ag-filter-condition-operator.ag-filter-condition-operator-or"), 'click', "locator(\".ag-labeled.ag-label-align-right.ag-radio-button.ag-input-field.ag-filter-condition-operator.ag-filter-condition-operator-or\")", )
    safe_action(page, page.get_by_role("button", name="Clear"), 'click', "get_by_role(\"button\", name=\"Clear\")", )
    safe_action(page, page.get_by_role("button", name="Reset"), 'click', "get_by_role(\"button\", name=\"Reset\")", )
    safe_action(page, page.locator(".ag-header-icon.ag-header-cell-filter-button > .ag-icon").first, 'click', "locator(\".ag-header-icon.ag-header-cell-filter-button > .ag-icon\").first", )
    safe_action(page, page.get_by_role("button", name="Apply"), 'click', "get_by_role(\"button\", name=\"Apply\")", )
    safe_action(page, page.get_by_text("System Forecast Total").nth(1), 'click', "get_by_text(\"System Forecast Total\").nth(1)", )
    safe_action(page, page.get_by_text("System Forecast Total").nth(1), 'click', "get_by_text(\"System Forecast Total\").nth(1)", )
    safe_action(page, page.get_by_text("System Forecast Total").nth(1), 'click', "get_by_text(\"System Forecast Total\").nth(1)", )
    safe_action(page, page.locator(".ag-header-cell.ag-header-parent-hidden.ag-header-cell-sortable.ag-header-background.ag-focus-managed.ag-header-active > .ag-header-cell-comp-wrapper > .ag-cell-label-container > .ag-header-icon > .ag-icon"), 'click', "locator(\".ag-header-cell.ag-header-parent-hidden.ag-header-cell-sortable.ag-header-background.ag-focus-managed.ag-header-active > .ag-header-cell-comp-wrapper > .ag-cell-label-container > .ag-header-icon > .ag-icon\")", )
    safe_action(page, page.locator(".ag-filter-body-wrapper"), 'click', "locator(\".ag-filter-body-wrapper\")", )
    safe_action(page, page.get_by_text("Equals"), 'click', "get_by_text(\"Equals\")", )
    safe_action(page, page.get_by_role("option", name="Equals"), 'click', "get_by_role(\"option\", name=\"Equals\")", )
    safe_action(page, page.get_by_text("Equals"), 'click', "get_by_text(\"Equals\")", )
    safe_action(page, page.get_by_role("option", name="Does not equal"), 'click', "get_by_role(\"option\", name=\"Does not equal\")", )
    safe_action(page, page.get_by_text("Does not equal"), 'click', "get_by_text(\"Does not equal\")", )
    safe_action(page, page.get_by_role("option", name="Greater than", exact=True), 'click', "get_by_role(\"option\", name=\"Greater than\", exact=True)", )
    safe_action(page, page.get_by_text("Greater than"), 'click', "get_by_text(\"Greater than\")", )
    safe_action(page, page.get_by_role("option", name="Less than", exact=True), 'click', "get_by_role(\"option\", name=\"Less than\", exact=True)", )
    safe_action(page, page.get_by_role("combobox", name="Filtering operator"), 'click', "get_by_role(\"combobox\", name=\"Filtering operator\")", )
    safe_action(page, page.get_by_text("Less than or equal to"), 'click', "get_by_text(\"Less than or equal to\")", )
    safe_action(page, page.get_by_text("Less than or equal to"), 'click', "get_by_text(\"Less than or equal to\")", )
    safe_action(page, page.get_by_role("option", name="Between"), 'click', "get_by_role(\"option\", name=\"Between\")", )
    safe_action(page, page.get_by_text("Between"), 'click', "get_by_text(\"Between\")", )
    safe_action(page, page.get_by_role("option", name="Blank", exact=True), 'click', "get_by_role(\"option\", name=\"Blank\", exact=True)", )
    safe_action(page, page.get_by_text("AND", exact=True), 'click', "get_by_text(\"AND\", exact=True)", )
    safe_action(page, page.get_by_text("OR", exact=True), 'click', "get_by_text(\"OR\", exact=True)", )
    safe_action(page, page.get_by_role("button", name="Clear"), 'click', "get_by_role(\"button\", name=\"Clear\")", )
    safe_action(page, page.get_by_role("button", name="Reset"), 'click', "get_by_role(\"button\", name=\"Reset\")", )
    safe_action(page, page.locator(".ag-header-cell.ag-header-parent-hidden.ag-header-cell-sortable.ag-header-background.ag-focus-managed.ag-header-active > .ag-header-cell-comp-wrapper > .ag-cell-label-container > .ag-header-icon > .ag-icon"), 'click', "locator(\".ag-header-cell.ag-header-parent-hidden.ag-header-cell-sortable.ag-header-background.ag-focus-managed.ag-header-active > .ag-header-cell-comp-wrapper > .ag-cell-label-container > .ag-header-icon > .ag-icon\")", )
    safe_action(page, page.get_by_role("button", name="Apply"), 'click', "get_by_role(\"button\", name=\"Apply\")", )
    safe_action(page, page.locator("esp-row-dimentional-grid #paginationId"), 'click', "locator(\"esp-row-dimentional-grid #paginationId\")", )
    safe_action(page, page.get_by_text("Showing 10 out of"), 'click', "get_by_text(\"Showing 10 out of\")", )
    safe_action(page, page.get_by_text("Rows per page"), 'click', "get_by_text(\"Rows per page\")", )
    safe_action(page, page.get_by_text("View 10 row(s)").first, 'click', "get_by_text(\"View 10 row(s)\").first", )
    safe_action(page, page.get_by_text("View 20 row(s)"), 'click', "get_by_text(\"View 20 row(s)\")", )
    safe_action(page, page.locator(".dropdown-caret.p-l-16").first, 'click', "locator(\".dropdown-caret.p-l-16\").first", )
    safe_action(page, page.get_by_text("Showing 20 out of 138 1234567Rows per page View 20 row(s) View 10 row(s)View 20"), 'click', "get_by_text(\"Showing 20 out of 138 1234567Rows per page View 20 row(s) View 10 row(s)View 20\")", )
    safe_action(page, page.locator(".pagination-next"), 'click', "locator(\".pagination-next\")", )
    safe_action(page, page.get_by_text("1234567"), 'click', "get_by_text(\"1234567\")", )
    safe_action(page, page.locator(".zeb-nav-to-last"), 'click', "locator(\".zeb-nav-to-last\")", )
    safe_action(page, page.get_by_role("listitem").filter(has_text=re.compile(r"^$")).nth(5), 'click', "get_by_role(\"listitem\").filter(has_text=re.compile(r\"^$\")).nth(5)", )
    safe_action(page, page.locator(".zeb-nav-to-first"), 'click', "locator(\".zeb-nav-to-first\")", )
    safe_action(page, page.get_by_text("FilterTime Latest 13 Next"), 'click', "get_by_text(\"FilterTime Latest 13 Next\")", )
    safe_action(page, page.locator("div").filter(has_text=re.compile(r"^Filter$")), 'click', "locator(\"div\").filter(has_text=re.compile(r\"^Filter$\"))", )
    safe_action(page, page.get_by_text("Filter"), 'click', "get_by_text(\"Filter\")", )
    safe_action(page, page.get_by_text("Time"), 'click', "get_by_text(\"Time\")", )
    safe_action(page, page.get_by_text("Latest 13 Next").first, 'click', "get_by_text(\"Latest 13 Next\").first", )
    safe_action(page, page.get_by_text("Latest 5 Next 4"), 'click', "get_by_text(\"Latest 5 Next 4\")", )
    safe_action(page, page.locator(".w-100.p-h-16.p-v-8.dropdown-label.background-white"), 'click', "locator(\".w-100.p-h-16.p-v-8.dropdown-label.background-white\")", )
    safe_action(page, page.locator("div").filter(has_text=re.compile(r"^Latest 5 Next 12$")).nth(1), 'click', "locator(\"div\").filter(has_text=re.compile(r\"^Latest 5 Next 12$\")).nth(1)", )
    safe_action(page, page.locator(".w-100.p-h-16.p-v-8.dropdown-label.background-white > .d-flex.align-items-center > .dropdown-caret"), 'click', "locator(\".w-100.p-h-16.p-v-8.dropdown-label.background-white > .d-flex.align-items-center > .dropdown-caret\")", )
    safe_action(page, page.locator("div").filter(has_text=re.compile(r"^Latest 13 Next 4$")).nth(1), 'click', "locator(\"div\").filter(has_text=re.compile(r\"^Latest 13 Next 4$\")).nth(1)", )
    safe_action(page, page.locator(".w-100.p-h-16.p-v-8.dropdown-label.background-white > .d-flex.align-items-center > .dropdown-caret"), 'click', "locator(\".w-100.p-h-16.p-v-8.dropdown-label.background-white > .d-flex.align-items-center > .dropdown-caret\")", )
    safe_action(page, page.get_by_text("Latest 13 Next 12"), 'click', "get_by_text(\"Latest 13 Next 12\")", )
    safe_action(page, page.locator(".w-100.p-h-16.p-v-8.dropdown-label.background-white > .d-flex.align-items-center > .dropdown-caret"), 'click', "locator(\".w-100.p-h-16.p-v-8.dropdown-label.background-white > .d-flex.align-items-center > .dropdown-caret\")", )
    safe_action(page, page.locator("div").filter(has_text=re.compile(r"^Latest 26 Next 4$")).nth(1), 'click', "locator(\"div\").filter(has_text=re.compile(r\"^Latest 26 Next 4$\")).nth(1)", )
    safe_action(page, page.get_by_text("Weekly Summary Customer:3RD"), 'click', "get_by_text(\"Weekly Summary Customer:3RD\")", )
    safe_action(page, page.get_by_text("Weekly Summary"), 'click', "get_by_text(\"Weekly Summary\")", )
    safe_action(page, page.get_by_text("Customer:3RD PARTY DISTRIB").first, 'click', "get_by_text(\"Customer:3RD PARTY DISTRIB\").first", )
    safe_action(page, page.get_by_text("Customer", exact=True).nth(2), 'click', "get_by_text(\"Customer\", exact=True).nth(2)", )
    safe_action(page, page.get_by_text("3RD PARTY DISTRIB").nth(1), 'click', "get_by_text(\"3RD PARTY DISTRIB\").nth(1)", )
    safe_action(page, page.locator(".wr-20.font-weight-normal > esp-multiselect-dropdown > .multiselect-dropdown > div > .w-100"), 'click', "locator(\".wr-20.font-weight-normal > esp-multiselect-dropdown > .multiselect-dropdown > div > .w-100\")", )
    safe_action(page, page.get_by_text("All").nth(4), 'click', "get_by_text(\"All\").nth(4)", )
    safe_action(page, page.get_by_text("All").nth(4), 'click', "get_by_text(\"All\").nth(4)", )
    safe_action(page, page.locator(".d-flex.flex-column.justify-content-center").first, 'click', "locator(\".d-flex.flex-column.justify-content-center\").first", )
    safe_action(page, page.locator(".d-flex.flex-column.justify-content-center").first, 'click', "locator(\".d-flex.flex-column.justify-content-center\").first", )
    safe_action(page, page.locator(".d-flex.dropdown-option.align-items-center.p-v-5.p-l-32 > .d-flex").first, 'click', "locator(\".d-flex.dropdown-option.align-items-center.p-v-5.p-l-32 > .d-flex\").first", )
    safe_action(page, page.locator(".d-flex.flex-column.justify-content-center.font-size-10.align-items-center.checkbox-v2.m-r-10.zeb-check").first, 'click', "locator(\".d-flex.flex-column.justify-content-center.font-size-10.align-items-center.checkbox-v2.m-r-10.zeb-check\").first", )
    safe_action(page, page.locator(".d-flex.flex-column.justify-content-center.font-size-10.align-items-center.checkbox-v2.m-r-10.zeb-check").first, 'click', "locator(\".d-flex.flex-column.justify-content-center.font-size-10.align-items-center.checkbox-v2.m-r-10.zeb-check\").first", )
    safe_action(page, page.get_by_text("User Override Total").nth(1), 'click', "get_by_text(\"User Override Total\").nth(1)", )
    safe_action(page, page.locator(".d-flex.dropdown-option.align-items-center.p-v-5.p-l-32.p-r-16.selected").first, 'click', "locator(\".d-flex.dropdown-option.align-items-center.p-v-5.p-l-32.p-r-16.selected\").first", )
    safe_action(page, page.get_by_text("User Override Promotion").nth(1), 'click', "get_by_text(\"User Override Promotion\").nth(1)", )
    safe_action(page, page.get_by_text("System Forecast Total").nth(5), 'click', "get_by_text(\"System Forecast Total\").nth(5)", )
    safe_action(page, page.get_by_text("System Forecast Base").nth(3), 'click', "get_by_text(\"System Forecast Base\").nth(3)", )
    safe_action(page, page.get_by_text("System Forecast Promotion").nth(3), 'click', "get_by_text(\"System Forecast Promotion\").nth(3)", )
    safe_action(page, page.locator(".d-flex.dropdown-option.align-items-center.p-v-5.p-l-32.p-r-16.selected").first, 'click', "locator(\".d-flex.dropdown-option.align-items-center.p-v-5.p-l-32.p-r-16.selected\").first", )
    safe_action(page, page.locator(".d-flex.dropdown-option.align-items-center.p-v-5.p-l-32.p-r-16.selected").first, 'click', "locator(\".d-flex.dropdown-option.align-items-center.p-v-5.p-l-32.p-r-16.selected\").first", )
    safe_action(page, page.get_by_text("Weekly Forecast Promotion", exact=True), 'click', "get_by_text(\"Weekly Forecast Promotion\", exact=True)", )
    safe_action(page, page.get_by_text("Daily Suggested Order Total").nth(1), 'click', "get_by_text(\"Daily Suggested Order Total\").nth(1)", )
    safe_action(page, page.get_by_text("Daily Suggested Order Base", exact=True), 'click', "get_by_text(\"Daily Suggested Order Base\", exact=True)", )
    safe_action(page, page.locator(".overflow-auto > div:nth-child(18)"), 'click', "locator(\".overflow-auto > div:nth-child(18)\")", )
    safe_action(page, page.get_by_text("Gross Units").nth(2), 'click', "get_by_text(\"Gross Units\").nth(2)", )
    safe_action(page, page.get_by_text("Raw Forecast").nth(1), 'click', "get_by_text(\"Raw Forecast\").nth(1)", )
    safe_action(page, page.get_by_text("Daily Suggested Order Promotion", exact=True), 'click', "get_by_text(\"Daily Suggested Order Promotion\", exact=True)", )
    safe_action(page, page.get_by_text("% Change Aged Net Units", exact=True), 'click', "get_by_text(\"% Change Aged Net Units\", exact=True)", )
    safe_action(page, page.get_by_text("Aged Net Units LY", exact=True), 'click', "get_by_text(\"Aged Net Units LY\", exact=True)", )
    safe_action(page, page.locator(".d-flex.dropdown-option.align-items-center.p-v-5.p-l-32.p-r-16.selected").first, 'click', "locator(\".d-flex.dropdown-option.align-items-center.p-v-5.p-l-32.p-r-16.selected\").first", )
    safe_action(page, page.get_by_text("Scan Units LY", exact=True), 'click', "get_by_text(\"Scan Units LY\", exact=True)", )
    safe_action(page, page.get_by_text("Scan Units LY", exact=True), 'click', "get_by_text(\"Scan Units LY\", exact=True)", )
    safe_action(page, page.get_by_text("Scan Units LY", exact=True), 'click', "get_by_text(\"Scan Units LY\", exact=True)", )
    safe_action(page, page.get_by_text("Freshness").nth(2), 'click', "get_by_text(\"Freshness\").nth(2)", )
    safe_action(page, page.get_by_text("% Change Scan Units", exact=True), 'click', "get_by_text(\"% Change Scan Units\", exact=True)", )
    safe_action(page, page.get_by_text("Aged Return Units").nth(1), 'click', "get_by_text(\"Aged Return Units\").nth(1)", )
    safe_action(page, page.locator(".d-flex.dropdown-option.align-items-center.p-v-5.p-l-32.p-r-16.selected").first, 'click', "locator(\".d-flex.dropdown-option.align-items-center.p-v-5.p-l-32.p-r-16.selected\").first", )
    safe_action(page, page.get_by_text("System MAPE", exact=True), 'click', "get_by_text(\"System MAPE\", exact=True)", )
    safe_action(page, page.get_by_text("Forecast Value Add - MAPE", exact=True), 'click', "get_by_text(\"Forecast Value Add - MAPE\", exact=True)", )
    safe_action(page, page.locator(".d-flex.dropdown-option.align-items-center.p-v-5.p-l-32.p-r-16.selected").first, 'click', "locator(\".d-flex.dropdown-option.align-items-center.p-v-5.p-l-32.p-r-16.selected\").first", )
    safe_action(page, page.get_by_text("System Bias", exact=True), 'click', "get_by_text(\"System Bias\", exact=True)", )
    safe_action(page, page.get_by_text("Forecast Value Add - Bias", exact=True), 'click', "get_by_text(\"Forecast Value Add - Bias\", exact=True)", )
    safe_action(page, page.get_by_text("Promo", exact=True).nth(1), 'click', "get_by_text(\"Promo\", exact=True).nth(1)", )
    safe_action(page, page.locator(".d-flex.dropdown-option").first, 'click', "locator(\".d-flex.dropdown-option\").first", )
    safe_action(page, page.locator("esp-card-component").filter(has_text="Weekly Summary Customer:3RD").get_by_role("button"), 'click', "locator(\"esp-card-component\").filter(has_text=\"Weekly Summary Customer:3RD\").get_by_role(\"button\")", )
    safe_action(page, page.get_by_role("textbox", name="Filter Columns Input"), 'click', "get_by_role(\"textbox\", name=\"Filter Columns Input\")", )
    safe_action(page, page.get_by_role("textbox", name="Filter Columns Input"), 'fill', "get_by_role(\"textbox\", name=\"Filter Columns Input\")", "2025-07-27")
    safe_action(page, page.get_by_text("-07-27 (31)"), 'click', "get_by_text(\"-07-27 (31)\")", )
    safe_action(page, page.get_by_role("checkbox", name="Press SPACE to toggle visibility (hidden)"), 'check', "get_by_role(\"checkbox\", name=\"Press SPACE to toggle visibility (hidden)\")", )
    safe_action(page, page.get_by_role("textbox", name="Filter Columns Input"), 'click', "get_by_role(\"textbox\", name=\"Filter Columns Input\")", )
    safe_action(page, page.get_by_role("textbox", name="Filter Columns Input"), 'fill', "get_by_role(\"textbox\", name=\"Filter Columns Input\")", "")
    safe_action(page, page.get_by_role("textbox", name="Filter Columns Input"), 'press', "get_by_role(\"textbox\", name=\"Filter Columns Input\")", "Enter")
    safe_action(page, page.get_by_role("checkbox", name="Toggle All Columns Visibility"), 'check', "get_by_role(\"checkbox\", name=\"Toggle All Columns Visibility\")", )
    safe_action(page, page.get_by_label("-07-27 (31) Column").get_by_text("-07-27 (31)"), 'click', "get_by_label(\"-07-27 (31) Column\").get_by_text(\"-07-27 (31)\")", )
    safe_action(page, page.get_by_label("-08-03 (32) Column").get_by_text("-08-03 (32)"), 'click', "get_by_label(\"-08-03 (32) Column\").get_by_text(\"-08-03 (32)\")", )
    safe_action(page, page.get_by_label("-08-10 (33) Column").get_by_text("-08-10 (33)"), 'click', "get_by_label(\"-08-10 (33) Column\").get_by_text(\"-08-10 (33)\")", )
    safe_action(page, page.get_by_label("-08-24 (35) Column").get_by_text("-08-24 (35)"), 'click', "get_by_label(\"-08-24 (35) Column\").get_by_text(\"-08-24 (35)\")", )
    safe_action(page, page.get_by_text("-08-24 (35)"), 'click', "get_by_text(\"-08-24 (35)\")", )
    safe_action(page, page.get_by_text("-10-19 (43)"), 'click', "get_by_text(\"-10-19 (43)\")", )
    safe_action(page, page.locator("esp-card-component").filter(has_text="Weekly Summary Customer:3RD").get_by_role("button"), 'click', "locator(\"esp-card-component\").filter(has_text=\"Weekly Summary Customer:3RD\").get_by_role(\"button\")", )
    with safe_download(page) as download2_info:
        safe_action(page, page.locator("esp-grid-icons-component").filter(has_text="Export").locator("#export-iconId"), 'click', "locator(\"esp-grid-icons-component\").filter(has_text=\"Export\").locator(\"#export-iconId\")", )
    download2 = download2_info.value
    safe_action(page, page.locator("div:nth-child(4) > #preference-iconId > .legend-font > .multiselect-dropdown > .pointer"), 'click', "locator(\"div:nth-child(4) > #preference-iconId > .legend-font > .multiselect-dropdown > .pointer\")", )
    safe_action(page, page.locator("div").filter(has_text=re.compile(r"^Save Preference$")).first, 'click', "locator(\"div\").filter(has_text=re.compile(r\"^Save Preference$\")).first", )
    safe_action(page, page.locator("div:nth-child(4) > #preference-iconId > .legend-font > .multiselect-dropdown > .pointer"), 'click', "locator(\"div:nth-child(4) > #preference-iconId > .legend-font > .multiselect-dropdown > .pointer\")", )
    safe_action(page, page.get_by_text("Reset Preference"), 'click', "get_by_text(\"Reset Preference\")", )
    safe_action(page, page.locator(".ag-header-cell.ag-column-first.ag-header-parent-hidden.ag-header-background.ag-focus-managed.ag-header-active > .ag-header-cell-comp-wrapper > .ag-cell-label-container > .ag-header-cell-label"), 'click', "locator(\".ag-header-cell.ag-column-first.ag-header-parent-hidden.ag-header-background.ag-focus-managed.ag-header-active > .ag-header-cell-comp-wrapper > .ag-cell-label-container > .ag-header-cell-label\")", )
    safe_action(page, page.locator("esp-column-dimentional-grid").get_by_text("User Forecast Total"), 'click', "locator(\"esp-column-dimentional-grid\").get_by_text(\"User Forecast Total\")", )
    safe_action(page, page.locator("i").first, 'click', "locator(\"i\").first", )
    safe_action(page, page.locator("i").nth(2), 'click', "locator(\"i\").nth(2)", )
    safe_action(page, page.locator("span").filter(has_text="User Override Total").first, 'click', "locator(\"span\").filter(has_text=\"User Override Total\").first", )
    safe_action(page, page.get_by_text("System Forecast Total", exact=True), 'click', "get_by_text(\"System Forecast Total\", exact=True)", )
    safe_action(page, page.locator("i").nth(4), 'click', "locator(\"i\").nth(4)", )
    safe_action(page, page.locator("span").filter(has_text="Weekly Forecast Total").first, 'click', "locator(\"span\").filter(has_text=\"Weekly Forecast Total\").first", )
    safe_action(page, page.locator(".ag-cell-value.ag-cell.ag-cell-not-inline-editing.ag-cell-normal-height.ag-cell-last-left-pinned.ag-column-first.ag-cell-override-normal.notosans-overwrite.no-border.ag-cell-focus > .ag-cell-wrapper > .ag-group-contracted > .zeb-chevron-right"), 'click', "locator(\".ag-cell-value.ag-cell.ag-cell-not-inline-editing.ag-cell-normal-height.ag-cell-last-left-pinned.ag-column-first.ag-cell-override-normal.notosans-overwrite.no-border.ag-cell-focus > .ag-cell-wrapper > .ag-group-contracted > .zeb-chevron-right\")", )
    safe_action(page, page.locator("span").filter(has_text="Daily Suggested Order Total").first, 'click', "locator(\"span\").filter(has_text=\"Daily Suggested Order Total\").first", )
    safe_action(page, page.locator(".ag-cell-value.ag-cell.ag-cell-not-inline-editing.ag-cell-normal-height.ag-cell-last-left-pinned.ag-column-first.ag-cell-override-normal.notosans-overwrite.no-border.ag-cell-focus > .ag-cell-wrapper > .ag-group-contracted > .zeb-chevron-right"), 'click', "locator(\".ag-cell-value.ag-cell.ag-cell-not-inline-editing.ag-cell-normal-height.ag-cell-last-left-pinned.ag-column-first.ag-cell-override-normal.notosans-overwrite.no-border.ag-cell-focus > .ag-cell-wrapper > .ag-group-contracted > .zeb-chevron-right\")", )
    safe_action(page, page.locator(".ag-cell-value.ag-cell.ag-cell-not-inline-editing.ag-cell-normal-height.ag-cell-last-left-pinned.ag-column-first.ag-cell-override-normal.notosans-overwrite.no-border.ag-cell-focus > .ag-cell-wrapper > .ag-group-expanded > .zeb-chevron-down"), 'click', "locator(\".ag-cell-value.ag-cell.ag-cell-not-inline-editing.ag-cell-normal-height.ag-cell-last-left-pinned.ag-column-first.ag-cell-override-normal.notosans-overwrite.no-border.ag-cell-focus > .ag-cell-wrapper > .ag-group-expanded > .zeb-chevron-down\")", )
    safe_action(page, page.locator(".ag-row-odd.ag-row-no-focus.ag-row-not-inline-editing.ag-row.ag-row-level-0.ag-row-group.ag-row-group-contracted.ag-row-position-absolute.ag-row-hover > .ag-cell-value > .ag-cell-wrapper > .ag-group-contracted > .zeb-chevron-right"), 'click', "locator(\".ag-row-odd.ag-row-no-focus.ag-row-not-inline-editing.ag-row.ag-row-level-0.ag-row-group.ag-row-group-contracted.ag-row-position-absolute.ag-row-hover > .ag-cell-value > .ag-cell-wrapper > .ag-group-contracted > .zeb-chevron-right\")", )
    safe_action(page, page.locator("esp-column-dimentional-grid").get_by_text("Aged Net Units", exact=True), 'click', "locator(\"esp-column-dimentional-grid\").get_by_text(\"Aged Net Units\", exact=True)", )
    safe_action(page, page.locator("esp-column-dimentional-grid").get_by_text("Scan Units"), 'click', "locator(\"esp-column-dimentional-grid\").get_by_text(\"Scan Units\")", )
    safe_action(page, page.locator(".ag-cell-value.ag-cell.ag-cell-not-inline-editing.ag-cell-normal-height.ag-cell-last-left-pinned.ag-column-first.ag-cell-override-normal.notosans-overwrite.no-border.ag-cell-focus > .ag-cell-wrapper > .ag-group-contracted > .zeb-chevron-right"), 'click', "locator(\".ag-cell-value.ag-cell.ag-cell-not-inline-editing.ag-cell-normal-height.ag-cell-last-left-pinned.ag-column-first.ag-cell-override-normal.notosans-overwrite.no-border.ag-cell-focus > .ag-cell-wrapper > .ag-group-contracted > .zeb-chevron-right\")", )
    safe_action(page, page.locator(".ag-row-odd.ag-row-no-focus.ag-row-not-inline-editing.ag-row.ag-row-level-0.ag-row-group.ag-row-group-contracted.ag-row-position-absolute.ag-row-hover > .ag-cell-value > .ag-cell-wrapper > .ag-group-contracted > .zeb-chevron-right"), 'click', "locator(\".ag-row-odd.ag-row-no-focus.ag-row-not-inline-editing.ag-row.ag-row-level-0.ag-row-group.ag-row-group-contracted.ag-row-position-absolute.ag-row-hover > .ag-cell-value > .ag-cell-wrapper > .ag-group-contracted > .zeb-chevron-right\")", )
    safe_action(page, page.locator("esp-column-dimentional-grid").get_by_text("User MAPE"), 'click', "locator(\"esp-column-dimentional-grid\").get_by_text(\"User MAPE\")", )
    safe_action(page, page.get_by_text("Weekly Trend Customer:3RD"), 'click', "get_by_text(\"Weekly Trend Customer:3RD\")", )
    safe_action(page, page.get_by_text("Weekly Trend"), 'click', "get_by_text(\"Weekly Trend\")", )
    safe_action(page, page.locator("dp-line-bar-chart").get_by_text("Customer:3RD PARTY DISTRIB"), 'click', "locator(\"dp-line-bar-chart\").get_by_text(\"Customer:3RD PARTY DISTRIB\")", )
    safe_action(page, page.locator("dp-line-bar-chart").get_by_text("Customer:3RD PARTY DISTRIB"), 'click', "locator(\"dp-line-bar-chart\").get_by_text(\"Customer:3RD PARTY DISTRIB\")", )
    safe_action(page, page.locator("dp-line-bar-chart").get_by_text("Customer", exact=True), 'click', "locator(\"dp-line-bar-chart\").get_by_text(\"Customer\", exact=True)", )
    safe_action(page, page.locator("dp-line-bar-chart").get_by_text("3RD PARTY DISTRIB"), 'click', "locator(\"dp-line-bar-chart\").get_by_text(\"3RD PARTY DISTRIB\")", )
    safe_action(page, page.get_by_text("User Forecast Total, User").first, 'click', "get_by_text(\"User Forecast Total, User\").first", )
    safe_action(page, page.locator("dp-line-bar-chart span").filter(has_text="User Forecast Total"), 'click', "locator(\"dp-line-bar-chart span\").filter(has_text=\"User Forecast Total\")", )
    safe_action(page, page.get_by_text("User Forecast Base"), 'click', "get_by_text(\"User Forecast Base\")", )
    safe_action(page, page.locator(".overflow-auto > div:nth-child(3)"), 'click', "locator(\".overflow-auto > div:nth-child(3)\")", )
    safe_action(page, page.locator("dp-line-bar-chart span").filter(has_text="User Override Total"), 'click', "locator(\"dp-line-bar-chart span\").filter(has_text=\"User Override Total\")", )
    safe_action(page, page.get_by_text("User Override Base"), 'click', "get_by_text(\"User Override Base\")", )
    safe_action(page, page.get_by_text("User Override Promotion"), 'click', "get_by_text(\"User Override Promotion\")", )
    safe_action(page, page.locator(".overflow-auto > div:nth-child(6)"), 'click', "locator(\".overflow-auto > div:nth-child(6)\")", )
    safe_action(page, page.locator("dp-line-bar-chart").get_by_text("System Forecast Total"), 'click', "locator(\"dp-line-bar-chart\").get_by_text(\"System Forecast Total\")", )
    safe_action(page, page.get_by_text("System Forecast Base", exact=True), 'click', "get_by_text(\"System Forecast Base\", exact=True)", )
    safe_action(page, page.get_by_text("System Forecast Promotion", exact=True), 'click', "get_by_text(\"System Forecast Promotion\", exact=True)", )
    safe_action(page, page.locator(".overflow-auto > div:nth-child(10)"), 'click', "locator(\".overflow-auto > div:nth-child(10)\")", )
    safe_action(page, page.locator("dp-line-bar-chart").get_by_text("Weekly Forecast Base"), 'click', "locator(\"dp-line-bar-chart\").get_by_text(\"Weekly Forecast Base\")", )
    safe_action(page, page.locator("dp-line-bar-chart").get_by_text("Weekly Forecast Promotion"), 'click', "locator(\"dp-line-bar-chart\").get_by_text(\"Weekly Forecast Promotion\")", )
    safe_action(page, page.locator("dp-line-bar-chart").get_by_text("Weekly Forecast Promotion"), 'click', "locator(\"dp-line-bar-chart\").get_by_text(\"Weekly Forecast Promotion\")", )
    safe_action(page, page.locator(".overflow-auto > div:nth-child(15)"), 'click', "locator(\".overflow-auto > div:nth-child(15)\")", )
    safe_action(page, page.locator(".overflow-auto > div:nth-child(14)"), 'click', "locator(\".overflow-auto > div:nth-child(14)\")", )
    safe_action(page, page.locator("dp-line-bar-chart").get_by_text("Daily Suggested Order Total"), 'click', "locator(\"dp-line-bar-chart\").get_by_text(\"Daily Suggested Order Total\")", )
    safe_action(page, page.locator("span").filter(has_text="Daily Suggested Order Promotion"), 'click', "locator(\"span\").filter(has_text=\"Daily Suggested Order Promotion\")", )
    safe_action(page, page.locator("span").filter(has_text="Daily Suggested Order Base"), 'click', "locator(\"span\").filter(has_text=\"Daily Suggested Order Base\")", )
    safe_action(page, page.locator("span").filter(has_text="Daily Suggested Order Base"), 'click', "locator(\"span\").filter(has_text=\"Daily Suggested Order Base\")", )
    safe_action(page, page.get_by_text("Aged Net Units", exact=True).nth(1), 'click', "get_by_text(\"Aged Net Units\", exact=True).nth(1)", )
    safe_action(page, page.locator(".overflow-auto > div:nth-child(15)"), 'click', "locator(\".overflow-auto > div:nth-child(15)\")", )
    safe_action(page, page.locator(".overflow-auto > div:nth-child(15)"), 'click', "locator(\".overflow-auto > div:nth-child(15)\")", )
    safe_action(page, page.locator(".overflow-auto > div:nth-child(17)"), 'click', "locator(\".overflow-auto > div:nth-child(17)\")", )
    safe_action(page, page.locator("dp-line-bar-chart").get_by_text("Aged Net Units", exact=True), 'click', "locator(\"dp-line-bar-chart\").get_by_text(\"Aged Net Units\", exact=True)", )
    safe_action(page, page.locator("dp-line-bar-chart").get_by_text("Aged Net Units LY"), 'click', "locator(\"dp-line-bar-chart\").get_by_text(\"Aged Net Units LY\")", )
    safe_action(page, page.locator("dp-line-bar-chart").get_by_text("Scan Units LY"), 'click', "locator(\"dp-line-bar-chart\").get_by_text(\"Scan Units LY\")", )
    safe_action(page, page.locator(".overflow-auto > div:nth-child(22)"), 'click', "locator(\".overflow-auto > div:nth-child(22)\")", )
    safe_action(page, page.locator(".overflow-auto > div:nth-child(23)"), 'click', "locator(\".overflow-auto > div:nth-child(23)\")", )
    safe_action(page, page.locator(".overflow-auto > div:nth-child(24)"), 'click', "locator(\".overflow-auto > div:nth-child(24)\")", )
    safe_action(page, page.locator("dp-line-bar-chart").get_by_text("Forecast Value Add - MAPE"), 'click', "locator(\"dp-line-bar-chart\").get_by_text(\"Forecast Value Add - MAPE\")", )
    safe_action(page, page.locator("div:nth-child(26)"), 'click', "locator(\"div:nth-child(26)\")", )
    safe_action(page, page.locator("div:nth-child(27)"), 'click', "locator(\"div:nth-child(27)\")", )
    safe_action(page, page.locator("dp-line-bar-chart").get_by_text("Forecast Value Add - Bias"), 'click', "locator(\"dp-line-bar-chart\").get_by_text(\"Forecast Value Add - Bias\")", )
    safe_action(page, page.get_by_text("User Forecast Base, User").first, 'click', "get_by_text(\"User Forecast Base, User\").first", )
    safe_action(page, page.locator(".title.d-flex.align-items-center.font-size-16.font-weight-bold.nunito.title-color > .grid-icons-container > esp-grid-icons-component > .display-grid-icons > div > #preference-iconId > .legend-font > .multiselect-dropdown > .pointer"), 'click', "locator(\".title.d-flex.align-items-center.font-size-16.font-weight-bold.nunito.title-color > .grid-icons-container > esp-grid-icons-component > .display-grid-icons > div > #preference-iconId > .legend-font > .multiselect-dropdown > .pointer\")", )
    safe_action(page, page.get_by_text("Save Preference"), 'click', "get_by_text(\"Save Preference\")", )
    safe_action(page, page.locator(".title.d-flex.align-items-center.font-size-16.font-weight-bold.nunito.title-color > .grid-icons-container > esp-grid-icons-component > .display-grid-icons > div > #preference-iconId > .legend-font > .multiselect-dropdown > .pointer"), 'click', "locator(\".title.d-flex.align-items-center.font-size-16.font-weight-bold.nunito.title-color > .grid-icons-container > esp-grid-icons-component > .display-grid-icons > div > #preference-iconId > .legend-font > .multiselect-dropdown > .pointer\")", )
    safe_action(page, page.locator("div").filter(has_text=re.compile(r"^Reset Preference$")).first, 'click', "locator(\"div\").filter(has_text=re.compile(r\"^Reset Preference$\")).first", )
    safe_action(page, page.locator("path:nth-child(157)"), 'click', "locator(\"path:nth-child(157)\")", )
    safe_action(page, page.locator("svg").get_by_text("User Forecast Total"), 'click', "locator(\"svg\").get_by_text(\"User Forecast Total\")", )
    safe_action(page, page.locator("svg").get_by_text("User Override Total"), 'click', "locator(\"svg\").get_by_text(\"User Override Total\")", )
    safe_action(page, page.locator("text").filter(has_text="Aged Net Units"), 'click', "locator(\"text\").filter(has_text=\"Aged Net Units\")", )
    safe_action(page, page.locator("svg"), 'click', "locator(\"svg\")", )
    safe_action(page, page.get_by_text("0%", exact=True), 'click', "get_by_text(\"0%\", exact=True)", )
    safe_action(page, page.get_by_text("20%"), 'click', "get_by_text(\"20%\")", )
    safe_action(page, page.get_by_text("02/01/"), 'click', "get_by_text(\"02/01/\")", )
    safe_action(page, page.get_by_text("01/11/"), 'click', "get_by_text(\"01/11/\")", )
    safe_action(page, page.get_by_text("12/21/"), 'click', "get_by_text(\"12/21/\")", )

    # ---------------------
    context.close()
    browser.close()


with sync_playwright() as playwright:
    run(playwright)
