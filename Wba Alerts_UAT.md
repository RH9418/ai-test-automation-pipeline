# Feature: Wba Alerts
**Tab Location:** Main Workspace

## Detailed User Interaction Flows

| Use Case ID | Test Case Description | Exact Locator | Pass/Fail |
|---|---|---|---|
```
| | --- NAVIGATION TO EXECUTIVE DASHBOARD --- | | --- |
| C.1 | Navigate to the Executive Dashboard page by opening the specified URL. | `page.goto("https://stage.wba.esp.antuit.ai/dp/demand-planning/executive-dashboard?workbookId=6&tabIndex=1")` | Pass/Fail |
```
```
| | --- ALERTS FILTER INTERACTION --- | | --- |
| D.1 | Click on the 'Alerts' filter dropdown to expand the filter options. | `page.locator("#alerts-filterId").click()` | Pass/Fail |
| D.2 | Select the 'MAPE' option from the dropdown list. | `page.locator("div").filter(has_text=re.compile(r"^MAPE$")).nth(1).click()` | Pass/Fail |
| D.3 | Click on the dropdown caret to open the filter options again. | `page.locator(".w-100.p-h-16.p-v-8.dropdown-label.background-white > .d-flex.align-items-center > .dropdown-caret").click()` | Pass/Fail |
| D.4 | Select the 'Under Bias' option from the dropdown list. | `page.locator("div").filter(has_text=re.compile(r"^Under Bias$")).nth(1).click()` | Pass/Fail |
| D.5 | Click on the dropdown caret to open the filter options again. | `page.locator(".w-100.p-h-16.p-v-8.dropdown-label.background-white > .d-flex.align-items-center > .dropdown-caret").click()` | Pass/Fail |
| D.6 | Select the 'Over Bias' option from the dropdown list. | `page.locator("div").filter(has_text=re.compile(r"^Over Bias$")).nth(1).click()` | Pass/Fail |
| D.7 | Click on the dropdown caret to open the filter options again. | `page.locator(".w-100.p-h-16.p-v-8.dropdown-label.background-white > .d-flex.align-items-center > .dropdown-caret").click()` | Pass/Fail |
| D.8 | Select the 'PVA' option from the dropdown list. | `page.locator("div").filter(has_text=re.compile(r"^PVA$")).nth(1).click()` | Pass/Fail |
| D.9 | Click on the dropdown caret to open the filter options again. | `page.locator(".w-100.p-h-16.p-v-8.dropdown-label.background-white > .d-flex.align-items-center > .dropdown-caret").click()` | Pass/Fail |
| D.10 | Select the 'SSIS' option from the dropdown list. | `page.locator("div").filter(has_text=re.compile(r"^SSIS$")).first.click()` | Pass/Fail |
```
```
| | --- COLUMN VISIBILITY CONFIGURATION --- | | --- |
| E.1 | Click on the 'Columns' button to open the column visibility configuration panel. | `page.get_by_role("button", name="columns").click()` | Pass/Fail |
| E.2 | Uncheck the 'Toggle All Columns Visibility' checkbox to hide all columns initially. | `page.get_by_role("checkbox", name="Toggle All Columns Visibility").uncheck()` | Pass/Fail |
| E.3 | Check the 'Store Count Column' checkbox to make the 'Store Count' column visible. | `page.get_by_role("treeitem", name="Store Count Column").get_by_label("Press SPACE to toggle").check()` | Pass/Fail |
| E.4 | Check the 'Product Count Column' checkbox to make the 'Product Count' column visible. | `page.get_by_role("treeitem", name="Product Count Column").get_by_label("Press SPACE to toggle").check()` | Pass/Fail |
| E.5 | Check the 'Stability Column' checkbox to make the 'Stability' column visible. | `page.get_by_role("treeitem", name="Stability Column").get_by_label("Press SPACE to toggle").check()` | Pass/Fail |
| E.6 | Check the 'SSIS Column' checkbox to make the 'SSIS' column visible. | `page.get_by_role("treeitem", name="SSIS Column").get_by_label("Press SPACE to toggle").check()` | Pass/Fail |
| E.7 | Check the 'User Bias Column' checkbox to make the 'User Bias' column visible. | `page.get_by_role("treeitem", name="User Bias Column").get_by_label("Press SPACE to toggle").check()` | Pass/Fail |
| E.8 | Check the 'System Bias Column' checkbox to make the 'System Bias' column visible. | `page.get_by_role("treeitem", name="System Bias Column").get_by_label("Press SPACE to toggle").check()` | Pass/Fail |
| E.9 | Check the 'User MAPE Column' checkbox to make the 'User MAPE' column visible. | `page.get_by_role("treeitem", name="User MAPE Column").get_by_label("Press SPACE to toggle visibility (hidden)").check()` | Pass/Fail |
| E.10 | Check the 'System MAPE Column' checkbox to make the 'System MAPE' column visible. | `page.get_by_role("treeitem", name="System MAPE Column").get_by_label("Press SPACE to toggle visibility (hidden)").check()` | Pass/Fail |
| E.11 | Check the 'Planner Value Add Column' checkbox to make the 'Planner Value Add' column visible. | `page.get_by_role("treeitem", name="Planner Value Add Column").get_by_label("Press SPACE to toggle visibility (hidden)").check()` | Pass/Fail |
| E.12 | Check the '13W-Fcst Column' checkbox to make the '13W-Fcst' column visible. | `page.get_by_role("treeitem", name="13W-Fcst Column").get_by_label("Press SPACE to toggle visibility (hidden)").check()` | Pass/Fail |
```
```
| | --- COLUMN FILTERING AND SELECTION --- | | --- |
| F.1 | Click on the column selector element to open the column selection panel. | `page.locator("div:nth-child(11) > .ag-column-select-column").click()` | Pass/Fail |
| F.2 | Click on the 'Filter Columns Input' textbox to focus on it for entering a filter value. | `page.get_by_role("textbox", name="Filter Columns Input").click()` | Pass/Fail |
| F.3 | Fill the 'Filter Columns Input' textbox with the value 'Store Count' to filter the columns. | `page.get_by_role("textbox", name="Filter Columns Input").fill("Store Count")` | Pass/Fail |
| F.4 | Press 'Enter' to apply the filter and display the filtered column options. | `page.get_by_role("textbox", name="Filter Columns Input").press("Enter")` | Pass/Fail |
| F.5 | Check the checkbox for the filtered column to make it visible. | `page.get_by_role("checkbox", name="Press SPACE to toggle").check()` | Pass/Fail |
| F.6 | Click on the 'Columns' button to close the column selection panel. | `page.get_by_role("button", name="columns").click()` | Pass/Fail |
```
```
| | --- ROW SELECTION AND FILTERING --- | | --- |
| G.1 | Select the radio button for the row with the name '002-SPIRITS' to apply row selection. | `page.get_by_role("row", name=" 002-SPIRITS").get_by_role("radio").check()` | Pass/Fail |
| G.2 | Click on the first 'Filter' button to open the filter configuration for the selected column. | `page.get_by_title("Filter").first.click()` | Pass/Fail |
| G.3 | Fill the 'Filter Value' textbox with '002-SPIRITS' to filter rows based on this value. | `page.get_by_role("textbox", name="Filter Value").fill("002-SPIRITS")` | Pass/Fail |
| G.4 | Click on the 'Apply' button to apply the column filter and update the displayed rows. | `page.get_by_label("Column Filter").get_by_role("button", name="Apply").click()` | Pass/Fail |
| G.5 | Click on the first 'Filter' button to open the filter configuration for the selected column. | `page.get_by_title("Filter").first.click()` | Pass/Fail |
| G.6 | Click on the dropdown icon to open the filter condition options. | `page.locator(".ag-icon.ag-icon-small-down").first.click()` | Pass/Fail |
| G.7 | Select the 'Does not contain' option from the filter condition dropdown. | `page.get_by_role("option", name="Does not contain").click()` | Pass/Fail |
| G.8 | Click on the dropdown icon again to open the filter condition options. | `page.locator(".ag-icon.ag-icon-small-down").first.click()` | Pass/Fail |
| G.9 | Select the 'Equals' option from the filter condition dropdown. | `page.get_by_role("option", name="Equals").click()` | Pass/Fail |
| G.10 | Click on the dropdown icon again to open the filter condition options. | `page.locator(".ag-icon.ag-icon-small-down").first.click()` | Pass/Fail |
| G.11 | Select the 'Does not equal' option from the filter condition dropdown. | `page.get_by_role("option", name="Does not equal").click()` | Pass/Fail |
| G.12 | Click on the dropdown icon again to open the filter condition options. | `page.locator(".ag-icon.ag-icon-small-down").first.click()` | Pass/Fail |
| G.13 | Select the 'Begins with' option from the filter condition dropdown. | `page.get_by_role("option", name="Begins with").click()` | Pass/Fail |
| G.14 | Click on the dropdown icon again to open the filter condition options. | `page.locator(".ag-icon.ag-icon-small-down").first.click()` | Pass/Fail |
| G.15 | Select the 'Ends with' option from the filter condition dropdown. | `page.get_by_role("option", name="Ends with").click()` | Pass/Fail |
| G.16 | Click on the dropdown icon again to open the filter condition options. | `page.locator(".ag-icon.ag-icon-small-down").first.click()` | Pass/Fail |
| G.17 | Select the 'Does not contain' option from the filter condition dropdown again. | `page.get_by_role("option", name="Does not contain").click()` | Pass/Fail |
| G.18 | Click on the 'Apply' button to apply the selected filter condition. | `page.get_by_label("Column Filter").get_by_role("button", name="Apply").click()` | Pass/Fail |
| G.19 | Click on the first 'Filter' button to reopen the filter configuration. | `page.get_by_title("Filter").first.click()` | Pass/Fail |
| G.20 | Click on the 'Reset' button to clear the applied filter and reset the filter configuration. | `page.get_by_role("button", name="Reset").click()` | Pass/Fail |
```
```
| | --- PAGINATION INTERACTION --- | | --- |
| H.1 | Click on the first pagination link to navigate to the first page of the table. | `page.locator("a").first.click()` | Pass/Fail |
| H.2 | Click on the second pagination link to navigate to the second page of the table. | `page.locator("a").nth(1).click()` | Pass/Fail |
| H.3 | Click on the 'Next' button to navigate to the next page in the pagination. | `page.locator(".pagination-next > .zeb-chevron-right").first.click()` | Pass/Fail |
| H.4 | Click on the 'Previous' button to navigate to the previous page in the pagination. | `page.locator(".zeb-chevron-left").first.click()` | Pass/Fail |
| H.5 | Click on the 'First' button to navigate to the first page in the pagination. | `page.locator(".zeb-nav-to-first").first.click()` | Pass/Fail |
| H.6 | Click on the dropdown to open the row view options. | `page.locator(".d-flex > esp-multiselect-dropdown > .multiselect-dropdown > div > .w-100 > .d-flex.align-items-center > .dropdown-caret").first.click()` | Pass/Fail |
| H.7 | Select the option to view 20 rows per page. | `page.locator("div").filter(has_text=re.compile(r"^View 20 row\\(s\\)$")).first.click()` | Pass/Fail |
| H.8 | Click on the dropdown again to open the row view options. | `page.locator(".d-flex > esp-multiselect-dropdown > .multiselect-dropdown > div > .w-100 > .d-flex.align-items-center > .dropdown-caret").first.click()` | Pass/Fail |
| H.9 | Select the option to view 50 rows per page. | `page.locator("div").filter(has_text=re.compile(r"^View 50 row\\(s\\)$")).first.click()` | Pass/Fail |
| H.10 | Click on the dropdown again to open the row view options. | `page.locator(".d-flex > esp-multiselect-dropdown > .multiselect-dropdown > div > .w-100 > .d-flex.align-items-center > .dropdown-caret").first.click()` | Pass/Fail |
| H.11 | Select the option to view 10 rows per page. | `page.locator("div").filter(has_text=re.compile(r"^View 10 row\\(s\\)$")).nth(1).click()` | Pass/Fail |
```
```
| | --- DETAILED ROW INTERACTION --- | | --- |
| I.1 | Click on the text displaying the current row count and total rows to view detailed information. | `page.get_by_text("Locations 20 rows out of 968").click()` | Pass/Fail |
| I.2 | Click on the collapsed chevron to expand the detailed view. | `page.locator(".pointer.chevron.zeb-chevron-right.m-r-12.collapsed").click()` | Pass/Fail |
| I.3 | Click on the 'Locations' text to navigate to the Locations section. | `page.get_by_text("Locations", exact=True).click()` | Pass/Fail |
| I.4 | Uncheck the checkbox in the row named 'Location'. | `page.get_by_role("row", name="Location").get_by_role("checkbox").uncheck()` | Pass/Fail |
| I.5 | Click on the 'Columns' button to open the column visibility options. | `page.get_by_role("button", name="columns").nth(1).click()` | Pass/Fail |
| I.6 | Uncheck the 'Toggle All Columns Visibility' checkbox. | `page.get_by_role("checkbox", name="Toggle All Columns Visibility").uncheck()` | Pass/Fail |
| I.7 | Check the 'Store Count Column' checkbox to make it visible. | `page.get_by_role("treeitem", name="Store Count Column").get_by_label("Press SPACE to toggle").check()` | Pass/Fail |
| I.8 | Check the 'Product Count Column' checkbox to make it visible. | `page.get_by_role("treeitem", name="Product Count Column").get_by_label("Press SPACE to toggle").check()` | Pass/Fail |
| I.9 | Check the '13W-Fcst Column' checkbox to make it visible. | `page.get_by_role("treeitem", name="13W-Fcst Column").get_by_label("Press SPACE to toggle").check()` | Pass/Fail |
| I.10 | Click on the 'Filter Columns Input' textbox to activate it. | `page.get_by_role("textbox", name="Filter Columns Input").click()` | Pass/Fail |
| I.11 | Fill the 'Filter Columns Input' textbox with the text 'Pre'. | `page.get_by_role("textbox", name="Filter Columns Input").fill("Pre")` | Pass/Fail |
| I.12 | Check the checkbox labeled 'Press SPACE to toggle' to apply the filter. | `page.get_by_role("checkbox", name="Press SPACE to toggle").check()` | Pass/Fail |
| I.13 | Click on the 'Columns' button again to close the column visibility options. | `page.get_by_role("button", name="columns").nth(1).click()` | Pass/Fail |
```
```
| | --- COLUMN MENU FILTERING --- | | --- |
| J.1 | Click on the filter icon in the column menu to open the filter options. | `page.locator("#ag-header-cell-menu-button > .filter-icon").click()` | Pass/Fail |
| J.2 | Click on the 'Filter Value' textbox to activate it. | `page.get_by_role("textbox", name="Filter Value").click()` | Pass/Fail |
| J.3 | Fill the 'Filter Value' textbox with the text 'CHICAGO'. | `page.get_by_role("textbox", name="Filter Value").fill("CHICAGO")` | Pass/Fail |
| J.4 | Click on the 'Apply' button in the column menu to apply the filter. | `page.get_by_label("Column Menu").get_by_role("button", name="Apply").click()` | Pass/Fail |
| J.5 | Check the checkbox in the grid cell labeled '00162-1554 E 55TH ST-CHICAGO-'. | `page.get_by_role("gridcell", name="00162-1554 E 55TH ST-CHICAGO-").get_by_role("checkbox").check()` | Pass/Fail |
| J.6 | Click on the filter icon in the column menu again to reopen the filter options. | `page.locator("#ag-header-cell-menu-button > .filter-icon").click()` | Pass/Fail |
| J.7 | Click on the 'Reset' button in the column menu to clear the filter. | `page.get_by_label("Column Menu").get_by_role("button", name="Reset").click()` | Pass/Fail |
```
```
| | --- ADDITIONAL ROW AND PAGINATION INTERACTION --- | | --- |
| K.1 | Check the checkbox in the row labeled 'Location'. | `page.get_by_role("row", name="Location").get_by_role("checkbox").check()` | Pass/Fail |
| K.2 | Click on the pagination link labeled '2'. | `page.locator("a").filter(has_text="2").nth(1).click()` | Pass/Fail |
| K.3 | Click on the pagination link labeled '3'. | `page.locator("a").filter(has_text="3").nth(1).click()` | Pass/Fail |
| K.4 | Click on the 'Next' button in the pagination controls. | `page.locator("div:nth-child(3) > esp-pagination-v2 > .d-flex.w-100 > .pagination-pager > .pagination-next > .zeb-chevron-right").click()` | Pass/Fail |
| K.5 | Click on the 'Previous' button in the pagination controls. | `page.locator("div:nth-child(3) > esp-pagination-v2 > .d-flex.w-100 > .pagination-pager > .pagination-previous > .zeb-chevron-left").click()` | Pass/Fail |
| K.6 | Click on the 'First' button in the pagination controls. | `page.locator("div:nth-child(3) > esp-pagination-v2 > .d-flex.w-100 > .pagination-pager > .pagination-first > .zeb-nav-to-first").click()` | Pass/Fail |
```
```
| | --- TIME FILTER INTERACTION --- | | --- |
| L.1 | Click on the 'Filter' button to expand the filter options. | `page.get_by_text("Filter").nth(2).click()` | Pass/Fail |
| L.2 | Click on the dropdown for the 'Time' filter to view available time range options. | `page.locator("#time-filterId > .wr-20 > esp-multiselect-dropdown > .multiselect-dropdown > div > .w-100 > .d-flex.align-items-center > .dropdown-caret").click()` | Pass/Fail |
| L.3 | Select the 'Latest 4 Next 4' option from the 'Time' filter dropdown. | `page.locator("div").filter(has_text=re.compile(r"^Latest 4 Next 4$")).nth(1).click()` | Pass/Fail |
| L.4 | Click on the dropdown for the 'Time' filter again to change the selection. | `page.locator("#time-filterId > .wr-20 > esp-multiselect-dropdown > .multiselect-dropdown > div > .w-100 > .d-flex.align-items-center > .dropdown-caret").click()` | Pass/Fail |
| L.5 | Select the 'Latest 4 Next 13' option from the 'Time' filter dropdown. | `page.locator("div").filter(has_text=re.compile(r"^Latest 4 Next 13$")).nth(1).click()` | Pass/Fail |
| L.6 | Click on the dropdown for the 'Time' filter again to change the selection. | `page.locator("#time-filterId > .wr-20 > esp-multiselect-dropdown > .multiselect-dropdown > div > .w-100 > .d-flex.align-items-center > .dropdown-caret").click()` | Pass/Fail |
| L.7 | Select the 'Latest 13 Next 13' option from the 'Time' filter dropdown. | `page.locator("div").filter(has_text=re.compile(r"^Latest 13 Next 13$")).nth(1).click()` | Pass/Fail |
| L.8 | Click on the dropdown for the 'Time' filter again to change the selection. | `page.locator("#time-filterId > .wr-20 > esp-multiselect-dropdown > .multiselect-dropdown > div > .w-100 > .d-flex.align-items-center > .dropdown-caret").click()` | Pass/Fail |
| L.9 | Select the 'Latest 52 Next 52' option from the 'Time' filter dropdown. | `page.locator("div").filter(has_text=re.compile(r"^Latest 52 Next 52$")).first.click()` | Pass/Fail |
| L.10 | Click on the dropdown for the 'Time' filter again to change the selection. | `page.locator("#time-filterId > .wr-20 > esp-multiselect-dropdown > .multiselect-dropdown > div > .w-100 > .d-flex.align-items-center > .dropdown-caret").click()` | Pass/Fail |
| L.11 | Select the 'Latest 104 Next 52' option from the 'Time' filter dropdown. | `page.locator("div").filter(has_text=re.compile(r"^Latest 104 Next 52$")).nth(1).click()` | Pass/Fail |
| L.12 | Click on the dropdown for the 'Time' filter again to reset the selection. | `page.locator("#time-filterId > .wr-20 > esp-multiselect-dropdown > .multiselect-dropdown > div > .w-100 > .d-flex.align-items-center > .dropdown-caret").click()` | Pass/Fail |
| L.13 | Select the 'Latest 4 Next 4' option from the 'Time' filter dropdown to reset the filter. | `page.locator("div").filter(has_text=re.compile(r"^Latest 4 Next 4$")).nth(1).click()` | Pass/Fail |
```
```
| | --- EVENT FILTER INTERACTION --- | | --- |
| M.1 | Click on the dropdown for the 'Event' filter to view available event options. | `page.locator("#event-filterId > .wr-20 > esp-multiselect-dropdown > .multiselect-dropdown > div > .w-100 > .d-flex.align-items-center > .dropdown-caret").click()` | Pass/Fail |
| M.2 | Click on the first element in the list to expand the filter options. | `page.locator(".d-flex.flex-column.justify-content-center").first.click()` | Pass/Fail |
| M.3 | Click on the 'Search' textbox to focus on it. | `page.get_by_role("textbox", name="Search").click()` | Pass/Fail |
| M.4 | Fill the 'Search' textbox with the value 'TLC'. | `page.get_by_role("textbox", name="Search").fill("TLC")` | Pass/Fail |
| M.5 | Click on the close icon to clear the search input. | `page.locator(".icon.d-flex.pointer.zeb-close").click()` | Pass/Fail |
```
```
| | --- AD LOCATION FILTER INTERACTION --- | | --- |
| N.1 | Click on the dropdown caret for the 'Ad Location' filter to expand the options. | `page.locator(".not-allowed > .w-100 > .d-flex.align-items-center > .dropdown-caret").first.click()` | Pass/Fail |
| N.2 | Click on the dropdown caret for the 'Ad Location' filter again to view the options. | `page.locator("#ad-location-filterId > .wr-20 > esp-multiselect-dropdown > .multiselect-dropdown > div > .w-100 > .d-flex.align-items-center > .dropdown-caret").click()` | Pass/Fail |
| N.3 | Click on the first element in the list to expand the filter options. | `page.locator(".d-flex.flex-column.justify-content-center").first.click()` | Pass/Fail |
| N.4 | Click on the first element in the list again to expand the filter options. | `page.locator(".d-flex.flex-column.justify-content-center").first.click()` | Pass/Fail |
| N.5 | Click on the dropdown caret for the 'Ad Location' filter to view the options again. | `page.locator("#ad-location-filterId > .wr-20 > esp-multiselect-dropdown > .multiselect-dropdown > div > .w-100 > .d-flex.align-items-center > .dropdown-caret").click()` | Pass/Fail |
```
```
| | --- SEGMENT FILTER INTERACTION --- | | --- |
| O.1 | Click on the dropdown caret for the 'Segment' filter to expand the options. | `page.locator("#segment-filterId > .wr-20 > esp-multiselect-dropdown > .multiselect-dropdown > div > .w-100 > .d-flex.align-items-center > .dropdown-caret").click()` | Pass/Fail |
| O.2 | Click on the first element in the list to expand the filter options. | `page.locator(".d-flex.flex-column.justify-content-center").first.click()` | Pass/Fail |
| O.3 | Click on the first element in the list again to expand the filter options. | `page.locator(".d-flex.flex-column.justify-content-center").first.click()` | Pass/Fail |
| O.4 | Click on the dropdown caret for the 'Segment' filter to view the options again. | `page.locator("#segment-filterId > .wr-20 > esp-multiselect-dropdown > .multiselect-dropdown > div > .w-100 > .d-flex.align-items-center > .dropdown-caret").click()` | Pass/Fail |
```
```
| | --- VENDOR FILTER INTERACTION --- | | --- |
| P.1 | Click on the dropdown for the 'Vendor' filter to expand the options. | `page.locator("#vendor-filterId > .wr-20 > esp-multiselect-dropdown > .multiselect-dropdown > div > .w-100").click()` | Pass/Fail |
| P.2 | Click on the first element in the list to expand the filter options. | `page.locator(".d-flex.flex-column.justify-content-center").first.click()` | Pass/Fail |
| P.3 | Click on the first option in the 'Vendor' filter dropdown to select it. | `page.locator(".d-flex.dropdown-option.align-items-center.p-v-5.p-l-32 > .d-flex").first.click()` | Pass/Fail |
| P.4 | Click on the second option in the 'Vendor' filter dropdown to select it. | `page.locator(".overflow-auto > div:nth-child(2) > .d-flex").click()` | Pass/Fail |
| P.5 | Click on the first element in the list again to expand the filter options. | `page.locator(".d-flex.flex-column.justify-content-center").first.click()` | Pass/Fail |
| P.6 | Click on the dropdown caret for the 'Vendor' filter again to view the options. | `page.locator("#vendor-filterId > .wr-20 > esp-multiselect-dropdown > .multiselect-dropdown > div > .w-100 > .d-flex.align-items-center > .dropdown-caret").click()` | Pass/Fail |
| P.7 | Click on the 'Apply' button to apply the selected filters. | `page.locator("button").filter(has_text=re.compile(r"^Apply$")).click()` | Pass/Fail |
```
```
| | --- COLUMN VISIBILITY DROPDOWN INTERACTION --- | | --- |
| Q.1 | Click on the dropdown caret to expand the column visibility options. | `page.locator(".ellipses > esp-multiselect-dropdown > .multiselect-dropdown > div > .w-100 > .d-flex.align-items-center > .dropdown-caret").click()` | Pass/Fail |
| Q.2 | Click on the first element in the list to expand the column visibility options. | `page.locator(".d-flex.flex-column.justify-content-center").first.click()` | Pass/Fail |
| Q.3 | Click on the first checkbox to select a column for visibility. | `page.locator(".d-flex.flex-column.justify-content-center.font-size-10.align-items-center.checkbox-v2.m-r-10.zeb-check").first.click()` | Pass/Fail |
| Q.4 | Click on the first checkbox again to deselect the column for visibility. | `page.locator(".d-flex.flex-column.justify-content-center.font-size-10.align-items-center.checkbox-v2.m-r-10.zeb-check").first.click()` | Pass/Fail |
| Q.5 | Click on the first checkbox again to reselect the column for visibility. | `page.locator(".d-flex.flex-column.justify-content-center.font-size-10.align-items-center.checkbox-v2.m-r-10.zeb-check").first.click()` | Pass/Fail |
| Q.6 | Click on the first checkbox again to toggle the column visibility off. | `page.locator(".d-flex.flex-column.justify-content-center.font-size-10.align-items-center.checkbox-v2.m-r-10.zeb-check").first.click()` | Pass/Fail |
| Q.7 | Click on the first element in the list again to collapse the column visibility options. | `page.locator(".d-flex.flex-column.justify-content-center").first.click()` | Pass/Fail |
| Q.8 | Click on the first deselected checkbox to select a column for visibility. | `page.locator(".d-flex.flex-column.justify-content-center.font-size-10.align-items-center.checkbox-v2.m-r-10.deselected").first.click()` | Pass/Fail |
| Q.9 | Click on the first deselected checkbox again to deselect the column for visibility. | `page.locator(".d-flex.flex-column.justify-content-center.font-size-10.align-items-center.checkbox-v2.m-r-10.deselected").first.click()` | Pass/Fail |
| Q.10 | Click on the first deselected checkbox again to reselect the column for visibility. | `page.locator(".d-flex.flex-column.justify-content-center.font-size-10.align-items-center.checkbox-v2.m-r-10.deselected").first.click()` | Pass/Fail |
| Q.11 | Click on the fifth element in the list to select a specific column for visibility. | `page.locator(".overflow-auto > div:nth-child(5)").click()` | Pass/Fail |
| Q.12 | Click on the dropdown caret again to collapse the column visibility options. | `page.locator(".ellipses > esp-multiselect-dropdown > .multiselect-dropdown > div > .w-100 > .d-flex.align-items-center > .dropdown-caret").click()` | Pass/Fail |
```
```
| | --- COLUMN VISIBILITY SETTINGS --- | | --- |
| R.1 | Click on the dropdown caret to expand the column visibility settings. | `page.locator(".wr-20.font-weight-normal > esp-multiselect-dropdown > .multiselect-dropdown > div > .w-100 > .d-flex.align-items-center > .dropdown-caret").click()` | Pass/Fail |
| R.2 | Click on the first element in the list to expand the column visibility options. | `page.locator(".d-flex.flex-column.justify-content-center").first.click()` | Pass/Fail |
| R.3 | Click on the first element in the list again to collapse the column visibility options. | `page.locator(".d-flex.flex-column.justify-content-center").first.click()` | Pass/Fail |
| R.4 | Click on the dropdown caret again to collapse the column visibility settings. | `page.locator(".wr-20.font-weight-normal > esp-multiselect-dropdown > .multiselect-dropdown > div > .w-100 > .d-flex.align-items-center > .dropdown-caret").click()` | Pass/Fail |
| R.5 | Click on the 'Columns' button to open the column visibility settings. | `page.get_by_role("button", name="columns").nth(2).click()` | Pass/Fail |
| R.6 | Uncheck the 'Toggle All Columns Visibility' checkbox to deselect all columns. | `page.get_by_role("checkbox", name="Toggle All Columns Visibility").uncheck()` | Pass/Fail |
| R.7 | Click on the first column in the list to select it for visibility. | `page.locator("#ag-6720 > .ag-column-panel > .ag-column-select > .ag-column-select-list > .ag-virtual-list-viewport > .ag-virtual-list-container > div > .ag-column-select-column").first.click()` | Pass/Fail |
| R.8 | Check the checkbox for the '/11/2026 Column' to make it visible. | `page.get_by_role("treeitem", name="/11/2026 Column").get_by_label("Press SPACE to toggle").check()` | Pass/Fail |
| R.9 | Check the checkbox for the '/18/2026 Column' to make it visible. | `page.get_by_role("treeitem", name="/18/2026 Column").get_by_label("Press SPACE to toggle").check()` | Pass/Fail |
| R.10 | Check the checkbox for the '/25/2026 Column' to make it visible. | `page.get_by_role("treeitem", name="/25/2026 Column").get_by_label("Press SPACE to toggle").check()` | Pass/Fail |
| R.11 | Check the checkbox for the '02/01/2026 Column' to make it visible. | `page.get_by_role("treeitem", name="02/01/2026 Column").get_by_label("Press SPACE to toggle visibility (hidden)").check()` | Pass/Fail |
| R.12 | Check the checkbox for the '/08/2026 Column' to make it visible. | `page.get_by_role("treeitem", name="/08/2026 Column").get_by_label("Press SPACE to toggle visibility (hidden)").check()` | Pass/Fail |
| R.13 | Check the 'Toggle All Columns Visibility' checkbox to select all columns. | `page.get_by_role("checkbox", name="Toggle All Columns Visibility").check()` | Pass/Fail |
| R.14 | Click on the 'Columns' button again to close the column visibility settings. | `page.get_by_role("button", name="columns").nth(2).click()` | Pass/Fail |
```
```
| | --- ADDITIONAL DROPDOWN AND COLUMN INTERACTION --- | | --- |
| S.1 | Click on the dropdown caret to expand the additional dropdown. | `page.locator(".wr-20.font-weight-normal > esp-multiselect-dropdown > .multiselect-dropdown > div > .w-100 > .d-flex.align-items-center > .dropdown-caret").click()` | Pass/Fail |
| S.2 | Click on the first element in the dropdown list to expand options. | `page.locator(".d-flex.flex-column.justify-content-center").first.click()` | Pass/Fail |
| S.3 | Click on the first element in the dropdown list again to collapse options. | `page.locator(".d-flex.flex-column.justify-content-center").first.click()` | Pass/Fail |
| S.4 | Click on the first dropdown option to select it. | `page.locator(".d-flex.dropdown-option.align-items-center.p-v-5.p-l-32 > .d-flex").first.click()` | Pass/Fail |
| S.5 | Click on the first dropdown option again to deselect it. | `page.locator(".d-flex.dropdown-option.align-items-center.p-v-5.p-l-32 > .d-flex").first.click()` | Pass/Fail |
| S.6 | Click on the first dropdown option a third time to reselect it. | `page.locator(".d-flex.dropdown-option.align-items-center.p-v-5.p-l-32 > .d-flex").first.click()` | Pass/Fail |
| S.7 | Click on the fourth element in the dropdown list. | `page.locator(".overflow-auto > div:nth-child(4) > .d-flex").click()` | Pass/Fail |
| S.8 | Click on the fifth element in the dropdown list. | `page.locator("div:nth-child(5) > .d-flex").click()` | Pass/Fail |
| S.9 | Click on the 'Maximum User Forecast' option. | `page.get_by_text("Maximum User Forecast").nth(1).click()` | Pass/Fail |
| S.10 | Click on the 'Average User Forecast' option. | `page.get_by_text("Average User Forecast").nth(1).click()` | Pass/Fail |
| S.11 | Click on the eighth element in the dropdown list. | `page.locator(".overflow-auto > div:nth-child(8)").click()` | Pass/Fail |
| S.12 | Click on the first dropdown option to interact with it. | `page.locator(".d-flex.dropdown-option").first.click()` | Pass/Fail |
| S.13 | Click on the dropdown caret to collapse the additional dropdown. | `page.locator(".wr-20.font-weight-normal > esp-multiselect-dropdown > .multiselect-dropdown > div > .w-100 > .d-flex.align-items-center > .dropdown-caret").click()` | Pass/Fail |
| S.14 | Click on the third span element to interact with it. | `page.locator("div:nth-child(3) > span > .align-middle").click()` | Pass/Fail |
| S.15 | Click on the filter icon in the header cell. | `page.locator(".ag-header-cell.ag-header-parent-hidden.ag-header-cell-sortable.ag-header-background.ag-focus-managed.ag-header-active > .ag-header-cell-comp-wrapper > .ag-cell-label-container > .ag-header-icon > .filter-icon").click()` | Pass/Fail |
| S.16 | Click on the 'Apply' button in the column filter. | `page.get_by_label("Column Filter").get_by_role("button", name="Apply").click()` | Pass/Fail |
| S.17 | Click on the 'Columns' button to open the column visibility settings. | `page.get_by_role("button", name="columns").nth(3).click()` | Pass/Fail |
| S.18 | Uncheck the 'Toggle All Columns Visibility' checkbox to deselect all columns. | `page.get_by_role("checkbox", name="Toggle All Columns Visibility").uncheck()` | Pass/Fail |
| S.19 | Check the checkbox for the 'Start Week Column' to make it visible. | `page.get_by_role("treeitem", name="Start Week Column").get_by_label("Press SPACE to toggle").check()` | Pass/Fail |
| S.20 | Check the checkbox for the 'End Week Column' to make it visible. | `page.get_by_role("treeitem", name="End Week Column").get_by_label("Press SPACE to toggle").check()` | Pass/Fail |
| S.21 | Check the checkbox for the 'Clone Column' to make it visible. | `page.get_by_role("treeitem", name="Clone Column").get_by_label("Press SPACE to toggle").check()` | Pass/Fail |
| S.22 | Check the checkbox for the 'Event Column' to make it visible. | `page.get_by_role("treeitem", name="Event Column").get_by_label("Press SPACE to toggle visibility (hidden)").check()` | Pass/Fail |
| S.23 | Check the checkbox for the 'Market Column' to make it visible. | `page.get_by_role("treeitem", name="Market Column").get_by_label("Press SPACE to toggle visibility (hidden)").check()` | Pass/Fail |
| S.24 | Check the checkbox for the 'Count of Stores Column' to make it visible. | `page.get_by_role("treeitem", name="Count of Stores Column").get_by_label("Press SPACE to toggle visibility (hidden)").check()` | Pass/Fail |
| S.25 | Check the checkbox for the 'Spot Column' to make it visible. | `page.get_by_role("treeitem", name="Spot Column").get_by_label("Press SPACE to toggle visibility (hidden)").check()` | Pass/Fail |
| S.26 | Check the 'Toggle All Columns Visibility' checkbox to select all columns. | `page.get_by_role("checkbox", name="Toggle All Columns Visibility").check()` | Pass/Fail |
| S.27 | Click on the 'Columns' button again to close the column visibility settings. | `page.get_by_role("button", name="columns").nth(3).click()` | Pass/Fail |
| S.28 | Click on the pagination link for page 2. | `page.locator("a").filter(has_text="2").nth(2).click()` | Pass/Fail |
| S.29 | Click on the pagination link for page 3. | `page.locator("a").filter(has_text="3").nth(2).click()` | Pass/Fail |
| S.30 | Click on the 'First Page' button in the pagination controls. | `page.locator("div:nth-child(7) > div > .componentParentWrapper > esp-grid-container > esp-card-component > .card-container > .card-content > esp-row-dimentional-grid > div > #paginationId > esp-pagination-v2 > .d-flex.w-100 > .pagination-pager > .pagination-first").click()` | Pass/Fail |
```
