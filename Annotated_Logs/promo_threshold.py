import re
from playwright.sync_api import Playwright, sync_playwright, expect


def run(playwright: Playwright) -> None:
    # Launch a Chromium browser instance in non-headless mode for visual debugging.
    browser = playwright.chromium.launch(headless=False)
    # Create a new browser context to isolate cookies, storage, and other session data.
    context = browser.new_context()
    # Open a new page within the created browser context.
    page = context.new_page()
    # Navigate to the 'Create Promotions' page on the staging environment.
    page.goto("https://stage.mkr.esp.antuit.ai/nglcp/promotions/create-promotions")
    # Click on the 'Event Name' input field to focus on it.
    page.get_by_test_id("promotionEventName").click()
    # Fill the 'Event Name' input field with the value 'rh--1220--0904'.
    page.get_by_test_id("promotionEventName").fill("rh--1220--0904")
    # Click on the 'Event Description' input field to focus on it.
    page.get_by_test_id("promotionEventDescription").click()
    # Fill the 'Event Description' input field with the value 'PROMO THRESHOLD'.
    page.get_by_test_id("promotionEventDescription").fill("PROMO THRESHOLD")
    # Click on the 'Start Date' input field to open the date picker.
    page.get_by_test_id("startDate").click()
    # Select the 10th day of the month as the start date from the date picker.
    page.get_by_text("10", exact=True).click()
    # Click on the 'End Date' input field to open the date picker.
    page.get_by_test_id("endDate").click()
    # Select the 17th day of the month as the end date from the date picker.
    page.get_by_text("17").click()
    # Click on the 'ASAP Pricing' checkbox to enable or disable this option.
    page.get_by_test_id("isAsapPricing").click()
    # Click on the first tier in the 'Zebra Tiers' section to select it.
    page.locator(".zeb-tiers").first.click()
    # Click on the 'Hierarchy' option in the 'Location' filter section to expand the hierarchy options.
    page.locator("#SideFilterlocationhierarchyId").get_by_text("Hierarchy").click()
    # Select the 'Region' option from the expanded hierarchy options.
    page.get_by_text("Region", exact=True).click()
    # Check the radio button for the 'NA' region to filter by this region.
    page.get_by_role("radio", name="NA", exact=True).check()
    # Click on 'Price Zone Type' to expand the available price zone type options.
    page.get_by_text("Price Zone Type").click()
    # Select the 'Collection' option under 'Price Zone Type' to filter by this type.
    page.locator("div").filter(has_text=re.compile(r"^Collection$")).click()
    # Click on 'Price Zone' to expand the available price zone options.
    page.get_by_text("Price Zone", exact=True).click()
    # Select the '1_US Collection' option under 'Price Zone' to apply this specific filter.
    page.get_by_text("1_US Collection").click()
    # Click on the 'Apply Filters' button to apply the selected location filters.
    page.get_by_role("button", name="Apply Filters").click()
    # Click on the 'Select Products' textbox to open the product filter options.
    page.get_by_role("textbox", name="Select Products").click()
    # Click on the 'Hierarchy' option in the product filter section to expand the hierarchy options.
    page.locator("#SideFilterproducthierarchyId").get_by_text("Hierarchy").click()
    # Select the 'Style Color' option from the expanded hierarchy options.
    page.get_by_text("Style Color").click()
    # Check the checkbox for 'Select All' under the 'Style Color' filter to select all available options.
    page.locator("div:nth-child(5) > esp-filter-sub-accordion-v1 > .sub-accordion-element > .fiter-values-container > .filter-options > .filter-values-options > .filter-values.d-flex.align-items-center.p-l-32.p-r-12 > .custom-checkbox-wrapper").click()
    # Check the checkbox for the specific product option 'C281-019999' under the 'Style Color' filter.
    page.locator("div:nth-child(5) > esp-filter-sub-accordion-v1 > .sub-accordion-element > .fiter-values-container > .filter-options > .filter-values-options > div:nth-child(2) > .custom-checkbox-wrapper > .pointer").click()
    # Check the checkbox for the specific product option '004AHK003490' under the 'Style Color' filter.
    page.locator(".pointer.custom-checkbox-unchecked").first.click()
    # Click on the 'Apply Filters' button to apply the selected product filters.
    page.get_by_role("button", name="Apply Filters").click()
    # Click on the dropdown for 'Optimization Objective' to view the available options.
    page.locator("#optimizationObjective > .multiselect-dropdown > div > .w-100").click()
    # Select the 'Optimize for Sales Unit' option from the 'Optimization Objective' dropdown.
    page.locator("div").filter(has_text=re.compile(r"^Optimize for Sales Unit$")).nth(1).click()
    # Click on the 'Next Promo Recommendations' button to proceed to the next step in the promotion creation process.
    page.get_by_test_id("create-promotions-next-button").click()
    # Click on 'Available Products' to view the list of products available for promotion.
    page.get_by_text("Available Products").click()
    # Click on 'Show More' to expand the list of available products.
    page.get_by_text("Show More").click()
    # Click on the 'Next' button to proceed to the promotion setup step.
    page.get_by_test_id("create-promotions-next-button").click()
    # Select the first option in the dropdown or list for promotion type.
    page.locator(".w-100.p-h-16").first.click()
    # Select 'Bundle' as the promotion type.
    page.get_by_text("Bundle").click()
    # Select 'Threshold' as an additional promotion type.
    page.get_by_text("Threshold").click()
    # Click on the first checkbox to enable stacking rules or constraints.
    page.locator(".d-flex.flex-column.justify-content-center.font-size-10.align-items-center.checkbox-v2.m-r-10.zeb-check").first.click()
    # Click on the dropdown to specify the type of promotions to compare, with a maximum limit of 5.
    page.get_by_text("What type of promotion(s) would you like to compare? *Max limit 5Promo Type").click()
    # Click on the 'Spend Amount' field to input the spending threshold for the promotion.
    page.get_by_test_id("spend_amount").click()
    # Enter '5000' as the spending threshold for the promotion.
    page.get_by_test_id("spend_amount").fill("5000")
    # Click on the 'Get' field to input the discount percentage or value.
    page.locator("#get").click()
    # Enter '25' as the discount percentage or value for the promotion.
    page.locator("#get").fill("25")
    # Click on the 'Next' button to proceed to the next step in the promotion creation process.
    page.get_by_test_id("create-promotions-next-button").click()
    # Click on 'Price Zone Adjustment' to navigate to the price zone adjustment section.
    page.get_by_text("Price Zone Adjustment").click()
    # Click on the 'Apply' button to replicate the promotion details to sub-levels.
    page.get_by_test_id("replicate-apply").click()
    # Navigate to the 'Product Details' page by accessing the specified URL.
    page.goto("https://stage.mkr.esp.antuit.ai/nglcp/product-level-details/product-details")
    # Click on the 'Close' button to dismiss the current modal or overlay.
    page.get_by_role("button", name="Close").click()
    # Click on the 'Submit All for Approval' button to initiate the approval process for the selected scenario.
    page.get_by_test_id("submit-all-for-approval").click()
    # Confirm the submission by clicking the 'Yes, Submit' button in the confirmation modal.
    page.get_by_test_id("confirm-modal-confirm-yes-button").click()
    # Open the 'Actions' dropdown menu to access further options for the scenario.
    page.get_by_role("button", name="Actions").click()
    # Select the 'Approve' option from the dropdown to approve the scenario.
    page.get_by_text("Approve", exact=True).click()
    # Confirm the approval action by clicking the 'Confirm' button in the modal.
    page.get_by_test_id("confirm-modal-confirm-yes-button").click()
    # Reopen the 'Actions' dropdown menu to access additional options.
    page.get_by_role("button", name="Actions").click()
    # Select the 'Reject' option from the dropdown to reject the scenario.
    page.get_by_text("Reject").click()
    # Confirm the rejection action by clicking the 'Confirm' button in the modal.
    page.get_by_test_id("confirm-modal-confirm-yes-button").click()
    # Reopen the 'Actions' dropdown menu to access further options.
    page.get_by_role("button", name="Actions").click()
    # Select the 'Withdraw' option from the dropdown to withdraw the scenario.
    page.get_by_text("Withdraw", exact=True).click()
    # Confirm the withdrawal action by clicking the 'Confirm' button in the modal.
    page.get_by_test_id("confirm-modal-confirm-yes-button").click()
    # Click on the 'Next' button to proceed to the next step in the promotion creation process.
    page.get_by_test_id("create-promotions-next-button").click()
    # Close the current page to complete the cleanup process.
    page.close()

    # ---------------------
    # Close the browser context to clean up resources associated with it.
    context.close()
    # Close the browser instance to terminate the session completely.
    browser.close()


# Initialize the Playwright context to manage browser automation.
with sync_playwright() as playwright:
    # Execute the 'run' function, passing the Playwright instance to perform the defined automation tasks.
    run(playwright)
