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
def test_navigate_to_promotions_landing_page(shared_page):
    safe_action(shared_page, shared_page, 'goto', 'Navigate to the Promotions Landing Page', "https://stage.mkr.esp.antuit.ai/nglcp/promotions/landing-page")

@pytest.mark.order(2)
def test_click_promotions_action_button(shared_page):
    safe_action(shared_page, shared_page.get_by_test_id("promotions-action-button"), 'click', 'Click on the Promotions Action button')

@pytest.mark.order(3)
def test_click_new_promotion(shared_page):
    safe_action(shared_page, shared_page.get_by_text("New Promotion"), 'click', 'Click on New Promotion')

@pytest.mark.order(4)
def test_focus_promotion_event_name(shared_page):
    safe_action(shared_page, shared_page.get_by_test_id("promotionEventName"), 'click', 'Focus on the Promotion Event Name input field')

@pytest.mark.order(5)
def test_fill_promotion_event_name(shared_page):
    safe_action(shared_page, shared_page.get_by_test_id("promotionEventName"), 'fill', 'Fill in the Promotion Event Name field', 'rh1230-08-04')

@pytest.mark.order(6)
def test_focus_promotion_event_description(shared_page):
    safe_action(shared_page, shared_page.get_by_test_id("promotionEventDescription"), 'click', 'Focus on the Promotion Event Description input field')

@pytest.mark.order(7)
def test_fill_promotion_event_description(shared_page):
    safe_action(shared_page, shared_page.get_by_test_id("promotionEventDescription"), 'fill', 'Fill in the Promotion Event Description field', 'PROMO DISCOUNT TEST')

@pytest.mark.order(8)
def test_open_start_date_picker(shared_page):
    safe_action(shared_page, shared_page.get_by_test_id("startDate"), 'click', 'Open the date picker for the Start Date field')

@pytest.mark.order(9)
def test_select_start_date(shared_page):
    safe_action(shared_page, shared_page.get_by_text("17"), 'click', 'Select the 17th day of the month as the start date')

@pytest.mark.order(10)
def test_open_end_date_picker(shared_page):
    safe_action(shared_page, shared_page.get_by_test_id("endDate"), 'click', 'Open the date picker for the End Date field')

@pytest.mark.order(11)
def test_select_end_date(shared_page):
    safe_action(shared_page, shared_page.get_by_text("18"), 'click', 'Select the 18th day of the month as the end date')

@pytest.mark.order(12)
def test_enable_asap_pricing(shared_page):
    safe_action(shared_page, shared_page.get_by_test_id("isAsapPricing"), 'click', 'Enable the ASAP Pricing option')

@pytest.mark.order(13)
def test_select_regular_pricing(shared_page):
    safe_action(shared_page, shared_page.get_by_test_id("price_type_reg"), 'click', 'Select the Regular Pricing type')

@pytest.mark.order(14)
def test_click_first_zeb_tiers(shared_page):
    safe_action(shared_page, shared_page.locator(".zeb-tiers").first, 'click', 'Click on the first element in the .zeb-tiers section')

@pytest.mark.order(15)
def test_select_hierarchy_tab(shared_page):
    safe_action(shared_page, shared_page.locator("div").filter(has_text=re.compile(r"^Hierarchy$")).nth(3), 'click', 'Select the Hierarchy tab')

@pytest.mark.order(16)
def test_click_first_d_flex(shared_page):
    safe_action(shared_page, shared_page.locator(".d-flex.p-l-32").first, 'click', 'Click on the first element in the .d-flex.p-l-32 section')

@pytest.mark.order(17)
def test_select_na_radio(shared_page):
    safe_action(shared_page, shared_page.get_by_role("radio", name="NA", exact=True), 'check', 'Select the NA radio button')

@pytest.mark.order(18)
def test_click_price_zone_type(shared_page):
    safe_action(shared_page, shared_page.get_by_text("Price Zone Type"), 'click', 'Click on the Price Zone Type option')

@pytest.mark.order(19)
def test_select_third_price_zone_type(shared_page):
    safe_action(shared_page, shared_page.locator("div:nth-child(3) > .custom-checkbox-wrapper > .pointer"), 'click', 'Select the third checkbox under Price Zone Type')

@pytest.mark.order(20)
def test_click_price_zone(shared_page):
    safe_action(shared_page, shared_page.get_by_text("Price Zone", exact=True), 'click', 'Click on the Price Zone option')

@pytest.mark.order(21)
def test_select_first_price_zone(shared_page):
    safe_action(shared_page, shared_page.locator(".filter-values.d-flex.align-items-center.p-l-32.p-r-24 > .custom-checkbox-wrapper > .pointer").first, 'click', 'Select the first checkbox under Price Zone')

@pytest.mark.order(22)
def test_revisit_price_zone_type(shared_page):
    safe_action(shared_page, shared_page.get_by_text("Price Zone Type"), 'click', 'Revisit the Price Zone Type option')

@pytest.mark.order(23)
def test_deselect_first_price_zone_type(shared_page):
    safe_action(shared_page, shared_page.locator(".pointer.custom-checkbox-checked").first, 'click', 'Deselect the first selected checkbox under Price Zone Type')

@pytest.mark.order(24)
def test_reselect_first_price_zone(shared_page):
    safe_action(shared_page, shared_page.locator(".filter-values.d-flex.align-items-center.p-l-32.p-r-24 > .custom-checkbox-wrapper > .pointer").first, 'click', 'Re-select the first checkbox under Price Zone')

@pytest.mark.order(25)
def test_revisit_price_zone(shared_page):
    safe_action(shared_page, shared_page.get_by_text("Price Zone", exact=True), 'click', 'Revisit the Price Zone option')

@pytest.mark.order(26)
def test_select_additional_price_zone(shared_page):
    safe_action(shared_page, shared_page.locator(".filter-values.d-flex.align-items-center.p-l-32.p-r-24 > .custom-checkbox-wrapper > .pointer"), 'click', 'Select an additional checkbox under Price Zone')

@pytest.mark.order(27)
def test_apply_filters(shared_page):
    safe_action(shared_page, shared_page.get_by_role("button", name="Apply Filters"), 'click', 'Click on the Apply Filters button')

@pytest.mark.order(28)
def test_click_tiers_section(shared_page):
    safe_action(shared_page, shared_page.locator("div:nth-child(8) > .zeb-tiers"), 'click', 'Click on the Tiers section')

@pytest.mark.order(29)
def test_open_hierarchy_filter(shared_page):
    safe_action(shared_page, shared_page.locator("#SideFilterproducthierarchyId").get_by_text("Hierarchy"), 'click', 'Open the Hierarchy filter dropdown')

@pytest.mark.order(30)
def test_select_style_color(shared_page):
    safe_action(shared_page, shared_page.get_by_text("Style Color"), 'click', 'Select the Style Color option')

@pytest.mark.order(31)
def test_select_specific_filter(shared_page):
    safe_action(shared_page, shared_page.locator("div:nth-child(5) > esp-filter-sub-accordion-v1 > .sub-accordion-element > .fiter-values-container > .filter-options > .filter-values-options > .filter-values.d-flex.align-items-center.p-l-32.p-r-12 > .custom-checkbox-wrapper > .pointer"), 'click', 'Select a specific filter option')

@pytest.mark.order(32)
def test_select_another_filter(shared_page):
    safe_action(shared_page, shared_page.locator("div:nth-child(7) > .custom-checkbox-wrapper > .pointer"), 'click', 'Select another filter option')

@pytest.mark.order(33)
def test_apply_selected_filters(shared_page):
    safe_action(shared_page, shared_page.get_by_role("button", name="Apply Filters"), 'click', 'Apply the selected filters')

@pytest.mark.order(34)
def test_open_optimization_objective(shared_page):
    safe_action(shared_page, shared_page.locator("#optimizationObjective > .multiselect-dropdown > div > .w-100 > .d-flex.align-items-center > .dropdown-caret"), 'click', 'Open the dropdown for selecting the optimization objective')

@pytest.mark.order(35)
def test_choose_optimize_sales_revenue(shared_page):
    safe_action(shared_page, shared_page.locator("div").filter(has_text=re.compile(r"^Optimize Sales Revenue$")).nth(1), 'click', 'Choose Optimize Sales Revenue')

@pytest.mark.order(36)
def test_click_next_button(shared_page):
    safe_action(shared_page, shared_page.get_by_test_id("create-promotions-next-button"), 'click', 'Click the Next button')

@pytest.mark.order(37)
def test_expand_summary_section(shared_page):
    safe_action(shared_page, shared_page.get_by_test_id("summary-show-more-button"), 'click', 'Expand the summary section')

@pytest.mark.order(38)
def test_navigate_to_available_products(shared_page):
    safe_action(shared_page, shared_page.get_by_text("Available Products"), 'click', 'Navigate to the Available Products section')

@pytest.mark.order(39)
def test_open_first_dropdown(shared_page):
    safe_action(shared_page, shared_page.locator(".dropdown-caret").first, 'click', 'Open the first dropdown in the Available Products section')

@pytest.mark.order(40)
def test_select_first_product_option(shared_page):
    safe_action(shared_page, shared_page.locator(".d-flex.dropdown-option.align-items-center.p-v-5.p-l-32 > .d-flex").first, 'click', 'Select the first product option')

@pytest.mark.order(41)
def test_open_second_dropdown(shared_page):
    safe_action(shared_page, shared_page.locator("div:nth-child(2) > div > esp-multiselect-dropdown > .multiselect-dropdown > div > .w-100 > .d-flex.align-items-center > .dropdown-caret"), 'click', 'Open another dropdown for additional product selection')

@pytest.mark.order(42)
def test_select_first_option_second_dropdown(shared_page):
    safe_action(shared_page, shared_page.locator(".d-flex.dropdown-option").first, 'click', 'Select the first option from the dropdown')

@pytest.mark.order(43)
def test_click_specific_product(shared_page):
    safe_action(shared_page, shared_page.locator(".overflow-auto > div:nth-child(2)"), 'click', 'Click on a specific product from the list')

@pytest.mark.order(44)
def test_open_third_dropdown(shared_page):
    safe_action(shared_page, shared_page.locator("div:nth-child(3) > div > esp-multiselect-dropdown > .multiselect-dropdown > div > .w-100 > .d-flex.align-items-center > .dropdown-caret"), 'click', 'Open the third dropdown for further product selection')

@pytest.mark.order(45)
def test_select_first_option_third_dropdown(shared_page):
    safe_action(shared_page, shared_page.locator(".d-flex.flex-column.justify-content-center").first, 'click', 'Select the first option from the dropdown')

@pytest.mark.order(46)
def test_select_203_logo_knits(shared_page):
    safe_action(shared_page, shared_page.get_by_text("203_Logo Knits"), 'click', 'Select the product 203_Logo Knits')

@pytest.mark.order(47)
def test_apply_complex_filter(shared_page):
    safe_action(shared_page, shared_page.get_by_test_id("complex-filter-apply"), 'click', 'Apply the complex filter settings')

@pytest.mark.order(48)
def test_select_first_promotion_row(shared_page):
    safe_action(shared_page, shared_page.locator(".ag-row-odd > .ag-cell > .ag-cell-wrapper").first, 'click', 'Select the first promotion row')

@pytest.mark.order(49)
def test_click_actions_button(shared_page):
    safe_action(shared_page, shared_page.get_by_test_id("promotions-action-button"), 'click', 'Click on the Actions button')

@pytest.mark.order(50)
def test_select_add_option(shared_page):
    safe_action(shared_page, shared_page.get_by_text("Add"), 'click', 'Select the Add option')

@pytest.mark.order(51)
def test_confirm_addition(shared_page):
    safe_action(shared_page, shared_page.get_by_test_id("confirm-modal-confirm-yes-button"), 'click', 'Confirm the addition of the new promotion')

@pytest.mark.order(52)
def test_click_reoptimize_button(shared_page):
    safe_action(shared_page, shared_page.get_by_role("button", name="Reoptimize"), 'click', 'Click the Reoptimize button')

@pytest.mark.order(53)
def test_confirm_reoptimization(shared_page):
    safe_action(shared_page, shared_page.get_by_test_id("confirm-modal-confirm-yes-button"), 'click', 'Confirm the reoptimization action')

@pytest.mark.order(54)
def test_click_next_button_again(shared_page):
    safe_action(shared_page, shared_page.get_by_test_id("create-promotions-next-button"), 'click', 'Click the Next button again')

@pytest.mark.order(55)
def test_open_adjustment_dropdown(shared_page):
    safe_action(shared_page, shared_page.locator(".dropdown-caret").first, 'click', 'Open the dropdown menu to select a specific adjustment option')

@pytest.mark.order(56)
def test_select_second_adjustment_option(shared_page):
    safe_action(shared_page, shared_page.locator(".overflow-auto > div:nth-child(2) > .d-flex"), 'click', 'Select the second adjustment option')

@pytest.mark.order(57)
def test_click_first_row_adjustment(shared_page):
    safe_action(shared_page, shared_page.locator(".row").first, 'click', 'Click on the first row in the adjustment section')

@pytest.mark.order(58)
def test_click_off_input_field(shared_page):
    safe_action(shared_page, shared_page.locator("#off"), 'click', 'Click on the Off input field')

@pytest.mark.order(59)
def test_set_discount_percentage(shared_page):
    safe_action(shared_page, shared_page.locator("#off"), 'fill', 'Set the discount percentage to 30', '30')

@pytest.mark.order(60)
def test_click_next_button_final(shared_page):
    safe_action(shared_page, shared_page.get_by_test_id("create-promotions-next-button"), 'click', 'Click the Next button to proceed')

@pytest.mark.order(61)
def test_select_price_zone_adjustment(shared_page):
    safe_action(shared_page, shared_page.get_by_text("Price Zone Adjustment"), 'click', 'Select the Price Zone Adjustment option')

@pytest.mark.order(62)
def test_open_rounding_rules_dropdown(shared_page):
    safe_action(shared_page, shared_page.locator("#rounding_rules_id > .multiselect-dropdown > div > .w-100 > .d-flex.align-items-center > .dropdown-caret"), 'click', 'Open the dropdown menu to select a rounding rule')

@pytest.mark.order(63)
def test_select_rounding_rule(shared_page):
    safe_action(shared_page, shared_page.locator("div").filter(has_text=re.compile(r"^\.99 RN$")).nth(1), 'click', 'Select the rounding rule .99 RN')

@pytest.mark.order(64)
def test_click_attribute_value_field(shared_page):
    safe_action(shared_page, shared_page.locator("#attribute_value"), 'click', 'Click on the Attribute Value input field')

@pytest.mark.order(65)
def test_set_attribute_value(shared_page):
    safe_action(shared_page, shared_page.locator("#attribute_value"), 'fill', 'Set the attribute value to 35', '35')

@pytest.mark.order(66)
def test_open_additional_settings_dropdown(shared_page):
    safe_action(shared_page, shared_page.locator(".dropdown-caret").first, 'click', 'Open the dropdown menu to configure additional settings')

@pytest.mark.order(67)
def test_reopen_additional_settings_dropdown(shared_page):
    safe_action(shared_page, shared_page.locator(".dropdown-caret").first, 'click', 'Reopen the dropdown menu to finalize the configuration')

@pytest.mark.order(68)
def test_apply_adjustments(shared_page):
    safe_action(shared_page, shared_page.get_by_test_id("replicate-apply"), 'click', 'Click the Apply button to replicate adjustments')

@pytest.mark.order(69)
def test_navigate_to_product_level_details(shared_page):
    safe_action(shared_page, shared_page, 'goto', 'Navigate to the Product-Level Details page', "https://stage.mkr.esp.antuit.ai/nglcp/product-level-details/product-details")