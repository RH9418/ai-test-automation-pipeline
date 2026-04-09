
import os
import sys
import time
import re
from datetime import datetime
import pytest
from playwright.sync_api import sync_playwright, Page, expect, TimeoutError

SCREENSHOT_DIR = "Test_Screenshots"
if not os.path.exists(SCREENSHOT_DIR): os.makedirs(SCREENSHOT_DIR)
screenshot_counter = 0

def capture_annotated_screenshot(page: Page, locator, full_action_description: str):
    '''Highlights element with a thick red box and glow, then captures screenshot.'''
    global screenshot_counter
    screenshot_counter += 1
    try:
        locator.scroll_into_view_if_needed()
        locator.wait_for(state='visible', timeout=5000)
        box = locator.bounding_box()
        if not box: return
            
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
        
        time.sleep(0.2)
        timestamp = datetime.now().strftime("%H-%M-%S")
        safe_filename = re.sub(r'[^a-z0-9]', '_', full_action_description.lower())[:40]
        filename = f"{timestamp}_{screenshot_counter:02d}_{safe_filename}.png"
        path = os.path.join(SCREENSHOT_DIR, filename)
        
        page.screenshot(path=path, full_page=False)
        print(f"   └── 📸 Screenshot saved: {path}")
        page.evaluate("() => { document.getElementById('ge-spotlight-box')?.remove(); document.getElementById('ge-spotlight-label')?.remove(); }")
    except Exception as e: print(f"   └── ⚠️ Screenshot Error: {e}")

def safe_action(page: Page, locator, action_name: str, description: str, *action_args):
    '''Performs action with spotlight screenshots and manual fallbacks.'''
    full_desc = f"{action_name.capitalize()}: {description}"
    if action_name == 'fill': full_desc += f" with '{action_args[0] if action_args else ''}'"
        
    try:
        if action_name == 'fill':
            print(f"\n⏸️ PAUSING FOR INPUT: About to fill '{description}'.")
            input("   └── Perform input manually in browser, then PRESS [ENTER] to continue...")
            page.wait_for_load_state('networkidle', timeout=5000)
            return

        if action_name in ['click', 'dblclick', 'check', 'uncheck', 'hover']:
            try: locator.hover(timeout=2000); time.sleep(0.3)
            except: pass
            
        if action_name == 'close':
            try: locator.close()
            except: pass
            print(f"✅ SUCCESS: {description} (Teardown handled by Pytest)")
            return

        if locator != page:
            capture_annotated_screenshot(page, locator, full_desc)
            action_func = getattr(locator, action_name)
            action_func(*action_args)
        else:
            if action_name == 'goto': page.goto(*action_args)
                
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


@pytest.mark.order(3)
def test_navigation_to_executive_dashboard(shared_page: Page):
    safe_action(
        shared_page.goto,
        "https://stage.wba.esp.antuit.ai/dp/demand-planning/executive-dashboard?workbookId=6&tabIndex=1",
        "Navigate to the Executive Dashboard page by opening the specified URL."
    )

@pytest.mark.order(4)
def test_alerts_filter_interaction(shared_page: Page):
    safe_action(
        shared_page.locator("#alerts-filterId").click,
        None,
        "Click on the 'Alerts' filter dropdown to expand the filter options."
    )
    safe_action(
        shared_page.locator("div").filter(has_text=re.compile(r"^MAPE$")).nth(1).click,
        None,
        "Select the 'MAPE' option from the dropdown list."
    )
    safe_action(
        shared_page.locator(".w-100.p-h-16.p-v-8.dropdown-label.background-white > .d-flex.align-items-center > .dropdown-caret").click,
        None,
        "Click on the dropdown caret to open the filter options again."
    )
    safe_action(
        shared_page.locator("div").filter(has_text=re.compile(r"^Under Bias$")).nth(1).click,
        None,
        "Select the 'Under Bias' option from the dropdown list."
    )
    safe_action(
        shared_page.locator(".w-100.p-h-16.p-v-8.dropdown-label.background-white > .d-flex.align-items-center > .dropdown-caret").click,
        None,
        "Click on the dropdown caret to open the filter options again."
    )
    safe_action(
        shared_page.locator("div").filter(has_text=re.compile(r"^Over Bias$")).nth(1).click,
        None,
        "Select the 'Over Bias' option from the dropdown list."
    )
    safe_action(
        shared_page.locator(".w-100.p-h-16.p-v-8.dropdown-label.background-white > .d-flex.align-items-center > .dropdown-caret").click,
        None,
        "Click on the dropdown caret to open the filter options again."
    )
    safe_action(
        shared_page.locator("div").filter(has_text=re.compile(r"^PVA$")).nth(1).click,
        None,
        "Select the 'PVA' option from the dropdown list."
    )
    safe_action(
        shared_page.locator(".w-100.p-h-16.p-v-8.dropdown-label.background-white > .d-flex.align-items-center > .dropdown-caret").click,
        None,
        "Click on the dropdown caret to open the filter options again."
    )
    safe_action(
        shared_page.locator("div").filter(has_text=re.compile(r"^SSIS$")).first.click,
        None,
        "Select the 'SSIS' option from the dropdown list."
    )

@pytest.mark.order(5)
def test_column_visibility_configuration(shared_page: Page):
    safe_action(
        shared_page.get_by_role("button", name="columns").click,
        None,
        "Click on the 'Columns' button to open the column visibility configuration panel."
    )
    safe_action(
        shared_page.get_by_role("checkbox", name="Toggle All Columns Visibility").uncheck,
        None,
        "Uncheck the 'Toggle All Columns Visibility' checkbox to hide all columns initially."
    )
    safe_action(
        shared_page.get_by_role("treeitem", name="Store Count Column").get_by_label("Press SPACE to toggle").check,
        None,
        "Check the 'Store Count Column' checkbox to make the 'Store Count' column visible."
    )
    safe_action(
        shared_page.get_by_role("treeitem", name="Product Count Column").get_by_label("Press SPACE to toggle").check,
        None,
        "Check the 'Product Count Column' checkbox to make the 'Product Count' column visible."
    )
    safe_action(
        shared_page.get_by_role("treeitem", name="Stability Column").get_by_label("Press SPACE to toggle").check,
        None,
        "Check the 'Stability Column' checkbox to make the 'Stability' column visible."
    )
    safe_action(
        shared_page.get_by_role("treeitem", name="SSIS Column").get_by_label("Press SPACE to toggle").check,
        None,
        "Check the 'SSIS Column' checkbox to make the 'SSIS' column visible."
    )
    safe_action(
        shared_page.get_by_role("treeitem", name="User Bias Column").get_by_label("Press SPACE to toggle").check,
        None,
        "Check the 'User Bias Column' checkbox to make the 'User Bias' column visible."
    )
    safe_action(
        shared_page.get_by_role("treeitem", name="System Bias Column").get_by_label("Press SPACE to toggle").check,
        None,
        "Check the 'System Bias Column' checkbox to make the 'System Bias' column visible."
    )
    safe_action(
        shared_page.get_by_role("treeitem", name="User MAPE Column").get_by_label("Press SPACE to toggle visibility (hidden)").check,
        None,
        "Check the 'User MAPE Column' checkbox to make the 'User MAPE' column visible."
    )
    safe_action(
        shared_page.get_by_role("treeitem", name="System MAPE Column").get_by_label("Press SPACE to toggle visibility (hidden)").check,
        None,
        "Check the 'System MAPE Column' checkbox to make the 'System MAPE' column visible."
    )
    safe_action(
        shared_page.get_by_role("treeitem", name="Planner Value Add Column").get_by_label("Press SPACE to toggle visibility (hidden)").check,
        None,
        "Check the 'Planner Value Add Column' checkbox to make the 'Planner Value Add' column visible."
    )
    safe_action(
        shared_page.get_by_role("treeitem", name="13W-Fcst Column").get_by_label("Press SPACE to toggle visibility (hidden)").check,
        None,
        "Check the '13W-Fcst Column' checkbox to make the '13W-Fcst' column visible."
    )

@pytest.mark.order(6)
def test_column_filtering_and_selection(shared_page: Page):
    safe_action(
        shared_page.locator("div:nth-child(11) > .ag-column-select-column").click,
        None,
        "Click on the column selector element to open the column selection panel."
    )
    safe_action(
        shared_page.get_by_role("textbox", name="Filter Columns Input").click,
        None,
        "Click on the 'Filter Columns Input' textbox to focus on it for entering a filter value."
    )
    safe_action(
        shared_page.get_by_role("textbox", name="Filter Columns Input").fill,
        "Store Count",
        "Fill the 'Filter Columns Input' textbox with the value 'Store Count' to filter the columns."
    )
    safe_action(
        shared_page.get_by_role("textbox", name="Filter Columns Input").press,
        "Enter",
        "Press 'Enter' to apply the filter and display the filtered column options."
    )
    safe_action(
        shared_page.get_by_role("checkbox", name="Press SPACE to toggle").check,
        None,
        "Check the checkbox for the filtered column to make it visible."
    )
    safe_action(
        shared_page.get_by_role("button", name="columns").click,
        None,
        "Click on the 'Columns' button to close the column selection panel."
    )

@pytest.mark.order(7)
def test_row_selection_and_filtering(shared_page: Page):
    safe_action(
        shared_page.get_by_role("row", name=" 002-SPIRITS").get_by_role("radio").check,
        None,
        "Select the radio button for the row with the name '002-SPIRITS' to apply row selection."
    )
    safe_action(
        shared_page.get_by_title("Filter").first.click,
        None,
        "Click on the first 'Filter' button to open the filter configuration for the selected column."
    )
    safe_action(
        shared_page.get_by_role("textbox", name="Filter Value").fill,
        "002-SPIRITS",
        "Fill the 'Filter Value' textbox with '002-SPIRITS' to filter rows based on this value."
    )
    safe_action(
        shared_page.get_by_label("Column Filter").get_by_role("button", name="Apply").click,
        None,
        "Click on the 'Apply' button to apply the column filter and update the displayed rows."
    )
    safe_action(
        shared_page.get_by_title("Filter").first.click,
        None,
        "Click on the first 'Filter' button to open the filter configuration for the selected column."
    )
    safe_action(
        shared_page.locator(".ag-icon.ag-icon-small-down").first.click,
        None,
        "Click on the dropdown icon to open the filter condition options."
    )
    safe_action(
        shared_page.get_by_role("option", name="Does not contain").click,
        None,
        "Select the 'Does not contain' option from the filter condition dropdown."
    )
    safe_action(
        shared_page.locator(".ag-icon.ag-icon-small-down").first.click,
        None,
        "Click on the dropdown icon again to open the filter condition options."
    )
    safe_action(
        shared_page.get_by_role("option", name="Equals").click,
        None,
        "Select the 'Equals' option from the filter condition dropdown."
    )
    safe_action(
        shared_page.locator(".ag-icon.ag-icon-small-down").first.click,
        None,
        "Click on the dropdown icon again to open the filter condition options."
    )
    safe_action(
        shared_page.get_by_role("option", name="Does not equal").click,
        None,
        "Select the 'Does not equal' option from the filter condition dropdown."
    )
    safe_action(
        shared_page.locator(".ag-icon.ag-icon-small-down").first.click,
        None,
        "Click on the dropdown icon again to open the filter condition options."
    )
    safe_action(
        shared_page.get_by_role("option", name="Begins with").click,
        None,
        "Select the 'Begins with' option from the filter condition dropdown."
    )
    safe_action(
        shared_page.locator(".ag-icon.ag-icon-small-down").first.click,
        None,
        "Click on the dropdown icon again to open the filter condition options."
    )
    safe_action(
        shared_page.get_by_role("option", name="Ends with").click,
        None,
        "Select the 'Ends with' option from the filter condition dropdown."
    )
    safe_action(
        shared_page.locator(".ag-icon.ag-icon-small-down").first.click,
        None,
        "Click on the dropdown icon again to open the filter condition options."
    )
    safe_action(
        shared_page.get_by_role("option", name="Does not contain").click,
        None,
        "Select the 'Does not contain' option from the filter condition dropdown again."
    )
    safe_action(
        shared_page.get_by_label("Column Filter").get_by_role("button", name="Apply").click,
        None,
        "Click on the 'Apply' button to apply the selected filter condition."
    )
    safe_action(
        shared_page.get_by_title("Filter").first.click,
        None,
        "Click on the first 'Filter' button to reopen the filter configuration."
    )
    safe_action(
        shared_page.get_by_role("button", name="Reset").click,
        None,
        "Click on the 'Reset' button to clear the applied filter and reset the filter configuration."
    )

@pytest.mark.order(8)
def test_pagination_interaction(shared_page: Page):
    safe_action(
        shared_page.locator("a").first.click,
        None,
        "Click on the first pagination link to navigate to the first page of the table."
    )
    safe_action(
        shared_page.locator("a").nth(1).click,
        None,
        "Click on the second pagination link to navigate to the second page of the table."
    )
    safe_action(
        shared_page.locator(".pagination-next > .zeb-chevron-right").first.click,
        None,
        "Click on the 'Next' button to navigate to the next page in the pagination."
    )
    safe_action(
        shared_page.locator(".zeb-chevron-left").first.click,
        None,
        "Click on the 'Previous' button to navigate to the previous page in the pagination."
    )
    safe_action(
        shared_page.locator(".zeb-nav-to-first").first.click,
        None,
        "Click on the 'First' button to navigate to the first page in the pagination."
    )
    safe_action(
        shared_page.locator(".d-flex > esp-multiselect-dropdown > .multiselect-dropdown > div > .w-100 > .d-flex.align-items-center > .dropdown-caret").first.click,
        None,
        "Click on the dropdown to open the row view options."
    )
    safe_action(
        shared_page.locator("div").filter(has_text=re.compile(r"^View 20 row\(s\)$")).first.click,
        None,
        "Select the option to view 20 rows per page."
    )
    safe_action(
        shared_page.locator(".d-flex > esp-multiselect-dropdown > .multiselect-dropdown > div > .w-100 > .d-flex.align-items-center > .dropdown-caret").first.click,
        None,
        "Click on the dropdown again to open the row view options."
    )
    safe_action(
        shared_page.locator("div").filter(has_text=re.compile(r"^View 50 row\(s\)$")).first.click,
        None,
        "Select the option to view 50 rows per page."
    )
    safe_action(
        shared_page.locator(".d-flex > esp-multiselect-dropdown > .multiselect-dropdown > div > .w-100 > .d-flex.align-items-center > .dropdown-caret").first.click,
        None,
        "Click on the dropdown again to open the row view options."
    )
    safe_action(
        shared_page.locator("div").filter(has_text=re.compile(r"^View 10 row\(s\)$")).nth(1).click,
        None,
        "Select the option to view 10 rows per page."
    )

@pytest.mark.order(9)
def test_detailed_row_interaction(shared_page: Page):
    safe_action(
        shared_page.get_by_text("Locations 20 rows out of 968").click,
        None,
        "Click on the text displaying the current row count and total rows to view detailed information."
    )
    safe_action(
        shared_page.locator(".pointer.chevron.zeb-chevron-right.m-r-12.collapsed").click,
        None,
        "Click on the collapsed chevron to expand the detailed view."
    )
    safe_action(
        shared_page.get_by_text("Locations", exact=True).click,
        None,
        "Click on the 'Locations' text to navigate to the Locations section."
    )
    safe_action(
        shared_page.get_by_role("row", name="Location").get_by_role("checkbox").uncheck,
        None,
        "Uncheck the checkbox in the row named 'Location'."
    )
    safe_action(
        shared_page.get_by_role("button", name="columns").nth(1).click,
        None,
        "Click on the 'Columns' button to open the column visibility options."
    )
    safe_action(
        shared_page.get_by_role("checkbox", name="Toggle All Columns Visibility").uncheck,
        None,
        "Uncheck the 'Toggle All Columns Visibility' checkbox."
    )
    safe_action(
        shared_page.get_by_role("treeitem", name="Store Count Column").get_by_label("Press SPACE to toggle").check,
        None,
        "Check the 'Store Count Column' checkbox to make it visible."
    )
    safe_action(
        shared_page.get_by_role("treeitem", name="Product Count Column").get_by_label("Press SPACE to toggle").check,
        None,
        "Check the 'Product Count Column' checkbox to make it visible."
    )
    safe_action(
        shared_page.get_by_role("treeitem", name="13W-Fcst Column").get_by_label("Press SPACE to toggle").check,
        None,
        "Check the '13W-Fcst Column' checkbox to make it visible."
    )
    safe_action(
        shared_page.get_by_role("textbox", name="Filter Columns Input").click,
        None,
        "Click on the 'Filter Columns Input' textbox to activate it."
    )
    safe_action(
        shared_page.get_by_role("textbox", name="Filter Columns Input").fill,
        "Pre",
        "Fill the 'Filter Columns Input' textbox with the text 'Pre'."
    )
    safe_action(
        shared_page.get_by_role("checkbox", name="Press SPACE to toggle").check,
        None,
        "Check the checkbox labeled 'Press SPACE to toggle' to apply the filter."
    )
    safe_action(
        shared_page.get_by_role("button", name="columns").nth(1).click,
        None,
        "Click on the 'Columns' button again to close the column visibility options."
    )

@pytest.mark.order(10)
def test_column_menu_filtering(shared_page: Page):
    safe_action(
        shared_page.locator("#ag-header-cell-menu-button > .filter-icon").click,
        None,
        "Click on the filter icon in the column menu to open the filter options."
    )
    safe_action(
        shared_page.get_by_role("textbox", name="Filter Value").click,
        None,
        "Click on the 'Filter Value' textbox to activate it."
    )
    safe_action(
        shared_page.get_by_role("textbox", name="Filter Value").fill,
        "CHICAGO",
        "Fill the 'Filter Value' textbox with the text 'CHICAGO'."
    )
    safe_action(
        shared_page.get_by_label("Column Menu").get_by_role("button", name="Apply").click,
        None,
        "Click on the 'Apply' button in the column menu to apply the filter."
    )
    safe_action(
        shared_page.get_by_role("gridcell", name="00162-1554 E 55TH ST-CHICAGO-").get_by_role("checkbox").check,
        None,
        "Check the checkbox in the grid cell labeled '00162-1554 E 55TH ST-CHICAGO-'."
    )
    safe_action(
        shared_page.locator("#ag-header-cell-menu-button > .filter-icon").click,
        None,
        "Click on the filter icon in the column menu again to reopen the filter options."
    )
    safe_action(
        shared_page.get_by_label("Column Menu").get_by_role("button", name="Reset").click,
        None,
        "Click on the 'Reset' button in the column menu to clear the filter."
    )

@pytest.mark.order(11)
def test_additional_row_and_pagination_interaction(shared_page: Page):
    safe_action(
        shared_page.get_by_role("row", name="Location").get_by_role("checkbox").check,
        None,
        "Check the checkbox in the row labeled 'Location'."
    )
    safe_action(
        shared_page.locator("a").filter(has_text="2").nth(1).click,
        None,
        "Click on the pagination link labeled '2'."
    )
    safe_action(
        shared_page.locator("a").filter(has_text="3").nth(1).click,
        None,
        "Click on the pagination link labeled '3'."
    )
    safe_action(
        shared_page.locator("div:nth-child(3) > esp-pagination-v2 > .d-flex.w-100 > .pagination-pager > .pagination-next > .zeb-chevron-right").click,
        None,
        "Click on the 'Next' button in the pagination controls."
    )
    safe_action(
        shared_page.locator("div:nth-child(3) > esp-pagination-v2 > .d-flex.w-100 > .pagination-pager > .pagination-previous > .zeb-chevron-left").click,
        None,
        "Click on the 'Previous' button in the pagination controls."
    )
    safe_action(
        shared_page.locator("div:nth-child(3) > esp-pagination-v2 > .d-flex.w-100 > .pagination-pager > .pagination-first > .zeb-nav-to-first").click,
        None,
        "Click on the 'First' button in the pagination controls."
    )

@pytest.mark.order(12)
def test_time_filter_interaction(shared_page: Page):
    safe_action(
        shared_page.get_by_text("Filter").nth(2).click,
        None,
        "Click on the 'Filter' button to expand the filter options."
    )
    safe_action(
        shared_page.locator("#time-filterId > .wr-20 > esp-multiselect-dropdown > .multiselect-dropdown > div > .w-100 > .d-flex.align-items-center > .dropdown-caret").click,
        None,
        "Click on the dropdown for the 'Time' filter to view available time range options."
    )
    safe_action(
        shared_page.locator("div").filter(has_text=re.compile(r"^Latest 4 Next 4$")).nth(1).click,
        None,
        "Select the 'Latest 4 Next 4' option from the 'Time' filter dropdown."
    )
    safe_action(
        shared_page.locator("#time-filterId > .wr-20 > esp-multiselect-dropdown > .multiselect-dropdown > div > .w-100 > .d-flex.align-items-center > .dropdown-caret").click,
        None,
        "Click on the dropdown for the 'Time' filter again to change the selection."
    )
    safe_action(
        shared_page.locator("div").filter(has_text=re.compile(r"^Latest 4 Next 13$")).nth(1).click,
        None,
        "Select the 'Latest 4 Next 13' option from the 'Time' filter dropdown."
    )
    safe_action(
        shared_page.locator("#time-filterId > .wr-20 > esp-multiselect-dropdown > .multiselect-dropdown > div > .w-100 > .d-flex.align-items-center > .dropdown-caret").click,
        None,
        "Click on the dropdown for the 'Time' filter again to change the selection."
    )
    safe_action(
        shared_page.locator("div").filter(has_text=re.compile(r"^Latest 13 Next 13$")).nth(1).click,
        None,
        "Select the 'Latest 13 Next 13' option from the 'Time' filter dropdown."
    )
    safe_action(
        shared_page.locator("#time-filterId > .wr-20 > esp-multiselect-dropdown > .multiselect-dropdown > div > .w-100 > .d-flex.align-items-center > .dropdown-caret").click,
        None,
        "Click on the dropdown for the 'Time' filter again to change the selection."
    )
    safe_action(
        shared_page.locator("div").filter(has_text=re.compile(r"^Latest 52 Next 52$")).first.click,
        None,
        "Select the 'Latest 52 Next 52' option from the 'Time' filter dropdown."
    )
    safe_action(
        shared_page.locator("#time-filterId > .wr-20 > esp-multiselect-dropdown > .multiselect-dropdown > div > .w-100 > .d-flex.align-items-center > .dropdown-caret").click,
        None,
        "Click on the dropdown for the 'Time' filter again to change the selection."
    )
    safe_action(
        shared_page.locator("div").filter(has_text=re.compile(r"^Latest 104 Next 52$")).nth(1).click,
        None,
        "Select the 'Latest 104 Next 52' option from the 'Time' filter dropdown."
    )
    safe_action(
        shared_page.locator("#time-filterId > .wr-20 > esp-multiselect-dropdown > .multiselect-dropdown > div > .w-100 > .d-flex.align-items-center > .dropdown-caret").click,
        None,
        "Click on the dropdown for the 'Time' filter again to reset the selection."
    )
    safe_action(
        shared_page.locator("div").filter(has_text=re.compile(r"^Latest 4 Next 4$")).nth(1).click,
        None,
        "Select the 'Latest 4 Next 4' option from the 'Time' filter dropdown to reset the filter."
    )

@pytest.mark.order(13)
def test_event_filter_interaction(shared_page: Page):
    safe_action(
        shared_page.locator("#event-filterId > .wr-20 > esp-multiselect-dropdown > .multiselect-dropdown > div > .w-100 > .d-flex.align-items-center > .dropdown-caret").click,
        None,
        "Click on the dropdown for the 'Event' filter to view available event options."
    )
    safe_action(
        shared_page.locator(".d-flex.flex-column.justify-content-center").first.click,
        None,
        "Click on the first element in the list to expand the filter options."
    )
    safe_action(
        shared_page.get_by_role("textbox", name="Search").click,
        None,
        "Click on the 'Search' textbox to focus on it."
    )
    safe_action(
        shared_page.get_by_role("textbox", name="Search").fill,
        "TLC",
        "Fill the 'Search' textbox with the value 'TLC'."
    )
    safe_action(
        shared_page.locator(".icon.d-flex.pointer.zeb-close").click,
        None,
        "Click on the close icon to clear the search input."
    )

@pytest.mark.order(14)
def test_ad_location_filter_interaction(shared_page: Page):
    safe_action(
        shared_page.locator(".not-allowed > .w-100 > .d-flex.align-items-center > .dropdown-caret").first.click,
        None,
        "Click on the dropdown caret for the 'Ad Location' filter to expand the options."
    )
    safe_action(
        shared_page.locator("#ad-location-filterId > .wr-20 > esp-multiselect-dropdown > .multiselect-dropdown > div > .w-100 > .d-flex.align-items-center > .dropdown-caret").click,
        None,
        "Click on the dropdown caret for the 'Ad Location' filter again to view the options."
    )
    safe_action(
        shared_page.locator(".d-flex.flex-column.justify-content-center").first.click,
        None,
        "Click on the first element in the list to expand the filter options."
    )
    safe_action(
        shared_page.locator(".d-flex.flex-column.justify-content-center").first.click,
        None,
        "Click on the first element in the list again to expand the filter options."
    )
    safe_action(
        shared_page.locator("#ad-location-filterId > .wr-20 > esp-multiselect-dropdown > .multiselect-dropdown > div > .w-100 > .d-flex.align-items-center > .dropdown-caret").click,
        None,
        "Click on the dropdown caret for the 'Ad Location' filter to view the options again."
    )

@pytest.mark.order(15)
def test_segment_filter_interaction(shared_page: Page):
    safe_action(
        shared_page.locator("#segment-filterId > .wr-20 > esp-multiselect-dropdown > .multiselect-dropdown > div > .w-100 > .d-flex.align-items-center > .dropdown-caret").click,
        None,
        "Click on the dropdown caret for the 'Segment' filter to expand the options."
    )
    safe_action(
        shared_page.locator(".d-flex.flex-column.justify-content-center").first.click,
        None,
        "Click on the first element in the list to expand the filter options."
    )
    safe_action(
        shared_page.locator(".d-flex.flex-column.justify-content-center").first.click,
        None,
        "Click on the first element in the list again to expand the filter options."
    )
    safe_action(
        shared_page.locator("#segment-filterId > .wr-20 > esp-multiselect-dropdown > .multiselect-dropdown > div > .w-100 > .d-flex.align-items-center > .dropdown-caret").click,
        None,
        "Click on the dropdown caret for the 'Segment' filter to view the options again."
    )

@pytest.mark.order(16)
def test_vendor_filter_interaction(shared_page: Page):
    safe_action(
        shared_page.locator("#vendor-filterId > .wr-20 > esp-multiselect-dropdown > .multiselect-dropdown > div > .w-100").click,
        None,
        "Click on the dropdown for the 'Vendor' filter to expand the options."
    )
    safe_action(
        shared_page.locator(".d-flex.flex-column.justify-content-center").first.click,
        None,
        "Click on the first element in the list to expand the filter options."
    )
    safe_action(
        shared_page.locator(".d-flex.dropdown-option.align-items-center.p-v-5.p-l-32 > .d-flex").first.click,
        None,
        "Click on the first option in the 'Vendor' filter dropdown to select it."
    )
    safe_action(
        shared_page.locator(".overflow-auto > div:nth-child(2) > .d-flex").click,
        None,
        "Click on the second option in the 'Vendor' filter dropdown to select it."
    )
    safe_action(
        shared_page.locator(".d-flex.flex-column.justify-content-center").first.click,
        None,
        "Click on the first element in the list again to expand the filter options."
    )
    safe_action(
        shared_page.locator("#vendor-filterId > .wr-20 > esp-multiselect-dropdown > .multiselect-dropdown > div > .w-100 > .d-flex.align-items-center > .dropdown-caret").click,
        None,
        "Click on the dropdown caret for the 'Vendor' filter again to view the options."
    )
    safe_action(
        shared_page.locator("button").filter(has_text=re.compile(r"^Apply$")).click,
        None,
        "Click on the 'Apply' button to apply the selected filters."
    )

@pytest.mark.order(17)
def test_column_visibility_dropdown_interaction(shared_page: Page):
    safe_action(
        shared_page.locator(".ellipses > esp-multiselect-dropdown > .multiselect-dropdown > div > .w-100 > .d-flex.align-items-center > .dropdown-caret").click,
        None,
        "Click on the dropdown caret to expand the column visibility options."
    )
    safe_action(
        shared_page.locator(".d-flex.flex-column.justify-content-center").first.click,
        None,
        "Click on the first element in the list to expand the column visibility options."
    )
    safe_action(
        shared_page.locator(".d-flex.flex-column.justify-content-center.font-size-10.align-items-center.checkbox-v2.m-r-10.zeb-check").first.click,
        None,
        "Click on the first checkbox to select a column for visibility."
    )
    safe_action(
        shared_page.locator(".d-flex.flex-column.justify-content-center.font-size-10.align-items-center.checkbox-v2.m-r-10.zeb-check").first.click,
        None,
        "Click on the first checkbox again to deselect the column for visibility."
    )
    safe_action(
        shared_page.locator(".d-flex.flex-column.justify-content-center.font-size-10.align-items-center.checkbox-v2.m-r-10.zeb-check").first.click,
        None,
        "Click on the first checkbox again to reselect the column for visibility."
    )
    safe_action(
        shared_page.locator(".d-flex.flex-column.justify-content-center.font-size-10.align-items-center.checkbox-v2.m-r-10.zeb-check").first.click,
        None,
        "Click on the first checkbox again to toggle the column visibility off."
    )
    safe_action(
        shared_page.locator(".d-flex.flex-column.justify-content-center").first.click,
        None,
        "Click on the first element in the list again to collapse the column visibility options."
    )
    safe_action(
        shared_page.locator(".d-flex.flex-column.justify-content-center.font-size-10.align-items-center.checkbox-v2.m-r-10.deselected").first.click,
        None,
        "Click on the first deselected checkbox to select a column for visibility."
    )
    safe_action(
        shared_page.locator(".d-flex.flex-column.justify-content-center.font-size-10.align-items-center.checkbox-v2.m-r-10.deselected").first.click,
        None,
        "Click on the first deselected checkbox again to deselect the column for visibility."
    )
    safe_action(
        shared_page.locator(".d-flex.flex-column.justify-content-center.font-size-10.align-items-center.checkbox-v2.m-r-10.deselected").first.click,
        None,
        "Click on the first deselected checkbox again to reselect the column for visibility."
    )
    safe_action(
        shared_page.locator(".overflow-auto > div:nth-child(5)").click,
        None,
        "Click on the fifth element in the list to select a specific column for visibility."
    )
    safe_action(
        shared_page.locator(".ellipses > esp-multiselect-dropdown > .multiselect-dropdown > div > .w-100 > .d-flex.align-items-center > .dropdown-caret").click,
        None,
        "Click on the dropdown caret again to collapse the column visibility options."
    )

@pytest.mark.order(18)
def test_column_visibility_settings(shared_page: Page):
    safe_action(
        shared_page.locator(".wr-20.font-weight-normal > esp-multiselect-dropdown > .multiselect-dropdown > div > .w-100 > .d-flex.align-items-center > .dropdown-caret").click,
        None,
        "Click on the dropdown caret to expand the column visibility settings."
    )
    safe_action(
        shared_page.locator(".d-flex.flex-column.justify-content-center").first.click,
        None,
        "Click on the first element in the list to expand the column visibility options."
    )
    safe_action(
        shared_page.locator(".d-flex.flex-column.justify-content-center").first.click,
        None,
        "Click on the first element in the list again to collapse the column visibility options."
    )
    safe_action(
        shared_page.locator(".wr-20.font-weight-normal > esp-multiselect-dropdown > .multiselect-dropdown > div > .w-100 > .d-flex.align-items-center > .dropdown-caret").click,
        None,
        "Click on the dropdown caret again to collapse the column visibility settings."
    )
    safe_action(
        shared_page.get_by_role("button", name="columns").nth(2).click,
        None,
        "Click on the 'Columns' button to open the column visibility settings."
    )
    safe_action(
        shared_page.get_by_role("checkbox", name="Toggle All Columns Visibility").uncheck,
        None,
        "Uncheck the 'Toggle All Columns Visibility' checkbox to deselect all columns."
    )
    safe_action(
        shared_page.locator("#ag-6720 > .ag-column-panel > .ag-column-select > .ag-column-select-list > .ag-virtual-list-viewport > .ag-virtual-list-container > div > .ag-column-select-column").first.click,
        None,
        "Click on the first column in the list to select it for visibility."
    )
    safe_action(
        shared_page.get_by_role("treeitem", name="/11/2026 Column").get_by_label("Press SPACE to toggle").check,
        None,
        "Check the checkbox for the '/11/2026 Column' to make it visible."
    )
    safe_action(
        shared_page.get_by_role("treeitem", name="/18/2026 Column").get_by_label("Press SPACE to toggle").check,
        None,
        "Check the checkbox for the '/18/2026 Column' to make it visible."
    )
    safe_action(
        shared_page.get_by_role("treeitem", name="/25/2026 Column").get_by_label("Press SPACE to toggle").check,
        None,
        "Check the checkbox for the '/25/2026 Column' to make it visible."
    )
    safe_action(
        shared_page.get_by_role("treeitem", name="02/01/2026 Column").get_by_label("Press SPACE to toggle visibility (hidden)").check,
        None,
        "Check the checkbox for the '02/01/2026 Column' to make it visible."
    )
    safe_action(
        shared_page.get_by_role("treeitem", name="/08/2026 Column").get_by_label("Press SPACE to toggle visibility (hidden)").check,
        None,
        "Check the checkbox for the '/08/2026 Column' to make it visible."
    )
    safe_action(
        shared_page.get_by_role("checkbox", name="Toggle All Columns Visibility").check,
        None,
        "Check the 'Toggle All Columns Visibility' checkbox to select all columns."
    )
    safe_action(
        shared_page.get_by_role("button", name="columns").nth(2).click,
        None,
        "Click on the 'Columns' button again to close the column visibility settings."
    )

@pytest.mark.order(19)
def test_additional_dropdown_and_column_interaction(shared_page: Page):
    safe_action(
        shared_page.locator(".wr-20.font-weight-normal > esp-multiselect-dropdown > .multiselect-dropdown > div > .w-100 > .d-flex.align-items-center > .dropdown-caret").click,
        None,
        "Click on the dropdown caret to expand the additional dropdown."
    )
    safe_action(
        shared_page.locator(".d-flex.flex-column.justify-content-center").first.click,
        None,
        "Click on the first element in the dropdown list to expand options."
    )
    safe_action(
        shared_page.locator(".d-flex.flex-column.justify-content-center").first.click,
        None,
        "Click on the first element in the dropdown list again to collapse options."
    )
    safe_action(
        shared_page.locator(".d-flex.dropdown-option.align-items-center.p-v-5.p-l-32 > .d-flex").first.click,
        None,
        "Click on the first dropdown option to select it."
    )
    safe_action(
        shared_page.locator(".d-flex.dropdown-option.align-items-center.p-v-5.p-l-32 > .d-flex").first.click,
        None,
        "Click on the first dropdown option again to deselect it."
    )
    safe_action(
        shared_page.locator(".d-flex.dropdown-option.align-items-center.p-v-5.p-l-32 > .d-flex").first.click,
        None,
        "Click on the first dropdown option a third time to reselect it."
    )
    safe_action(
        shared_page.locator(".overflow-auto > div:nth-child(4) > .d-flex").click,
        None,
        "Click on the fourth element in the dropdown list."
    )
    safe_action(
        shared_page.locator("div:nth-child(5) > .d-flex").click,
        None,
        "Click on the fifth element in the dropdown list."
    )
    safe_action(
        shared_page.get_by_text("Maximum User Forecast").nth(1).click,
        None,
        "Click on the 'Maximum User Forecast' option."
    )
    safe_action(
        shared_page.get_by_text("Average User Forecast").nth(1).click,
        None,
        "Click on the 'Average User Forecast' option."
    )
    safe_action(
        shared_page.locator(".overflow-auto > div:nth-child(8)").click,
        None,
        "Click on the eighth element in the dropdown list."
    )
    safe_action(
        shared_page.locator(".d-flex.dropdown-option").first.click,
        None,
        "Click on the first dropdown option to interact with it."
    )
    safe_action(
        shared_page.locator(".wr-20.font-weight-normal > esp-multiselect-dropdown > .multiselect-dropdown > div > .w-100 > .d-flex.align-items-center > .dropdown-caret").click,
        None,
        "Click on the dropdown caret to collapse the additional dropdown."
    )
    safe_action(
        shared_page.locator("div:nth-child(3) > span > .align-middle").click,
        None,
        "Click on the third span element to interact with it."
    )
    safe_action(
        shared_page.locator(".ag-header-cell.ag-header-parent-hidden.ag-header-cell-sortable.ag-header-background.ag-focus-managed.ag-header-active > .ag-header-cell-comp-wrapper > .ag-cell-label-container > .ag-header-icon > .filter-icon").click,
        None,
        "Click on the filter icon in the header cell."
    )
    safe_action(
        shared_page.get_by_label("Column Filter").get_by_role("button", name="Apply").click,
        None,
        "Click on the 'Apply' button in the column filter."
    )
    safe_action(
        shared_page.get_by_role("button", name="columns").nth(3).click,
        None,
        "Click on the 'Columns' button to open the column visibility settings."
    )
    safe_action(
        shared_page.get_by_role("checkbox", name="Toggle All Columns Visibility").uncheck,
        None,
        "Uncheck the 'Toggle All Columns Visibility' checkbox to deselect all columns."
    )
    safe_action(
        shared_page.get_by_role("treeitem", name="Start Week Column").get_by_label("Press SPACE to toggle").check,
        None,
        "Check the checkbox for the 'Start Week Column' to make it visible."
    )
    safe_action(
        shared_page.get_by_role("treeitem", name="End Week Column").get_by_label("Press SPACE to toggle").check,
        None,
        "Check the checkbox for the 'End Week Column' to make it visible."
    )
    safe_action(
        shared_page.get_by_role("treeitem", name="Clone Column").get_by_label("Press SPACE to toggle").check,
        None,
        "Check the checkbox for the 'Clone Column' to make it visible."
    )
    safe_action(
        shared_page.get_by_role("treeitem", name="Event Column").get_by_label("Press SPACE to toggle visibility (hidden)").check,
        None,
        "Check the checkbox for the 'Event Column' to make it visible."
    )
    safe_action(
        shared_page.get_by_role("treeitem", name="Market Column").get_by_label("Press SPACE to toggle visibility (hidden)").check,
        None,
        "Check the checkbox for the 'Market Column' to make it visible."
    )
    safe_action(
        shared_page.get_by_role("treeitem", name="Count of Stores Column").get_by_label("Press SPACE to toggle visibility (hidden)").check,
        None,
        "Check the checkbox for the 'Count of Stores Column' to make it visible."
    )
    safe_action(
        shared_page.get_by_role("treeitem", name="Spot Column").get_by_label("Press SPACE to toggle visibility (hidden)").check,
        None,
        "Check the checkbox for the 'Spot Column' to make it visible."
    )
    safe_action(
        shared_page.get_by_role("checkbox", name="Toggle All Columns Visibility").check,
        None,
        "Check the 'Toggle All Columns Visibility' checkbox to select all columns."
    )
    safe_action(
        shared_page.get_by_role("button", name="columns").nth(3).click,
        None,
        "Click on the 'Columns' button again to close the column visibility settings."
    )
    safe_action(
        shared_page.locator("a").filter(has_text="2").nth(2).click,
        None,
        "Click on the pagination link for page 2."
    )
    safe_action(
        shared_page.locator("a").filter(has_text="3").nth(2).click,
        None,
        "Click on the pagination link for page 3."
    )
    safe_action(
        shared_page.locator("div:nth-child(7) > div > .componentParentWrapper > esp-grid-container > esp-card-component > .card-container > .card-content > esp-row-dimentional-grid > div > #paginationId > esp-pagination-v2 > .d-flex.w-100 > .pagination-pager > .pagination-first").click,
        None,
        "Click on the 'First Page' button in the pagination controls."
    )

