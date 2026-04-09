
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
def test_initial_navigation_to_dashboard(shared_page: Page):
    safe_action(
        shared_page.goto,
        "https://stage.bbu.esp.antuit.ai/dp/demand-planning/executive-dashboard?workbookId=4&tabIndex=1",
        "Navigate to the specified URL for the 'Executive Dashboard' in the demand planning application."
    )

@pytest.mark.order(4)
def test_filter_interactions(shared_page: Page):
    safe_action(
        shared_page.get_by_text("Filter").click,
        "Click on the 'Filter' button to open the filter options."
    )
    safe_action(
        shared_page.locator("#alerts-filterId").get_by_text("Alerts").click,
        "Select the 'Alerts' option from the filter dropdown."
    )
    safe_action(
        shared_page.locator(".dropdown-caret").first.click,
        "Click on the dropdown caret to expand the filter options."
    )
    safe_action(
        shared_page.locator("div").filter(has_text=re.compile(r"^Over Bias$")).nth(1).click,
        "Select the 'Over Bias' filter option from the dropdown."
    )
    safe_action(
        shared_page.locator(".dropdown-caret").first.click,
        "Click on the dropdown caret again to expand the filter options."
    )
    safe_action(
        shared_page.locator("div").filter(has_text=re.compile(r"^Under Bias$")).nth(1).click,
        "Select the 'Under Bias' filter option from the dropdown."
    )
    safe_action(
        shared_page.locator(".dropdown-caret").first.click,
        "Click on the dropdown caret again to expand the filter options."
    )
    safe_action(
        shared_page.locator("div").filter(has_text=re.compile(r"^MAPE$")).nth(1).click,
        "Select the 'MAPE' filter option from the dropdown."
    )
    safe_action(
        shared_page.locator(".dropdown-caret").first.click,
        "Click on the dropdown caret again to expand the filter options."
    )
    safe_action(
        shared_page.locator("div").filter(has_text=re.compile(r"^Stability$")).nth(1).click,
        "Select the 'Stability' filter option from the dropdown."
    )
    safe_action(
        shared_page.locator(".dropdown-caret").first.click,
        "Click on the dropdown caret again to expand the filter options."
    )
    safe_action(
        shared_page.locator("div").filter(has_text=re.compile(r"^FVA$")).nth(1).click,
        "Select the 'FVA' filter option from the dropdown."
    )

@pytest.mark.order(5)
def test_column_visibility_configuration(shared_page: Page):
    safe_action(
        shared_page.get_by_role("button", name="columns").click,
        "Click on the 'Columns' button to open the column visibility configuration panel."
    )
    safe_action(
        shared_page.get_by_role("checkbox", name="Toggle All Columns Visibility").check,
        "Check the 'Toggle All Columns Visibility' checkbox to make all columns visible."
    )
    safe_action(
        shared_page.get_by_role("treeitem", name="6W-Actuals Column").get_by_label("Press SPACE to toggle visibility (visible)").uncheck,
        "Uncheck the '6W-Actuals Column' checkbox to hide this specific column."
    )
    safe_action(
        shared_page.get_by_role("treeitem", name="User Bias Column").get_by_label("Press SPACE to toggle visibility (visible)").uncheck,
        "Uncheck the 'User Bias Column' checkbox to hide this specific column."
    )

@pytest.mark.order(6)
def test_preferences_and_download_handling(shared_page: Page):
    safe_action(
        shared_page.locator(".pointer.zeb-adjustments").click,
        "Click on the 'Adjustments' button to open the preferences menu."
    )
    safe_action(
        shared_page.get_by_text("Save Preference").click,
        "Click on 'Save Preference' to save the current column visibility settings."
    )
    safe_action(
        lambda: shared_page.expect_download(lambda: shared_page.locator(".icon-color-toolbar-active.zeb-download-underline").click()),
        "Click on the 'Download' button to export the saved preferences and handle the file download."
    )

@pytest.mark.order(7)
def test_filter_and_status_dropdown_interactions(shared_page: Page):
    safe_action(
        shared_page.locator(".pointer.zeb-adjustments").click,
        "Click on the 'Adjustments' button again to reopen the preferences menu."
    )
    safe_action(
        shared_page.get_by_text("Reset Preference").click,
        "Click on 'Reset Preference' to revert to the default column visibility settings."
    )
    safe_action(
        shared_page.locator(".ag-icon.ag-icon-filter").first.click,
        "Click on the filter icon to open the filter menu for the first column."
    )
    safe_action(
        shared_page.get_by_role("textbox", name="Filter Value").fill("WINCO"),
        "Enter 'WINCO' into the filter text box to filter the data by this value."
    )
    safe_action(
        shared_page.get_by_role("button", name="Apply").click,
        "Click on the 'Apply' button to apply the filter and update the data view."
    )
    safe_action(
        shared_page.locator(".ag-icon.ag-icon-filter").first.click,
        "Click on the filter icon again to reopen the filter menu for the first column."
    )
    safe_action(
        shared_page.get_by_role("button", name="Reset").click,
        "Click on the 'Reset' button to clear the applied filter and restore the default data view."
    )
    safe_action(
        shared_page.locator(".w-100.p-h-16.p-v-8.dropdown-label.icon-small-dropdown > .d-flex.align-items-center > .dropdown-caret").first.click,
        "Click on the dropdown caret to open the dropdown menu for selecting a status."
    )
    safe_action(
        shared_page.get_by_text("In progress").click,
        "Select the 'In progress' option from the dropdown menu."
    )
    safe_action(
        shared_page.locator(".w-100.p-h-16.p-v-8.dropdown-label.icon-small-dropdown > .d-flex.align-items-center > .dropdown-caret").first.click,
        "Click on the dropdown caret again to reopen the dropdown menu for selecting a status."
    )
    safe_action(
        shared_page.get_by_text("Completed").click,
        "Select the 'Completed' option from the dropdown menu."
    )
    safe_action(
        shared_page.locator(".w-100.p-h-16.p-v-8.dropdown-label.icon-small-dropdown > .d-flex.align-items-center > .dropdown-caret").first.click,
        "Click on the dropdown caret again to reopen the dropdown menu for selecting a status."
    )
    safe_action(
        shared_page.get_by_text("Not started").click,
        "Select the 'Not started' option from the dropdown menu."
    )

@pytest.mark.order(8)
def test_treegrid_interactions(shared_page: Page):
    safe_action(
        shared_page.get_by_role("treegrid").get_by_text("WALMART STORES HQ").dblclick,
        "Double-click on 'WALMART STORES HQ' in the treegrid to expand its details."
    )
    safe_action(
        shared_page.locator("span").filter(has_text="WALMART").first.dblclick,
        "Double-click on the first occurrence of the text 'WALMART' to navigate further."
    )
    safe_action(
        shared_page.get_by_role("treegrid").get_by_text("WALMART 0906 SC B-0006805-01-").dblclick,
        "Double-click on 'WALMART 0906 SC B-0006805-01-' in the treegrid to expand its details."
    )
    safe_action(
        shared_page.get_by_text("WALMART 0906 SC B-0006805-01-").click(button="right"),
        "Right-click on 'WALMART 0906 SC B-0006805-01-' to open the context menu."
    )
    safe_action(
        shared_page.get_by_text("Drill up").click,
        "Click on 'Drill up' from the context menu to navigate up one level."
    )
    safe_action(
        shared_page.locator(".ag-row-even.ag-row-focus.ag-row-not-inline-editing.ag-row.ag-row-level-0.ag-row-position-absolute.ag-row-first.ag-row-hover > .ag-cell-value > .ag-cell-wrapper").click(button="right"),
        "Right-click on the highlighted row in the treegrid to open the context menu."
    )
    safe_action(
        shared_page.get_by_text("Drill up").click,
        "Click on 'Drill up' from the context menu to navigate up one level."
    )
    safe_action(
        shared_page.get_by_role("treegrid").get_by_text("WALMART STORES HQ").click(button="right"),
        "Right-click on 'WALMART STORES HQ' in the treegrid to open the context menu."
    )
    safe_action(
        shared_page.get_by_text("Drill up").click,
        "Click on 'Drill up' from the context menu to navigate up one level."
    )

@pytest.mark.order(9)
def test_pagination_and_grid_interactions(shared_page: Page):
    safe_action(
        shared_page.get_by_role("columnheader", name="6W-Actuals").click,
        "Click on the column header '6W-Actuals' to sort or interact with the column."
    )
    safe_action(
        shared_page.locator("a").filter(has_text="2").click,
        "Click on the page number '2' in the pagination control to navigate to the second page of the grid."
    )
    safe_action(
        shared_page.locator(".zeb-nav-to-first").click,
        "Click on the 'First Page' button in the pagination control to navigate to the first page of the grid."
    )
    safe_action(
        shared_page.get_by_role("gridcell", name="Press Space to toggle row selection (unchecked)   WALMART STORES HQ").get_by_label("Press Space to toggle row").check,
        "Select the row containing 'WALMART STORES HQ' by checking the checkbox in the grid cell."
    )
    safe_action(
        shared_page.locator(".checkbox-primary-color").first.uncheck,
        "Uncheck the first checkbox in the grid using the '.checkbox-primary-color' locator."
    )
    safe_action(
        shared_page.locator(".checkbox-primary-color").first.check,
        "Check the first checkbox in the grid using the '.checkbox-primary-color' locator."
    )
    safe_action(
        shared_page.locator(".d-flex.align-items-center.checkbox-primary-color").first.uncheck,
        "Uncheck the first checkbox in the grid using the '.d-flex.align-items-center.checkbox-primary-color' locator."
    )
    safe_action(
        shared_page.locator(".ag-row-odd > .ag-cell-value > .ag-cell-wrapper > .ag-group-value > aeap-group-cell-renderer > .d-flex.align-items-center.w-fit-content > .d-flex").first.uncheck,
        "Uncheck the first checkbox in the grid using a more specific locator targeting a nested structure within the grid."
    )

@pytest.mark.order(10)
def test_advanced_column_visibility_configuration(shared_page: Page):
    safe_action(
        shared_page.get_by_role("button", name="columns").nth(1).click,
        "Click on the 'Columns' button to open the column visibility configuration panel."
    )
    safe_action(
        shared_page.get_by_role("checkbox", name="Toggle All Columns Visibility").check,
        "Check the 'Toggle All Columns Visibility' checkbox to make all columns visible."
    )
    safe_action(
        shared_page.get_by_role("textbox", name="Filter Columns Input").click,
        "Click on the 'Filter Columns Input' textbox to focus on it."
    )
    safe_action(
        shared_page.get_by_role("textbox", name="Filter Columns Input").fill("User Bias"),
        "Fill the 'Filter Columns Input' textbox with the text 'User Bias' to filter columns by this keyword."
    )
    safe_action(
        shared_page.get_by_role("checkbox", name="Press SPACE to toggle visibility (visible)").uncheck,
        "Uncheck the checkbox corresponding to the 'User Bias' column to hide it."
    )
    safe_action(
        shared_page.get_by_role("textbox", name="Filter Columns Input").click,
        "Click on the 'Filter Columns Input' textbox again to focus on it."
    )
    safe_action(
        shared_page.get_by_role("textbox", name="Filter Columns Input").press("ControlOrMeta+a"),
        "Select all text in the 'Filter Columns Input' textbox using the 'ControlOrMeta+a' keyboard shortcut."
    )
    safe_action(
        shared_page.get_by_role("textbox", name="Filter Columns Input").fill(""),
        "Clear the 'Filter Columns Input' textbox by filling it with an empty string."
    )
    safe_action(
        shared_page.get_by_role("checkbox", name="Toggle All Columns Visibility").check,
        "Check the 'Toggle All Columns Visibility' checkbox again to ensure all columns are visible."
    )
    safe_action(
        shared_page.get_by_role("button", name="columns").nth(1).click,
        "Click on the 'Columns' button to close the column visibility configuration panel."
    )

@pytest.mark.order(11)
def test_preference_and_export_handling(shared_page: Page):
    safe_action(
        shared_page.locator("div:nth-child(3) > #preference-iconId > .legend-font > .multiselect-dropdown > .pointer").click,
        "Click on the 'Preference' dropdown menu to open the preference options."
    )
    safe_action(
        shared_page.get_by_text("Save Preference").click,
        "Click on the 'Save Preference' option to save the current grid settings."
    )
    safe_action(
        lambda: shared_page.expect_download(lambda: shared_page.locator("div:nth-child(2) > #export-iconId > .icon-color-toolbar-active").click()),
        "Click on the 'Export' button to export the grid data, triggering a file download."
    )

@pytest.mark.order(12)
def test_column_filtering_and_reset(shared_page: Page):
    safe_action(
        shared_page.locator("div:nth-child(3) > #preference-iconId > .legend-font > .multiselect-dropdown > .pointer").click,
        "Click on the 'Preference' dropdown menu again to reopen the preference options."
    )
    safe_action(
        shared_page.get_by_text("Reset Preference").click,
        "Click on the 'Reset Preference' option to revert the grid settings to their default state."
    )
    safe_action(
        shared_page.locator(".ag-header-cell.ag-header-parent-hidden.ag-header-background.ag-focus-managed.ag-header-active > .ag-header-cell-comp-wrapper > .ag-cell-label-container > .ag-header-icon > .ag-icon").click,
        "Click on the filter icon in the column header to open the filter options for the selected column."
    )
    safe_action(
        lambda: shared_page.get_by_role("spinbutton", name="Filter Value").fill("761"),
        "Enter the filter value '761' into the filter input field to apply a filter to the column."
    )
    safe_action(
        shared_page.get_by_label("Column Filter").get_by_role("button", name="Apply").click,
        "Click on the 'Apply' button in the column filter menu to apply the filter and update the grid data."
    )
    safe_action(
        shared_page.locator(".ag-header-icon.ag-header-cell-filter-button.ag-filter-active > .ag-icon").click,
        "Click on the filter icon again to reopen the column filter menu after applying the filter."
    )
    safe_action(
        shared_page.get_by_label("Column Filter").get_by_role("button", name="Reset").click,
        "Click on the 'Reset' button in the column filter menu to clear the applied filter and restore the grid data to its original state."
    )

@pytest.mark.order(13)
def test_row_and_drill_down_interactions(shared_page: Page):
    safe_action(
        lambda: shared_page.locator(".checkbox-primary-color").first.check(),
        "Check the first checkbox with the primary color styling to select the corresponding row."
    )
    safe_action(
        lambda: shared_page.locator("span").filter(has_text="ENTENMANNS").first.dblclick(),
        "Double-click on the row containing the text 'ENTENMANNS' to drill down into its details."
    )
    safe_action(
        lambda: shared_page.locator("span").filter(has_text="EN BITES").first.dblclick(),
        "Double-click on the row containing the text 'EN BITES' to further drill down into its details."
    )
    safe_action(
        lambda: shared_page.get_by_text("EN LITTLE BITES CP").first.dblclick(),
        "Double-click on the row containing the text 'EN LITTLE BITES CP' to navigate deeper into its details."
    )
    safe_action(
        lambda: shared_page.get_by_text("EN LB CHOCCH MFN 10P-").first.click(button="right"),
        "Right-click on the row containing the text 'EN LB CHOCCH MFN 10P-' to open the context menu for additional actions."
    )
    safe_action(
        lambda: shared_page.get_by_text("Drill up").click(),
        "Click on the 'Drill up' option in the context menu to navigate back to the previous level."
    )
    safe_action(
        lambda: shared_page.get_by_role("gridcell").filter(has_text=re.compile(r"^$")).first.click(button="right"),
        "Right-click on the first grid cell with an empty text value to open the context menu."
    )
    safe_action(
        lambda: shared_page.get_by_role("gridcell").filter(has_text=re.compile(r"^$")).first.click(),
        "Click on the first grid cell with an empty text value to select it."
    )

@pytest.mark.order(14)
def test_product_navigation_and_time_filter(shared_page: Page):
    safe_action(
        lambda: shared_page.locator("esp-card-component").filter(has_text="Products10 rows out of 11").locator("a").click(),
        "Click on the link within the 'Products' card to navigate to the detailed view of the products."
    )
    safe_action(
        lambda: shared_page.locator("div:nth-child(3) > esp-pagination-v2 > .d-flex.w-100 > .pagination-pager > .pagination-first > .zeb-nav-to-first").click(),
        "Click on the 'First Page' button in the pagination controls to navigate to the first page of the product list."
    )
    safe_action(
        lambda: shared_page.get_by_role("button", name="Apply").click(),
        "Click on the 'Apply' button to apply the selected filters or changes."
    )
    safe_action(
        lambda: shared_page.locator("div").filter(has_text=re.compile(r"^Filter$")).nth(1).click(),
        "Click on the 'Filter' section to expand or interact with the filter options."
    )
    safe_action(
        lambda: shared_page.locator("#time-filterId > .wr-20 > esp-multiselect-dropdown > .multiselect-dropdown > div > .w-100 > .d-flex.align-items-center > .dropdown-caret").click(),
        "Click on the dropdown caret in the 'Time' filter to open the dropdown menu."
    )
    safe_action(
        lambda: shared_page.locator("div").filter(has_text=re.compile(r"^Latest 5 Next 4$")).nth(1).click(),
        "Select the 'Latest 5 Next 4' option from the 'Time' filter dropdown."
    )
    safe_action(
        lambda: shared_page.locator("#time-filterId > .wr-20 > esp-multiselect-dropdown > .multiselect-dropdown > div > .w-100 > .d-flex.align-items-center > .dropdown-caret").click(),
        "Click on the dropdown caret in the 'Time' filter again to open the dropdown menu for a new selection."
    )
    safe_action(
        lambda: shared_page.locator("div").filter(has_text=re.compile(r"^Latest 5 Next 12$")).nth(1).click(),
        "Select the 'Latest 5 Next 12' option from the 'Time' filter dropdown."
    )
    safe_action(
        lambda: shared_page.locator("#time-filterId > .wr-20 > esp-multiselect-dropdown > .multiselect-dropdown > div > .w-100 > .d-flex.align-items-center > .dropdown-caret").click(),
        "Click on the dropdown caret in the 'Time' filter again to open the dropdown menu for another selection."
    )
    safe_action(
        lambda: shared_page.locator("div").filter(has_text=re.compile(r"^Latest 13 Next 4$")).nth(1).click(),
        "Select the 'Latest 13 Next 4' option from the 'Time' filter dropdown."
    )

@pytest.mark.order(15)
def test_weekly_summary_and_column_visibility(shared_page: Page):
    safe_action(
        lambda: shared_page.locator("esp-card-component").filter(has_text="Weekly Summary Customer:").get_by_role("button").click(),
        "Click on the 'Weekly Summary Customer:' card button to expand or interact with the card."
    )
    safe_action(
        lambda: shared_page.get_by_role("treeitem", name="-11-02 (45) Column").get_by_label("Press SPACE to toggle visibility (visible)").uncheck(),
        "Uncheck the visibility toggle for the column labeled '-11-02 (45) Column'."
    )
    safe_action(
        lambda: shared_page.get_by_role("treeitem", name="-11-09 (46) Column").get_by_label("Press SPACE to toggle visibility (visible)").uncheck(),
        "Uncheck the visibility toggle for the column labeled '-11-09 (46) Column'."
    )
    safe_action(
        lambda: shared_page.get_by_role("treeitem", name="-11-16 (47) Column").get_by_label("Press SPACE to toggle visibility (visible)").uncheck(),
        "Uncheck the visibility toggle for the column labeled '-11-16 (47) Column'."
    )
    safe_action(
        lambda: shared_page.get_by_role("checkbox", name="Toggle All Columns Visibility").check(),
        "Check the 'Toggle All Columns Visibility' checkbox to make all columns visible."
    )
    safe_action(
        lambda: shared_page.locator("div:nth-child(4) > #preference-iconId > .legend-font > .multiselect-dropdown > .pointer").click(),
        "Click on the preference dropdown icon to open the preference options."
    )
    safe_action(
        lambda: shared_page.get_by_text("Save Preference").click(),
        "Click on 'Save Preference' to save the current column visibility settings."
    )
    safe_action(
        lambda: shared_page.locator("div:nth-child(4) > #preference-iconId > .legend-font > .multiselect-dropdown > .pointer").click(),
        "Click on the preference dropdown icon again to reopen the preference options."
    )
    safe_action(
        lambda: shared_page.get_by_text("Reset Preference").click(),
        "Click on 'Reset Preference' to reset the column visibility settings to their default state."
    )

@pytest.mark.order(16)
def test_export_and_pagination_interactions(shared_page: Page):
    safe_action(
        lambda: shared_page.expect_download(lambda: shared_page.locator("div:nth-child(3) > #export-iconId > .icon-color-toolbar-active").click()),
        "Set up an expectation for a file download and click on the export icon to initiate the download process."
    )
    safe_action(
        lambda: shared_page.locator(".align-middle").first.click(),
        "Click on the first element with the class 'align-middle' to interact with it."
    )
    safe_action(
        lambda: shared_page.get_by_text("Event").nth(1).click(),
        "Click on the second occurrence of the text 'Event' to navigate or interact with the Event section."
    )
    safe_action(
        lambda: shared_page.locator("esp-card-component").filter(has_text="Event Details columns (0)").get_by_role("button").click(),
        "Click on the button within the 'Event Details columns (0)' card to open column visibility options."
    )
    safe_action(
        lambda: shared_page.get_by_role("treeitem", name="Event Column").get_by_label("Press SPACE to toggle visibility (visible)").uncheck(),
        "Uncheck the visibility toggle for the 'Event Column' to hide it."
    )
    safe_action(
        lambda: shared_page.get_by_role("treeitem", name="UPC 12 Column").get_by_label("Press SPACE to toggle visibility (visible)").uncheck(),
        "Uncheck the visibility toggle for the 'UPC 12 Column' to hide it."
    )
    safe_action(
        lambda: shared_page.get_by_role("treeitem", name="Customer Level 2 Column").get_by_label("Press SPACE to toggle visibility (visible)").uncheck(),
        "Uncheck the visibility toggle for the 'Customer Level 2 Column' to hide it."
    )
    safe_action(
        lambda: shared_page.get_by_role("treeitem", name="Start Date Column").get_by_label("Press SPACE to toggle visibility (visible)").uncheck(),
        "Uncheck the visibility toggle for the 'Start Date Column' to hide it."
    )
    safe_action(
        lambda: shared_page.get_by_role("treeitem", name="End Date Column").get_by_label("Press SPACE to toggle visibility (visible)").uncheck(),
        "Uncheck the visibility toggle for the 'End Date Column' to hide it."
    )
    safe_action(
        lambda: shared_page.get_by_role("treeitem", name="Max Promo Price Column").get_by_label("Press SPACE to toggle visibility (visible)").uncheck(),
        "Uncheck the visibility toggle for the 'Max Promo Price Column' to hide it."
    )
    safe_action(
        lambda: shared_page.get_by_role("treeitem", name="Min Promo Price Column").get_by_label("Press SPACE to toggle visibility (visible)").uncheck(),
        "Uncheck the visibility toggle for the 'Min Promo Price Column' to hide it."
    )
    safe_action(
        lambda: shared_page.get_by_role("checkbox", name="Toggle All Columns Visibility").check(),
        "Check the 'Toggle All Columns Visibility' checkbox to make all columns visible again."
    )
    safe_action(
        lambda: shared_page.get_by_role("textbox", name="Filter Columns Input").click(),
        "Click on the 'Filter Columns Input' textbox to focus on it."
    )
    safe_action(
        lambda: shared_page.get_by_role("textbox", name="Filter Columns Input").fill("UPC"),
        "Fill the 'Filter Columns Input' textbox with the text 'UPC' to filter columns by this keyword."
    )
    safe_action(
        lambda: shared_page.get_by_role("checkbox", name="Press SPACE to toggle visibility (visible)").uncheck(),
        "Uncheck the visibility toggle for the filtered column matching 'UPC' to hide it."
    )
    safe_action(
        lambda: shared_page.locator("div:nth-child(7) > div > esp-grid-container > esp-card-component > .card-container > .title > .grid-icons-container > esp-grid-icons-component > .display-grid-icons > div:nth-child(2) > #preference-iconId > .legend-font > .multiselect-dropdown > .pointer").click(),
        "Click on the 'Preference' icon to open the dropdown menu for saving preferences."
    )
    safe_action(
        lambda: shared_page.get_by_text("Save Preference").click(),
        "Click on 'Save Preference' to save the current grid settings or preferences."
    )
    safe_action(
        lambda: shared_page.expect_download(lambda: shared_page.locator("div:nth-child(7) > div > esp-grid-container > esp-card-component > .card-container > .title > .grid-icons-container > esp-grid-icons-component > .display-grid-icons > div > #export-iconId > .icon-color-toolbar-active").click()),
        "Set up an expectation for a file download and click on the 'Export' icon to initiate the export process."
    )
    safe_action(
        lambda: shared_page.locator("a").nth(2).click(),
        "Click on the second page link in the pagination to navigate to the second page of the grid."
    )
    safe_action(
        lambda: shared_page.locator("a").filter(has_text="3").click(),
        "Click on the page link labeled '3' to navigate to the third page of the grid."
    )
    safe_action(
        lambda: shared_page.locator("div:nth-child(7) > div > esp-grid-container > esp-card-component > .card-container > .card-content > esp-row-dimentional-grid > div > #paginationId > esp-pagination-v2 > .d-flex.w-100 > .pagination-pager > .pagination-first").click(),
        "Click on the 'First Page' button in the pagination controls to navigate back to the first page of the grid."
    )

@pytest.mark.order(17)
def test_row_display_and_column_filtering(shared_page: Page):
    safe_action(
        lambda: shared_page.get_by_text("View 10 row(s)").nth(2).click(),
        "Click on the dropdown labeled 'View 10 row(s)' to open the row display options."
    )
    safe_action(
        lambda: shared_page.locator("div").filter(has_text=re.compile(r"^View 20 row\(s\)$")).nth(1).click(),
        "Select the option 'View 20 row(s)' from the dropdown to change the number of rows displayed."
    )
    safe_action(
        lambda: shared_page.locator(".ag-header-cell.ag-header-parent-hidden.ag-header-cell-sortable.ag-header-background.ag-focus-managed.ag-header-active > .ag-header-cell-comp-wrapper > .ag-cell-label-container > .ag-header-icon > .ag-icon").click(),
        "Click on the column header icon to open the filter options for the column."
    )
    safe_action(
        lambda: shared_page.get_by_role("textbox", name="Filter Value").fill("Promotion"),
        "Fill the filter textbox with the value 'Promotion' to filter the column based on this value."
    )
    safe_action(
        lambda: shared_page.get_by_label("Column Filter").get_by_role("button", name="Apply").click(),
        "Click the 'Apply' button to apply the column filter."
    )
    safe_action(
        lambda: shared_page.locator(".ag-header-cell.ag-header-parent-hidden.ag-header-cell-sortable.ag-header-background.ag-focus-managed.ag-header-cell-filtered > .ag-header-cell-comp-wrapper > .ag-cell-label-container").click(),
        "Click on the filtered column header to interact with the column filter settings."
    )
    safe_action(
        lambda: shared_page.locator(".ag-header-icon.ag-header-cell-filter-button.ag-filter-active > .ag-icon").click(),
        "Click on the filter icon to open the active filter options for the column."
    )
    safe_action(
        lambda: shared_page.get_by_label("Column Filter").get_by_role("button", name="Reset").click(),
        "Click the 'Reset' button to clear the applied column filter."
    )

@pytest.mark.order(18)
def test_final_grid_interactions_and_cleanup(shared_page: Page):
    safe_action(
        lambda: shared_page.get_by_role("gridcell", name="Promotion-TH PRO BAGEL ROLLBACK 12/29/25 thru 03/29/").dblclick(),
        "Double-click on the grid cell with the name 'Promotion-TH PRO BAGEL ROLLBACK 12/29/25 thru 03/29/' to interact with or edit the cell."
    )
    safe_action(
        lambda: shared_page.close(),
        "Close the current page after completing the interaction."
    )
    safe_action(
        lambda: shared_page.context.close(),
        "Close the browser context to clean up resources and end the session."
    )
    safe_action(
        lambda: shared_page.context.browser.close(),
        "Close the browser instance to terminate all associated contexts and sessions."
    )

