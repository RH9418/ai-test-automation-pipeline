import re
import time
import random
from playwright.sync_api import Playwright, sync_playwright, expect

def safe_action(action, description: str):
    """
    Wraps a Playwright action in a try-except block and adds a random wait time.
    
    Args:
        action: A lambda function containing the Playwright action to perform.
        description: A human-readable description of the action for logging.
    """
    try:
        action()
        print(f"✅ SUCCESS: {description}")
    except Exception as e:
        print(f"❌ ERROR: Failed to {description}.")
        # To see the detailed error from Playwright, uncomment the line below
        # print(f"   └── Details: {e}")
    finally:
        # Add a random delay between 3 and 5 seconds after every action
        wait_time = random.uniform(3, 5)
        print(f"   └── Pausing for {wait_time:.2f} seconds...")
        time.sleep(wait_time)

def run(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()

    safe_action(lambda: page.goto("https://stage.mkr.esp.antuit.ai/nglcp/promotions/landing-page"), "Navigate to promotions landing page")

    mfa_message = """
================================================================================
  ACTION REQUIRED: MANUAL LOGIN & MFA
--------------------------------------------------------------------------------
  The script is now paused. Please complete the following in the browser window:
  1. Log in with your credentials.
  2. Complete the Multi-Factor Authentication (MFA) step.
  3. Wait for the application's main dashboard or landing page to fully load.

  ---> PRESS [ENTER] IN THIS TERMINAL WHEN YOU ARE READY TO PROCEED <---
================================================================================
"""
    print(mfa_message)
    input()

    print("\n🚀 Starting automated actions...")
    
    # --- Start of All Automated Actions with Error Handling and Delays ---

    safe_action(lambda: page.get_by_test_id("promotions-action-button").click(), "Click promotions action button")
    safe_action(lambda: page.get_by_text("New Promotion").click(), "Click 'New Promotion'")
    
    # Fill Promotion Details
    safe_action(lambda: page.get_by_test_id("promotionEventName").click(), "Click promotion event name field")
    safe_action(lambda: page.get_by_test_id("promotionEventName").fill("rh"), "Fill promotion name with 'rh'")
    safe_action(lambda: page.get_by_test_id("promotionEventName").click(), "Click promotion event name field again")
    safe_action(lambda: page.get_by_test_id("promotionEventName").fill("rh06041025"), "Update promotion name to 'rh06041025'")
    safe_action(lambda: page.get_by_test_id("promotionEventDescription").click(), "Click promotion description field")
    safe_action(lambda: page.get_by_test_id("promotionEventDescription").fill("Test Promotion"), "Fill promotion description")

    # Date Selection
    safe_action(lambda: page.get_by_test_id("startDate").click(), "Click start date field")
    safe_action(lambda: page.get_by_role("button", name="April").click(), "Click month 'April' button")
    safe_action(lambda: page.get_by_text("April").click(), "Select 'April'")
    safe_action(lambda: page.get_by_role("button", name="2026").click(), "Click year '2026' button")
    safe_action(lambda: page.get_by_text("2026").click(), "Select '2026'")
    safe_action(lambda: page.get_by_text("April").click(), "Select 'April' again")
    safe_action(lambda: page.get_by_text("15").click(), "Select start day '15'")
    safe_action(lambda: page.get_by_test_id("endDate").click(), "Click end date field")
    safe_action(lambda: page.get_by_text("22").click(), "Select end day '22'")

    # Ticket and Price Type
    safe_action(lambda: page.get_by_test_id("isAsapPricing").click(), "Click 'ASAP Pricing'")
    safe_action(lambda: page.get_by_test_id("ticket_type_current").click(), "Select ticket type 'Current'")
    safe_action(lambda: page.get_by_test_id("price_type_all").click(), "Select price type 'All'")

    # Location Selection
    safe_action(lambda: page.get_by_role("textbox", name="Select Locations").click(), "Open location selection dialog")
    safe_action(lambda: page.locator("div").filter(has_text=re.compile(r"^Hierarchy$")).nth(3).click(), "Click 'Hierarchy' filter")
    safe_action(lambda: page.get_by_text("Region", exact=True).click(), "Select 'Region' hierarchy")
    safe_action(lambda: page.get_by_role("radio", name="EUR").check(), "Check 'EUR' region")
    safe_action(lambda: page.get_by_role("radio", name="NA", exact=True).check(), "Check 'NA' region")
    safe_action(lambda: page.locator("div:nth-child(3) > esp-filter-sub-accordion-v1 > .sub-accordion-element > .d-flex").click(), "Click 3rd sub-accordion for location")
    safe_action(lambda: page.locator(".pointer.custom-checkbox-unchecked").first.click(), "Click first unchecked location checkbox")
    safe_action(lambda: page.locator("div:nth-child(4) > esp-filter-sub-accordion-v1 > .sub-accordion-element > .d-flex").click(), "Click 4th sub-accordion for location")
    safe_action(lambda: page.locator(".pointer.custom-checkbox-unchecked").first.click(), "Click first unchecked location checkbox again")
    safe_action(lambda: page.locator("#SideFilterlocationhierarchyId div").filter(has_text=re.compile(r"^Hierarchy$")).click(), "Click side filter hierarchy")
    safe_action(lambda: page.locator("div").filter(has_text=re.compile(r"^Hierarchy$")).nth(3).click(), "Click 'Hierarchy' filter again")
    safe_action(lambda: page.locator("#SideFilterlocationhierarchyId div").filter(has_text=re.compile(r"^Hierarchy$")).click(), "Click side filter hierarchy again")
    safe_action(lambda: page.get_by_role("dialog", name="Manage Selection Location").click(), "Click 'Manage Selection Location' dialog")
    safe_action(lambda: page.locator(".zeb-tiers").first.click(), "Click first '.zeb-tiers' element")
    safe_action(lambda: page.get_by_role("dialog", name="Manage Selection Location").click(), "Click 'Manage Selection Location' dialog again")

    # Store Sets Selection
    safe_action(lambda: page.locator("#locationsAndProducts").get_by_text("Store Sets").click(), "Switch to 'Store Sets' tab")
    safe_action(lambda: page.locator(".zeb-tiers").first.click(), "Click first '.zeb-tiers' element in Store Sets")
    safe_action(lambda: page.locator("#SideFilterstore_sethierarchyId > esp-filter-accordion-v1 > .filter-accordion-element > .accordion-label").click(), "Click accordion label for store set hierarchy")
    safe_action(lambda: page.locator("#SideFilterstore_sethierarchyId").get_by_text("Store Sets").click(), "Click 'Store Sets' in side filter")
    safe_action(lambda: page.get_by_role("radio", name="NA All Store Set").check(), "Check 'NA All Store Set'")
    safe_action(lambda: page.get_by_text("Store Sets 1 Selected").click(), "Confirm '1 Selected' for Store Sets")
    safe_action(lambda: page.locator("div:nth-child(3) > esp-filter-sub-accordion-v1 > .sub-accordion-element > .d-flex").click(), "Click 3rd sub-accordion for store sets")
    safe_action(lambda: page.locator(".pointer.custom-checkbox-unchecked").first.click(), "Click first unchecked store set checkbox")
    safe_action(lambda: page.get_by_role("dialog", name="Manage Selection Location").click(), "Click 'Manage Selection Location' dialog again")
    safe_action(lambda: page.get_by_text("Paste Price Zone").click(), "Click 'Paste Price Zone'")
    safe_action(lambda: page.locator("#locationsAndProducts").get_by_text("Store Sets").click(), "Switch back to 'Store Sets' tab")

    # Optimization and Discounts
    safe_action(lambda: page.locator("#optimizationObjective > .multiselect-dropdown > div > .w-100 > .d-flex.align-items-center > .dropdown-caret").click(), "Open optimization objective dropdown")
    safe_action(lambda: page.locator("div").filter(has_text=re.compile(r"^Optimize Sales Revenue$")).first.click(), "Select 'Optimize Sales Revenue'")
    safe_action(lambda: page.get_by_test_id("minSellThruPercent").click(), "Click Min Sell Thru % field")
    safe_action(lambda: page.get_by_test_id("minSellThruPercent").fill("10"), "Fill Min Sell Thru %")
    safe_action(lambda: page.get_by_test_id("minMarginPercent").click(), "Click Min Margin % field")
    safe_action(lambda: page.get_by_test_id("minMarginPercent").fill("10"), "Fill Min Margin %")
    safe_action(lambda: page.get_by_test_id("minDiscountPercent").click(), "Click Min Discount % field")
    safe_action(lambda: page.get_by_test_id("minDiscountPercent").fill("15"), "Fill Min Discount %")
    safe_action(lambda: page.get_by_test_id("maxDiscountPercent").click(), "Click Max Discount % field")
    safe_action(lambda: page.get_by_test_id("maxDiscountPercent").fill("20"), "Fill Max Discount %")

    # Final Adjustment and Naming
    safe_action(lambda: page.get_by_text("2", exact=True).click(), "Click tab '2'")
    safe_action(lambda: page.get_by_test_id("promotionEventName").click(), "Click promotion event name field")
    for _ in range(9): # Press ArrowLeft 9 times
        safe_action(lambda: page.get_by_test_id("promotionEventName").press("ArrowLeft"), "Press Left Arrow on promotion name")
    safe_action(lambda: page.get_by_test_id("promotionEventName").fill("Test-rh06041025"), "Update final promotion name")

    print("\n🚀 Script execution completed.")
    
    # ---------------------
    context.close()
    browser.close()

with sync_playwright() as playwright:
    run(playwright)
