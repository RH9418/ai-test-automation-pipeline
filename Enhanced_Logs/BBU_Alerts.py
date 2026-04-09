
import os
import sys
import time
import random
import re
from datetime import datetime
from playwright.sync_api import sync_playwright, Playwright, expect, TimeoutError

# --- Screenshot Directory Setup ---
SCREENSHOT_DIR = r"Test_Screenshots/BBU_Alerts"
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


def run(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    safe_action(page, page, 'goto', 'Navigate to https://stage.bbu.esp.antuit.ai/dp/demand-planning/executive-dashboard?workbookId=4&tabIndex=1', 'https://stage.bbu.esp.antuit.ai/dp/demand-planning/executive-dashboard?workbookId=4&tabIndex=1')

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
    safe_action(page, page.get_by_text("Filter"), 'click', "get_by_text(\"Filter\")", )
    safe_action(page, page.locator("#alerts-filterId").get_by_text("Alerts"), 'click', "locator(\"#alerts-filterId\").get_by_text(\"Alerts\")", )
    safe_action(page, page.locator(".dropdown-caret").first, 'click', "locator(\".dropdown-caret\").first", )
    safe_action(page, page.locator("div").filter(has_text=re.compile(r"^Over Bias$")).nth(1), 'click', "locator(\"div\").filter(has_text=re.compile(r\"^Over Bias$\")).nth(1)", )
    safe_action(page, page.locator(".dropdown-caret").first, 'click', "locator(\".dropdown-caret\").first", )
    safe_action(page, page.locator("div").filter(has_text=re.compile(r"^Under Bias$")).nth(1), 'click', "locator(\"div\").filter(has_text=re.compile(r\"^Under Bias$\")).nth(1)", )
    safe_action(page, page.locator(".dropdown-caret").first, 'click', "locator(\".dropdown-caret\").first", )
    safe_action(page, page.locator("div").filter(has_text=re.compile(r"^MAPE$")).nth(1), 'click', "locator(\"div\").filter(has_text=re.compile(r\"^MAPE$\")).nth(1)", )
    safe_action(page, page.locator(".dropdown-caret").first, 'click', "locator(\".dropdown-caret\").first", )
    safe_action(page, page.locator("div").filter(has_text=re.compile(r"^Stability$")).nth(1), 'click', "locator(\"div\").filter(has_text=re.compile(r\"^Stability$\")).nth(1)", )
    safe_action(page, page.locator(".dropdown-caret").first, 'click', "locator(\".dropdown-caret\").first", )
    safe_action(page, page.locator("div").filter(has_text=re.compile(r"^FVA$")).nth(1), 'click', "locator(\"div\").filter(has_text=re.compile(r\"^FVA$\")).nth(1)", )
    safe_action(page, page.get_by_role("button", name="columns"), 'click', "get_by_role(\"button\", name=\"columns\")", )
    safe_action(page, page.get_by_role("checkbox", name="Toggle All Columns Visibility"), 'check', "get_by_role(\"checkbox\", name=\"Toggle All Columns Visibility\")", )
    safe_action(page, page.get_by_role("treeitem", name="6W-Actuals Column").get_by_label("Press SPACE to toggle visibility (visible)"), 'uncheck', "get_by_role(\"treeitem\", name=\"6W-Actuals Column\").get_by_label(\"Press SPACE to toggle visibility (visible)\")", )
    safe_action(page, page.get_by_role("treeitem", name="User Bias Column").get_by_label("Press SPACE to toggle visibility (visible)"), 'uncheck', "get_by_role(\"treeitem\", name=\"User Bias Column\").get_by_label(\"Press SPACE to toggle visibility (visible)\")", )
    safe_action(page, page.locator(".pointer.zeb-adjustments"), 'click', "locator(\".pointer.zeb-adjustments\")", )
    safe_action(page, page.get_by_text("Save Preference"), 'click', "get_by_text(\"Save Preference\")", )
    with page.expect_download() as download_info:
        safe_action(page, page.locator(".icon-color-toolbar-active.zeb-download-underline"), 'click', "locator(\".icon-color-toolbar-active.zeb-download-underline\")", )
    download = download_info.value
    safe_action(page, page.locator(".pointer.zeb-adjustments"), 'click', "locator(\".pointer.zeb-adjustments\")", )
    safe_action(page, page.get_by_text("Reset Preference"), 'click', "get_by_text(\"Reset Preference\")", )
    safe_action(page, page.locator(".ag-icon.ag-icon-filter").first, 'click', "locator(\".ag-icon.ag-icon-filter\").first", )
    safe_action(page, page.get_by_role("textbox", name="Filter Value"), 'fill', "get_by_role(\"textbox\", name=\"Filter Value\")", "WINCO")
    safe_action(page, page.get_by_role("button", name="Apply"), 'click', "get_by_role(\"button\", name=\"Apply\")", )
    safe_action(page, page.locator(".ag-icon.ag-icon-filter").first, 'click', "locator(\".ag-icon.ag-icon-filter\").first", )
    safe_action(page, page.get_by_role("button", name="Reset"), 'click', "get_by_role(\"button\", name=\"Reset\")", )
    safe_action(page, page.locator(".w-100.p-h-16.p-v-8.dropdown-label.icon-small-dropdown > .d-flex.align-items-center > .dropdown-caret").first, 'click', "locator(\".w-100.p-h-16.p-v-8.dropdown-label.icon-small-dropdown > .d-flex.align-items-center > .dropdown-caret\").first", )
    safe_action(page, page.get_by_text("In progress"), 'click', "get_by_text(\"In progress\")", )
    safe_action(page, page.locator(".w-100.p-h-16.p-v-8.dropdown-label.icon-small-dropdown > .d-flex.align-items-center > .dropdown-caret").first, 'click', "locator(\".w-100.p-h-16.p-v-8.dropdown-label.icon-small-dropdown > .d-flex.align-items-center > .dropdown-caret\").first", )
    safe_action(page, page.get_by_text("Completed"), 'click', "get_by_text(\"Completed\")", )
    safe_action(page, page.locator(".w-100.p-h-16.p-v-8.dropdown-label.icon-small-dropdown > .d-flex.align-items-center > .dropdown-caret").first, 'click', "locator(\".w-100.p-h-16.p-v-8.dropdown-label.icon-small-dropdown > .d-flex.align-items-center > .dropdown-caret\").first", )
    safe_action(page, page.get_by_text("Not started"), 'click', "get_by_text(\"Not started\")", )
    safe_action(page, page.get_by_role("treegrid").get_by_text("WALMART STORES HQ"), 'dblclick', "get_by_role(\"treegrid\").get_by_text(\"WALMART STORES HQ\")", )
    safe_action(page, page.locator("span").filter(has_text="WALMART").first, 'dblclick', "locator(\"span\").filter(has_text=\"WALMART\").first", )
    safe_action(page, page.get_by_role("treegrid").get_by_text("WALMART 0906 SC B-0006805-01-"), 'dblclick', "get_by_role(\"treegrid\").get_by_text(\"WALMART 0906 SC B-0006805-01-\")", )
    safe_action(page, page.get_by_text("WALMART 0906 SC B-0006805-01-"), 'click', "get_by_text(\"WALMART 0906 SC B-0006805-01-\")", button="right")
    safe_action(page, page.get_by_text("Drill up"), 'click', "get_by_text(\"Drill up\")", )
    safe_action(page, page.locator(".ag-row-even.ag-row-focus.ag-row-not-inline-editing.ag-row.ag-row-level-0.ag-row-position-absolute.ag-row-first.ag-row-hover > .ag-cell-value > .ag-cell-wrapper"), 'click', "locator(\".ag-row-even.ag-row-focus.ag-row-not-inline-editing.ag-row.ag-row-level-0.ag-row-position-absolute.ag-row-first.ag-row-hover > .ag-cell-value > .ag-cell-wrapper\")", button="right")
    safe_action(page, page.get_by_text("Drill up"), 'click', "get_by_text(\"Drill up\")", )
    safe_action(page, page.get_by_role("treegrid").get_by_text("WALMART STORES HQ"), 'click', "get_by_role(\"treegrid\").get_by_text(\"WALMART STORES HQ\")", button="right")
    safe_action(page, page.get_by_text("Drill up"), 'click', "get_by_text(\"Drill up\")", )
    safe_action(page, page.get_by_role("columnheader", name="6W-Actuals"), 'click', "get_by_role(\"columnheader\", name=\"6W-Actuals\")", )
    safe_action(page, page.locator("a").filter(has_text="2"), 'click', "locator(\"a\").filter(has_text=\"2\")", )
    safe_action(page, page.locator(".zeb-nav-to-first"), 'click', "locator(\".zeb-nav-to-first\")", )
    safe_action(page, page.get_by_role("gridcell", name="Press Space to toggle row selection (unchecked)   WALMART STORES HQ").get_by_label("Press Space to toggle row"), 'check', "get_by_role(\"gridcell\", name=\"Press Space to toggle row selection (unchecked)   WALMART STORES HQ\").get_by_label(\"Press Space to toggle row\")", )
    safe_action(page, page.locator(".checkbox-primary-color").first, 'uncheck', "locator(\".checkbox-primary-color\").first", )
    safe_action(page, page.locator(".checkbox-primary-color").first, 'check', "locator(\".checkbox-primary-color\").first", )
    safe_action(page, page.locator(".d-flex.align-items-center.checkbox-primary-color").first, 'uncheck', "locator(\".d-flex.align-items-center.checkbox-primary-color\").first", )
    safe_action(page, page.locator(".ag-row-odd > .ag-cell-value > .ag-cell-wrapper > .ag-group-value > aeap-group-cell-renderer > .d-flex.align-items-center.w-fit-content > .d-flex").first, 'uncheck', "locator(\".ag-row-odd > .ag-cell-value > .ag-cell-wrapper > .ag-group-value > aeap-group-cell-renderer > .d-flex.align-items-center.w-fit-content > .d-flex\").first", )
    safe_action(page, page.get_by_role("button", name="columns").nth(1), 'click', "get_by_role(\"button\", name=\"columns\").nth(1)", )
    safe_action(page, page.get_by_role("checkbox", name="Toggle All Columns Visibility"), 'check', "get_by_role(\"checkbox\", name=\"Toggle All Columns Visibility\")", )
    safe_action(page, page.get_by_role("textbox", name="Filter Columns Input"), 'click', "get_by_role(\"textbox\", name=\"Filter Columns Input\")", )
    safe_action(page, page.get_by_role("textbox", name="Filter Columns Input"), 'fill', "get_by_role(\"textbox\", name=\"Filter Columns Input\")", "User Bias")
    safe_action(page, page.get_by_role("checkbox", name="Press SPACE to toggle visibility (visible)"), 'uncheck', "get_by_role(\"checkbox\", name=\"Press SPACE to toggle visibility (visible)\")", )
    safe_action(page, page.get_by_role("textbox", name="Filter Columns Input"), 'click', "get_by_role(\"textbox\", name=\"Filter Columns Input\")", )
    safe_action(page, page.get_by_role("textbox", name="Filter Columns Input"), 'press', "get_by_role(\"textbox\", name=\"Filter Columns Input\")", "ControlOrMeta+a")
    safe_action(page, page.get_by_role("textbox", name="Filter Columns Input"), 'fill', "get_by_role(\"textbox\", name=\"Filter Columns Input\")", "")
    safe_action(page, page.get_by_role("checkbox", name="Toggle All Columns Visibility"), 'check', "get_by_role(\"checkbox\", name=\"Toggle All Columns Visibility\")", )
    safe_action(page, page.get_by_role("button", name="columns").nth(1), 'click', "get_by_role(\"button\", name=\"columns\").nth(1)", )
    safe_action(page, page.locator("div:nth-child(3) > #preference-iconId > .legend-font > .multiselect-dropdown > .pointer"), 'click', "locator(\"div:nth-child(3) > #preference-iconId > .legend-font > .multiselect-dropdown > .pointer\")", )
    safe_action(page, page.get_by_text("Save Preference"), 'click', "get_by_text(\"Save Preference\")", )
    with page.expect_download() as download1_info:
        safe_action(page, page.locator("div:nth-child(2) > #export-iconId > .icon-color-toolbar-active"), 'click', "locator(\"div:nth-child(2) > #export-iconId > .icon-color-toolbar-active\")", )
    download1 = download1_info.value
    safe_action(page, page.locator("div:nth-child(3) > #preference-iconId > .legend-font > .multiselect-dropdown > .pointer"), 'click', "locator(\"div:nth-child(3) > #preference-iconId > .legend-font > .multiselect-dropdown > .pointer\")", )
    safe_action(page, page.get_by_text("Reset Preference"), 'click', "get_by_text(\"Reset Preference\")", )
    safe_action(page, page.locator(".ag-header-cell.ag-header-parent-hidden.ag-header-background.ag-focus-managed.ag-header-active > .ag-header-cell-comp-wrapper > .ag-cell-label-container > .ag-header-icon > .ag-icon"), 'click', "locator(\".ag-header-cell.ag-header-parent-hidden.ag-header-background.ag-focus-managed.ag-header-active > .ag-header-cell-comp-wrapper > .ag-cell-label-container > .ag-header-icon > .ag-icon\")", )
    safe_action(page, page.get_by_role("spinbutton", name="Filter Value"), 'fill', "get_by_role(\"spinbutton\", name=\"Filter Value\")", "761")
    safe_action(page, page.get_by_label("Column Filter").get_by_role("button", name="Apply"), 'click', "get_by_label(\"Column Filter\").get_by_role(\"button\", name=\"Apply\")", )
    safe_action(page, page.locator(".ag-header-icon.ag-header-cell-filter-button.ag-filter-active > .ag-icon"), 'click', "locator(\".ag-header-icon.ag-header-cell-filter-button.ag-filter-active > .ag-icon\")", )
    safe_action(page, page.get_by_label("Column Filter").get_by_role("button", name="Reset"), 'click', "get_by_label(\"Column Filter\").get_by_role(\"button\", name=\"Reset\")", )
    safe_action(page, page.locator(".checkbox-primary-color").first, 'check', "locator(\".checkbox-primary-color\").first", )
    safe_action(page, page.locator("span").filter(has_text="ENTENMANNS").first, 'dblclick', "locator(\"span\").filter(has_text=\"ENTENMANNS\").first", )
    safe_action(page, page.locator("span").filter(has_text="EN BITES").first, 'dblclick', "locator(\"span\").filter(has_text=\"EN BITES\").first", )
    safe_action(page, page.get_by_text("EN LITTLE BITES CP").first, 'dblclick', "get_by_text(\"EN LITTLE BITES CP\").first", )
    safe_action(page, page.get_by_text("EN LB CHOCCH MFN 10P-").first, 'click', "get_by_text(\"EN LB CHOCCH MFN 10P-\").first", button="right")
    safe_action(page, page.get_by_text("Drill up"), 'click', "get_by_text(\"Drill up\")", )
    safe_action(page, page.get_by_role("gridcell").filter(has_text=re.compile(r"^$")).first, 'click', "get_by_role(\"gridcell\").filter(has_text=re.compile(r\"^$\")).first", button="right")
    safe_action(page, page.get_by_role("gridcell").filter(has_text=re.compile(r"^$")).first, 'click', "get_by_role(\"gridcell\").filter(has_text=re.compile(r\"^$\")).first", )
    safe_action(page, page.locator("esp-card-component").filter(has_text="Products10 rows out of 11").locator("a"), 'click', "locator(\"esp-card-component\").filter(has_text=\"Products10 rows out of 11\").locator(\"a\")", )
    safe_action(page, page.locator("div:nth-child(3) > esp-pagination-v2 > .d-flex.w-100 > .pagination-pager > .pagination-first > .zeb-nav-to-first"), 'click', "locator(\"div:nth-child(3) > esp-pagination-v2 > .d-flex.w-100 > .pagination-pager > .pagination-first > .zeb-nav-to-first\")", )
    safe_action(page, page.get_by_role("button", name="Apply"), 'click', "get_by_role(\"button\", name=\"Apply\")", )
    safe_action(page, page.locator("div").filter(has_text=re.compile(r"^Filter$")).nth(1), 'click', "locator(\"div\").filter(has_text=re.compile(r\"^Filter$\")).nth(1)", )
    safe_action(page, page.locator("#time-filterId > .wr-20 > esp-multiselect-dropdown > .multiselect-dropdown > div > .w-100 > .d-flex.align-items-center > .dropdown-caret"), 'click', "locator(\"#time-filterId > .wr-20 > esp-multiselect-dropdown > .multiselect-dropdown > div > .w-100 > .d-flex.align-items-center > .dropdown-caret\")", )
    safe_action(page, page.locator("div").filter(has_text=re.compile(r"^Latest 5 Next 4$")).nth(1), 'click', "locator(\"div\").filter(has_text=re.compile(r\"^Latest 5 Next 4$\")).nth(1)", )
    safe_action(page, page.locator("#time-filterId > .wr-20 > esp-multiselect-dropdown > .multiselect-dropdown > div > .w-100 > .d-flex.align-items-center > .dropdown-caret"), 'click', "locator(\"#time-filterId > .wr-20 > esp-multiselect-dropdown > .multiselect-dropdown > div > .w-100 > .d-flex.align-items-center > .dropdown-caret\")", )
    safe_action(page, page.locator("div").filter(has_text=re.compile(r"^Latest 5 Next 12$")).nth(1), 'click', "locator(\"div\").filter(has_text=re.compile(r\"^Latest 5 Next 12$\")).nth(1)", )
    safe_action(page, page.locator("#time-filterId > .wr-20 > esp-multiselect-dropdown > .multiselect-dropdown > div > .w-100 > .d-flex.align-items-center > .dropdown-caret"), 'click', "locator(\"#time-filterId > .wr-20 > esp-multiselect-dropdown > .multiselect-dropdown > div > .w-100 > .d-flex.align-items-center > .dropdown-caret\")", )
    safe_action(page, page.locator("div").filter(has_text=re.compile(r"^Latest 13 Next 4$")).nth(1), 'click', "locator(\"div\").filter(has_text=re.compile(r\"^Latest 13 Next 4$\")).nth(1)", )
    safe_action(page, page.locator("esp-card-component").filter(has_text="Weekly Summary Customer:").get_by_role("button"), 'click', "locator(\"esp-card-component\").filter(has_text=\"Weekly Summary Customer:\").get_by_role(\"button\")", )
    safe_action(page, page.get_by_role("treeitem", name="-11-02 (45) Column").get_by_label("Press SPACE to toggle visibility (visible)"), 'uncheck', "get_by_role(\"treeitem\", name=\"-11-02 (45) Column\").get_by_label(\"Press SPACE to toggle visibility (visible)\")", )
    safe_action(page, page.get_by_role("treeitem", name="-11-09 (46) Column").get_by_label("Press SPACE to toggle visibility (visible)"), 'uncheck', "get_by_role(\"treeitem\", name=\"-11-09 (46) Column\").get_by_label(\"Press SPACE to toggle visibility (visible)\")", )
    safe_action(page, page.get_by_role("treeitem", name="-11-16 (47) Column").get_by_label("Press SPACE to toggle visibility (visible)"), 'uncheck', "get_by_role(\"treeitem\", name=\"-11-16 (47) Column\").get_by_label(\"Press SPACE to toggle visibility (visible)\")", )
    safe_action(page, page.get_by_role("checkbox", name="Toggle All Columns Visibility"), 'check', "get_by_role(\"checkbox\", name=\"Toggle All Columns Visibility\")", )
    safe_action(page, page.locator("div:nth-child(4) > #preference-iconId > .legend-font > .multiselect-dropdown > .pointer"), 'click', "locator(\"div:nth-child(4) > #preference-iconId > .legend-font > .multiselect-dropdown > .pointer\")", )
    safe_action(page, page.get_by_text("Save Preference"), 'click', "get_by_text(\"Save Preference\")", )
    safe_action(page, page.locator("div:nth-child(4) > #preference-iconId > .legend-font > .multiselect-dropdown > .pointer"), 'click', "locator(\"div:nth-child(4) > #preference-iconId > .legend-font > .multiselect-dropdown > .pointer\")", )
    safe_action(page, page.get_by_text("Reset Preference"), 'click', "get_by_text(\"Reset Preference\")", )
    with page.expect_download() as download2_info:
        safe_action(page, page.locator("div:nth-child(3) > #export-iconId > .icon-color-toolbar-active"), 'click', "locator(\"div:nth-child(3) > #export-iconId > .icon-color-toolbar-active\")", )
    download2 = download2_info.value
    safe_action(page, page.locator(".align-middle").first, 'click', "locator(\".align-middle\").first", )
    safe_action(page, page.get_by_text("Event").nth(1), 'click', "get_by_text(\"Event\").nth(1)", )
    safe_action(page, page.locator("esp-card-component").filter(has_text="Event Details columns (0)").get_by_role("button"), 'click', "locator(\"esp-card-component\").filter(has_text=\"Event Details columns (0)\").get_by_role(\"button\")", )
    safe_action(page, page.get_by_role("treeitem", name="Event Column").get_by_label("Press SPACE to toggle visibility (visible)"), 'uncheck', "get_by_role(\"treeitem\", name=\"Event Column\").get_by_label(\"Press SPACE to toggle visibility (visible)\")", )
    safe_action(page, page.get_by_role("treeitem", name="UPC 12 Column").get_by_label("Press SPACE to toggle visibility (visible)"), 'uncheck', "get_by_role(\"treeitem\", name=\"UPC 12 Column\").get_by_label(\"Press SPACE to toggle visibility (visible)\")", )
    safe_action(page, page.get_by_role("treeitem", name="Customer Level 2 Column").get_by_label("Press SPACE to toggle visibility (visible)"), 'uncheck', "get_by_role(\"treeitem\", name=\"Customer Level 2 Column\").get_by_label(\"Press SPACE to toggle visibility (visible)\")", )
    safe_action(page, page.get_by_role("treeitem", name="Start Date Column").get_by_label("Press SPACE to toggle visibility (visible)"), 'uncheck', "get_by_role(\"treeitem\", name=\"Start Date Column\").get_by_label(\"Press SPACE to toggle visibility (visible)\")", )
    safe_action(page, page.get_by_role("treeitem", name="End Date Column").get_by_label("Press SPACE to toggle visibility (visible)"), 'uncheck', "get_by_role(\"treeitem\", name=\"End Date Column\").get_by_label(\"Press SPACE to toggle visibility (visible)\")", )
    safe_action(page, page.get_by_role("treeitem", name="Max Promo Price Column").get_by_label("Press SPACE to toggle visibility (visible)"), 'uncheck', "get_by_role(\"treeitem\", name=\"Max Promo Price Column\").get_by_label(\"Press SPACE to toggle visibility (visible)\")", )
    safe_action(page, page.get_by_role("treeitem", name="Min Promo Price Column").get_by_label("Press SPACE to toggle visibility (visible)"), 'uncheck', "get_by_role(\"treeitem\", name=\"Min Promo Price Column\").get_by_label(\"Press SPACE to toggle visibility (visible)\")", )
    safe_action(page, page.get_by_role("checkbox", name="Toggle All Columns Visibility"), 'check', "get_by_role(\"checkbox\", name=\"Toggle All Columns Visibility\")", )
    safe_action(page, page.get_by_role("textbox", name="Filter Columns Input"), 'click', "get_by_role(\"textbox\", name=\"Filter Columns Input\")", )
    safe_action(page, page.get_by_role("textbox", name="Filter Columns Input"), 'fill', "get_by_role(\"textbox\", name=\"Filter Columns Input\")", "UPC")
    safe_action(page, page.get_by_role("checkbox", name="Press SPACE to toggle visibility (visible)"), 'uncheck', "get_by_role(\"checkbox\", name=\"Press SPACE to toggle visibility (visible)\")", )
    safe_action(page, page.locator("div:nth-child(7) > div > esp-grid-container > esp-card-component > .card-container > .title > .grid-icons-container > esp-grid-icons-component > .display-grid-icons > div:nth-child(2) > #preference-iconId > .legend-font > .multiselect-dropdown > .pointer"), 'click', "locator(\"div:nth-child(7) > div > esp-grid-container > esp-card-component > .card-container > .title > .grid-icons-container > esp-grid-icons-component > .display-grid-icons > div:nth-child(2) > #preference-iconId > .legend-font > .multiselect-dropdown > .pointer\")", )
    safe_action(page, page.get_by_text("Save Preference"), 'click', "get_by_text(\"Save Preference\")", )
    with page.expect_download() as download3_info:
        safe_action(page, page.locator("div:nth-child(7) > div > esp-grid-container > esp-card-component > .card-container > .title > .grid-icons-container > esp-grid-icons-component > .display-grid-icons > div > #export-iconId > .icon-color-toolbar-active"), 'click', "locator(\"div:nth-child(7) > div > esp-grid-container > esp-card-component > .card-container > .title > .grid-icons-container > esp-grid-icons-component > .display-grid-icons > div > #export-iconId > .icon-color-toolbar-active\")", )
    download3 = download3_info.value
    safe_action(page, page.locator("a").nth(2), 'click', "locator(\"a\").nth(2)", )
    safe_action(page, page.locator("a").filter(has_text="3"), 'click', "locator(\"a\").filter(has_text=\"3\")", )
    safe_action(page, page.locator("div:nth-child(7) > div > esp-grid-container > esp-card-component > .card-container > .card-content > esp-row-dimentional-grid > div > #paginationId > esp-pagination-v2 > .d-flex.w-100 > .pagination-pager > .pagination-first"), 'click', "locator(\"div:nth-child(7) > div > esp-grid-container > esp-card-component > .card-container > .card-content > esp-row-dimentional-grid > div > #paginationId > esp-pagination-v2 > .d-flex.w-100 > .pagination-pager > .pagination-first\")", )
    safe_action(page, page.get_by_text("View 10 row(s)").nth(2), 'click', "get_by_text(\"View 10 row(s)\").nth(2)", )
    safe_action(page, page.locator("div").filter(has_text=re.compile(r"^View 20 row\(s\)$")).nth(1), 'click', "locator(\"div\").filter(has_text=re.compile(r\"^View 20 row\\(s\\)$\")).nth(1)", )
    safe_action(page, page.locator(".ag-header-cell.ag-header-parent-hidden.ag-header-cell-sortable.ag-header-background.ag-focus-managed.ag-header-active > .ag-header-cell-comp-wrapper > .ag-cell-label-container > .ag-header-icon > .ag-icon"), 'click', "locator(\".ag-header-cell.ag-header-parent-hidden.ag-header-cell-sortable.ag-header-background.ag-focus-managed.ag-header-active > .ag-header-cell-comp-wrapper > .ag-cell-label-container > .ag-header-icon > .ag-icon\")", )
    safe_action(page, page.get_by_role("textbox", name="Filter Value"), 'fill', "get_by_role(\"textbox\", name=\"Filter Value\")", "Promotion")
    safe_action(page, page.get_by_label("Column Filter").get_by_role("button", name="Apply"), 'click', "get_by_label(\"Column Filter\").get_by_role(\"button\", name=\"Apply\")", )
    safe_action(page, page.locator(".ag-header-cell.ag-header-parent-hidden.ag-header-cell-sortable.ag-header-background.ag-focus-managed.ag-header-cell-filtered > .ag-header-cell-comp-wrapper > .ag-cell-label-container"), 'click', "locator(\".ag-header-cell.ag-header-parent-hidden.ag-header-cell-sortable.ag-header-background.ag-focus-managed.ag-header-cell-filtered > .ag-header-cell-comp-wrapper > .ag-cell-label-container\")", )
    safe_action(page, page.locator(".ag-header-icon.ag-header-cell-filter-button.ag-filter-active > .ag-icon"), 'click', "locator(\".ag-header-icon.ag-header-cell-filter-button.ag-filter-active > .ag-icon\")", )
    safe_action(page, page.get_by_label("Column Filter").get_by_role("button", name="Reset"), 'click', "get_by_label(\"Column Filter\").get_by_role(\"button\", name=\"Reset\")", )
    safe_action(page, page.get_by_role("gridcell", name="Promotion-TH PRO BAGEL ROLLBACK 12/29/25 thru 03/29/"), 'dblclick', "get_by_role(\"gridcell\", name=\"Promotion-TH PRO BAGEL ROLLBACK 12/29/25 thru 03/29/\")", )
    page.close()

    # ---------------------
    context.close()
    browser.close()


with sync_playwright() as playwright:
    run(playwright)
