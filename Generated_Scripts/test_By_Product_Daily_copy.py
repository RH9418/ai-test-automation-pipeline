
import os
import sys
import time
import re
import atexit
import contextlib
from datetime import datetime
import pytest
from playwright.sync_api import sync_playwright, Playwright, Page, expect, TimeoutError

SCREENSHOT_DIR = "Test_Screenshots"
if not os.path.exists(SCREENSHOT_DIR): os.makedirs(SCREENSHOT_DIR)
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
        locator.scroll_into_view_if_needed(timeout=1000)
        locator.wait_for(state='visible', timeout=1000)
        
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
            
            time.sleep(0.05) 
            page.screenshot(path=path, full_page=False)
            print(f"   └── 📸 Screenshot saved: {path}")
            
            page.evaluate('''() => {
                document.getElementById('ge-spotlight-box')?.remove();
                document.getElementById('ge-spotlight-label')?.remove();
            }''')
            return
            
    except Exception:
        pass 

    try:
        page.screenshot(path=path, full_page=False)
        print(f"   └── 📸 Context Screenshot saved (Element was transient): {path}")
    except Exception as e:
        print(f"   └── ⚠️ Total Screenshot Error: {e}")

@contextlib.contextmanager
def safe_download(page: Page, timeout_ms=300000): # 5 minutes default timeout
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
    except Exception as e:
        print(f"\n❌ ERROR: Download failed or timed out: {e}")
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
    
    try:
        if action_name == 'fill':
            print(f"\n⏸️ PAUSING FOR INPUT: About to fill '{description}'.")
            input("   └── Perform input manually in browser, then PRESS [ENTER] to continue...")
            page.wait_for_load_state('networkidle', timeout=5000)
            return

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
        
        try:
            global screenshot_counter
            screenshot_counter += 1
            timestamp = datetime.now().strftime("%H-%M-%S")
            safe_filename = re.sub(r'[^a-z0-9]', '_', description.lower())[:40]
            fail_path = os.path.join(SCREENSHOT_DIR, f"{timestamp}_{screenshot_counter:02d}_FAILED_{safe_filename}.png")
            page.screenshot(path=fail_path, full_page=False)
            print(f"   └── 📸 Pre-Intervention Context Screenshot saved: {fail_path}")
        except: pass
        
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
    safe_action(shared_page, shared_page, 'goto', "Navigate to the specified URL for the 'Executive Dashboard' in the demand planning application.", "https://stage.bbu.esp.antuit.ai/dp/demand-planning/executive-dashboard?workbookId=4&tabIndex=3")
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
def test_product_total_columns_configuration(shared_page: Page):
    # Click on the 'Product Total columns (0)' text to open the configuration panel for product total columns.
    safe_action(shared_page, shared_page.get_by_text("Product Total columns (0)"), 'click', "Click on the 'Product Total columns (0)' text to open the configuration panel for product total columns.")
    # Repeat the click on 'Product Total columns (0)' to ensure the panel is opened (possibly redundant or for stability).
    safe_action(shared_page, shared_page.get_by_text("Product Total columns (0)"), 'click', "Repeat the click on 'Product Total columns (0)' to ensure the panel is opened (possibly redundant or for stability).")
    # Click on the 'Product Total' text to select or focus on the product total section.
    safe_action(shared_page, shared_page.get_by_text("Product Total"), 'click', "Click on the 'Product Total' text to select or focus on the product total section.")
    # Click on the button within the 'Product Total columns (0)' card component to proceed with further configuration.
    safe_action(shared_page, shared_page.locator("esp-card-component").filter(has_text="Product Total columns (0)").get_by_role("button"), 'click', "Click on the button within the 'Product Total columns (0)' card component to proceed with further configuration.")

@pytest.mark.order(4)
def test_filter_columns_input_interaction(shared_page: Page):
    # Click on the 'Filter Columns Input' textbox to focus on the input field for filtering columns.
    safe_action(shared_page, shared_page.get_by_role("textbox", name="Filter Columns Input"), 'click', "Click on the 'Filter Columns Input' textbox to focus on the input field for filtering columns.")
    # Uncheck the 'Toggle All Columns Visibility' checkbox to hide all columns initially.
    safe_action(shared_page, shared_page.get_by_role("checkbox", name="Toggle All Columns Visibility"), 'uncheck', "Uncheck the 'Toggle All Columns Visibility' checkbox to hide all columns initially.")
    # Click on the 'Filter Columns Input' textbox again to ensure it is focused for input.
    safe_action(shared_page, shared_page.get_by_role("textbox", name="Filter Columns Input"), 'click', "Click on the 'Filter Columns Input' textbox again to ensure it is focused for input.")
    # Fill the 'Filter Columns Input' textbox with the text 'system' to filter columns containing this keyword.
    safe_action(shared_page, shared_page.get_by_role("textbox", name="Filter Columns Input"), 'fill', "Fill the 'Filter Columns Input' textbox with the text 'system' to filter columns containing this keyword.", "system")
    # Press 'Enter' in the 'Filter Columns Input' textbox to apply the filter.
    safe_action(shared_page, shared_page.get_by_role("textbox", name="Filter Columns Input"), 'press', "Press 'Enter' in the 'Filter Columns Input' textbox to apply the filter.", "Enter")

@pytest.mark.order(5)
def test_column_selection_and_deselection(shared_page: Page):
    # Click on the first column in the filtered list to select it.
    safe_action(shared_page, shared_page.locator(".ag-column-select-column").first, 'click', "Click on the first column in the filtered list to select it.")
    # Uncheck the checkbox for 'System Forecast Base (Plan' to deselect this column.
    safe_action(shared_page, shared_page.get_by_role("treeitem", name="System Forecast Base (Plan").get_by_label("Press SPACE to toggle"), 'uncheck', "Uncheck the checkbox for 'System Forecast Base (Plan' to deselect this column.")
    # Click on the 'Filter Columns Input' textbox to clear or modify the filter.
    safe_action(shared_page, shared_page.get_by_role("textbox", name="Filter Columns Input"), 'click', "Click on the 'Filter Columns Input' textbox to clear or modify the filter.")
    # Clear the 'Filter Columns Input' textbox by filling it with an empty string.
    safe_action(shared_page, shared_page.get_by_role("textbox", name="Filter Columns Input"), 'fill', "Clear the 'Filter Columns Input' textbox by filling it with an empty string.", "")
    # Press 'Enter' in the 'Filter Columns Input' textbox to reset the filter.
    safe_action(shared_page, shared_page.get_by_role("textbox", name="Filter Columns Input"), 'press', "Press 'Enter' in the 'Filter Columns Input' textbox to reset the filter.", "Enter")
    # Click on the 'System Forecast Total (Plan Week) Column' tree item to select it.
    safe_action(shared_page, shared_page.get_by_role("treeitem", name="System Forecast Total (Plan Week) Column"), 'click', "Click on the 'System Forecast Total (Plan Week) Column' tree item to select it.")
    # Uncheck the checkbox for 'System Forecast Base (Plan' again to ensure it is deselected.
    safe_action(shared_page, shared_page.get_by_role("treeitem", name="System Forecast Base (Plan").get_by_label("Press SPACE to toggle"), 'uncheck', "Uncheck the checkbox for 'System Forecast Base (Plan' again to ensure it is deselected.")

@pytest.mark.order(6)
def test_additional_column_selection(shared_page: Page):
    # Click on the 'System Forecast Promotion (' label to select this column.
    safe_action(shared_page, shared_page.get_by_label("System Forecast Promotion (").get_by_text("System Forecast Promotion ("), 'click', "Click on the 'System Forecast Promotion (' label to select this column.")
    # Click on the 'System Forecast Total (Plan+1' label to select this column.
    safe_action(shared_page, shared_page.get_by_label("System Forecast Total (Plan+1").get_by_text("System Forecast Total (Plan+1"), 'click', "Click on the 'System Forecast Total (Plan+1' label to select this column.")
    # Click on the 'System Forecast Base (Plan+1' label to select this column.
    safe_action(shared_page, shared_page.get_by_label("System Forecast Base (Plan+1").get_by_text("System Forecast Base (Plan+1"), 'click', "Click on the 'System Forecast Base (Plan+1' label to select this column.")
    # Click on the 'System Forecast Promotion (Plan+1 Week) Column' label to select this column.
    safe_action(shared_page, shared_page.get_by_label("System Forecast Promotion (Plan+1 Week) Column").get_by_text("System Forecast Promotion ("), 'click', "Click on the 'System Forecast Promotion (Plan+1 Week) Column' label to select this column.")
    # Click on the '6 Week Gross Units Average' label to select this column.
    safe_action(shared_page, shared_page.get_by_label("6 Week Gross Units Average").get_by_text("Week Gross Units Average"), 'click', "Click on the '6 Week Gross Units Average' label to select this column.")
    # Click on the '6 Week Aged Net Units Average Column' label to select this column.
    safe_action(shared_page, shared_page.get_by_label("6 Week Aged Net Units Average Column", exact=True).get_by_text("Week Aged Net Units Average"), 'click', "Click on the '6 Week Aged Net Units Average Column' label to select this column.")
    # Click on the 'LY 6 Week Aged Net Units' label to select this column.
    safe_action(shared_page, shared_page.get_by_label("LY 6 Week Aged Net Units").get_by_text("LY 6 Week Aged Net Units"), 'click', "Click on the 'LY 6 Week Aged Net Units' label to select this column.")
    # Click on the 'LY 6 Week Scan Units Average' label to select this column.

@pytest.mark.order(7)
def test_column_selection_and_visibility_toggles(shared_page: Page):
    safe_action(shared_page, shared_page.get_by_label("LY 6 Week Scan Units Average").get_by_text("LY 6 Week Scan Units Average"), 'click', "Perform click on page.get_by_label(\"LY 6 Week Scan Units Average\").get_by_text(\"LY 6 Week Scan Units Average\")")
    # Click on the '6 Week Scan Units Average Column' label to select this column.
    safe_action(shared_page, shared_page.get_by_label("6 Week Scan Units Average Column", exact=True).get_by_text("Week Scan Units Average"), 'click', "Click on the '6 Week Scan Units Average Column' label to select this column.")
    # Click on the '% Change 6 Week Aged Net' label to select this column.
    safe_action(shared_page, shared_page.get_by_label("% Change 6 Week Aged Net").get_by_text("% Change 6 Week Aged Net"), 'click', "Click on the '% Change 6 Week Aged Net' label to select this column.")
    # Click on the '% Change 6 Week Scan Units' label to select this column.
    safe_action(shared_page, shared_page.get_by_label("% Change 6 Week Scan Units").get_by_text("% Change 6 Week Scan Units"), 'click', "Click on the '% Change 6 Week Scan Units' label to select this column.")
    # Click on the 'Freshness (6 Week Average)' label to select this column.
    safe_action(shared_page, shared_page.get_by_label("Freshness (6 Week Average)").get_by_text("Freshness (6 Week Average)"), 'click', "Click on the 'Freshness (6 Week Average)' label to select this column.")
    # Click on the '6 Week Aged Returns Units' label to select this column.
    safe_action(shared_page, shared_page.get_by_label("6 Week Aged Returns Units").get_by_text("6 Week Aged Returns Units"), 'click', "Click on the '6 Week Aged Returns Units' label to select this column.")
    # Check the 'Toggle All Columns Visibility' checkbox to make all columns visible again.
    safe_action(shared_page, shared_page.get_by_role("checkbox", name="Toggle All Columns Visibility"), 'check', "Check the 'Toggle All Columns Visibility' checkbox to make all columns visible again.")

@pytest.mark.order(8)
def test_download_data_process(shared_page: Page):
    # Click on the 'Product Total columns (0)' button to open the column selection menu.
    safe_action(shared_page, shared_page.locator("esp-card-component").filter(has_text="Product Total columns (0)").get_by_role("button"), 'click', "Click on the 'Product Total columns (0)' button to open the column selection menu.")
    # Prepare to capture the download event triggered by the next action.
    with safe_download(shared_page) as download_info:
    # Click on the download icon to initiate the download of the selected data.
        safe_action(shared_page, shared_page.locator(".icon-color-toolbar-active.zeb-download-underline").first, 'click', "Click on the download icon to initiate the download of the selected data.")
    # Store the download information for further processing or validation.
    download = download_info.value

@pytest.mark.order(9)
def test_preference_management(shared_page: Page):
    # Click on the informational message 'Please note that a maximum of' to acknowledge it.
    safe_action(shared_page, shared_page.get_by_text("Please note that a maximum of"), 'click', "Click on the informational message 'Please note that a maximum of' to acknowledge it.")
    # Click on the adjustments icon to open the settings menu.
    safe_action(shared_page, shared_page.locator(".pointer.zeb-adjustments").first, 'click', "Click on the adjustments icon to open the settings menu.")
    # Click on 'Save Preference' to save the current column visibility settings.
    safe_action(shared_page, shared_page.get_by_text("Save Preference"), 'click', "Click on 'Save Preference' to save the current column visibility settings.")
    # Click on the adjustments icon again to reopen the settings menu.
    safe_action(shared_page, shared_page.locator(".pointer.zeb-adjustments").first, 'click', "Click on the adjustments icon again to reopen the settings menu.")
    # Click on 'Reset Preference' to reset the column visibility settings to default.
    safe_action(shared_page, shared_page.get_by_text("Reset Preference"), 'click', "Click on 'Reset Preference' to reset the column visibility settings to default.")

@pytest.mark.order(10)
def test_product_column_configuration(shared_page: Page):
    # Click on the horizontal scroll container to ensure the view is scrolled to the appropriate section.
    safe_action(shared_page, shared_page.locator(".ag-body-horizontal-scroll-container").first, 'click', "Click on the horizontal scroll container to ensure the view is scrolled to the appropriate section.")
    # Click on the 'Products columns (0) TopBottom' button to open the column selection menu.
    safe_action(shared_page, shared_page.get_by_text("Products columns (0) TopBottom"), 'click', "Click on the 'Products columns (0) TopBottom' button to open the column selection menu.")
    # Click on the 'Products' section to focus on the product-related columns.
    safe_action(shared_page, shared_page.get_by_text("Products"), 'click', "Click on the 'Products' section to focus on the product-related columns.")
    # Click on the button within the 'Products columns (0)' card to open the column configuration options.
    safe_action(shared_page, shared_page.locator("esp-card-component").filter(has_text="Products columns (0)").get_by_role("button"), 'click', "Click on the button within the 'Products columns (0)' card to open the column configuration options.")
    # Click on the 'Filter Columns Input' textbox to prepare for entering a filter value.
    safe_action(shared_page, shared_page.get_by_role("textbox", name="Filter Columns Input"), 'click', "Click on the 'Filter Columns Input' textbox to prepare for entering a filter value.")
    # Fill the 'Filter Columns Input' textbox with the value '6' to filter columns containing '6'.
    safe_action(shared_page, shared_page.get_by_role("textbox", name="Filter Columns Input"), 'fill', "Fill the 'Filter Columns Input' textbox with the value '6' to filter columns containing '6'.", "6")
    # Press 'Enter' to apply the filter and display the relevant columns.
    safe_action(shared_page, shared_page.get_by_role("textbox", name="Filter Columns Input"), 'press', "Press 'Enter' to apply the filter and display the relevant columns.", "Enter")

@pytest.mark.order(11)
def test_column_filtering_and_selection(shared_page: Page):
    # Check the visibility toggle for the 'Week Gross Units Average Column' to make it visible.
    safe_action(shared_page, shared_page.get_by_role("treeitem", name="Week Gross Units Average Column").get_by_label("Press SPACE to toggle visibility (hidden)"), 'check', "Check the visibility toggle for the 'Week Gross Units Average Column' to make it visible.")
    # Click on the '6 Week Aged Net Units Average' column to select it.
    safe_action(shared_page, shared_page.get_by_label("Column List 9 Columns").get_by_text("6 Week Aged Net Units Average", exact=True), 'click', "Click on the '6 Week Aged Net Units Average' column to select it.")
    # Click on the 'LY 6 Week Aged Net Units' column to select it.
    safe_action(shared_page, shared_page.get_by_label("LY 6 Week Aged Net Units").get_by_text("LY 6 Week Aged Net Units"), 'click', "Click on the 'LY 6 Week Aged Net Units' column to select it.")
    # Click on the '% Change 6 Week Aged Net' column to select it.
    safe_action(shared_page, shared_page.get_by_text("% Change 6 Week Aged Net"), 'click', "Click on the '% Change 6 Week Aged Net' column to select it.")
    # Click on the 'Filter Columns Input' textbox to clear the filter.
    safe_action(shared_page, shared_page.get_by_role("textbox", name="Filter Columns Input"), 'click', "Click on the 'Filter Columns Input' textbox to clear the filter.")
    # Clear the 'Filter Columns Input' textbox by filling it with an empty value.
    safe_action(shared_page, shared_page.get_by_role("textbox", name="Filter Columns Input"), 'fill', "Clear the 'Filter Columns Input' textbox by filling it with an empty value.", "")
    # Press 'Enter' to reset the filter and display all columns.
    safe_action(shared_page, shared_page.get_by_role("textbox", name="Filter Columns Input"), 'press', "Press 'Enter' to reset the filter and display all columns.", "Enter")

@pytest.mark.order(13)
def test_toggle_all_columns_visibility(shared_page: Page):
    safe_action(shared_page, shared_page.get_by_role("checkbox", name="Toggle All Columns Visibility"), 'uncheck', "Perform uncheck on page.get_by_role(\"checkbox\", name=\"Toggle All Columns Visibility\")")
    # Check the 'Toggle All Columns Visibility' checkbox to make all columns visible again.
    safe_action(shared_page, shared_page.get_by_role("checkbox", name="Toggle All Columns Visibility"), 'check', "Check the 'Toggle All Columns Visibility' checkbox to make all columns visible again.")

@pytest.mark.order(14)
def test_column_selection_and_visibility_management(shared_page: Page):
    # Click on the first column in the column list to select it.
    safe_action(shared_page, shared_page.locator("#ag-87 > .ag-column-panel > .ag-column-select > .ag-column-select-list > .ag-virtual-list-viewport > .ag-virtual-list-container > div > .ag-column-select-column").first, 'click', "Click on the first column in the column list to select it.")
    # Uncheck the visibility toggle for the 'System Forecast Base (Plan Week) Column' to hide it.
    safe_action(shared_page, shared_page.get_by_role("treeitem", name="System Forecast Base (Plan Week) Column").get_by_label("Press SPACE to toggle visibility (visible)"), 'uncheck', "Uncheck the visibility toggle for the 'System Forecast Base (Plan Week) Column' to hide it.")
    # Uncheck the visibility toggle for the 'System Forecast Promotion (Plan Week) Column' to hide it.
    safe_action(shared_page, shared_page.get_by_role("treeitem", name="System Forecast Promotion (Plan Week) Column").get_by_label("Press SPACE to toggle visibility (visible)"), 'uncheck', "Uncheck the visibility toggle for the 'System Forecast Promotion (Plan Week) Column' to hide it.")
    # Uncheck the visibility toggle for the 'System Forecast Total (Plan+1)' column to hide it.
    safe_action(shared_page, shared_page.get_by_role("treeitem", name="System Forecast Total (Plan+1").get_by_label("Press SPACE to toggle visibility (visible)"), 'uncheck', "Uncheck the visibility toggle for the 'System Forecast Total (Plan+1)' column to hide it.")
    # Uncheck the visibility toggle for the 'System Forecast Base (Plan+1)' column to hide it.
    safe_action(shared_page, shared_page.get_by_role("treeitem", name="System Forecast Base (Plan+1").get_by_label("Press SPACE to toggle visibility (visible)"), 'uncheck', "Uncheck the visibility toggle for the 'System Forecast Base (Plan+1)' column to hide it.")
    # Uncheck the visibility toggle for the 'System Forecast Promotion (Plan+1 Week) Column' to hide it.
    safe_action(shared_page, shared_page.get_by_role("treeitem", name="System Forecast Promotion (Plan+1 Week) Column").get_by_label("Press SPACE to toggle visibility (visible)"), 'uncheck', "Uncheck the visibility toggle for the 'System Forecast Promotion (Plan+1 Week) Column' to hide it.")
    # Click on the column selector in the 7th position to interact with its visibility settings.
    safe_action(shared_page, shared_page.locator("div:nth-child(7) > .ag-column-select-column"), 'click', "Click on the column selector in the 7th position to interact with its visibility settings.")
    # Uncheck the visibility toggle for the '6 Week Aged Net Units Average Column' to hide it.
    safe_action(shared_page, shared_page.get_by_role("treeitem", name="6 Week Aged Net Units Average Column", exact=True).get_by_label("Press SPACE to toggle visibility (visible)"), 'uncheck', "Uncheck the visibility toggle for the '6 Week Aged Net Units Average Column' to hide it.")
    # Uncheck the visibility toggle for the 'LY 6 Week Aged Net Units' column to hide it.
    safe_action(shared_page, shared_page.get_by_role("treeitem", name="LY 6 Week Aged Net Units").get_by_label("Press SPACE to toggle visibility (visible)"), 'uncheck', "Uncheck the visibility toggle for the 'LY 6 Week Aged Net Units' column to hide it.")
    # Click on the column selector in the 11th position to interact with its visibility settings.
    safe_action(shared_page, shared_page.locator("div:nth-child(11) > .ag-column-select-column"), 'click', "Click on the column selector in the 11th position to interact with its visibility settings.")
    # Uncheck the visibility toggle for the '% Change 6 Week Aged Net' column to hide it.
    safe_action(shared_page, shared_page.get_by_role("treeitem", name="% Change 6 Week Aged Net").get_by_label("Press SPACE to toggle visibility (visible)"), 'uncheck', "Uncheck the visibility toggle for the '% Change 6 Week Aged Net' column to hide it.")
    # Uncheck the visibility toggle for the 'LY 6 Week Scan Units Average' column to hide it.
    safe_action(shared_page, shared_page.get_by_role("treeitem", name="LY 6 Week Scan Units Average").get_by_label("Press SPACE to toggle visibility (visible)"), 'uncheck', "Uncheck the visibility toggle for the 'LY 6 Week Scan Units Average' column to hide it.")
    # Uncheck the visibility toggle for the '% Change 6 Week Scan Units' column to hide it.
    safe_action(shared_page, shared_page.get_by_role("treeitem", name="% Change 6 Week Scan Units").get_by_label("Press SPACE to toggle visibility (visible)"), 'uncheck', "Uncheck the visibility toggle for the '% Change 6 Week Scan Units' column to hide it.")
    # Click on the column selector in the 14th position to interact with its visibility settings.
    safe_action(shared_page, shared_page.locator("div:nth-child(14) > .ag-column-select-column"), 'click', "Click on the column selector in the 14th position to interact with its visibility settings.")
    # Uncheck the visibility toggle for the column in the 15th position to hide it.
    safe_action(shared_page, shared_page.locator("div:nth-child(15) > .ag-column-select-column"), 'uncheck', "Uncheck the visibility toggle for the column in the 15th position to hide it.")

@pytest.mark.order(15)
def test_final_column_visibility_toggle(shared_page: Page):
    # Uncheck the visibility toggle for the checkbox controlling column visibility to hide all columns.
    safe_action(shared_page, shared_page.get_by_role("checkbox", name="Press SPACE to toggle visibility (visible)"), 'uncheck', "Uncheck the visibility toggle for the checkbox controlling column visibility to hide all columns.")
    # Check the 'Toggle All Columns Visibility' checkbox to make all columns visible.
    safe_action(shared_page, shared_page.get_by_role("checkbox", name="Toggle All Columns Visibility"), 'check', "Check the 'Toggle All Columns Visibility' checkbox to make all columns visible.")

@pytest.mark.order(16)
def test_export_process(shared_page: Page):
    # Click on the button within the 'Products columns (0)' card to interact with its settings.
    safe_action(shared_page, shared_page.locator("esp-card-component").filter(has_text="Products columns (0)").get_by_role("button"), 'click', "Click on the button within the 'Products columns (0)' card to interact with its settings.")
    # Prepare to capture a download event triggered by the next action.
    with safe_download(shared_page) as download1_info:
    # Click on the export icon to initiate the export process.
        safe_action(shared_page, shared_page.locator("div:nth-child(2) > #export-iconId > .icon-color-toolbar-active"), 'click', "Click on the export icon to initiate the export process.")
    # Store the download information from the export process.
    download1 = download1_info.value

@pytest.mark.order(17)
def test_preferences_management(shared_page: Page):
    # Click on the informational text to acknowledge the export limit message.
    safe_action(shared_page, shared_page.get_by_text("Please note that a maximum of"), 'click', "Click on the informational text to acknowledge the export limit message.")
    # Click on the preferences dropdown to open the preferences menu.
    safe_action(shared_page, shared_page.locator("div:nth-child(3) > #preference-iconId > .legend-font > .multiselect-dropdown > .pointer"), 'click', "Click on the preferences dropdown to open the preferences menu.")
    # Click on 'Save Preference' to save the current settings.
    safe_action(shared_page, shared_page.get_by_text("Save Preference"), 'click', "Click on 'Save Preference' to save the current settings.")
    # Click on the preferences dropdown again to reopen the preferences menu.
    safe_action(shared_page, shared_page.locator("div:nth-child(3) > #preference-iconId > .legend-font > .multiselect-dropdown > .pointer"), 'click', "Click on the preferences dropdown again to reopen the preferences menu.")
    # Click on 'Reset Preference' to reset the settings to their default state.
    safe_action(shared_page, shared_page.get_by_text("Reset Preference"), 'click', "Click on 'Reset Preference' to reset the settings to their default state.")

@pytest.mark.order(18)
def test_grid_interaction(shared_page: Page):
    # Click on the header cell to open the sorting or filtering options for the first column.
    safe_action(shared_page, shared_page.locator(".ag-header-cell.ag-column-first.ag-header-parent-hidden.ag-header-cell-sortable > .ag-header-cell-comp-wrapper > .ag-cell-label-container"), 'click', "Click on the header cell to open the sorting or filtering options for the first column.")
    # Click on the 'Product' text within the grid to select the 'Product' column.
    safe_action(shared_page, shared_page.locator("esp-row-dimentional-grid").get_by_text("Product"), 'click', "Click on the 'Product' text within the grid to select the 'Product' column.")

@pytest.mark.order(19)
def test_product_selection_and_filter_activation(shared_page: Page):
    # Select 'Product 1' from the list of available products.
    safe_action(shared_page, shared_page.get_by_text("Product 1"), 'click', "Select 'Product 1' from the list of available products.")
    # Click on the filter icon in the header to open the filter options for the column.
    safe_action(shared_page, shared_page.locator(".ag-header-icon.ag-header-cell-filter-button > .ag-icon").first, 'click', "Click on the filter icon in the header to open the filter options for the column.")
    # Click on the filter body wrapper to activate the filter input area.
    safe_action(shared_page, shared_page.locator(".ag-filter-body-wrapper"), 'click', "Click on the filter body wrapper to activate the filter input area.")

@pytest.mark.order(20)
def test_filter_operator_selection_and_exploration(shared_page: Page):
    # Open the filtering operator dropdown to select a filter condition.
    safe_action(shared_page, shared_page.get_by_role("combobox", name="Filtering operator"), 'click', "Open the filtering operator dropdown to select a filter condition.")
    # Select the 'Contains' option from the filtering operator dropdown.
    safe_action(shared_page, shared_page.get_by_role("option", name="Contains"), 'click', "Select the 'Contains' option from the filtering operator dropdown.")
    # Click on the 'Contains' text to confirm the selection.
    safe_action(shared_page, shared_page.get_by_text("Contains"), 'click', "Click on the 'Contains' text to confirm the selection.")
    # Click on the 'Does not contain' text to explore or select this filter condition.
    safe_action(shared_page, shared_page.get_by_text("Does not contain"), 'click', "Click on the 'Does not contain' text to explore or select this filter condition.")
    # Reopen the filtering operator dropdown to select another filter condition.
    safe_action(shared_page, shared_page.get_by_role("combobox", name="Filtering operator"), 'click', "Reopen the filtering operator dropdown to select another filter condition.")
    # Select the 'Equals' option from the filtering operator dropdown.
    safe_action(shared_page, shared_page.get_by_role("option", name="Equals"), 'click', "Select the 'Equals' option from the filtering operator dropdown.")
    # Click on the 'Equals' text to confirm the selection.
    safe_action(shared_page, shared_page.get_by_text("Equals"), 'click', "Click on the 'Equals' text to confirm the selection.")
    # Click on the 'Does not equal' text to explore or select this filter condition.
    safe_action(shared_page, shared_page.get_by_text("Does not equal"), 'click', "Click on the 'Does not equal' text to explore or select this filter condition.")
    # Click on the 'Does not equal' text again to confirm or toggle the selection.
    safe_action(shared_page, shared_page.get_by_text("Does not equal"), 'click', "Click on the 'Does not equal' text again to confirm or toggle the selection.")
    # Select the 'Begins with' option from the filtering operator dropdown.
    safe_action(shared_page, shared_page.get_by_role("option", name="Begins with"), 'click', "Select the 'Begins with' option from the filtering operator dropdown.")
    # Click on the 'Begins with' text to confirm the selection.
    safe_action(shared_page, shared_page.get_by_text("Begins with"), 'click', "Click on the 'Begins with' text to confirm the selection.")
    # Select the 'Ends with' option from the filtering operator dropdown.
    safe_action(shared_page, shared_page.get_by_role("option", name="Ends with"), 'click', "Select the 'Ends with' option from the filtering operator dropdown.")
    # Click on the 'Ends with' text to confirm the selection.
    safe_action(shared_page, shared_page.get_by_text("Ends with"), 'click', "Click on the 'Ends with' text to confirm the selection.")
    # Select the 'Blank' option from the filtering operator dropdown.
    safe_action(shared_page, shared_page.get_by_role("option", name="Blank", exact=True), 'click', "Select the 'Blank' option from the filtering operator dropdown.")

@pytest.mark.order(21)
def test_logical_operator_and_filter_reset(shared_page: Page):
    # Click on the 'AND' text to set the logical operator for combining filter conditions.
    safe_action(shared_page, shared_page.get_by_text("AND", exact=True), 'click', "Click on the 'AND' text to set the logical operator for combining filter conditions.")
    # Click on the 'OR' text to set the logical operator for combining filter conditions.
    safe_action(shared_page, shared_page.get_by_text("OR", exact=True), 'click', "Click on the 'OR' text to set the logical operator for combining filter conditions.")
    # Click on the 'Clear' button to remove all applied filters.
    safe_action(shared_page, shared_page.get_by_role("button", name="Clear"), 'click', "Click on the 'Clear' button to remove all applied filters.")
    # Click on the 'Reset' button to reset the filter settings to their default state.
    safe_action(shared_page, shared_page.get_by_role("button", name="Reset"), 'click', "Click on the 'Reset' button to reset the filter settings to their default state.")
    # Click on the filter icon again to close the filter options.
    safe_action(shared_page, shared_page.locator(".ag-header-icon.ag-header-cell-filter-button > .ag-icon").first, 'click', "Click on the filter icon again to close the filter options.")

@pytest.mark.order(22)
def test_filter_application_and_row_selection(shared_page: Page):
    # Click on the 'Apply' button to apply the selected filter conditions.
    safe_action(shared_page, shared_page.get_by_role("button", name="Apply"), 'click', "Click on the 'Apply' button to apply the selected filter conditions.")
    # Click on the first occurrence of the text 'ARNOLD-BRWNBRY-OROWT' within a span element to select the row.
    safe_action(shared_page, shared_page.locator("span").filter(has_text="ARNOLD-BRWNBRY-OROWT").first, 'click', "Click on the first occurrence of the text 'ARNOLD-BRWNBRY-OROWT' within a span element to select the row.")
    # Check the checkbox for the row containing 'ARNOLD-BRWNBRY-OROWT' to toggle its selection.
    safe_action(shared_page, shared_page.get_by_role("gridcell", name="Press Space to toggle row selection (unchecked)  ARNOLD-BRWNBRY-OROWT").get_by_label("Press Space to toggle row"), 'check', "Check the checkbox for the row containing 'ARNOLD-BRWNBRY-OROWT' to toggle its selection.")

@pytest.mark.order(23)
def test_row_context_menu_and_selection_confirmation(shared_page: Page):
    # Right-click on the row containing 'ARNOLD-BRWNBRY-OROWT' to open the context menu.
    safe_action(shared_page, shared_page.locator("esp-row-dimentional-grid span").filter(has_text=re.compile(r"^ARNOLD-BRWNBRY-OROWT$")), 'click', "Right-click on the row containing 'ARNOLD-BRWNBRY-OROWT' to open the context menu.", button="right")
    # Click on the row containing 'ARNOLD-BRWNBRY-OROWT' to select it.
    safe_action(shared_page, shared_page.locator("esp-row-dimentional-grid").get_by_text("ARNOLD-BRWNBRY-OROWT"), 'click', "Click on the row containing 'ARNOLD-BRWNBRY-OROWT' to select it.")
    # Click on the row containing 'ARNOLD-BRWNBRY-OROWT' again, possibly to confirm or toggle the selection.
    safe_action(shared_page, shared_page.locator("esp-row-dimentional-grid").get_by_text("ARNOLD-BRWNBRY-OROWT"), 'click', "Click on the row containing 'ARNOLD-BRWNBRY-OROWT' again, possibly to confirm or toggle the selection.")
    # Click on the span element containing the text 'ARTESANO' to select the corresponding row.
    safe_action(shared_page, shared_page.locator("span").filter(has_text=re.compile(r"^ARTESANO$")), 'click', "Click on the span element containing the text 'ARTESANO' to select the corresponding row.")
    # Click on the text 'ARTESANO' to confirm or highlight the selection.
    safe_action(shared_page, shared_page.get_by_text("ARTESANO"), 'click', "Click on the text 'ARTESANO' to confirm or highlight the selection.")

@pytest.mark.order(24)
def test_row_selection_and_interaction(shared_page: Page):
    # Check the checkbox for the row containing 'ARTESANO' to toggle its selection.
    safe_action(shared_page, shared_page.get_by_role("gridcell", name="Press Space to toggle row selection (unchecked)  ARTESANO").get_by_label("Press Space to toggle row"), 'check', "Check the checkbox for the row containing 'ARTESANO' to toggle its selection.")
    # Double-click on the checkbox within the row to perform an additional action, possibly to confirm selection.
    safe_action(shared_page, shared_page.locator(".ag-cell-value.ag-cell.ag-cell-not-inline-editing.ag-cell-normal-height.ag-cell-last-left-pinned.ag-column-first.no-border.ag-cell-focus > .ag-cell-wrapper > .ag-group-checkbox"), 'dblclick', "Double-click on the checkbox within the row to perform an additional action, possibly to confirm selection.")

@pytest.mark.order(25)
def test_column_header_interaction_and_sorting(shared_page: Page):
    # Click on the text 'System Forecast Total (Plan' to interact with the column header or data.
    safe_action(shared_page, shared_page.get_by_text("System Forecast Total (Plan").nth(3), 'click', "Click on the text 'System Forecast Total (Plan' to interact with the column header or data.")
    # Click on the descending sort icon in the column header to sort the data in descending order.
    safe_action(shared_page, shared_page.locator(".ag-cell-label-container.ag-header-cell-sorted-desc > .ag-header-cell-label > .ag-sort-indicator-container > .ag-sort-indicator-icon.ag-sort-descending-icon > .ag-icon"), 'click', "Click on the descending sort icon in the column header to sort the data in descending order.")
    # Click on the ascending sort icon in the column header to sort the data in ascending order.
    safe_action(shared_page, shared_page.locator(".ag-cell-label-container.ag-header-cell-sorted-asc > .ag-header-cell-label > .ag-sort-indicator-container > .ag-sort-indicator-icon.ag-sort-ascending-icon > .ag-icon"), 'click', "Click on the ascending sort icon in the column header to sort the data in ascending order.")
    # Click on the header icon to interact with the column, possibly to open a menu or perform an action.
    safe_action(shared_page, shared_page.locator(".ag-header-cell.ag-header-parent-hidden.ag-header-cell-sortable.ag-header-background.ag-focus-managed.ag-header-active > .ag-header-cell-comp-wrapper > .ag-cell-label-container > .ag-header-icon > .ag-icon"), 'click', "Click on the header icon to interact with the column, possibly to open a menu or perform an action.")

@pytest.mark.order(26)
def test_filter_menu_interaction(shared_page: Page):
    # Click on the filter body wrapper to open the filter options.
    safe_action(shared_page, shared_page.locator(".ag-filter-body-wrapper"), 'click', "Click on the filter body wrapper to open the filter options.")
    # Click on the combobox labeled 'Filtering operator' to open the dropdown menu.
    safe_action(shared_page, shared_page.get_by_role("combobox", name="Filtering operator"), 'click', "Click on the combobox labeled 'Filtering operator' to open the dropdown menu.")
    # Select the 'Equals' option from the dropdown menu.
    safe_action(shared_page, shared_page.get_by_role("option", name="Equals"), 'click', "Select the 'Equals' option from the dropdown menu.")

@pytest.mark.order(27)
def test_filter_option_selection(shared_page: Page):
    # Click on the text 'Equals' to confirm the selection.
    safe_action(shared_page, shared_page.get_by_text("Equals"), 'click', "Click on the text 'Equals' to confirm the selection.")
    # Select the 'Does not equal' option from the dropdown menu.
    safe_action(shared_page, shared_page.get_by_role("option", name="Does not equal"), 'click', "Select the 'Does not equal' option from the dropdown menu.")
    # Click on the text 'Does not equal' to confirm the selection.
    safe_action(shared_page, shared_page.get_by_text("Does not equal"), 'click', "Click on the text 'Does not equal' to confirm the selection.")
    # Select the 'Greater than' option from the dropdown menu.
    safe_action(shared_page, shared_page.get_by_role("option", name="Greater than", exact=True), 'click', "Select the 'Greater than' option from the dropdown menu.")
    # Click on the text 'Greater than' to confirm the selection.
    safe_action(shared_page, shared_page.get_by_text("Greater than"), 'click', "Click on the text 'Greater than' to confirm the selection.")
    # Click on the text 'Greater than or equal to' to confirm the selection.
    safe_action(shared_page, shared_page.get_by_text("Greater than or equal to"), 'click', "Click on the text 'Greater than or equal to' to confirm the selection.")
    # Click on the text 'Greater than or equal to' again, possibly to confirm or toggle the selection.
    safe_action(shared_page, shared_page.get_by_text("Greater than or equal to"), 'click', "Click on the text 'Greater than or equal to' again, possibly to confirm or toggle the selection.")
    # Select the 'Less than' option from the dropdown menu.
    safe_action(shared_page, shared_page.get_by_role("option", name="Less than", exact=True), 'click', "Select the 'Less than' option from the dropdown menu.")
    # Click on the text 'Less than' to confirm the selection.
    safe_action(shared_page, shared_page.get_by_text("Less than"), 'click', "Click on the text 'Less than' to confirm the selection.")
    # Select the 'Between' option from the dropdown menu.
    safe_action(shared_page, shared_page.get_by_role("option", name="Between"), 'click', "Select the 'Between' option from the dropdown menu.")
    # Click on the text 'Between' to confirm the selection.
    safe_action(shared_page, shared_page.get_by_text("Between"), 'click', "Click on the text 'Between' to confirm the selection.")
    # Select the 'Blank' option from the dropdown menu.
    safe_action(shared_page, shared_page.get_by_role("option", name="Blank", exact=True), 'click', "Select the 'Blank' option from the dropdown menu.")

@pytest.mark.order(28)
def test_logical_operator_and_filter_value_input(shared_page: Page):
    # Click on the text 'AND' to set the logical operator for the filter.
    safe_action(shared_page, shared_page.get_by_text("AND", exact=True), 'click', "Click on the text 'AND' to set the logical operator for the filter.")
    # Click on the text 'OR' to set the logical operator for the filter.
    safe_action(shared_page, shared_page.get_by_text("OR", exact=True), 'click', "Click on the text 'OR' to set the logical operator for the filter.")
    # Click on the spinbutton labeled 'Filter Value' to activate the input field.
    safe_action(shared_page, shared_page.get_by_role("spinbutton", name="Filter Value"), 'click', "Click on the spinbutton labeled 'Filter Value' to activate the input field.")
    # Fill the spinbutton labeled 'Filter Value' with the value '1'.
    safe_action(shared_page, shared_page.get_by_role("spinbutton", name="Filter Value"), 'fill', "Fill the spinbutton labeled 'Filter Value' with the value '1'.", "1")
    # Click on the spinbutton labeled 'Filter Value' again, possibly to confirm the input.
    safe_action(shared_page, shared_page.get_by_role("spinbutton", name="Filter Value"), 'click', "Click on the spinbutton labeled 'Filter Value' again, possibly to confirm the input.")
    # Click on the 'Apply' button to apply the filter settings.
    safe_action(shared_page, shared_page.get_by_role("button", name="Apply"), 'click', "Click on the 'Apply' button to apply the filter settings.")

@pytest.mark.order(29)
def test_filter_application_and_clearing(shared_page: Page):
    # Click on the header cell to interact with the column, possibly to open a menu or perform an action.
    safe_action(shared_page, shared_page.locator(".ag-header-cell.ag-header-parent-hidden.ag-header-cell-sortable.ag-header-background.ag-focus-managed.ag-header-cell-filtered > .ag-header-cell-comp-wrapper > .ag-cell-label-container"), 'click', "Click on the header cell to interact with the column, possibly to open a menu or perform an action.")
    # Click on the filter button in the column header to activate the filter options.
    safe_action(shared_page, shared_page.locator(".ag-header-icon.ag-header-cell-filter-button.ag-filter-active > .ag-icon"), 'click', "Click on the filter button in the column header to activate the filter options.")
    # Click on the 'Clear' button to remove any existing filters.
    safe_action(shared_page, shared_page.get_by_role("button", name="Clear"), 'click', "Click on the 'Clear' button to remove any existing filters.")

@pytest.mark.order(30)
def test_reset_and_column_visibility_configuration_part_1(shared_page: Page):
    # Click on the 'Reset' button to reset the filter settings to their default state.
    safe_action(shared_page, shared_page.get_by_role("button", name="Reset"), 'click', "Click on the 'Reset' button to reset the filter settings to their default state.")
    # Click on the button within the 'Products columns (0)' card to open the column visibility configuration.
    safe_action(shared_page, shared_page.locator("esp-card-component").filter(has_text="Products columns (0)").get_by_role("button"), 'click', "Click on the button within the 'Products columns (0)' card to open the column visibility configuration.")
    # Click on the 'Filter Columns Input' textbox to activate it for entering a search term.
    safe_action(shared_page, shared_page.get_by_role("textbox", name="Filter Columns Input"), 'click', "Click on the 'Filter Columns Input' textbox to activate it for entering a search term.")
    # Uncheck the 'Toggle All Columns Visibility' checkbox to hide all columns.
    safe_action(shared_page, shared_page.get_by_role("checkbox", name="Toggle All Columns Visibility"), 'uncheck', "Uncheck the 'Toggle All Columns Visibility' checkbox to hide all columns.")
    # Check the 'Toggle All Columns Visibility' checkbox to make all columns visible.
    safe_action(shared_page, shared_page.get_by_role("checkbox", name="Toggle All Columns Visibility"), 'check', "Check the 'Toggle All Columns Visibility' checkbox to make all columns visible.")
    # Uncheck the checkbox for the 'System Forecast Total (Plan Week) Column' to hide this specific column.
    safe_action(shared_page, shared_page.get_by_role("treeitem", name="System Forecast Total (Plan Week) Column").get_by_label("Press SPACE to toggle visibility (visible)"), 'uncheck', "Uncheck the checkbox for the 'System Forecast Total (Plan Week) Column' to hide this specific column.")
    # Uncheck the checkbox for the 'System Forecast Base (Plan Week) Column' to hide this specific column.
    safe_action(shared_page, shared_page.get_by_role("treeitem", name="System Forecast Base (Plan Week) Column").get_by_label("Press SPACE to toggle visibility (visible)"), 'uncheck', "Uncheck the checkbox for the 'System Forecast Base (Plan Week) Column' to hide this specific column.")
    # Click on the label for the 'System Forecast Promotion (Plan Week) Column' to interact with or highlight it.
    safe_action(shared_page, shared_page.get_by_label("System Forecast Promotion (Plan Week) Column").get_by_text("System Forecast Promotion ("), 'click', "Click on the label for the 'System Forecast Promotion (Plan Week) Column' to interact with or highlight it.")
    # Click on the label for the 'System Forecast Total (Plan+1)' column to interact with or highlight it.
    safe_action(shared_page, shared_page.get_by_label("System Forecast Total (Plan+1").get_by_text("System Forecast Total (Plan+1"), 'click', "Click on the label for the 'System Forecast Total (Plan+1)' column to interact with or highlight it.")
    # Click on the label for the 'System Forecast Base (Plan+1)' column to interact with or highlight it.
    safe_action(shared_page, shared_page.get_by_label("System Forecast Base (Plan+1").get_by_text("System Forecast Base (Plan+1"), 'click', "Click on the label for the 'System Forecast Base (Plan+1)' column to interact with or highlight it.")
    # Click on the label for the 'System Forecast Promotion (Plan+1 Week) Column' to interact with or highlight it.
    safe_action(shared_page, shared_page.get_by_label("System Forecast Promotion (Plan+1 Week) Column").get_by_text("System Forecast Promotion ("), 'click', "Click on the label for the 'System Forecast Promotion (Plan+1 Week) Column' to interact with or highlight it.")
    # Click on the label for the '6 Week Gross Units Average' column to interact with or highlight it.

@pytest.mark.order(31)
def test_reset_and_column_visibility_configuration_part_2(shared_page: Page):
    safe_action(shared_page, shared_page.get_by_label("6 Week Gross Units Average").get_by_text("Week Gross Units Average"), 'click', "Perform click on page.get_by_label(\"6 Week Gross Units Average\").get_by_text(\"Week Gross Units Average\")")
    # Click on the label for the 'LY 6 Week Aged Net Units' column to interact with or highlight it.
    safe_action(shared_page, shared_page.get_by_label("LY 6 Week Aged Net Units").get_by_text("LY 6 Week Aged Net Units"), 'click', "Click on the label for the 'LY 6 Week Aged Net Units' column to interact with or highlight it.")
    # Click on the label for the '6 Week Aged Net Units Average Column' to interact with or highlight it.
    safe_action(shared_page, shared_page.get_by_label("6 Week Aged Net Units Average Column", exact=True).get_by_text("Week Aged Net Units Average"), 'click', "Click on the label for the '6 Week Aged Net Units Average Column' to interact with or highlight it.")
    # Click on the label for the '6 Week Aged Net Units Average Column' again, possibly to confirm or toggle the selection.
    safe_action(shared_page, shared_page.get_by_label("6 Week Aged Net Units Average Column", exact=True).get_by_text("Week Aged Net Units Average"), 'click', "Click on the label for the '6 Week Aged Net Units Average Column' again, possibly to confirm or toggle the selection.")
    # Click on the label for the '% Change 6 Week Aged Net' column to interact with or highlight it.
    safe_action(shared_page, shared_page.get_by_label("% Change 6 Week Aged Net").get_by_text("% Change 6 Week Aged Net"), 'click', "Click on the label for the '% Change 6 Week Aged Net' column to interact with or highlight it.")
    # Click on the label for the '% Change 6 Week Scan Units' column to interact with or highlight it.
    safe_action(shared_page, shared_page.get_by_label("% Change 6 Week Scan Units").get_by_text("% Change 6 Week Scan Units"), 'click', "Click on the label for the '% Change 6 Week Scan Units' column to interact with or highlight it.")
    # Click on the label for the '6 Week Aged Returns Units' column to interact with or highlight it.
    safe_action(shared_page, shared_page.get_by_label("6 Week Aged Returns Units").get_by_text("6 Week Aged Returns Units"), 'click', "Click on the label for the '6 Week Aged Returns Units' column to interact with or highlight it.")
    # Click on the label for the 'Freshness (6 Week Average)' column to interact with or highlight it.
    safe_action(shared_page, shared_page.get_by_label("Freshness (6 Week Average)").get_by_text("Freshness (6 Week Average)"), 'click', "Click on the label for the 'Freshness (6 Week Average)' column to interact with or highlight it.")
    # Click on the label for the 'LY 6 Week Scan Units Average' column to interact with or highlight it.
    safe_action(shared_page, shared_page.get_by_label("LY 6 Week Scan Units Average").get_by_text("LY 6 Week Scan Units Average"), 'click', "Click on the label for the 'LY 6 Week Scan Units Average' column to interact with or highlight it.")
    # Click on the label for the '6 Week Scan Units Average Column' to interact with or highlight it.
    safe_action(shared_page, shared_page.get_by_label("6 Week Scan Units Average Column", exact=True).get_by_text("Week Scan Units Average"), 'click', "Click on the label for the '6 Week Scan Units Average Column' to interact with or highlight it.")
    # Click on the button within the 'Products columns (0)' card again, possibly to close the column visibility configuration.
    safe_action(shared_page, shared_page.locator("esp-card-component").filter(has_text="Products columns (0)").get_by_role("button"), 'click', "Click on the button within the 'Products columns (0)' card again, possibly to close the column visibility configuration.")

@pytest.mark.order(32)
def test_file_export_process(shared_page: Page):
    # Set up an expectation for a file download to occur during the subsequent action.
    with safe_download(shared_page) as download2_info:
    # Click on the export icon to initiate the export process.
        safe_action(shared_page, shared_page.locator("div:nth-child(2) > #export-iconId > .icon-color-toolbar-active"), 'click', "Click on the export icon to initiate the export process.")
    # Capture the downloaded file information after the export action is triggered.
    download2 = download2_info.value

@pytest.mark.order(33)
def test_preference_management(shared_page: Page):
    # Click on the informational message that notifies the user about the export limit.
    safe_action(shared_page, shared_page.get_by_text("Please note that a maximum of"), 'click', "Click on the informational message that notifies the user about the export limit.")
    # Click on the preference dropdown menu to open the options for managing preferences.
    safe_action(shared_page, shared_page.locator("div:nth-child(3) > #preference-iconId > .legend-font > .multiselect-dropdown > .pointer"), 'click', "Click on the preference dropdown menu to open the options for managing preferences.")
    # Click on the 'Save Preference' option to save the current settings.
    safe_action(shared_page, shared_page.get_by_text("Save Preference"), 'click', "Click on the 'Save Preference' option to save the current settings.")
    # Click on the preference dropdown menu again to reopen the options.
    safe_action(shared_page, shared_page.locator("div:nth-child(3) > #preference-iconId > .legend-font > .multiselect-dropdown > .pointer"), 'click', "Click on the preference dropdown menu again to reopen the options.")
    # Click on the 'Reset Preference' option to reset the settings to their default state.
    safe_action(shared_page, shared_page.get_by_text("Reset Preference"), 'click', "Click on the 'Reset Preference' option to reset the settings to their default state.")

@pytest.mark.order(34)
def test_pagination_interaction_and_navigation(shared_page: Page):
    # Click on the text 'Showing 10 out of 28 123Rows' to interact with the pagination display.
    safe_action(shared_page, shared_page.get_by_text("Showing 10 out of 28 123Rows"), 'click', "Click on the text 'Showing 10 out of 28 123Rows' to interact with the pagination display.")
    # Click on the 'Rows per page View 10 row(s)' dropdown to open the options for changing the number of rows displayed.
    safe_action(shared_page, shared_page.get_by_text("Rows per page View 10 row(s)"), 'click', "Click on the 'Rows per page View 10 row(s)' dropdown to open the options for changing the number of rows displayed.")
    # Click on the option 'View 10 row(s)' to confirm the selection of 10 rows per page.
    safe_action(shared_page, shared_page.locator("span").filter(has_text=re.compile(r"^View 10 row\(s\)$")), 'click', "Click on the option 'View 10 row(s)' to confirm the selection of 10 rows per page.")
    # Click on the text 'Showing 10 out of' to refresh or interact with the pagination display.
    safe_action(shared_page, shared_page.get_by_text("Showing 10 out of"), 'click', "Click on the text 'Showing 10 out of' to refresh or interact with the pagination display.")
    # Click on the first instance of 'View 10 row(s)' to ensure the selection of 10 rows per page.
    safe_action(shared_page, shared_page.get_by_text("View 10 row(s)").first, 'click', "Click on the first instance of 'View 10 row(s)' to ensure the selection of 10 rows per page.")
    # Click on the first instance of 'View 20 row(s)' to change the number of rows displayed to 20.
    safe_action(shared_page, shared_page.locator("div").filter(has_text=re.compile(r"^View 20 row\(s\)$")).first, 'click', "Click on the first instance of 'View 20 row(s)' to change the number of rows displayed to 20.")
    # Click on the text 'Showing 20 out of' to interact with the updated pagination display.
    safe_action(shared_page, shared_page.get_by_text("Showing 20 out of"), 'click', "Click on the text 'Showing 20 out of' to interact with the updated pagination display.")
    # Click on the exact text '12' to navigate to page 12 in the pagination.
    safe_action(shared_page, shared_page.get_by_text("12", exact=True), 'click', "Click on the exact text '12' to navigate to page 12 in the pagination.")
    # Click on the link with the text '2' to navigate to page 2 in the pagination.
    safe_action(shared_page, shared_page.locator("a").filter(has_text="2"), 'click', "Click on the link with the text '2' to navigate to page 2 in the pagination.")
    # Click on the left chevron icon to navigate to the previous page in the pagination.
    safe_action(shared_page, shared_page.locator(".zeb-chevron-left"), 'click', "Click on the left chevron icon to navigate to the previous page in the pagination.")
    # Click on the exact text '12' again to navigate back to page 12.
    safe_action(shared_page, shared_page.get_by_text("12", exact=True), 'click', "Click on the exact text '12' again to navigate back to page 12.")
    # Click on the exact text '12' once more to confirm navigation to page 12.
    safe_action(shared_page, shared_page.get_by_text("12", exact=True), 'click', "Click on the exact text '12' once more to confirm navigation to page 12.")
    # Click on the 'pagination-last' button to navigate to the last page in the pagination.
    safe_action(shared_page, shared_page.locator(".pagination-last"), 'click', "Click on the 'pagination-last' button to navigate to the last page in the pagination.")
    # Click on the 'zeb-nav-to-first' button to navigate back to the first page in the pagination.
    safe_action(shared_page, shared_page.locator(".zeb-nav-to-first"), 'click', "Click on the 'zeb-nav-to-first' button to navigate back to the first page in the pagination.")

@pytest.mark.order(35)
def test_row_selection_and_card_interaction(shared_page: Page):
    # Check the checkbox in the row labeled 'Press Space to toggle row selection (unchecked)' to select the row for 'THOMAS BRANDS'.
    safe_action(shared_page, shared_page.get_by_role("row", name="Press Space to toggle row selection (unchecked)  THOMAS BRANDS").get_by_label("Press Space to toggle row"), 'check', "Check the checkbox in the row labeled 'Press Space to toggle row selection (unchecked)' to select the row for 'THOMAS BRANDS'.")
    # Click on the card content area to interact with the main filter and summary section.
    safe_action(shared_page, shared_page.locator(".card-content.p-24"), 'click', "Click on the card content area to interact with the main filter and summary section.")

@pytest.mark.order(36)
def test_filter_application_and_summary_interaction(shared_page: Page):
    # Click on the text 'FilterTime Latest Order &' to open the filter options.
    safe_action(shared_page, shared_page.get_by_text("FilterTime Latest Order &"), 'click', "Click on the text 'FilterTime Latest Order &' to open the filter options.")
    # Click on the 'Filter' button to apply or modify the filter settings.
    safe_action(shared_page, shared_page.locator("div").filter(has_text=re.compile(r"^Filter$")), 'click', "Click on the 'Filter' button to apply or modify the filter settings.")
    # Click on the 'Time' option to select the time-based filter.
    safe_action(shared_page, shared_page.get_by_text("Time"), 'click', "Click on the 'Time' option to select the time-based filter.")
    # Click on 'Latest Order & Plan Week' to apply this specific filter.
    safe_action(shared_page, shared_page.get_by_text("Latest Order & Plan Week").first, 'click', "Click on 'Latest Order & Plan Week' to apply this specific filter.")
    # Click on 'Daily Summary Product:THOMAS' to view the daily summary for the product 'THOMAS'.
    safe_action(shared_page, shared_page.get_by_text("Daily Summary Product:THOMAS"), 'click', "Click on 'Daily Summary Product:THOMAS' to view the daily summary for the product 'THOMAS'.")
    # Click on 'Daily Summary' to interact with the summary section.
    safe_action(shared_page, shared_page.get_by_text("Daily Summary"), 'click', "Click on 'Daily Summary' to interact with the summary section.")
    # Click on 'Product:THOMAS BRANDS' to focus on the product-specific summary.
    safe_action(shared_page, shared_page.get_by_text("Product:THOMAS BRANDS").first, 'click', "Click on 'Product:THOMAS BRANDS' to focus on the product-specific summary.")
    # Click on the third instance of the exact text 'Product' to refine the selection.
    safe_action(shared_page, shared_page.get_by_text("Product", exact=True).nth(2), 'click', "Click on the third instance of the exact text 'Product' to refine the selection.")
    # Click on the second instance of 'THOMAS BRANDS' to confirm the selection of this product.
    safe_action(shared_page, shared_page.get_by_text("THOMAS BRANDS").nth(1), 'click', "Click on the second instance of 'THOMAS BRANDS' to confirm the selection of this product.")
    # Click on 'Daily Summary Product:THOMAS' again to refresh or interact with the summary.
    safe_action(shared_page, shared_page.get_by_text("Daily Summary Product:THOMAS"), 'click', "Click on 'Daily Summary Product:THOMAS' again to refresh or interact with the summary.")

@pytest.mark.order(37)
def test_dropdown_interaction_and_measure_selection(shared_page: Page):
    # Click on the dropdown to open the multiselect options for filtering.
    safe_action(shared_page, shared_page.locator(".wr-20.font-weight-normal > esp-multiselect-dropdown > .multiselect-dropdown > div > .w-100"), 'click', "Click on the dropdown to open the multiselect options for filtering.")
    # Select the first option in the dropdown list.
    safe_action(shared_page, shared_page.locator(".d-flex.dropdown-option").first, 'click', "Select the first option in the dropdown list.")
    # Select the first option in the dropdown list again, possibly to toggle or confirm the selection.
    safe_action(shared_page, shared_page.locator(".d-flex.dropdown-option").first, 'click', "Select the first option in the dropdown list again, possibly to toggle or confirm the selection.")
    # Click on 'User Suggested Order Total' to select this measure.
    safe_action(shared_page, shared_page.get_by_text("User Suggested Order Total").first, 'click', "Click on 'User Suggested Order Total' to select this measure.")

@pytest.mark.order(38)
def test_measure_selection___user_suggested_and_override(shared_page: Page):
    # Click on the second instance of 'User Suggested Order Base' to select this measure.
    safe_action(shared_page, shared_page.get_by_text("User Suggested Order Base").nth(1), 'click', "Click on the second instance of 'User Suggested Order Base' to select this measure.")
    # Click on the second instance of 'User Suggested Order Promotion' to select this measure.
    safe_action(shared_page, shared_page.get_by_text("User Suggested Order Promotion").nth(1), 'click', "Click on the second instance of 'User Suggested Order Promotion' to select this measure.")
    # Click on the second instance of 'User Override Total' to select this measure.
    safe_action(shared_page, shared_page.get_by_text("User Override Total").nth(1), 'click', "Click on the second instance of 'User Override Total' to select this measure.")
    # Click on the second instance of 'User Override Base' to select this measure.
    safe_action(shared_page, shared_page.get_by_text("User Override Base").nth(1), 'click', "Click on the second instance of 'User Override Base' to select this measure.")

@pytest.mark.order(39)
def test_checkbox_interaction___initial_toggling(shared_page: Page):
    # Click on the first checkbox to select or toggle it.
    safe_action(shared_page, shared_page.locator(".d-flex.flex-column.justify-content-center.font-size-10.align-items-center.checkbox-v2.m-r-10.zeb-check").first, 'click', "Click on the first checkbox to select or toggle it.")
    # Click on the first checkbox again, possibly to toggle or confirm the selection.
    safe_action(shared_page, shared_page.locator(".d-flex.flex-column.justify-content-center.font-size-10.align-items-center.checkbox-v2.m-r-10.zeb-check").first, 'click', "Click on the first checkbox again, possibly to toggle or confirm the selection.")
    # Click on the first checkbox again, possibly to toggle or confirm the selection.
    safe_action(shared_page, shared_page.locator(".d-flex.flex-column.justify-content-center.font-size-10.align-items-center.checkbox-v2.m-r-10.zeb-check").first, 'click', "Click on the first checkbox again, possibly to toggle or confirm the selection.")

@pytest.mark.order(40)
def test_measure_selection___ion_suggested_and_gross_units(shared_page: Page):
    # Click on the second instance of 'ION Suggested Order Promotion' to select this measure.
    safe_action(shared_page, shared_page.get_by_text("ION Suggested Order Promotion").nth(1), 'click', "Click on the second instance of 'ION Suggested Order Promotion' to select this measure.")
    # Click on 'Gross Units (CW-4)' to select this measure.
    safe_action(shared_page, shared_page.get_by_text("Gross Units (CW-4)", exact=True), 'click', "Click on 'Gross Units (CW-4)' to select this measure.")
    # Click on the second instance of 'Gross Units (CW-3)' to select this measure.
    safe_action(shared_page, shared_page.get_by_text("Gross Units (CW-3)").nth(1), 'click', "Click on the second instance of 'Gross Units (CW-3)' to select this measure.")
    # Click on the second instance of 'Aged Net Units (CW-3)' to select this measure.
    safe_action(shared_page, shared_page.get_by_text("Aged Net Units (CW-3)").nth(1), 'click', "Click on the second instance of 'Aged Net Units (CW-3)' to select this measure.")

@pytest.mark.order(41)
def test_dropdown_interaction___deselect_or_modify(shared_page: Page):
    # Click on the first selected dropdown option to deselect or modify the selection.
    safe_action(shared_page, shared_page.locator(".d-flex.dropdown-option.align-items-center.p-v-5.p-l-32.p-r-16.selected").first, 'click', "Click on the first selected dropdown option to deselect or modify the selection.")
    # Click on the first selected dropdown option again, possibly to confirm the deselection or modification.
    safe_action(shared_page, shared_page.locator(".d-flex.dropdown-option.align-items-center.p-v-5.p-l-32.p-r-16.selected").first, 'click', "Click on the first selected dropdown option again, possibly to confirm the deselection or modification.")

@pytest.mark.order(42)
def test_checkbox_interaction___additional_toggling(shared_page: Page):
    # Click on the first checkbox to select or toggle it again.
    safe_action(shared_page, shared_page.locator(".d-flex.flex-column.justify-content-center.font-size-10.align-items-center.checkbox-v2.m-r-10.zeb-check").first, 'click', "Click on the first checkbox to select or toggle it again.")
    # Click on the first checkbox again, possibly to toggle or confirm the selection.
    safe_action(shared_page, shared_page.locator(".d-flex.flex-column.justify-content-center.font-size-10.align-items-center.checkbox-v2.m-r-10.zeb-check").first, 'click', "Click on the first checkbox again, possibly to toggle or confirm the selection.")

@pytest.mark.order(43)
def test_measure_selection___aged_net_and_scan_units(shared_page: Page):
    # Click on 'Aged Net Units (CW-6)' to select this measure.
    safe_action(shared_page, shared_page.get_by_text("Aged Net Units (CW-6)", exact=True), 'click', "Click on 'Aged Net Units (CW-6)' to select this measure.")
    # Click on the first selected dropdown option to deselect or modify the selection.
    safe_action(shared_page, shared_page.locator(".d-flex.dropdown-option.align-items-center.p-v-5.p-l-32.p-r-16.selected").first, 'click', "Click on the first selected dropdown option to deselect or modify the selection.")
    # Click on 'Scan Units (CW-4)' to select this measure.
    safe_action(shared_page, shared_page.get_by_text("Scan Units (CW-4)", exact=True), 'click', "Click on 'Scan Units (CW-4)' to select this measure.")
    # Click on 'Scan Units (CW-4)' again, possibly to confirm or toggle the selection.
    safe_action(shared_page, shared_page.get_by_text("Scan Units (CW-4)", exact=True), 'click', "Click on 'Scan Units (CW-4)' again, possibly to confirm or toggle the selection.")

@pytest.mark.order(44)
def test_child_element_selection___overflow_container(shared_page: Page):
    # Click on the 21st child element within the overflow container, possibly to select a specific option.
    safe_action(shared_page, shared_page.locator(".overflow-auto > div:nth-child(21)"), 'click', "Click on the 21st child element within the overflow container, possibly to select a specific option.")
    # Click on the 20th child element with the specified class, possibly to select another option.
    safe_action(shared_page, shared_page.locator("div:nth-child(20) > .d-flex"), 'click', "Click on the 20th child element with the specified class, possibly to select another option.")

@pytest.mark.order(45)
def test_measure_selection___scan_units_and_select_all(shared_page: Page):
    # Click on the first instance of 'Scan Units (CW-4)' to select this measure.
    safe_action(shared_page, shared_page.get_by_text("Scan Units (CW-4)").first, 'click', "Click on the first instance of 'Scan Units (CW-4)' to select this measure.")
    # Click on the first instance of 'Scan Units (CW-4)' again, possibly to confirm or toggle the selection.
    safe_action(shared_page, shared_page.get_by_text("Scan Units (CW-4)").first, 'click', "Click on the first instance of 'Scan Units (CW-4)' again, possibly to confirm or toggle the selection.")
    # Click on 'Select All' to select all available measures in the dropdown.
    safe_action(shared_page, shared_page.get_by_text("Select All"), 'click', "Click on 'Select All' to select all available measures in the dropdown.")

@pytest.mark.order(46)
def test_interaction_with__all__and_daily_summary_card(shared_page: Page):
    # Click on the fourth instance of the 'All' text to select or interact with it.
    safe_action(shared_page, shared_page.get_by_text("All").nth(4), 'click', "Click on the fourth instance of the 'All' text to select or interact with it.")
    # Click on the button within the 'Daily Summary Product:THOMAS' card to expand or interact with it.
    safe_action(shared_page, shared_page.locator("esp-card-component").filter(has_text="Daily Summary Product:THOMAS").get_by_role("button"), 'click', "Click on the button within the 'Daily Summary Product:THOMAS' card to expand or interact with it.")

@pytest.mark.order(47)
def test_filter_columns_input_and_column_selection(shared_page: Page):
    # Click on the 'Filter Columns Input' textbox to focus on it.
    safe_action(shared_page, shared_page.get_by_role("textbox", name="Filter Columns Input"), 'click', "Click on the 'Filter Columns Input' textbox to focus on it.")
    # Fill the 'Filter Columns Input' textbox with the value '02/1' to filter columns based on this input.
    safe_action(shared_page, shared_page.get_by_role("textbox", name="Filter Columns Input"), 'fill', "Fill the 'Filter Columns Input' textbox with the value '02/1' to filter columns based on this input.", "02/1")
    # Click on the first column in the filtered list to select it.
    safe_action(shared_page, shared_page.locator("#ag-4958 > .ag-column-panel > .ag-column-select > .ag-column-select-list > .ag-virtual-list-viewport > .ag-virtual-list-container > div > .ag-column-select-column").first, 'click', "Click on the first column in the filtered list to select it.")

@pytest.mark.order(48)
def test_column_visibility_toggle(shared_page: Page):
    # Uncheck the visibility toggle for the '/11(Wed) Column' to hide it.
    safe_action(shared_page, shared_page.get_by_role("treeitem", name="/11(Wed) Column").get_by_label("Press SPACE to toggle visibility (visible)"), 'uncheck', "Uncheck the visibility toggle for the '/11(Wed) Column' to hide it.")

@pytest.mark.order(49)
def test_column_visibility_management(shared_page: Page):
    # Uncheck the visibility toggle for the '/12(Thu) Column' to hide it.
    safe_action(shared_page, shared_page.get_by_role("treeitem", name="/12(Thu) Column").get_by_label("Press SPACE to toggle visibility (visible)"), 'uncheck', "Uncheck the visibility toggle for the '/12(Thu) Column' to hide it.")
    # Check the 'Toggle All Columns Visibility' checkbox to make all columns visible.
    safe_action(shared_page, shared_page.get_by_role("checkbox", name="Toggle All Columns Visibility"), 'check', "Check the 'Toggle All Columns Visibility' checkbox to make all columns visible.")
    # Click on the 'Filter Columns Input' textbox again to focus on it.
    safe_action(shared_page, shared_page.get_by_role("textbox", name="Filter Columns Input"), 'click', "Click on the 'Filter Columns Input' textbox again to focus on it.")
    # Clear the 'Filter Columns Input' textbox by filling it with an empty string.
    safe_action(shared_page, shared_page.get_by_role("textbox", name="Filter Columns Input"), 'fill', "Clear the 'Filter Columns Input' textbox by filling it with an empty string.", "")
    # Press 'Enter' in the 'Filter Columns Input' textbox to apply the filter or finalize the action.
    safe_action(shared_page, shared_page.get_by_role("textbox", name="Filter Columns Input"), 'press', "Press 'Enter' in the 'Filter Columns Input' textbox to apply the filter or finalize the action.", "Enter")

@pytest.mark.order(50)
def test_daily_summary_product_interaction(shared_page: Page):
    # Click on the button within the 'Daily Summary Product:THOMAS' card to expand or interact with it.
    safe_action(shared_page, shared_page.locator("esp-card-component").filter(has_text="Daily Summary Product:THOMAS").get_by_role("button"), 'click', "Click on the button within the 'Daily Summary Product:THOMAS' card to expand or interact with it.")
    # Click on the button within the 'Daily Summary Product:THOMAS' card again, possibly to toggle or confirm the action.
    safe_action(shared_page, shared_page.locator("esp-card-component").filter(has_text="Daily Summary Product:THOMAS").get_by_role("button"), 'click', "Click on the button within the 'Daily Summary Product:THOMAS' card again, possibly to toggle or confirm the action.")

@pytest.mark.order(51)
def test_toggle_individual_column_visibility(shared_page: Page):
    # Check the visibility toggle for the '/01(Sun) Column' to make it visible.
    safe_action(shared_page, shared_page.get_by_role("treeitem", name="/01(Sun) Column").get_by_label("Press SPACE to toggle visibility (hidden)"), 'check', "Check the visibility toggle for the '/01(Sun) Column' to make it visible.")
    # Check the visibility toggle for the '/02(Mon) Column' to make it visible.
    safe_action(shared_page, shared_page.get_by_role("treeitem", name="/02(Mon) Column").get_by_label("Press SPACE to toggle visibility (hidden)"), 'check', "Check the visibility toggle for the '/02(Mon) Column' to make it visible.")
    # Check the visibility toggle for the '/03(Tue) Column' to make it visible.
    safe_action(shared_page, shared_page.get_by_role("treeitem", name="/03(Tue) Column").get_by_label("Press SPACE to toggle visibility (hidden)"), 'check', "Check the visibility toggle for the '/03(Tue) Column' to make it visible.")
    # Check the visibility toggle for the '/04(Wed) Column' to make it visible.
    safe_action(shared_page, shared_page.get_by_role("treeitem", name="/04(Wed) Column").get_by_label("Press SPACE to toggle visibility (hidden)"), 'check', "Check the visibility toggle for the '/04(Wed) Column' to make it visible.")
    # Check the visibility toggle for the '/05(Thu) Column' to make it visible.
    safe_action(shared_page, shared_page.get_by_role("treeitem", name="/05(Thu) Column").get_by_label("Press SPACE to toggle visibility (hidden)"), 'check', "Check the visibility toggle for the '/05(Thu) Column' to make it visible.")
    # Check the visibility toggle for the '/06(Fri) Column' to make it visible.
    safe_action(shared_page, shared_page.get_by_role("treeitem", name="/06(Fri) Column").get_by_label("Press SPACE to toggle visibility (hidden)"), 'check', "Check the visibility toggle for the '/06(Fri) Column' to make it visible.")
    # Check the visibility toggle for the '/07(Sat) Column' to make it visible.
    safe_action(shared_page, shared_page.get_by_role("treeitem", name="/07(Sat) Column").get_by_label("Press SPACE to toggle visibility (hidden)"), 'check', "Check the visibility toggle for the '/07(Sat) Column' to make it visible.")
    # Check the visibility toggle for the '/08(Sun) Column' to make it visible.
    safe_action(shared_page, shared_page.get_by_role("treeitem", name="/08(Sun) Column").get_by_label("Press SPACE to toggle visibility (hidden)"), 'check', "Check the visibility toggle for the '/08(Sun) Column' to make it visible.")
    # Check the visibility toggle for the '/09(Mon) Column' to make it visible.
    safe_action(shared_page, shared_page.get_by_role("treeitem", name="/09(Mon) Column").get_by_label("Press SPACE to toggle visibility (hidden)"), 'check', "Check the visibility toggle for the '/09(Mon) Column' to make it visible.")
    # Click on the column element located at 'div:nth-child(10) > .ag-column-select-column' to interact with it.
    safe_action(shared_page, shared_page.locator("div:nth-child(10) > .ag-column-select-column"), 'click', "Click on the column element located at 'div:nth-child(10) > .ag-column-select-column' to interact with it.")
    # Check the visibility toggle for the '/11(Wed) Column' to make it visible.
    safe_action(shared_page, shared_page.get_by_role("treeitem", name="/11(Wed) Column").get_by_label("Press SPACE to toggle visibility (hidden)"), 'check', "Check the visibility toggle for the '/11(Wed) Column' to make it visible.")
    # Check the visibility toggle for the '/12(Thu) Column' to make it visible.
    safe_action(shared_page, shared_page.get_by_role("treeitem", name="/12(Thu) Column").get_by_label("Press SPACE to toggle visibility (hidden)"), 'check', "Check the visibility toggle for the '/12(Thu) Column' to make it visible.")
    # Check the visibility toggle for the '/13(Fri) Column' to make it visible.
    safe_action(shared_page, shared_page.get_by_role("treeitem", name="/13(Fri) Column").get_by_label("Press SPACE to toggle visibility (hidden)"), 'check', "Check the visibility toggle for the '/13(Fri) Column' to make it visible.")

@pytest.mark.order(52)
def test_toggle_all_columns_visibility(shared_page: Page):
    # Check the 'Toggle All Columns Visibility' checkbox to make all columns visible.
    safe_action(shared_page, shared_page.get_by_role("checkbox", name="Press SPACE to toggle visibility (hidden)"), 'check', "Check the 'Toggle All Columns Visibility' checkbox to make all columns visible.")

@pytest.mark.order(53)
def test_daily_summary_product_re_interaction(shared_page: Page):
    # Click on the button within the 'Daily Summary Product:THOMAS' card to expand or interact with it.
    safe_action(shared_page, shared_page.locator("esp-card-component").filter(has_text="Daily Summary Product:THOMAS").get_by_role("button"), 'click', "Click on the button within the 'Daily Summary Product:THOMAS' card to expand or interact with it.")

@pytest.mark.order(54)
def test_export_process(shared_page: Page):
    # Click on the export icon to initiate the export process.
    safe_action(shared_page, shared_page.locator("span:nth-child(6) > esp-grid-icons-component > .display-grid-icons > div:nth-child(2) > #export-iconId > .icon-color-toolbar-active"), 'click', "Click on the export icon to initiate the export process.")
    # Set up an expectation to handle a file download triggered by the next action.
    with safe_download(shared_page) as download3_info:
    # Click on the text element that provides information about the export limit.
        safe_action(shared_page, shared_page.get_by_text("Please note that a maximum of"), 'click', "Click on the text element that provides information about the export limit.")
    # Store the downloaded file information for further use or validation.
    download3 = download3_info.value

@pytest.mark.order(55)
def test_preference_management(shared_page: Page):
    # Click on the preference icon to open the preferences dropdown menu.
    safe_action(shared_page, shared_page.locator("span:nth-child(6) > esp-grid-icons-component > .display-grid-icons > div:nth-child(3) > #preference-iconId > .legend-font > .multiselect-dropdown > .pointer"), 'click', "Click on the preference icon to open the preferences dropdown menu.")
    # Click on the 'Save Preference' option to save the current preferences.
    safe_action(shared_page, shared_page.locator("div").filter(has_text=re.compile(r"^Save Preference$")).first, 'click', "Click on the 'Save Preference' option to save the current preferences.")
    # Click on the preference icon again to reopen the preferences dropdown menu.
    safe_action(shared_page, shared_page.locator("span:nth-child(6) > esp-grid-icons-component > .display-grid-icons > div:nth-child(3) > #preference-iconId > .legend-font > .multiselect-dropdown > .pointer"), 'click', "Click on the preference icon again to reopen the preferences dropdown menu.")
    # Click on the 'Reset Preference' option to reset the preferences to default.
    safe_action(shared_page, shared_page.locator("div").filter(has_text=re.compile(r"^Reset Preference$")).first, 'click', "Click on the 'Reset Preference' option to reset the preferences to default.")

@pytest.mark.order(56)
def test_grid_header_and_column_interactions(shared_page: Page):
    # Click on the header cell to interact with the first column in the grid.
    safe_action(shared_page, shared_page.locator(".ag-header-cell.ag-column-first.ag-header-parent-hidden.ag-header-background.ag-focus-managed.ag-header-active > .ag-header-cell-comp-wrapper > .ag-cell-label-container > .ag-header-cell-label"), 'click', "Click on the header cell to interact with the first column in the grid.")
    # Click on the 'User Suggested Order Total' text to select or interact with it.
    safe_action(shared_page, shared_page.get_by_text("User Suggested Order Total"), 'click', "Click on the 'User Suggested Order Total' text to select or interact with it.")
    # Click on the first icon within the grid, possibly to open a filter or perform an action.
    safe_action(shared_page, shared_page.locator("i").first, 'click', "Click on the first icon within the grid, possibly to open a filter or perform an action.")
    # Click on the 'User Override Total' text to select or interact with it.
    safe_action(shared_page, shared_page.get_by_text("User Override Total"), 'click', "Click on the 'User Override Total' text to select or interact with it.")
    # Click on the grid cell labeled 'User Override Total' to interact with it.
    safe_action(shared_page, shared_page.get_by_role("gridcell", name=" User Override Total"), 'click', "Click on the grid cell labeled 'User Override Total' to interact with it.")
    # Click on the second icon within the grid, possibly to open a filter or perform an action.
    safe_action(shared_page, shared_page.locator("i").nth(2), 'click', "Click on the second icon within the grid, possibly to open a filter or perform an action.")
    # Click on the 'Gross Units (CW-3)' text within the grid to select or interact with it.
    safe_action(shared_page, shared_page.locator("esp-column-dimentional-grid").get_by_text("Gross Units (CW-3)"), 'click', "Click on the 'Gross Units (CW-3)' text within the grid to select or interact with it.")

@pytest.mark.order(57)
def test_grid_chevron_and_text_interactions(shared_page: Page):
    # Click on the fifth icon within the grid, possibly to open a filter or perform an action.
    safe_action(shared_page, shared_page.locator("i").nth(5), 'click', "Click on the fifth icon within the grid, possibly to open a filter or perform an action.")
    # Click on the 'Aged Net Units (CW-3)' text within the grid to select or interact with it.
    safe_action(shared_page, shared_page.locator("esp-column-dimentional-grid").get_by_text("Aged Net Units (CW-3)"), 'click', "Click on the 'Aged Net Units (CW-3)' text within the grid to select or interact with it.")
    # Click on the chevron icon to expand or collapse a group within the grid.
    safe_action(shared_page, shared_page.locator(".ag-cell-value.ag-cell.ag-cell-not-inline-editing.ag-cell-normal-height.ag-cell-last-left-pinned.ag-column-first.ag-cell-override-normal.notosans-overwrite.no-border.ag-cell-focus > .ag-cell-wrapper > .ag-group-contracted > .zeb-chevron-right"), 'click', "Click on the chevron icon to expand or collapse a group within the grid.")
    # Click on the 'Scan Units (CW-3)' text within the grid to select or interact with it.
    safe_action(shared_page, shared_page.locator("esp-column-dimentional-grid").get_by_text("Scan Units (CW-3)"), 'click', "Click on the 'Scan Units (CW-3)' text within the grid to select or interact with it.")
    # Click on the chevron icon again to expand or collapse another group within the grid.
    safe_action(shared_page, shared_page.locator(".ag-cell-value.ag-cell.ag-cell-not-inline-editing.ag-cell-normal-height.ag-cell-last-left-pinned.ag-column-first.ag-cell-override-normal.notosans-overwrite.no-border.ag-cell-focus > .ag-cell-wrapper > .ag-group-contracted > .zeb-chevron-right"), 'click', "Click on the chevron icon again to expand or collapse another group within the grid.")

@pytest.mark.order(58)
def test_daily_trend_and_line_bar_chart_interactions(shared_page: Page):
    # Click on the 'Daily Trend Product:THOMAS' text to navigate or interact with it.
    safe_action(shared_page, shared_page.get_by_text("Daily Trend Product:THOMAS"), 'click', "Click on the 'Daily Trend Product:THOMAS' text to navigate or interact with it.")
    # Click on the 'Daily Trend' text to navigate or interact with it.
    safe_action(shared_page, shared_page.get_by_text("Daily Trend"), 'click', "Click on the 'Daily Trend' text to navigate or interact with it.")
    # Click on the 'Product:THOMAS BRANDS' text within the line-bar chart to interact with it.
    safe_action(shared_page, shared_page.locator("dp-line-bar-chart").get_by_text("Product:THOMAS BRANDS"), 'click', "Click on the 'Product:THOMAS BRANDS' text within the line-bar chart to interact with it.")
    # Click on the 'Product' text within the line-bar chart to interact with it.
    safe_action(shared_page, shared_page.locator("dp-line-bar-chart").get_by_text("Product", exact=True), 'click', "Click on the 'Product' text within the line-bar chart to interact with it.")
    # Click on the 'THOMAS BRANDS' text within the line-bar chart to interact with it.
    safe_action(shared_page, shared_page.locator("dp-line-bar-chart").get_by_text("THOMAS BRANDS"), 'click', "Click on the 'THOMAS BRANDS' text within the line-bar chart to interact with it.")

@pytest.mark.order(59)
def test_dropdown_and_filter_selections(shared_page: Page):
    # Click on the dropdown caret within the multiselect dropdown to open the filter options.
    safe_action(shared_page, shared_page.locator(".ellipses > esp-multiselect-dropdown > .multiselect-dropdown > div > .w-100 > .d-flex.align-items-center > .dropdown-caret"), 'click', "Click on the dropdown caret within the multiselect dropdown to open the filter options.")
    # Select the 'User Suggested Order Base' option from the dropdown.
    safe_action(shared_page, shared_page.locator("span").filter(has_text="User Suggested Order Base"), 'click', "Select the 'User Suggested Order Base' option from the dropdown.")
    # Select the 'User Suggested Order Promotion' option from the dropdown.
    safe_action(shared_page, shared_page.locator("span").filter(has_text="User Suggested Order Promotion"), 'click', "Select the 'User Suggested Order Promotion' option from the dropdown.")
    # Select the 'User Override Base' option from the dropdown.
    safe_action(shared_page, shared_page.locator("span").filter(has_text="User Override Base"), 'click', "Select the 'User Override Base' option from the dropdown.")
    # Select the 'User Override Promotion' option from the dropdown.
    safe_action(shared_page, shared_page.locator("span").filter(has_text="User Override Promotion"), 'click', "Select the 'User Override Promotion' option from the dropdown.")

@pytest.mark.order(60)
def test_line_bar_chart_and_grid_element_interactions(shared_page: Page):
    # Click on the 'Gross Units (CW-3)' text within the line-bar chart to interact with it.
    safe_action(shared_page, shared_page.locator("dp-line-bar-chart span").filter(has_text="Gross Units (CW-3)"), 'click', "Click on the 'Gross Units (CW-3)' text within the line-bar chart to interact with it.")
    # Click on the 'Gross Units (CW-4)' text within the line-bar chart to interact with it.
    safe_action(shared_page, shared_page.locator("dp-line-bar-chart").get_by_text("Gross Units (CW-4)"), 'click', "Click on the 'Gross Units (CW-4)' text within the line-bar chart to interact with it.")
    # Click on the seventh element in the grid, possibly to interact with a specific data point or group.
    safe_action(shared_page, shared_page.locator("div:nth-child(7) > .d-flex"), 'click', "Click on the seventh element in the grid, possibly to interact with a specific data point or group.")
    # Click on the eighth element in the grid, possibly to interact with a specific data point or group.
    safe_action(shared_page, shared_page.locator("div:nth-child(8) > .d-flex"), 'click', "Click on the eighth element in the grid, possibly to interact with a specific data point or group.")
    # Click on the ninth element in the grid, possibly to interact with a specific data point or group.
    safe_action(shared_page, shared_page.locator("div:nth-child(9) > .d-flex"), 'click', "Click on the ninth element in the grid, possibly to interact with a specific data point or group.")
    # Click on the tenth element in the grid, possibly to interact with a specific data point or group.
    safe_action(shared_page, shared_page.locator("div:nth-child(10) > .d-flex"), 'click', "Click on the tenth element in the grid, possibly to interact with a specific data point or group.")
    # Click on the eleventh element in the grid, possibly to interact with a specific data point or group.
    safe_action(shared_page, shared_page.locator("div:nth-child(11) > .d-flex"), 'click', "Click on the eleventh element in the grid, possibly to interact with a specific data point or group.")
    # Click on the twelfth element in the grid, possibly to interact with a specific data point or group.
    safe_action(shared_page, shared_page.locator("div:nth-child(12) > .d-flex"), 'click', "Click on the twelfth element in the grid, possibly to interact with a specific data point or group.")

@pytest.mark.order(61)
def test_interaction_with_line_bar_chart_elements(shared_page: Page):
    # Click on the 'Scan Units (CW-3)' text within the line-bar chart to interact with it.
    safe_action(shared_page, shared_page.locator("dp-line-bar-chart span").filter(has_text="Scan Units (CW-3)"), 'click', "Click on the 'Scan Units (CW-3)' text within the line-bar chart to interact with it.")
    # Click on the 'Scan Units (CW-4)' text within the line-bar chart to interact with it.
    safe_action(shared_page, shared_page.locator("dp-line-bar-chart").get_by_text("Scan Units (CW-4)"), 'click', "Click on the 'Scan Units (CW-4)' text within the line-bar chart to interact with it.")
    # Click on the 'Scan Units (CW-5)' text within the line-bar chart to interact with it.
    safe_action(shared_page, shared_page.locator("dp-line-bar-chart").get_by_text("Scan Units (CW-5)"), 'click', "Click on the 'Scan Units (CW-5)' text within the line-bar chart to interact with it.")
    # Click on the 'Scan Units (CW-6)' text within the line-bar chart to interact with it.
    safe_action(shared_page, shared_page.locator("dp-line-bar-chart").get_by_text("Scan Units (CW-6)"), 'click', "Click on the 'Scan Units (CW-6)' text within the line-bar chart to interact with it.")

@pytest.mark.order(62)
def test_preference_management_actions(shared_page: Page):
    # Click on the 'Gross Units (CW-4), Gross' text to interact with it, possibly to select or highlight it.
    safe_action(shared_page, shared_page.get_by_text("Gross Units (CW-4), Gross").first, 'click', "Click on the 'Gross Units (CW-4), Gross' text to interact with it, possibly to select or highlight it.")
    # Click on the multiselect dropdown within the preference icon container to open the preference options.
    safe_action(shared_page, shared_page.locator(".title.d-flex.align-items-center.font-size-16.font-weight-bold.nunito.title-color > .grid-icons-container > esp-grid-icons-component > .display-grid-icons > div > #preference-iconId > .legend-font > .multiselect-dropdown > .pointer"), 'click', "Click on the multiselect dropdown within the preference icon container to open the preference options.")
    # Click on 'Save Preference' to save the current settings or selections.
    safe_action(shared_page, shared_page.get_by_text("Save Preference"), 'click', "Click on 'Save Preference' to save the current settings or selections.")
    # Click on the multiselect dropdown within the preference icon container again, possibly to access additional options.
    safe_action(shared_page, shared_page.locator(".title.d-flex.align-items-center.font-size-16.font-weight-bold.nunito.title-color > .grid-icons-container > esp-grid-icons-component > .display-grid-icons > div > #preference-iconId > .legend-font > .multiselect-dropdown > .pointer"), 'click', "Click on the multiselect dropdown within the preference icon container again, possibly to access additional options.")
    # Click on 'Reset Preference' to reset the preferences to their default state.
    safe_action(shared_page, shared_page.get_by_text("Reset Preference"), 'click', "Click on 'Reset Preference' to reset the preferences to their default state.")

@pytest.mark.order(63)
def test_table_interaction_actions(shared_page: Page):
    # Click on the element identified by 'path:nth-child(81)', possibly to interact with a specific UI component. The exact purpose is unclear from the locator.
    safe_action(shared_page, shared_page.locator("path:nth-child(81)"), 'click', "Click on the element identified by 'path:nth-child(81)', possibly to interact with a specific UI component. The exact purpose is unclear from the locator.")
    # Click on the 'User Override Base' text to select or highlight this option in the table.
    safe_action(shared_page, shared_page.get_by_text("User Override Base", exact=True), 'click', "Click on the 'User Override Base' text to select or highlight this option in the table.")
    # Click on the 'User Suggested Order Promotion' text to select or highlight this option in the table.
    safe_action(shared_page, shared_page.get_by_text("User Suggested Order Promotion", exact=True), 'click', "Click on the 'User Suggested Order Promotion' text to select or highlight this option in the table.")
    # Click on the 'User Override Base' text again, possibly to toggle or reselect this option.
    safe_action(shared_page, shared_page.get_by_text("User Override Base", exact=True), 'click', "Click on the 'User Override Base' text again, possibly to toggle or reselect this option.")
    # Click on the 'User Suggested Order Promotion' text again, possibly to toggle or reselect this option.
    safe_action(shared_page, shared_page.get_by_text("User Suggested Order Promotion", exact=True), 'click', "Click on the 'User Suggested Order Promotion' text again, possibly to toggle or reselect this option.")

@pytest.mark.order(64)
def test_chart_and_graph_interactions(shared_page: Page):
    # Click on the SVG element, possibly to interact with a chart or graph. The exact purpose is unclear from the locator.
    safe_action(shared_page, shared_page.locator("svg"), 'click', "Click on the SVG element, possibly to interact with a chart or graph. The exact purpose is unclear from the locator.")
    # Click on the SVG element again, likely to perform a secondary interaction with the chart or graph.
    safe_action(shared_page, shared_page.locator("svg"), 'click', "Click on the SVG element again, likely to perform a secondary interaction with the chart or graph.")
    # Click on the date '02/03/2026' in the chart to select or highlight data associated with this specific date.
    safe_action(shared_page, shared_page.get_by_text("02/03/2026", exact=True), 'click', "Click on the date '02/03/2026' in the chart to select or highlight data associated with this specific date.")
    # Click on the text '300K', likely to select or highlight data associated with this value in the chart.
    safe_action(shared_page, shared_page.get_by_text("300K"), 'click', "Click on the text '300K', likely to select or highlight data associated with this value in the chart.")
    # Click on the text '600K', likely to select or highlight data associated with this value in the chart.
    safe_action(shared_page, shared_page.get_by_text("600K"), 'click', "Click on the text '600K', likely to select or highlight data associated with this value in the chart.")
    # Click on the bar chart element corresponding to 'path:nth-child(57)', likely to highlight or interact with a specific data point in the chart.
    safe_action(shared_page, shared_page.locator("path:nth-child(57)"), 'click', "Click on the bar chart element corresponding to 'path:nth-child(57)', likely to highlight or interact with a specific data point in the chart.")
    # Repeat the click action on the same bar chart element ('path:nth-child(57)'), possibly to ensure the interaction is registered.
    safe_action(shared_page, shared_page.locator("path:nth-child(57)"), 'click', "Repeat the click action on the same bar chart element ('path:nth-child(57)'), possibly to ensure the interaction is registered.")
    # Click on the bar chart element corresponding to 'path:nth-child(99)', likely to highlight or interact with another specific data point in the chart.
    safe_action(shared_page, shared_page.locator("path:nth-child(99)"), 'click', "Click on the bar chart element corresponding to 'path:nth-child(99)', likely to highlight or interact with another specific data point in the chart.")
    # Click on the bar chart element corresponding to 'path:nth-child(98)', likely to highlight or interact with yet another specific data point in the chart.
    safe_action(shared_page, shared_page.locator("path:nth-child(98)"), 'click', "Click on the bar chart element corresponding to 'path:nth-child(98)', likely to highlight or interact with yet another specific data point in the chart.")

