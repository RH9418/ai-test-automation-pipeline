
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
    # Navigate to the specified URL for the 'Executive Dashboard' in the demand planning module.
    safe_action(shared_page, shared_page, 'goto', "Navigate to the specified URL for the 'Executive Dashboard' in the demand planning module.", "https://stage.bbu.esp.antuit.ai/dp/demand-planning/executive-dashboard?workbookId=4&tabIndex=5")
    print('''
    ================================================================================
      ACTION REQUIRED: MANUAL LOGIN & MFA
    --------------------------------------------------------------------------------
      1. Log in manually. 2. Complete MFA. 3. Wait for dashboard to load.
      ---> PRESS [ENTER] IN THIS TERMINAL WHEN READY <---
    ================================================================================
    ''')
    input()
    print('\n🚀 Starting automated actions...')

@pytest.mark.order(4)
def test_customer_total_column_selection(shared_page: Page):
    # Click on the 'Customer Total columns (0)' text to open the column selection menu.
    safe_action(shared_page, shared_page.get_by_text("Customer Total columns (0)"), 'click', "Click on the 'Customer Total columns (0)' text to open the column selection menu.")
    # Click on the 'Customer Total' text to select the corresponding column.
    safe_action(shared_page, shared_page.get_by_text("Customer Total"), 'click', "Click on the 'Customer Total' text to select the corresponding column.")
    # Click on the button within the 'Customer Total columns (0)' card to confirm the selection or perform an action.
    safe_action(shared_page, shared_page.locator("esp-card-component").filter(has_text="Customer Total columns (0)").get_by_role("button"), 'click', "Click on the button within the 'Customer Total columns (0)' card to confirm the selection or perform an action.")

@pytest.mark.order(5)
def test_filter_columns_input_interaction(shared_page: Page):
    # Click on the 'Filter Columns Input' textbox to focus on it for entering a filter value.
    safe_action(shared_page, shared_page.get_by_role("textbox", name="Filter Columns Input"), 'click', "Click on the 'Filter Columns Input' textbox to focus on it for entering a filter value.")
    # Fill the 'Filter Columns Input' textbox with the text 'System' to filter columns containing this keyword.
    safe_action(shared_page, shared_page.get_by_role("textbox", name="Filter Columns Input"), 'fill', "Fill the 'Filter Columns Input' textbox with the text 'System' to filter columns containing this keyword.", "System")
    # Press 'Enter' to apply the filter and display matching columns.
    safe_action(shared_page, shared_page.get_by_role("textbox", name="Filter Columns Input"), 'press', "Press 'Enter' to apply the filter and display matching columns.", "Enter")

@pytest.mark.order(6)
def test_column_selection_and_checkbox_toggle(shared_page: Page):
    # Click on the first column in the filtered list to select it.
    safe_action(shared_page, shared_page.locator(".ag-column-select-column").first, 'click', "Click on the first column in the filtered list to select it.")
    # Check the checkbox for 'System Forecast Base (Plan)' by toggling it using the SPACE key.
    safe_action(shared_page, shared_page.get_by_role("treeitem", name="System Forecast Base (Plan").get_by_label("Press SPACE to toggle"), 'check', "Check the checkbox for 'System Forecast Base (Plan)' by toggling it using the SPACE key.")

@pytest.mark.order(7)
def test_filter_reset_and_additional_column_selection(shared_page: Page):
    # Click on the third column in the list to select it.
    safe_action(shared_page, shared_page.locator("div:nth-child(3) > .ag-column-select-column"), 'click', "Click on the third column in the list to select it.")
    # Click on the 'Filter Columns Input' textbox again to clear or modify the filter.
    safe_action(shared_page, shared_page.get_by_role("textbox", name="Filter Columns Input"), 'click', "Click on the 'Filter Columns Input' textbox again to clear or modify the filter.")
    # Clear the 'Filter Columns Input' textbox by filling it with an empty string.
    safe_action(shared_page, shared_page.get_by_role("textbox", name="Filter Columns Input"), 'fill', "Clear the 'Filter Columns Input' textbox by filling it with an empty string.", "")
    # Press 'Enter' to reset the filter and display all columns.
    safe_action(shared_page, shared_page.get_by_role("textbox", name="Filter Columns Input"), 'press', "Press 'Enter' to reset the filter and display all columns.", "Enter")

@pytest.mark.order(8)
def test_system_forecast_column_selection(shared_page: Page):
    # Click on the 'System Forecast Promotion (' label to select the corresponding column.
    safe_action(shared_page, shared_page.get_by_label("System Forecast Promotion (").get_by_text("System Forecast Promotion ("), 'click', "Click on the 'System Forecast Promotion (' label to select the corresponding column.")
    # Click on the 'System Forecast Total (Plan+1)' label to select the corresponding column.
    safe_action(shared_page, shared_page.get_by_label("System Forecast Total (Plan+1").get_by_text("System Forecast Total (Plan+1"), 'click', "Click on the 'System Forecast Total (Plan+1)' label to select the corresponding column.")
    # Click on the 'System Forecast Base (Plan+1)' label to select the corresponding column.
    safe_action(shared_page, shared_page.get_by_label("System Forecast Base (Plan+1").get_by_text("System Forecast Base (Plan+1"), 'click', "Click on the 'System Forecast Base (Plan+1)' label to select the corresponding column.")
    # Click on the 'System Forecast Promotion (' label again to toggle its selection.
    safe_action(shared_page, shared_page.get_by_label("System Forecast Promotion (").get_by_text("System Forecast Promotion ("), 'click', "Click on the 'System Forecast Promotion (' label again to toggle its selection.")

@pytest.mark.order(9)
def test_6_week_metrics_column_selection(shared_page: Page):
    # Click on the '6 Week Gross Units Average' column to select it.
    safe_action(shared_page, shared_page.get_by_label("6 Week Gross Units Average").get_by_text("Week Gross Units Average"), 'click', "Click on the '6 Week Gross Units Average' column to select it.")
    # Click on the '6 Week Aged Net Units Average Column' to select it, ensuring the exact match is used.
    safe_action(shared_page, shared_page.get_by_label("6 Week Aged Net Units Average Column", exact=True).get_by_text("Week Aged Net Units Average"), 'click', "Click on the '6 Week Aged Net Units Average Column' to select it, ensuring the exact match is used.")
    # Click on the 'LY 6 Week Aged Net Units' column to select it.
    safe_action(shared_page, shared_page.get_by_label("LY 6 Week Aged Net Units").get_by_text("LY 6 Week Aged Net Units"), 'click', "Click on the 'LY 6 Week Aged Net Units' column to select it.")
    # Click on the '% Change 6 Week Aged Net' column to select it.
    safe_action(shared_page, shared_page.get_by_label("% Change 6 Week Aged Net").get_by_text("% Change 6 Week Aged Net"), 'click', "Click on the '% Change 6 Week Aged Net' column to select it.")
    # Click on the '6 Week Scan Units Average Column' to select it, ensuring the exact match is used.
    safe_action(shared_page, shared_page.get_by_label("6 Week Scan Units Average Column", exact=True).get_by_text("Week Scan Units Average"), 'click', "Click on the '6 Week Scan Units Average Column' to select it, ensuring the exact match is used.")
    # Click on the 'LY 6 Week Scan Units Average' column to select it.
    safe_action(shared_page, shared_page.get_by_label("LY 6 Week Scan Units Average").get_by_text("LY 6 Week Scan Units Average"), 'click', "Click on the 'LY 6 Week Scan Units Average' column to select it.")
    # Click on the '% Change 6 Week Scan Units' column to select it.
    safe_action(shared_page, shared_page.get_by_label("% Change 6 Week Scan Units").get_by_text("% Change 6 Week Scan Units"), 'click', "Click on the '% Change 6 Week Scan Units' column to select it.")

@pytest.mark.order(10)
def test_column_selection_actions(shared_page: Page):
    # Click on the 'Freshness (6 Week Average)' column to select it.
    safe_action(shared_page, shared_page.get_by_label("Freshness (6 Week Average)").get_by_text("Freshness (6 Week Average)"), 'click', "Click on the 'Freshness (6 Week Average)' column to select it.")
    # Click on the '6 Week Aged Returns Units' column to select it.
    safe_action(shared_page, shared_page.get_by_label("6 Week Aged Returns Units").get_by_text("6 Week Aged Returns Units"), 'click', "Click on the '6 Week Aged Returns Units' column to select it.")
    # Click on the 'System Forecast Total (Plan Week)' column to select it using its locator.
    safe_action(shared_page, shared_page.locator("#ag-169").get_by_text("System Forecast Total (Plan Week)"), 'click', "Click on the 'System Forecast Total (Plan Week)' column to select it using its locator.")
    safe_action(shared_page, shared_page.get_by_label("System Forecast Base (Plan").get_by_text("System Forecast Base (Plan"), 'click', "Perform click on page.get_by_label(\"System Forecast Base (Plan\").get_by_text(\"System Forecast Base (Plan\")")
    safe_action(shared_page, shared_page.locator("esp-card-component").filter(has_text="Customer Total columns (0)").get_by_role("button"), 'click', "Perform click on page.locator(\"esp-card-component\").filter(has_text=\"Customer Total columns (0)\").get_by_role(\"button\")")

@pytest.mark.order(11)
def test_file_export_handling(shared_page: Page):
    # Set up an expectation to handle a file download triggered by the subsequent action.
    with shared_page.expect_download() as download_info:
    # Click on the 'Export' icon within the 'esp-grid-icons-component' to initiate the export process.
        safe_action(shared_page, shared_page.locator("esp-grid-icons-component").filter(has_text="Export").locator("#export-iconId"), 'click', "Click on the 'Export' icon within the 'esp-grid-icons-component' to initiate the export process.")
    # Retrieve the downloaded file information after the export action is triggered.
    download = download_info.value

@pytest.mark.order(12)
def test_preference_management(shared_page: Page):
    # Click on the first 'Adjustments' icon (identified by the '.pointer.zeb-adjustments' locator) to open the adjustments menu.
    safe_action(shared_page, shared_page.locator(".pointer.zeb-adjustments").first, 'click', "Click on the first 'Adjustments' icon (identified by the '.pointer.zeb-adjustments' locator) to open the adjustments menu.")
    # Click on the 'Save Preference' option to save the current preferences.
    safe_action(shared_page, shared_page.get_by_text("Save Preference"), 'click', "Click on the 'Save Preference' option to save the current preferences.")
    # Click on the first 'Adjustments' icon again to reopen the adjustments menu.
    safe_action(shared_page, shared_page.locator(".pointer.zeb-adjustments").first, 'click', "Click on the first 'Adjustments' icon again to reopen the adjustments menu.")
    # Click on the 'Reset Preference' option to reset the preferences to their default state.
    safe_action(shared_page, shared_page.get_by_text("Reset Preference"), 'click', "Click on the 'Reset Preference' option to reset the preferences to their default state.")

@pytest.mark.order(13)
def test_grid_interaction_and_column_configuration(shared_page: Page):
    # Click on the first horizontal scroll container to interact with the grid.
    safe_action(shared_page, shared_page.locator(".ag-body-horizontal-scroll-container").first, 'click', "Click on the first horizontal scroll container to interact with the grid.")
    # Click on the 'Customers columns (0)' text to open the column configuration panel.
    safe_action(shared_page, shared_page.get_by_text("Customers columns (0)"), 'click', "Click on the 'Customers columns (0)' text to open the column configuration panel.")
    # Click on the 'Customers' text to select the Customers section.
    safe_action(shared_page, shared_page.get_by_text("Customers"), 'click', "Click on the 'Customers' text to select the Customers section.")
    # Click on 'Customers columns (0)' again to toggle the column configuration panel.
    safe_action(shared_page, shared_page.get_by_text("Customers columns (0)"), 'click', "Click on 'Customers columns (0)' again to toggle the column configuration panel.")
    # Click on the button within the 'Customers columns (0)' card to expand its options.
    safe_action(shared_page, shared_page.locator("esp-card-component").filter(has_text="Customers columns (0)").get_by_role("button"), 'click', "Click on the button within the 'Customers columns (0)' card to expand its options.")
    # Click on the column panel header to access column selection options.
    safe_action(shared_page, shared_page.locator("#ag-87 > .ag-column-panel > .ag-column-select > .ag-column-select-header"), 'click', "Click on the column panel header to access column selection options.")

@pytest.mark.order(14)
def test_column_filtering_and_visibility_management(shared_page: Page):
    # Fill the 'Filter Columns Input' textbox with the text 'Fresh' to filter columns.
    safe_action(shared_page, shared_page.get_by_role("textbox", name="Filter Columns Input"), 'fill', "Fill the 'Filter Columns Input' textbox with the text 'Fresh' to filter columns.", "Fresh")
    # Press 'Enter' in the 'Filter Columns Input' textbox to apply the filter.
    safe_action(shared_page, shared_page.get_by_role("textbox", name="Filter Columns Input"), 'press', "Press 'Enter' in the 'Filter Columns Input' textbox to apply the filter.", "Enter")
    # Check the checkbox to make the column with the label 'Press SPACE to toggle visibility (hidden)' visible.
    safe_action(shared_page, shared_page.get_by_role("checkbox", name="Press SPACE to toggle visibility (hidden)"), 'check', "Check the checkbox to make the column with the label 'Press SPACE to toggle visibility (hidden)' visible.")
    # Uncheck the 'Toggle All Columns Visibility' checkbox to hide all columns.
    safe_action(shared_page, shared_page.get_by_role("checkbox", name="Toggle All Columns Visibility"), 'uncheck', "Uncheck the 'Toggle All Columns Visibility' checkbox to hide all columns.")
    # Click on the 'Filter Columns Input' textbox to focus on it.
    safe_action(shared_page, shared_page.get_by_role("textbox", name="Filter Columns Input"), 'click', "Click on the 'Filter Columns Input' textbox to focus on it.")
    # Clear the 'Filter Columns Input' textbox by filling it with an empty string.
    safe_action(shared_page, shared_page.get_by_role("textbox", name="Filter Columns Input"), 'fill', "Clear the 'Filter Columns Input' textbox by filling it with an empty string.", "")
    # Press 'Enter' in the 'Filter Columns Input' textbox to apply the filter.
    safe_action(shared_page, shared_page.get_by_role("textbox", name="Filter Columns Input"), 'press', "Press 'Enter' in the 'Filter Columns Input' textbox to apply the filter.", "Enter")

@pytest.mark.order(15)
def test_system_forecast_column_selection(shared_page: Page):
    # Click on the column labeled 'System Forecast Total (Plan Week)' to select it.
    safe_action(shared_page, shared_page.locator("#ag-87").get_by_text("System Forecast Total (Plan Week)"), 'click', "Click on the column labeled 'System Forecast Total (Plan Week)' to select it.")
    # Click on the column labeled 'System Forecast Base (Plan Week)' to select it.
    safe_action(shared_page, shared_page.get_by_label("System Forecast Base (Plan Week) Column").get_by_text("System Forecast Base (Plan"), 'click', "Click on the column labeled 'System Forecast Base (Plan Week)' to select it.")
    # Click on the column labeled 'System Forecast Promotion (Plan Week)' to select it.
    safe_action(shared_page, shared_page.get_by_label("System Forecast Promotion (Plan Week) Column").get_by_text("System Forecast Promotion ("), 'click', "Click on the column labeled 'System Forecast Promotion (Plan Week)' to select it.")
    # Click on the column labeled 'System Forecast Total (Plan+1)' to select it.
    safe_action(shared_page, shared_page.get_by_label("System Forecast Total (Plan+1").get_by_text("System Forecast Total (Plan+1"), 'click', "Click on the column labeled 'System Forecast Total (Plan+1)' to select it.")
    # Click on the column labeled 'System Forecast Base (Plan+1)' to select it.
    safe_action(shared_page, shared_page.get_by_label("System Forecast Base (Plan+1").get_by_text("System Forecast Base (Plan+1"), 'click', "Click on the column labeled 'System Forecast Base (Plan+1)' to select it.")
    # Click on the column labeled 'System Forecast Promotion (Plan+1 Week)' to select it.
    safe_action(shared_page, shared_page.get_by_label("System Forecast Promotion (Plan+1 Week) Column").get_by_text("System Forecast Promotion ("), 'click', "Click on the column labeled 'System Forecast Promotion (Plan+1 Week)' to select it.")

@pytest.mark.order(16)
def test_column_selection_actions(shared_page: Page):
    # Click on the column labeled '6 Week Gross Units Average' to select it.
    safe_action(shared_page, shared_page.get_by_label("6 Week Gross Units Average").get_by_text("Week Gross Units Average"), 'click', "Click on the column labeled '6 Week Gross Units Average' to select it.")
    # Click on the column labeled '6 Week Aged Net Units Average' to select it.
    safe_action(shared_page, shared_page.get_by_label("6 Week Aged Net Units Average Column", exact=True).get_by_text("6 Week Aged Net Units Average", exact=True), 'click', "Click on the column labeled '6 Week Aged Net Units Average' to select it.")
    # Click on the column labeled 'LY 6 Week Aged Net Units' to select it.
    safe_action(shared_page, shared_page.get_by_label("LY 6 Week Aged Net Units").get_by_text("LY 6 Week Aged Net Units"), 'click', "Click on the column labeled 'LY 6 Week Aged Net Units' to select it.")
    # Click on the column labeled '% Change 6 Week Aged Net' to select it.
    safe_action(shared_page, shared_page.get_by_label("% Change 6 Week Aged Net").get_by_text("% Change 6 Week Aged Net"), 'click', "Click on the column labeled '% Change 6 Week Aged Net' to select it.")
    # Click on the column labeled 'LY 6 Week Scan Units Average' to select it.
    safe_action(shared_page, shared_page.get_by_label("LY 6 Week Scan Units Average").get_by_text("LY 6 Week Scan Units Average"), 'click', "Click on the column labeled 'LY 6 Week Scan Units Average' to select it.")
    # Click on the column labeled '6 Week Scan Units Average' to select it.
    safe_action(shared_page, shared_page.get_by_label("6 Week Scan Units Average Column", exact=True).get_by_text("Week Scan Units Average"), 'click', "Click on the column labeled '6 Week Scan Units Average' to select it.")
    # Click on the column labeled '% Change 6 Week Scan Units' to select it.
    safe_action(shared_page, shared_page.get_by_label("% Change 6 Week Scan Units").get_by_text("% Change 6 Week Scan Units"), 'click', "Click on the column labeled '% Change 6 Week Scan Units' to select it.")
    # Click on the column labeled 'Freshness (6 Week Average)' to select it.
    safe_action(shared_page, shared_page.get_by_label("Freshness (6 Week Average)").get_by_text("Freshness (6 Week Average)"), 'click', "Click on the column labeled 'Freshness (6 Week Average)' to select it.")
    # Click on the column labeled '6 Week Aged Returns Units' to select it.
    safe_action(shared_page, shared_page.get_by_label("6 Week Aged Returns Units").get_by_text("6 Week Aged Returns Units"), 'click', "Click on the column labeled '6 Week Aged Returns Units' to select it.")

@pytest.mark.order(17)
def test_customer_columns_expansion_and_export(shared_page: Page):
    # Click on the button within the 'Customers columns (0)' card to expand its options.
    safe_action(shared_page, shared_page.locator("esp-card-component").filter(has_text="Customers columns (0)").get_by_role("button"), 'click', "Click on the button within the 'Customers columns (0)' card to expand its options.")
    # Set up an expectation to handle a file download triggered by the next action.
    with shared_page.expect_download() as download1_info:
    # Click on the 'Export' icon to initiate the export process.
        safe_action(shared_page, shared_page.locator("div:nth-child(2) > #export-iconId > .icon-color-toolbar-active"), 'click', "Click on the 'Export' icon to initiate the export process.")
    # Capture the downloaded file information after the export action is triggered.
    download1 = download1_info.value

@pytest.mark.order(18)
def test_preferences_management(shared_page: Page):
    # Click on the 'Preferences' dropdown menu to view available options.
    safe_action(shared_page, shared_page.locator("div:nth-child(3) > #preference-iconId > .legend-font > .multiselect-dropdown > .pointer"), 'click', "Click on the 'Preferences' dropdown menu to view available options.")
    # Select the 'Save Preference' option from the dropdown to save the current preferences.
    safe_action(shared_page, shared_page.get_by_text("Save Preference"), 'click', "Select the 'Save Preference' option from the dropdown to save the current preferences.")
    # Reopen the 'Preferences' dropdown menu to access additional options.
    safe_action(shared_page, shared_page.locator("div:nth-child(3) > #preference-iconId > .legend-font > .multiselect-dropdown > .pointer"), 'click', "Reopen the 'Preferences' dropdown menu to access additional options.")
    # Select the 'Reset Preference' option from the dropdown to reset preferences to default.
    safe_action(shared_page, shared_page.get_by_text("Reset Preference"), 'click', "Select the 'Reset Preference' option from the dropdown to reset preferences to default.")

@pytest.mark.order(19)
def test_customer_column_sorting_and_filtering(shared_page: Page):
    # Click on the 'Customer' column header to sort or filter the column.
    safe_action(shared_page, shared_page.locator("esp-row-dimentional-grid").get_by_text("Customer"), 'click', "Click on the 'Customer' column header to sort or filter the column.")
    # Click on the descending sort icon to sort the 'Customer' column in descending order.
    safe_action(shared_page, shared_page.locator(".ag-icon.ag-icon-desc").first, 'click', "Click on the descending sort icon to sort the 'Customer' column in descending order.")
    # Click on the descending sort icon again to toggle the sorting order.
    safe_action(shared_page, shared_page.locator(".ag-icon.ag-icon-desc").first, 'click', "Click on the descending sort icon again to toggle the sorting order.")
    # Open the filter menu for the 'Customer' column.
    safe_action(shared_page, shared_page.locator(".ag-filter-body-wrapper"), 'click', "Open the filter menu for the 'Customer' column.")
    # Select the 'Contains' filter option from the filter menu.
    safe_action(shared_page, shared_page.get_by_text("Contains"), 'click', "Select the 'Contains' filter option from the filter menu.")
    # Click on the 'Select Field' dropdown and choose the 'Contains' option.
    safe_action(shared_page, shared_page.get_by_label("Select Field").get_by_text("Contains"), 'click', "Click on the 'Select Field' dropdown and choose the 'Contains' option.")
    # Re-select the 'Contains' filter option to confirm the selection.
    safe_action(shared_page, shared_page.get_by_text("Contains"), 'click', "Re-select the 'Contains' filter option to confirm the selection.")
    # Select the 'Does not contain' filter option from the filter menu.
    safe_action(shared_page, shared_page.get_by_text("Does not contain"), 'click', "Select the 'Does not contain' filter option from the filter menu.")
    # Re-select the 'Does not contain' filter option to confirm the selection.
    safe_action(shared_page, shared_page.get_by_text("Does not contain"), 'click', "Re-select the 'Does not contain' filter option to confirm the selection.")
    # Select the 'Equals' filter option from the filter menu.
    safe_action(shared_page, shared_page.get_by_role("option", name="Equals"), 'click', "Select the 'Equals' filter option from the filter menu.")
    # Re-select the 'Equals' filter option to confirm the selection.
    safe_action(shared_page, shared_page.get_by_text("Equals"), 'click', "Re-select the 'Equals' filter option to confirm the selection.")
    # Select the 'Does not equal' filter option from the filter menu.
    safe_action(shared_page, shared_page.get_by_role("option", name="Does not equal"), 'click', "Select the 'Does not equal' filter option from the filter menu.")
    # Re-select the 'Does not equal' filter option to confirm the selection.
    safe_action(shared_page, shared_page.get_by_text("Does not equal"), 'click', "Re-select the 'Does not equal' filter option to confirm the selection.")

@pytest.mark.order(20)
def test_filter_option_selection_and_confirmation(shared_page: Page):
    # Select the 'Begins with' filter option from the filter menu.
    safe_action(shared_page, shared_page.get_by_role("option", name="Begins with"), 'click', "Select the 'Begins with' filter option from the filter menu.")
    # Open the filtering operator dropdown to choose a different operator.
    safe_action(shared_page, shared_page.get_by_role("combobox", name="Filtering operator"), 'click', "Open the filtering operator dropdown to choose a different operator.")
    # Select the 'Ends with' filter option from the filter menu.
    safe_action(shared_page, shared_page.get_by_role("option", name="Ends with"), 'click', "Select the 'Ends with' filter option from the filter menu.")
    # Re-select the 'Ends with' filter option to confirm the selection.
    safe_action(shared_page, shared_page.get_by_text("Ends with"), 'click', "Re-select the 'Ends with' filter option to confirm the selection.")
    # Select the 'Blank' filter option from the filter menu.
    safe_action(shared_page, shared_page.get_by_role("option", name="Blank", exact=True), 'click', "Select the 'Blank' filter option from the filter menu.")
    # Re-select the 'Blank' filter option to confirm the selection.
    safe_action(shared_page, shared_page.get_by_text("Blank"), 'click', "Re-select the 'Blank' filter option to confirm the selection.")
    # Select the 'Not blank' filter option from the filter menu.
    safe_action(shared_page, shared_page.get_by_role("option", name="Not blank"), 'click', "Select the 'Not blank' filter option from the filter menu.")

@pytest.mark.order(21)
def test_logical_operator_selection(shared_page: Page):
    # Select the 'AND' logical operator for combining filter conditions.
    safe_action(shared_page, shared_page.get_by_text("AND", exact=True), 'click', "Select the 'AND' logical operator for combining filter conditions.")
    # Select the 'OR' logical operator for combining filter conditions.
    safe_action(shared_page, shared_page.get_by_text("OR", exact=True), 'click', "Select the 'OR' logical operator for combining filter conditions.")

@pytest.mark.order(22)
def test_column_filter_and_value_input(shared_page: Page):
    # Re-select the 'Contains' filter option to confirm the selection.
    safe_action(shared_page, shared_page.get_by_text("Contains"), 'click', "Re-select the 'Contains' filter option to confirm the selection.")
    # Click on the 'Column Filter' dropdown and choose the 'Contains' option.
    safe_action(shared_page, shared_page.get_by_label("Column Filter").get_by_text("Contains"), 'click', "Click on the 'Column Filter' dropdown and choose the 'Contains' option.")
    # Click on the 'Filter Value' textbox to input a value for filtering.
    safe_action(shared_page, shared_page.get_by_role("textbox", name="Filter Value"), 'click', "Click on the 'Filter Value' textbox to input a value for filtering.")

@pytest.mark.order(23)
def test_filter_reset_and_application(shared_page: Page):
    # Click on the 'Clear' button to clear the current filter value.
    safe_action(shared_page, shared_page.get_by_role("button", name="Clear"), 'click', "Click on the 'Clear' button to clear the current filter value.")
    # Click on the 'Reset' button to reset all filter settings to default.
    safe_action(shared_page, shared_page.get_by_role("button", name="Reset"), 'click', "Click on the 'Reset' button to reset all filter settings to default.")
    # Click on the filter icon in the column header to close the filter menu.
    safe_action(shared_page, shared_page.locator(".ag-header-icon.ag-header-cell-filter-button > .ag-icon").first, 'click', "Click on the filter icon in the column header to close the filter menu.")
    # Click on the 'Apply' button to apply the selected filter settings.
    safe_action(shared_page, shared_page.get_by_role("button", name="Apply"), 'click', "Click on the 'Apply' button to apply the selected filter settings.")

@pytest.mark.order(24)
def test_row_and_checkbox_selection(shared_page: Page):
    # Click on the first occurrence of the '3RD PARTY DISTRIB' text to select it.
    safe_action(shared_page, shared_page.locator("span").filter(has_text="3RD PARTY DISTRIB").first, 'click', "Click on the first occurrence of the '3RD PARTY DISTRIB' text to select it.")
    # Click on the '3RD PARTY DISTRIB' text to confirm the selection.
    safe_action(shared_page, shared_page.get_by_text("3RD PARTY DISTRIB"), 'click', "Click on the '3RD PARTY DISTRIB' text to confirm the selection.")
    # Click on the first checkbox in the group to select it.
    safe_action(shared_page, shared_page.locator(".ag-group-checkbox").first, 'click', "Click on the first checkbox in the group to select it.")
    # Check the row with the label 'Press Space to toggle row selection (unchecked)' for '99 CENT'.
    safe_action(shared_page, shared_page.get_by_role("gridcell", name="Press Space to toggle row selection (unchecked)  99 CENT").get_by_label("Press Space to toggle row"), 'check', "Check the row with the label 'Press Space to toggle row selection (unchecked)' for '99 CENT'.")

@pytest.mark.order(25)
def test_sorting_and_filter_menu_interaction(shared_page: Page):
    # Click on the third occurrence of the 'System Forecast Total (Plan' text to select it.
    safe_action(shared_page, shared_page.get_by_text("System Forecast Total (Plan").nth(2), 'click', "Click on the third occurrence of the 'System Forecast Total (Plan' text to select it.")
    # Click on the descending sort icon in the column header to toggle the sorting order.
    safe_action(shared_page, shared_page.locator(".ag-cell-label-container.ag-header-cell-sorted-desc > .ag-header-icon > .ag-icon"), 'click', "Click on the descending sort icon in the column header to toggle the sorting order.")
    # Open the filter menu by clicking on the filter body wrapper.
    safe_action(shared_page, shared_page.locator(".ag-filter-body-wrapper"), 'click', "Open the filter menu by clicking on the filter body wrapper.")

@pytest.mark.order(26)
def test_equality_and_comparison_filter_selection(shared_page: Page):
    # Select the 'Equals' filter option from the filter menu.
    safe_action(shared_page, shared_page.get_by_text("Equals"), 'click', "Select the 'Equals' filter option from the filter menu.")
    # Click on the 'Select Field' dropdown and choose the 'Equals' option.
    safe_action(shared_page, shared_page.get_by_label("Select Field").get_by_text("Equals"), 'click', "Click on the 'Select Field' dropdown and choose the 'Equals' option.")
    # Re-select the 'Equals' filter option to confirm the selection.
    safe_action(shared_page, shared_page.get_by_text("Equals"), 'click', "Re-select the 'Equals' filter option to confirm the selection.")
    # Select the 'Does not equal' filter option from the filter menu.
    safe_action(shared_page, shared_page.get_by_text("Does not equal"), 'click', "Select the 'Does not equal' filter option from the filter menu.")
    # Re-select the 'Does not equal' filter option to confirm the selection.
    safe_action(shared_page, shared_page.get_by_text("Does not equal"), 'click', "Re-select the 'Does not equal' filter option to confirm the selection.")
    # Select the 'Greater than' filter option from the filter menu.
    safe_action(shared_page, shared_page.get_by_text("Greater than", exact=True), 'click', "Select the 'Greater than' filter option from the filter menu.")
    # Re-select the 'Greater than' filter option to confirm the selection.
    safe_action(shared_page, shared_page.get_by_text("Greater than"), 'click', "Re-select the 'Greater than' filter option to confirm the selection.")

@pytest.mark.order(27)
def test_filter_selection_and_confirmation(shared_page: Page):
    # Select the 'Greater than or equal to' filter option from the filter menu.
    safe_action(shared_page, shared_page.get_by_text("Greater than or equal to"), 'click', "Select the 'Greater than or equal to' filter option from the filter menu.")
    # Re-select the 'Greater than or equal to' filter option to confirm the selection.
    safe_action(shared_page, shared_page.get_by_text("Greater than or equal to"), 'click', "Re-select the 'Greater than or equal to' filter option to confirm the selection.")
    # Select the 'Less than' filter option from the filter menu.
    safe_action(shared_page, shared_page.get_by_role("option", name="Less than", exact=True), 'click', "Select the 'Less than' filter option from the filter menu.")
    # Re-select the 'Less than' filter option to confirm the selection.
    safe_action(shared_page, shared_page.get_by_text("Less than"), 'click', "Re-select the 'Less than' filter option to confirm the selection.")
    # Select the 'Less than or equal to' filter option from the filter menu.
    safe_action(shared_page, shared_page.get_by_text("Less than or equal to"), 'click', "Select the 'Less than or equal to' filter option from the filter menu.")
    # Re-select the 'Less than or equal to' filter option to confirm the selection.
    safe_action(shared_page, shared_page.get_by_text("Less than or equal to"), 'click', "Re-select the 'Less than or equal to' filter option to confirm the selection.")
    # Select the 'Between' filter option from the filter menu.
    safe_action(shared_page, shared_page.get_by_role("option", name="Between"), 'click', "Select the 'Between' filter option from the filter menu.")
    # Re-select the 'Between' filter option to confirm the selection.
    safe_action(shared_page, shared_page.get_by_text("Between"), 'click', "Re-select the 'Between' filter option to confirm the selection.")
    # Select the 'Blank' filter option from the filter menu.
    safe_action(shared_page, shared_page.get_by_role("option", name="Blank", exact=True), 'click', "Select the 'Blank' filter option from the filter menu.")
    # Re-select the 'Blank' filter option to confirm the selection.
    safe_action(shared_page, shared_page.get_by_text("Blank"), 'click', "Re-select the 'Blank' filter option to confirm the selection.")
    # Select the 'Not blank' filter option from the filter menu.
    safe_action(shared_page, shared_page.get_by_role("option", name="Not blank"), 'click', "Select the 'Not blank' filter option from the filter menu.")

@pytest.mark.order(28)
def test_filter_reset_and_application(shared_page: Page):
    # Click on the 'Clear' button to clear the current filter value.
    safe_action(shared_page, shared_page.get_by_role("button", name="Clear"), 'click', "Click on the 'Clear' button to clear the current filter value.")
    # Click on the 'Reset' button to reset all filter settings to default.
    safe_action(shared_page, shared_page.get_by_role("button", name="Reset"), 'click', "Click on the 'Reset' button to reset all filter settings to default.")
    # Click on the descending sort icon in the column header to toggle the sorting order.
    safe_action(shared_page, shared_page.locator(".ag-cell-label-container.ag-header-cell-sorted-desc > .ag-header-icon > .ag-icon"), 'click', "Click on the descending sort icon in the column header to toggle the sorting order.")
    # Click on the 'Apply' button to apply the selected filter settings.
    safe_action(shared_page, shared_page.get_by_role("button", name="Apply"), 'click', "Click on the 'Apply' button to apply the selected filter settings.")

@pytest.mark.order(29)
def test_sorting_operations(shared_page: Page):
    # Click on the descending sort icon in the column header to sort the column in descending order.
    safe_action(shared_page, shared_page.locator(".ag-cell-label-container.ag-header-cell-sorted-desc > .ag-header-cell-label > .ag-sort-indicator-container > .ag-sort-indicator-icon.ag-sort-descending-icon > .ag-icon"), 'click', "Click on the descending sort icon in the column header to sort the column in descending order.")
    # Click on the ascending sort icon in the column header to sort the column in ascending order.
    safe_action(shared_page, shared_page.locator(".ag-cell-label-container.ag-header-cell-sorted-asc > .ag-header-cell-label > .ag-sort-indicator-container > .ag-sort-indicator-icon.ag-sort-ascending-icon > .ag-icon"), 'click', "Click on the ascending sort icon in the column header to sort the column in ascending order.")
    # Click on the 'System Forecast Base (Plan Week)' column header to select it.
    safe_action(shared_page, shared_page.get_by_text("System Forecast Base (Plan Week)"), 'click', "Click on the 'System Forecast Base (Plan Week)' column header to select it.")
    # Click on the descending sort icon in the column header to sort the column in descending order again.
    safe_action(shared_page, shared_page.locator(".ag-cell-label-container.ag-header-cell-sorted-desc > .ag-header-cell-label > .ag-sort-indicator-container > .ag-sort-indicator-icon.ag-sort-descending-icon > .ag-icon"), 'click', "Click on the descending sort icon in the column header to sort the column in descending order again.")
    # Click on the descending sort icon in the column header to toggle the sorting order.
    safe_action(shared_page, shared_page.locator(".ag-cell-label-container.ag-header-cell-sorted-desc > .ag-header-cell-label > .ag-sort-indicator-container > .ag-sort-indicator-icon.ag-sort-descending-icon > .ag-icon"), 'click', "Click on the descending sort icon in the column header to toggle the sorting order.")

@pytest.mark.order(30)
def test_filter_menu_interaction(shared_page: Page):
    # Click on the filter button in the column header to open the filter menu.
    safe_action(shared_page, shared_page.locator(".ag-header-icon.ag-header-cell-filter-button.ag-has-popup-positioned-under > .ag-icon"), 'click', "Click on the filter button in the column header to open the filter menu.")
    # Click on the filter body wrapper to open the advanced filtering options.
    safe_action(shared_page, shared_page.locator(".ag-filter-body-wrapper"), 'click', "Click on the filter body wrapper to open the advanced filtering options.")
    # Click on the 'Filtering operator' dropdown to select a filtering condition.
    safe_action(shared_page, shared_page.get_by_role("combobox", name="Filtering operator"), 'click', "Click on the 'Filtering operator' dropdown to select a filtering condition.")

@pytest.mark.order(31)
def test_filtering_operator_selection(shared_page: Page):
    # Select the 'Equals' option from the filtering operator dropdown.
    safe_action(shared_page, shared_page.get_by_label("Select Field").get_by_text("Equals"), 'click', "Select the 'Equals' option from the filtering operator dropdown.")
    safe_action(shared_page, shared_page.get_by_text("Equals"), 'click', "Perform click on page.get_by_text(\"Equals\")")
    # Select the 'Does not equal' option from the filtering operator dropdown.
    safe_action(shared_page, shared_page.get_by_text("Does not equal"), 'click', "Select the 'Does not equal' option from the filtering operator dropdown.")
    safe_action(shared_page, shared_page.get_by_text("Does not equal"), 'click', "Perform click on page.get_by_text(\"Does not equal\")")
    # Select the 'Greater than' option from the filtering operator dropdown.
    safe_action(shared_page, shared_page.get_by_role("option", name="Greater than", exact=True), 'click', "Select the 'Greater than' option from the filtering operator dropdown.")
    safe_action(shared_page, shared_page.get_by_text("Greater than"), 'click', "Perform click on page.get_by_text(\"Greater than\")")
    # Select the 'Less than' option from the filtering operator dropdown.
    safe_action(shared_page, shared_page.get_by_role("option", name="Less than", exact=True), 'click', "Select the 'Less than' option from the filtering operator dropdown.")
    safe_action(shared_page, shared_page.get_by_text("Less than"), 'click', "Perform click on page.get_by_text(\"Less than\")")
    # Select the 'Greater than or equal to' option from the filtering operator dropdown.
    safe_action(shared_page, shared_page.get_by_text("Greater than or equal to"), 'click', "Select the 'Greater than or equal to' option from the filtering operator dropdown.")

@pytest.mark.order(32)
def test_filter_operator_selection(shared_page: Page):
    safe_action(shared_page, shared_page.get_by_text("Greater than or equal to"), 'click', "Perform click on page.get_by_text(\"Greater than or equal to\")")
    # Select the 'Less than or equal to' option from the filtering operator dropdown.
    safe_action(shared_page, shared_page.get_by_role("option", name="Less than or equal to"), 'click', "Select the 'Less than or equal to' option from the filtering operator dropdown.")
    safe_action(shared_page, shared_page.get_by_text("Less than or equal to"), 'click', "Perform click on page.get_by_text(\"Less than or equal to\")")
    # Select the 'Between' option from the filtering operator dropdown.
    safe_action(shared_page, shared_page.get_by_role("option", name="Between"), 'click', "Select the 'Between' option from the filtering operator dropdown.")
    safe_action(shared_page, shared_page.get_by_text("Between"), 'click', "Perform click on page.get_by_text(\"Between\")")
    # Select the 'Blank' option from the filtering operator dropdown.
    safe_action(shared_page, shared_page.get_by_role("option", name="Blank", exact=True), 'click', "Select the 'Blank' option from the filtering operator dropdown.")
    safe_action(shared_page, shared_page.get_by_text("Blank"), 'click', "Perform click on page.get_by_text(\"Blank\")")
    # Select the 'Not blank' option from the filtering operator dropdown.
    safe_action(shared_page, shared_page.get_by_role("option", name="Not blank"), 'click', "Select the 'Not blank' option from the filtering operator dropdown.")

@pytest.mark.order(33)
def test_filter_condition_and_value_input(shared_page: Page):
    # Click on the 'AND' radio button to set the filter condition to 'AND'.
    safe_action(shared_page, shared_page.locator(".ag-labeled.ag-label-align-right.ag-radio-button").first, 'click', "Click on the 'AND' radio button to set the filter condition to 'AND'.")
    # Click on the 'OR' radio button to set the filter condition to 'OR'.
    safe_action(shared_page, shared_page.locator(".ag-labeled.ag-label-align-right.ag-radio-button.ag-input-field.ag-filter-condition-operator.ag-filter-condition-operator-or"), 'click', "Click on the 'OR' radio button to set the filter condition to 'OR'.")
    # Click on the 'Filter Value' input field to enter a value for filtering.
    safe_action(shared_page, shared_page.get_by_role("spinbutton", name="Filter Value"), 'click', "Click on the 'Filter Value' input field to enter a value for filtering.")
    # Fill the 'Filter Value' input field with the value '2'.
    safe_action(shared_page, shared_page.get_by_role("spinbutton", name="Filter Value"), 'fill', "Fill the 'Filter Value' input field with the value '2'.", "2")
    # Press 'Enter' to apply the entered filter value.
    safe_action(shared_page, shared_page.get_by_role("spinbutton", name="Filter Value"), 'press', "Press 'Enter' to apply the entered filter value.", "Enter")

@pytest.mark.order(34)
def test_filter_application_and_reset(shared_page: Page):
    safe_action(shared_page, shared_page.get_by_role("spinbutton", name="Filter Value"), 'click', "Perform click on page.get_by_role(\"spinbutton\", name=\"Filter Value\")")
    # Click on the 'Apply' button to apply the selected filter criteria.
    safe_action(shared_page, shared_page.get_by_role("button", name="Apply"), 'click', "Click on the 'Apply' button to apply the selected filter criteria.")
    # Click on the active filter icon to open the filter options for the column.
    safe_action(shared_page, shared_page.locator(".ag-header-icon.ag-header-cell-filter-button.ag-filter-active > .ag-icon"), 'click', "Click on the active filter icon to open the filter options for the column.")
    # Click on the 'Reset' button to reset the filter settings to their default state.
    safe_action(shared_page, shared_page.get_by_role("button", name="Reset"), 'click', "Click on the 'Reset' button to reset the filter settings to their default state.")

@pytest.mark.order(35)
def test_column_and_filter_options(shared_page: Page):
    # Click on the column header icon to open sorting or additional options for the column.
    safe_action(shared_page, shared_page.locator(".ag-header-cell.ag-header-parent-hidden.ag-header-cell-sortable.ag-header-background.ag-focus-managed.ag-header-active > .ag-header-cell-comp-wrapper > .ag-cell-label-container > .ag-header-icon > .ag-icon"), 'click', "Click on the column header icon to open sorting or additional options for the column.")
    # Click on the 'Clear' button to remove all applied filters from the column.
    safe_action(shared_page, shared_page.get_by_role("button", name="Clear"), 'click', "Click on the 'Clear' button to remove all applied filters from the column.")
    # Click on the 'Customers columns (0)' text to open the column options.
    safe_action(shared_page, shared_page.get_by_text("Customers columns (0)"), 'click', "Click on the 'Customers columns (0)' text to open the column options.")

@pytest.mark.order(36)
def test_pagination_interaction(shared_page: Page):
    # Click on the pagination element to interact with the pagination controls.
    safe_action(shared_page, shared_page.locator("esp-row-dimentional-grid #paginationId"), 'click', "Click on the pagination element to interact with the pagination controls.")
    # Click on the 'Showing 10 out of' text to view the current row display information.
    safe_action(shared_page, shared_page.get_by_text("Showing 10 out of"), 'click', "Click on the 'Showing 10 out of' text to view the current row display information.")
    safe_action(shared_page, shared_page.get_by_text("Showing 10 out of 138 12345"), 'click', "Perform click on page.get_by_text(\"Showing 10 out of 138 12345\")")
    # Click on the 'View 10 row(s)' option to set the number of rows displayed to 10.
    safe_action(shared_page, shared_page.get_by_text("View 10 row(s)").first, 'click', "Click on the 'View 10 row(s)' option to set the number of rows displayed to 10.")
    safe_action(shared_page, shared_page.locator("span").filter(has_text=re.compile(r"^View 10 row\(s\)$")), 'click', "Perform click on page.locator(\"span\").filter(has_text=re.compile(r\"^View 10 row\\(s\\)$\"))")
    # Click on the 'Rows per page' text to open the dropdown for selecting the number of rows displayed per page.
    safe_action(shared_page, shared_page.get_by_text("Rows per page"), 'click', "Click on the 'Rows per page' text to open the dropdown for selecting the number of rows displayed per page.")
    safe_action(shared_page, shared_page.get_by_text("Showing 10 out of 138 12345"), 'click', "Perform click on page.get_by_text(\"Showing 10 out of 138 12345\")")
    # Click on the list item with the text '1' to navigate to the first page of the pagination.
    safe_action(shared_page, shared_page.get_by_role("listitem").filter(has_text=re.compile(r"^1$")), 'click', "Click on the list item with the text '1' to navigate to the first page of the pagination.")
    # Click on the pagination link with the text '2' to navigate to the second page.
    safe_action(shared_page, shared_page.locator("a").filter(has_text="2"), 'click', "Click on the pagination link with the text '2' to navigate to the second page.")
    # Click on the left chevron icon to navigate to the previous page in the pagination.
    safe_action(shared_page, shared_page.locator(".zeb-chevron-left"), 'click', "Click on the left chevron icon to navigate to the previous page in the pagination.")
    safe_action(shared_page, shared_page.get_by_text("12345...14"), 'click', "Perform click on page.get_by_text(\"12345...14\")")
    safe_action(shared_page, shared_page.get_by_text("12345...14"), 'click', "Perform click on page.get_by_text(\"12345...14\")")
    # Click on the right chevron icon to navigate to the next page in the pagination.
    safe_action(shared_page, shared_page.locator(".pagination-next > .zeb-chevron-right"), 'click', "Click on the right chevron icon to navigate to the next page in the pagination.")
    # Click on the 'Last' navigation button to navigate to the last page in the pagination.
    safe_action(shared_page, shared_page.locator(".zeb-nav-to-last"), 'click', "Click on the 'Last' navigation button to navigate to the last page in the pagination.")

@pytest.mark.order(37)
def test_row_display_adjustment(shared_page: Page):
    safe_action(shared_page, shared_page.locator(".w-100.p-h-16"), 'click', "Perform click on page.locator(\".w-100.p-h-16\")")
    # Click on the 'View 20 row(s)' option to set the number of rows displayed to 20.

@pytest.mark.order(38)
def test_row_display_and_selection(shared_page: Page):
    safe_action(shared_page, shared_page.locator("div").filter(has_text=re.compile(r"^View 20 row\(s\)$")).first, 'click', "Perform click on page.locator(\"div\").filter(has_text=re.compile(r\"^View 20 row\\(s\\)$\")).first")
    # Click on the 'Showing 20 out of' text to view the updated row display information.
    safe_action(shared_page, shared_page.get_by_text("Showing 20 out of"), 'click', "Click on the 'Showing 20 out of' text to view the updated row display information.")
    # Select the grid cell labeled 'Press Space to toggle row selection (unchecked)' for the row '3RD PARTY DISTRIB'.
    safe_action(shared_page, shared_page.get_by_role("gridcell", name="Press Space to toggle row selection (unchecked)  3RD PARTY DISTRIB").get_by_label("Press Space to toggle row"), 'check', "Select the grid cell labeled 'Press Space to toggle row selection (unchecked)' for the row '3RD PARTY DISTRIB'.")

@pytest.mark.order(39)
def test_filter_options_interaction(shared_page: Page):
    # Click on the 'FilterTime Latest Order &' text to open the filter options.
    safe_action(shared_page, shared_page.get_by_text("FilterTime Latest Order &"), 'click', "Click on the 'FilterTime Latest Order &' text to open the filter options.")
    # Click on the 'Filter' button within a div element to apply or modify filters.
    safe_action(shared_page, shared_page.locator("div").filter(has_text=re.compile(r"^Filter$")), 'click', "Click on the 'Filter' button within a div element to apply or modify filters.")
    # Click on the 'Time' text to select the time filter option.
    safe_action(shared_page, shared_page.get_by_text("Time"), 'click', "Click on the 'Time' text to select the time filter option.")
    # Click on the dropdown labeled '.w-100.p-h-16.p-v-8.dropdown-label.background-white' to open the filter options.
    safe_action(shared_page, shared_page.locator(".w-100.p-h-16.p-v-8.dropdown-label.background-white"), 'click', "Click on the dropdown labeled '.w-100.p-h-16.p-v-8.dropdown-label.background-white' to open the filter options.")
    # Select the filter option labeled 'Latest Order & Plan Week' from the dropdown.
    safe_action(shared_page, shared_page.locator("span").filter(has_text="Latest Order & Plan Week"), 'click', "Select the filter option labeled 'Latest Order & Plan Week' from the dropdown.")
    # Click on the 'FilterTime Latest Order &' text again to confirm or apply the selected filter.
    safe_action(shared_page, shared_page.get_by_text("FilterTime Latest Order &"), 'click', "Click on the 'FilterTime Latest Order &' text again to confirm or apply the selected filter.")

@pytest.mark.order(40)
def test_daily_summary_navigation(shared_page: Page):
    # Click on the 'Daily Summary Customer:3RD' text to navigate to the daily summary for the specified customer.
    safe_action(shared_page, shared_page.get_by_text("Daily Summary Customer:3RD"), 'click', "Click on the 'Daily Summary Customer:3RD' text to navigate to the daily summary for the specified customer.")
    # Click on the 'Daily Summary' text to view the daily summary section.
    safe_action(shared_page, shared_page.get_by_text("Daily Summary"), 'click', "Click on the 'Daily Summary' text to view the daily summary section.")
    # Click on the 'Customer' text (exact match) to interact with the customer-specific options.
    safe_action(shared_page, shared_page.get_by_text("Customer", exact=True).nth(2), 'click', "Click on the 'Customer' text (exact match) to interact with the customer-specific options.")
    # Click on the 'Customer:3RD PARTY DISTRIB' text to select the specific customer.
    safe_action(shared_page, shared_page.get_by_text("Customer:3RD PARTY DISTRIB").first, 'click', "Click on the 'Customer:3RD PARTY DISTRIB' text to select the specific customer.")
    # Click on the '3RD PARTY DISTRIB' text (second occurrence) to confirm or refine the selection.
    safe_action(shared_page, shared_page.get_by_text("3RD PARTY DISTRIB").nth(1), 'click', "Click on the '3RD PARTY DISTRIB' text (second occurrence) to confirm or refine the selection.")

@pytest.mark.order(41)
def test_dropdown_selection_and_confirmation(shared_page: Page):
    # Click on the dropdown to open the list of options for selection.
    safe_action(shared_page, shared_page.locator(".wr-20.font-weight-normal > esp-multiselect-dropdown > .multiselect-dropdown > div > .w-100"), 'click', "Click on the dropdown to open the list of options for selection.")
    # Select the first option from the dropdown list.
    safe_action(shared_page, shared_page.locator(".d-flex.dropdown-option").first, 'click', "Select the first option from the dropdown list.")
    # Re-select the first option from the dropdown list, possibly to confirm the selection.
    safe_action(shared_page, shared_page.locator(".d-flex.dropdown-option").first, 'click', "Re-select the first option from the dropdown list, possibly to confirm the selection.")
    # Click on a specific dropdown option with additional alignment and padding styles.
    safe_action(shared_page, shared_page.locator(".d-flex.dropdown-option.align-items-center.p-v-5.p-l-32 > .d-flex").first, 'click', "Click on a specific dropdown option with additional alignment and padding styles.")
    # Click on the first checkbox to select it.
    safe_action(shared_page, shared_page.locator(".d-flex.flex-column.justify-content-center.font-size-10.align-items-center.checkbox-v2.m-r-10.zeb-check").first, 'click', "Click on the first checkbox to select it.")
    # Click on the first checkbox again, possibly to toggle or confirm the selection.
    safe_action(shared_page, shared_page.locator(".d-flex.flex-column.justify-content-center.font-size-10.align-items-center.checkbox-v2.m-r-10.zeb-check").first, 'click', "Click on the first checkbox again, possibly to toggle or confirm the selection.")
    # Click on the first checkbox again, possibly as part of a repeated action.
    safe_action(shared_page, shared_page.locator(".d-flex.flex-column.justify-content-center.font-size-10.align-items-center.checkbox-v2.m-r-10.zeb-check").first, 'click', "Click on the first checkbox again, possibly as part of a repeated action.")
    safe_action(shared_page, shared_page.locator(".d-flex.flex-column.justify-content-center.font-size-10.align-items-center.checkbox-v2.m-r-10.zeb-check").first, 'click', "Perform click on page.locator(\".d-flex.flex-column.justify-content-center.font-size-10.align-items-center.checkbox-v2.m-r-10.zeb-check\").first")
    safe_action(shared_page, shared_page.locator(".d-flex.flex-column.justify-content-center.font-size-10.align-items-center.checkbox-v2.m-r-10.zeb-check").first, 'click', "Perform click on page.locator(\".d-flex.flex-column.justify-content-center.font-size-10.align-items-center.checkbox-v2.m-r-10.zeb-check\").first")
    safe_action(shared_page, shared_page.locator(".d-flex.flex-column.justify-content-center.font-size-10.align-items-center.checkbox-v2.m-r-10.zeb-check").first, 'click', "Perform click on page.locator(\".d-flex.flex-column.justify-content-center.font-size-10.align-items-center.checkbox-v2.m-r-10.zeb-check\").first")
    safe_action(shared_page, shared_page.locator(".d-flex.flex-column.justify-content-center.font-size-10.align-items-center.checkbox-v2.m-r-10.zeb-check").first, 'click', "Perform click on page.locator(\".d-flex.flex-column.justify-content-center.font-size-10.align-items-center.checkbox-v2.m-r-10.zeb-check\").first")
    safe_action(shared_page, shared_page.locator(".d-flex.flex-column.justify-content-center.font-size-10.align-items-center.checkbox-v2.m-r-10.zeb-check").first, 'click', "Perform click on page.locator(\".d-flex.flex-column.justify-content-center.font-size-10.align-items-center.checkbox-v2.m-r-10.zeb-check\").first")
    safe_action(shared_page, shared_page.locator(".d-flex.flex-column.justify-content-center.font-size-10.align-items-center.checkbox-v2.m-r-10.zeb-check").first, 'click', "Perform click on page.locator(\".d-flex.flex-column.justify-content-center.font-size-10.align-items-center.checkbox-v2.m-r-10.zeb-check\").first")
    safe_action(shared_page, shared_page.locator(".d-flex.flex-column.justify-content-center.font-size-10.align-items-center.checkbox-v2.m-r-10.zeb-check").first, 'click', "Perform click on page.locator(\".d-flex.flex-column.justify-content-center.font-size-10.align-items-center.checkbox-v2.m-r-10.zeb-check\").first")
    safe_action(shared_page, shared_page.locator(".d-flex.flex-column.justify-content-center.font-size-10.align-items-center.checkbox-v2.m-r-10.zeb-check").first, 'click', "Perform click on page.locator(\".d-flex.flex-column.justify-content-center.font-size-10.align-items-center.checkbox-v2.m-r-10.zeb-check\").first")
    safe_action(shared_page, shared_page.locator(".d-flex.flex-column.justify-content-center.font-size-10.align-items-center.checkbox-v2.m-r-10.zeb-check").first, 'click', "Perform click on page.locator(\".d-flex.flex-column.justify-content-center.font-size-10.align-items-center.checkbox-v2.m-r-10.zeb-check\").first")
    safe_action(shared_page, shared_page.locator(".d-flex.flex-column.justify-content-center.font-size-10.align-items-center.checkbox-v2.m-r-10.zeb-check").first, 'click', "Perform click on page.locator(\".d-flex.flex-column.justify-content-center.font-size-10.align-items-center.checkbox-v2.m-r-10.zeb-check\").first")
    # Click on a selected dropdown option to finalize or confirm the selection.
    safe_action(shared_page, shared_page.locator(".d-flex.dropdown-option.align-items-center.p-v-5.p-l-32.p-r-16.selected").first, 'click', "Click on a selected dropdown option to finalize or confirm the selection.")

@pytest.mark.order(42)
def test_specific_option_selection(shared_page: Page):
    # Click on the 'Aged Net Units (CW-5)' option to select it from the dropdown.
    safe_action(shared_page, shared_page.get_by_text("Aged Net Units (CW-5)", exact=True), 'click', "Click on the 'Aged Net Units (CW-5)' option to select it from the dropdown.")
    # Click on the 'Aged Net Units (CW-6)' option to select it from the dropdown.
    safe_action(shared_page, shared_page.get_by_text("Aged Net Units (CW-6)", exact=True), 'click', "Click on the 'Aged Net Units (CW-6)' option to select it from the dropdown.")
    # Click on the 'Scan Units (CW-4)' option to select it from the dropdown.
    safe_action(shared_page, shared_page.get_by_text("Scan Units (CW-4)", exact=True), 'click', "Click on the 'Scan Units (CW-4)' option to select it from the dropdown.")
    # Click on the second occurrence of the 'Scan Units (CW-3)' option to select it.

@pytest.mark.order(43)
def test_dropdown_selection_and_navigation(shared_page: Page):
    safe_action(shared_page, shared_page.get_by_text("Scan Units (CW-3)").nth(1), 'click', "Perform click on page.get_by_text(\"Scan Units (CW-3)\").nth(1)")
    # Click on the 'Scan Units (CW-5)' option to select it from the dropdown.
    safe_action(shared_page, shared_page.get_by_text("Scan Units (CW-5)", exact=True), 'click', "Click on the 'Scan Units (CW-5)' option to select it from the dropdown.")
    # Click on the 'Scan Units (CW-6)' option within a span element to select it.
    safe_action(shared_page, shared_page.locator("span").filter(has_text="Scan Units (CW-6)"), 'click', "Click on the 'Scan Units (CW-6)' option within a span element to select it.")
    # Click on the 'Daily Summary Customer:3RD' option to select it from the dropdown.
    safe_action(shared_page, shared_page.get_by_text("Daily Summary Customer:3RD"), 'click', "Click on the 'Daily Summary Customer:3RD' option to select it from the dropdown.")
    # Click on the button within the 'Daily Summary Customer:3RD' card to open its options.
    safe_action(shared_page, shared_page.locator("esp-card-component").filter(has_text="Daily Summary Customer:3RD").get_by_role("button"), 'click', "Click on the button within the 'Daily Summary Customer:3RD' card to open its options.")

@pytest.mark.order(44)
def test_column_visibility_management(shared_page: Page):
    # Click on the textbox labeled 'Filter Columns Input' to activate the column filter input field.
    safe_action(shared_page, shared_page.get_by_role("textbox", name="Filter Columns Input"), 'click', "Click on the textbox labeled 'Filter Columns Input' to activate the column filter input field.")
    # Uncheck the checkbox labeled 'Toggle All Columns Visibility' to hide all columns.
    safe_action(shared_page, shared_page.get_by_role("checkbox", name="Toggle All Columns Visibility"), 'uncheck', "Uncheck the checkbox labeled 'Toggle All Columns Visibility' to hide all columns.")
    # Check the checkbox labeled 'Toggle All Columns Visibility' to make all columns visible again.
    safe_action(shared_page, shared_page.get_by_role("checkbox", name="Toggle All Columns Visibility"), 'check', "Check the checkbox labeled 'Toggle All Columns Visibility' to make all columns visible again.")
    # Click on the '/01(Sun)' label within the '/01(Sun) Column' to toggle its visibility.
    safe_action(shared_page, shared_page.get_by_label("/01(Sun) Column").get_by_text("/01(Sun)"), 'click', "Click on the '/01(Sun)' label within the '/01(Sun) Column' to toggle its visibility.")
    # Click on the '/02(Mon)' label within the '/02(Mon) Column' to toggle its visibility.
    safe_action(shared_page, shared_page.get_by_label("/02(Mon) Column").get_by_text("/02(Mon)"), 'click', "Click on the '/02(Mon)' label within the '/02(Mon) Column' to toggle its visibility.")
    # Uncheck the checkbox for the '/03(Tue) Column' to hide this column.
    safe_action(shared_page, shared_page.get_by_role("treeitem", name="/03(Tue) Column").get_by_label("Press SPACE to toggle visibility (visible)"), 'uncheck', "Uncheck the checkbox for the '/03(Tue) Column' to hide this column.")
    # Uncheck the checkbox for the '/05(Thu) Column' to hide this column.
    safe_action(shared_page, shared_page.get_by_role("treeitem", name="/05(Thu) Column").get_by_label("Press SPACE to toggle visibility (visible)"), 'uncheck', "Uncheck the checkbox for the '/05(Thu) Column' to hide this column.")
    # Uncheck the checkbox for the '/04(Wed) Column' to hide this column.
    safe_action(shared_page, shared_page.get_by_role("treeitem", name="/04(Wed) Column").get_by_label("Press SPACE to toggle visibility (visible)"), 'uncheck', "Uncheck the checkbox for the '/04(Wed) Column' to hide this column.")

@pytest.mark.order(45)
def test_file_export_and_preferences_management(shared_page: Page):
    # Wait for a file download to be triggered when the export icon is clicked.
    with shared_page.expect_download() as download2_info:
    # Click on the export icon to initiate the download of the grid data.
        safe_action(shared_page, shared_page.locator("span:nth-child(6) > esp-grid-icons-component > .display-grid-icons > div:nth-child(2) > #export-iconId > .icon-color-toolbar-active"), 'click', "Click on the export icon to initiate the download of the grid data.")
    download2 = download2_info.value
    # Click on the preferences icon to open the preferences dropdown menu.
    safe_action(shared_page, shared_page.locator("span:nth-child(6) > esp-grid-icons-component > .display-grid-icons > div:nth-child(3) > #preference-iconId > .legend-font > .multiselect-dropdown > .pointer"), 'click', "Click on the preferences icon to open the preferences dropdown menu.")
    # Select the 'Save Preference' option from the preferences dropdown to save the current grid settings.
    safe_action(shared_page, shared_page.get_by_text("Save Preference"), 'click', "Select the 'Save Preference' option from the preferences dropdown to save the current grid settings.")
    # Click on the preferences icon again to reopen the preferences dropdown menu.
    safe_action(shared_page, shared_page.locator("span:nth-child(6) > esp-grid-icons-component > .display-grid-icons > div:nth-child(3) > #preference-iconId > .legend-font > .multiselect-dropdown > .pointer"), 'click', "Click on the preferences icon again to reopen the preferences dropdown menu.")
    # Select the 'Reset Preference' option from the preferences dropdown to reset the grid settings to default.
    safe_action(shared_page, shared_page.get_by_text("Reset Preference"), 'click', "Select the 'Reset Preference' option from the preferences dropdown to reset the grid settings to default.")
    # Click on the preferences icon once more to reopen the preferences dropdown menu.
    safe_action(shared_page, shared_page.locator("span:nth-child(6) > esp-grid-icons-component > .display-grid-icons > div:nth-child(3) > #preference-iconId > .legend-font > .multiselect-dropdown > .pointer"), 'click', "Click on the preferences icon once more to reopen the preferences dropdown menu.")

@pytest.mark.order(46)
def test_filter_and_grid_interaction(shared_page: Page):
    # Click on the button within the 'Daily Summary Customer:3RD' card to open the dropdown menu for further actions.
    safe_action(shared_page, shared_page.locator("esp-card-component").filter(has_text="Daily Summary Customer:3RD").get_by_role("button"), 'click', "Click on the button within the 'Daily Summary Customer:3RD' card to open the dropdown menu for further actions.")
    # Click on the dropdown field to expand the multiselect options for filtering.
    safe_action(shared_page, shared_page.locator(".wr-20.font-weight-normal > esp-multiselect-dropdown > .multiselect-dropdown > div > .w-100"), 'click', "Click on the dropdown field to expand the multiselect options for filtering.")
    # Select the 'Select All' option to include all available items in the filter.
    safe_action(shared_page, shared_page.get_by_text("Select All"), 'click', "Select the 'Select All' option to include all available items in the filter.")
    # Click on the 'Daily Summary Customer:3RD' option to specifically filter by this customer.
    safe_action(shared_page, shared_page.get_by_text("Daily Summary Customer:3RD"), 'click', "Click on the 'Daily Summary Customer:3RD' option to specifically filter by this customer.")
    # Click on the header cell to interact with the first column in the grid.
    safe_action(shared_page, shared_page.locator(".ag-header-cell.ag-column-first.ag-header-parent-hidden.ag-header-background.ag-focus-managed.ag-header-active > .ag-header-cell-comp-wrapper > .ag-cell-label-container > .ag-header-cell-label"), 'click', "Click on the header cell to interact with the first column in the grid.")
    # Click on the 'User Suggested Order Total' column header to sort or interact with this column.
    safe_action(shared_page, shared_page.get_by_text("User Suggested Order Total"), 'click', "Click on the 'User Suggested Order Total' column header to sort or interact with this column.")
    # Click on the first icon (likely a dropdown or action button) within the grid.
    safe_action(shared_page, shared_page.locator("i").first, 'click', "Click on the first icon (likely a dropdown or action button) within the grid.")
    # Click on the 'User Override Total' column header to sort or interact with this column.
    safe_action(shared_page, shared_page.get_by_text("User Override Total"), 'click', "Click on the 'User Override Total' column header to sort or interact with this column.")
    # Click on the third icon (likely a dropdown or action button) within the grid.
    safe_action(shared_page, shared_page.locator("i").nth(2), 'click', "Click on the third icon (likely a dropdown or action button) within the grid.")
    # Click on the 'Gross Units (CW-3)' column header within the grid to interact with it.
    safe_action(shared_page, shared_page.locator("esp-column-dimentional-grid").get_by_text("Gross Units (CW-3)"), 'click', "Click on the 'Gross Units (CW-3)' column header within the grid to interact with it.")

@pytest.mark.order(47)
def test_grid_interaction_and_expansion(shared_page: Page):
    # Click on the first 'Gross Units (CW-3)' text element to interact with it.
    safe_action(shared_page, shared_page.locator("span").filter(has_text="Gross Units (CW-3)").first, 'click', "Click on the first 'Gross Units (CW-3)' text element to interact with it.")
    # Click on the sixth icon (likely a dropdown or action button) within the grid.
    safe_action(shared_page, shared_page.locator("i").nth(5), 'click', "Click on the sixth icon (likely a dropdown or action button) within the grid.")
    # Click on the 'Aged Net Units (CW-3)' column header within the grid to interact with it.
    safe_action(shared_page, shared_page.locator("esp-column-dimentional-grid").get_by_text("Aged Net Units (CW-3)"), 'click', "Click on the 'Aged Net Units (CW-3)' column header within the grid to interact with it.")
    # Click on the expand/collapse icon within the last left-pinned cell of the grid to expand or collapse the row.
    safe_action(shared_page, shared_page.locator(".ag-cell-value.ag-cell.ag-cell-not-inline-editing.ag-cell-normal-height.ag-cell-last-left-pinned.ag-column-first.ag-cell-override-normal.notosans-overwrite.no-border.ag-cell-focus > .ag-cell-wrapper > .ag-group-contracted > .zeb-chevron-right"), 'click', "Click on the expand/collapse icon within the last left-pinned cell of the grid to expand or collapse the row.")
    # Click on the expand icon (chevron) in the first row of the grid to expand the group.
    safe_action(shared_page, shared_page.locator(".ag-row-no-focus.ag-row-not-inline-editing.ag-row.ag-row-level-0.ag-row-group.ag-row-group-contracted.ag-row-position-absolute.ag-row-even.ag-row-hover > .ag-cell-value > .ag-cell-wrapper > .ag-group-contracted > .zeb-chevron-right"), 'click', "Click on the expand icon (chevron) in the first row of the grid to expand the group.")

@pytest.mark.order(48)
def test_column_and_trend_analysis_interaction(shared_page: Page):
    # Click on the 'Scan Units (CW-3)' column header within the grid to interact with it.
    safe_action(shared_page, shared_page.locator("esp-column-dimentional-grid").get_by_text("Scan Units (CW-3)"), 'click', "Click on the 'Scan Units (CW-3)' column header within the grid to interact with it.")
    # Click on the 'Daily Trend Customer:3RD' text element to interact with the trend analysis for this customer.
    safe_action(shared_page, shared_page.get_by_text("Daily Trend Customer:3RD"), 'click', "Click on the 'Daily Trend Customer:3RD' text element to interact with the trend analysis for this customer.")

@pytest.mark.order(49)
def test_chart_and_graphical_element_interaction(shared_page: Page):
    # Click on an SVG element, possibly to interact with a chart or graphical element.
    safe_action(shared_page, shared_page.locator("svg"), 'click', "Click on an SVG element, possibly to interact with a chart or graphical element.")
    # Click on the title element to interact with or navigate to a specific section.
    safe_action(shared_page, shared_page.locator(".title.d-flex.align-items-center.font-size-16.font-weight-bold.nunito.title-color > .p-l-40"), 'click', "Click on the title element to interact with or navigate to a specific section.")
    # Click on the 'Customer' label within the line-bar chart to filter or interact with customer-specific data.
    safe_action(shared_page, shared_page.locator("dp-line-bar-chart").get_by_text("Customer", exact=True), 'click', "Click on the 'Customer' label within the line-bar chart to filter or interact with customer-specific data.")
    # Click on the 'Customer:3RD PARTY DISTRIB' label within the line-bar chart to filter or interact with this specific customer data.
    safe_action(shared_page, shared_page.locator("dp-line-bar-chart").get_by_text("Customer:3RD PARTY DISTRIB"), 'click', "Click on the 'Customer:3RD PARTY DISTRIB' label within the line-bar chart to filter or interact with this specific customer data.")
    # Click on a specific path element within the chart, possibly to highlight or interact with a data point.
    safe_action(shared_page, shared_page.locator("path:nth-child(79)"), 'click', "Click on a specific path element within the chart, possibly to highlight or interact with a data point.")

@pytest.mark.order(50)
def test_user_suggested_and_override_interaction(shared_page: Page):
    # Click on the first occurrence of the 'User Suggested Order Base' text to interact with it.
    safe_action(shared_page, shared_page.get_by_text("User Suggested Order Base,").first, 'click', "Click on the first occurrence of the 'User Suggested Order Base' text to interact with it.")
    # Click on the 'User Suggested Order Base' text element to interact with it.
    safe_action(shared_page, shared_page.locator("span").filter(has_text="User Suggested Order Base"), 'click', "Click on the 'User Suggested Order Base' text element to interact with it.")
    # Click on the 'User Suggested Order Promotion' text element to interact with it.
    safe_action(shared_page, shared_page.locator("span").filter(has_text="User Suggested Order Promotion"), 'click', "Click on the 'User Suggested Order Promotion' text element to interact with it.")
    # Click on the 'User Override Base' text element to interact with it.
    safe_action(shared_page, shared_page.locator("span").filter(has_text="User Override Base"), 'click', "Click on the 'User Override Base' text element to interact with it.")
    # Click on the 'User Override Promotion' text element to interact with it.
    safe_action(shared_page, shared_page.locator("span").filter(has_text="User Override Promotion"), 'click', "Click on the 'User Override Promotion' text element to interact with it.")

@pytest.mark.order(51)
def test_line_bar_chart_interaction(shared_page: Page):
    # Click on the 'Gross Units (CW-3)' text element within the line-bar chart to interact with it.
    safe_action(shared_page, shared_page.locator("dp-line-bar-chart span").filter(has_text="Gross Units (CW-3)"), 'click', "Click on the 'Gross Units (CW-3)' text element within the line-bar chart to interact with it.")
    # Click on the 'Gross Units (CW-4)' text element within the line-bar chart to interact with it.
    safe_action(shared_page, shared_page.locator("dp-line-bar-chart").get_by_text("Gross Units (CW-4)"), 'click', "Click on the 'Gross Units (CW-4)' text element within the line-bar chart to interact with it.")
    # Click on the seventh div element within the overflow container to interact with it.
    safe_action(shared_page, shared_page.locator(".overflow-auto > div:nth-child(7)"), 'click', "Click on the seventh div element within the overflow container to interact with it.")
    # Click on the eighth div element with a flex layout to interact with it.
    safe_action(shared_page, shared_page.locator("div:nth-child(8) > .d-flex"), 'click', "Click on the eighth div element with a flex layout to interact with it.")
    # Click on the ninth div element within the overflow container to interact with it.
    safe_action(shared_page, shared_page.locator(".overflow-auto > div:nth-child(9)"), 'click', "Click on the ninth div element within the overflow container to interact with it.")
    # Click on the tenth div element with a flex layout to interact with it.
    safe_action(shared_page, shared_page.locator("div:nth-child(10) > .d-flex"), 'click', "Click on the tenth div element with a flex layout to interact with it.")
    # Click on the 'Aged Net Units (CW-5)' text element within the line-bar chart to interact with it.
    safe_action(shared_page, shared_page.locator("dp-line-bar-chart").get_by_text("Aged Net Units (CW-5)"), 'click', "Click on the 'Aged Net Units (CW-5)' text element within the line-bar chart to interact with it.")
    # Click on the 'Aged Net Units (CW-6)' text element within the line-bar chart to interact with it.
    safe_action(shared_page, shared_page.locator("dp-line-bar-chart").get_by_text("Aged Net Units (CW-6)"), 'click', "Click on the 'Aged Net Units (CW-6)' text element within the line-bar chart to interact with it.")
    # Click on the 'Scan Units (CW-3)' text element within the line-bar chart to interact with it.
    safe_action(shared_page, shared_page.locator("dp-line-bar-chart span").filter(has_text="Scan Units (CW-3)"), 'click', "Click on the 'Scan Units (CW-3)' text element within the line-bar chart to interact with it.")
    # Click on the 'Scan Units (CW-4)' text element within the line-bar chart to interact with it.
    safe_action(shared_page, shared_page.locator("dp-line-bar-chart").get_by_text("Scan Units (CW-4)"), 'click', "Click on the 'Scan Units (CW-4)' text element within the line-bar chart to interact with it.")
    # Click on the fifteenth div element within the overflow container to interact with it.
    safe_action(shared_page, shared_page.locator(".overflow-auto > div:nth-child(15)"), 'click', "Click on the fifteenth div element within the overflow container to interact with it.")
    # Click on the 'Scan Units (CW-6)' text element within the line-bar chart to interact with it.
    safe_action(shared_page, shared_page.locator("dp-line-bar-chart").get_by_text("Scan Units (CW-6)"), 'click', "Click on the 'Scan Units (CW-6)' text element within the line-bar chart to interact with it.")

@pytest.mark.order(52)
def test_dropdown_interaction(shared_page: Page):
    # Click on the dropdown element within the ellipses container to interact with the multiselect options.
    safe_action(shared_page, shared_page.locator(".ellipses > esp-multiselect-dropdown > .multiselect-dropdown > div > .w-100"), 'click', "Click on the dropdown element within the ellipses container to interact with the multiselect options.")

@pytest.mark.order(53)
def test_customer_trend_interaction(shared_page: Page):
    # Click on the 'Daily Trend Customer:3RD' text element to interact with the trend analysis for this customer.
    safe_action(shared_page, shared_page.get_by_text("Daily Trend Customer:3RD"), 'click', "Click on the 'Daily Trend Customer:3RD' text element to interact with the trend analysis for this customer.")

@pytest.mark.order(54)
def test_preference_management(shared_page: Page):
    # Click on the preference icon within the grid icons container to open the preferences dropdown.
    safe_action(shared_page, shared_page.locator(".title.d-flex.align-items-center.font-size-16.font-weight-bold.nunito.title-color > .grid-icons-container > esp-grid-icons-component > .display-grid-icons > div > #preference-iconId > .legend-font > .multiselect-dropdown > .pointer"), 'click', "Click on the preference icon within the grid icons container to open the preferences dropdown.")
    # Click on the 'Save Preference' option to save the current preferences.
    safe_action(shared_page, shared_page.get_by_text("Save Preference"), 'click', "Click on the 'Save Preference' option to save the current preferences.")
    # Click on the preference icon again to open the preferences dropdown.
    safe_action(shared_page, shared_page.locator(".title.d-flex.align-items-center.font-size-16.font-weight-bold.nunito.title-color > .grid-icons-container > esp-grid-icons-component > .display-grid-icons > div > #preference-iconId > .legend-font > .multiselect-dropdown > .pointer"), 'click', "Click on the preference icon again to open the preferences dropdown.")
    # Click on the 'Reset Preference' option to reset the preferences to default.
    safe_action(shared_page, shared_page.get_by_text("Reset Preference"), 'click', "Click on the 'Reset Preference' option to reset the preferences to default.")

@pytest.mark.order(55)
def test_date_selection_in_svg(shared_page: Page):
    # Click on an SVG element, possibly to interact with a chart or graphical element.
    safe_action(shared_page, shared_page.locator("svg"), 'click', "Click on an SVG element, possibly to interact with a chart or graphical element.")
    # Click on the '02/01/' text within the SVG element, likely to select a specific date.
    safe_action(shared_page, shared_page.locator("svg").get_by_text("02/01/"), 'click', "Click on the '02/01/' text within the SVG element, likely to select a specific date.")
    # Click on the '02/02/' text to select another specific date.
    safe_action(shared_page, shared_page.get_by_text("02/02/"), 'click', "Click on the '02/02/' text to select another specific date.")
    # Click on the '02/03/' text to select another specific date.
    safe_action(shared_page, shared_page.get_by_text("02/03/"), 'click', "Click on the '02/03/' text to select another specific date.")

@pytest.mark.order(56)
def test_svg_path_interaction(shared_page: Page):
    # Click on an SVG element, possibly to interact with a chart or graphical element again.
    safe_action(shared_page, shared_page.locator("svg"), 'click', "Click on an SVG element, possibly to interact with a chart or graphical element again.")
    # Click on the 67th path element within the SVG, possibly to interact with a specific data point.
    safe_action(shared_page, shared_page.locator("path:nth-child(67)"), 'click', "Click on the 67th path element within the SVG, possibly to interact with a specific data point.")
    # Click on the 'User Override Promotion' text element to interact with it.
    safe_action(shared_page, shared_page.get_by_text("User Override Promotion", exact=True), 'click', "Click on the 'User Override Promotion' text element to interact with it.")
    # Click on the 'User Override Base' text element to interact with it.
    safe_action(shared_page, shared_page.get_by_text("User Override Base", exact=True), 'click', "Click on the 'User Override Base' text element to interact with it.")
    # Click on the 79th path element within the SVG, possibly to interact with a specific data point.
    safe_action(shared_page, shared_page.locator("path:nth-child(79)"), 'click', "Click on the 79th path element within the SVG, possibly to interact with a specific data point.")
    # Click on the 96th path element within the SVG, possibly to interact with a specific data point.
    safe_action(shared_page, shared_page.locator("path:nth-child(96)"), 'click', "Click on the 96th path element within the SVG, possibly to interact with a specific data point.")
    # Click on the 102nd path element within the SVG, possibly to interact with a specific data point.
    safe_action(shared_page, shared_page.locator("path:nth-child(102)"), 'click', "Click on the 102nd path element within the SVG, possibly to interact with a specific data point.")
    # Click on an SVG element, possibly to interact with a chart or graphical element again.
    safe_action(shared_page, shared_page.locator("svg"), 'click', "Click on an SVG element, possibly to interact with a chart or graphical element again.")
    # Click on the 102nd path element within the SVG again, possibly to interact with the same data point.
    safe_action(shared_page, shared_page.locator("path:nth-child(102)"), 'click', "Click on the 102nd path element within the SVG again, possibly to interact with the same data point.")

