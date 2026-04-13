
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


@pytest.mark.order(2)
def test_browser_initialization_and_page_navigation(shared_page: Page):
    # Launch a Chromium browser instance in non-headless mode.
    # Create a new browser context to isolate session data.
    # Open a new page within the created browser context.
    # Navigate to the specified URL for the 'Executive Dashboard' in the demand planning application.
    safe_action(shared_page, shared_page, 'goto', "Navigate to the specified URL for the 'Executive Dashboard' in the demand planning application.", "https://stage.bbu.esp.antuit.ai/dp/demand-planning/executive-dashboard?workbookId=4&tabIndex=4")
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

@pytest.mark.order(3)
def test_customer_total_columns_configuration(shared_page: Page):
    # Click on the 'Customer Total columns (0)' text to open the configuration panel for customer total columns.
    safe_action(shared_page, shared_page.get_by_text("Customer Total columns (0)"), 'click', "Click on the 'Customer Total columns (0)' text to open the configuration panel for customer total columns.")
    # Click on the 'Customer Total' text to focus on the customer total section.
    safe_action(shared_page, shared_page.get_by_text("Customer Total"), 'click', "Click on the 'Customer Total' text to focus on the customer total section.")
    # Click on the button within the 'Customer Total columns (0)' card to open the column visibility settings.
    safe_action(shared_page, shared_page.locator("esp-card-component").filter(has_text="Customer Total columns (0)").get_by_role("button"), 'click', "Click on the button within the 'Customer Total columns (0)' card to open the column visibility settings.")

@pytest.mark.order(4)
def test_column_visibility_toggle(shared_page: Page):
    # Uncheck the 'Toggle All Columns Visibility' checkbox to hide all columns.
    safe_action(shared_page, shared_page.get_by_role("checkbox", name="Toggle All Columns Visibility"), 'uncheck', "Uncheck the 'Toggle All Columns Visibility' checkbox to hide all columns.")
    # Click on the 'Filter Columns Input' textbox to prepare for filtering specific columns.
    safe_action(shared_page, shared_page.get_by_role("textbox", name="Filter Columns Input"), 'click', "Click on the 'Filter Columns Input' textbox to prepare for filtering specific columns.")
    # Check the 'Toggle All Columns Visibility' checkbox to make all columns visible again.
    safe_action(shared_page, shared_page.get_by_role("checkbox", name="Toggle All Columns Visibility"), 'check', "Check the 'Toggle All Columns Visibility' checkbox to make all columns visible again.")

@pytest.mark.order(5)
def test_filter_columns_input_interaction(shared_page: Page):
    # Click on the 'Filter Columns Input' textbox to focus on it for input.
    safe_action(shared_page, shared_page.get_by_role("textbox", name="Filter Columns Input"), 'click', "Click on the 'Filter Columns Input' textbox to focus on it for input.")
    # Fill the 'Filter Columns Input' textbox with the text 'System Forecast' to filter columns by this keyword.
    safe_action(shared_page, shared_page.get_by_role("textbox", name="Filter Columns Input"), 'fill', "Fill the 'Filter Columns Input' textbox with the text 'System Forecast' to filter columns by this keyword.", "System Forecast")
    # Press 'Enter' in the 'Filter Columns Input' textbox to apply the filter.
    safe_action(shared_page, shared_page.get_by_role("textbox", name="Filter Columns Input"), 'press', "Press 'Enter' in the 'Filter Columns Input' textbox to apply the filter.", "Enter")

@pytest.mark.order(6)
def test_column_selection_and_visibility(shared_page: Page):
    # Click on the first column in the filtered list to select it.
    safe_action(shared_page, shared_page.locator(".ag-column-select-column").first, 'click', "Click on the first column in the filtered list to select it.")
    # Check the checkbox for the 'System Forecast Base (Plan)' column to make it visible.
    safe_action(shared_page, shared_page.get_by_role("treeitem", name="System Forecast Base (Plan").get_by_label("Press SPACE to toggle"), 'check', "Check the checkbox for the 'System Forecast Base (Plan)' column to make it visible.")

@pytest.mark.order(7)
def test_filter_reset(shared_page: Page):
    # Click on the 'Filter Columns Input' textbox to clear the filter.
    safe_action(shared_page, shared_page.get_by_role("textbox", name="Filter Columns Input"), 'click', "Click on the 'Filter Columns Input' textbox to clear the filter.")
    # Clear the 'Filter Columns Input' textbox to reset the filter.
    safe_action(shared_page, shared_page.get_by_role("textbox", name="Filter Columns Input"), 'fill', "Clear the 'Filter Columns Input' textbox to reset the filter.", "")
    # Press 'Enter' in the 'Filter Columns Input' textbox to confirm clearing the filter.
    safe_action(shared_page, shared_page.get_by_role("textbox", name="Filter Columns Input"), 'press', "Press 'Enter' in the 'Filter Columns Input' textbox to confirm clearing the filter.", "Enter")

@pytest.mark.order(8)
def test_system_forecast_column_selection(shared_page: Page):
    # Click on the 'System Forecast Total (Plan Week)' column to select it.
    safe_action(shared_page, shared_page.locator("#ag-839").get_by_text("System Forecast Total (Plan Week)"), 'click', "Click on the 'System Forecast Total (Plan Week)' column to select it.")
    # Click on the 'System Forecast Base (Plan)' column to select it.
    safe_action(shared_page, shared_page.get_by_label("System Forecast Base (Plan").get_by_text("System Forecast Base (Plan"), 'click', "Click on the 'System Forecast Base (Plan)' column to select it.")
    # Click on the 'System Forecast Promotion (' column to select it.
    safe_action(shared_page, shared_page.get_by_label("System Forecast Promotion (").get_by_text("System Forecast Promotion ("), 'click', "Click on the 'System Forecast Promotion (' column to select it.")
    # Click on the 'System Forecast Total (Plan+1)' column to select it.
    safe_action(shared_page, shared_page.get_by_label("System Forecast Total (Plan+1").get_by_text("System Forecast Total (Plan+1"), 'click', "Click on the 'System Forecast Total (Plan+1)' column to select it.")
    # Click on the 'System Forecast Base (Plan+1)' column to select it.
    safe_action(shared_page, shared_page.get_by_label("System Forecast Base (Plan+1").get_by_text("System Forecast Base (Plan+1"), 'click', "Click on the 'System Forecast Base (Plan+1)' column to select it.")
    # Click on the 'System Forecast Base (Plan+1)' column again to confirm selection.
    safe_action(shared_page, shared_page.get_by_label("System Forecast Base (Plan+1").get_by_text("System Forecast Base (Plan+1"), 'click', "Click on the 'System Forecast Base (Plan+1)' column again to confirm selection.")

@pytest.mark.order(9)
def test_additional_column_selection(shared_page: Page):
    # Click on the 'LY 6 Week Aged Net Units' column to select it.
    safe_action(shared_page, shared_page.get_by_label("LY 6 Week Aged Net Units").get_by_text("LY 6 Week Aged Net Units"), 'click', "Click on the 'LY 6 Week Aged Net Units' column to select it.")
    # Click on the '% Change 6 Week Aged Net' column to select it.
    safe_action(shared_page, shared_page.get_by_label("% Change 6 Week Aged Net").get_by_text("% Change 6 Week Aged Net"), 'click', "Click on the '% Change 6 Week Aged Net' column to select it.")
    # Click on the '6 Week Scan Units Average Column' to select it.
    safe_action(shared_page, shared_page.get_by_label("6 Week Scan Units Average Column", exact=True).get_by_text("Week Scan Units Average"), 'click', "Click on the '6 Week Scan Units Average Column' to select it.")

@pytest.mark.order(10)
def test_column_selection_and_visibility_toggle(shared_page: Page):
    # Click on the 'LY 6 Week Scan Units Average' column to select it.
    safe_action(shared_page, shared_page.get_by_label("LY 6 Week Scan Units Average").get_by_text("LY 6 Week Scan Units Average"), 'click', "Click on the 'LY 6 Week Scan Units Average' column to select it.")
    # Click on the '% Change 6 Week Scan Units' column to select it.
    safe_action(shared_page, shared_page.get_by_label("% Change 6 Week Scan Units").get_by_text("% Change 6 Week Scan Units"), 'click', "Click on the '% Change 6 Week Scan Units' column to select it.")
    # Click on the 'Freshness (6 Week Average)' column to select it.
    safe_action(shared_page, shared_page.get_by_label("Freshness (6 Week Average)").get_by_text("Freshness (6 Week Average)"), 'click', "Click on the 'Freshness (6 Week Average)' column to select it.")
    # Uncheck the checkbox to toggle visibility for a specific column.
    safe_action(shared_page, shared_page.get_by_role("checkbox", name="Press SPACE to toggle visibility (visible)"), 'uncheck', "Uncheck the checkbox to toggle visibility for a specific column.")
    # Check the 'Toggle All Columns Visibility' checkbox to make all columns visible again.
    safe_action(shared_page, shared_page.get_by_role("checkbox", name="Toggle All Columns Visibility"), 'check', "Check the 'Toggle All Columns Visibility' checkbox to make all columns visible again.")
    # Click on the button within the 'Customer Total columns (0)' card to close the column visibility settings.
    safe_action(shared_page, shared_page.locator("esp-card-component").filter(has_text="Customer Total columns (0)").get_by_role("button"), 'click', "Click on the button within the 'Customer Total columns (0)' card to close the column visibility settings.")

@pytest.mark.order(11)
def test_file_download_setup_and_execution(shared_page: Page):
    # Set up an expectation to handle a file download triggered by subsequent actions.
    with shared_page.expect_download() as download_info:
    # Click on the download button (identified by '.icon-color-toolbar-active.zeb-download-underline') to initiate the download process.
        safe_action(shared_page, shared_page.locator(".icon-color-toolbar-active.zeb-download-underline").first, 'click', "Click on the download button (identified by '.icon-color-toolbar-active.zeb-download-underline') to initiate the download process.")
    # Retrieve the download information after the download is triggered.
    download = download_info.value

@pytest.mark.order(12)
def test_preference_management(shared_page: Page):
    # Click on the adjustments button (identified by '.pointer.zeb-adjustments') to open the preferences menu.
    safe_action(shared_page, shared_page.locator(".pointer.zeb-adjustments").first, 'click', "Click on the adjustments button (identified by '.pointer.zeb-adjustments') to open the preferences menu.")
    # Click on the 'Save Preference' option to save the current settings.
    safe_action(shared_page, shared_page.locator("div").filter(has_text=re.compile(r"^Save Preference$")).first, 'click', "Click on the 'Save Preference' option to save the current settings.")
    # Click on the adjustments button again to reopen the preferences menu.
    safe_action(shared_page, shared_page.locator(".pointer.zeb-adjustments").first, 'click', "Click on the adjustments button again to reopen the preferences menu.")
    # Click on the 'Reset Preference' option to reset the settings to their default values.
    safe_action(shared_page, shared_page.get_by_text("Reset Preference"), 'click', "Click on the 'Reset Preference' option to reset the settings to their default values.")

@pytest.mark.order(13)
def test_customer_column_configuration(shared_page: Page):
    # Click on the horizontal scroll container to ensure the view is scrolled to the appropriate section.
    safe_action(shared_page, shared_page.locator(".ag-body-horizontal-scroll-container").first, 'click', "Click on the horizontal scroll container to ensure the view is scrolled to the appropriate section.")
    # Click on the 'Customers columns (0)' button to open the configuration panel for customer columns.
    safe_action(shared_page, shared_page.get_by_text("Customers columns (0)"), 'click', "Click on the 'Customers columns (0)' button to open the configuration panel for customer columns.")
    # Click on the 'Customers' section to expand and view its options.
    safe_action(shared_page, shared_page.get_by_text("Customers"), 'click', "Click on the 'Customers' section to expand and view its options.")
    # Click on the button within the 'Customers columns (0)' card to access column configuration options.
    safe_action(shared_page, shared_page.locator("esp-card-component").filter(has_text="Customers columns (0)").get_by_role("button"), 'click', "Click on the button within the 'Customers columns (0)' card to access column configuration options.")
    # Click on the 'Filter Columns Input' textbox to focus on it for entering a filter value.
    safe_action(shared_page, shared_page.get_by_role("textbox", name="Filter Columns Input"), 'click', "Click on the 'Filter Columns Input' textbox to focus on it for entering a filter value.")
    # Uncheck the 'Toggle All Columns Visibility' checkbox to hide all columns.
    safe_action(shared_page, shared_page.get_by_role("checkbox", name="Toggle All Columns Visibility"), 'uncheck', "Uncheck the 'Toggle All Columns Visibility' checkbox to hide all columns.")
    # Check the 'Toggle All Columns Visibility' checkbox to make all columns visible again.
    safe_action(shared_page, shared_page.get_by_role("checkbox", name="Toggle All Columns Visibility"), 'check', "Check the 'Toggle All Columns Visibility' checkbox to make all columns visible again.")

@pytest.mark.order(14)
def test_column_filtering_and_visibility_adjustment(shared_page: Page):
    # Click on the 'Filter Columns Input' textbox to focus on it for entering a filter value.
    safe_action(shared_page, shared_page.get_by_role("textbox", name="Filter Columns Input"), 'click', "Click on the 'Filter Columns Input' textbox to focus on it for entering a filter value.")
    # Enter the value '6' into the 'Filter Columns Input' textbox to filter columns containing '6'.
    safe_action(shared_page, shared_page.get_by_role("textbox", name="Filter Columns Input"), 'fill', "Enter the value '6' into the 'Filter Columns Input' textbox to filter columns containing '6'.", "6")
    # Press 'Enter' in the 'Filter Columns Input' textbox to apply the filter.
    safe_action(shared_page, shared_page.get_by_role("textbox", name="Filter Columns Input"), 'press', "Press 'Enter' in the 'Filter Columns Input' textbox to apply the filter.", "Enter")
    # Check the checkbox to make the 'Week Gross Units Average Column' visible.
    safe_action(shared_page, shared_page.get_by_role("treeitem", name="Week Gross Units Average Column").get_by_label("Press SPACE to toggle visibility (hidden)"), 'check', "Check the checkbox to make the 'Week Gross Units Average Column' visible.")
    # Check the checkbox to make the '6 Week Aged Net Units Average Column' visible.
    safe_action(shared_page, shared_page.get_by_role("treeitem", name="6 Week Aged Net Units Average Column", exact=True).get_by_label("Press SPACE to toggle visibility (hidden)"), 'check', "Check the checkbox to make the '6 Week Aged Net Units Average Column' visible.")
    # Check the checkbox to make the 'LY 6 Week Aged Net Units' column visible.
    safe_action(shared_page, shared_page.get_by_role("treeitem", name="LY 6 Week Aged Net Units").get_by_label("Press SPACE to toggle visibility (hidden)"), 'check', "Check the checkbox to make the 'LY 6 Week Aged Net Units' column visible.")
    # Check the checkbox to make the '% Change 6 Week Aged Net' column visible.
    safe_action(shared_page, shared_page.get_by_role("treeitem", name="% Change 6 Week Aged Net").get_by_label("Press SPACE to toggle visibility (hidden)"), 'check', "Check the checkbox to make the '% Change 6 Week Aged Net' column visible.")

@pytest.mark.order(15)
def test_column_list_selection(shared_page: Page):
    # Click on the '6 Week Scan Units Average' column in the column list to select it.
    safe_action(shared_page, shared_page.get_by_label("Column List 9 Columns").get_by_text("6 Week Scan Units Average", exact=True), 'click', "Click on the '6 Week Scan Units Average' column in the column list to select it.")
    # Click on the 'LY 6 Week Scan Units Average' column in the column list to select it.
    safe_action(shared_page, shared_page.get_by_label("LY 6 Week Scan Units Average").get_by_text("LY 6 Week Scan Units Average"), 'click', "Click on the 'LY 6 Week Scan Units Average' column in the column list to select it.")
    # Click on the '% Change 6 Week Scan Units' column in the column list to select it.
    safe_action(shared_page, shared_page.get_by_label("% Change 6 Week Scan Units").get_by_text("% Change 6 Week Scan Units"), 'click', "Click on the '% Change 6 Week Scan Units' column in the column list to select it.")

@pytest.mark.order(16)
def test_column_selection_and_filter_clearing(shared_page: Page):
    # Click on the '6 Week Aged Returns Units' column in the column list to select it.
    safe_action(shared_page, shared_page.get_by_label("6 Week Aged Returns Units").get_by_text("6 Week Aged Returns Units"), 'click', "Click on the '6 Week Aged Returns Units' column in the column list to select it.")
    # Click on the 'Filter Columns Input' textbox to clear the filter.
    safe_action(shared_page, shared_page.get_by_role("textbox", name="Filter Columns Input"), 'click', "Click on the 'Filter Columns Input' textbox to clear the filter.")
    # Clear the 'Filter Columns Input' textbox to remove the filter.
    safe_action(shared_page, shared_page.get_by_role("textbox", name="Filter Columns Input"), 'fill', "Clear the 'Filter Columns Input' textbox to remove the filter.", "")
    # Press 'Enter' in the 'Filter Columns Input' textbox to confirm clearing the filter.
    safe_action(shared_page, shared_page.get_by_role("textbox", name="Filter Columns Input"), 'press', "Press 'Enter' in the 'Filter Columns Input' textbox to confirm clearing the filter.", "Enter")

@pytest.mark.order(17)
def test_sequential_column_selection(shared_page: Page):
    # Click on the first column in the column panel to select it.
    safe_action(shared_page, shared_page.locator("#ag-989 > .ag-column-panel > .ag-column-select > .ag-column-select-list > .ag-virtual-list-viewport > .ag-virtual-list-container > div > .ag-column-select-column").first, 'click', "Click on the first column in the column panel to select it.")
    # Click on the 'System Forecast Base (Plan Week)' column in the column list to select it.
    safe_action(shared_page, shared_page.get_by_label("System Forecast Base (Plan Week) Column").get_by_text("System Forecast Base (Plan"), 'click', "Click on the 'System Forecast Base (Plan Week)' column in the column list to select it.")
    # Click on the 'System Forecast Promotion (Plan Week)' column in the column list to select it.
    safe_action(shared_page, shared_page.get_by_label("System Forecast Promotion (Plan Week) Column").get_by_text("System Forecast Promotion ("), 'click', "Click on the 'System Forecast Promotion (Plan Week)' column in the column list to select it.")
    # Click on the 'System Forecast Total (Plan+1)' column in the column list to select it.
    safe_action(shared_page, shared_page.get_by_label("System Forecast Total (Plan+1").get_by_text("System Forecast Total (Plan+1"), 'click', "Click on the 'System Forecast Total (Plan+1)' column in the column list to select it.")
    # Click on the 'System Forecast Base (Plan+1)' column in the column list to select it.
    safe_action(shared_page, shared_page.get_by_label("System Forecast Base (Plan+1").get_by_text("System Forecast Base (Plan+1"), 'click', "Click on the 'System Forecast Base (Plan+1)' column in the column list to select it.")
    # Click on the 'System Forecast Promotion (Plan+1 Week)' column in the column list to select it.
    safe_action(shared_page, shared_page.get_by_label("System Forecast Promotion (Plan+1 Week) Column").get_by_text("System Forecast Promotion ("), 'click', "Click on the 'System Forecast Promotion (Plan+1 Week)' column in the column list to select it.")
    # Click on the '6 Week Gross Units Average' column in the column list to select it.
    safe_action(shared_page, shared_page.get_by_label("6 Week Gross Units Average").get_by_text("Week Gross Units Average"), 'click', "Click on the '6 Week Gross Units Average' column in the column list to select it.")
    # Click on the '6 Week Aged Net Units Average Column' in the column list to select it.
    safe_action(shared_page, shared_page.get_by_label("6 Week Aged Net Units Average Column", exact=True).get_by_text("6 Week Aged Net Units Average", exact=True), 'click', "Click on the '6 Week Aged Net Units Average Column' in the column list to select it.")
    # Click on the 'LY 6 Week Aged Net Units' column in the column list to select it.
    safe_action(shared_page, shared_page.get_by_label("LY 6 Week Aged Net Units").get_by_text("LY 6 Week Aged Net Units"), 'click', "Click on the 'LY 6 Week Aged Net Units' column in the column list to select it.")
    # Click on the '% Change 6 Week Aged Net' column in the column list to select it.
    safe_action(shared_page, shared_page.get_by_label("% Change 6 Week Aged Net").get_by_text("% Change 6 Week Aged Net"), 'click', "Click on the '% Change 6 Week Aged Net' column in the column list to select it.")
    # Click on the '6 Week Scan Units Average Column' in the column list to select it.
    safe_action(shared_page, shared_page.get_by_label("6 Week Scan Units Average Column", exact=True).get_by_text("6 Week Scan Units Average", exact=True), 'click', "Click on the '6 Week Scan Units Average Column' in the column list to select it.")
    # Click on the 'LY 6 Week Scan Units Average' column in the column list to select it.
    safe_action(shared_page, shared_page.get_by_label("LY 6 Week Scan Units Average").get_by_text("LY 6 Week Scan Units Average"), 'click', "Click on the 'LY 6 Week Scan Units Average' column in the column list to select it.")
    # Click on the '% Change 6 Week Scan Units' column in the column list to select it.
    safe_action(shared_page, shared_page.get_by_label("% Change 6 Week Scan Units").get_by_text("% Change 6 Week Scan Units"), 'click', "Click on the '% Change 6 Week Scan Units' column in the column list to select it.")
    # Click on the 'Freshness (6 Week Average)' column in the column list to select it.
    safe_action(shared_page, shared_page.get_by_label("Freshness (6 Week Average)").get_by_text("Freshness (6 Week Average)"), 'click', "Click on the 'Freshness (6 Week Average)' column in the column list to select it.")
    # Click on the '6 Week Aged Returns Units' column in the column list to select it.
    safe_action(shared_page, shared_page.get_by_label("6 Week Aged Returns Units").get_by_text("6 Week Aged Returns Units"), 'click', "Click on the '6 Week Aged Returns Units' column in the column list to select it.")

@pytest.mark.order(18)
def test_toggle_column_visibility(shared_page: Page):
    # Check the 'Toggle All Columns Visibility' checkbox to make all columns visible.
    safe_action(shared_page, shared_page.get_by_role("checkbox", name="Toggle All Columns Visibility"), 'check', "Check the 'Toggle All Columns Visibility' checkbox to make all columns visible.")

@pytest.mark.order(19)
def test_file_export_handling(shared_page: Page):
    # Set up an expectation to handle a file download triggered by subsequent actions.
    with shared_page.expect_download() as download1_info:
    # Click on the 'Export' icon within the 'esp-grid-icons-component' to initiate the export process.
        safe_action(shared_page, shared_page.locator("esp-grid-icons-component").filter(has_text="Export").locator("#export-iconId"), 'click', "Click on the 'Export' icon within the 'esp-grid-icons-component' to initiate the export process.")
    # Capture the downloaded file information after the export action is triggered.
    download1 = download1_info.value

@pytest.mark.order(20)
def test_preference_reset(shared_page: Page):
    # Click on the 'Preference' icon within the 'Customers columns (0)' card to open the preferences menu.
    safe_action(shared_page, shared_page.locator("esp-card-component").filter(has_text="Customers columns (0)").locator("#preference-iconId"), 'click', "Click on the 'Preference' icon within the 'Customers columns (0)' card to open the preferences menu.")
    # Click on the 'Reset Preference' option to reset the preferences to their default state.
    safe_action(shared_page, shared_page.locator("div").filter(has_text=re.compile(r"^Reset Preference$")).first, 'click', "Click on the 'Reset Preference' option to reset the preferences to their default state.")

@pytest.mark.order(21)
def test_sorting_actions(shared_page: Page):
    # Click on the header cell to initiate sorting or selection actions.
    safe_action(shared_page, shared_page.locator(".ag-header-cell.ag-column-first > .ag-header-cell-comp-wrapper > .ag-cell-label-container > .ag-header-cell-label"), 'click', "Click on the header cell to initiate sorting or selection actions.")
    # Click on the descending sort icon to sort the column in descending order.
    safe_action(shared_page, shared_page.locator(".ag-icon.ag-icon-desc").first, 'click', "Click on the descending sort icon to sort the column in descending order.")
    # Click on the ascending sort icon to sort the column in ascending order.
    safe_action(shared_page, shared_page.locator(".ag-icon.ag-icon-asc").first, 'click', "Click on the ascending sort icon to sort the column in ascending order.")

@pytest.mark.order(22)
def test_group_and_column_selection(shared_page: Page):
    # Select the '3RD PARTY DISTRIB' column by clicking on its text.
    safe_action(shared_page, shared_page.get_by_text("3RD PARTY DISTRIB"), 'click', "Select the '3RD PARTY DISTRIB' column by clicking on its text.")
    # Click on the first group checkbox to select or deselect a group of columns.
    safe_action(shared_page, shared_page.locator(".ag-group-checkbox").first, 'click', "Click on the first group checkbox to select or deselect a group of columns.")

@pytest.mark.order(23)
def test_context_menu_and_column_selection(shared_page: Page):
    # Right-click on the '3RD PARTY DISTRIB' column within the 'esp-row-dimentional-grid' to open a context menu or perform a specific action.
    safe_action(shared_page, shared_page.locator("esp-row-dimentional-grid span").filter(has_text=re.compile(r"^3RD PARTY DISTRIB$")), 'click', "Right-click on the '3RD PARTY DISTRIB' column within the 'esp-row-dimentional-grid' to open a context menu or perform a specific action.", button="right")
    # Click on the '3RD PARTY DISTRIB' column within the 'esp-row-dimentional-grid' to select it or perform an action.
    safe_action(shared_page, shared_page.locator("esp-row-dimentional-grid").get_by_text("3RD PARTY DISTRIB"), 'click', "Click on the '3RD PARTY DISTRIB' column within the 'esp-row-dimentional-grid' to select it or perform an action.")

@pytest.mark.order(24)
def test_filter_options_interaction(shared_page: Page):
    # Click on the filter button in the header to open the filter options.
    safe_action(shared_page, shared_page.locator(".ag-header-icon.ag-header-cell-filter-button > .ag-icon").first, 'click', "Click on the filter button in the header to open the filter options.")
    # Click on the filter body wrapper to interact with the filter options.
    safe_action(shared_page, shared_page.locator(".ag-filter-body-wrapper"), 'click', "Click on the filter body wrapper to interact with the filter options.")
    # Select the 'Contains' filter option from the dropdown.
    safe_action(shared_page, shared_page.get_by_text("Contains"), 'click', "Select the 'Contains' filter option from the dropdown.")
    # Click on the 'Contains' option to confirm selection.
    safe_action(shared_page, shared_page.get_by_role("option", name="Contains"), 'click', "Click on the 'Contains' option to confirm selection.")
    safe_action(shared_page, shared_page.get_by_text("Contains"), 'click', "Perform click on page.get_by_text(\"Contains\")")
    # Select the 'Does not contain' filter option from the dropdown.
    safe_action(shared_page, shared_page.get_by_text("Does not contain"), 'click', "Select the 'Does not contain' filter option from the dropdown.")
    safe_action(shared_page, shared_page.get_by_text("Does not contain"), 'click', "Perform click on page.get_by_text(\"Does not contain\")")
    # Select the 'Equals' filter option from the dropdown.
    safe_action(shared_page, shared_page.get_by_role("option", name="Equals"), 'click', "Select the 'Equals' filter option from the dropdown.")
    safe_action(shared_page, shared_page.get_by_text("Equals"), 'click', "Perform click on page.get_by_text(\"Equals\")")
    # Select the 'Does not equal' filter option from the dropdown.
    safe_action(shared_page, shared_page.get_by_role("option", name="Does not equal"), 'click', "Select the 'Does not equal' filter option from the dropdown.")
    safe_action(shared_page, shared_page.get_by_text("Does not equal"), 'click', "Perform click on page.get_by_text(\"Does not equal\")")
    # Select the 'Begins with' filter option from the dropdown.
    safe_action(shared_page, shared_page.get_by_role("option", name="Begins with"), 'click', "Select the 'Begins with' filter option from the dropdown.")
    safe_action(shared_page, shared_page.get_by_text("Begins with"), 'click', "Perform click on page.get_by_text(\"Begins with\")")
    # Select the 'Ends with' filter option from the dropdown.
    safe_action(shared_page, shared_page.get_by_role("option", name="Ends with"), 'click', "Select the 'Ends with' filter option from the dropdown.")
    safe_action(shared_page, shared_page.get_by_text("Ends with"), 'click', "Perform click on page.get_by_text(\"Ends with\")")
    # Select the 'Blank' filter option from the dropdown.
    safe_action(shared_page, shared_page.get_by_role("option", name="Blank", exact=True), 'click', "Select the 'Blank' filter option from the dropdown.")
    # Click on the 'AND' operator to set the filter condition.
    safe_action(shared_page, shared_page.get_by_text("AND", exact=True), 'click', "Click on the 'AND' operator to set the filter condition.")
    # Click on the 'OR' radio button to change the filter condition operator.
    safe_action(shared_page, shared_page.locator(".ag-labeled.ag-label-align-right.ag-radio-button.ag-input-field.ag-filter-condition-operator.ag-filter-condition-operator-or"), 'click', "Click on the 'OR' radio button to change the filter condition operator.")
    # Click on the 'Clear' button to clear all filter settings.
    safe_action(shared_page, shared_page.get_by_role("button", name="Clear"), 'click', "Click on the 'Clear' button to clear all filter settings.")
    # Click on the 'Reset' button to reset the filter settings to default.
    safe_action(shared_page, shared_page.get_by_role("button", name="Reset"), 'click', "Click on the 'Reset' button to reset the filter settings to default.")
    # Click on the filter button in the header again to close the filter options.
    safe_action(shared_page, shared_page.locator(".ag-header-icon.ag-header-cell-filter-button > .ag-icon").first, 'click', "Click on the filter button in the header again to close the filter options.")

@pytest.mark.order(25)
def test_filter_application_and_system_forecast_interaction(shared_page: Page):
    # Click on the 'Apply' button to apply the selected filter settings.
    safe_action(shared_page, shared_page.get_by_role("button", name="Apply"), 'click', "Click on the 'Apply' button to apply the selected filter settings.")
    # Click on the 'System Forecast Total (Plan' text to interact with the corresponding element.
    safe_action(shared_page, shared_page.get_by_text("System Forecast Total (Plan").nth(1), 'click', "Click on the 'System Forecast Total (Plan' text to interact with the corresponding element.")
    safe_action(shared_page, shared_page.get_by_text("System Forecast Total (Plan").nth(1), 'click', "Perform click on page.get_by_text(\"System Forecast Total (Plan\").nth(1)")
    safe_action(shared_page, shared_page.get_by_text("System Forecast Total (Plan").nth(1), 'click', "Perform click on page.get_by_text(\"System Forecast Total (Plan\").nth(1)")

@pytest.mark.order(26)
def test_additional_filter_options_interaction(shared_page: Page):
    # Click on the header icon to open the filter options for a specific column.
    safe_action(shared_page, shared_page.locator(".ag-header-cell.ag-header-parent-hidden.ag-header-cell-sortable.ag-header-background.ag-focus-managed.ag-header-active > .ag-header-cell-comp-wrapper > .ag-cell-label-container > .ag-header-icon > .ag-icon"), 'click', "Click on the header icon to open the filter options for a specific column.")
    # Click on the filter body wrapper to interact with the filter options again.
    safe_action(shared_page, shared_page.locator(".ag-filter-body-wrapper"), 'click', "Click on the filter body wrapper to interact with the filter options again.")
    # Select the 'Equals' filter option from the dropdown.
    safe_action(shared_page, shared_page.get_by_text("Equals"), 'click', "Select the 'Equals' filter option from the dropdown.")
    safe_action(shared_page, shared_page.get_by_role("option", name="Equals"), 'click', "Perform click on page.get_by_role(\"option\", name=\"Equals\")")
    safe_action(shared_page, shared_page.get_by_text("Equals"), 'click', "Perform click on page.get_by_text(\"Equals\")")
    # Select the 'Does not equal' filter option from the dropdown.
    safe_action(shared_page, shared_page.get_by_role("option", name="Does not equal"), 'click', "Select the 'Does not equal' filter option from the dropdown.")
    safe_action(shared_page, shared_page.get_by_text("Does not equal"), 'click', "Perform click on page.get_by_text(\"Does not equal\")")
    # Select the 'Greater than' filter option from the dropdown.
    safe_action(shared_page, shared_page.get_by_role("option", name="Greater than", exact=True), 'click', "Select the 'Greater than' filter option from the dropdown.")
    safe_action(shared_page, shared_page.get_by_text("Greater than"), 'click', "Perform click on page.get_by_text(\"Greater than\")")

@pytest.mark.order(27)
def test_filter_selection_and_operator_configuration(shared_page: Page):
    # Select the 'Less than' filter option from the dropdown.
    safe_action(shared_page, shared_page.get_by_role("option", name="Less than", exact=True), 'click', "Select the 'Less than' filter option from the dropdown.")
    # Click on the filtering operator combobox to open the operator options.
    safe_action(shared_page, shared_page.get_by_role("combobox", name="Filtering operator"), 'click', "Click on the filtering operator combobox to open the operator options.")
    # Select the 'Less than or equal to' filter option from the dropdown.
    safe_action(shared_page, shared_page.get_by_text("Less than or equal to"), 'click', "Select the 'Less than or equal to' filter option from the dropdown.")
    safe_action(shared_page, shared_page.get_by_text("Less than or equal to"), 'click', "Perform click on page.get_by_text(\"Less than or equal to\")")
    # Select the 'Between' filter option from the dropdown.
    safe_action(shared_page, shared_page.get_by_role("option", name="Between"), 'click', "Select the 'Between' filter option from the dropdown.")
    safe_action(shared_page, shared_page.get_by_text("Between"), 'click', "Perform click on page.get_by_text(\"Between\")")
    # Select the 'Blank' filter option from the dropdown again.
    safe_action(shared_page, shared_page.get_by_role("option", name="Blank", exact=True), 'click', "Select the 'Blank' filter option from the dropdown again.")
    # Click on the 'AND' operator to set the filter condition again.
    safe_action(shared_page, shared_page.get_by_text("AND", exact=True), 'click', "Click on the 'AND' operator to set the filter condition again.")
    # Click on the 'OR' operator to change the filter condition operator again.
    safe_action(shared_page, shared_page.get_by_text("OR", exact=True), 'click', "Click on the 'OR' operator to change the filter condition operator again.")
    # Click on the 'Clear' button to clear all filter settings again.
    safe_action(shared_page, shared_page.get_by_role("button", name="Clear"), 'click', "Click on the 'Clear' button to clear all filter settings again.")
    # Click on the 'Reset' button to reset the filter settings to default again.
    safe_action(shared_page, shared_page.get_by_role("button", name="Reset"), 'click', "Click on the 'Reset' button to reset the filter settings to default again.")
    # Click on the header icon to close the filter options for the specific column.
    safe_action(shared_page, shared_page.locator(".ag-header-cell.ag-header-parent-hidden.ag-header-cell-sortable.ag-header-background.ag-focus-managed.ag-header-active > .ag-header-cell-comp-wrapper > .ag-cell-label-container > .ag-header-icon > .ag-icon"), 'click', "Click on the header icon to close the filter options for the specific column.")
    # Click on the 'Apply' button to apply the selected filter settings again.
    safe_action(shared_page, shared_page.get_by_role("button", name="Apply"), 'click', "Click on the 'Apply' button to apply the selected filter settings again.")

@pytest.mark.order(28)
def test_pagination_interaction_and_row_display_settings(shared_page: Page):
    # Click on the pagination element to interact with the pagination controls.
    safe_action(shared_page, shared_page.locator("esp-row-dimentional-grid #paginationId"), 'click', "Click on the pagination element to interact with the pagination controls.")
    # Click on the text displaying the current row count to open the row display options.
    safe_action(shared_page, shared_page.get_by_text("Showing 10 out of"), 'click', "Click on the text displaying the current row count to open the row display options.")
    # Click on the 'Rows per page' text to interact with the row display dropdown.
    safe_action(shared_page, shared_page.get_by_text("Rows per page"), 'click', "Click on the 'Rows per page' text to interact with the row display dropdown.")
    # Select the option to view 10 rows per page from the dropdown.
    safe_action(shared_page, shared_page.get_by_text("View 10 row(s)").first, 'click', "Select the option to view 10 rows per page from the dropdown.")
    # Select the option to view 20 rows per page from the dropdown.
    safe_action(shared_page, shared_page.get_by_text("View 20 row(s)"), 'click', "Select the option to view 20 rows per page from the dropdown.")
    # Click on the dropdown caret to expand additional options.
    safe_action(shared_page, shared_page.locator(".dropdown-caret.p-l-16").first, 'click', "Click on the dropdown caret to expand additional options.")
    # Click on the text displaying the updated row count and options to confirm the selection.
    safe_action(shared_page, shared_page.get_by_text("Showing 20 out of 138 1234567Rows per page View 20 row(s) View 10 row(s)View 20"), 'click', "Click on the text displaying the updated row count and options to confirm the selection.")
    # Click on the 'Next' button in the pagination controls to navigate to the next page.
    safe_action(shared_page, shared_page.locator(".pagination-next"), 'click', "Click on the 'Next' button in the pagination controls to navigate to the next page.")
    # Click on the specific page number '1234567' to navigate to that page.
    safe_action(shared_page, shared_page.get_by_text("1234567"), 'click', "Click on the specific page number '1234567' to navigate to that page.")
    # Click on the 'Last' button in the pagination controls to navigate to the last page.
    safe_action(shared_page, shared_page.locator(".zeb-nav-to-last"), 'click', "Click on the 'Last' button in the pagination controls to navigate to the last page.")

@pytest.mark.order(29)
def test_advanced_navigation_and_filter_interaction(shared_page: Page):
    # Click on the fifth list item that matches an empty text filter.
    safe_action(shared_page, shared_page.get_by_role("listitem").filter(has_text=re.compile(r"^$")).nth(5), 'click', "Click on the fifth list item that matches an empty text filter.")
    # Click on the 'Navigate to First' button to go to the first page.
    safe_action(shared_page, shared_page.locator(".zeb-nav-to-first"), 'click', "Click on the 'Navigate to First' button to go to the first page.")
    # Click on the text 'FilterTime Latest 13 Next' to interact with the filter options.
    safe_action(shared_page, shared_page.get_by_text("FilterTime Latest 13 Next"), 'click', "Click on the text 'FilterTime Latest 13 Next' to interact with the filter options.")
    # Click on the 'Filter' text within a div element to open filter settings.
    safe_action(shared_page, shared_page.locator("div").filter(has_text=re.compile(r"^Filter$")), 'click', "Click on the 'Filter' text within a div element to open filter settings.")
    # Click on the 'Filter' text to select the filter option.
    safe_action(shared_page, shared_page.get_by_text("Filter"), 'click', "Click on the 'Filter' text to select the filter option.")
    # Click on the 'Time' text to adjust time-related filters.
    safe_action(shared_page, shared_page.get_by_text("Time"), 'click', "Click on the 'Time' text to adjust time-related filters.")
    # Click on the first occurrence of 'Latest 13 Next' to select this time filter.
    safe_action(shared_page, shared_page.get_by_text("Latest 13 Next").first, 'click', "Click on the first occurrence of 'Latest 13 Next' to select this time filter.")
    # Click on the 'Latest 5 Next 4' text to select this specific time filter.
    safe_action(shared_page, shared_page.get_by_text("Latest 5 Next 4"), 'click', "Click on the 'Latest 5 Next 4' text to select this specific time filter.")

@pytest.mark.order(30)
def test_dropdown_interaction_and_filter_selection(shared_page: Page):
    # Click on the dropdown labeled '.w-100.p-h-16.p-v-8.dropdown-label.background-white' to expand options.
    safe_action(shared_page, shared_page.locator(".w-100.p-h-16.p-v-8.dropdown-label.background-white"), 'click', "Click on the dropdown labeled '.w-100.p-h-16.p-v-8.dropdown-label.background-white' to expand options.")
    # Click on the second occurrence of 'Latest 5 Next 12' within a div element to select this filter.
    safe_action(shared_page, shared_page.locator("div").filter(has_text=re.compile(r"^Latest 5 Next 12$")).nth(1), 'click', "Click on the second occurrence of 'Latest 5 Next 12' within a div element to select this filter.")
    # Click on the dropdown caret within the '.w-100.p-h-16.p-v-8.dropdown-label.background-white' element to expand additional options.
    safe_action(shared_page, shared_page.locator(".w-100.p-h-16.p-v-8.dropdown-label.background-white > .d-flex.align-items-center > .dropdown-caret"), 'click', "Click on the dropdown caret within the '.w-100.p-h-16.p-v-8.dropdown-label.background-white' element to expand additional options.")
    # Click on the second occurrence of 'Latest 13 Next 4' within a div element to select this filter.
    safe_action(shared_page, shared_page.locator("div").filter(has_text=re.compile(r"^Latest 13 Next 4$")).nth(1), 'click', "Click on the second occurrence of 'Latest 13 Next 4' within a div element to select this filter.")
    # Click on the dropdown caret within the '.w-100.p-h-16.p-v-8.dropdown-label.background-white' element to expand additional options again.
    safe_action(shared_page, shared_page.locator(".w-100.p-h-16.p-v-8.dropdown-label.background-white > .d-flex.align-items-center > .dropdown-caret"), 'click', "Click on the dropdown caret within the '.w-100.p-h-16.p-v-8.dropdown-label.background-white' element to expand additional options again.")
    # Click on the 'Latest 13 Next 12' text to select this specific filter.
    safe_action(shared_page, shared_page.get_by_text("Latest 13 Next 12"), 'click', "Click on the 'Latest 13 Next 12' text to select this specific filter.")
    # Click on the dropdown caret within the '.w-100.p-h-16.p-v-8.dropdown-label.background-white' element to expand additional options again.
    safe_action(shared_page, shared_page.locator(".w-100.p-h-16.p-v-8.dropdown-label.background-white > .d-flex.align-items-center > .dropdown-caret"), 'click', "Click on the dropdown caret within the '.w-100.p-h-16.p-v-8.dropdown-label.background-white' element to expand additional options again.")
    # Click on the second occurrence of 'Latest 26 Next 4' within a div element to select this filter.
    safe_action(shared_page, shared_page.locator("div").filter(has_text=re.compile(r"^Latest 26 Next 4$")).nth(1), 'click', "Click on the second occurrence of 'Latest 26 Next 4' within a div element to select this filter.")

@pytest.mark.order(31)
def test_weekly_summary_navigation(shared_page: Page):
    # Click on the 'Weekly Summary Customer:3RD' text to view the weekly summary for the specified customer.
    safe_action(shared_page, shared_page.get_by_text("Weekly Summary Customer:3RD"), 'click', "Click on the 'Weekly Summary Customer:3RD' text to view the weekly summary for the specified customer.")
    # Click on the 'Weekly Summary' text to navigate to the Weekly Summary section.
    safe_action(shared_page, shared_page.get_by_text("Weekly Summary"), 'click', "Click on the 'Weekly Summary' text to navigate to the Weekly Summary section.")

@pytest.mark.order(32)
def test_customer_selection(shared_page: Page):
    # Click on the first occurrence of 'Customer:3RD PARTY DISTRIB' to select this customer.
    safe_action(shared_page, shared_page.get_by_text("Customer:3RD PARTY DISTRIB").first, 'click', "Click on the first occurrence of 'Customer:3RD PARTY DISTRIB' to select this customer.")
    # Click on the third occurrence of the exact text 'Customer' to refine the selection.
    safe_action(shared_page, shared_page.get_by_text("Customer", exact=True).nth(2), 'click', "Click on the third occurrence of the exact text 'Customer' to refine the selection.")
    # Click on the second occurrence of '3RD PARTY DISTRIB' to finalize the customer selection.
    safe_action(shared_page, shared_page.get_by_text("3RD PARTY DISTRIB").nth(1), 'click', "Click on the second occurrence of '3RD PARTY DISTRIB' to finalize the customer selection.")

@pytest.mark.order(33)
def test_filter_options_interaction(shared_page: Page):
    # Click on the dropdown to open the filter options for selection.
    safe_action(shared_page, shared_page.locator(".wr-20.font-weight-normal > esp-multiselect-dropdown > .multiselect-dropdown > div > .w-100"), 'click', "Click on the dropdown to open the filter options for selection.")
    # Select the 'All' option from the dropdown (4th occurrence).
    safe_action(shared_page, shared_page.get_by_text("All").nth(4), 'click', "Select the 'All' option from the dropdown (4th occurrence).")
    # Re-select the 'All' option from the dropdown (4th occurrence) to confirm the selection.
    safe_action(shared_page, shared_page.get_by_text("All").nth(4), 'click', "Re-select the 'All' option from the dropdown (4th occurrence) to confirm the selection.")
    # Click on the first element in the list of filter options to apply the filter.
    safe_action(shared_page, shared_page.locator(".d-flex.flex-column.justify-content-center").first, 'click', "Click on the first element in the list of filter options to apply the filter.")
    # Re-click on the first element in the list of filter options to ensure the filter is applied.
    safe_action(shared_page, shared_page.locator(".d-flex.flex-column.justify-content-center").first, 'click', "Re-click on the first element in the list of filter options to ensure the filter is applied.")
    # Click on the first dropdown option to refine the filter selection.
    safe_action(shared_page, shared_page.locator(".d-flex.dropdown-option.align-items-center.p-v-5.p-l-32 > .d-flex").first, 'click', "Click on the first dropdown option to refine the filter selection.")
    # Click on the first checkbox to enable or select the corresponding filter option.
    safe_action(shared_page, shared_page.locator(".d-flex.flex-column.justify-content-center.font-size-10.align-items-center.checkbox-v2.m-r-10.zeb-check").first, 'click', "Click on the first checkbox to enable or select the corresponding filter option.")
    # Re-click on the first checkbox to confirm the selection or toggle the filter option.
    safe_action(shared_page, shared_page.locator(".d-flex.flex-column.justify-content-center.font-size-10.align-items-center.checkbox-v2.m-r-10.zeb-check").first, 'click', "Re-click on the first checkbox to confirm the selection or toggle the filter option.")

@pytest.mark.order(34)
def test_dropdown_option_selection(shared_page: Page):
    # Click on the 'User Override Total' option (2nd occurrence) to select it from the dropdown.
    safe_action(shared_page, shared_page.get_by_text("User Override Total").nth(1), 'click', "Click on the 'User Override Total' option (2nd occurrence) to select it from the dropdown.")
    # Click on the first selected dropdown option to confirm or refine the selection.
    safe_action(shared_page, shared_page.locator(".d-flex.dropdown-option.align-items-center.p-v-5.p-l-32.p-r-16.selected").first, 'click', "Click on the first selected dropdown option to confirm or refine the selection.")
    # Click on the 'User Override Promotion' option (2nd occurrence) to select it from the dropdown.
    safe_action(shared_page, shared_page.get_by_text("User Override Promotion").nth(1), 'click', "Click on the 'User Override Promotion' option (2nd occurrence) to select it from the dropdown.")
    # Click on the 'System Forecast Total' option (6th occurrence) to select it from the dropdown.
    safe_action(shared_page, shared_page.get_by_text("System Forecast Total").nth(5), 'click', "Click on the 'System Forecast Total' option (6th occurrence) to select it from the dropdown.")
    # Click on the 'System Forecast Base' option (4th occurrence) to select it from the dropdown.
    safe_action(shared_page, shared_page.get_by_text("System Forecast Base").nth(3), 'click', "Click on the 'System Forecast Base' option (4th occurrence) to select it from the dropdown.")
    # Click on the 'System Forecast Promotion' option (4th occurrence) to select it from the dropdown.
    safe_action(shared_page, shared_page.get_by_text("System Forecast Promotion").nth(3), 'click', "Click on the 'System Forecast Promotion' option (4th occurrence) to select it from the dropdown.")
    # Click on the first selected dropdown option again to confirm or refine the selection.
    safe_action(shared_page, shared_page.locator(".d-flex.dropdown-option.align-items-center.p-v-5.p-l-32.p-r-16.selected").first, 'click', "Click on the first selected dropdown option again to confirm or refine the selection.")
    # Re-click on the first selected dropdown option to ensure the selection is applied.
    safe_action(shared_page, shared_page.locator(".d-flex.dropdown-option.align-items-center.p-v-5.p-l-32.p-r-16.selected").first, 'click', "Re-click on the first selected dropdown option to ensure the selection is applied.")
    # Click on the 'Weekly Forecast Promotion' option (exact match) to select it from the dropdown.
    safe_action(shared_page, shared_page.get_by_text("Weekly Forecast Promotion", exact=True), 'click', "Click on the 'Weekly Forecast Promotion' option (exact match) to select it from the dropdown.")

@pytest.mark.order(35)
def test_dropdown_selection_actions_part_1(shared_page: Page):
    # Click on the 'Daily Suggested Order Total' option (2nd occurrence) to select it from the dropdown.
    safe_action(shared_page, shared_page.get_by_text("Daily Suggested Order Total").nth(1), 'click', "Click on the 'Daily Suggested Order Total' option (2nd occurrence) to select it from the dropdown.")
    # Click on the 'Daily Suggested Order Base' option (exact match) to select it from the dropdown.
    safe_action(shared_page, shared_page.get_by_text("Daily Suggested Order Base", exact=True), 'click', "Click on the 'Daily Suggested Order Base' option (exact match) to select it from the dropdown.")
    # Click on the 18th child element within the '.overflow-auto > div' container to select a specific option.
    safe_action(shared_page, shared_page.locator(".overflow-auto > div:nth-child(18)"), 'click', "Click on the 18th child element within the '.overflow-auto > div' container to select a specific option.")
    # Click on the 'Gross Units' option (3rd occurrence) to select it from the dropdown.
    safe_action(shared_page, shared_page.get_by_text("Gross Units").nth(2), 'click', "Click on the 'Gross Units' option (3rd occurrence) to select it from the dropdown.")
    # Click on the 'Raw Forecast' option (2nd occurrence) to select it from the dropdown.
    safe_action(shared_page, shared_page.get_by_text("Raw Forecast").nth(1), 'click', "Click on the 'Raw Forecast' option (2nd occurrence) to select it from the dropdown.")
    # Click on the 'Daily Suggested Order Promotion' option (exact match) to select it from the dropdown.
    safe_action(shared_page, shared_page.get_by_text("Daily Suggested Order Promotion", exact=True), 'click', "Click on the 'Daily Suggested Order Promotion' option (exact match) to select it from the dropdown.")
    # Click on the '% Change Aged Net Units' option (exact match) to select it from the dropdown.
    safe_action(shared_page, shared_page.get_by_text("% Change Aged Net Units", exact=True), 'click', "Click on the '% Change Aged Net Units' option (exact match) to select it from the dropdown.")
    # Click on the 'Aged Net Units LY' option (exact match) to select it from the dropdown.
    safe_action(shared_page, shared_page.get_by_text("Aged Net Units LY", exact=True), 'click', "Click on the 'Aged Net Units LY' option (exact match) to select it from the dropdown.")
    # Click on the first selected dropdown option to confirm or refine the selection.
    safe_action(shared_page, shared_page.locator(".d-flex.dropdown-option.align-items-center.p-v-5.p-l-32.p-r-16.selected").first, 'click', "Click on the first selected dropdown option to confirm or refine the selection.")
    # Click on the 'Scan Units LY' option (exact match) to select it from the dropdown.
    safe_action(shared_page, shared_page.get_by_text("Scan Units LY", exact=True), 'click', "Click on the 'Scan Units LY' option (exact match) to select it from the dropdown.")
    # Re-click on the 'Scan Units LY' option (exact match) to ensure the selection is applied.
    safe_action(shared_page, shared_page.get_by_text("Scan Units LY", exact=True), 'click', "Re-click on the 'Scan Units LY' option (exact match) to ensure the selection is applied.")
    # Re-click on the 'Scan Units LY' option (exact match) again to confirm the selection.
    safe_action(shared_page, shared_page.get_by_text("Scan Units LY", exact=True), 'click', "Re-click on the 'Scan Units LY' option (exact match) again to confirm the selection.")

@pytest.mark.order(36)
def test_dropdown_selection_actions_part_2(shared_page: Page):
    # Click on the 'Freshness' option (3rd occurrence) to select it from the dropdown.
    safe_action(shared_page, shared_page.get_by_text("Freshness").nth(2), 'click', "Click on the 'Freshness' option (3rd occurrence) to select it from the dropdown.")
    # Click on the '% Change Scan Units' option (exact match) to select it from the dropdown.
    safe_action(shared_page, shared_page.get_by_text("% Change Scan Units", exact=True), 'click', "Click on the '% Change Scan Units' option (exact match) to select it from the dropdown.")
    # Click on the 'Aged Return Units' option (2nd occurrence) to select it from the dropdown.
    safe_action(shared_page, shared_page.get_by_text("Aged Return Units").nth(1), 'click', "Click on the 'Aged Return Units' option (2nd occurrence) to select it from the dropdown.")
    # Click on the first selected dropdown option to confirm or refine the selection.
    safe_action(shared_page, shared_page.locator(".d-flex.dropdown-option.align-items-center.p-v-5.p-l-32.p-r-16.selected").first, 'click', "Click on the first selected dropdown option to confirm or refine the selection.")
    # Click on the 'System MAPE' option (exact match) to select it from the dropdown.
    safe_action(shared_page, shared_page.get_by_text("System MAPE", exact=True), 'click', "Click on the 'System MAPE' option (exact match) to select it from the dropdown.")
    # Click on the 'Forecast Value Add - MAPE' option (exact match) to select it from the dropdown.
    safe_action(shared_page, shared_page.get_by_text("Forecast Value Add - MAPE", exact=True), 'click', "Click on the 'Forecast Value Add - MAPE' option (exact match) to select it from the dropdown.")
    # Click on the first selected dropdown option to confirm or refine the selection.
    safe_action(shared_page, shared_page.locator(".d-flex.dropdown-option.align-items-center.p-v-5.p-l-32.p-r-16.selected").first, 'click', "Click on the first selected dropdown option to confirm or refine the selection.")
    # Click on the 'System Bias' option (exact match) to select it from the dropdown.
    safe_action(shared_page, shared_page.get_by_text("System Bias", exact=True), 'click', "Click on the 'System Bias' option (exact match) to select it from the dropdown.")
    # Click on the 'Forecast Value Add - Bias' option (exact match) to select it from the dropdown.
    safe_action(shared_page, shared_page.get_by_text("Forecast Value Add - Bias", exact=True), 'click', "Click on the 'Forecast Value Add - Bias' option (exact match) to select it from the dropdown.")
    # Click on the second occurrence of the 'Promo' option to select it from the dropdown.
    safe_action(shared_page, shared_page.get_by_text("Promo", exact=True).nth(1), 'click', "Click on the second occurrence of the 'Promo' option to select it from the dropdown.")
    # Click on the first element within the '.d-flex.dropdown-option' container to select it.
    safe_action(shared_page, shared_page.locator(".d-flex.dropdown-option").first, 'click', "Click on the first element within the '.d-flex.dropdown-option' container to select it.")

@pytest.mark.order(37)
def test_weekly_summary_interaction(shared_page: Page):
    # Click on the button within the 'esp-card-component' that contains the text 'Weekly Summary Customer:3RD'.
    safe_action(shared_page, shared_page.locator("esp-card-component").filter(has_text="Weekly Summary Customer:3RD").get_by_role("button"), 'click', "Click on the button within the 'esp-card-component' that contains the text 'Weekly Summary Customer:3RD'.")

@pytest.mark.order(38)
def test_filter_columns_input_handling(shared_page: Page):
    # Click on the textbox labeled 'Filter Columns Input' to activate it for input.
    safe_action(shared_page, shared_page.get_by_role("textbox", name="Filter Columns Input"), 'click', "Click on the textbox labeled 'Filter Columns Input' to activate it for input.")
    # Fill the 'Filter Columns Input' textbox with the date '2025-07-27' to filter columns.
    safe_action(shared_page, shared_page.get_by_role("textbox", name="Filter Columns Input"), 'fill', "Fill the 'Filter Columns Input' textbox with the date '2025-07-27' to filter columns.", "2025-07-27")
    # Click on the text '-07-27 (31)' to select the corresponding column.
    safe_action(shared_page, shared_page.get_by_text("-07-27 (31)"), 'click', "Click on the text '-07-27 (31)' to select the corresponding column.")
    # Check the checkbox labeled 'Press SPACE to toggle visibility (hidden)' to make the column visible.
    safe_action(shared_page, shared_page.get_by_role("checkbox", name="Press SPACE to toggle visibility (hidden)"), 'check', "Check the checkbox labeled 'Press SPACE to toggle visibility (hidden)' to make the column visible.")
    # Click on the 'Filter Columns Input' textbox to activate it for further input.
    safe_action(shared_page, shared_page.get_by_role("textbox", name="Filter Columns Input"), 'click', "Click on the 'Filter Columns Input' textbox to activate it for further input.")
    # Clear the 'Filter Columns Input' textbox by filling it with an empty string.
    safe_action(shared_page, shared_page.get_by_role("textbox", name="Filter Columns Input"), 'fill', "Clear the 'Filter Columns Input' textbox by filling it with an empty string.", "")

@pytest.mark.order(39)
def test_filter_and_column_visibility_actions(shared_page: Page):
    # Press 'Enter' in the 'Filter Columns Input' textbox to apply the filter.
    safe_action(shared_page, shared_page.get_by_role("textbox", name="Filter Columns Input"), 'press', "Press 'Enter' in the 'Filter Columns Input' textbox to apply the filter.", "Enter")
    # Check the 'Toggle All Columns Visibility' checkbox to make all columns visible.
    safe_action(shared_page, shared_page.get_by_role("checkbox", name="Toggle All Columns Visibility"), 'check', "Check the 'Toggle All Columns Visibility' checkbox to make all columns visible.")

@pytest.mark.order(40)
def test_column_interaction_by_label_and_text(shared_page: Page):
    # Click on the text '-07-27 (31)' within the label '-07-27 (31) Column' to interact with the column.
    safe_action(shared_page, shared_page.get_by_label("-07-27 (31) Column").get_by_text("-07-27 (31)"), 'click', "Click on the text '-07-27 (31)' within the label '-07-27 (31) Column' to interact with the column.")
    # Click on the text '-08-03 (32)' within the label '-08-03 (32) Column' to interact with the column.
    safe_action(shared_page, shared_page.get_by_label("-08-03 (32) Column").get_by_text("-08-03 (32)"), 'click', "Click on the text '-08-03 (32)' within the label '-08-03 (32) Column' to interact with the column.")
    # Click on the text '-08-10 (33)' within the label '-08-10 (33) Column' to interact with the column.
    safe_action(shared_page, shared_page.get_by_label("-08-10 (33) Column").get_by_text("-08-10 (33)"), 'click', "Click on the text '-08-10 (33)' within the label '-08-10 (33) Column' to interact with the column.")
    # Click on the text '-08-24 (35)' within the label '-08-24 (35) Column' to interact with the column.
    safe_action(shared_page, shared_page.get_by_label("-08-24 (35) Column").get_by_text("-08-24 (35)"), 'click', "Click on the text '-08-24 (35)' within the label '-08-24 (35) Column' to interact with the column.")
    # Click on the text '-08-24 (35)' to interact with the column.
    safe_action(shared_page, shared_page.get_by_text("-08-24 (35)"), 'click', "Click on the text '-08-24 (35)' to interact with the column.")
    # Click on the text '-10-19 (43)' to interact with the column.
    safe_action(shared_page, shared_page.get_by_text("-10-19 (43)"), 'click', "Click on the text '-10-19 (43)' to interact with the column.")

@pytest.mark.order(41)
def test_weekly_summary_and_export_actions(shared_page: Page):
    # Click on the button within the 'esp-card-component' containing the text 'Weekly Summary Customer:3RD' to perform an action.
    safe_action(shared_page, shared_page.locator("esp-card-component").filter(has_text="Weekly Summary Customer:3RD").get_by_role("button"), 'click', "Click on the button within the 'esp-card-component' containing the text 'Weekly Summary Customer:3RD' to perform an action.")
    # Start monitoring for a file download triggered by the next action.
    with shared_page.expect_download() as download2_info:
    # Click on the 'Export' icon within the 'esp-grid-icons-component' to initiate the export process.
        safe_action(shared_page, shared_page.locator("esp-grid-icons-component").filter(has_text="Export").locator("#export-iconId"), 'click', "Click on the 'Export' icon within the 'esp-grid-icons-component' to initiate the export process.")
    download2 = download2_info.value

@pytest.mark.order(42)
def test_preference_management(shared_page: Page):
    # Click on the dropdown menu under the 'Preference' section to open the options.
    safe_action(shared_page, shared_page.locator("div:nth-child(4) > #preference-iconId > .legend-font > .multiselect-dropdown > .pointer"), 'click', "Click on the dropdown menu under the 'Preference' section to open the options.")
    # Click on the 'Save Preference' option to save the current preferences.
    safe_action(shared_page, shared_page.locator("div").filter(has_text=re.compile(r"^Save Preference$")).first, 'click', "Click on the 'Save Preference' option to save the current preferences.")
    # Click on the dropdown menu under the 'Preference' section again to reopen the options.
    safe_action(shared_page, shared_page.locator("div:nth-child(4) > #preference-iconId > .legend-font > .multiselect-dropdown > .pointer"), 'click', "Click on the dropdown menu under the 'Preference' section again to reopen the options.")
    # Click on the 'Reset Preference' option to reset the preferences to their default state.
    safe_action(shared_page, shared_page.get_by_text("Reset Preference"), 'click', "Click on the 'Reset Preference' option to reset the preferences to their default state.")

@pytest.mark.order(43)
def test_grid_column_and_icon_interactions(shared_page: Page):
    # Click on the first column header in the grid to interact with it.
    safe_action(shared_page, shared_page.locator(".ag-header-cell.ag-column-first.ag-header-parent-hidden.ag-header-background.ag-focus-managed.ag-header-active > .ag-header-cell-comp-wrapper > .ag-cell-label-container > .ag-header-cell-label"), 'click', "Click on the first column header in the grid to interact with it.")
    # Select the 'User Forecast Total' column from the grid.
    safe_action(shared_page, shared_page.locator("esp-column-dimentional-grid").get_by_text("User Forecast Total"), 'click', "Select the 'User Forecast Total' column from the grid.")
    # Click on the first icon (likely an expand or action button) in the grid.
    safe_action(shared_page, shared_page.locator("i").first, 'click', "Click on the first icon (likely an expand or action button) in the grid.")
    # Click on the third icon in the grid (possibly another action or expand button).
    safe_action(shared_page, shared_page.locator("i").nth(2), 'click', "Click on the third icon in the grid (possibly another action or expand button).")
    # Select the 'User Override Total' column from the grid.
    safe_action(shared_page, shared_page.locator("span").filter(has_text="User Override Total").first, 'click', "Select the 'User Override Total' column from the grid.")
    # Click on the 'System Forecast Total' column header to interact with it.
    safe_action(shared_page, shared_page.get_by_text("System Forecast Total", exact=True), 'click', "Click on the 'System Forecast Total' column header to interact with it.")
    # Click on the fifth icon in the grid (likely another action or expand button).
    safe_action(shared_page, shared_page.locator("i").nth(4), 'click', "Click on the fifth icon in the grid (likely another action or expand button).")
    # Select the 'Weekly Forecast Total' column from the grid.
    safe_action(shared_page, shared_page.locator("span").filter(has_text="Weekly Forecast Total").first, 'click', "Select the 'Weekly Forecast Total' column from the grid.")

@pytest.mark.order(44)
def test_grid_group_expansion_and_column_selection(shared_page: Page):
    # Expand the first group in the grid by clicking the right chevron icon.
    safe_action(shared_page, shared_page.locator(".ag-cell-value.ag-cell.ag-cell-not-inline-editing.ag-cell-normal-height.ag-cell-last-left-pinned.ag-column-first.ag-cell-override-normal.notosans-overwrite.no-border.ag-cell-focus > .ag-cell-wrapper > .ag-group-contracted > .zeb-chevron-right"), 'click', "Expand the first group in the grid by clicking the right chevron icon.")
    # Select the 'Daily Suggested Order Total' column from the grid.
    safe_action(shared_page, shared_page.locator("span").filter(has_text="Daily Suggested Order Total").first, 'click', "Select the 'Daily Suggested Order Total' column from the grid.")
    # Expand the first group in the grid again by clicking the right chevron icon.
    safe_action(shared_page, shared_page.locator(".ag-cell-value.ag-cell.ag-cell-not-inline-editing.ag-cell-normal-height.ag-cell-last-left-pinned.ag-column-first.ag-cell-override-normal.notosans-overwrite.no-border.ag-cell-focus > .ag-cell-wrapper > .ag-group-contracted > .zeb-chevron-right"), 'click', "Expand the first group in the grid again by clicking the right chevron icon.")
    # Collapse the expanded group in the grid by clicking the down chevron icon.
    safe_action(shared_page, shared_page.locator(".ag-cell-value.ag-cell.ag-cell-not-inline-editing.ag-cell-normal-height.ag-cell-last-left-pinned.ag-column-first.ag-cell-override-normal.notosans-overwrite.no-border.ag-cell-focus > .ag-cell-wrapper > .ag-group-expanded > .zeb-chevron-down"), 'click', "Collapse the expanded group in the grid by clicking the down chevron icon.")
    # Expand another group in the grid by clicking the right chevron icon.
    safe_action(shared_page, shared_page.locator(".ag-row-odd.ag-row-no-focus.ag-row-not-inline-editing.ag-row.ag-row-level-0.ag-row-group.ag-row-group-contracted.ag-row-position-absolute.ag-row-hover > .ag-cell-value > .ag-cell-wrapper > .ag-group-contracted > .zeb-chevron-right"), 'click', "Expand another group in the grid by clicking the right chevron icon.")
    # Select the 'Aged Net Units' column from the grid.
    safe_action(shared_page, shared_page.locator("esp-column-dimentional-grid").get_by_text("Aged Net Units", exact=True), 'click', "Select the 'Aged Net Units' column from the grid.")

@pytest.mark.order(45)
def test_grid_interaction_and_initial_navigation(shared_page: Page):
    # Select the 'Scan Units' column from the grid.
    safe_action(shared_page, shared_page.locator("esp-column-dimentional-grid").get_by_text("Scan Units"), 'click', "Select the 'Scan Units' column from the grid.")
    # Expand the first group in the grid again by clicking the right chevron icon.
    safe_action(shared_page, shared_page.locator(".ag-cell-value.ag-cell.ag-cell-not-inline-editing.ag-cell-normal-height.ag-cell-last-left-pinned.ag-column-first.ag-cell-override-normal.notosans-overwrite.no-border.ag-cell-focus > .ag-cell-wrapper > .ag-group-contracted > .zeb-chevron-right"), 'click', "Expand the first group in the grid again by clicking the right chevron icon.")
    # Expand another group in the grid by clicking the right chevron icon.
    safe_action(shared_page, shared_page.locator(".ag-row-odd.ag-row-no-focus.ag-row-not-inline-editing.ag-row.ag-row-level-0.ag-row-group.ag-row-group-contracted.ag-row-position-absolute.ag-row-hover > .ag-cell-value > .ag-cell-wrapper > .ag-group-contracted > .zeb-chevron-right"), 'click', "Expand another group in the grid by clicking the right chevron icon.")
    # Select the 'User MAPE' column from the grid.
    safe_action(shared_page, shared_page.locator("esp-column-dimentional-grid").get_by_text("User MAPE"), 'click', "Select the 'User MAPE' column from the grid.")
    # Click on the 'Weekly Trend Customer:3RD' text to select the customer.
    safe_action(shared_page, shared_page.get_by_text("Weekly Trend Customer:3RD"), 'click', "Click on the 'Weekly Trend Customer:3RD' text to select the customer.")
    # Click on the 'Weekly Trend' text to navigate to the Weekly Trend section.
    safe_action(shared_page, shared_page.get_by_text("Weekly Trend"), 'click', "Click on the 'Weekly Trend' text to navigate to the Weekly Trend section.")

@pytest.mark.order(46)
def test_line_bar_chart_interaction___customer_selection(shared_page: Page):
    # Click on the 'Customer:3RD PARTY DISTRIB' label in the line-bar chart to interact with it.
    safe_action(shared_page, shared_page.locator("dp-line-bar-chart").get_by_text("Customer:3RD PARTY DISTRIB"), 'click', "Click on the 'Customer:3RD PARTY DISTRIB' label in the line-bar chart to interact with it.")
    # Click on the 'Customer:3RD PARTY DISTRIB' label in the line-bar chart again, possibly to toggle or confirm selection.
    safe_action(shared_page, shared_page.locator("dp-line-bar-chart").get_by_text("Customer:3RD PARTY DISTRIB"), 'click', "Click on the 'Customer:3RD PARTY DISTRIB' label in the line-bar chart again, possibly to toggle or confirm selection.")
    # Click on the 'Customer' label in the line-bar chart with exact match to interact with it.
    safe_action(shared_page, shared_page.locator("dp-line-bar-chart").get_by_text("Customer", exact=True), 'click', "Click on the 'Customer' label in the line-bar chart with exact match to interact with it.")
    # Click on the '3RD PARTY DISTRIB' label in the line-bar chart to interact with it.
    safe_action(shared_page, shared_page.locator("dp-line-bar-chart").get_by_text("3RD PARTY DISTRIB"), 'click', "Click on the '3RD PARTY DISTRIB' label in the line-bar chart to interact with it.")

@pytest.mark.order(47)
def test_line_bar_chart_interaction___user_forecast(shared_page: Page):
    # Click on the first occurrence of 'User Forecast Total, User' text to select it.
    safe_action(shared_page, shared_page.get_by_text("User Forecast Total, User").first, 'click', "Click on the first occurrence of 'User Forecast Total, User' text to select it.")
    # Click on the 'User Forecast Total' label within the line-bar chart to interact with it.
    safe_action(shared_page, shared_page.locator("dp-line-bar-chart span").filter(has_text="User Forecast Total"), 'click', "Click on the 'User Forecast Total' label within the line-bar chart to interact with it.")
    # Click on the 'User Forecast Base' text to select it.
    safe_action(shared_page, shared_page.get_by_text("User Forecast Base"), 'click', "Click on the 'User Forecast Base' text to select it.")
    # Click on the third child element within the '.overflow-auto' container, likely to interact with a dropdown or menu.
    safe_action(shared_page, shared_page.locator(".overflow-auto > div:nth-child(3)"), 'click', "Click on the third child element within the '.overflow-auto' container, likely to interact with a dropdown or menu.")
    # Click on the 'User Override Total' label within the line-bar chart to interact with it.
    safe_action(shared_page, shared_page.locator("dp-line-bar-chart span").filter(has_text="User Override Total"), 'click', "Click on the 'User Override Total' label within the line-bar chart to interact with it.")

@pytest.mark.order(48)
def test_line_bar_chart_interaction___user_override(shared_page: Page):
    # Click on the 'User Override Base' text to select it.
    safe_action(shared_page, shared_page.get_by_text("User Override Base"), 'click', "Click on the 'User Override Base' text to select it.")
    # Click on the 'User Override Promotion' text to select it.
    safe_action(shared_page, shared_page.get_by_text("User Override Promotion"), 'click', "Click on the 'User Override Promotion' text to select it.")
    # Click on the sixth child element within the '.overflow-auto' container, likely to interact with a dropdown or menu.
    safe_action(shared_page, shared_page.locator(".overflow-auto > div:nth-child(6)"), 'click', "Click on the sixth child element within the '.overflow-auto' container, likely to interact with a dropdown or menu.")

@pytest.mark.order(49)
def test_line_bar_chart_interaction___system_forecast(shared_page: Page):
    # Click on the 'System Forecast Total' label within the line-bar chart to interact with it.
    safe_action(shared_page, shared_page.locator("dp-line-bar-chart").get_by_text("System Forecast Total"), 'click', "Click on the 'System Forecast Total' label within the line-bar chart to interact with it.")
    # Click on the 'System Forecast Base' text with exact match to select it.
    safe_action(shared_page, shared_page.get_by_text("System Forecast Base", exact=True), 'click', "Click on the 'System Forecast Base' text with exact match to select it.")
    # Click on the 'System Forecast Promotion' text with exact match to select it.
    safe_action(shared_page, shared_page.get_by_text("System Forecast Promotion", exact=True), 'click', "Click on the 'System Forecast Promotion' text with exact match to select it.")
    # Click on the tenth child element within the '.overflow-auto' container, likely to interact with a dropdown or menu.
    safe_action(shared_page, shared_page.locator(".overflow-auto > div:nth-child(10)"), 'click', "Click on the tenth child element within the '.overflow-auto' container, likely to interact with a dropdown or menu.")

@pytest.mark.order(50)
def test_line_bar_chart_interaction___weekly_forecast(shared_page: Page):
    # Click on the 'Weekly Forecast Base' label within the line-bar chart to interact with it.
    safe_action(shared_page, shared_page.locator("dp-line-bar-chart").get_by_text("Weekly Forecast Base"), 'click', "Click on the 'Weekly Forecast Base' label within the line-bar chart to interact with it.")
    # Click on the 'Weekly Forecast Promotion' label within the line-bar chart to interact with it.
    safe_action(shared_page, shared_page.locator("dp-line-bar-chart").get_by_text("Weekly Forecast Promotion"), 'click', "Click on the 'Weekly Forecast Promotion' label within the line-bar chart to interact with it.")
    # Click on the 'Weekly Forecast Promotion' label within the line-bar chart again, possibly to toggle or confirm selection.
    safe_action(shared_page, shared_page.locator("dp-line-bar-chart").get_by_text("Weekly Forecast Promotion"), 'click', "Click on the 'Weekly Forecast Promotion' label within the line-bar chart again, possibly to toggle or confirm selection.")
    # Click on the fifteenth child element within the '.overflow-auto' container, likely to interact with a dropdown or menu.
    safe_action(shared_page, shared_page.locator(".overflow-auto > div:nth-child(15)"), 'click', "Click on the fifteenth child element within the '.overflow-auto' container, likely to interact with a dropdown or menu.")

@pytest.mark.order(51)
def test_line_bar_chart_interaction___daily_suggested_order(shared_page: Page):
    # Click on the fourteenth child element within the '.overflow-auto' container, likely to interact with a dropdown or menu.
    safe_action(shared_page, shared_page.locator(".overflow-auto > div:nth-child(14)"), 'click', "Click on the fourteenth child element within the '.overflow-auto' container, likely to interact with a dropdown or menu.")
    # Click on the 'Daily Suggested Order Total' label within the line-bar chart to interact with it.
    safe_action(shared_page, shared_page.locator("dp-line-bar-chart").get_by_text("Daily Suggested Order Total"), 'click', "Click on the 'Daily Suggested Order Total' label within the line-bar chart to interact with it.")
    # Click on the 'Daily Suggested Order Promotion' text to select it.
    safe_action(shared_page, shared_page.locator("span").filter(has_text="Daily Suggested Order Promotion"), 'click', "Click on the 'Daily Suggested Order Promotion' text to select it.")
    # Click on the 'Daily Suggested Order Base' text to select it.
    safe_action(shared_page, shared_page.locator("span").filter(has_text="Daily Suggested Order Base"), 'click', "Click on the 'Daily Suggested Order Base' text to select it.")

@pytest.mark.order(52)
def test_daily_suggested_order_base_interaction(shared_page: Page):
    # Click on the 'Daily Suggested Order Base' text again, possibly to toggle or confirm selection.
    safe_action(shared_page, shared_page.locator("span").filter(has_text="Daily Suggested Order Base"), 'click', "Click on the 'Daily Suggested Order Base' text again, possibly to toggle or confirm selection.")

@pytest.mark.order(53)
def test_aged_net_units_selection(shared_page: Page):
    # Click on the second occurrence of the 'Aged Net Units' text with an exact match to select it.
    safe_action(shared_page, shared_page.get_by_text("Aged Net Units", exact=True).nth(1), 'click', "Click on the second occurrence of the 'Aged Net Units' text with an exact match to select it.")

@pytest.mark.order(54)
def test_overflow_auto_container_interactions(shared_page: Page):
    # Click on the fifteenth child element within the '.overflow-auto' container, likely to interact with a dropdown or menu.
    safe_action(shared_page, shared_page.locator(".overflow-auto > div:nth-child(15)"), 'click', "Click on the fifteenth child element within the '.overflow-auto' container, likely to interact with a dropdown or menu.")
    # Click on the fifteenth child element within the '.overflow-auto' container again, possibly to toggle or confirm selection.
    safe_action(shared_page, shared_page.locator(".overflow-auto > div:nth-child(15)"), 'click', "Click on the fifteenth child element within the '.overflow-auto' container again, possibly to toggle or confirm selection.")
    # Click on the seventeenth child element within the '.overflow-auto' container, likely to interact with a dropdown or menu.
    safe_action(shared_page, shared_page.locator(".overflow-auto > div:nth-child(17)"), 'click', "Click on the seventeenth child element within the '.overflow-auto' container, likely to interact with a dropdown or menu.")
    # Click on the 'Aged Net Units' label within the line-bar chart with an exact match to interact with it.
    safe_action(shared_page, shared_page.locator("dp-line-bar-chart").get_by_text("Aged Net Units", exact=True), 'click', "Click on the 'Aged Net Units' label within the line-bar chart with an exact match to interact with it.")
    # Click on the 'Aged Net Units LY' label within the line-bar chart to interact with it.
    safe_action(shared_page, shared_page.locator("dp-line-bar-chart").get_by_text("Aged Net Units LY"), 'click', "Click on the 'Aged Net Units LY' label within the line-bar chart to interact with it.")
    # Click on the 'Scan Units LY' label within the line-bar chart to interact with it.
    safe_action(shared_page, shared_page.locator("dp-line-bar-chart").get_by_text("Scan Units LY"), 'click', "Click on the 'Scan Units LY' label within the line-bar chart to interact with it.")
    # Click on the twenty-second child element within the '.overflow-auto' container, likely to interact with a dropdown or menu.
    safe_action(shared_page, shared_page.locator(".overflow-auto > div:nth-child(22)"), 'click', "Click on the twenty-second child element within the '.overflow-auto' container, likely to interact with a dropdown or menu.")
    # Click on the twenty-third child element within the '.overflow-auto' container, likely to interact with a dropdown or menu.
    safe_action(shared_page, shared_page.locator(".overflow-auto > div:nth-child(23)"), 'click', "Click on the twenty-third child element within the '.overflow-auto' container, likely to interact with a dropdown or menu.")
    # Click on the twenty-fourth child element within the '.overflow-auto' container, likely to interact with a dropdown or menu.
    safe_action(shared_page, shared_page.locator(".overflow-auto > div:nth-child(24)"), 'click', "Click on the twenty-fourth child element within the '.overflow-auto' container, likely to interact with a dropdown or menu.")

@pytest.mark.order(55)
def test_line_bar_chart_interactions(shared_page: Page):
    # Click on the 'Forecast Value Add - MAPE' label within the line-bar chart to interact with it.
    safe_action(shared_page, shared_page.locator("dp-line-bar-chart").get_by_text("Forecast Value Add - MAPE"), 'click', "Click on the 'Forecast Value Add - MAPE' label within the line-bar chart to interact with it.")
    # Click on the twenty-sixth child element within the parent 'div', likely to interact with a dropdown or menu.
    safe_action(shared_page, shared_page.locator("div:nth-child(26)"), 'click', "Click on the twenty-sixth child element within the parent 'div', likely to interact with a dropdown or menu.")
    # Click on the twenty-seventh child element within the parent 'div', likely to interact with a dropdown or menu.
    safe_action(shared_page, shared_page.locator("div:nth-child(27)"), 'click', "Click on the twenty-seventh child element within the parent 'div', likely to interact with a dropdown or menu.")
    # Click on the 'Forecast Value Add - Bias' label within the line-bar chart to interact with it.
    safe_action(shared_page, shared_page.locator("dp-line-bar-chart").get_by_text("Forecast Value Add - Bias"), 'click', "Click on the 'Forecast Value Add - Bias' label within the line-bar chart to interact with it.")

@pytest.mark.order(56)
def test_user_forecast_base_and_preferences(shared_page: Page):
    # Click on the text 'User Forecast Base, User' to select or interact with the corresponding element.
    safe_action(shared_page, shared_page.get_by_text("User Forecast Base, User").first, 'click', "Click on the text 'User Forecast Base, User' to select or interact with the corresponding element.")
    # Click on the dropdown menu associated with the preference icon to open the preference options.
    safe_action(shared_page, shared_page.locator(".title.d-flex.align-items-center.font-size-16.font-weight-bold.nunito.title-color > .grid-icons-container > esp-grid-icons-component > .display-grid-icons > div > #preference-iconId > .legend-font > .multiselect-dropdown > .pointer"), 'click', "Click on the dropdown menu associated with the preference icon to open the preference options.")
    # Click on the 'Save Preference' button to save the current user preferences.
    safe_action(shared_page, shared_page.get_by_text("Save Preference"), 'click', "Click on the 'Save Preference' button to save the current user preferences.")
    # Click on the dropdown menu associated with the preference icon again, likely to perform another action.
    safe_action(shared_page, shared_page.locator(".title.d-flex.align-items-center.font-size-16.font-weight-bold.nunito.title-color > .grid-icons-container > esp-grid-icons-component > .display-grid-icons > div > #preference-iconId > .legend-font > .multiselect-dropdown > .pointer"), 'click', "Click on the dropdown menu associated with the preference icon again, likely to perform another action.")
    # Click on the 'Reset Preference' option to reset the user preferences to their default state.
    safe_action(shared_page, shared_page.locator("div").filter(has_text=re.compile(r"^Reset Preference$")).first, 'click', "Click on the 'Reset Preference' option to reset the user preferences to their default state.")

@pytest.mark.order(57)
def test_svg_and_text_element_interactions(shared_page: Page):
    # Click on a specific SVG path element, likely to interact with a visual component or chart.
    safe_action(shared_page, shared_page.locator("path:nth-child(157)"), 'click', "Click on a specific SVG path element, likely to interact with a visual component or chart.")
    # Click on the text 'User Forecast Total' within an SVG element, possibly to select or highlight it.
    safe_action(shared_page, shared_page.locator("svg").get_by_text("User Forecast Total"), 'click', "Click on the text 'User Forecast Total' within an SVG element, possibly to select or highlight it.")
    # Click on the text 'User Override Total' within an SVG element, likely to interact with or select it.
    safe_action(shared_page, shared_page.locator("svg").get_by_text("User Override Total"), 'click', "Click on the text 'User Override Total' within an SVG element, likely to interact with or select it.")
    # Click on the text 'Aged Net Units' within a text element, possibly to filter or highlight related data.
    safe_action(shared_page, shared_page.locator("text").filter(has_text="Aged Net Units"), 'click', "Click on the text 'Aged Net Units' within a text element, possibly to filter or highlight related data.")
    # Click on the SVG element, potentially to reset or deselect a previous selection.
    safe_action(shared_page, shared_page.locator("svg"), 'click', "Click on the SVG element, potentially to reset or deselect a previous selection.")

@pytest.mark.order(58)
def test_percentage_and_date_selection(shared_page: Page):
    # Click on the exact text '0%' to interact with a specific data point or value.
    safe_action(shared_page, shared_page.get_by_text("0%", exact=True), 'click', "Click on the exact text '0%' to interact with a specific data point or value.")
    # Click on the text '20%' to interact with or select a specific percentage value.
    safe_action(shared_page, shared_page.get_by_text("20%"), 'click', "Click on the text '20%' to interact with or select a specific percentage value.")
    # Click on the text '02/01/' to select or interact with a specific date.
    safe_action(shared_page, shared_page.get_by_text("02/01/"), 'click', "Click on the text '02/01/' to select or interact with a specific date.")
    # Click on the text '01/11/' to select or interact with another specific date.
    safe_action(shared_page, shared_page.get_by_text("01/11/"), 'click', "Click on the text '01/11/' to select or interact with another specific date.")
    # Click on the text '12/21/' to select or interact with another specific date.
    safe_action(shared_page, shared_page.get_by_text("12/21/"), 'click', "Click on the text '12/21/' to select or interact with another specific date.")

