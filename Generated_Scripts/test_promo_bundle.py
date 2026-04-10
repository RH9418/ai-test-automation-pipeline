
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
def test_navigation_to_create_promotions_page(shared_page: Page):
    safe_action(shared_page, shared_page, 'goto', "Navigate to the 'Create Promotions' page using the specified URL.", "https://stage.mkr.esp.antuit.ai/nglcp/promotions/create-promotions")
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
def test_promotion_event_details_input(shared_page: Page):
    safe_action(shared_page, shared_page.get_by_test_id("promotionEventName"), 'click', "Click on the 'Name' input field to begin entering the promotion event name.")
    safe_action(shared_page, shared_page.get_by_test_id("promotionEventName"), 'fill', "Fill the 'Name' input field with the value 'rh--1137-0904'.", "rh--1137-0904")
    safe_action(shared_page, shared_page.get_by_test_id("promotionEventDescription"), 'click', "Click on the 'Description' input field to begin entering the promotion event description.")
    safe_action(shared_page, shared_page.get_by_test_id("promotionEventDescription"), 'fill', "Fill the 'Description' input field with the value 'PROMO BUNDLE TEST 2'.", "PROMO BUNDLE TEST 2")

@pytest.mark.order(5)
def test_date_selection(shared_page: Page):
    safe_action(shared_page, shared_page.get_by_test_id("startDate"), 'click', "Click on the 'Start Date' field to open the date picker.")
    safe_action(shared_page, shared_page.get_by_text("16"), 'click', "Select the 16th day of the month as the start date from the date picker.")
    safe_action(shared_page, shared_page.get_by_test_id("endDate"), 'click', "Click on the 'End Date' field to open the date picker.")
    safe_action(shared_page, shared_page.get_by_text("23", exact=True), 'click', "Select the 23rd day of the month as the end date from the date picker.")

@pytest.mark.order(6)
def test_additional_considerations_and_location_selection(shared_page: Page):
    safe_action(shared_page, shared_page.get_by_test_id("isAsapPricing"), 'click', "Click on the 'ASAP Pricing' checkbox to enable this option under 'Additional Considerations'.")
    safe_action(shared_page, shared_page.get_by_role("textbox", name="Select Locations"), 'click', "Click on the 'Select Locations' textbox to open the location selection panel.")
    safe_action(shared_page, shared_page.locator("#SideFilterlocationhierarchyId").get_by_text("Hierarchy"), 'click', "Click on 'Hierarchy' in the location selection panel to expand the hierarchy options.")
    safe_action(shared_page, shared_page.get_by_text("Region", exact=True), 'click', "Select 'Region' from the hierarchy options.")
    safe_action(shared_page, shared_page.get_by_role("radio", name="JPN"), 'check', "Select the 'JPN' radio button to filter locations by the Japan region.")
    safe_action(shared_page, shared_page.get_by_text("Price Zone Type"), 'click', "Click on 'Price Zone Type' to expand the price zone type options.")
    safe_action(shared_page, shared_page.locator(".filter-values.d-flex.align-items-center.p-l-32.p-r-24 > .custom-checkbox-wrapper > .pointer").first, 'click', "Select the first checkbox under 'Price Zone Type' (e.g., 'Select All').")
    safe_action(shared_page, shared_page.get_by_text("Price Zone", exact=True), 'click', "Click on 'Price Zone' to expand the price zone options.")
    safe_action(shared_page, shared_page.locator(".filter-values.d-flex.align-items-center.p-l-32.p-r-24 > .custom-checkbox-wrapper > .pointer"), 'click', "Select a specific price zone checkbox (e.g., 'Collection').")
    safe_action(shared_page, shared_page.get_by_role("button", name="Apply Filters"), 'click', "Click on the 'Apply Filters' button to apply the selected location and price zone filters.")

@pytest.mark.order(7)
def test_product_selection(shared_page: Page):
    safe_action(shared_page, shared_page.get_by_role("textbox", name="Select Products"), 'click', "Click on the 'Select Products' textbox to open the product selection panel.")
    safe_action(shared_page, shared_page.locator("#SideFilterproducthierarchyId").get_by_text("Hierarchy"), 'click', "Click on 'Hierarchy' in the product selection panel to expand the hierarchy options.")
    safe_action(shared_page, shared_page.get_by_text("Style Color"), 'click', "Click on 'Style Color' in the hierarchy options to filter products by style color.")
    safe_action(shared_page, shared_page.get_by_text("Style Color"), 'click', "Click on 'Style Color' again to ensure the filter is selected.")
    safe_action(shared_page, shared_page.locator("div:nth-child(5) > esp-filter-sub-accordion-v1 > .sub-accordion-element > .fiter-values-container > .filter-options > .filter-values-options > .filter-values.d-flex.align-items-center.p-l-32.p-r-12 > .custom-checkbox-wrapper"), 'click', "Select the first checkbox under 'Style Color' (e.g., 'Select All') to include all style colors.")
    safe_action(shared_page, shared_page.locator("div:nth-child(5) > esp-filter-sub-accordion-v1 > .sub-accordion-element > .fiter-values-container > .filter-options > .filter-values-options > div:nth-child(2) > .custom-checkbox-wrapper > .pointer"), 'click', "Select a specific style color checkbox (e.g., '-2C8-01J999') to include it in the selection.")
    safe_action(shared_page, shared_page.locator(".pointer.custom-checkbox-unchecked").first, 'click', "Click on the first unchecked checkbox to include another style color in the selection.")
    safe_action(shared_page, shared_page.locator(".pointer.custom-checkbox-unchecked").first, 'click', "Click on the first unchecked checkbox again to ensure it is selected.")
    safe_action(shared_page, shared_page.locator("div").filter(has_text=re.compile(r"^101AKB0201$")), 'click', "Click on a specific product (e.g., '101AKB0201') to include it in the selection.")
    safe_action(shared_page, shared_page.get_by_role("button", name="Apply Filters"), 'click', "Click on the 'Apply Filters' button to apply the selected product filters.")

@pytest.mark.order(8)
def test_optimization_objective_and_summary_navigation(shared_page: Page):
    safe_action(shared_page, shared_page.locator("#optimizationObjective > .multiselect-dropdown > div > .w-100"), 'click', "Click on the dropdown menu under 'Set Optimization Objective' to view the available optimization options.")
    safe_action(shared_page, shared_page.get_by_text("Optimize for Margin Revenue"), 'click', "Select 'Optimize for Margin Revenue' from the dropdown menu to set it as the optimization objective.")
    safe_action(shared_page, shared_page.get_by_test_id("create-promotions-next-button"), 'click', "Click on the 'Next Promo Recommendations' button to proceed to the summary page.")
    safe_action(shared_page, shared_page.get_by_test_id("summary-show-more-button"), 'click', "Click on the 'Show More' button to expand additional details in the summary section.")
    safe_action(shared_page, shared_page.get_by_text("Available Products"), 'click', "Click on the 'Available Products' tab to view the list of products included in the promotion.")
    safe_action(shared_page, shared_page.get_by_test_id("create-promotions-next-button"), 'click', "Click on the 'Next Promo Recommendations' button again to finalize and proceed.")

@pytest.mark.order(9)
def test_promotion_group_configuration(shared_page: Page):
    safe_action(shared_page, shared_page.locator(".dropdown-caret").first, 'click', "Click on the first dropdown caret to expand the options for defining promotion groups.")
    safe_action(shared_page, shared_page.locator(".overflow-auto > div:nth-child(4)"), 'click', "Select the fourth option from the dropdown to choose a specific group configuration.")
    safe_action(shared_page, shared_page.locator(".flex-grow-1").first, 'click', "Click on the first element with the 'flex-grow-1' class to proceed with the group selection.")
    safe_action(shared_page, shared_page.get_by_test_id("group-name-edit-btn"), 'click', "Click on the 'Edit Group Name' button to modify the name of the selected group.")
    safe_action(shared_page, shared_page.get_by_test_id("name"), 'fill', "Fill in the group name field with 'Watch' to name the group.", "Watch")
    safe_action(shared_page, shared_page.get_by_text("Buy 1 0 Eligible Products Selected Add"), 'click', "Click on the 'Buy 1 0 Eligible Products Selected Add' button to add eligible products to the group.")
    safe_action(shared_page, shared_page.get_by_test_id("group-add"), 'click', "Click on the 'Add Group' button to create a new group.")
    safe_action(shared_page, shared_page.get_by_test_id("product-ids"), 'click', "Click on the 'Product IDs' field to input product identifiers for the group.")
    safe_action(shared_page, shared_page.get_by_test_id("product-ids"), 'fill', "Fill in the 'Product IDs' field with the specified product IDs, separated by new lines.", "005DKI0041\n100DKX5271\n100DKX534704\n101AKB0201")
    safe_action(shared_page, shared_page.get_by_test_id("save"), 'click', "Click on the 'Save' button to save the group configuration.")

@pytest.mark.order(10)
def test_promotion_value_and_price_zone_adjustment(shared_page: Page):
    safe_action(shared_page, shared_page.get_by_role("textbox", name="Add Value"), 'click', "Click on the 'Add Value' textbox to input a value for the promotion.")
    safe_action(shared_page, shared_page.get_by_role("textbox", name="Add Value"), 'fill', "Fill in the 'Add Value' textbox with '35' to set the promotion value.", "35")
    safe_action(shared_page, shared_page.get_by_test_id("create-promotions-next-button"), 'click', "Click on the 'Next' button to proceed to the next step in the promotion creation process.")
    safe_action(shared_page, shared_page.get_by_text("Price Zone Adjustment"), 'click', "Click on 'Price Zone Adjustment' to navigate to the section for adjusting price zones.")
    safe_action(shared_page, shared_page.locator("#attribute_value"), 'click', "Click on the '#attribute_value' field to select it for input.")
    safe_action(shared_page, shared_page.locator("#attribute_value"), 'fill', "Fill in the '#attribute_value' field with '40' to set the adjustment value.", "40")
    safe_action(shared_page, shared_page.get_by_test_id("replicate-apply"), 'click', "Click on the 'Apply' button to save and apply the price zone adjustment.")

@pytest.mark.order(11)
def test_submission_and_approval_workflow(shared_page: Page):
    safe_action(shared_page, shared_page.get_by_role("button", name="Submit All for Approval"), 'click', "Click on the 'Submit All for Approval' button to initiate the submission of the promotion for approval.")
    safe_action(shared_page, shared_page.get_by_test_id("confirm-modal-confirm-yes-button"), 'click', "Confirm the submission by clicking the 'Yes, Submit' button in the confirmation modal.")
    safe_action(shared_page, shared_page.get_by_role("button", name="Close"), 'click', "Click on the 'Close' button to close the submission confirmation modal.")
    safe_action(shared_page, shared_page.get_by_role("button", name="Actions"), 'click', "Click on the 'Actions' button to open the actions menu.")
    safe_action(shared_page, shared_page.get_by_text("Approve", exact=True), 'click', "Select 'Approve' from the actions menu to approve the promotion.")
    safe_action(shared_page, shared_page.get_by_test_id("confirm-modal-confirm-yes-button"), 'click', "Confirm the approval by clicking the 'Confirm' button in the confirmation modal.")
    safe_action(shared_page, shared_page.get_by_role("button", name="Actions"), 'click', "Click on the 'Actions' button again to open the actions menu.")
    safe_action(shared_page, shared_page.get_by_text("Reject"), 'click', "Select 'Reject' from the actions menu to reject the promotion.")
    safe_action(shared_page, shared_page.get_by_test_id("confirm-modal-confirm-yes-button"), 'click', "Confirm the rejection by clicking the 'Confirm' button in the confirmation modal.")
    safe_action(shared_page, shared_page.get_by_role("button", name="Actions"), 'click', "Click on the 'Actions' button again to open the actions menu.")
    safe_action(shared_page, shared_page.get_by_text("Withdraw", exact=True), 'click', "Select 'Withdraw' from the actions menu to withdraw the promotion.")
    safe_action(shared_page, shared_page.get_by_test_id("confirm-modal-confirm-yes-button"), 'click', "Confirm the withdrawal by clicking the 'Confirm' button in the confirmation modal.")

@pytest.mark.order(12)
def test_final_steps_and_cleanup(shared_page: Page):
    safe_action(shared_page, shared_page.get_by_test_id("create-promotions-next-button"), 'click', "Click on the 'Next' button in the promotion creation flow to proceed to the next step.")

