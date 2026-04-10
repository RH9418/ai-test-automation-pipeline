
import os
import sys
import time
import random
import re
from datetime import datetime
from playwright.sync_api import sync_playwright, Playwright, expect, TimeoutError

# --- Screenshot Directory Setup ---
SCREENSHOT_DIR = r"Test_Screenshots/promo_threshold"
if not os.path.exists(SCREENSHOT_DIR):
    os.makedirs(SCREENSHOT_DIR)
screenshot_counter = 0

def capture_annotated_screenshot(page, locator, full_action_description: str):
    '''Highlights element with a thick red box and glow, then captures screenshot.'''
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
        page.evaluate('''() => {
            document.getElementById('ge-spotlight-box')?.remove();
            document.getElementById('ge-spotlight-label')?.remove();
        }''')
    except Exception as e:
        print(f"   └── ⚠️ Screenshot Error: {e}")

def safe_action(page, locator, action_name: str, description: str, *action_args, **action_kwargs):
    '''Performs action with spotlight screenshots and manual fallbacks.'''
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
            
        if action_name == 'close':
            try: locator.close()
            except: pass
            print(f"✅ SUCCESS: {description} (Teardown handled by Pytest)")
            return
            
        if locator != page:
            capture_annotated_screenshot(page, locator, full_desc)
            
        # Execution
        action_func = getattr(locator, action_name)
        action_func(*action_args, **action_kwargs)
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
    safe_action(page, page, 'goto', 'Navigate to https://stage.mkr.esp.antuit.ai/nglcp/promotions/create-promotions', 'https://stage.mkr.esp.antuit.ai/nglcp/promotions/create-promotions')

    print('''
================================================================================
  ACTION REQUIRED: MANUAL LOGIN & MFA
--------------------------------------------------------------------------------
  1. Log in manually. 2. Complete MFA. 3. Wait for dashboard to load.
  ---> PRESS [ENTER] IN THIS TERMINAL WHEN READY <---
================================================================================
''')
    input()
    print("\n🚀 Starting automated actions...")
    safe_action(page, page.get_by_test_id("promotionEventName"), 'click', "get_by_test_id(\"promotionEventName\")", )
    safe_action(page, page.get_by_test_id("promotionEventName"), 'fill', "get_by_test_id(\"promotionEventName\")", "rh--1220--0904")
    safe_action(page, page.get_by_test_id("promotionEventDescription"), 'click', "get_by_test_id(\"promotionEventDescription\")", )
    safe_action(page, page.get_by_test_id("promotionEventDescription"), 'fill', "get_by_test_id(\"promotionEventDescription\")", "PROMO THRESHOLD")
    safe_action(page, page.get_by_test_id("startDate"), 'click', "get_by_test_id(\"startDate\")", )
    safe_action(page, page.get_by_text("10", exact=True), 'click', "get_by_text(\"10\", exact=True)", )
    safe_action(page, page.get_by_test_id("endDate"), 'click', "get_by_test_id(\"endDate\")", )
    safe_action(page, page.get_by_text("17"), 'click', "get_by_text(\"17\")", )
    safe_action(page, page.get_by_test_id("isAsapPricing"), 'click', "get_by_test_id(\"isAsapPricing\")", )
    safe_action(page, page.locator(".zeb-tiers").first, 'click', "locator(\".zeb-tiers\").first", )
    safe_action(page, page.locator("#SideFilterlocationhierarchyId").get_by_text("Hierarchy"), 'click', "locator(\"#SideFilterlocationhierarchyId\").get_by_text(\"Hierarchy\")", )
    safe_action(page, page.get_by_text("Region", exact=True), 'click', "get_by_text(\"Region\", exact=True)", )
    safe_action(page, page.get_by_role("radio", name="NA", exact=True), 'check', "get_by_role(\"radio\", name=\"NA\", exact=True)", )
    safe_action(page, page.get_by_text("Price Zone Type"), 'click', "get_by_text(\"Price Zone Type\")", )
    safe_action(page, page.locator("div").filter(has_text=re.compile(r"^Collection$")), 'click', "locator(\"div\").filter(has_text=re.compile(r\"^Collection$\"))", )
    safe_action(page, page.get_by_text("Price Zone", exact=True), 'click', "get_by_text(\"Price Zone\", exact=True)", )
    safe_action(page, page.get_by_text("1_US Collection"), 'click', "get_by_text(\"1_US Collection\")", )
    safe_action(page, page.get_by_role("button", name="Apply Filters"), 'click', "get_by_role(\"button\", name=\"Apply Filters\")", )
    safe_action(page, page.get_by_role("textbox", name="Select Products"), 'click', "get_by_role(\"textbox\", name=\"Select Products\")", )
    safe_action(page, page.locator("#SideFilterproducthierarchyId").get_by_text("Hierarchy"), 'click', "locator(\"#SideFilterproducthierarchyId\").get_by_text(\"Hierarchy\")", )
    safe_action(page, page.get_by_text("Style Color"), 'click', "get_by_text(\"Style Color\")", )
    safe_action(page, page.locator("div:nth-child(5) > esp-filter-sub-accordion-v1 > .sub-accordion-element > .fiter-values-container > .filter-options > .filter-values-options > .filter-values.d-flex.align-items-center.p-l-32.p-r-12 > .custom-checkbox-wrapper"), 'click', "locator(\"div:nth-child(5) > esp-filter-sub-accordion-v1 > .sub-accordion-element > .fiter-values-container > .filter-options > .filter-values-options > .filter-values.d-flex.align-items-center.p-l-32.p-r-12 > .custom-checkbox-wrapper\")", )
    safe_action(page, page.locator("div:nth-child(5) > esp-filter-sub-accordion-v1 > .sub-accordion-element > .fiter-values-container > .filter-options > .filter-values-options > div:nth-child(2) > .custom-checkbox-wrapper > .pointer"), 'click', "locator(\"div:nth-child(5) > esp-filter-sub-accordion-v1 > .sub-accordion-element > .fiter-values-container > .filter-options > .filter-values-options > div:nth-child(2) > .custom-checkbox-wrapper > .pointer\")", )
    safe_action(page, page.locator(".pointer.custom-checkbox-unchecked").first, 'click', "locator(\".pointer.custom-checkbox-unchecked\").first", )
    safe_action(page, page.get_by_role("button", name="Apply Filters"), 'click', "get_by_role(\"button\", name=\"Apply Filters\")", )
    safe_action(page, page.locator("#optimizationObjective > .multiselect-dropdown > div > .w-100"), 'click', "locator(\"#optimizationObjective > .multiselect-dropdown > div > .w-100\")", )
    safe_action(page, page.locator("div").filter(has_text=re.compile(r"^Optimize for Sales Unit$")).nth(1), 'click', "locator(\"div\").filter(has_text=re.compile(r\"^Optimize for Sales Unit$\")).nth(1)", )
    safe_action(page, page.get_by_test_id("create-promotions-next-button"), 'click', "get_by_test_id(\"create-promotions-next-button\")", )
    safe_action(page, page.get_by_text("Available Products"), 'click', "get_by_text(\"Available Products\")", )
    safe_action(page, page.get_by_text("Show More"), 'click', "get_by_text(\"Show More\")", )
    safe_action(page, page.get_by_test_id("create-promotions-next-button"), 'click', "get_by_test_id(\"create-promotions-next-button\")", )
    safe_action(page, page.locator(".w-100.p-h-16").first, 'click', "locator(\".w-100.p-h-16\").first", )
    safe_action(page, page.get_by_text("Bundle"), 'click', "get_by_text(\"Bundle\")", )
    safe_action(page, page.get_by_text("Threshold"), 'click', "get_by_text(\"Threshold\")", )
    safe_action(page, page.locator(".d-flex.flex-column.justify-content-center.font-size-10.align-items-center.checkbox-v2.m-r-10.zeb-check").first, 'click', "locator(\".d-flex.flex-column.justify-content-center.font-size-10.align-items-center.checkbox-v2.m-r-10.zeb-check\").first", )
    safe_action(page, page.get_by_text("What type of promotion(s) would you like to compare? *Max limit 5Promo Type"), 'click', "get_by_text(\"What type of promotion(s) would you like to compare? *Max limit 5Promo Type\")", )
    safe_action(page, page.get_by_test_id("spend_amount"), 'click', "get_by_test_id(\"spend_amount\")", )
    safe_action(page, page.get_by_test_id("spend_amount"), 'fill', "get_by_test_id(\"spend_amount\")", "5000")
    safe_action(page, page.locator("#get"), 'click', "locator(\"#get\")", )
    safe_action(page, page.locator("#get"), 'fill', "locator(\"#get\")", "25")
    safe_action(page, page.get_by_test_id("create-promotions-next-button"), 'click', "get_by_test_id(\"create-promotions-next-button\")", )
    safe_action(page, page.get_by_text("Price Zone Adjustment"), 'click', "get_by_text(\"Price Zone Adjustment\")", )
    safe_action(page, page.get_by_test_id("replicate-apply"), 'click', "get_by_test_id(\"replicate-apply\")", )
    page.goto("https://stage.mkr.esp.antuit.ai/nglcp/product-level-details/product-details")
    safe_action(page, page.get_by_role("button", name="Close"), 'click', "get_by_role(\"button\", name=\"Close\")", )
    safe_action(page, page.get_by_test_id("submit-all-for-approval"), 'click', "get_by_test_id(\"submit-all-for-approval\")", )
    safe_action(page, page.get_by_test_id("confirm-modal-confirm-yes-button"), 'click', "get_by_test_id(\"confirm-modal-confirm-yes-button\")", )
    safe_action(page, page.get_by_role("button", name="Actions"), 'click', "get_by_role(\"button\", name=\"Actions\")", )
    safe_action(page, page.get_by_text("Approve", exact=True), 'click', "get_by_text(\"Approve\", exact=True)", )
    safe_action(page, page.get_by_test_id("confirm-modal-confirm-yes-button"), 'click', "get_by_test_id(\"confirm-modal-confirm-yes-button\")", )
    safe_action(page, page.get_by_role("button", name="Actions"), 'click', "get_by_role(\"button\", name=\"Actions\")", )
    safe_action(page, page.get_by_text("Reject"), 'click', "get_by_text(\"Reject\")", )
    safe_action(page, page.get_by_test_id("confirm-modal-confirm-yes-button"), 'click', "get_by_test_id(\"confirm-modal-confirm-yes-button\")", )
    safe_action(page, page.get_by_role("button", name="Actions"), 'click', "get_by_role(\"button\", name=\"Actions\")", )
    safe_action(page, page.get_by_text("Withdraw", exact=True), 'click', "get_by_text(\"Withdraw\", exact=True)", )
    safe_action(page, page.get_by_test_id("confirm-modal-confirm-yes-button"), 'click', "get_by_test_id(\"confirm-modal-confirm-yes-button\")", )
    safe_action(page, page.get_by_test_id("create-promotions-next-button"), 'click', "get_by_test_id(\"create-promotions-next-button\")", )
    page.close()

    # ---------------------
    context.close()
    browser.close()


with sync_playwright() as playwright:
    run(playwright)
