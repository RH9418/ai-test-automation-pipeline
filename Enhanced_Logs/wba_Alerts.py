
import os
import sys
import time
import random
import re
from datetime import datetime
from playwright.sync_api import sync_playwright, Playwright, expect, TimeoutError

# --- Screenshot Directory Setup ---
SCREENSHOT_DIR = r"Test_Screenshots/wba_Alerts"
if not os.path.exists(SCREENSHOT_DIR):
    os.makedirs(SCREENSHOT_DIR)
screenshot_counter = 0

def capture_annotated_screenshot(page, locator, full_action_description: str):
    """Highlights element with a thick red box and glow, then captures screenshot."""
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
        page.evaluate("""() => {
            document.getElementById('ge-spotlight-box')?.remove();
            document.getElementById('ge-spotlight-label')?.remove();
        }""")
    except Exception as e:
        print(f"   └── ⚠️ Screenshot Error: {e}")

def safe_action(page, locator, action_name: str, description: str, *action_args):
    """Performs action with spotlight screenshots and manual fallbacks."""
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
            
        capture_annotated_screenshot(page, locator, full_desc)
        
        # Execution
        action_func = getattr(locator, action_name)
        action_func(*action_args)
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
    safe_action(page, page, 'goto', 'Navigate to https://stage.wba.esp.antuit.ai/dp/demand-planning/executive-dashboard?workbookId=6&tabIndex=1', 'https://stage.wba.esp.antuit.ai/dp/demand-planning/executive-dashboard?workbookId=6&tabIndex=1')

    print("""
================================================================================
  ACTION REQUIRED: MANUAL LOGIN & MFA
--------------------------------------------------------------------------------
  1. Log in manually. 2. Complete MFA. 3. Wait for dashboard to load.
  ---> PRESS [ENTER] IN THIS TERMINAL WHEN READY <---
================================================================================
""")
    input()
    print("\n🚀 Starting automated actions...")
    safe_action(page, page.locator("#alerts-filterId"), 'click', "locator(\"#alerts-filterId\")", )
    safe_action(page, page.locator("div").filter(has_text=re.compile(r"^MAPE$")).nth(1), 'click', "locator(\"div\").filter(has_text=re.compile(r\"^MAPE$\")).nth(1)", )
    safe_action(page, page.locator(".w-100.p-h-16.p-v-8.dropdown-label.background-white > .d-flex.align-items-center > .dropdown-caret"), 'click', "locator(\".w-100.p-h-16.p-v-8.dropdown-label.background-white > .d-flex.align-items-center > .dropdown-caret\")", )
    safe_action(page, page.locator("div").filter(has_text=re.compile(r"^Under Bias$")).nth(1), 'click', "locator(\"div\").filter(has_text=re.compile(r\"^Under Bias$\")).nth(1)", )
    safe_action(page, page.locator(".w-100.p-h-16.p-v-8.dropdown-label.background-white > .d-flex.align-items-center > .dropdown-caret"), 'click', "locator(\".w-100.p-h-16.p-v-8.dropdown-label.background-white > .d-flex.align-items-center > .dropdown-caret\")", )
    safe_action(page, page.locator("div").filter(has_text=re.compile(r"^Over Bias$")).nth(1), 'click', "locator(\"div\").filter(has_text=re.compile(r\"^Over Bias$\")).nth(1)", )
    safe_action(page, page.locator(".w-100.p-h-16.p-v-8.dropdown-label.background-white > .d-flex.align-items-center > .dropdown-caret"), 'click', "locator(\".w-100.p-h-16.p-v-8.dropdown-label.background-white > .d-flex.align-items-center > .dropdown-caret\")", )
    safe_action(page, page.locator("div").filter(has_text=re.compile(r"^PVA$")).nth(1), 'click', "locator(\"div\").filter(has_text=re.compile(r\"^PVA$\")).nth(1)", )
    safe_action(page, page.locator(".w-100.p-h-16.p-v-8.dropdown-label.background-white > .d-flex.align-items-center > .dropdown-caret"), 'click', "locator(\".w-100.p-h-16.p-v-8.dropdown-label.background-white > .d-flex.align-items-center > .dropdown-caret\")", )
    safe_action(page, page.locator("div").filter(has_text=re.compile(r"^SSIS$")).first, 'click', "locator(\"div\").filter(has_text=re.compile(r\"^SSIS$\")).first", )
    safe_action(page, page.get_by_role("button", name="columns"), 'click', "get_by_role(\"button\", name=\"columns\")", )
    safe_action(page, page.get_by_role("checkbox", name="Toggle All Columns Visibility"), 'uncheck', "get_by_role(\"checkbox\", name=\"Toggle All Columns Visibility\")", )
    safe_action(page, page.get_by_role("treeitem", name="Store Count Column").get_by_label("Press SPACE to toggle"), 'check', "get_by_role(\"treeitem\", name=\"Store Count Column\").get_by_label(\"Press SPACE to toggle\")", )
    safe_action(page, page.get_by_role("treeitem", name="Product Count Column").get_by_label("Press SPACE to toggle"), 'check', "get_by_role(\"treeitem\", name=\"Product Count Column\").get_by_label(\"Press SPACE to toggle\")", )
    safe_action(page, page.get_by_role("treeitem", name="Stability Column").get_by_label("Press SPACE to toggle"), 'check', "get_by_role(\"treeitem\", name=\"Stability Column\").get_by_label(\"Press SPACE to toggle\")", )
    safe_action(page, page.get_by_role("treeitem", name="SSIS Column").get_by_label("Press SPACE to toggle"), 'check', "get_by_role(\"treeitem\", name=\"SSIS Column\").get_by_label(\"Press SPACE to toggle\")", )
    safe_action(page, page.get_by_role("treeitem", name="User Bias Column").get_by_label("Press SPACE to toggle"), 'check', "get_by_role(\"treeitem\", name=\"User Bias Column\").get_by_label(\"Press SPACE to toggle\")", )
    safe_action(page, page.get_by_role("treeitem", name="System Bias Column").get_by_label("Press SPACE to toggle"), 'check', "get_by_role(\"treeitem\", name=\"System Bias Column\").get_by_label(\"Press SPACE to toggle\")", )
    safe_action(page, page.get_by_role("treeitem", name="User MAPE Column").get_by_label("Press SPACE to toggle visibility (hidden)"), 'check', "get_by_role(\"treeitem\", name=\"User MAPE Column\").get_by_label(\"Press SPACE to toggle visibility (hidden)\")", )
    safe_action(page, page.get_by_role("treeitem", name="System MAPE Column").get_by_label("Press SPACE to toggle visibility (hidden)"), 'check', "get_by_role(\"treeitem\", name=\"System MAPE Column\").get_by_label(\"Press SPACE to toggle visibility (hidden)\")", )
    safe_action(page, page.get_by_role("treeitem", name="Planner Value Add Column").get_by_label("Press SPACE to toggle visibility (hidden)"), 'check', "get_by_role(\"treeitem\", name=\"Planner Value Add Column\").get_by_label(\"Press SPACE to toggle visibility (hidden)\")", )
    safe_action(page, page.get_by_role("treeitem", name="13W-Fcst Column").get_by_label("Press SPACE to toggle visibility (hidden)"), 'check', "get_by_role(\"treeitem\", name=\"13W-Fcst Column\").get_by_label(\"Press SPACE to toggle visibility (hidden)\")", )
    safe_action(page, page.locator("div:nth-child(11) > .ag-column-select-column"), 'click', "locator(\"div:nth-child(11) > .ag-column-select-column\")", )
    safe_action(page, page.get_by_role("textbox", name="Filter Columns Input"), 'click', "get_by_role(\"textbox\", name=\"Filter Columns Input\")", )
    safe_action(page, page.get_by_role("textbox", name="Filter Columns Input"), 'fill', "get_by_role(\"textbox\", name=\"Filter Columns Input\")", "Store Count")
    safe_action(page, page.get_by_role("textbox", name="Filter Columns Input"), 'press', "get_by_role(\"textbox\", name=\"Filter Columns Input\")", "Enter")
    safe_action(page, page.get_by_role("checkbox", name="Press SPACE to toggle"), 'check', "get_by_role(\"checkbox\", name=\"Press SPACE to toggle\")", )
    safe_action(page, page.get_by_role("button", name="columns"), 'click', "get_by_role(\"button\", name=\"columns\")", )
    safe_action(page, page.get_by_role("row", name=" 002-SPIRITS").get_by_role("radio"), 'check', "get_by_role(\"row\", name=\" 002-SPIRITS\").get_by_role(\"radio\")", )
    safe_action(page, page.get_by_title("Filter").first, 'click', "get_by_title(\"Filter\").first", )
    safe_action(page, page.get_by_role("textbox", name="Filter Value"), 'fill', "get_by_role(\"textbox\", name=\"Filter Value\")", "002-SPIRITS")
    safe_action(page, page.get_by_label("Column Filter").get_by_role("button", name="Apply"), 'click', "get_by_label(\"Column Filter\").get_by_role(\"button\", name=\"Apply\")", )
    safe_action(page, page.get_by_title("Filter").first, 'click', "get_by_title(\"Filter\").first", )
    safe_action(page, page.locator(".ag-icon.ag-icon-small-down").first, 'click', "locator(\".ag-icon.ag-icon-small-down\").first", )
    safe_action(page, page.get_by_role("option", name="Does not contain"), 'click', "get_by_role(\"option\", name=\"Does not contain\")", )
    safe_action(page, page.locator(".ag-icon.ag-icon-small-down").first, 'click', "locator(\".ag-icon.ag-icon-small-down\").first", )
    safe_action(page, page.get_by_role("option", name="Equals"), 'click', "get_by_role(\"option\", name=\"Equals\")", )
    safe_action(page, page.locator(".ag-icon.ag-icon-small-down").first, 'click', "locator(\".ag-icon.ag-icon-small-down\").first", )
    safe_action(page, page.get_by_role("option", name="Does not equal"), 'click', "get_by_role(\"option\", name=\"Does not equal\")", )
    safe_action(page, page.locator(".ag-icon.ag-icon-small-down").first, 'click', "locator(\".ag-icon.ag-icon-small-down\").first", )
    safe_action(page, page.get_by_role("option", name="Begins with"), 'click', "get_by_role(\"option\", name=\"Begins with\")", )
    safe_action(page, page.locator(".ag-icon.ag-icon-small-down").first, 'click', "locator(\".ag-icon.ag-icon-small-down\").first", )
    safe_action(page, page.get_by_role("option", name="Ends with"), 'click', "get_by_role(\"option\", name=\"Ends with\")", )
    safe_action(page, page.locator(".ag-icon.ag-icon-small-down").first, 'click', "locator(\".ag-icon.ag-icon-small-down\").first", )
    safe_action(page, page.get_by_role("option", name="Does not contain"), 'click', "get_by_role(\"option\", name=\"Does not contain\")", )
    safe_action(page, page.get_by_label("Column Filter").get_by_role("button", name="Apply"), 'click', "get_by_label(\"Column Filter\").get_by_role(\"button\", name=\"Apply\")", )
    safe_action(page, page.get_by_title("Filter").first, 'click', "get_by_title(\"Filter\").first", )
    safe_action(page, page.get_by_role("button", name="Reset"), 'click', "get_by_role(\"button\", name=\"Reset\")", )
    safe_action(page, page.locator("a").first, 'click', "locator(\"a\").first", )
    safe_action(page, page.locator("a").nth(1), 'click', "locator(\"a\").nth(1)", )
    safe_action(page, page.locator(".pagination-next > .zeb-chevron-right").first, 'click', "locator(\".pagination-next > .zeb-chevron-right\").first", )
    safe_action(page, page.locator(".zeb-chevron-left").first, 'click', "locator(\".zeb-chevron-left\").first", )
    safe_action(page, page.locator(".zeb-nav-to-first").first, 'click', "locator(\".zeb-nav-to-first\").first", )
    safe_action(page, page.locator(".d-flex > esp-multiselect-dropdown > .multiselect-dropdown > div > .w-100 > .d-flex.align-items-center > .dropdown-caret").first, 'click', "locator(\".d-flex > esp-multiselect-dropdown > .multiselect-dropdown > div > .w-100 > .d-flex.align-items-center > .dropdown-caret\").first", )
    safe_action(page, page.locator("div").filter(has_text=re.compile(r"^View 20 row\(s\)$")).first, 'click', "locator(\"div\").filter(has_text=re.compile(r\"^View 20 row\\(s\\)$\")).first", )
    safe_action(page, page.locator(".d-flex > esp-multiselect-dropdown > .multiselect-dropdown > div > .w-100 > .d-flex.align-items-center > .dropdown-caret").first, 'click', "locator(\".d-flex > esp-multiselect-dropdown > .multiselect-dropdown > div > .w-100 > .d-flex.align-items-center > .dropdown-caret\").first", )
    safe_action(page, page.locator("div").filter(has_text=re.compile(r"^View 50 row\(s\)$")).first, 'click', "locator(\"div\").filter(has_text=re.compile(r\"^View 50 row\\(s\\)$\")).first", )
    safe_action(page, page.locator(".d-flex > esp-multiselect-dropdown > .multiselect-dropdown > div > .w-100 > .d-flex.align-items-center > .dropdown-caret").first, 'click', "locator(\".d-flex > esp-multiselect-dropdown > .multiselect-dropdown > div > .w-100 > .d-flex.align-items-center > .dropdown-caret\").first", )
    safe_action(page, page.locator("div").filter(has_text=re.compile(r"^View 10 row\(s\)$")).nth(1), 'click', "locator(\"div\").filter(has_text=re.compile(r\"^View 10 row\\(s\\)$\")).nth(1)", )
    safe_action(page, page.get_by_text("Locations 20 rows out of 968"), 'click', "get_by_text(\"Locations 20 rows out of 968\")", )
    safe_action(page, page.locator(".pointer.chevron.zeb-chevron-right.m-r-12.collapsed"), 'click', "locator(\".pointer.chevron.zeb-chevron-right.m-r-12.collapsed\")", )
    safe_action(page, page.get_by_text("Locations", exact=True), 'click', "get_by_text(\"Locations\", exact=True)", )
    safe_action(page, page.get_by_role("row", name="Location").get_by_role("checkbox"), 'uncheck', "get_by_role(\"row\", name=\"Location\").get_by_role(\"checkbox\")", )
    safe_action(page, page.get_by_role("button", name="columns").nth(1), 'click', "get_by_role(\"button\", name=\"columns\").nth(1)", )
    safe_action(page, page.get_by_role("checkbox", name="Toggle All Columns Visibility"), 'uncheck', "get_by_role(\"checkbox\", name=\"Toggle All Columns Visibility\")", )
    safe_action(page, page.get_by_role("treeitem", name="Store Count Column").get_by_label("Press SPACE to toggle"), 'check', "get_by_role(\"treeitem\", name=\"Store Count Column\").get_by_label(\"Press SPACE to toggle\")", )
    safe_action(page, page.get_by_role("treeitem", name="Product Count Column").get_by_label("Press SPACE to toggle"), 'check', "get_by_role(\"treeitem\", name=\"Product Count Column\").get_by_label(\"Press SPACE to toggle\")", )
    safe_action(page, page.get_by_role("treeitem", name="13W-Fcst Column").get_by_label("Press SPACE to toggle"), 'check', "get_by_role(\"treeitem\", name=\"13W-Fcst Column\").get_by_label(\"Press SPACE to toggle\")", )
    safe_action(page, page.get_by_role("textbox", name="Filter Columns Input"), 'click', "get_by_role(\"textbox\", name=\"Filter Columns Input\")", )
    safe_action(page, page.get_by_role("textbox", name="Filter Columns Input"), 'fill', "get_by_role(\"textbox\", name=\"Filter Columns Input\")", "Pre")
    safe_action(page, page.get_by_role("checkbox", name="Press SPACE to toggle"), 'check', "get_by_role(\"checkbox\", name=\"Press SPACE to toggle\")", )
    safe_action(page, page.get_by_role("button", name="columns").nth(1), 'click', "get_by_role(\"button\", name=\"columns\").nth(1)", )
    safe_action(page, page.locator("#ag-header-cell-menu-button > .filter-icon"), 'click', "locator(\"#ag-header-cell-menu-button > .filter-icon\")", )
    safe_action(page, page.get_by_role("textbox", name="Filter Value"), 'click', "get_by_role(\"textbox\", name=\"Filter Value\")", )
    safe_action(page, page.get_by_role("textbox", name="Filter Value"), 'fill', "get_by_role(\"textbox\", name=\"Filter Value\")", "CHICAGO")
    safe_action(page, page.get_by_label("Column Menu").get_by_role("button", name="Apply"), 'click', "get_by_label(\"Column Menu\").get_by_role(\"button\", name=\"Apply\")", )
    safe_action(page, page.get_by_role("gridcell", name="00162-1554 E 55TH ST-CHICAGO-").get_by_role("checkbox"), 'check', "get_by_role(\"gridcell\", name=\"00162-1554 E 55TH ST-CHICAGO-\").get_by_role(\"checkbox\")", )
    safe_action(page, page.locator("#ag-header-cell-menu-button > .filter-icon"), 'click', "locator(\"#ag-header-cell-menu-button > .filter-icon\")", )
    safe_action(page, page.get_by_label("Column Menu").get_by_role("button", name="Reset"), 'click', "get_by_label(\"Column Menu\").get_by_role(\"button\", name=\"Reset\")", )
    safe_action(page, page.get_by_role("row", name="Location").get_by_role("checkbox"), 'check', "get_by_role(\"row\", name=\"Location\").get_by_role(\"checkbox\")", )
    safe_action(page, page.locator("a").filter(has_text="2").nth(1), 'click', "locator(\"a\").filter(has_text=\"2\").nth(1)", )
    safe_action(page, page.locator("a").filter(has_text="3").nth(1), 'click', "locator(\"a\").filter(has_text=\"3\").nth(1)", )
    safe_action(page, page.locator("div:nth-child(3) > esp-pagination-v2 > .d-flex.w-100 > .pagination-pager > .pagination-next > .zeb-chevron-right"), 'click', "locator(\"div:nth-child(3) > esp-pagination-v2 > .d-flex.w-100 > .pagination-pager > .pagination-next > .zeb-chevron-right\")", )
    safe_action(page, page.locator("div:nth-child(3) > esp-pagination-v2 > .d-flex.w-100 > .pagination-pager > .pagination-previous > .zeb-chevron-left"), 'click', "locator(\"div:nth-child(3) > esp-pagination-v2 > .d-flex.w-100 > .pagination-pager > .pagination-previous > .zeb-chevron-left\")", )
    safe_action(page, page.locator("div:nth-child(3) > esp-pagination-v2 > .d-flex.w-100 > .pagination-pager > .pagination-first > .zeb-nav-to-first"), 'click', "locator(\"div:nth-child(3) > esp-pagination-v2 > .d-flex.w-100 > .pagination-pager > .pagination-first > .zeb-nav-to-first\")", )
    safe_action(page, page.get_by_role("button", name="Apply"), 'click', "get_by_role(\"button\", name=\"Apply\")", )
    safe_action(page, page.get_by_text("Filter").nth(2), 'click', "get_by_text(\"Filter\").nth(2)", )
    safe_action(page, page.locator("#time-filterId > .wr-20 > esp-multiselect-dropdown > .multiselect-dropdown > div > .w-100 > .d-flex.align-items-center > .dropdown-caret"), 'click', "locator(\"#time-filterId > .wr-20 > esp-multiselect-dropdown > .multiselect-dropdown > div > .w-100 > .d-flex.align-items-center > .dropdown-caret\")", )
    safe_action(page, page.locator("div").filter(has_text=re.compile(r"^Latest 4 Next 4$")).nth(1), 'click', "locator(\"div\").filter(has_text=re.compile(r\"^Latest 4 Next 4$\")).nth(1)", )
    safe_action(page, page.locator("#time-filterId > .wr-20 > esp-multiselect-dropdown > .multiselect-dropdown > div > .w-100 > .d-flex.align-items-center > .dropdown-caret"), 'click', "locator(\"#time-filterId > .wr-20 > esp-multiselect-dropdown > .multiselect-dropdown > div > .w-100 > .d-flex.align-items-center > .dropdown-caret\")", )
    safe_action(page, page.locator("div").filter(has_text=re.compile(r"^Latest 4 Next 13$")).nth(1), 'click', "locator(\"div\").filter(has_text=re.compile(r\"^Latest 4 Next 13$\")).nth(1)", )
    safe_action(page, page.locator("#time-filterId > .wr-20 > esp-multiselect-dropdown > .multiselect-dropdown > div > .w-100 > .d-flex.align-items-center > .dropdown-caret"), 'click', "locator(\"#time-filterId > .wr-20 > esp-multiselect-dropdown > .multiselect-dropdown > div > .w-100 > .d-flex.align-items-center > .dropdown-caret\")", )
    safe_action(page, page.locator("div").filter(has_text=re.compile(r"^Latest 13 Next 13$")).nth(1), 'click', "locator(\"div\").filter(has_text=re.compile(r\"^Latest 13 Next 13$\")).nth(1)", )
    safe_action(page, page.locator("#time-filterId > .wr-20 > esp-multiselect-dropdown > .multiselect-dropdown > div > .w-100 > .d-flex.align-items-center > .dropdown-caret"), 'click', "locator(\"#time-filterId > .wr-20 > esp-multiselect-dropdown > .multiselect-dropdown > div > .w-100 > .d-flex.align-items-center > .dropdown-caret\")", )
    safe_action(page, page.locator("div").filter(has_text=re.compile(r"^Latest 52 Next 52$")).first, 'click', "locator(\"div\").filter(has_text=re.compile(r\"^Latest 52 Next 52$\")).first", )
    safe_action(page, page.locator("#time-filterId > .wr-20 > esp-multiselect-dropdown > .multiselect-dropdown > div > .w-100 > .d-flex.align-items-center > .dropdown-caret"), 'click', "locator(\"#time-filterId > .wr-20 > esp-multiselect-dropdown > .multiselect-dropdown > div > .w-100 > .d-flex.align-items-center > .dropdown-caret\")", )
    safe_action(page, page.locator("div").filter(has_text=re.compile(r"^Latest 104 Next 52$")).nth(1), 'click', "locator(\"div\").filter(has_text=re.compile(r\"^Latest 104 Next 52$\")).nth(1)", )
    safe_action(page, page.locator("#time-filterId > .wr-20 > esp-multiselect-dropdown > .multiselect-dropdown > div > .w-100 > .d-flex.align-items-center > .dropdown-caret"), 'click', "locator(\"#time-filterId > .wr-20 > esp-multiselect-dropdown > .multiselect-dropdown > div > .w-100 > .d-flex.align-items-center > .dropdown-caret\")", )
    safe_action(page, page.locator("div").filter(has_text=re.compile(r"^Latest 4 Next 4$")).nth(1), 'click', "locator(\"div\").filter(has_text=re.compile(r\"^Latest 4 Next 4$\")).nth(1)", )
    safe_action(page, page.locator("#event-filterId > .wr-20 > esp-multiselect-dropdown > .multiselect-dropdown > div > .w-100 > .d-flex.align-items-center > .dropdown-caret"), 'click', "locator(\"#event-filterId > .wr-20 > esp-multiselect-dropdown > .multiselect-dropdown > div > .w-100 > .d-flex.align-items-center > .dropdown-caret\")", )
    safe_action(page, page.locator(".d-flex.flex-column.justify-content-center").first, 'click', "locator(\".d-flex.flex-column.justify-content-center\").first", )
    safe_action(page, page.get_by_role("textbox", name="Search"), 'click', "get_by_role(\"textbox\", name=\"Search\")", )
    safe_action(page, page.get_by_role("textbox", name="Search"), 'fill', "get_by_role(\"textbox\", name=\"Search\")", "TLC")
    safe_action(page, page.locator(".icon.d-flex.pointer.zeb-close"), 'click', "locator(\".icon.d-flex.pointer.zeb-close\")", )
    safe_action(page, page.locator(".not-allowed > .w-100 > .d-flex.align-items-center > .dropdown-caret").first, 'click', "locator(\".not-allowed > .w-100 > .d-flex.align-items-center > .dropdown-caret\").first", )
    safe_action(page, page.locator("#ad-location-filterId > .wr-20 > esp-multiselect-dropdown > .multiselect-dropdown > div > .w-100 > .d-flex.align-items-center > .dropdown-caret"), 'click', "locator(\"#ad-location-filterId > .wr-20 > esp-multiselect-dropdown > .multiselect-dropdown > div > .w-100 > .d-flex.align-items-center > .dropdown-caret\")", )
    safe_action(page, page.locator(".d-flex.flex-column.justify-content-center").first, 'click', "locator(\".d-flex.flex-column.justify-content-center\").first", )
    safe_action(page, page.locator(".d-flex.flex-column.justify-content-center").first, 'click', "locator(\".d-flex.flex-column.justify-content-center\").first", )
    safe_action(page, page.locator("#ad-location-filterId > .wr-20 > esp-multiselect-dropdown > .multiselect-dropdown > div > .w-100 > .d-flex.align-items-center > .dropdown-caret"), 'click', "locator(\"#ad-location-filterId > .wr-20 > esp-multiselect-dropdown > .multiselect-dropdown > div > .w-100 > .d-flex.align-items-center > .dropdown-caret\")", )
    safe_action(page, page.locator("#segment-filterId > .wr-20 > esp-multiselect-dropdown > .multiselect-dropdown > div > .w-100 > .d-flex.align-items-center > .dropdown-caret"), 'click', "locator(\"#segment-filterId > .wr-20 > esp-multiselect-dropdown > .multiselect-dropdown > div > .w-100 > .d-flex.align-items-center > .dropdown-caret\")", )
    safe_action(page, page.locator(".d-flex.flex-column.justify-content-center").first, 'click', "locator(\".d-flex.flex-column.justify-content-center\").first", )
    safe_action(page, page.locator(".d-flex.flex-column.justify-content-center").first, 'click', "locator(\".d-flex.flex-column.justify-content-center\").first", )
    safe_action(page, page.locator("#segment-filterId > .wr-20 > esp-multiselect-dropdown > .multiselect-dropdown > div > .w-100 > .d-flex.align-items-center > .dropdown-caret"), 'click', "locator(\"#segment-filterId > .wr-20 > esp-multiselect-dropdown > .multiselect-dropdown > div > .w-100 > .d-flex.align-items-center > .dropdown-caret\")", )
    safe_action(page, page.locator("#vendor-filterId > .wr-20 > esp-multiselect-dropdown > .multiselect-dropdown > div > .w-100"), 'click', "locator(\"#vendor-filterId > .wr-20 > esp-multiselect-dropdown > .multiselect-dropdown > div > .w-100\")", )
    safe_action(page, page.locator(".d-flex.flex-column.justify-content-center").first, 'click', "locator(\".d-flex.flex-column.justify-content-center\").first", )
    safe_action(page, page.locator(".d-flex.dropdown-option.align-items-center.p-v-5.p-l-32 > .d-flex").first, 'click', "locator(\".d-flex.dropdown-option.align-items-center.p-v-5.p-l-32 > .d-flex\").first", )
    safe_action(page, page.locator(".overflow-auto > div:nth-child(2) > .d-flex"), 'click', "locator(\".overflow-auto > div:nth-child(2) > .d-flex\")", )
    safe_action(page, page.locator(".d-flex.flex-column.justify-content-center").first, 'click', "locator(\".d-flex.flex-column.justify-content-center\").first", )
    safe_action(page, page.locator("#vendor-filterId > .wr-20 > esp-multiselect-dropdown > .multiselect-dropdown > div > .w-100 > .d-flex.align-items-center > .dropdown-caret"), 'click', "locator(\"#vendor-filterId > .wr-20 > esp-multiselect-dropdown > .multiselect-dropdown > div > .w-100 > .d-flex.align-items-center > .dropdown-caret\")", )
    safe_action(page, page.locator("button").filter(has_text=re.compile(r"^Apply$")), 'click', "locator(\"button\").filter(has_text=re.compile(r\"^Apply$\"))", )
    safe_action(page, page.locator(".ellipses > esp-multiselect-dropdown > .multiselect-dropdown > div > .w-100 > .d-flex.align-items-center > .dropdown-caret"), 'click', "locator(\".ellipses > esp-multiselect-dropdown > .multiselect-dropdown > div > .w-100 > .d-flex.align-items-center > .dropdown-caret\")", )
    safe_action(page, page.locator(".d-flex.flex-column.justify-content-center").first, 'click', "locator(\".d-flex.flex-column.justify-content-center\").first", )
    safe_action(page, page.locator(".d-flex.flex-column.justify-content-center.font-size-10.align-items-center.checkbox-v2.m-r-10.zeb-check").first, 'click', "locator(\".d-flex.flex-column.justify-content-center.font-size-10.align-items-center.checkbox-v2.m-r-10.zeb-check\").first", )
    safe_action(page, page.locator(".d-flex.flex-column.justify-content-center.font-size-10.align-items-center.checkbox-v2.m-r-10.zeb-check").first, 'click', "locator(\".d-flex.flex-column.justify-content-center.font-size-10.align-items-center.checkbox-v2.m-r-10.zeb-check\").first", )
    safe_action(page, page.locator(".d-flex.flex-column.justify-content-center.font-size-10.align-items-center.checkbox-v2.m-r-10.zeb-check").first, 'click', "locator(\".d-flex.flex-column.justify-content-center.font-size-10.align-items-center.checkbox-v2.m-r-10.zeb-check\").first", )
    safe_action(page, page.locator(".d-flex.flex-column.justify-content-center.font-size-10.align-items-center.checkbox-v2.m-r-10.zeb-check").first, 'click', "locator(\".d-flex.flex-column.justify-content-center.font-size-10.align-items-center.checkbox-v2.m-r-10.zeb-check\").first", )
    safe_action(page, page.locator(".d-flex.flex-column.justify-content-center").first, 'click', "locator(\".d-flex.flex-column.justify-content-center\").first", )
    safe_action(page, page.locator(".d-flex.flex-column.justify-content-center.font-size-10.align-items-center.checkbox-v2.m-r-10.deselected").first, 'click', "locator(\".d-flex.flex-column.justify-content-center.font-size-10.align-items-center.checkbox-v2.m-r-10.deselected\").first", )
    safe_action(page, page.locator(".d-flex.flex-column.justify-content-center.font-size-10.align-items-center.checkbox-v2.m-r-10.deselected").first, 'click', "locator(\".d-flex.flex-column.justify-content-center.font-size-10.align-items-center.checkbox-v2.m-r-10.deselected\").first", )
    safe_action(page, page.locator(".d-flex.flex-column.justify-content-center.font-size-10.align-items-center.checkbox-v2.m-r-10.deselected").first, 'click', "locator(\".d-flex.flex-column.justify-content-center.font-size-10.align-items-center.checkbox-v2.m-r-10.deselected\").first", )
    safe_action(page, page.locator(".overflow-auto > div:nth-child(5)"), 'click', "locator(\".overflow-auto > div:nth-child(5)\")", )
    safe_action(page, page.locator(".ellipses > esp-multiselect-dropdown > .multiselect-dropdown > div > .w-100 > .d-flex.align-items-center > .dropdown-caret"), 'click', "locator(\".ellipses > esp-multiselect-dropdown > .multiselect-dropdown > div > .w-100 > .d-flex.align-items-center > .dropdown-caret\")", )
    safe_action(page, page.locator(".wr-20.font-weight-normal > esp-multiselect-dropdown > .multiselect-dropdown > div > .w-100 > .d-flex.align-items-center > .dropdown-caret"), 'click', "locator(\".wr-20.font-weight-normal > esp-multiselect-dropdown > .multiselect-dropdown > div > .w-100 > .d-flex.align-items-center > .dropdown-caret\")", )
    safe_action(page, page.locator(".d-flex.flex-column.justify-content-center").first, 'click', "locator(\".d-flex.flex-column.justify-content-center\").first", )
    safe_action(page, page.locator(".d-flex.flex-column.justify-content-center").first, 'click', "locator(\".d-flex.flex-column.justify-content-center\").first", )
    safe_action(page, page.locator(".wr-20.font-weight-normal > esp-multiselect-dropdown > .multiselect-dropdown > div > .w-100 > .d-flex.align-items-center > .dropdown-caret"), 'click', "locator(\".wr-20.font-weight-normal > esp-multiselect-dropdown > .multiselect-dropdown > div > .w-100 > .d-flex.align-items-center > .dropdown-caret\")", )
    safe_action(page, page.get_by_role("button", name="columns").nth(2), 'click', "get_by_role(\"button\", name=\"columns\").nth(2)", )
    safe_action(page, page.get_by_role("checkbox", name="Toggle All Columns Visibility"), 'uncheck', "get_by_role(\"checkbox\", name=\"Toggle All Columns Visibility\")", )
    safe_action(page, page.locator("#ag-6720 > .ag-column-panel > .ag-column-select > .ag-column-select-list > .ag-virtual-list-viewport > .ag-virtual-list-container > div > .ag-column-select-column").first, 'click', "locator(\"#ag-6720 > .ag-column-panel > .ag-column-select > .ag-column-select-list > .ag-virtual-list-viewport > .ag-virtual-list-container > div > .ag-column-select-column\").first", )
    safe_action(page, page.get_by_role("treeitem", name="/11/2026 Column").get_by_label("Press SPACE to toggle"), 'check', "get_by_role(\"treeitem\", name=\"/11/2026 Column\").get_by_label(\"Press SPACE to toggle\")", )
    safe_action(page, page.get_by_role("treeitem", name="/18/2026 Column").get_by_label("Press SPACE to toggle"), 'check', "get_by_role(\"treeitem\", name=\"/18/2026 Column\").get_by_label(\"Press SPACE to toggle\")", )
    safe_action(page, page.get_by_role("treeitem", name="/25/2026 Column").get_by_label("Press SPACE to toggle"), 'check', "get_by_role(\"treeitem\", name=\"/25/2026 Column\").get_by_label(\"Press SPACE to toggle\")", )
    safe_action(page, page.get_by_role("treeitem", name="02/01/2026 Column").get_by_label("Press SPACE to toggle visibility (hidden)"), 'check', "get_by_role(\"treeitem\", name=\"02/01/2026 Column\").get_by_label(\"Press SPACE to toggle visibility (hidden)\")", )
    safe_action(page, page.get_by_role("treeitem", name="/08/2026 Column").get_by_label("Press SPACE to toggle visibility (hidden)"), 'check', "get_by_role(\"treeitem\", name=\"/08/2026 Column\").get_by_label(\"Press SPACE to toggle visibility (hidden)\")", )
    safe_action(page, page.get_by_role("checkbox", name="Toggle All Columns Visibility"), 'check', "get_by_role(\"checkbox\", name=\"Toggle All Columns Visibility\")", )
    safe_action(page, page.get_by_role("button", name="columns").nth(2), 'click', "get_by_role(\"button\", name=\"columns\").nth(2)", )
    safe_action(page, page.locator(".wr-20.font-weight-normal > esp-multiselect-dropdown > .multiselect-dropdown > div > .w-100 > .d-flex.align-items-center > .dropdown-caret"), 'click', "locator(\".wr-20.font-weight-normal > esp-multiselect-dropdown > .multiselect-dropdown > div > .w-100 > .d-flex.align-items-center > .dropdown-caret\")", )
    safe_action(page, page.locator(".d-flex.flex-column.justify-content-center").first, 'click', "locator(\".d-flex.flex-column.justify-content-center\").first", )
    safe_action(page, page.locator(".d-flex.flex-column.justify-content-center").first, 'click', "locator(\".d-flex.flex-column.justify-content-center\").first", )
    safe_action(page, page.locator(".d-flex.dropdown-option.align-items-center.p-v-5.p-l-32 > .d-flex").first, 'click', "locator(\".d-flex.dropdown-option.align-items-center.p-v-5.p-l-32 > .d-flex\").first", )
    safe_action(page, page.locator(".d-flex.dropdown-option.align-items-center.p-v-5.p-l-32 > .d-flex").first, 'click', "locator(\".d-flex.dropdown-option.align-items-center.p-v-5.p-l-32 > .d-flex\").first", )
    safe_action(page, page.locator(".d-flex.dropdown-option.align-items-center.p-v-5.p-l-32 > .d-flex").first, 'click', "locator(\".d-flex.dropdown-option.align-items-center.p-v-5.p-l-32 > .d-flex\").first", )
    safe_action(page, page.locator(".overflow-auto > div:nth-child(4) > .d-flex"), 'click', "locator(\".overflow-auto > div:nth-child(4) > .d-flex\")", )
    safe_action(page, page.locator("div:nth-child(5) > .d-flex"), 'click', "locator(\"div:nth-child(5) > .d-flex\")", )
    safe_action(page, page.get_by_text("Maximum User Forecast").nth(1), 'click', "get_by_text(\"Maximum User Forecast\").nth(1)", )
    safe_action(page, page.get_by_text("Average User Forecast").nth(1), 'click', "get_by_text(\"Average User Forecast\").nth(1)", )
    safe_action(page, page.locator(".overflow-auto > div:nth-child(8)"), 'click', "locator(\".overflow-auto > div:nth-child(8)\")", )
    safe_action(page, page.locator(".d-flex.dropdown-option").first, 'click', "locator(\".d-flex.dropdown-option\").first", )
    safe_action(page, page.locator(".wr-20.font-weight-normal > esp-multiselect-dropdown > .multiselect-dropdown > div > .w-100 > .d-flex.align-items-center > .dropdown-caret"), 'click', "locator(\".wr-20.font-weight-normal > esp-multiselect-dropdown > .multiselect-dropdown > div > .w-100 > .d-flex.align-items-center > .dropdown-caret\")", )
    safe_action(page, page.locator("div:nth-child(3) > span > .align-middle"), 'click', "locator(\"div:nth-child(3) > span > .align-middle\")", )
    safe_action(page, page.locator(".ag-header-cell.ag-header-parent-hidden.ag-header-cell-sortable.ag-header-background.ag-focus-managed.ag-header-active > .ag-header-cell-comp-wrapper > .ag-cell-label-container > .ag-header-icon > .filter-icon"), 'click', "locator(\".ag-header-cell.ag-header-parent-hidden.ag-header-cell-sortable.ag-header-background.ag-focus-managed.ag-header-active > .ag-header-cell-comp-wrapper > .ag-cell-label-container > .ag-header-icon > .filter-icon\")", )
    safe_action(page, page.get_by_label("Column Filter").get_by_role("button", name="Apply"), 'click', "get_by_label(\"Column Filter\").get_by_role(\"button\", name=\"Apply\")", )
    safe_action(page, page.get_by_role("button", name="columns").nth(3), 'click', "get_by_role(\"button\", name=\"columns\").nth(3)", )
    safe_action(page, page.get_by_role("checkbox", name="Toggle All Columns Visibility"), 'uncheck', "get_by_role(\"checkbox\", name=\"Toggle All Columns Visibility\")", )
    safe_action(page, page.get_by_role("treeitem", name="Start Week Column").get_by_label("Press SPACE to toggle"), 'check', "get_by_role(\"treeitem\", name=\"Start Week Column\").get_by_label(\"Press SPACE to toggle\")", )
    safe_action(page, page.get_by_role("treeitem", name="End Week Column").get_by_label("Press SPACE to toggle"), 'check', "get_by_role(\"treeitem\", name=\"End Week Column\").get_by_label(\"Press SPACE to toggle\")", )
    safe_action(page, page.get_by_role("treeitem", name="Clone Column").get_by_label("Press SPACE to toggle"), 'check', "get_by_role(\"treeitem\", name=\"Clone Column\").get_by_label(\"Press SPACE to toggle\")", )
    safe_action(page, page.get_by_role("treeitem", name="Event Column").get_by_label("Press SPACE to toggle visibility (hidden)"), 'check', "get_by_role(\"treeitem\", name=\"Event Column\").get_by_label(\"Press SPACE to toggle visibility (hidden)\")", )
    safe_action(page, page.get_by_role("treeitem", name="Market Column").get_by_label("Press SPACE to toggle visibility (hidden)"), 'check', "get_by_role(\"treeitem\", name=\"Market Column\").get_by_label(\"Press SPACE to toggle visibility (hidden)\")", )
    safe_action(page, page.get_by_role("treeitem", name="Count of Stores Column").get_by_label("Press SPACE to toggle visibility (hidden)"), 'check', "get_by_role(\"treeitem\", name=\"Count of Stores Column\").get_by_label(\"Press SPACE to toggle visibility (hidden)\")", )
    safe_action(page, page.get_by_role("treeitem", name="Spot Column").get_by_label("Press SPACE to toggle visibility (hidden)"), 'check', "get_by_role(\"treeitem\", name=\"Spot Column\").get_by_label(\"Press SPACE to toggle visibility (hidden)\")", )
    safe_action(page, page.get_by_role("checkbox", name="Toggle All Columns Visibility"), 'check', "get_by_role(\"checkbox\", name=\"Toggle All Columns Visibility\")", )
    safe_action(page, page.get_by_role("button", name="columns").nth(3), 'click', "get_by_role(\"button\", name=\"columns\").nth(3)", )
    safe_action(page, page.locator("a").filter(has_text="2").nth(2), 'click', "locator(\"a\").filter(has_text=\"2\").nth(2)", )
    safe_action(page, page.locator("a").filter(has_text="3").nth(2), 'click', "locator(\"a\").filter(has_text=\"3\").nth(2)", )
    safe_action(page, page.locator("div:nth-child(7) > div > .componentParentWrapper > esp-grid-container > esp-card-component > .card-container > .card-content > esp-row-dimentional-grid > div > #paginationId > esp-pagination-v2 > .d-flex.w-100 > .pagination-pager > .pagination-first"), 'click', "locator(\"div:nth-child(7) > div > .componentParentWrapper > esp-grid-container > esp-card-component > .card-container > .card-content > esp-row-dimentional-grid > div > #paginationId > esp-pagination-v2 > .d-flex.w-100 > .pagination-pager > .pagination-first\")", )

    # ---------------------
    context.close()
    browser.close()


with sync_playwright() as playwright:
    run(playwright)
