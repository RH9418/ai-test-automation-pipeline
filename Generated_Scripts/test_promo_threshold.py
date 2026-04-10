
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


@pytest.mark.order(4)
def test_navigation_to_promotions_page(shared_page: Page):
    safe_action(shared_page, shared_page, 'goto', "Navigate to the 'Create Promotions' page on the staging environment.", "https://stage.mkr.esp.antuit.ai/nglcp/promotions/create-promotions")
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


@pytest.mark.order(5)
def test_event_details_input(shared_page: Page):
    safe_action(shared_page, shared_page.get_by_test_id("promotionEventName"), 'click', "Click on the 'Event Name' input field to focus on it.")
    safe_action(shared_page, shared_page.get_by_test_id("promotionEventName"), 'fill', "Fill the 'Event Name' input field with the value 'rh--1220--0904'.", "rh--1220--0904")
    safe_action(shared_page, shared_page.get_by_test_id("promotionEventDescription"), 'click', "Click on the 'Event Description' input field to focus on it.")
    safe_action(shared_page, shared_page.get_by_test_id("promotionEventDescription"), 'fill', "Fill the 'Event Description' input field with the value 'PROMO THRESHOLD'.", "PROMO THRESHOLD")

@pytest.mark.order(6)
def test_date_selection(shared_page: Page):
    safe_action(shared_page, shared_page.get_by_test_id("startDate"), 'click', "Click on the 'Start Date' input field to open the date picker.")
    safe_action(shared_page, shared_page.get_by_text("10", exact=True), 'click', "Select the 10th day of the month as the start date from the date picker.")
    safe_action(shared_page, shared_page.get_by_test_id("endDate"), 'click', "Click on the 'End Date' input field to open the date picker.")
    safe_action(shared_page, shared_page.get_by_text("17"), 'click', "Select the 17th day of the month as the end date from the date picker.")

@pytest.mark.order(7)
def test_asap_pricing_and_zebra_tiers(shared_page: Page):
    safe_action(shared_page, shared_page.get_by_test_id("isAsapPricing"), 'click', "Click on the 'ASAP Pricing' checkbox to enable or disable this option.")
    safe_action(shared_page, shared_page.locator(".zeb-tiers").first, 'click', "Click on the first tier in the 'Zebra Tiers' section to select it.")

@pytest.mark.order(8)
def test_location_filters(shared_page: Page):
    safe_action(shared_page, shared_page.locator("#SideFilterlocationhierarchyId").get_by_text("Hierarchy"), 'click', "Click on the 'Hierarchy' option in the 'Location' filter section to expand the hierarchy options.")
    safe_action(shared_page, shared_page.get_by_text("Region", exact=True), 'click', "Select the 'Region' option from the expanded hierarchy options.")
    safe_action(shared_page, shared_page.get_by_role("radio", name="NA", exact=True), 'check', "Check the radio button for the 'NA' region to filter by this region.")
    safe_action(shared_page, shared_page.get_by_text("Price Zone Type"), 'click', "Click on 'Price Zone Type' to expand the available price zone type options.")
    safe_action(shared_page, shared_page.locator("div").filter(has_text=re.compile(r"^Collection$")), 'click', "Select the 'Collection' option under 'Price Zone Type' to filter by this type.")
    safe_action(shared_page, shared_page.get_by_text("Price Zone", exact=True), 'click', "Click on 'Price Zone' to expand the available price zone options.")
    safe_action(shared_page, shared_page.get_by_text("1_US Collection"), 'click', "Select the '1_US Collection' option under 'Price Zone' to apply this specific filter.")
    safe_action(shared_page, shared_page.get_by_role("button", name="Apply Filters"), 'click', "Click on the 'Apply Filters' button to apply the selected location filters.")

@pytest.mark.order(9)
def test_product_filters(shared_page: Page):
    safe_action(shared_page, shared_page.get_by_role("textbox", name="Select Products"), 'click', "Click on the 'Select Products' textbox to open the product filter options.")
    safe_action(shared_page, shared_page.locator("#SideFilterproducthierarchyId").get_by_text("Hierarchy"), 'click', "Click on the 'Hierarchy' option in the product filter section to expand the hierarchy options.")
    safe_action(shared_page, shared_page.get_by_text("Style Color"), 'click', "Select the 'Style Color' option from the expanded hierarchy options.")
    safe_action(shared_page, shared_page.locator("div:nth-child(5) > esp-filter-sub-accordion-v1 > .sub-accordion-element > .fiter-values-container > .filter-options > .filter-values-options > .filter-values.d-flex.align-items-center.p-l-32.p-r-12 > .custom-checkbox-wrapper"), 'click', "Check the checkbox for 'Select All' under the 'Style Color' filter to select all available options.")
    safe_action(shared_page, shared_page.locator("div:nth-child(5) > esp-filter-sub-accordion-v1 > .sub-accordion-element > .fiter-values-container > .filter-options > .filter-values-options > div:nth-child(2) > .custom-checkbox-wrapper > .pointer"), 'click', "Check the checkbox for the specific product option 'C281-019999' under the 'Style Color' filter.")
    safe_action(shared_page, shared_page.locator(".pointer.custom-checkbox-unchecked").first, 'click', "Check the checkbox for the specific product option '004AHK003490' under the 'Style Color' filter.")
    safe_action(shared_page, shared_page.get_by_role("button", name="Apply Filters"), 'click', "Click on the 'Apply Filters' button to apply the selected product filters.")

@pytest.mark.order(10)
def test_optimization_objective(shared_page: Page):
    safe_action(shared_page, shared_page.locator("#optimizationObjective > .multiselect-dropdown > div > .w-100"), 'click', "Click on the dropdown for 'Optimization Objective' to view the available options.")
    safe_action(shared_page, shared_page.locator("div").filter(has_text=re.compile(r"^Optimize for Sales Unit$")).nth(1), 'click', "Select the 'Optimize for Sales Unit' option from the 'Optimization Objective' dropdown.")

@pytest.mark.order(11)
def test_promo_recommendations(shared_page: Page):
    safe_action(shared_page, shared_page.get_by_test_id("create-promotions-next-button"), 'click', "Click on the 'Next Promo Recommendations' button to proceed to the next step in the promotion creation process.")
    safe_action(shared_page, shared_page.get_by_text("Available Products"), 'click', "Click on 'Available Products' to view the list of products available for promotion.")
    safe_action(shared_page, shared_page.get_by_text("Show More"), 'click', "Click on 'Show More' to expand the list of available products.")
    safe_action(shared_page, shared_page.get_by_test_id("create-promotions-next-button"), 'click', "Click on the 'Next' button to proceed to the promotion setup step.")

@pytest.mark.order(12)
def test_promotion_type_selection(shared_page: Page):
    safe_action(shared_page, shared_page.locator(".w-100.p-h-16").first, 'click', "Select the first option in the dropdown or list for promotion type.")
    safe_action(shared_page, shared_page.get_by_text("Bundle"), 'click', "Select 'Bundle' as the promotion type.")
    safe_action(shared_page, shared_page.get_by_text("Threshold"), 'click', "Select 'Threshold' as an additional promotion type.")

@pytest.mark.order(13)
def test_promotion_rules_and_spend_threshold(shared_page: Page):
    safe_action(shared_page, shared_page.locator(".d-flex.flex-column.justify-content-center.font-size-10.align-items-center.checkbox-v2.m-r-10.zeb-check").first, 'click', "Click on the first checkbox to enable stacking rules or constraints.")
    safe_action(shared_page, shared_page.get_by_text("What type of promotion(s) would you like to compare? *Max limit 5Promo Type"), 'click', "Click on the dropdown to specify the type of promotions to compare, with a maximum limit of 5.")
    safe_action(shared_page, shared_page.get_by_test_id("spend_amount"), 'click', "Click on the 'Spend Amount' field to input the spending threshold for the promotion.")
    safe_action(shared_page, shared_page.get_by_test_id("spend_amount"), 'fill', "Enter '5000' as the spending threshold for the promotion.", "5000")
    safe_action(shared_page, shared_page.locator("#get"), 'click', "Click on the 'Get' field to input the discount percentage or value.")
    safe_action(shared_page, shared_page.locator("#get"), 'fill', "Enter '25' as the discount percentage or value for the promotion.", "25")

@pytest.mark.order(14)
def test_price_zone_adjustment(shared_page: Page):
    safe_action(shared_page, shared_page.get_by_test_id("create-promotions-next-button"), 'click', "Click on the 'Next' button to proceed to the next step in the promotion creation process.")
    safe_action(shared_page, shared_page.get_by_text("Price Zone Adjustment"), 'click', "Click on 'Price Zone Adjustment' to navigate to the price zone adjustment section.")
    safe_action(shared_page, shared_page.get_by_test_id("replicate-apply"), 'click', "Click on the 'Apply' button to replicate the promotion details to sub-levels.")

@pytest.mark.order(15)
def test_product_details_navigation(shared_page: Page):
    safe_action(shared_page, shared_page, 'goto', "Navigate to the 'Product Details' page by accessing the specified URL.", "https://stage.mkr.esp.antuit.ai/nglcp/product-level-details/product-details")

@pytest.mark.order(16)
def test_approval_workflow(shared_page: Page):
    safe_action(shared_page, shared_page.get_by_role("button", name="Close"), 'click', "Click on the 'Close' button to dismiss the current modal or overlay.")
    safe_action(shared_page, shared_page.get_by_test_id("submit-all-for-approval"), 'click', "Click on the 'Submit All for Approval' button to initiate the approval process for the selected scenario.")
    safe_action(shared_page, shared_page.get_by_test_id("confirm-modal-confirm-yes-button"), 'click', "Confirm the submission by clicking the 'Yes, Submit' button in the confirmation modal.")
    safe_action(shared_page, shared_page.get_by_role("button", name="Actions"), 'click', "Open the 'Actions' dropdown menu to access further options for the scenario.")
    safe_action(shared_page, shared_page.get_by_text("Approve", exact=True), 'click', "Select the 'Approve' option from the dropdown to approve the scenario.")
    safe_action(shared_page, shared_page.get_by_test_id("confirm-modal-confirm-yes-button"), 'click', "Confirm the approval action by clicking the 'Confirm' button in the modal.")
    safe_action(shared_page, shared_page.get_by_role("button", name="Actions"), 'click', "Reopen the 'Actions' dropdown menu to access additional options.")
    safe_action(shared_page, shared_page.get_by_text("Reject"), 'click', "Select the 'Reject' option from the dropdown to reject the scenario.")
    safe_action(shared_page, shared_page.get_by_test_id("confirm-modal-confirm-yes-button"), 'click', "Confirm the rejection action by clicking the 'Confirm' button in the modal.")
    safe_action(shared_page, shared_page.get_by_role("button", name="Actions"), 'click', "Reopen the 'Actions' dropdown menu to access further options.")
    safe_action(shared_page, shared_page.get_by_text("Withdraw", exact=True), 'click', "Select the 'Withdraw' option from the dropdown to withdraw the scenario.")
    safe_action(shared_page, shared_page.get_by_test_id("confirm-modal-confirm-yes-button"), 'click', "Confirm the withdrawal action by clicking the 'Confirm' button in the modal.")

@pytest.mark.order(17)
def test_final_steps_and_cleanup(shared_page: Page):
    safe_action(shared_page, shared_page.get_by_test_id("create-promotions-next-button"), 'click', "Click on the 'Next' button to proceed to the next step in the promotion creation process.")

