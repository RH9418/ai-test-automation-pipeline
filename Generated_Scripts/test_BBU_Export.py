
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


@pytest.mark.order(3)
def test_page_navigation(shared_page: Page):
    # Navigate to the specified URL, which appears to be the Executive Dashboard in the Demand Planning module.
    safe_action(shared_page, shared_page, 'goto', "Navigate to the specified URL, which appears to be the Executive Dashboard in the Demand Planning module.", "https://stage.bbu.esp.antuit.ai/dp/demand-planning/executive-dashboard?workbookId=4&tabIndex=7")
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
def test_filter_interaction(shared_page: Page):
    # Click on the 'FilterStart Week 01/25/2026' text to open the filter configuration.
    safe_action(shared_page, shared_page.get_by_text("FilterStart Week 01/25/2026"), 'click', "Click on the 'FilterStart Week 01/25/2026' text to open the filter configuration.")
    # Click on the 'Filter' text to expand the filter options.
    safe_action(shared_page, shared_page.get_by_text("Filter"), 'click', "Click on the 'Filter' text to expand the filter options.")
    # Click on 'Start Week / End Week' to open the date range selection.
    safe_action(shared_page, shared_page.get_by_text("Start Week / End Week"), 'click', "Click on 'Start Week / End Week' to open the date range selection.")

@pytest.mark.order(5)
def test_date_picker_interaction(shared_page: Page):
    # Click on the date picker input field to open the calendar widget.
    safe_action(shared_page, shared_page.locator("#Datepick"), 'click', "Click on the date picker input field to open the calendar widget.")
    # Select the month and year header displaying '‹ January 2026 ›' to navigate the calendar.
    safe_action(shared_page, shared_page.locator("div").filter(has_text="‹ January 2026 ›").nth(4), 'click', "Select the month and year header displaying '‹ January 2026 ›' to navigate the calendar.")
    # Click on the first occurrence of the date '4' in the calendar to select it.
    safe_action(shared_page, shared_page.get_by_text("4").first, 'click', "Click on the first occurrence of the date '4' in the calendar to select it.")
    # Click on the 'January' button to open the month selection dropdown.
    safe_action(shared_page, shared_page.get_by_role("button", name="January"), 'click', "Click on the 'January' button to open the month selection dropdown.")
    # Select 'February' from the month dropdown.
    safe_action(shared_page, shared_page.get_by_text("February").first, 'click', "Select 'February' from the month dropdown.")
    # Click on the '2026' button to open the year selection dropdown.
    safe_action(shared_page, shared_page.get_by_role("button", name="2026").first, 'click', "Click on the '2026' button to open the year selection dropdown.")
    # Select the year '2025' from the year grid.
    safe_action(shared_page, shared_page.get_by_role("gridcell", name="2025"), 'click', "Select the year '2025' from the year grid.")
    # Click on the '2026' button to return to the year selection dropdown.
    safe_action(shared_page, shared_page.get_by_role("button", name="2026"), 'click', "Click on the '2026' button to return to the year selection dropdown.")
    # Select the year '2024' from the year grid.
    safe_action(shared_page, shared_page.get_by_role("gridcell", name="2024"), 'click', "Select the year '2024' from the year grid.")
    # Select the second occurrence of 'January' from the month grid.
    safe_action(shared_page, shared_page.get_by_role("gridcell", name="January").nth(1), 'click', "Select the second occurrence of 'January' from the month grid.")
    # Click on the exact date '2' in the calendar to select it.
    safe_action(shared_page, shared_page.get_by_text("2", exact=True).nth(2), 'click', "Click on the exact date '2' in the calendar to select it.")
    # Click on the 'Start Week 01/25/2026 End' text to finalize the date selection.
    safe_action(shared_page, shared_page.get_by_text("Start Week 01/25/2026 End"), 'click', "Click on the 'Start Week 01/25/2026 End' text to finalize the date selection.")

@pytest.mark.order(6)
def test_dropdown_interaction(shared_page: Page):
    # Click on the 'Total ByProduct Level None' dropdown to open the options.
    safe_action(shared_page, shared_page.get_by_text("Total ByProduct Level None"), 'click', "Click on the 'Total ByProduct Level None' dropdown to open the options.")
    # Click on the 'Total By' option to select it.
    safe_action(shared_page, shared_page.get_by_text("Total By"), 'click', "Click on the 'Total By' option to select it.")
    # Click on the 'Product Level None Location' dropdown to open the options.
    safe_action(shared_page, shared_page.get_by_text("Product Level None Location"), 'click', "Click on the 'Product Level None Location' dropdown to open the options.")
    # Click on the 'Product Level' option to select it.
    safe_action(shared_page, shared_page.get_by_text("Product Level"), 'click', "Click on the 'Product Level' option to select it.")
    # Click on the first occurrence of 'None' in the dropdown to select it.
    safe_action(shared_page, shared_page.get_by_text("None").first, 'click', "Click on the first occurrence of 'None' in the dropdown to select it.")
    # Click on the 'Select All' option to select all available product levels.
    safe_action(shared_page, shared_page.get_by_text("Select All"), 'click', "Click on the 'Select All' option to select all available product levels.")
    # Click on the first element with the locator '.d-flex.flex-column.justify-content-center' to confirm the selection.
    safe_action(shared_page, shared_page.locator(".d-flex.flex-column.justify-content-center").first, 'click', "Click on the first element with the locator '.d-flex.flex-column.justify-content-center' to confirm the selection.")
    # Click on 'Brand Level 4' to select it.
    safe_action(shared_page, shared_page.get_by_text("Brand Level 4"), 'click', "Click on 'Brand Level 4' to select it.")

@pytest.mark.order(7)
def test_brand_selection(shared_page: Page):
    # Click on 'Brand Level 3' to select it.
    safe_action(shared_page, shared_page.get_by_text("Brand Level 3"), 'click', "Click on 'Brand Level 3' to select it.")
    # Click on 'Brand Level 2' to select it.
    safe_action(shared_page, shared_page.get_by_text("Brand Level 2"), 'click', "Click on 'Brand Level 2' to select it.")
    # Click on the third child element within the '.overflow-auto' container to select it.
    safe_action(shared_page, shared_page.locator(".overflow-auto > div:nth-child(3)"), 'click', "Click on the third child element within the '.overflow-auto' container to select it.")
    # Click on 'UPC' to select it.
    safe_action(shared_page, shared_page.get_by_text("UPC"), 'click', "Click on 'UPC' to select it.")

@pytest.mark.order(8)
def test_product_selection(shared_page: Page):
    # Click on 'Product Level 4' to select it.
    safe_action(shared_page, shared_page.get_by_text("Product Level 4"), 'click', "Click on 'Product Level 4' to select it.")
    # Click on 'Product Level 3' to select it.
    safe_action(shared_page, shared_page.get_by_text("Product Level 3"), 'click', "Click on 'Product Level 3' to select it.")
    # Click on 'Product Level 2' to select it.
    safe_action(shared_page, shared_page.get_by_text("Product Level 2"), 'click', "Click on 'Product Level 2' to select it.")

@pytest.mark.order(9)
def test_location_level_selection(shared_page: Page):
    # Click on 'Location Level' to open the location level dropdown.
    safe_action(shared_page, shared_page.get_by_text("Location Level"), 'click', "Click on 'Location Level' to open the location level dropdown.")
    # Click on the first occurrence of 'None' in the location level dropdown to select it.
    safe_action(shared_page, shared_page.get_by_text("None").first, 'click', "Click on the first occurrence of 'None' in the location level dropdown to select it.")
    # Click on 'Select All' to select all available location levels.
    safe_action(shared_page, shared_page.get_by_text("Select All"), 'click', "Click on 'Select All' to select all available location levels.")
    # Click on 'Sales Level 6' to select it.
    safe_action(shared_page, shared_page.get_by_text("Sales Level 6"), 'click', "Click on 'Sales Level 6' to select it.")
    # Click on 'Sales Level 5' to select it from the Location Level dropdown.
    safe_action(shared_page, shared_page.get_by_text("Sales Level 5", exact=True), 'click', "Click on 'Sales Level 5' to select it from the Location Level dropdown.")
    # Click on 'Sales Level 4' to select it from the Location Level dropdown.
    safe_action(shared_page, shared_page.get_by_text("Sales Level 4", exact=True), 'click', "Click on 'Sales Level 4' to select it from the Location Level dropdown.")
    # Click on the eighth child element within the dropdown to select 'City'.
    safe_action(shared_page, shared_page.locator("div:nth-child(8)"), 'click', "Click on the eighth child element within the dropdown to select 'City'.")
    # Click on 'Sales Level 1' to select it from the Location Level dropdown.
    safe_action(shared_page, shared_page.get_by_text("Sales Level 1", exact=True), 'click', "Click on 'Sales Level 1' to select it from the Location Level dropdown.")
    # Click on the fifth child element within the '.overflow-auto' container to select 'Sales Level 3'.
    safe_action(shared_page, shared_page.locator(".overflow-auto > div:nth-child(5)"), 'click', "Click on the fifth child element within the '.overflow-auto' container to select 'Sales Level 3'.")
    # Click on the seventh child element within the dropdown to select 'Sales Level 1'.
    safe_action(shared_page, shared_page.locator("div:nth-child(7)"), 'click', "Click on the seventh child element within the dropdown to select 'Sales Level 1'.")
    # Click on 'Depot' to select it from the Location Level dropdown.
    safe_action(shared_page, shared_page.get_by_text("Depot", exact=True), 'click', "Click on 'Depot' to select it from the Location Level dropdown.")
    # Click on 'Sales Level 3' to select it from the Location Level dropdown.
    safe_action(shared_page, shared_page.get_by_text("Sales Level 3", exact=True), 'click', "Click on 'Sales Level 3' to select it from the Location Level dropdown.")
    # Click on 'BUSS Environment' to select it from the Location Level dropdown.
    safe_action(shared_page, shared_page.get_by_text("BUSS Environment", exact=True), 'click', "Click on 'BUSS Environment' to select it from the Location Level dropdown.")

@pytest.mark.order(10)
def test_buss_route_and_customer_level_selection(shared_page: Page):
    # Click on the span element containing the text 'BUSS Route ID' to select it.
    safe_action(shared_page, shared_page.locator("span").filter(has_text="BUSS Route ID"), 'click', "Click on the span element containing the text 'BUSS Route ID' to select it.")
    # Click on the dropdown for the second multiselect field under Location Level to open it.
    safe_action(shared_page, shared_page.locator("div:nth-child(2) > esp-multiselect-dropdown > .multiselect-dropdown > div > .w-100"), 'click', "Click on the dropdown for the second multiselect field under Location Level to open it.")
    # Click on 'Customer Level' to select it from the dropdown.
    safe_action(shared_page, shared_page.get_by_text("Customer Level"), 'click', "Click on 'Customer Level' to select it from the dropdown.")
    # Click on the dropdown for the third multiselect field under Customer Level to open it.
    safe_action(shared_page, shared_page.locator("div:nth-child(3) > esp-multiselect-dropdown > .multiselect-dropdown > div > .w-100"), 'click', "Click on the dropdown for the third multiselect field under Customer Level to open it.")
    # Click on 'Select All' to select all options under Customer Level.
    safe_action(shared_page, shared_page.get_by_text("Select All"), 'click', "Click on 'Select All' to select all options under Customer Level.")
    # Click on the third occurrence of 'All' to select it under Customer Level.
    safe_action(shared_page, shared_page.get_by_text("All").nth(3), 'click', "Click on the third occurrence of 'All' to select it under Customer Level.")

@pytest.mark.order(11)
def test_time_and_measures_selection(shared_page: Page):
    # Click on 'Time' to open the Time dropdown.
    safe_action(shared_page, shared_page.get_by_text("Time"), 'click', "Click on 'Time' to open the Time dropdown.")
    # Click on the second occurrence of 'None' to select it under Time.
    safe_action(shared_page, shared_page.get_by_text("None").nth(1), 'click', "Click on the second occurrence of 'None' to select it under Time.")
    # Click on the third occurrence of 'Weekly' to select it under Time.
    safe_action(shared_page, shared_page.locator("div").filter(has_text=re.compile(r"^Weekly$")).nth(3), 'click', "Click on the third occurrence of 'Weekly' to select it under Time.")
    # Click on 'Measures' to open the Measures dropdown.
    safe_action(shared_page, shared_page.get_by_text("Measures", exact=True), 'click', "Click on 'Measures' to open the Measures dropdown.")

@pytest.mark.order(12)
def test_measure_selection_workflow(shared_page: Page):
    # Click on the '.measure-filter-list' element to open the measure filter options.
    safe_action(shared_page, shared_page.locator(".measure-filter-list"), 'click', "Click on the '.measure-filter-list' element to open the measure filter options.")
    # Click on 'Measure' to select it from the Measures dropdown.
    safe_action(shared_page, shared_page.get_by_text("Measure", exact=True), 'click', "Click on 'Measure' to select it from the Measures dropdown.")
    # Click on the first occurrence of 'All Measures' to select it.
    safe_action(shared_page, shared_page.get_by_text("All Measures").first, 'click', "Click on the first occurrence of 'All Measures' to select it.")
    # Click on 'Select All Measures' to select all available measures.
    safe_action(shared_page, shared_page.get_by_text("Select All Measures"), 'click', "Click on 'Select All Measures' to select all available measures.")
    # Click on 'Select All Measures' again to confirm the selection.
    safe_action(shared_page, shared_page.get_by_text("Select All Measures"), 'click', "Click on 'Select All Measures' again to confirm the selection.")
    # Click on 'User Forecast Total' to select it from the Measures dropdown.
    safe_action(shared_page, shared_page.get_by_text("User Forecast Total"), 'click', "Click on 'User Forecast Total' to select it from the Measures dropdown.")
    # Click on the first '.d-flex.dropdown-option.align-items-center.p-v-5.p-l-32' element to confirm the selection.
    safe_action(shared_page, shared_page.locator(".d-flex.dropdown-option.align-items-center.p-v-5.p-l-32").first, 'click', "Click on the first '.d-flex.dropdown-option.align-items-center.p-v-5.p-l-32' element to confirm the selection.")
    # Click on 'User Forecast Base' to select it from the Measures dropdown.
    safe_action(shared_page, shared_page.get_by_text("User Forecast Base"), 'click', "Click on 'User Forecast Base' to select it from the Measures dropdown.")
    # Click on the third child element within the '.overflow-auto' container to select 'User Override Total'.
    safe_action(shared_page, shared_page.locator(".overflow-auto > div:nth-child(3)"), 'click', "Click on the third child element within the '.overflow-auto' container to select 'User Override Total'.")
    # Click on the fifth child element within the '.overflow-auto' container to select 'User Override Base'.
    safe_action(shared_page, shared_page.locator(".overflow-auto > div:nth-child(5)"), 'click', "Click on the fifth child element within the '.overflow-auto' container to select 'User Override Base'.")
    # Click on 'Select All Measures' to select all measures again.
    safe_action(shared_page, shared_page.get_by_text("Select All Measures"), 'click', "Click on 'Select All Measures' to select all measures again.")
    # Click on the text 'Measure' to ensure the Measures dropdown is selected.
    safe_action(shared_page, shared_page.get_by_text("Measure", exact=True), 'click', "Click on the text 'Measure' to ensure the Measures dropdown is selected.")

@pytest.mark.order(13)
def test_download_and_reset_actions(shared_page: Page):
    # Click on the 'Download' button to initiate the download process.
    safe_action(shared_page, shared_page.get_by_role("button", name="Download"), 'click', "Click on the 'Download' button to initiate the download process.")
    # Click on the text 'Please note that a maximum of' to display the information about the maximum number of rows that can be exported.
    safe_action(shared_page, shared_page.get_by_text("Please note that a maximum of"), 'click', "Click on the text 'Please note that a maximum of' to display the information about the maximum number of rows that can be exported.")
    # Click on the 'Reset' button to reset the filter selections.
    safe_action(shared_page, shared_page.get_by_role("button", name="Reset"), 'click', "Click on the 'Reset' button to reset the filter selections.")
    # Click on the 'Reset' button again to confirm the reset action.
    safe_action(shared_page, shared_page.get_by_role("button", name="Reset"), 'click', "Click on the 'Reset' button again to confirm the reset action.")

