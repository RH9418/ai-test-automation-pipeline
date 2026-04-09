
import os
import sys
import time
import random
import re
from datetime import datetime
from playwright.sync_api import sync_playwright, Playwright, expect, TimeoutError

# --- Screenshot Directory Setup ---
SCREENSHOT_DIR = r"Test_Screenshots/promo_main"
if not os.path.exists(SCREENSHOT_DIR):
    os.makedirs(SCREENSHOT_DIR)
screenshot_counter = 0

def capture_annotated_screenshot(page, locator, full_action_description: str):
    """Highlights element with a thick red box and glow, then captures screenshot."""
    global screenshot_counter
    screenshot_counter += 1
    
    try:
        # 1. Force element into view so the agent can see it
        locator.scroll_into_view_if_needed()
        locator.wait_for(state='visible', timeout=5000)
        
        box = locator.bounding_box()
        if not box:
            print(f"   └── ⚠️ Screenshot Warning: Bounding box null for '{full_action_description}'.")
            return
            
        js_description = full_action_description.replace("'", "\\'")
        # 2. Inject a high-visibility "Spotlight" annotation
        page.evaluate(f'''(params) => {{
            const {{ box, desc }} = params;
            
            // Create High-Visibility Box
            const div = document.createElement('div');
            div.id = 'ge-spotlight-box';
            div.style.position = 'absolute';
            div.style.left = `${{box.x}}px`;
            div.style.top = `${{box.y}}px`;
            div.style.width = `${{box.width}}px`;
            div.style.height = `${{box.height}}px`;
            div.style.border = '5px solid #FF0000'; // Thick Red
            div.style.boxShadow = '0 0 15px 5px rgba(255, 0, 0, 0.7)'; // Red Glow
            div.style.boxSizing = 'border-box';
            div.style.zIndex = '2147483647';
            div.style.pointerEvents = 'none'; // Don't interfere with clicks
            
            // Create High-Contrast Label
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
            label.style.fontFamily = 'Arial, sans-serif';
            document.body.appendChild(div);
            document.body.appendChild(label);
        }}''', {'box': box, 'desc': js_description})
        
        # 3. Small sleep to allow the browser to 'paint' the red box
        time.sleep(0.2)
        timestamp = datetime.now().strftime("%H-%M-%S")
        safe_filename = re.sub(r'[^a-z0-9]', '_', full_action_description.lower())[:40]
        filename = f"{timestamp}_{screenshot_counter:02d}_{safe_filename}.png"
        path = os.path.join(SCREENSHOT_DIR, filename)
        
        # Capture the screen
        page.screenshot(path=path, full_page=False) # Full page can sometimes blur annotations
        print(f"   └── 📸 Screenshot saved: {path}")
        
        # 4. Clean up
        page.evaluate("""() => {
            document.getElementById('ge-spotlight-box')?.remove();
            document.getElementById('ge-spotlight-label')?.remove();
        }""")
    except Exception as e:
        print(f"   └── ⚠️ Screenshot Error: {e}")

def safe_action(page, locator, action_name: str, description: str, *action_args):
    """Performs action with spotlight screenshots and manual fallbacks."""
    full_desc = f"{action_name.capitalize()}: {description}"
    if action_name == 'fill':
        full_desc += f" with '{action_args[0] if action_args else ''}'"
        
    try:
        # Pre-Fill Intervention
        if action_name == 'fill':
            print(f"\n⏸️ PAUSING FOR INPUT: About to fill '{description}'.")
            input("   └── Perform input manually in browser, then PRESS [ENTER] to continue...")
            page.wait_for_load_state('networkidle', timeout=5000)
            return

        # Screenshot Logic
        if action_name in ['click', 'dblclick', 'check', 'uncheck', 'hover']:
            try:
                locator.hover(timeout=2000)
                time.sleep(0.3)
            except: pass
            
        capture_annotated_screenshot(page, locator, full_desc)
        
        # Execution
        action_func = getattr(locator, action_name)
        action_func(*action_args)
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


def run(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    safe_action(page, page, 'goto', 'Navigate to https://stage.mkr.esp.antuit.ai/nglcp/promotions/', 'https://stage.mkr.esp.antuit.ai/nglcp/promotions/')

    print("""
================================================================================
  ACTION REQUIRED: MANUAL LOGIN & MFA
--------------------------------------------------------------------------------
  1. Log in manually. 2. Complete MFA. 3. Wait for dashboard to load.
  ---> PRESS [ENTER] IN THIS TERMINAL WHEN READY <---
================================================================================
""")
    input()
    print("\n🚀 Starting automated actions...")
    safe_action(page, page.get_by_test_id("promotions-action-button"), 'click', "get_by_test_id(\"promotions-action-button\")", )
    safe_action(page, page.get_by_text("New Promotion"), 'click', "get_by_text(\"New Promotion\")", )
    safe_action(page, page.get_by_test_id("promotionEventName"), 'click', "get_by_test_id(\"promotionEventName\")", )
    safe_action(page, page.get_by_test_id("promotionEventName"), 'fill', "get_by_test_id(\"promotionEventName\")", "rh-1205070436")
    safe_action(page, page.get_by_test_id("promotionEventDescription"), 'click', "get_by_test_id(\"promotionEventDescription\")", )
    safe_action(page, page.get_by_test_id("promotionEventDescription"), 'fill', "get_by_test_id(\"promotionEventDescription\")", "PROMO TEST 3")
    safe_action(page, page.get_by_test_id("startDate"), 'click', "get_by_test_id(\"startDate\")", )
    safe_action(page, page.get_by_text("9").nth(1), 'click', "get_by_text(\"9\").nth(1)", )
    safe_action(page, page.get_by_test_id("endDate"), 'click', "get_by_test_id(\"endDate\")", )
    safe_action(page, page.get_by_text("12", exact=True), 'click', "get_by_text(\"12\", exact=True)", )
    safe_action(page, page.get_by_test_id("isAsapPricing"), 'click', "get_by_test_id(\"isAsapPricing\")", )
    safe_action(page, page.locator(".zeb-tiers").first, 'click', "locator(\".zeb-tiers\").first", )
    safe_action(page, page.locator("div").filter(has_text=re.compile(r"^Hierarchy$")).nth(3), 'click', "locator(\"div\").filter(has_text=re.compile(r\"^Hierarchy$\")).nth(3)", )
    safe_action(page, page.get_by_text("Region", exact=True), 'click', "get_by_text(\"Region\", exact=True)", )
    safe_action(page, page.get_by_role("radio", name="NA", exact=True), 'check', "get_by_role(\"radio\", name=\"NA\", exact=True)", )
    safe_action(page, page.get_by_text("Price Zone Type"), 'click', "get_by_text(\"Price Zone Type\")", )
    safe_action(page, page.locator(".filter-values.d-flex.align-items-center.p-l-32.p-r-24 > .custom-checkbox-wrapper > .pointer").first, 'click', "locator(\".filter-values.d-flex.align-items-center.p-l-32.p-r-24 > .custom-checkbox-wrapper > .pointer\").first", )
    safe_action(page, page.get_by_text("Price Zone", exact=True), 'click', "get_by_text(\"Price Zone\", exact=True)", )
    safe_action(page, page.locator(".filter-values.d-flex.align-items-center.p-l-32.p-r-24 > .custom-checkbox-wrapper > .pointer"), 'click', "locator(\".filter-values.d-flex.align-items-center.p-l-32.p-r-24 > .custom-checkbox-wrapper > .pointer\")", )
    safe_action(page, page.get_by_role("button", name="Apply Filters"), 'click', "get_by_role(\"button\", name=\"Apply Filters\")", )
    safe_action(page, page.locator("div:nth-child(8) > .zeb-tiers"), 'click', "locator(\"div:nth-child(8) > .zeb-tiers\")", )
    safe_action(page, page.locator("#SideFilterproducthierarchyId").get_by_text("Hierarchy"), 'click', "locator(\"#SideFilterproducthierarchyId\").get_by_text(\"Hierarchy\")", )
    safe_action(page, page.get_by_text("Style Color"), 'click', "get_by_text(\"Style Color\")", )
    safe_action(page, page.locator("div:nth-child(5) > esp-filter-sub-accordion-v1 > .sub-accordion-element > .fiter-values-container > .filter-options > .filter-values-options > .filter-values.d-flex.align-items-center.p-l-32.p-r-12 > .custom-checkbox-wrapper > .pointer"), 'click', "locator(\"div:nth-child(5) > esp-filter-sub-accordion-v1 > .sub-accordion-element > .fiter-values-container > .filter-options > .filter-values-options > .filter-values.d-flex.align-items-center.p-l-32.p-r-12 > .custom-checkbox-wrapper > .pointer\")", )
    safe_action(page, page.locator("div:nth-child(6) > .custom-checkbox-wrapper > .pointer"), 'click', "locator(\"div:nth-child(6) > .custom-checkbox-wrapper > .pointer\")", )
    safe_action(page, page.locator("div:nth-child(5) > .custom-checkbox-wrapper > .pointer"), 'click', "locator(\"div:nth-child(5) > .custom-checkbox-wrapper > .pointer\")", )
    safe_action(page, page.get_by_role("button", name="Apply Filters"), 'click', "get_by_role(\"button\", name=\"Apply Filters\")", )
    safe_action(page, page.locator("#optimizationObjective > .multiselect-dropdown > div > .w-100"), 'click', "locator(\"#optimizationObjective > .multiselect-dropdown > div > .w-100\")", )
    safe_action(page, page.locator("div").filter(has_text=re.compile(r"^Optimize for Sales Unit$")).nth(1), 'click', "locator(\"div\").filter(has_text=re.compile(r\"^Optimize for Sales Unit$\")).nth(1)", )
    safe_action(page, page.get_by_test_id("create-promotions-next-button"), 'click', "get_by_test_id(\"create-promotions-next-button\")", )
    safe_action(page, page.get_by_text("Show More"), 'click', "get_by_text(\"Show More\")", )
    safe_action(page, page.get_by_role("checkbox", name="Column with Header Selection"), 'check', "get_by_role(\"checkbox\", name=\"Column with Header Selection\")", )
    safe_action(page, page.get_by_test_id("promotions-action-button"), 'click', "get_by_test_id(\"promotions-action-button\")", )
    safe_action(page, page.get_by_text("Reset Preferences"), 'click', "get_by_text(\"Reset Preferences\")", )
    safe_action(page, page.get_by_role("textbox", name="Search"), 'click', "get_by_role(\"textbox\", name=\"Search\")", )
    safe_action(page, page.get_by_role("textbox", name="Search"), 'fill', "get_by_role(\"textbox\", name=\"Search\")", "005")
    safe_action(page, page.get_by_role("textbox", name="Search"), 'press', "get_by_role(\"textbox\", name=\"Search\")", "Enter")
    safe_action(page, page.locator("a").nth(1), 'click', "locator(\"a\").nth(1)", )
    safe_action(page, page.get_by_text("Available Products"), 'click', "get_by_text(\"Available Products\")", )
    safe_action(page, page.locator("div:nth-child(3) > div > esp-multiselect-dropdown > .multiselect-dropdown > div > .w-100 > .d-flex.align-items-center > .dropdown-caret"), 'click', "locator(\"div:nth-child(3) > div > esp-multiselect-dropdown > .multiselect-dropdown > div > .w-100 > .d-flex.align-items-center > .dropdown-caret\")", )
    safe_action(page, page.locator("div:nth-child(7) > .d-flex"), 'click', "locator(\"div:nth-child(7) > .d-flex\")", )
    safe_action(page, page.locator(".ag-center-cols-viewport"), 'click', "locator(\".ag-center-cols-viewport\")", )
    safe_action(page, page.locator(".w-100.p-h-16").first, 'click', "locator(\".w-100.p-h-16\").first", )
    safe_action(page, page.locator(".d-flex.dropdown-option.align-items-center.p-v-5.p-l-32").first, 'click', "locator(\".d-flex.dropdown-option.align-items-center.p-v-5.p-l-32\").first", )
    safe_action(page, page.get_by_text("21_Men's Underwear"), 'click', "get_by_text(\"21_Men's Underwear\")", )
    safe_action(page, page.locator("div:nth-child(2) > div > esp-multiselect-dropdown > .multiselect-dropdown > div > .w-100 > .d-flex.align-items-center > .dropdown-caret"), 'click', "locator(\"div:nth-child(2) > div > esp-multiselect-dropdown > .multiselect-dropdown > div > .w-100 > .d-flex.align-items-center > .dropdown-caret\")", )
    safe_action(page, page.locator("div:nth-child(3) > div > esp-multiselect-dropdown > .multiselect-dropdown > div > .w-100 > .d-flex.align-items-center > .dropdown-caret"), 'click', "locator(\"div:nth-child(3) > div > esp-multiselect-dropdown > .multiselect-dropdown > div > .w-100 > .d-flex.align-items-center > .dropdown-caret\")", )
    safe_action(page, page.locator(".d-flex.flex-column.justify-content-center").first, 'click', "locator(\".d-flex.flex-column.justify-content-center\").first", )
    safe_action(page, page.locator(".overflow-auto > div:nth-child(2) > .d-flex"), 'click', "locator(\".overflow-auto > div:nth-child(2) > .d-flex\")", )
    safe_action(page, page.get_by_test_id("complex-filter-apply"), 'click', "get_by_test_id(\"complex-filter-apply\")", )
    safe_action(page, page.locator("#ag-2170-input"), 'check', "locator(\"#ag-2170-input\")", )
    safe_action(page, page.get_by_test_id("promotions-action-button"), 'click', "get_by_test_id(\"promotions-action-button\")", )
    safe_action(page, page.get_by_text("Add"), 'click', "get_by_text(\"Add\")", )
    safe_action(page, page.get_by_test_id("confirm-modal-confirm-yes-button"), 'click', "get_by_test_id(\"confirm-modal-confirm-yes-button\")", )
    safe_action(page, page.get_by_role("button", name="Reoptimize"), 'click', "get_by_role(\"button\", name=\"Reoptimize\")", )
    safe_action(page, page.get_by_test_id("confirm-modal-confirm-yes-button"), 'click', "get_by_test_id(\"confirm-modal-confirm-yes-button\")", )
    safe_action(page, page.get_by_test_id("create-promotions-next-button"), 'click', "get_by_test_id(\"create-promotions-next-button\")", )
    safe_action(page, page.locator(".dropdown-caret").first, 'click', "locator(\".dropdown-caret\").first", )
    safe_action(page, page.get_by_text("BOGO"), 'click', "get_by_text(\"BOGO\")", )
    safe_action(page, page.locator(".row").first, 'click', "locator(\".row\").first", )
    safe_action(page, page.locator("#numberOfBuyGroups > .multiselect-dropdown > div > .w-100 > .d-flex.align-items-center > .dropdown-caret"), 'click', "locator(\"#numberOfBuyGroups > .multiselect-dropdown > div > .w-100 > .d-flex.align-items-center > .dropdown-caret\")", )
    safe_action(page, page.locator("div").filter(has_text=re.compile(r"^1$")).nth(1), 'click', "locator(\"div\").filter(has_text=re.compile(r\"^1$\")).nth(1)", )
    safe_action(page, page.locator("#numberOfUnitsToBuyFromEachGroup > .multiselect-dropdown > div > .w-100 > .d-flex.align-items-center > .dropdown-caret"), 'click', "locator(\"#numberOfUnitsToBuyFromEachGroup > .multiselect-dropdown > div > .w-100 > .d-flex.align-items-center > .dropdown-caret\")", )
    safe_action(page, page.locator("div").filter(has_text=re.compile(r"^1$")).nth(1), 'click', "locator(\"div\").filter(has_text=re.compile(r\"^1$\")).nth(1)", )
    safe_action(page, page.get_by_role("textbox", name="Add Value"), 'click', "get_by_role(\"textbox\", name=\"Add Value\")", )
    safe_action(page, page.get_by_role("textbox", name="Add Value"), 'fill', "get_by_role(\"textbox\", name=\"Add Value\")", "34")
    safe_action(page, page.get_by_test_id("group-add").first, 'click', "get_by_test_id(\"group-add\").first", )
    safe_action(page, page.get_by_test_id("product-ids"), 'click', "get_by_test_id(\"product-ids\")", )
    safe_action(page, page.get_by_test_id("product-ids"), 'fill', "get_by_test_id(\"product-ids\")", "005DKI004106")
    safe_action(page, page.get_by_test_id("save"), 'click', "get_by_test_id(\"save\")", )
    safe_action(page, page.get_by_test_id("group-add"), 'click', "get_by_test_id(\"group-add\")", )
    safe_action(page, page.get_by_test_id("product-ids"), 'click', "get_by_test_id(\"product-ids\")", )
    safe_action(page, page.get_by_test_id("product-ids"), 'fill', "get_by_test_id(\"product-ids\")", "022DKI005106")
    safe_action(page, page.get_by_test_id("save"), 'click', "get_by_test_id(\"save\")", )
    safe_action(page, page.get_by_test_id("create-promotions-next-button"), 'click', "get_by_test_id(\"create-promotions-next-button\")", )
    safe_action(page, page.get_by_test_id("replicate"), 'click', "get_by_test_id(\"replicate\")", )
    safe_action(page, page.locator("#attribute_value"), 'click', "locator(\"#attribute_value\")", )
    safe_action(page, page.locator("#attribute_value"), 'fill', "locator(\"#attribute_value\")", "45")
    safe_action(page, page.locator("#attribute_value"), 'press', "locator(\"#attribute_value\")", "Enter")
    safe_action(page, page.locator("#end_date"), 'click', "locator(\"#end_date\")", )
    safe_action(page, page.get_by_text("18"), 'click', "get_by_text(\"18\")", )
    safe_action(page, page.get_by_role("gridcell", name="$ (1.00000)"), 'click', "get_by_role(\"gridcell\", name=\"$ (1.00000)\")", )
    page.close()

    # ---------------------
    context.close()
    browser.close()


with sync_playwright() as playwright:
    run(playwright)
