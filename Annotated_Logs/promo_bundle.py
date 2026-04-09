# Import the 're' module for regular expression operations.
import re
# Import Playwright's synchronous API and related utilities for browser automation.
from playwright.sync_api import Playwright, sync_playwright, expect


# Define the main function 'run' which will execute the Playwright automation script.
def run(playwright: Playwright) -> None:
    # Launch a Chromium browser instance in non-headless mode for visual debugging.
    browser = playwright.chromium.launch(headless=False)
    # Create a new browser context to isolate cookies, storage, and other session data.
    context = browser.new_context()
    # Open a new page (tab) within the created browser context for interaction.
    page = context.new_page()
    # Navigate to the 'Create Promotions' page using the specified URL.
    page.goto("https://stage.mkr.esp.antuit.ai/nglcp/promotions/create-promotions")
    # Click on the 'Name' input field to begin entering the promotion event name.
    page.get_by_test_id("promotionEventName").click()
    # Fill the 'Name' input field with the value 'rh--1137-0904'.
    page.get_by_test_id("promotionEventName").fill("rh--1137-0904")
    # Click on the 'Description' input field to begin entering the promotion event description.
    page.get_by_test_id("promotionEventDescription").click()
    # Fill the 'Description' input field with the value 'PROMO BUNDLE TEST 2'.
    page.get_by_test_id("promotionEventDescription").fill("PROMO BUNDLE TEST 2")
    # Click on the 'Start Date' field to open the date picker.
    page.get_by_test_id("startDate").click()
    # Select the 16th day of the month as the start date from the date picker.
    page.get_by_text("16").click()
    # Click on the 'End Date' field to open the date picker.
    page.get_by_test_id("endDate").click()
    # Select the 23rd day of the month as the end date from the date picker.
    page.get_by_text("23", exact=True).click()
    # Click on the 'ASAP Pricing' checkbox to enable this option under 'Additional Considerations'.
    page.get_by_test_id("isAsapPricing").click()
    # Click on the 'Select Locations' textbox to open the location selection panel.
    page.get_by_role("textbox", name="Select Locations").click()
    # Click on 'Hierarchy' in the location selection panel to expand the hierarchy options.
    page.locator("#SideFilterlocationhierarchyId").get_by_text("Hierarchy").click()
    # Select 'Region' from the hierarchy options.
    page.get_by_text("Region", exact=True).click()
    # Select the 'JPN' radio button to filter locations by the Japan region.
    page.get_by_role("radio", name="JPN").check()
    # Click on 'Price Zone Type' to expand the price zone type options.
    page.get_by_text("Price Zone Type").click()
    # Select the first checkbox under 'Price Zone Type' (e.g., 'Select All').
    page.locator(".filter-values.d-flex.align-items-center.p-l-32.p-r-24 > .custom-checkbox-wrapper > .pointer").first.click()
    # Click on 'Price Zone' to expand the price zone options.
    page.get_by_text("Price Zone", exact=True).click()
    # Select a specific price zone checkbox (e.g., 'Collection').
    page.locator(".filter-values.d-flex.align-items-center.p-l-32.p-r-24 > .custom-checkbox-wrapper > .pointer").click()
    # Click on the 'Apply Filters' button to apply the selected location and price zone filters.
    page.get_by_role("button", name="Apply Filters").click()
    # Click on the 'Select Products' textbox to open the product selection panel.
    page.get_by_role("textbox", name="Select Products").click()
    # Click on 'Hierarchy' in the product selection panel to expand the hierarchy options.
    page.locator("#SideFilterproducthierarchyId").get_by_text("Hierarchy").click()
    # Click on 'Style Color' in the hierarchy options to filter products by style color.
    page.get_by_text("Style Color").click()
    # Click on 'Style Color' again to ensure the filter is selected.
    page.get_by_text("Style Color").click()
    # Select the first checkbox under 'Style Color' (e.g., 'Select All') to include all style colors.
    page.locator("div:nth-child(5) > esp-filter-sub-accordion-v1 > .sub-accordion-element > .fiter-values-container > .filter-options > .filter-values-options > .filter-values.d-flex.align-items-center.p-l-32.p-r-12 > .custom-checkbox-wrapper").click()
    # Select a specific style color checkbox (e.g., '-2C8-01J999') to include it in the selection.
    page.locator("div:nth-child(5) > esp-filter-sub-accordion-v1 > .sub-accordion-element > .fiter-values-container > .filter-options > .filter-values-options > div:nth-child(2) > .custom-checkbox-wrapper > .pointer").click()
    # Click on the first unchecked checkbox to include another style color in the selection.
    page.locator(".pointer.custom-checkbox-unchecked").first.click()
    # Click on the first unchecked checkbox again to ensure it is selected.
    page.locator(".pointer.custom-checkbox-unchecked").first.click()
    # Click on a specific product (e.g., '101AKB0201') to include it in the selection.
    page.locator("div").filter(has_text=re.compile(r"^101AKB0201$")).click()
    # Click on the 'Apply Filters' button to apply the selected product filters.
    page.get_by_role("button", name="Apply Filters").click()
    # Click on the dropdown menu under 'Set Optimization Objective' to view the available optimization options.
    page.locator("#optimizationObjective > .multiselect-dropdown > div > .w-100").click()
    # Select 'Optimize for Margin Revenue' from the dropdown menu to set it as the optimization objective.
    page.get_by_text("Optimize for Margin Revenue").click()
    # Click on the 'Next Promo Recommendations' button to proceed to the summary page.
    page.get_by_test_id("create-promotions-next-button").click()
    # Click on the 'Show More' button to expand additional details in the summary section.
    page.get_by_test_id("summary-show-more-button").click()
    # Click on the 'Available Products' tab to view the list of products included in the promotion.
    page.get_by_text("Available Products").click()
    # Click on the 'Next Promo Recommendations' button again to finalize and proceed.
    page.get_by_test_id("create-promotions-next-button").click()
    # Click on the first dropdown caret to expand the options for defining promotion groups.
    page.locator(".dropdown-caret").first.click()
    # Select the fourth option from the dropdown to choose a specific group configuration.
    page.locator(".overflow-auto > div:nth-child(4)").click()
    # Click on the first element with the 'flex-grow-1' class to proceed with the group selection.
    page.locator(".flex-grow-1").first.click()
    # Click on the 'Edit Group Name' button to modify the name of the selected group.
    page.get_by_test_id("group-name-edit-btn").click()
    # Fill in the group name field with 'Watch' to name the group.
    page.get_by_test_id("name").fill("Watch")
    # Click on the 'Buy 1 0 Eligible Products Selected Add' button to add eligible products to the group.
    page.get_by_text("Buy 1 0 Eligible Products Selected Add").click()
    # Click on the 'Add Group' button to create a new group.
    page.get_by_test_id("group-add").click()
    # Click on the 'Product IDs' field to input product identifiers for the group.
    page.get_by_test_id("product-ids").click()
    # Fill in the 'Product IDs' field with the specified product IDs, separated by new lines.
    page.get_by_test_id("product-ids").fill("005DKI0041\n100DKX5271\n100DKX534704\n101AKB0201")
    # Click on the 'Save' button to save the group configuration.
    page.get_by_test_id("save").click()
    # Click on the 'Add Value' textbox to input a value for the promotion.
    page.get_by_role("textbox", name="Add Value").click()
    # Fill in the 'Add Value' textbox with '35' to set the promotion value.
    page.get_by_role("textbox", name="Add Value").fill("35")
    # Click on the 'Next' button to proceed to the next step in the promotion creation process.
    page.get_by_test_id("create-promotions-next-button").click()
    # Click on 'Price Zone Adjustment' to navigate to the section for adjusting price zones.
    page.get_by_text("Price Zone Adjustment").click()
    # Click on the '#attribute_value' field to select it for input.
    page.locator("#attribute_value").click()
    # Fill in the '#attribute_value' field with '40' to set the adjustment value.
    page.locator("#attribute_value").fill("40")
    # Click on the 'Apply' button to save and apply the price zone adjustment.
    page.get_by_test_id("replicate-apply").click()
    # Click on the 'Submit All for Approval' button to initiate the submission of the promotion for approval.
    page.get_by_role("button", name="Submit All for Approval").click()
    # Confirm the submission by clicking the 'Yes, Submit' button in the confirmation modal.
    page.get_by_test_id("confirm-modal-confirm-yes-button").click()
    # Click on the 'Close' button to close the submission confirmation modal.
    page.get_by_role("button", name="Close").click()
    # Click on the 'Actions' button to open the actions menu.
    page.get_by_role("button", name="Actions").click()
    # Select 'Approve' from the actions menu to approve the promotion.
    page.get_by_text("Approve", exact=True).click()
    # Confirm the approval by clicking the 'Confirm' button in the confirmation modal.
    page.get_by_test_id("confirm-modal-confirm-yes-button").click()
    # Click on the 'Actions' button again to open the actions menu.
    page.get_by_role("button", name="Actions").click()
    # Select 'Reject' from the actions menu to reject the promotion.
    page.get_by_text("Reject").click()
    # Confirm the rejection by clicking the 'Confirm' button in the confirmation modal.
    page.get_by_test_id("confirm-modal-confirm-yes-button").click()
    # Click on the 'Actions' button again to open the actions menu.
    page.get_by_role("button", name="Actions").click()
    # Select 'Withdraw' from the actions menu to withdraw the promotion.
    page.get_by_text("Withdraw", exact=True).click()
    # Confirm the withdrawal by clicking the 'Confirm' button in the confirmation modal.
    page.get_by_test_id("confirm-modal-confirm-yes-button").click()
    # Click on the 'Next' button in the promotion creation flow to proceed to the next step.
    page.get_by_test_id("create-promotions-next-button").click()
    # Close the current page to end the session for this specific tab or window.
    page.close()

    # ---------------------
    # Close the browser context to clean up resources associated with this context.
    context.close()
    # Close the browser to terminate the entire browser session.
    browser.close()


# Initialize the Playwright context to start browser automation.
with sync_playwright() as playwright:
    # Call the 'run' function, passing the Playwright instance to execute the defined automation script.
    run(playwright)
