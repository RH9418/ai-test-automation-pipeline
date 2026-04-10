# Feature: Promo Threshold
**Tab Location:** Main Workspace

## Detailed User Interaction Flows

| Use Case ID | Test Case Description | Exact Locator | Pass/Fail | Notes | Issues |
|:---|:---|:---|:---|:---|:---|
```markdown
| | **--- NAVIGATION TO PROMOTIONS PAGE ---** | | | | |
| D.1 | Navigate to the 'Create Promotions' page by entering the provided URL in the browser. | `page.goto("https://stage.mkr.esp.antuit.ai/nglcp/promotions/create-promotions")` | | | |
```
```markdown
| | **--- EVENT DETAILS INPUT ---** | | | | |
| E.1 | Click on the 'Event Name' input field to focus on it. | `page.get_by_test_id("promotionEventName").click()` | | | |
| E.2 | Enter the value 'rh--1220--0904' into the 'Event Name' input field. | `page.get_by_test_id("promotionEventName").fill("rh--1220--0904")` | | | |
| E.3 | Click on the 'Event Description' input field to focus on it. | `page.get_by_test_id("promotionEventDescription").click()` | | | |
| E.4 | Enter the value 'PROMO THRESHOLD' into the 'Event Description' input field. | `page.get_by_test_id("promotionEventDescription").fill("PROMO THRESHOLD")` | | | |
```
```markdown
| | **--- DATE SELECTION ---** | | | | |
| F.1 | Click on the 'Start Date' input field to open the date picker. | `page.get_by_test_id("startDate").click()` | | | |
| F.2 | From the date picker, select the 10th day of the month as the start date. | `page.get_by_text("10", exact=True).click()` | | | |
| F.3 | Click on the 'End Date' input field to open the date picker. | `page.get_by_test_id("endDate").click()` | | | |
| F.4 | From the date picker, select the 17th day of the month as the end date. | `page.get_by_text("17").click()` | | | |
```
```markdown
| | **--- ASAP PRICING AND ZEBRA TIERS ---** | | | | |
| G.1 | Click on the 'ASAP Pricing' checkbox to enable or disable this option. | `page.get_by_test_id("isAsapPricing").click()` | | | |
| G.2 | Click on the first tier in the 'Zebra Tiers' section to select it. | `page.locator(".zeb-tiers").first.click()` | | | |
```
```markdown
| | **--- LOCATION FILTERS ---** | | | | |
| H.1 | Click on the 'Hierarchy' option in the 'Location' filter section to expand the hierarchy options. | `page.locator("#SideFilterlocationhierarchyId").get_by_text("Hierarchy").click()` | | | |
| H.2 | Select the 'Region' option from the expanded hierarchy options. | `page.get_by_text("Region", exact=True).click()` | | | |
| H.3 | Check the radio button for the 'NA' region to filter by this region. | `page.get_by_role("radio", name="NA", exact=True).check()` | | | |
| H.4 | Click on 'Price Zone Type' to expand the available price zone type options. | `page.get_by_text("Price Zone Type").click()` | | | |
| H.5 | Select the 'Collection' option under 'Price Zone Type' to filter by this type. | `page.locator("div").filter(has_text=re.compile(r"^Collection$")).click()` | | | |
| H.6 | Click on 'Price Zone' to expand the available price zone options. | `page.get_by_text("Price Zone", exact=True).click()` | | | |
| H.7 | Select the '1_US Collection' option under 'Price Zone' to apply this specific filter. | `page.get_by_text("1_US Collection").click()` | | | |
| H.8 | Click on the 'Apply Filters' button to apply the selected location filters. | `page.get_by_role("button", name="Apply Filters").click()` | | | |
```
```markdown
| | **--- PRODUCT FILTERS ---** | | | | |
| I.1 | Click on the 'Select Products' textbox to open the product filter options. | `page.get_by_role("textbox", name="Select Products").click()` | | | |
| I.2 | Click on the 'Hierarchy' option in the product filter section to expand the hierarchy options. | `page.locator("#SideFilterproducthierarchyId").get_by_text("Hierarchy").click()` | | | |
| I.3 | Select the 'Style Color' option from the expanded hierarchy options. | `page.get_by_text("Style Color").click()` | | | |
| I.4 | Check the checkbox for 'Select All' under the 'Style Color' filter to select all available options. | `page.locator("div:nth-child(5) > esp-filter-sub-accordion-v1 > .sub-accordion-element > .fiter-values-container > .filter-options > .filter-values-options > .filter-values.d-flex.align-items-center.p-l-32.p-r-12 > .custom-checkbox-wrapper").click()` | | | |
| I.5 | Check the checkbox for the specific product option 'C281-019999' under the 'Style Color' filter. | `page.locator("div:nth-child(5) > esp-filter-sub-accordion-v1 > .sub-accordion-element > .fiter-values-container > .filter-options > .filter-values-options > div:nth-child(2) > .custom-checkbox-wrapper > .pointer").click()` | | | |
| I.6 | Check the checkbox for the specific product option '004AHK003490' under the 'Style Color' filter. | `page.locator(".pointer.custom-checkbox-unchecked").first.click()` | | | |
| I.7 | Click on the 'Apply Filters' button to apply the selected product filters. | `page.get_by_role("button", name="Apply Filters").click()` | | | |
```
```markdown
| | **--- OPTIMIZATION OBJECTIVE ---** | | | | |
| J.1 | Click on the dropdown for 'Optimization Objective' to view the available options. | `page.locator("#optimizationObjective > .multiselect-dropdown > div > .w-100").click()` | | | |
| J.2 | Select the 'Optimize for Sales Unit' option from the 'Optimization Objective' dropdown. | `page.locator("div").filter(has_text=re.compile(r"^Optimize for Sales Unit$")).nth(1).click()` | | | |
```
```markdown
| | **--- PROMO RECOMMENDATIONS ---** | | | | |
| K.1 | Click on the 'Next Promo Recommendations' button to proceed to the next step in the promotion creation process. | `page.get_by_test_id("create-promotions-next-button").click()` | | | |
| K.2 | Click on 'Available Products' to view the list of products available for promotion. | `page.get_by_text("Available Products").click()` | | | |
| K.3 | Click on 'Show More' to expand the list of available products. | `page.get_by_text("Show More").click()` | | | |
| K.4 | Click on the 'Next' button to proceed to the promotion setup step. | `page.get_by_test_id("create-promotions-next-button").click()` | | | |
```
```markdown
| | **--- PROMOTION TYPE SELECTION ---** | | | | |
| L.1 | Select the first option in the dropdown or list for promotion type by clicking on it. | `page.locator(".w-100.p-h-16").first.click()` | | | |
| L.2 | Click on the 'Bundle' option to select it as the promotion type. | `page.get_by_text("Bundle").click()` | | | |
| L.3 | Click on the 'Threshold' option to select it as an additional promotion type. | `page.get_by_text("Threshold").click()` | | | |
```
```markdown
| | **--- PROMOTION RULES AND SPEND THRESHOLD ---** | | | | |
| M.1 | Click on the first checkbox to enable stacking rules or constraints. | `page.locator(".d-flex.flex-column.justify-content-center.font-size-10.align-items-center.checkbox-v2.m-r-10.zeb-check").first.click()` | | | |
| M.2 | Click on the dropdown to specify the type of promotions to compare, with a maximum limit of 5. | `page.get_by_text("What type of promotion(s) would you like to compare? *Max limit 5Promo Type").click()` | | | |
| M.3 | Click on the 'Spend Amount' field to input the spending threshold for the promotion. | `page.get_by_test_id("spend_amount").click()` | | | |
| M.4 | Enter '5000' as the spending threshold for the promotion. | `page.get_by_test_id("spend_amount").fill("5000")` | | | |
| M.5 | Click on the 'Get' field to input the discount percentage or value. | `page.locator("#get").click()` | | | |
| M.6 | Enter '25' as the discount percentage or value for the promotion. | `page.locator("#get").fill("25")` | | | |
```
```markdown
| | **--- PRICE ZONE ADJUSTMENT ---** | | | | |
| N.1 | Click on the 'Next' button to proceed to the next step in the promotion creation process. | `page.get_by_test_id("create-promotions-next-button").click()` | | | |
| N.2 | Click on 'Price Zone Adjustment' to navigate to the price zone adjustment section. | `page.get_by_text("Price Zone Adjustment").click()` | | | |
| N.3 | Click on the 'Apply' button to replicate the promotion details to sub-levels. | `page.get_by_test_id("replicate-apply").click()` | | | |
```
```markdown
| | **--- PRODUCT DETAILS NAVIGATION ---** | | | | |
| O.1 | Navigate to the 'Product Details' page by entering the specified URL in the browser. | `page.goto("https://stage.mkr.esp.antuit.ai/nglcp/product-level-details/product-details")` | | | |
```
```markdown
| | **--- APPROVAL WORKFLOW ---** | | | | |
| P.1 | Click on the 'Close' button to dismiss the current modal or overlay. | `page.get_by_role("button", name="Close").click()` | | | |
| P.2 | Click on the 'Submit All for Approval' button to initiate the approval process for the selected scenario. | `page.get_by_test_id("submit-all-for-approval").click()` | | | |
| P.3 | Confirm the submission by clicking the 'Yes, Submit' button in the confirmation modal. | `page.get_by_test_id("confirm-modal-confirm-yes-button").click()` | | | |
| P.4 | Open the 'Actions' dropdown menu to access further options for the scenario. | `page.get_by_role("button", name="Actions").click()` | | | |
| P.5 | Select the 'Approve' option from the dropdown to approve the scenario. | `page.get_by_text("Approve", exact=True).click()` | | | |
| P.6 | Confirm the approval action by clicking the 'Confirm' button in the modal. | `page.get_by_test_id("confirm-modal-confirm-yes-button").click()` | | | |
| P.7 | Reopen the 'Actions' dropdown menu to access additional options. | `page.get_by_role("button", name="Actions").click()` | | | |
| P.8 | Select the 'Reject' option from the dropdown to reject the scenario. | `page.get_by_text("Reject").click()` | | | |
| P.9 | Confirm the rejection action by clicking the 'Confirm' button in the modal. | `page.get_by_test_id("confirm-modal-confirm-yes-button").click()` | | | |
| P.10 | Reopen the 'Actions' dropdown menu to access further options. | `page.get_by_role("button", name="Actions").click()` | | | |
| P.11 | Select the 'Withdraw' option from the dropdown to withdraw the scenario. | `page.get_by_text("Withdraw", exact=True).click()` | | | |
| P.12 | Confirm the withdrawal action by clicking the 'Confirm' button in the modal. | `page.get_by_test_id("confirm-modal-confirm-yes-button").click()` | | | |
```
```markdown
| | **--- FINAL STEPS AND CLEANUP ---** | | | | |
| Q.1 | Click on the 'Next' button to proceed to the next step in the promotion creation process. | `page.get_by_test_id("create-promotions-next-button").click()` | | | |
| Q.2 | Close the current page to complete the cleanup process. | `page.close()` | | | |
| Q.3 | Close the browser context to clean up resources associated with it. | `context.close()` | | | |
| Q.4 | Close the browser instance to terminate the session completely. | `browser.close()` | | | |
```
