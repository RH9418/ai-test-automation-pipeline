```markdown
# Feature: Promo Main  
**Tab Location:** Main Workspace  

## Detailed User Interaction Flows  

| Use Case ID | Test Case Description | Exact Locator | Pass/Fail |  
|---|---|---|---|  
| | --- NAVIGATE TO PROMOTIONS PAGE AND OPEN PROMOTIONS MENU --- | | --- |  
| A.1 | Navigate to the Promotions page | `page.goto("https://stage.mkr.esp.antuit.ai/nglcp/promotions/")` | --- |  
| A.1.1 | Click on the promotions action button | `page.get_by_test_id("promotions-action-button").click()` | --- |  

| | --- CREATE A NEW PROMOTION AND CONFIGURE BASIC DETAILS --- | | --- |  
| A.2 | Click on 'New Promotion' | `page.get_by_text("New Promotion").click()` | --- |  
| A.2.1 | Click on the promotion event name field | `page.get_by_test_id("promotionEventName").click()` | --- |  
| A.2.2 | Fill the promotion event name field | `page.get_by_test_id("promotionEventName").fill("rh-1205070436")` | --- |  
| A.2.3 | Click on the promotion event description field | `page.get_by_test_id("promotionEventDescription").click()` | --- |  
| A.2.4 | Fill the promotion event description field | `page.get_by_test_id("promotionEventDescription").fill("PROMO TEST 3")` | --- |  
| A.2.5 | Click on the 'Start Date' field | `page.get_by_test_id("startDate").click()` | --- |  
| A.2.6 | Select the 9th day as the start date | `page.get_by_text("9").nth(1).click()` | --- |  
| A.2.7 | Click on the 'End Date' field | `page.get_by_test_id("endDate").click()` | --- |  
| A.2.8 | Select the 12th day as the end date | `page.get_by_text("12", exact=True).click()` | --- |  

| | --- APPLY LOCATION FILTERS --- | | --- |  
| A.3 | Enable 'ASAP Pricing' option | `page.get_by_test_id("isAsapPricing").click()` | --- |  
| A.3.1 | Click on the first '.zeb-tiers' element | `page.locator(".zeb-tiers").first.click()` | --- |  
| A.3.2 | Select 'Hierarchy' option | `page.locator("div").filter(has_text=re.compile(r"^Hierarchy$")).nth(3).click()` | --- |  
| A.3.3 | Click on 'Region' option | `page.get_by_text("Region", exact=True).click()` | --- |  
| A.3.4 | Select 'NA' radio button | `page.get_by_role("radio", name="NA", exact=True).check()` | --- |  
| A.3.5 | Click on 'Price Zone Type' | `page.get_by_text("Price Zone Type").click()` | --- |  
| A.3.6 | Select first checkbox under 'Price Zone Type' | `page.locator(".filter-values.d-flex.align-items-center.p-l-32.p-r-24 > .custom-checkbox-wrapper > .pointer").first.click()` | --- |  
| A.3.7 | Click on 'Price Zone' | `page.get_by_text("Price Zone", exact=True).click()` | --- |  
| A.3.8 | Select a checkbox under 'Price Zone' | `page.locator(".filter-values.d-flex.align-items-center.p-l-32.p-r-24 > .custom-checkbox-wrapper > .pointer").click()` | --- |  
| A.3.9 | Click on 'Apply Filters' button | `page.get_by_role("button", name="Apply Filters").click()` | --- |  

| | --- APPLY PRODUCT HIERARCHY FILTERS --- | | --- |  
| A.4 | Click on the eighth '.zeb-tiers' element | `page.locator("div:nth-child(8) > .zeb-tiers").click()` | --- |  
| A.4.1 | Click on 'Hierarchy' in '#SideFilterproducthierarchyId' | `page.locator("#SideFilterproducthierarchyId").get_by_text("Hierarchy").click()` | --- |  
| A.4.2 | Select 'Style Color' option | `page.get_by_text("Style Color").click()` | --- |  
| A.4.3 | Select a checkbox under 'Style Color' | `page.locator("div:nth-child(5) > esp-filter-sub-accordion-v1 > .sub-accordion-element > .fiter-values-container > .filter-options > .filter-values-options > .filter-values.d-flex.align-items-center.p-l-32.p-r-12 > .custom-checkbox-wrapper > .pointer").click()` | --- |  
| A.4.4 | Click on the sixth child checkbox | `page.locator("div:nth-child(6) > .custom-checkbox-wrapper > .pointer").click()` | --- |  
| A.4.5 | Click on the fifth child checkbox | `page.locator("div:nth-child(5) > .custom-checkbox-wrapper > .pointer").click()` | --- |  
| A.4.6 | Click on 'Apply Filters' button | `page.get_by_role("button", name="Apply Filters").click()` | --- |  

| | --- SELECT OPTIMIZATION OBJECTIVE --- | | --- |  
| A.5 | Open dropdown for optimization objective | `page.locator("#optimizationObjective > .multiselect-dropdown > div > .w-100").click()` | --- |  
| A.5.1 | Select 'Optimize for Sales Unit' | `page.locator("div").filter(has_text=re.compile(r"^Optimize for Sales Unit$")).nth(1).click()` | --- |  
| A.5.2 | Click 'Next' button | `page.get_by_test_id("create-promotions-next-button").click()` | --- |  

| | --- CONFIGURE GRID SETTINGS AND SEARCH FOR PRODUCTS --- | | --- |  
| A.6 | Click on 'Show More' | `page.get_by_text("Show More").click()` | --- |  
| A.6.1 | Select 'Column with Header Selection' checkbox | `page.get_by_role("checkbox", name="Column with Header Selection").check()` | --- |  
| A.6.2 | Click on promotions action button | `page.get_by_test_id("promotions-action-button").click()` | --- |  
| A.6.3 | Click 'Reset Preferences' | `page.get_by_text("Reset Preferences").click()` | --- |  
| A.6.4 | Focus on search textbox | `page.get_by_role("textbox", name="Search").click()` | --- |  
| A.6.5 | Fill search textbox with '005' | `page.get_by_role("textbox", name="Search").fill("005")` | --- |  
| A.6.6 | Submit search query | `page.get_by_role("textbox", name="Search").press("Enter")` | --- |  
| A.6.7 | Click on second link in list | `page.locator("a").nth(1).click()` | --- |  

| | --- APPLY PRODUCT FILTERS AND SELECT SPECIFIC PRODUCTS --- | | --- |  
| A.7 | Click on 'Available Products' | `page.get_by_text("Available Products").click()` | --- |  
| A.7.1 | Open dropdown for product filtering | `page.locator("div:nth-child(3) > div > esp-multiselect-dropdown > .multiselect-dropdown > div > .w-100 > .d-flex.align-items-center > .dropdown-caret").click()` | --- |  
| A.7.2 | Select specific filter option | `page.locator("div:nth-child(7) > .d-flex").click()` | --- |  
| A.7.3 | Interact with grid center column | `page.locator(".ag-center-cols-viewport").click()` | --- |  
| A.7.4 | Select first item in list | `page.locator(".w-100.p-h-16").first.click()` | --- |  
| A.7.5 | Click first dropdown option | `page.locator(".d-flex.dropdown-option.align-items-center.p-v-5.p-l-32").first.click()` | --- |  
| A.7.6 | Select '21_Men's Underwear' | `page.get_by_text("21_Men's Underwear").click()` | --- |  
| A.7.7 | Open additional dropdown | `page.locator("div:nth-child(2) > div > esp-multiselect-dropdown > .multiselect-dropdown > div > .w-100 > .d-flex.align-items-center > .dropdown-caret").click()` | --- |  
| A.7.8 | Open third dropdown | `page.locator("div:nth-child(3) > div > esp-multiselect-dropdown > .multiselect-dropdown > div > .w-100 > .d-flex.align-items-center > .dropdown-caret").click()` | --- |  
| A.7.9 | Select first option in flex column dropdown | `page.locator(".d-flex.flex-column.justify-content-center").first.click()` | --- |  
| A.7.10 | Select second option in overflow auto dropdown | `page.locator(".overflow-auto > div:nth-child(2) > .d-flex").click()` | --- |  
| A.7.11 | Apply complex filter | `page.get_by_test_id("complex-filter-apply").click()` | --- |  

| | --- ADD AND CONFIGURE PROMOTION DETAILS --- | | --- |  
| A.8 | Enable promotion creation checkbox | `page.locator("#ag-2170-input").check()` | --- |  
| A.8.1 | Click on 'Promotions Action' button | `page.get_by_test_id("promotions-action-button").click()` | --- |  
| A.8.2 | Click on 'Add' | `page.get_by_text("Add").click()` | --- |  
| A.8.3 | Confirm action in modal | `page.get_by_test_id("confirm-modal-confirm-yes-button").click()` | --- |  
| A.8.4 | Click on 'Reoptimize' button | `page.get_by_role("button", name="Reoptimize").click()` | --- |  
| A.8.5 | Confirm reoptimization in modal | `page.get_by_test_id("confirm-modal-confirm-yes-button").click()` | --- |  
| A.8.6 | Click 'Next' button | `page.get_by_test_id("create-promotions-next-button").click()` | --- |  
| A.8.7 | Open dropdown for promotion type | `page.locator(".dropdown-caret").first.click()` | --- |  
| A.8.8 | Select 'BOGO' promotion type | `page.get_by_text("BOGO").click()` | --- |  
| A.8.9 | Click on first row for group details | `page.locator(".row").first.click()` | --- |  
| A.8.10 | Open dropdown for buy groups | `page.locator("#numberOfBuyGroups > .multiselect-dropdown > div > .w-100 > .d-flex.align-items-center > .dropdown-caret").click()` | --- |  
| A.8.11 | Select '1' as buy groups | `page.locator("div").filter(has_text=re.compile(r"^1$")).nth(1).click()` | --- |  
| A.8.12 | Open dropdown for units to buy | `page.locator("#numberOfUnitsToBuyFromEachGroup > .multiselect-dropdown > div > .w-100 > .d-flex.align-items-center > .dropdown-caret").click()` | --- |  
| A.8.13 | Select '1' as units to buy | `page.locator("div").filter(has_text=re.compile(r"^1$")).nth(1).click()` | --- |  
| A.8.14 | Click on 'Add Value' textbox | `page.get_by_role("textbox", name="Add Value").click()` | --- |  
| A.8.15 | Fill 'Add Value' textbox with '34' | `page.get_by_role("textbox", name="Add Value").fill("34")` | --- |  
| A.8.16 | Click 'Add Group' button | `page.get_by_test_id("group-add").first.click()` | --- |  
| A.8.17 | Click on 'Product IDs' field | `page.get_by_test_id("product-ids").click()` | --- |  
| A.8.18 | Fill 'Product IDs' field with '005DKI004106' | `page.get_by_test_id("product-ids").fill("005DKI004106")` | --- |  
| A.8.19 | Click 'Save' button | `page.get_by_test_id("save").click()` | --- |  

| | --- SAVE PROMOTION DETAILS AND ADD ADDITIONAL GROUPS --- | | --- |  
| A.9 | Click 'Add Group' | `page.get_by_test_id("group-add").click()` | --- |  
| A.9.1 | Click on 'Product IDs' field | `page.get_by_test_id("product-ids").click()` | --- |  
| A.9.2 | Fill 'Product IDs' field with '022DKI005106' | `page.get_by_test_id("product-ids").fill("022DKI005106")` | --- |  
| A.9.3 | Click 'Save' | `page.get_by_test_id("save").click()` | --- |  
| A.9.4 | Click 'Next' | `page.get_by_test_id("create-promotions-next-button").click()` | --- |  

| | --- REPLICATE PROMOTION SETTINGS AND ADJUST ATTRIBUTES --- | | --- |  
| A.10 | Click 'Replicate' | `page.get_by_test_id("replicate").click()` | --- |  
| A.10.1 | Click on 'Attribute Value' field | `page.locator("#attribute_value").click()` | --- |  
| A.10.2 | Fill 'Attribute Value' field with '45' | `page.locator("#attribute_value").fill("45")` | --- |  
| A.10.3 | Press 'Enter' to confirm | `page.locator("#attribute_value").press("Enter")` | --- |  
| A.10.4 | Click on 'End Date' field | `page.locator("#end_date").click()` | --- |  
| A.10.5 | Select 18th day as end date | `page.get_by_text("18").click()` | --- |  
| A.10.6 | Click on grid cell with '$ (1.00000)' | `page.get_by_role("gridcell", name="$ (1.00000)").click()` | --- |  

| | --- FINALIZE PROMOTION CREATION AND CLOSE SESSION --- | | --- |  
| A.11 | Close the page | `page.close()` | --- |  
| A.11.1 | Close the context | `context.close()` | --- |  
| A.11.2 | Close the browser | `browser.close()` | --- |  
```