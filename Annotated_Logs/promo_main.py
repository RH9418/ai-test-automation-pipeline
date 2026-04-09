import re
from playwright.sync_api import Playwright, sync_playwright, expect


def run(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    # Navigate to the Promotions page to begin interacting with the application.
    page.goto("https://stage.mkr.esp.antuit.ai/nglcp/promotions/")
    # Click on the promotions action button to open the promotions menu.
    page.get_by_test_id("promotions-action-button").click()
    # Click on 'New Promotion' to initiate the creation of a new promotion.
    page.get_by_text("New Promotion").click()
    # Click on the promotion event name field to focus on it.
    page.get_by_test_id("promotionEventName").click()
    # Fill the promotion event name field with the specified identifier.
    page.get_by_test_id("promotionEventName").fill("rh-1205070436")
    # Click on the promotion event description field to focus on it.
    page.get_by_test_id("promotionEventDescription").click()
    # Fill the promotion event description field with the specified description.
    page.get_by_test_id("promotionEventDescription").fill("PROMO TEST 3")
    # Click on the 'Start Date' field to open the date picker.
    page.get_by_test_id("startDate").click()
    # Select the 9th day of the month as the start date.
    page.get_by_text("9").nth(1).click()
    # Click on the 'End Date' field to open the date picker.
    page.get_by_test_id("endDate").click()
    # Select the 12th day of the month as the end date.
    page.get_by_text("12", exact=True).click()
    # Enable the 'ASAP Pricing' option by clicking the corresponding checkbox.
    page.get_by_test_id("isAsapPricing").click()
    # Click on the first element in the '.zeb-tiers' class to initiate the hierarchy selection process.
    page.locator(".zeb-tiers").first.click()
    # Select the 'Hierarchy' option from the filtered list of div elements.
    page.locator("div").filter(has_text=re.compile(r"^Hierarchy$")).nth(3).click()
    # Click on the 'Region' option to specify the region filter.
    page.get_by_text("Region", exact=True).click()
    # Select the 'NA' radio button to apply the North America region filter.
    page.get_by_role("radio", name="NA", exact=True).check()
    # Click on 'Price Zone Type' to open the corresponding filter options.
    page.get_by_text("Price Zone Type").click()
    # Select the first checkbox under 'Price Zone Type' filter options.
    page.locator(".filter-values.d-flex.align-items-center.p-l-32.p-r-24 > .custom-checkbox-wrapper > .pointer").first.click()
    # Click on 'Price Zone' to open the filter options for price zones.
    page.get_by_text("Price Zone", exact=True).click()
    # Select a checkbox under the 'Price Zone' filter options.
    page.locator(".filter-values.d-flex.align-items-center.p-l-32.p-r-24 > .custom-checkbox-wrapper > .pointer").click()
    # Click on the 'Apply Filters' button to apply the selected filters.
    page.get_by_role("button", name="Apply Filters").click()
    # Click on the eighth child element in '.zeb-tiers' to proceed with the next hierarchy selection.
    page.locator("div:nth-child(8) > .zeb-tiers").click()
    # Click on 'Hierarchy' within the '#SideFilterproducthierarchyId' section to refine the hierarchy filter.
    page.locator("#SideFilterproducthierarchyId").get_by_text("Hierarchy").click()
    # Select the 'Style Color' option to apply a specific style filter.
    page.get_by_text("Style Color").click()
    # Select a checkbox under the 'Style Color' filter options to refine the selection.
    page.locator("div:nth-child(5) > esp-filter-sub-accordion-v1 > .sub-accordion-element > .fiter-values-container > .filter-options > .filter-values-options > .filter-values.d-flex.align-items-center.p-l-32.p-r-12 > .custom-checkbox-wrapper > .pointer").click()
    # Click on the sixth child checkbox to apply an additional filter.
    page.locator("div:nth-child(6) > .custom-checkbox-wrapper > .pointer").click()
    # Click on the fifth child checkbox to apply another filter.
    page.locator("div:nth-child(5) > .custom-checkbox-wrapper > .pointer").click()
    # Click on the 'Apply Filters' button again to finalize the filter selections.
    page.get_by_role("button", name="Apply Filters").click()
    # Click on the dropdown menu to select an optimization objective.
    page.locator("#optimizationObjective > .multiselect-dropdown > div > .w-100").click()
    # Select 'Optimize for Sales Unit' from the dropdown options.
    page.locator("div").filter(has_text=re.compile(r"^Optimize for Sales Unit$")).nth(1).click()
    # Click the 'Next' button to proceed to the next step in the promotion creation process.
    page.get_by_test_id("create-promotions-next-button").click()
    # Click on 'Show More' to expand additional options.
    page.get_by_text("Show More").click()
    # Select the checkbox for 'Column with Header Selection'.
    page.get_by_role("checkbox", name="Column with Header Selection").check()
    # Click on the promotions action button to proceed with the next step.
    page.get_by_test_id("promotions-action-button").click()
    # Reset user preferences by clicking 'Reset Preferences'.
    page.get_by_text("Reset Preferences").click()
    # Focus on the search textbox to input a query.
    page.get_by_role("textbox", name="Search").click()
    # Fill the search textbox with the value '005'.
    page.get_by_role("textbox", name="Search").fill("005")
    # Submit the search query by pressing 'Enter'.
    page.get_by_role("textbox", name="Search").press("Enter")
    # Click on the second link in the list of available links.
    page.locator("a").nth(1).click()
    # Click on 'Available Products' to view product options.
    page.get_by_text("Available Products").click()
    # Open the dropdown menu for product filtering.
    page.locator("div:nth-child(3) > div > esp-multiselect-dropdown > .multiselect-dropdown > div > .w-100 > .d-flex.align-items-center > .dropdown-caret").click()
    # Select a specific filter option from the dropdown.
    page.locator("div:nth-child(7) > .d-flex").click()
    # Click on the center column viewport to interact with the grid.
    page.locator(".ag-center-cols-viewport").click()
    # Select the first item in the list of available options.
    page.locator(".w-100.p-h-16").first.click()
    # Click on the first dropdown option to refine the selection.
    page.locator(".d-flex.dropdown-option.align-items-center.p-v-5.p-l-32").first.click()
    # Select the product '21_Men's Underwear' from the list.
    page.get_by_text("21_Men's Underwear").click()
    # Open another dropdown menu for additional filtering.
    page.locator("div:nth-child(2) > div > esp-multiselect-dropdown > .multiselect-dropdown > div > .w-100 > .d-flex.align-items-center > .dropdown-caret").click()
    # Open a third dropdown menu for further filtering options.
    page.locator("div:nth-child(3) > div > esp-multiselect-dropdown > .multiselect-dropdown > div > .w-100 > .d-flex.align-items-center > .dropdown-caret").click()
    # Select the first option in the flex column dropdown.
    page.locator(".d-flex.flex-column.justify-content-center").first.click()
    # Click on the second option in the overflow auto dropdown.
    page.locator(".overflow-auto > div:nth-child(2) > .d-flex").click()
    # Apply the complex filter by clicking the 'Apply' button.
    page.get_by_test_id("complex-filter-apply").click()
    # Check the checkbox to enable the promotion creation process.
    page.locator("#ag-2170-input").check()
    # Click on the 'Promotions Action' button to proceed with promotion actions.
    page.get_by_test_id("promotions-action-button").click()
    # Click on 'Add' to initiate adding a new promotion.
    page.get_by_text("Add").click()
    # Confirm the action in the modal by clicking 'Yes'.
    page.get_by_test_id("confirm-modal-confirm-yes-button").click()
    # Click on the 'Reoptimize' button to optimize the promotion settings.
    page.get_by_role("button", name="Reoptimize").click()
    # Confirm the reoptimization action in the modal by clicking 'Yes'.
    page.get_by_test_id("confirm-modal-confirm-yes-button").click()
    # Click on the 'Next' button to proceed to the next step in the promotion creation process.
    page.get_by_test_id("create-promotions-next-button").click()
    # Open the dropdown menu to select a promotion type.
    page.locator(".dropdown-caret").first.click()
    # Select 'BOGO' (Buy One Get One) as the promotion type.
    page.get_by_text("BOGO").click()
    # Click on the first row to select or configure group details.
    page.locator(".row").first.click()
    # Open the dropdown to select the number of buy groups.
    page.locator("#numberOfBuyGroups > .multiselect-dropdown > div > .w-100 > .d-flex.align-items-center > .dropdown-caret").click()
    # Select '1' as the number of buy groups.
    page.locator("div").filter(has_text=re.compile(r"^1$")).nth(1).click()
    # Open the dropdown to select the number of units to buy from each group.
    page.locator("#numberOfUnitsToBuyFromEachGroup > .multiselect-dropdown > div > .w-100 > .d-flex.align-items-center > .dropdown-caret").click()
    # Select '1' as the number of units to buy from each group.
    page.locator("div").filter(has_text=re.compile(r"^1$")).nth(1).click()
    # Click on the 'Add Value' textbox to input a value for the promotion.
    page.get_by_role("textbox", name="Add Value").click()
    # Fill the 'Add Value' textbox with the value '34'.
    page.get_by_role("textbox", name="Add Value").fill("34")
    # Click on the 'Add Group' button to add a new group to the promotion.
    page.get_by_test_id("group-add").first.click()
    # Click on the 'Product IDs' field to input product identifiers.
    page.get_by_test_id("product-ids").click()
    # Fill the 'Product IDs' field with the product ID '005DKI004106'.
    page.get_by_test_id("product-ids").fill("005DKI004106")
    # Click on the 'Save' button to save the promotion details.
    page.get_by_test_id("save").click()
    # Click on 'Add Group' to start adding a new group.
    page.get_by_test_id("group-add").click()
    # Click on the 'Product IDs' field to focus on it.
    page.get_by_test_id("product-ids").click()
    # Fill the 'Product IDs' field with the product identifier '022DKI005106'.
    page.get_by_test_id("product-ids").fill("022DKI005106")
    # Click on 'Save' to save the entered product details.
    page.get_by_test_id("save").click()
    # Click on 'Next' to proceed to the next step in the promotion creation process.
    page.get_by_test_id("create-promotions-next-button").click()
    # Click on 'Replicate' to replicate the promotion settings.
    page.get_by_test_id("replicate").click()
    # Click on the 'Attribute Value' field to focus on it.
    page.locator("#attribute_value").click()
    # Fill the 'Attribute Value' field with the value '45'.
    page.locator("#attribute_value").fill("45")
    # Press 'Enter' to confirm the entered attribute value.
    page.locator("#attribute_value").press("Enter")
    # Click on the 'End Date' field to open the date picker.
    page.locator("#end_date").click()
    # Select the 18th day from the date picker as the end date.
    page.get_by_text("18").click()
    # Click on the grid cell with the value '$ (1.00000)' to select the price adjustment.
    page.get_by_role("gridcell", name="$ (1.00000)").click()
    # Close the page to finalize the process.
    page.close()

    # ---------------------
    # Close the context to clean up resources associated with the browser session.
    context.close()
    # Close the browser to terminate the automation session completely.
    browser.close()


with sync_playwright() as playwright:
    run(playwright)
