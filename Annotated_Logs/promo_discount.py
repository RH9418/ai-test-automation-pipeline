import re
from playwright.sync_api import Playwright, sync_playwright, expect


def run(playwright: Playwright) -> None:
    # Launch a Chromium browser instance in non-headless mode for debugging purposes.
    browser = playwright.chromium.launch(headless=False)
    # Create a new browser context to isolate cookies, storage, and other session data.
    context = browser.new_context()
    # Open a new page within the created browser context.
    page = context.new_page()
    # Navigate to the specified URL, which appears to be a staging environment for a promotions landing page.
    page.goto("https://stage.mkr.esp.antuit.ai/nglcp/promotions/landing-page")
    # Click on the 'Promotions Action' button to access promotion-related actions.
    page.get_by_test_id("promotions-action-button").click()
    # Click on 'New Promotion' to initiate the creation of a new promotion.
    page.get_by_text("New Promotion").click()
    # Click on the 'Promotion Event Name' input field to begin entering the name of the promotion.
    page.get_by_test_id("promotionEventName").click()
    # Fill the 'Promotion Event Name' input field with the value 'rh1230-08-04'.
    page.get_by_test_id("promotionEventName").fill("rh1230-08-04")
    # Click on the 'Promotion Event Description' input field to begin entering the description of the promotion.
    page.get_by_test_id("promotionEventDescription").click()
    # Fill the 'Promotion Event Description' input field with the value 'PROMO DISCOUNT TEST'.
    page.get_by_test_id("promotionEventDescription").fill("PROMO DISCOUNT TEST")
    # Click on the 'Start Date' field to open the date picker for selecting the promotion's start date.
    page.get_by_test_id("startDate").click()
    # Select the 17th day from the date picker as the start date for the promotion.
    page.get_by_text("17").click()
    # Click on the 'End Date' field to open the date picker for selecting the promotion's end date.
    page.get_by_test_id("endDate").click()
    # Select the 18th day from the date picker as the end date for the promotion.
    page.get_by_text("18").click()
    # Click on the 'ASAP Pricing' checkbox to enable or disable ASAP pricing for the promotion.
    page.get_by_test_id("isAsapPricing").click()
    # Select the 'Regular Price Only' option under 'Price Type' to specify the pricing type for the promotion.
    page.get_by_test_id("price_type_reg").click()
    # Click on the first element in the '.zeb-tiers' section, likely to configure tiered pricing or related settings.
    page.locator(".zeb-tiers").first.click()
    # Click on the third 'Hierarchy' element in the list to expand or select it.
    page.locator("div").filter(has_text=re.compile(r"^Hierarchy$")).nth(3).click()
    # Click on the first element within the '.d-flex.p-l-32' section, likely to select a specific hierarchy option.
    page.locator(".d-flex.p-l-32").first.click()
    # Select the 'NA' radio button under the hierarchy options to specify the region.
    page.get_by_role("radio", name="NA", exact=True).check()
    # Click on 'Price Zone Type' to expand the options for selection.
    page.get_by_text("Price Zone Type").click()
    # Select the third checkbox under 'Price Zone Type', likely to choose a specific category.
    page.locator("div:nth-child(3) > .custom-checkbox-wrapper > .pointer").click()
    # Click on 'Price Zone' to expand the options for filtering.
    page.get_by_text("Price Zone", exact=True).click()
    # Select the first checkbox under 'Price Zone', likely to choose a specific filter value.
    page.locator(".filter-values.d-flex.align-items-center.p-l-32.p-r-24 > .custom-checkbox-wrapper > .pointer").first.click()
    # Click on 'Price Zone Type' again, possibly to modify or confirm the selection.
    page.get_by_text("Price Zone Type").click()
    # Deselect the first selected checkbox under 'Price Zone Type'.
    page.locator(".pointer.custom-checkbox-checked").first.click()
    # Select the first checkbox under 'Price Zone' again, likely to reapply the filter.
    page.locator(".filter-values.d-flex.align-items-center.p-l-32.p-r-24 > .custom-checkbox-wrapper > .pointer").first.click()
    # Click on 'Price Zone' again, possibly to modify or confirm the selection.
    page.get_by_text("Price Zone", exact=True).click()
    # Select another checkbox under 'Price Zone', likely to add an additional filter value.
    page.locator(".filter-values.d-flex.align-items-center.p-l-32.p-r-24 > .custom-checkbox-wrapper > .pointer").click()
    # Click on the 'Apply Filters' button to finalize the selected filters.
    page.get_by_role("button", name="Apply Filters").click()
    # Click on the 8th div element with the class 'zeb-tiers', likely to expand or interact with a specific section.
    page.locator("div:nth-child(8) > .zeb-tiers").click()
    # Click on the 'Hierarchy' option under the product hierarchy filter to expand its options.
    page.locator("#SideFilterproducthierarchyId").get_by_text("Hierarchy").click()
    # Select 'Style Color' from the hierarchy options, likely to filter by this category.
    page.get_by_text("Style Color").click()
    # Select the first checkbox under 'Style Color', likely to choose a specific filter value.
    page.locator("div:nth-child(5) > esp-filter-sub-accordion-v1 > .sub-accordion-element > .fiter-values-container > .filter-options > .filter-values-options > .filter-values.d-flex.align-items-center.p-l-32.p-r-12 > .custom-checkbox-wrapper > .pointer").click()
    # Select another checkbox under 'Style Color', likely to add an additional filter value.
    page.locator("div:nth-child(7) > .custom-checkbox-wrapper > .pointer").click()
    # Click on the 'Apply Filters' button to finalize the selected filters.
    page.get_by_role("button", name="Apply Filters").click()
    # Click on the dropdown under 'Optimization Objective' to reveal the available options.
    page.locator("#optimizationObjective > .multiselect-dropdown > div > .w-100 > .d-flex.align-items-center > .dropdown-caret").click()
    # Select the 'Optimize Sales Revenue' option from the dropdown to set the optimization objective.
    page.locator("div").filter(has_text=re.compile(r"^Optimize Sales Revenue$")).nth(1).click()
    # Click on the 'Next' button to proceed to the summary section of the promotion creation process.
    page.get_by_test_id("create-promotions-next-button").click()
    # Expand the summary section by clicking the 'Show More' button to view additional details.
    page.get_by_test_id("summary-show-more-button").click()
    # Click on the 'Available Products' tab to switch to the product selection view.
    page.get_by_text("Available Products").click()
    # Click on the first dropdown caret to reveal the department filter options.
    page.locator(".dropdown-caret").first.click()
    # Select the '20_Apparel' option from the department dropdown.
    page.locator(".d-flex.dropdown-option.align-items-center.p-v-5.p-l-32 > .d-flex").first.click()
    # Click on the second dropdown caret to reveal the sub-department filter options.
    page.locator("div:nth-child(2) > div > esp-multiselect-dropdown > .multiselect-dropdown > div > .w-100 > .d-flex.align-items-center > .dropdown-caret").click()
    # Click on the second dropdown caret again to ensure the sub-department options are visible.
    page.locator("div:nth-child(2) > div > esp-multiselect-dropdown > .multiselect-dropdown > div > .w-100 > .d-flex.align-items-center > .dropdown-caret").click()
    # Select the first sub-department option, '20_MMK', from the dropdown.
    page.locator(".d-flex.dropdown-option").first.click()
    # Click on the second product category option to refine the product selection.
    page.locator(".overflow-auto > div:nth-child(2)").click()
    # Click on the third dropdown caret to reveal the class filter options.
    page.locator("div:nth-child(3) > div > esp-multiselect-dropdown > .multiselect-dropdown > div > .w-100 > .d-flex.align-items-center > .dropdown-caret").click()
    # Click on the third dropdown caret again to ensure the class options are visible.
    page.locator("div:nth-child(3) > div > esp-multiselect-dropdown > .multiselect-dropdown > div > .w-100 > .d-flex.align-items-center > .dropdown-caret").click()
    # Select the first class option from the dropdown to further refine the product selection.
    page.locator(".d-flex.flex-column.justify-content-center").first.click()
    # Click on the '203_Logo Knits' option to finalize the product selection.
    page.get_by_text("203_Logo Knits").click()
    # Click on the 'Apply' button to apply the selected filters and finalize the product selection.
    page.get_by_test_id("complex-filter-apply").click()
    # Click on the first product row in the table to select it for promotion.
    page.locator(".ag-row-odd > .ag-cell > .ag-cell-wrapper").first.click()
    # Click on the 'Promotions Action' button to open the action menu for the selected product.
    page.get_by_test_id("promotions-action-button").click()
    # Click on the 'Add' option to add the selected product to the promotion.
    page.get_by_text("Add").click()
    # Confirm the addition of the selected product to the promotion by clicking 'Yes' in the confirmation modal.
    page.get_by_test_id("confirm-modal-confirm-yes-button").click()
    # Click on the 'Reoptimize' button to optimize the promotion based on the selected products.
    page.get_by_role("button", name="Reoptimize").click()
    # Confirm the reoptimization process by clicking 'Yes' in the confirmation modal.
    page.get_by_test_id("confirm-modal-confirm-yes-button").click()
    # Click on the 'Next' button to proceed to the 'Define Type & Constraints' step.
    page.get_by_test_id("create-promotions-next-button").click()
    # Click on the first dropdown caret to reveal the promotion type options.
    page.locator(".dropdown-caret").first.click()
    # Select the second promotion type option (e.g., 'BOGO') from the dropdown.
    page.locator(".overflow-auto > div:nth-child(2) > .d-flex").click()
    # Click on the first row in the 'Promo Type' section to select '% or $ Off' as the promotion type.
    page.locator(".row").first.click()
    # Click on the '% or $ Off' input field to activate it for editing.
    page.locator("#off").click()
    # Enter '30' in the '% or $ Off' input field to set the discount value.
    page.locator("#off").fill("30")
    # Click on the 'Next' button to proceed to the 'Analyze Scenarios' step.
    page.get_by_test_id("create-promotions-next-button").click()
    # Click on the 'Price Zone Adjustment' option to adjust the price zone for the promotion.
    page.get_by_text("Price Zone Adjustment").click()
    # Click on the dropdown caret in the 'Rounding Rules' section to reveal the rounding rule options.
    page.locator("#rounding_rules_id > .multiselect-dropdown > div > .w-100 > .d-flex.align-items-center > .dropdown-caret").click()
    # Select the '.99 RN' rounding rule from the dropdown to apply it to the promotion.
    page.locator("div").filter(has_text=re.compile(r"^\.99 RN$")).nth(1).click()
    # Click on the 'Attribute Value' input field to activate it for editing.
    page.locator("#attribute_value").click()
    # Enter '35' in the 'Attribute Value' input field to set the attribute value.
    page.locator("#attribute_value").fill("35")
    # Click on the first dropdown caret to reveal additional options for replication.
    page.locator(".dropdown-caret").first.click()
    # Click on the first dropdown caret again to ensure the options are visible.
    page.locator(".dropdown-caret").first.click()
    # Click on the 'Apply' button to replicate the promotion to sub-levels.
    page.get_by_test_id("replicate-apply").click()
    # Navigate to the 'Product Level Details' page to review the promotion details.
    page.goto("https://stage.mkr.esp.antuit.ai/nglcp/product-level-details/product-details")

    # ---------------------
    # Close the browser context to clean up session-specific data.
    context.close()
    # Close the browser to end the automation session and release resources.
    browser.close()


with sync_playwright() as playwright:
    run(playwright)
