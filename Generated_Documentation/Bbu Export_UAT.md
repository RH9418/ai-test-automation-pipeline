# Feature: Bbu Export
**Tab Location:** Main Workspace

## Detailed User Interaction Flows

| Use Case ID | Test Case Description | Exact Locator | Pass/Fail | Notes | Issues |
|:---|:---|:---|:---|:---|:---|
```
| | **--- PAGE NAVIGATION ---** | | | | |
| C.1 | Navigate to the Executive Dashboard in the Demand Planning module by entering the specified URL. | `page.goto("https://stage.bbu.esp.antuit.ai/dp/demand-planning/executive-dashboard?workbookId=4&tabIndex=7")` | | | |
```
```
| | **--- FILTER INTERACTION ---** | | | | |
| D.1 | Open the filter configuration by clicking on the 'FilterStart Week 01/25/2026' text. | `page.get_by_text("FilterStart Week 01/25/2026").click()` | | | |
| D.2 | Expand the filter options by clicking on the 'Filter' text. | `page.get_by_text("Filter").click()` | | | |
| D.3 | Open the date range selection by clicking on 'Start Week / End Week'. | `page.get_by_text("Start Week / End Week").click()` | | | |
```
```
| | **--- DATE PICKER INTERACTION ---** | | | | |
| E.1 | Click on the date picker input field to open the calendar widget. | `page.locator("#Datepick").click()` | | | |
| E.2 | Select the month and year header displaying '‹ January 2026 ›' to navigate the calendar. | `page.locator("div").filter(has_text="‹ January 2026 ›").nth(4).click()` | | | |
| E.3 | Click on the first occurrence of the date '4' in the calendar to select it. | `page.get_by_text("4").first.click()` | | | |
| E.4 | Click on the 'January' button to open the month selection dropdown. | `page.get_by_role("button", name="January").click()` | | | |
| E.5 | Select 'February' from the month dropdown. | `page.get_by_text("February").first.click()` | | | |
| E.6 | Click on the '2026' button to open the year selection dropdown. | `page.get_by_role("button", name="2026").first.click()` | | | |
| E.7 | Select the year '2025' from the year grid. | `page.get_by_role("gridcell", name="2025").click()` | | | |
| E.8 | Click on the '2026' button to return to the year selection dropdown. | `page.get_by_role("button", name="2026").click()` | | | |
| E.9 | Select the year '2024' from the year grid. | `page.get_by_role("gridcell", name="2024").click()` | | | |
| E.10 | Select the second occurrence of 'January' from the month grid. | `page.get_by_role("gridcell", name="January").nth(1).click()` | | | |
| E.11 | Click on the exact date '2' in the calendar to select it. | `page.get_by_text("2", exact=True).nth(2).click()` | | | |
| E.12 | Click on the 'Start Week 01/25/2026 End' text to finalize the date selection. | `page.get_by_text("Start Week 01/25/2026 End").click()` | | | |
```
```
| | **--- DROPDOWN INTERACTION ---** | | | | |
| F.1 | Click on the 'Total ByProduct Level None' dropdown to open the options. | `page.get_by_text("Total ByProduct Level None").click()` | | | |
| F.2 | Click on the 'Total By' option to select it. | `page.get_by_text("Total By").click()` | | | |
| F.3 | Click on the 'Product Level None Location' dropdown to open the options. | `page.get_by_text("Product Level None Location").click()` | | | |
| F.4 | Click on the 'Product Level' option to select it. | `page.get_by_text("Product Level").click()` | | | |
| F.5 | Click on the first occurrence of 'None' in the dropdown to select it. | `page.get_by_text("None").first.click()` | | | |
| F.6 | Click on the 'Select All' option to select all available product levels. | `page.get_by_text("Select All").click()` | | | |
| F.7 | Click on the first element with the locator '.d-flex.flex-column.justify-content-center' to confirm the selection. | `page.locator(".d-flex.flex-column.justify-content-center").first.click()` | | | |
| F.8 | Click on 'Brand Level 4' to select it. | `page.get_by_text("Brand Level 4").click()` | | | |
```
```
| | **--- BRAND SELECTION ---** | | | | |
| G.1 | Click on 'Brand Level 3' to select it. | `page.get_by_text("Brand Level 3").click()` | | | |
| G.2 | Click on 'Brand Level 2' to select it. | `page.get_by_text("Brand Level 2").click()` | | | |
| G.3 | Click on the third child element within the '.overflow-auto' container to select it. | `page.locator(".overflow-auto > div:nth-child(3)").click()` | | | |
| G.4 | Click on 'UPC' to select it. | `page.get_by_text("UPC").click()` | | | |
```
```
| | **--- PRODUCT SELECTION ---** | | | | |
| H.1 | Click on 'Product Level 4' to select it. | `page.get_by_text("Product Level 4").click()` | | | |
| H.2 | Click on 'Product Level 3' to select it. | `page.get_by_text("Product Level 3").click()` | | | |
| H.3 | Click on 'Product Level 2' to select it. | `page.get_by_text("Product Level 2").click()` | | | |
```
```
| | **--- LOCATION LEVEL SELECTION ---** | | | | |
| I.1 | Click on 'Location Level' to open the location level dropdown. | `page.get_by_text("Location Level").click()` | | | |
| I.2 | Click on the first occurrence of 'None' in the location level dropdown to select it. | `page.get_by_text("None").first.click()` | | | |
| I.3 | Click on 'Select All' to select all available location levels. | `page.get_by_text("Select All").click()` | | | |
| I.4 | Click on 'Sales Level 6' to select it. | `page.get_by_text("Sales Level 6").click()` | | | |
| I.5 | Click on 'Sales Level 5' to select it from the Location Level dropdown. | `page.get_by_text("Sales Level 5", exact=True).click()` | | | |
| I.6 | Click on 'Sales Level 4' to select it from the Location Level dropdown. | `page.get_by_text("Sales Level 4", exact=True).click()` | | | |
| I.7 | Click on the eighth child element within the dropdown to select 'City'. | `page.locator("div:nth-child(8)").click()` | | | |
| I.8 | Click on 'Sales Level 1' to select it from the Location Level dropdown. | `page.get_by_text("Sales Level 1", exact=True).click()` | | | |
| I.9 | Click on the fifth child element within the '.overflow-auto' container to select 'Sales Level 3'. | `page.locator(".overflow-auto > div:nth-child(5)").click()` | | | |
| I.10 | Click on the seventh child element within the dropdown to select 'Sales Level 1'. | `page.locator("div:nth-child(7)").click()` | | | |
| I.11 | Click on 'Depot' to select it from the Location Level dropdown. | `page.get_by_text("Depot", exact=True).click()` | | | |
| I.12 | Click on 'Sales Level 3' to select it from the Location Level dropdown. | `page.get_by_text("Sales Level 3", exact=True).click()` | | | |
| I.13 | Click on 'BUSS Environment' to select it from the Location Level dropdown. | `page.get_by_text("BUSS Environment", exact=True).click()` | | | |
```
```
| | **--- BUSS ROUTE AND CUSTOMER LEVEL SELECTION ---** | | | | |
| J.1 | Click on the span element containing the text 'BUSS Route ID' to select it. | `page.locator("span").filter(has_text="BUSS Route ID").click()` | | | |
| J.2 | Click on the dropdown for the second multiselect field under Location Level to open it. | `page.locator("div:nth-child(2) > esp-multiselect-dropdown > .multiselect-dropdown > div > .w-100").click()` | | | |
| J.3 | Click on 'Customer Level' to select it from the dropdown. | `page.get_by_text("Customer Level").click()` | | | |
| J.4 | Click on the dropdown for the third multiselect field under Customer Level to open it. | `page.locator("div:nth-child(3) > esp-multiselect-dropdown > .multiselect-dropdown > div > .w-100").click()` | | | |
| J.5 | Click on 'Select All' to select all options under Customer Level. | `page.get_by_text("Select All").click()` | | | |
| J.6 | Click on the third occurrence of 'All' to select it under Customer Level. | `page.get_by_text("All").nth(3).click()` | | | |
```
```
| | **--- TIME AND MEASURES SELECTION ---** | | | | |
| K.1 | Click on 'Time' to open the Time dropdown. | `page.get_by_text("Time").click()` | | | |
| K.2 | Click on the second occurrence of 'None' to select it under Time. | `page.get_by_text("None").nth(1).click()` | | | |
| K.3 | Click on the third occurrence of 'Weekly' to select it under Time. | `page.locator("div").filter(has_text=re.compile(r"^Weekly$")).nth(3).click()` | | | |
| K.4 | Click on 'Measures' to open the Measures dropdown. | `page.get_by_text("Measures", exact=True).click()` | | | |
```
```
| | **--- MEASURE SELECTION WORKFLOW ---** | | | | |
| L.1 | Click on the '.measure-filter-list' element to open the measure filter options. | `page.locator(".measure-filter-list").click()` | | | |
| L.2 | Click on 'Measure' to select it from the Measures dropdown. | `page.get_by_text("Measure", exact=True).click()` | | | |
| L.3 | Click on the first occurrence of 'All Measures' to select it. | `page.get_by_text("All Measures").first.click()` | | | |
| L.4 | Click on 'Select All Measures' to select all available measures. | `page.get_by_text("Select All Measures").click()` | | | |
| L.5 | Click on 'Select All Measures' again to confirm the selection. | `page.get_by_text("Select All Measures").click()` | | | |
| L.6 | Click on 'User Forecast Total' to select it from the Measures dropdown. | `page.get_by_text("User Forecast Total").click()` | | | |
| L.7 | Click on the first '.d-flex.dropdown-option.align-items-center.p-v-5.p-l-32' element to confirm the selection. | `page.locator(".d-flex.dropdown-option.align-items-center.p-v-5.p-l-32").first.click()` | | | |
| L.8 | Click on 'User Forecast Base' to select it from the Measures dropdown. | `page.get_by_text("User Forecast Base").click()` | | | |
| L.9 | Click on the third child element within the '.overflow-auto' container to select 'User Override Total'. | `page.locator(".overflow-auto > div:nth-child(3)").click()` | | | |
| L.10 | Click on the fifth child element within the '.overflow-auto' container to select 'User Override Base'. | `page.locator(".overflow-auto > div:nth-child(5)").click()` | | | |
| L.11 | Click on 'Select All Measures' to select all measures again. | `page.get_by_text("Select All Measures").click()` | | | |
| L.12 | Click on the text 'Measure' to ensure the Measures dropdown is selected. | `page.get_by_text("Measure", exact=True).click()` | | | |
```
```
| | **--- DOWNLOAD AND RESET ACTIONS ---** | | | | |
| M.1 | Click on the 'Download' button to initiate the download process. | `page.get_by_role("button", name="Download").click()` | | | |
| M.2 | Click on the text 'Please note that a maximum of' to display the information about the maximum number of rows that can be exported. | `page.get_by_text("Please note that a maximum of").click()` | | | |
| M.3 | Click on the 'Reset' button to reset the filter selections. | `page.get_by_role("button", name="Reset").click()` | | | |
| M.4 | Click on the 'Reset' button again to confirm the reset action. | `page.get_by_role("button", name="Reset").click()` | | | |
```
