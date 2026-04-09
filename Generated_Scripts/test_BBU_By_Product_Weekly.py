
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

def safe_action(page: Page, locator, action_name: str, description: str, *action_args, **action_kwargs):
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
            action_func(*action_args, **action_kwargs)
        else:
            if action_name == 'goto': page.goto(*action_args, **action_kwargs)
                
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
def test_initial_navigation_to_executive_dashboard(shared_page: Page):
    safe_action(
        shared_page.goto,
        "https://stage.bbu.esp.antuit.ai/dp/demand-planning/executive-dashboard?workbookId=4&tabIndex=2",
        "Navigate to the specified URL for the 'Executive Dashboard' in the demand planning application."
    )

@pytest.mark.order(4)
def test_column_configuration___product_total(shared_page: Page):
    safe_action(
        shared_page.locator("esp-card-component").filter(has_text="Product Total columns (0)").get_by_role("button").click,
        "Click on the 'Product Total columns (0)' button to open the column configuration panel."
    )
    safe_action(
        shared_page.get_by_role("treeitem", name="System Forecast Total (Plan Week) Column").get_by_label("Press SPACE to toggle").uncheck,
        "Uncheck the 'System Forecast Total (Plan Week)' column to hide it from the view."
    )
    safe_action(
        shared_page.get_by_role("treeitem", name="System Forecast Base (Plan").get_by_label("Press SPACE to toggle").uncheck,
        "Uncheck the 'System Forecast Base (Plan)' column to hide it from the view."
    )
    safe_action(
        shared_page.get_by_role("treeitem", name="System Forecast Promotion (").get_by_label("Press SPACE to toggle").uncheck,
        "Uncheck the 'System Forecast Promotion (' column to hide it from the view."
    )
    safe_action(
        shared_page.locator("div:nth-child(3) > .ag-column-select-column").click,
        "Click on the third column selector in the configuration panel to modify its settings."
    )
    safe_action(
        shared_page.get_by_role("treeitem", name="System Forecast Promotion (").get_by_label("Press SPACE to toggle").uncheck,
        "Uncheck the 'System Forecast Promotion (' column again to ensure it is hidden."
    )
    safe_action(
        shared_page.get_by_role("checkbox", name="Toggle All Columns Visibility").check,
        "Check the 'Toggle All Columns Visibility' checkbox to make all columns visible."
    )
    safe_action(
        shared_page.locator(".pointer.zeb-adjustments").first.click,
        "Click on the first adjustment option to apply changes to the column configuration."
    )
    safe_action(
        shared_page.locator("div").filter(has_text=re.compile(r"^Save Preference$")).nth(1).click,
        "Click on the 'Save Preference' button to save the updated column configuration."
    )

@pytest.mark.order(5)
def test_file_download___executive_dashboard(shared_page: Page):
    safe_action(
        lambda: shared_page.expect_download(lambda download_info: shared_page.locator(".icon-color-toolbar-active.zeb-download-underline").first.click()),
        "Set up an expectation to handle a file download triggered by clicking the first download button (identified by '.icon-color-toolbar-active.zeb-download-underline') and capture the downloaded file information for further processing or validation."
    )

@pytest.mark.order(6)
def test_reset_preferences_and_navigate_to_products_tab(shared_page: Page):
    safe_action(
        lambda: shared_page.locator(".pointer.zeb-adjustments").first.click(),
        "Click on the first adjustments button (identified by '.pointer.zeb-adjustments') to open the adjustments menu."
    )
    safe_action(
        lambda: shared_page.get_by_text("Reset Preference").click(),
        "Click on the 'Reset Preference' option to reset the preferences to their default state."
    )
    safe_action(
        lambda: shared_page.get_by_text("Products").click(),
        "Click on the 'Products' tab to access the product configuration section."
    )

@pytest.mark.order(7)
def test_column_configuration___products(shared_page: Page):
    safe_action(
        lambda: shared_page.locator("esp-card-component").filter(has_text="Products columns (0)").get_by_role("button").click(),
        "Open the 'Products columns' configuration menu by clicking the button within the 'esp-card-component' element."
    )
    safe_action(
        lambda: shared_page.get_by_role("checkbox", name="Toggle All Columns Visibility").uncheck(),
        "Uncheck the 'Toggle All Columns Visibility' checkbox to hide all columns initially."
    )
    safe_action(
        lambda: shared_page.get_by_role("treeitem", name="System Forecast Total (Plan Week) Column").get_by_label("Press SPACE to toggle visibility (hidden)").check(),
        "Enable visibility for the 'System Forecast Total (Plan Week)' column by checking its corresponding checkbox."
    )
    safe_action(
        lambda: shared_page.get_by_role("treeitem", name="System Forecast Base (Plan Week) Column").get_by_label("Press SPACE to toggle visibility (hidden)").check(),
        "Enable visibility for the 'System Forecast Base (Plan Week)' column by checking its corresponding checkbox."
    )
    safe_action(
        lambda: shared_page.get_by_role("treeitem", name="System Forecast Promotion (Plan Week) Column").get_by_label("Press SPACE to toggle visibility (hidden)").check(),
        "Enable visibility for the 'System Forecast Promotion (Plan Week)' column by checking its corresponding checkbox."
    )
    safe_action(
        lambda: shared_page.get_by_role("treeitem", name="System Forecast Total (Plan+1").get_by_label("Press SPACE to toggle visibility (hidden)").check(),
        "Enable visibility for the 'System Forecast Total (Plan+1)' column by checking its corresponding checkbox."
    )
    safe_action(
        lambda: shared_page.get_by_role("treeitem", name="System Forecast Base (Plan+1").get_by_label("Press SPACE to toggle visibility (hidden)").check(),
        "Enable visibility for the 'System Forecast Base (Plan+1)' column by checking its corresponding checkbox."
    )
    safe_action(
        lambda: shared_page.get_by_role("treeitem", name="System Forecast Promotion (Plan+1 Week) Column").get_by_label("Press SPACE to toggle visibility (hidden)").check(),
        "Enable visibility for the 'System Forecast Promotion (Plan+1 Week)' column by checking its corresponding checkbox."
    )
    safe_action(
        lambda: shared_page.get_by_role("treeitem", name="Week Gross Units Average Column").get_by_label("Press SPACE to toggle visibility (hidden)").check(),
        "Enable visibility for the 'Week Gross Units Average' column by checking its corresponding checkbox."
    )
    safe_action(
        lambda: shared_page.get_by_role("treeitem", name="6 Week Aged Net Units Average Column", exact=True).get_by_label("Press SPACE to toggle visibility (hidden)").check(),
        "Enable visibility for the '6 Week Aged Net Units Average' column by checking its corresponding checkbox."
    )
    safe_action(
        lambda: shared_page.get_by_role("checkbox", name="Toggle All Columns Visibility").check(),
        "Recheck the 'Toggle All Columns Visibility' checkbox to ensure all selected columns are visible."
    )
    safe_action(
        lambda: shared_page.locator("div:nth-child(3) > #preference-iconId > .legend-font > .multiselect-dropdown > .pointer").click(),
        "Click on the preferences dropdown menu to access options for saving or resetting preferences."
    )
    safe_action(
        lambda: shared_page.locator("div").filter(has_text=re.compile(r"^Save Preference$")).nth(1).click(),
        "Select the 'Save Preference' option to save the current column visibility settings."
    )
    safe_action(
        lambda: shared_page.locator("div:nth-child(3) > #preference-iconId > .legend-font > .multiselect-dropdown > .pointer").click(),
        "Reopen the preferences dropdown menu to access the reset option."
    )
    safe_action(
        lambda: shared_page.get_by_text("Reset Preference").click(),
        "Select the 'Reset Preference' option to revert to the default column visibility settings."
    )

@pytest.mark.order(8)
def test_filter_and_pagination_actions(shared_page: Page):
    safe_action(
        lambda: shared_page.locator(".ag-header-icon.ag-header-cell-filter-button > .ag-icon").first.click(),
        "Click on the filter icon in the header to open the filter options for the column."
    )
    safe_action(
        lambda: shared_page.get_by_role("textbox", name="Filter Value").fill("BARCEL"),
        "Enter the filter value 'BARCEL' into the textbox to filter the column data."
    )
    safe_action(
        lambda: shared_page.get_by_role("button", name="Apply").click(),
        "Click on the 'Apply' button to apply the filter and update the displayed data."
    )
    safe_action(
        lambda: shared_page.locator(".ag-header-icon.ag-header-cell-filter-button > .ag-icon").first.click(),
        "Click on the filter icon in the header again to reopen the filter options."
    )
    safe_action(
        lambda: shared_page.get_by_role("button", name="Reset").click(),
        "Click on the 'Reset' button to clear the filter and revert the column data to its default state."
    )
    safe_action(
        lambda: shared_page.get_by_role("gridcell", name="Press Space to toggle row selection (unchecked)  ARNOLD-BRWNBRY-OROWT").get_by_label("Press Space to toggle row").check(),
        "Select the row with the name 'ARNOLD-BRWNBRY-OROWT' by toggling the checkbox in the grid cell."
    )
    safe_action(
        lambda: shared_page.locator("a").filter(has_text="2").click(),
        "Navigate to the second page of the table by clicking on the pagination link labeled '2'."
    )
    safe_action(
        lambda: shared_page.locator("a").filter(has_text="3").click(),
        "Navigate to the third page of the table by clicking on the pagination link labeled '3'."
    )

@pytest.mark.order(9)
def test_dropdown_and_multi_select_actions(shared_page: Page):
    safe_action(
        lambda: shared_page.get_by_role("listitem").filter(has_text=re.compile(r"^$")).nth(4).click(),
        "Click on the fourth item in the list to select it. The specific item is not clear from the screenshot or code."
    )
    safe_action(
        lambda: shared_page.locator(".dropdown-caret.p-l-16").first.click(),
        "Click on the first dropdown caret to open the dropdown menu."
    )
    safe_action(
        lambda: shared_page.locator("div").filter(has_text=re.compile(r"^View 20 row\(s\)$")).nth(1).click(),
        "Select the option 'View 20 row(s)' from the dropdown menu to adjust the number of rows displayed."
    )
    safe_action(
        lambda: shared_page.get_by_text("Filter").click(),
        "Click on the 'Filter' button to open the filter options."
    )
    safe_action(
        lambda: shared_page.locator(".w-100.p-h-16.p-v-8.dropdown-label.background-white > .d-flex.align-items-center > .dropdown-caret").click(),
        "Click on the dropdown caret within the filter section to open the time filter options."
    )
    safe_action(
        lambda: shared_page.locator("div").filter(has_text=re.compile(r"^Latest 5 Next 4$")).nth(1).click(),
        "Select the 'Latest 5 Next 4' option from the time filter dropdown."
    )
    safe_action(
        lambda: shared_page.locator(".w-100.p-h-16.p-v-8.dropdown-label.background-white > .d-flex.align-items-center > .dropdown-caret").click(),
        "Click on the dropdown caret within the filter section again to reopen the time filter options."
    )
    safe_action(
        lambda: shared_page.locator("div").filter(has_text=re.compile(r"^Latest 5 Next 12$")).nth(1).click(),
        "Select the 'Latest 5 Next 12' option from the time filter dropdown."
    )
    safe_action(
        lambda: shared_page.locator(".w-100.p-h-16.p-v-8.dropdown-label.background-white > .d-flex.align-items-center > .dropdown-caret").click(),
        "Click on the dropdown caret within the filter section again to reopen the time filter options."
    )
    safe_action(
        lambda: shared_page.locator("div").filter(has_text=re.compile(r"^Latest 13 Next 4$")).nth(1).click(),
        "Select the 'Latest 13 Next 4' option from the time filter dropdown."
    )
    safe_action(
        lambda: shared_page.locator(".w-100.p-h-16.p-v-8.dropdown-label.background-white > .d-flex.align-items-center > .dropdown-caret").click(),
        "Click on the dropdown caret within the filter section again to reopen the time filter options."
    )
    safe_action(
        lambda: shared_page.locator("div").filter(has_text=re.compile(r"^Latest 13 Next 12$")).nth(1).click(),
        "Select the 'Latest 13 Next 12' option from the time filter dropdown."
    )
    safe_action(
        lambda: shared_page.locator(".wr-20.font-weight-normal > esp-multiselect-dropdown > .multiselect-dropdown > div > .w-100 > .d-flex.align-items-center > .dropdown-caret").click(),
        "Click on the dropdown caret to open the multi-select dropdown menu."
    )
    safe_action(
        lambda: shared_page.locator(".d-flex.flex-column.justify-content-center").first.click(),
        "Click on the first option in the dropdown menu to select it. The specific option is not clear from the screenshot."
    )
    safe_action(
        lambda: shared_page.locator(".d-flex.dropdown-option.align-items-center.p-v-5.p-l-32 > .d-flex").first.click(),
        "Click on the first option under the 'dropdown-option' class to select it. The specific option is not clear from the screenshot."
    )
    safe_action(
        lambda: shared_page.locator(".overflow-auto > div:nth-child(2) > .d-flex").click(),
        "Click on the second option in the dropdown menu to select it. The specific option is not clear from the screenshot."
    )
    safe_action(
        lambda: shared_page.locator(".overflow-auto > div:nth-child(3) > .d-flex").click(),
        "Click on the third option in the dropdown menu to select it. The specific option is not clear from the screenshot."
    )
    safe_action(
        lambda: shared_page.locator(".overflow-auto > div:nth-child(4)").click(),
        "Click on the fourth option in the dropdown menu to select it. The specific option is not clear from the screenshot."
    )
    safe_action(
        lambda: shared_page.locator(".overflow-auto > div:nth-child(5)").click(),
        "Click on the fifth option in the dropdown menu to select it. The specific option is not clear from the screenshot."
    )
    safe_action(
        lambda: shared_page.locator(".overflow-auto > div:nth-child(6)").click(),
        "Click on the sixth option in the dropdown menu to select it. The specific option is not clear from the screenshot."
    )
    safe_action(
        lambda: shared_page.locator(".d-flex.flex-column.justify-content-center").first.click(),
        "Click on the first option in the dropdown menu again to deselect it. The specific option is not clear from the screenshot."
    )

@pytest.mark.order(10)
def test_weekly_summary_product_configuration(shared_page: Page):
    safe_action(
        lambda: shared_page.locator(".wr-20.font-weight-normal > esp-multiselect-dropdown > .multiselect-dropdown > div > .w-100 > .d-flex.align-items-center > .dropdown-caret").click(),
        "Click on the dropdown caret to open the multi-select dropdown menu for column visibility options."
    )
    safe_action(
        lambda: shared_page.locator("esp-card-component").filter(has_text="Weekly Summary Product:ARNOLD").get_by_role("button").click(),
        "Click on the button within the 'Weekly Summary Product:ARNOLD' card to expand or collapse the product details."
    )
    safe_action(
        lambda: shared_page.get_by_role("checkbox", name="Toggle All Columns Visibility").uncheck(),
        "Uncheck the 'Toggle All Columns Visibility' checkbox to hide all columns in the Weekly Summary table."
    )
    safe_action(
        lambda: shared_page.get_by_role("treeitem", name="-10-26 (44) Column").get_by_label("Press SPACE to toggle visibility (hidden)").check(),
        "Check the visibility of the column labeled '-10-26 (44)' by toggling its checkbox."
    )
    safe_action(
        lambda: shared_page.get_by_role("treeitem", name="-11-02 (45) Column").get_by_label("Press SPACE to toggle visibility (hidden)").check(),
        "Check the visibility of the column labeled '-11-02 (45)' by toggling its checkbox."
    )
    safe_action(
        lambda: shared_page.get_by_role("treeitem", name="-11-09 (46) Column").get_by_label("Press SPACE to toggle visibility (hidden)").check(),
        "Check the visibility of the column labeled '-11-09 (46)' by toggling its checkbox."
    )
    safe_action(
        lambda: shared_page.get_by_role("treeitem", name="-11-16 (47) Column").get_by_label("Press SPACE to toggle visibility (hidden)").check(),
        "Check the visibility of the column labeled '-11-16 (47)' by toggling its checkbox."
    )
    safe_action(
        lambda: shared_page.get_by_role("checkbox", name="Toggle All Columns Visibility").check(),
        "Recheck the 'Toggle All Columns Visibility' checkbox to make all columns visible again in the Weekly Summary table."
    )
    safe_action(
        lambda: shared_page.locator("esp-card-component").filter(has_text="Weekly Summary Product:ARNOLD").get_by_role("button").click(),
        "Click on the button within the 'Weekly Summary Product:ARNOLD' card again to collapse the product details."
    )

@pytest.mark.order(11)
def test_preference_management_and_export_actions(shared_page: Page):
    safe_action(
        lambda: shared_page.locator("div:nth-child(4) > #preference-iconId > .legend-font > .multiselect-dropdown > .pointer").click(),
        "Click on the 'Preference' icon to open the dropdown menu for managing preferences."
    )
    safe_action(
        lambda: shared_page.get_by_text("Save Preference").click(),
        "Click on the 'Save Preference' button to save the current table preferences."
    )
    safe_action(
        lambda: shared_page.expect_download(lambda: shared_page.locator("div:nth-child(3) > #export-iconId > .icon-color-toolbar-active").click()),
        "Prepare to handle a file download triggered by the 'Export' icon click and store the downloaded file information."
    )
    safe_action(
        lambda: shared_page.locator("div:nth-child(4) > #preference-iconId > .legend-font > .multiselect-dropdown > .pointer").click(),
        "Click on the 'Preference' dropdown to open the menu for managing preferences."
    )
    safe_action(
        lambda: shared_page.get_by_text("Reset Preference").click(),
        "Select 'Reset Preference' from the dropdown to reset the table preferences to default."
    )
    safe_action(
        lambda: shared_page.get_by_text("-02-15 (08)").click(),
        "Click on the date '-02-15 (08)' to select it from the available options."
    )
    safe_action(
        lambda: shared_page.get_by_role("img").nth(5).click(),
        "Click on the fifth image element to initiate the column visibility settings."
    )
    safe_action(
        lambda: shared_page.locator("esp-card-component").filter(has_text="Event Details columns (0)").get_by_role("button").click(),
        "Click on the button within the 'Event Details columns (0)' card to open the column visibility options."
    )
    safe_action(
        lambda: shared_page.get_by_role("treeitem", name="Event Column").get_by_label("Press SPACE to toggle visibility (visible)").uncheck(),
        "Uncheck the 'Event Column' to hide it from the table."
    )
    safe_action(
        lambda: shared_page.get_by_role("treeitem", name="UPC 12 Column").get_by_label("Press SPACE to toggle visibility (visible)").uncheck(),
        "Uncheck the 'UPC 12 Column' to hide it from the table."
    )
    safe_action(
        lambda: shared_page.get_by_role("treeitem", name="Customer Level 2 Column").get_by_label("Press SPACE to toggle visibility (visible)").uncheck(),
        "Uncheck the 'Customer Level 2 Column' to hide it from the table."
    )
    safe_action(
        lambda: shared_page.get_by_role("treeitem", name="Start Date Column").get_by_label("Press SPACE to toggle visibility (visible)").uncheck(),
        "Uncheck the 'Start Date Column' to hide it from the table."
    )
    safe_action(
        lambda: shared_page.get_by_role("treeitem", name="End Date Column").get_by_label("Press SPACE to toggle visibility (visible)").uncheck(),
        "Uncheck the 'End Date Column' to hide it from the table."
    )
    safe_action(
        lambda: shared_page.get_by_role("checkbox", name="Toggle All Columns Visibility").check(),
        "Check the 'Toggle All Columns Visibility' checkbox to make all columns visible again."
    )
    safe_action(
        lambda: shared_page.locator(".col-12.m-t-16 > div > esp-grid-container > esp-card-component > .card-container > .title > .grid-icons-container > esp-grid-icons-component > .display-grid-icons > div:nth-child(2) > #preference-iconId > .legend-font > .multiselect-dropdown > .pointer").click(),
        "Click on the 'Preference' icon to open the dropdown menu for saving or resetting preferences."
    )
    safe_action(
        lambda: shared_page.get_by_text("Save Preference").click(),
        "Click on 'Save Preference' to save the current column visibility settings."
    )
    safe_action(
        lambda: shared_page.expect_download(lambda: shared_page.locator("div:nth-child(6) > div > esp-grid-container > esp-card-component > .card-container > .title > .grid-icons-container > esp-grid-icons-component > .display-grid-icons > div > #export-iconId > .icon-color-toolbar-active").click()),
        "Prepare to capture the download event triggered by the 'Export' icon click and store the downloaded file information."
    )

@pytest.mark.order(12)
def test_event_details_column_configuration(shared_page: Page):
    safe_action(
        lambda: shared_page.locator(".col-12.m-t-16 > div > esp-grid-container > esp-card-component > .card-container > .title > .grid-icons-container > esp-grid-icons-component > .display-grid-icons > div:nth-child(2) > #preference-iconId > .legend-font > .multiselect-dropdown > .pointer").click(),
        "Click on the 'Preference' icon to open the dropdown menu for resetting preferences."
    )
    safe_action(
        lambda: shared_page.get_by_text("Reset Preference").click(),
        "Click on 'Reset Preference' to revert to the default column visibility settings."
    )

@pytest.mark.order(13)
def test_filter_actions___scan_track(shared_page: Page):
    safe_action(
        lambda: shared_page.locator(".ag-header-cell.ag-header-parent-hidden.ag-header-cell-sortable.ag-header-background.ag-focus-managed.ag-header-active > .ag-header-cell-comp-wrapper > .ag-cell-label-container > .ag-header-icon > .ag-icon").click(),
        "Click on the filter icon in the column header to open the filter options."
    )
    safe_action(
        lambda: shared_page.get_by_role("textbox", name="Filter Value").fill("Scan Track"),
        "Enter 'Scan Track' into the filter textbox to filter the data based on this value."
    )
    safe_action(
        lambda: shared_page.get_by_role("button", name="Apply").click(),
        "Click on the 'Apply' button to apply the filter and update the displayed data."
    )
    safe_action(
        lambda: shared_page.locator(".ag-header-icon.ag-header-cell-filter-button.ag-filter-active > .ag-icon").click(),
        "Click on the active filter icon to open the filter options for resetting."
    )
    safe_action(
        lambda: shared_page.get_by_role("button", name="Reset").click(),
        "Click on the 'Reset' button to clear the applied filter and restore the unfiltered data."
    )

@pytest.mark.order(14)
def test_product_drill_down_and_context_menu_actions(shared_page: Page):
    safe_action(
        lambda: shared_page.get_by_text("Products").click(),
        "Click on the 'Products' tab to navigate to the product selection view."
    )
    safe_action(
        lambda: shared_page.locator("span").filter(has_text="ARNOLD-BRWNBRY-OROWT").first.dblclick(),
        "Double-click on the product 'ARNOLD-BRWNBRY-OROWT' to drill down into its details."
    )
    safe_action(
        lambda: shared_page.locator("span").filter(has_text="ABO COUNTRY").first.dblclick(),
        "Double-click on 'ABO COUNTRY' to further drill down into its details."
    )
    safe_action(
        lambda: shared_page.locator("span").filter(has_text="ABO COUNTRY").first.click(),
        "Click on 'ABO COUNTRY' to select it."
    )
    safe_action(
        lambda: shared_page.get_by_text("ABO COUNTRY").nth(1).dblclick(),
        "Double-click on the second instance of 'ABO COUNTRY' to drill down further."
    )
    safe_action(
        lambda: shared_page.locator("span").filter(has_text=re.compile(r"^OR CTY BTRMK WP 24Z-731300012500$")).click(button="right"),
        "Right-click on the product 'OR CTY BTRMK WP 24Z-731300012500' to open the context menu."
    )
    safe_action(
        lambda: shared_page.get_by_text("Drill up").click(),
        "Click on 'Drill up' from the context menu to navigate back to the previous level."
    )
    safe_action(
        lambda: shared_page.locator("span").filter(has_text="ABO COUNTRY").first.click(button="right"),
        "Right-click on 'ABO COUNTRY' to open the context menu again."
    )
    safe_action(
        lambda: shared_page.get_by_text("Drill up").click(),
        "Click on 'Drill up' from the context menu to navigate back another level."
    )
    safe_action(
        lambda: shared_page.locator("span").filter(has_text="ABO COUNTRY").first.click(button="right"),
        "Right-click on 'ABO COUNTRY' to open the context menu once more."
    )
    safe_action(
        lambda: shared_page.get_by_text("Drill up").click(),
        "Click on 'Drill up' from the context menu to return to the top level."
    )

@pytest.mark.order(15)
def test_row_selection_and_cleanup(shared_page: Page):
    safe_action(
        lambda: shared_page.get_by_role("gridcell", name="Press Space to toggle row selection (unchecked)  ARNOLD-BRWNBRY-OROWT").get_by_label("Press Space to toggle row").check(),
        "Select the row for the product 'ARNOLD-BRWNBRY-OROWT' by toggling the checkbox in the grid cell."
    )
    shared_page.close()
    shared_page.context.close()
    shared_page.browser.close()

