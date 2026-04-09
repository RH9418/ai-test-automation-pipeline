```markdown
# Feature: Promo Discount  
**Tab Location:** Main Workspace  

## Detailed User Interaction Flows  

| Use Case ID | Test Case Description | Exact Locator | Pass/Fail |  
|---|---|---|---|  
| | --- NAVIGATE TO PROMOTIONS LANDING PAGE AND ACCESS PROMOTIONS MANAGEMENT SECTION --- | | --- |  
| A.1 | Navigate to Promotions Landing Page and Access Promotions Management Section | | --- |  
| A.1.1 | Navigate to the Promotions Landing Page | `page.goto("https://stage.mkr.esp.antuit.ai/nglcp/promotions/landing-page")` | --- |  
| A.1.2 | Click on the 'Promotions Action' button | `page.get_by_test_id("promotions-action-button").click()` | --- |  

| | --- CREATE A NEW PROMOTION AND ENTER BASIC PROMOTION DETAILS (NAME, DESCRIPTION, DATES) --- | | --- |  
| A.2 | Create a New Promotion and Enter Basic Promotion Details | | --- |  
| A.2.1 | Click on 'New Promotion' | `page.get_by_text("New Promotion").click()` | --- |  
| A.2.2 | Focus on the 'Promotion Event Name' input field | `page.get_by_test_id("promotionEventName").click()` | --- |  
| A.2.3 | Fill in the 'Promotion Event Name' field | `page.get_by_test_id("promotionEventName").fill("rh1230-08-04")` | --- |  
| A.2.4 | Focus on the 'Promotion Event Description' input field | `page.get_by_test_id("promotionEventDescription").click()` | --- |  
| A.2.5 | Fill in the 'Promotion Event Description' field | `page.get_by_test_id("promotionEventDescription").fill("PROMO DISCOUNT TEST")` | --- |  
| A.2.6 | Open the date picker for the 'Start Date' field | `page.get_by_test_id("startDate").click()` | --- |  
| A.2.7 | Select the 17th day of the month as the start date | `page.get_by_text("17").click()` | --- |  
| A.2.8 | Open the date picker for the 'End Date' field | `page.get_by_test_id("endDate").click()` | --- |  
| A.2.9 | Select the 18th day of the month as the end date | `page.get_by_text("18").click()` | --- |  

| | --- CONFIGURE PRICING OPTIONS (ASAP PRICING, REGULAR PRICING) --- | | --- |  
| A.3 | Configure Pricing Options | | --- |  
| A.3.1 | Enable the 'ASAP Pricing' option | `page.get_by_test_id("isAsapPricing").click()` | --- |  
| A.3.2 | Select the 'Regular Pricing' type | `page.get_by_test_id("price_type_reg").click()` | --- |  

| | --- APPLY HIERARCHY FILTERS (REGION, PRICE ZONE TYPE, PRICE ZONE) --- | | --- |  
| A.4 | Apply Hierarchy Filters | | --- |  
| A.4.1 | Click on the first element in the '.zeb-tiers' section | `page.locator(".zeb-tiers").first.click()` | --- |  
| A.4.2 | Select the 'Hierarchy' tab | `page.locator("div").filter(has_text=re.compile(r"^Hierarchy$")).nth(3).click()` | --- |  
| A.4.3 | Click on the first element in the '.d-flex.p-l-32' section | `page.locator(".d-flex.p-l-32").first.click()` | --- |  
| A.4.4 | Select the 'NA' radio button | `page.get_by_role("radio", name="NA", exact=True).check()` | --- |  
| A.4.5 | Click on the 'Price Zone Type' option | `page.get_by_text("Price Zone Type").click()` | --- |  
| A.4.6 | Select the third checkbox under 'Price Zone Type' | `page.locator("div:nth-child(3) > .custom-checkbox-wrapper > .pointer").click()` | --- |  
| A.4.7 | Click on the 'Price Zone' option | `page.get_by_text("Price Zone", exact=True).click()` | --- |  
| A.4.8 | Select the first checkbox under 'Price Zone' | `page.locator(".filter-values.d-flex.align-items-center.p-l-32.p-r-24 > .custom-checkbox-wrapper > .pointer").first.click()` | --- |  
| A.4.9 | Revisit the 'Price Zone Type' option | `page.get_by_text("Price Zone Type").click()` | --- |  
| A.4.10 | Deselect the first selected checkbox under 'Price Zone Type' | `page.locator(".pointer.custom-checkbox-checked").first.click()` | --- |  
| A.4.11 | Re-select the first checkbox under 'Price Zone' | `page.locator(".filter-values.d-flex.align-items-center.p-l-32.p-r-24 > .custom-checkbox-wrapper > .pointer").first.click()` | --- |  
| A.4.12 | Revisit the 'Price Zone' option | `page.get_by_text("Price Zone", exact=True).click()` | --- |  
| A.4.13 | Select an additional checkbox under 'Price Zone' | `page.locator(".filter-values.d-flex.align-items-center.p-l-32.p-r-24 > .custom-checkbox-wrapper > .pointer").click()` | --- |  
| A.4.14 | Click on the 'Apply Filters' button | `page.get_by_role("button", name="Apply Filters").click()` | --- |  

| | --- REFINE PRODUCT SELECTION USING HIERARCHY AND STYLE FILTERS --- | | --- |  
| A.5 | Refine Product Selection Using Hierarchy and Style Filters | | --- |  
| A.5.1 | Click on the 'Tiers' section | `page.locator("div:nth-child(8) > .zeb-tiers").click()` | --- |  
| A.5.2 | Open the 'Hierarchy' filter dropdown | `page.locator("#SideFilterproducthierarchyId").get_by_text("Hierarchy").click()` | --- |  
| A.5.3 | Select the 'Style Color' option | `page.get_by_text("Style Color").click()` | --- |  
| A.5.4 | Select a specific filter option | `page.locator("div:nth-child(5) > esp-filter-sub-accordion-v1 > .sub-accordion-element > .fiter-values-container > .filter-options > .filter-values-options > .filter-values.d-flex.align-items-center.p-l-32.p-r-12 > .custom-checkbox-wrapper > .pointer").click()` | --- |  
| A.5.5 | Select another filter option | `page.locator("div:nth-child(7) > .custom-checkbox-wrapper > .pointer").click()` | --- |  
| A.5.6 | Apply the selected filters | `page.get_by_role("button", name="Apply Filters").click()` | --- |  

| | --- SELECT OPTIMIZATION OBJECTIVE FOR THE PROMOTION --- | | --- |  
| A.6 | Select Optimization Objective for the Promotion | | --- |  
| A.6.1 | Open the dropdown for selecting the optimization objective | `page.locator("#optimizationObjective > .multiselect-dropdown > div > .w-100 > .d-flex.align-items-center > .dropdown-caret").click()` | --- |  
| A.6.2 | Choose 'Optimize Sales Revenue' | `page.locator("div").filter(has_text=re.compile(r"^Optimize Sales Revenue$")).nth(1).click()` | --- |  

| | --- ADD PRODUCTS TO THE PROMOTION FROM THE AVAILABLE PRODUCTS SECTION --- | | --- |  
| A.7 | Add Products to the Promotion | | --- |  
| A.7.1 | Navigate to the 'Available Products' section | `page.get_by_text("Available Products").click()` | --- |  
| A.7.2 | Open the first dropdown in the 'Available Products' section | `page.locator(".dropdown-caret").first.click()` | --- |  
| A.7.3 | Select the first product option | `page.locator(".d-flex.dropdown-option.align-items-center.p-v-5.p-l-32 > .d-flex").first.click()` | --- |  
| A.7.4 | Open another dropdown for additional product selection | `page.locator("div:nth-child(2) > div > esp-multiselect-dropdown > .multiselect-dropdown > div > .w-100 > .d-flex.align-items-center > .dropdown-caret").click()` | --- |  
| A.7.5 | Select the first option from the dropdown | `page.locator(".d-flex.dropdown-option").first.click()` | --- |  
| A.7.6 | Click on a specific product from the list | `page.locator(".overflow-auto > div:nth-child(2)").click()` | --- |  
| A.7.7 | Open the third dropdown for further product selection | `page.locator("div:nth-child(3) > div > esp-multiselect-dropdown > .multiselect-dropdown > div > .w-100 > .d-flex.align-items-center > .dropdown-caret").click()` | --- |  
| A.7.8 | Select the first option from the dropdown | `page.locator(".d-flex.flex-column.justify-content-center").first.click()` | --- |  
| A.7.9 | Select the product '203_Logo Knits' | `page.get_by_text("203_Logo Knits").click()` | --- |  
| A.7.10 | Apply the complex filter settings | `page.get_by_test_id("complex-filter-apply").click()` | --- |  

| | --- PERFORM ACTIONS ON PROMOTIONS (ADD, REOPTIMIZE, CONFIRM ACTIONS) --- | | --- |  
| A.8 | Perform Actions on Promotions | | --- |  
| A.8.1 | Select the first promotion row | `page.locator(".ag-row-odd > .ag-cell > .ag-cell-wrapper").first.click()` | --- |  
| A.8.2 | Click on the 'Actions' button | `page.get_by_test_id("promotions-action-button").click()` | --- |  
| A.8.3 | Select the 'Add' option | `page.get_by_text("Add").click()` | --- |  
| A.8.4 | Confirm the addition of the new promotion | `page.get_by_test_id("confirm-modal-confirm-yes-button").click()` | --- |  
| A.8.5 | Click the 'Reoptimize' button | `page.get_by_role("button", name="Reoptimize").click()` | --- |  
| A.8.6 | Confirm the reoptimization action | `page.get_by_test_id("confirm-modal-confirm-yes-button").click()` | --- |  

| | --- CONFIGURE DISCOUNT ADJUSTMENTS (PERCENTAGE, PRICE ZONE ADJUSTMENTS, ROUNDING RULES) --- | | --- |  
| A.9 | Configure Discount Adjustments | | --- |  
| A.9.1 | Click on the 'Off' input field | `page.locator("#off").click()` | --- |  
| A.9.2 | Set the discount percentage to '30' | `page.locator("#off").fill("30")` | --- |  
| A.9.3 | Select the 'Price Zone Adjustment' option | `page.get_by_text("Price Zone Adjustment").click()` | --- |  
| A.9.4 | Open the dropdown menu for rounding rules | `page.locator("#rounding_rules_id > .multiselect-dropdown > div > .w-100 > .d-flex.align-items-center > .dropdown-caret").click()` | --- |  
| A.9.5 | Select the rounding rule '.99 RN' | `page.locator("div").filter(has_text=re.compile(r"^\.99 RN$")).nth(1).click()` | --- |  
| A.9.6 | Click on the 'Attribute Value' input field | `page.locator("#attribute_value").click()` | --- |  
| A.9.7 | Set the attribute value to '35' | `page.locator("#attribute_value").fill("35")` | --- |  

| | --- REPLICATE ADJUSTMENTS ACROSS PROMOTIONS --- | | --- |  
| A.10 | Replicate Adjustments Across Promotions | | --- |  
| A.10.1 | Open the dropdown menu to configure additional settings | `page.locator(".dropdown-caret").first.click()` | --- |  
| A.10.2 | Reopen the dropdown menu to finalize the configuration | `page.locator(".dropdown-caret").first.click()` | --- |  
| A.10.3 | Click the 'Apply' button to replicate adjustments | `page.get_by_test_id("replicate-apply").click()` | --- |  

| | --- NAVIGATE TO PRODUCT-LEVEL DETAILS PAGE FOR FURTHER ANALYSIS --- | | --- |  
| A.11 | Navigate to Product-Level Details Page | | --- |  
| A.11.1 | Navigate to the 'Product-Level Details' page | `page.goto("https://stage.mkr.esp.antuit.ai/nglcp/product-level-details/product-details")` | --- |  
```