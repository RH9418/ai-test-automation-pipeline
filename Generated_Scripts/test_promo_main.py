import os
import sys
import time
import re
from datetime import datetime
import pytest
from playwright.sync_api import sync_playwright, Page, expect, TimeoutError

# --- Screenshot Directory Setup ---
SCREENSHOT_DIR = "Test_Screenshots"
if not os.path.exists(SCREENSHOT_DIR):
    os.makedirs(SCREENSHOT_DIR)
screenshot_counter = 0

def capture_annotated_screenshot(page: Page, locator, full_action_description: str):
    '''Highlights element with a thick red box and glow, then captures screenshot.'''
    global screenshot_counter
    screenshot_counter += 1
    try:
        locator.scroll_into_view_if_needed()
        locator.wait_for(state='visible', timeout=5000)
        box = locator.bounding_box()
        if not box:
            print(f"   └── ⚠️ Screenshot Warning: Bounding box null for '{full_action_description}'.")
            return
            
        js_description = full_action_description.replace("'", "\\'")
        page.evaluate(f'''(params) => {{
            const {{ box, desc }} = params;
            const div = document.createElement('div');
            div.id = 'ge-spotlight-box';
            div.style.position = 'absolute';
            div.style.left = `${{box.x}}px`;
            div.style.top = `${{box.y}}px`;
            div.style.width = `${{box.width}}px`;
            div.style.height = `${{box.height}}px`;
            div.style.border = '5px solid #FF0000';
            div.style.boxShadow = '0 0 15px 5px rgba(255, 0, 0, 0.7)';
            div.style.boxSizing = 'border-box';
            div.style.zIndex = '2147483647';
            div.style.pointerEvents = 'none';
            
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
            document.body.appendChild(div);
            document.body.appendChild(label);
        }}''', {'box': box, 'desc': js_description})
        
        time.sleep(0.2)
        timestamp = datetime.now().strftime("%H-%M-%S")
        safe_filename = re.sub(r'[^a-z0-9]', '_', full_action_description.lower())[:40]
        filename = f"{timestamp}_{screenshot_counter:02d}_{safe_filename}.png"
        path = os.path.join(SCREENSHOT_DIR, filename)
        
        page.screenshot(path=path, full_page=False)
        print(f"   └── 📸 Screenshot saved: {path}")
        
        page.evaluate("() => { document.getElementById('ge-spotlight-box')?.remove(); document.getElementById('ge-spotlight-label')?.remove(); }")
    except Exception as e:
        print(f"   └── ⚠️ Screenshot Error: {e}")

def safe_action(page: Page, locator, action_name: str, description: str, *action_args):
    '''Performs action with spotlight screenshots and manual fallbacks.'''
    full_desc = f"{action_name.capitalize()}: {description}"
    if action_name == 'fill':
        full_desc += f" with '{action_args[0] if action_args else ''}'"
        
    try:
        if action_name == 'fill':
            print(f"\n⏸️ PAUSING FOR INPUT: About to fill '{description}'.")
            input("   └── Perform input manually in browser, then PRESS [ENTER] to continue...")
            page.wait_for_load_state('networkidle', timeout=5000)
            return

        if action_name in ['click', 'dblclick', 'check', 'uncheck', 'hover']:
            try:
                locator.hover(timeout=2000)
                time.sleep(0.3)
            except: pass
            
        # --- BULLETPROOF TEARDOWN FIX ---
        if action_name == 'close':
            try: locator.close()
            except: pass
            print(f"✅ SUCCESS: {description} (Teardown handled by Pytest)")
            return

        if locator != page: # Don't try to draw a box around the entire page object
            capture_annotated_screenshot(page, locator, full_desc)
            action_func = getattr(locator, action_name)
            action_func(*action_args)
        else:
            if action_name == 'goto':
                page.goto(*action_args)
                
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

@pytest.mark.order(1)
def test_navigate_to_promotions(shared_page: Page):
    safe_action(shared_page, shared_page, 'goto', 'Navigate to the Promotions page', "https://stage.mkr.esp.antuit.ai/nglcp/promotions/")
    safe_action(shared_page, shared_page.get_by_test_id("promotions-action-button"), 'click', 'Click on the promotions action button')

@pytest.mark.order(2)
def test_create_new_promotion(shared_page: Page):
    safe_action(shared_page, shared_page.get_by_text("New Promotion"), 'click', 'Click on New Promotion')
    safe_action(shared_page, shared_page.get_by_test_id("promotionEventName"), 'click', 'Click on the promotion event name field')
    safe_action(shared_page, shared_page.get_by_test_id("promotionEventName"), 'fill', 'Fill the promotion event name field', "rh-1205070436")
    safe_action(shared_page, shared_page.get_by_test_id("promotionEventDescription"), 'click', 'Click on the promotion event description field')
    safe_action(shared_page, shared_page.get_by_test_id("promotionEventDescription"), 'fill', 'Fill the promotion event description field', "PROMO TEST 3")
    safe_action(shared_page, shared_page.get_by_test_id("startDate"), 'click', 'Click on the Start Date field')
    safe_action(shared_page, shared_page.get_by_text("9").nth(1), 'click', 'Select the 9th day as the start date')
    safe_action(shared_page, shared_page.get_by_test_id("endDate"), 'click', 'Click on the End Date field')
    safe_action(shared_page, shared_page.get_by_text("12", exact=True), 'click', 'Select the 12th day as the end date')

@pytest.mark.order(3)
def test_apply_location_filters(shared_page: Page):
    safe_action(shared_page, shared_page.get_by_test_id("isAsapPricing"), 'click', 'Enable ASAP Pricing option')
    safe_action(shared_page, shared_page.locator(".zeb-tiers").first, 'click', 'Click on the first .zeb-tiers element')
    safe_action(shared_page, shared_page.locator("div").filter(has_text=re.compile(r"^Hierarchy$")).nth(3), 'click', 'Select Hierarchy option')
    safe_action(shared_page, shared_page.get_by_text("Region", exact=True), 'click', 'Click on Region option')
    safe_action(shared_page, shared_page.get_by_role("radio", name="NA", exact=True), 'check', 'Select NA radio button')
    safe_action(shared_page, shared_page.get_by_text("Price Zone Type"), 'click', 'Click on Price Zone Type')
    safe_action(shared_page, shared_page.locator(".filter-values.d-flex.align-items-center.p-l-32.p-r-24 > .custom-checkbox-wrapper > .pointer").first, 'click', 'Select first checkbox under Price Zone Type')
    safe_action(shared_page, shared_page.get_by_text("Price Zone", exact=True), 'click', 'Click on Price Zone')
    safe_action(shared_page, shared_page.locator(".filter-values.d-flex.align-items-center.p-l-32.p-r-24 > .custom-checkbox-wrapper > .pointer"), 'click', 'Select a checkbox under Price Zone')
    safe_action(shared_page, shared_page.get_by_role("button", name="Apply Filters"), 'click', 'Click on Apply Filters button')

@pytest.mark.order(4)
def test_apply_product_hierarchy_filters(shared_page: Page):
    safe_action(shared_page, shared_page.locator("div:nth-child(8) > .zeb-tiers"), 'click', 'Click on the eighth .zeb-tiers element')
    safe_action(shared_page, shared_page.locator("#SideFilterproducthierarchyId").get_by_text("Hierarchy"), 'click', 'Click on Hierarchy in #SideFilterproducthierarchyId')
    safe_action(shared_page, shared_page.get_by_text("Style Color"), 'click', 'Select Style Color option')
    safe_action(shared_page, shared_page.locator("div:nth-child(5) > esp-filter-sub-accordion-v1 > .sub-accordion-element > .fiter-values-container > .filter-options > .filter-values-options > .filter-values.d-flex.align-items-center.p-l-32.p-r-12 > .custom-checkbox-wrapper > .pointer"), 'click', 'Select a checkbox under Style Color')
    safe_action(shared_page, shared_page.locator("div:nth-child(6) > .custom-checkbox-wrapper > .pointer"), 'click', 'Click on the sixth child checkbox')
    safe_action(shared_page, shared_page.locator("div:nth-child(5) > .custom-checkbox-wrapper > .pointer"), 'click', 'Click on the fifth child checkbox')
    safe_action(shared_page, shared_page.get_by_role("button", name="Apply Filters"), 'click', 'Click on Apply Filters button')

@pytest.mark.order(5)
def test_select_optimization_objective(shared_page: Page):
    safe_action(shared_page, shared_page.locator("#optimizationObjective > .multiselect-dropdown > div > .w-100"), 'click', 'Open dropdown for optimization objective')
    safe_action(shared_page, shared_page.locator("div").filter(has_text=re.compile(r"^Optimize for Sales Unit$")).nth(1), 'click', 'Select Optimize for Sales Unit')
    safe_action(shared_page, shared_page.get_by_test_id("create-promotions-next-button"), 'click', 'Click Next button')

@pytest.mark.order(6)
def test_configure_grid_settings(shared_page: Page):
    safe_action(shared_page, shared_page.get_by_text("Show More"), 'click', 'Click on Show More')
    safe_action(shared_page, shared_page.get_by_role("checkbox", name="Column with Header Selection"), 'check', 'Select Column with Header Selection checkbox')
    safe_action(shared_page, shared_page.get_by_test_id("promotions-action-button"), 'click', 'Click on promotions action button')
    safe_action(shared_page, shared_page.get_by_text("Reset Preferences"), 'click', 'Click Reset Preferences')
    safe_action(shared_page, shared_page.get_by_role("textbox", name="Search"), 'click', 'Focus on search textbox')
    safe_action(shared_page, shared_page.get_by_role("textbox", name="Search"), 'fill', 'Fill search textbox with 005', "005")
    safe_action(shared_page, shared_page.get_by_role("textbox", name="Search"), 'press', 'Submit search query', "Enter")
    safe_action(shared_page, shared_page.locator("a").nth(1), 'click', 'Click on second link in list')

@pytest.mark.order(7)
def test_apply_product_filters(shared_page: Page):
    safe_action(shared_page, shared_page.get_by_text("Available Products"), 'click', 'Click on Available Products')
    safe_action(shared_page, shared_page.locator("div:nth-child(3) > div > esp-multiselect-dropdown > .multiselect-dropdown > div > .w-100 > .d-flex.align-items-center > .dropdown-caret"), 'click', 'Open dropdown for product filtering')
    safe_action(shared_page, shared_page.locator("div:nth-child(7) > .d-flex"), 'click', 'Select specific filter option')
    safe_action(shared_page, shared_page.locator(".ag-center-cols-viewport"), 'click', 'Interact with grid center column')
    safe_action(shared_page, shared_page.locator(".w-100.p-h-16").first, 'click', 'Select first item in list')
    safe_action(shared_page, shared_page.locator(".d-flex.dropdown-option.align-items-center.p-v-5.p-l-32").first, 'click', 'Click first dropdown option')
    safe_action(shared_page, shared_page.get_by_text("21_Men's Underwear"), 'click', 'Select 21_Men\'s Underwear')
    safe_action(shared_page, shared_page.locator("div:nth-child(2) > div > esp-multiselect-dropdown > .multiselect-dropdown > div > .w-100 > .d-flex.align-items-center > .dropdown-caret"), 'click', 'Open additional dropdown')
    safe_action(shared_page, shared_page.locator("div:nth-child(3) > div > esp-multiselect-dropdown > .multiselect-dropdown > div > .w-100 > .d-flex.align-items-center > .dropdown-caret"), 'click', 'Open third dropdown')
    safe_action(shared_page, shared_page.locator(".d-flex.flex-column.justify-content-center").first, 'click', 'Select first option in flex column dropdown')
    safe_action(shared_page, shared_page.locator(".overflow-auto > div:nth-child(2) > .d-flex"), 'click', 'Select second option in overflow auto dropdown')
    safe_action(shared_page, shared_page.get_by_test_id("complex-filter-apply"), 'click', 'Apply complex filter')

@pytest.mark.order(8)
def test_add_promotion_details(shared_page: Page):
    safe_action(shared_page, shared_page.locator("#ag-2170-input"), 'check', 'Enable promotion creation checkbox')
    safe_action(shared_page, shared_page.get_by_test_id("promotions-action-button"), 'click', 'Click on Promotions Action button')
    safe_action(shared_page, shared_page.get_by_text("Add"), 'click', 'Click on Add')
    safe_action(shared_page, shared_page.get_by_test_id("confirm-modal-confirm-yes-button"), 'click', 'Confirm action in modal')
    safe_action(shared_page, shared_page.get_by_role("button", name="Reoptimize"), 'click', 'Click on Reoptimize button')
    safe_action(shared_page, shared_page.get_by_test_id("confirm-modal-confirm-yes-button"), 'click', 'Confirm reoptimization in modal')
    safe_action(shared_page, shared_page.get_by_test_id("create-promotions-next-button"), 'click', 'Click Next button')
    safe_action(shared_page, shared_page.locator(".dropdown-caret").first, 'click', 'Open dropdown for promotion type')
    safe_action(shared_page, shared_page.get_by_text("BOGO"), 'click', 'Select BOGO promotion type')
    safe_action(shared_page, shared_page.locator(".row").first, 'click', 'Click on first row for group details')
    safe_action(shared_page, shared_page.locator("#numberOfBuyGroups > .multiselect-dropdown > div > .w-100 > .d-flex.align-items-center > .dropdown-caret"), 'click', 'Open dropdown for buy groups')
    safe_action(shared_page, shared_page.locator("div").filter(has_text=re.compile(r"^1$")).nth(1), 'click', 'Select 1 as buy groups')
    safe_action(shared_page, shared_page.locator("#numberOfUnitsToBuyFromEachGroup > .multiselect-dropdown > div > .w-100 > .d-flex.align-items-center > .dropdown-caret"), 'click', 'Open dropdown for units to buy')
    safe_action(shared_page, shared_page.locator("div").filter(has_text=re.compile(r"^1$")).nth(1), 'click', 'Select 1 as units to buy')
    safe_action(shared_page, shared_page.get_by_role("textbox", name="Add Value"), 'click', 'Click on Add Value textbox')
    safe_action(shared_page, shared_page.get_by_role("textbox", name="Add Value"), 'fill', 'Fill Add Value textbox with 34', "34")
    safe_action(shared_page, shared_page.get_by_test_id("group-add").first, 'click', 'Click Add Group button')
    safe_action(shared_page, shared_page.get_by_test_id("product-ids"), 'click', 'Click on Product IDs field')
    safe_action(shared_page, shared_page.get_by_test_id("product-ids"), 'fill', 'Fill Product IDs field with 005DKI004106', "005DKI004106")
    safe_action(shared_page, shared_page.get_by_test_id("save"), 'click', 'Click Save button')

@pytest.mark.order(9)
def test_save_promotion_and_add_groups(shared_page: Page):
    safe_action(shared_page, shared_page.get_by_test_id("group-add"), 'click', 'Click Add Group')
    safe_action(shared_page, shared_page.get_by_test_id("product-ids"), 'click', 'Click on Product IDs field')
    safe_action(shared_page, shared_page.get_by_test_id("product-ids"), 'fill', 'Fill Product IDs field with 022DKI005106', "022DKI005106")
    safe_action(shared_page, shared_page.get_by_test_id("save"), 'click', 'Click Save')
    safe_action(shared_page, shared_page.get_by_test_id("create-promotions-next-button"), 'click', 'Click Next')

@pytest.mark.order(10)
def test_replicate_promotion_settings(shared_page: Page):
    safe_action(shared_page, shared_page.get_by_test_id("replicate"), 'click', 'Click Replicate')
    safe_action(shared_page, shared_page.locator("#attribute_value"), 'click', 'Click on Attribute Value field')
    safe_action(shared_page, shared_page.locator("#attribute_value"), 'fill', 'Fill Attribute Value field with 45', "45")
    safe_action(shared_page, shared_page.locator("#attribute_value"), 'press', 'Press Enter to confirm', "Enter")
    safe_action(shared_page, shared_page.locator("#end_date"), 'click', 'Click on End Date field')
    safe_action(shared_page, shared_page.get_by_text("18"), 'click', 'Select 18th day as end date')
    safe_action(shared_page, shared_page.get_by_role("gridcell", name="$ (1.00000)"), 'click', 'Click on grid cell with $ (1.00000)')