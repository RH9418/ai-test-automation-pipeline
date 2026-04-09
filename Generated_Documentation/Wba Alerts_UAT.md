# Feature: Wba Alerts
**Tab Location:** Main Workspace

## Detailed User Interaction Flows

| Use Case ID | Test Case Description | Exact Locator | Pass/Fail | Notes | Issues |
|:---|:---|:---|:---|:---|:---|
```
| | **--- NAVIGATION TO DASHBOARD ---** | | | | |
| D.1 | Open the Executive Dashboard page by navigating to the specified URL. | `page.goto("https://stage.wba.esp.antuit.ai/dp/demand-planning/executive-dashboard?workbookId=6&tabIndex=1")` | | | |
```
```
| | **--- ALERTS FILTER INTERACTION ---** | | | | |
| E.1 | Click on the 'Alerts' filter dropdown to expand the filter options. | `page.locator("#alerts-filterId").click()` | | | |
| E.2 | From the dropdown list, select the 'MAPE' option to apply the filter. | `page.locator("div").filter(has_text=re.compile(r"^MAPE$")).nth(1).click()` | | | |
| E.3 | Click on the dropdown caret to open the filter options again. | `page.locator(".w-100.p-h-16.p-v-8.dropdown-label.background-white > .d-flex.align-items-center > .dropdown-caret").click()` | | | |
| E.4 | From the dropdown list, select the 'Under Bias' option to apply the filter. | `page.locator("div").filter(has_text=re.compile(r"^Under Bias$")).nth(1).click()` | | | |
| E.5 | Click on the dropdown caret to open the filter options again. | `page.locator(".w-100.p-h-16.p-v-8.dropdown-label.background-white > .d-flex.align-items-center > .dropdown-caret").click()` | | | |
| E.6 | From the dropdown list, select the 'Over Bias' option to apply the filter. | `page.locator("div").filter(has_text=re.compile(r"^Over Bias$")).nth(1).click()` | | | |
| E.7 | Click on the dropdown caret to open the filter options again. | `page.locator(".w-100.p-h-16.p-v-8.dropdown-label.background-white > .d-flex.align-items-center > .dropdown-caret").click()` | | | |
| E.8 | From the dropdown list, select the 'PVA' option to apply the filter. | `page.locator("div").filter(has_text=re.compile(r"^PVA$")).nth(1).click()` | | | |
| E.9 | Click on the dropdown caret to open the filter options again. | `page.locator(".w-100.p-h-16.p-v-8.dropdown-label.background-white > .d-flex.align-items-center > .dropdown-caret").click()` | | | |
| E.10 | From the dropdown list, select the 'SSIS' option to apply the filter. | `page.locator("div").filter(has_text=re.compile(r"^SSIS$")).first.click()` | | | |
```
```
| | **--- COLUMN VISIBILITY CONFIGURATION ---** | | | | |
| F.1 | Click on the 'Columns' button to open the column visibility configuration panel. | `page.get_by_role("button", name="columns").click()` | | | |
| F.2 | Uncheck the 'Toggle All Columns Visibility' checkbox to hide all columns initially. | `page.get_by_role("checkbox", name="Toggle All Columns Visibility").uncheck()` | | | |
| F.3 | Check the 'Store Count Column' checkbox to make the 'Store Count' column visible. | `page.get_by_role("treeitem", name="Store Count Column").get_by_label("Press SPACE to toggle").check()` | | | |
| F.4 | Check the 'Product Count Column' checkbox to make the 'Product Count' column visible. | `page.get_by_role("treeitem", name="Product Count Column").get_by_label("Press SPACE to toggle").check()` | | | |
| F.5 | Check the 'Stability Column' checkbox to make the 'Stability' column visible. | `page.get_by_role("treeitem", name="Stability Column").get_by_label("Press SPACE to toggle").check()` | | | |
| F.6 | Check the 'SSIS Column' checkbox to make the 'SSIS' column visible. | `page.get_by_role("treeitem", name="SSIS Column").get_by_label("Press SPACE to toggle").check()` | | | |
| F.7 | Check the 'User Bias Column' checkbox to make the 'User Bias' column visible. | `page.get_by_role("treeitem", name="User Bias Column").get_by_label("Press SPACE to toggle").check()` | | | |
| F.8 | Check the 'System Bias Column' checkbox to make the 'System Bias' column visible. | `page.get_by_role("treeitem", name="System Bias Column").get_by_label("Press SPACE to toggle").check()` | | | |
| F.9 | Check the 'User MAPE Column' checkbox to make the 'User MAPE' column visible. | `page.get_by_role("treeitem", name="User MAPE Column").get_by_label("Press SPACE to toggle visibility (hidden)").check()` | | | |
| F.10 | Check the 'System MAPE Column' checkbox to make the 'System MAPE' column visible. | `page.get_by_role("treeitem", name="System MAPE Column").get_by_label("Press SPACE to toggle visibility (hidden)").check()` | | | |
| F.11 | Check the 'Planner Value Add Column' checkbox to make the 'Planner Value Add' column visible. | `page.get_by_role("treeitem", name="Planner Value Add Column").get_by_label("Press SPACE to toggle visibility (hidden)").check()` | | | |
| F.12 | Check the '13W-Fcst Column' checkbox to make the '13W-Fcst' column visible. | `page.get_by_role("treeitem", name="13W-Fcst Column").get_by_label("Press SPACE to toggle visibility (hidden)").check()` | | | |
```
```
| | **--- COLUMN FILTERING ---** | | | | |
| G.1 | Click on the column selector element to open the column selection panel. | `page.locator("div:nth-child(11) > .ag-column-select-column").click()` | | | |
| G.2 | Click on the 'Filter Columns Input' textbox to focus on it for entering a filter value. | `page.get_by_role("textbox", name="Filter Columns Input").click()` | | | |
| G.3 | Fill the 'Filter Columns Input' textbox with the value 'Store Count' to filter the columns. | `page.get_by_role("textbox", name="Filter Columns Input").fill("Store Count")` | | | |
| G.4 | Press 'Enter' to apply the filter and display the filtered column options. | `page.get_by_role("textbox", name="Filter Columns Input").press("Enter")` | | | |
| G.5 | Check the checkbox for the filtered column to make it visible. | `page.get_by_role("checkbox", name="Press SPACE to toggle").check()` | | | |
| G.6 | Click on the 'Columns' button to close the column selection panel. | `page.get_by_role("button", name="columns").click()` | | | |
```
```markdown
| | **--- ROW SELECTION AND FILTERING ---** | | | | |
| H.1 | Select the radio button for the row with the name '002-SPIRITS' to apply row selection. | `page.get_by_role("row", name=" 002-SPIRITS").get_by_role("radio").check()` | | | |
| H.2 | Click on the first 'Filter' button to open the filter configuration for the selected column. | `page.get_by_title("Filter").first.click()` | | | |
| H.3 | Fill the 'Filter Value' textbox with '002-SPIRITS' to filter rows based on this value. | `page.get_by_role("textbox", name="Filter Value").fill("002-SPIRITS")` | | | |
| H.4 | Click on the 'Apply' button to apply the column filter and update the displayed rows. | `page.get_by_label("Column Filter").get_by_role("button", name="Apply").click()` | | | |
| H.5 | Click on the first 'Filter' button to open the filter configuration for the selected column. | `page.get_by_title("Filter").first.click()` | | | |
| H.6 | Click on the dropdown icon to open the filter condition options. | `page.locator(".ag-icon.ag-icon-small-down").first.click()` | | | |
| H.7 | Select the 'Does not contain' option from the filter condition dropdown. | `page.get_by_role("option", name="Does not contain").click()` | | | |
| H.8 | Click on the dropdown icon again to open the filter condition options. | `page.locator(".ag-icon.ag-icon-small-down").first.click()` | | | |
| H.9 | Select the 'Equals' option from the filter condition dropdown. | `page.get_by_role("option", name="Equals").click()` | | | |
| H.10 | Click on the dropdown icon again to open the filter condition options. | `page.locator(".ag-icon.ag-icon-small-down").first.click()` | | | |
| H.11 | Select the 'Does not equal' option from the filter condition dropdown. | `page.get_by_role("option", name="Does not equal").click()` | | | |
| H.12 | Click on the dropdown icon again to open the filter condition options. | `page.locator(".ag-icon.ag-icon-small-down").first.click()` | | | |
| H.13 | Select the 'Begins with' option from the filter condition dropdown. | `page.get_by_role("option", name="Begins with").click()` | | | |
| H.14 | Click on the dropdown icon again to open the filter condition options. | `page.locator(".ag-icon.ag-icon-small-down").first.click()` | | | |
| H.15 | Select the 'Ends with' option from the filter condition dropdown. | `page.get_by_role("option", name="Ends with").click()` | | | |
| H.16 | Click on the dropdown icon again to open the filter condition options. | `page.locator(".ag-icon.ag-icon-small-down").first.click()` | | | |
| H.17 | Select the 'Does not contain' option from the filter condition dropdown again. | `page.get_by_role("option", name="Does not contain").click()` | | | |
| H.18 | Click on the 'Apply' button to apply the selected filter condition. | `page.get_by_label("Column Filter").get_by_role("button", name="Apply").click()` | | | |
| H.19 | Click on the first 'Filter' button to reopen the filter configuration. | `page.get_by_title("Filter").first.click()` | | | |
| H.20 | Click on the 'Reset' button to clear the applied filter and reset the filter configuration. | `page.get_by_role("button", name="Reset").click()` | | | |
```
```markdown
| | **--- PAGINATION INTERACTION ---** | | | | |
| I.1 | Click on the first pagination link to navigate to the first page of the table. | `page.locator("a").first.click()` | | | |
| I.2 | Click on the second pagination link to navigate to the second page of the table. | `page.locator("a").nth(1).click()` | | | |
| I.3 | Click on the 'Next' button to navigate to the next page in the pagination. | `page.locator(".pagination-next > .zeb-chevron-right").first.click()` | | | |
| I.4 | Click on the 'Previous' button to navigate to the previous page in the pagination. | `page.locator(".zeb-chevron-left").first.click()` | | | |
| I.5 | Click on the 'First' button to navigate to the first page in the pagination. | `page.locator(".zeb-nav-to-first").first.click()` | | | |
```
```markdown
| | **--- ROW VIEW OPTIONS ---** | | | | |
| J.1 | Click on the dropdown to open the row view options. | `page.locator(".d-flex > esp-multiselect-dropdown > .multiselect-dropdown > div > .w-100 > .d-flex.align-items-center > .dropdown-caret").first.click()` | | | |
| J.2 | Select the option to view 20 rows per page from the dropdown menu. | `page.locator("div").filter(has_text=re.compile(r"^View 20 row\(s\)$")).first.click()` | | | |
| J.3 | Click on the dropdown again to open the row view options. | `page.locator(".d-flex > esp-multiselect-dropdown > .multiselect-dropdown > div > .w-100 > .d-flex.align-items-center > .dropdown-caret").first.click()` | | | |
| J.4 | Select the option to view 50 rows per page from the dropdown menu. | `page.locator("div").filter(has_text=re.compile(r"^View 50 row\(s\)$")).first.click()` | | | |
| J.5 | Click on the dropdown again to open the row view options. | `page.locator(".d-flex > esp-multiselect-dropdown > .multiselect-dropdown > div > .w-100 > .d-flex.align-items-center > .dropdown-caret").first.click()` | | | |
| J.6 | Select the option to view 10 rows per page from the dropdown menu. | `page.locator("div").filter(has_text=re.compile(r"^View 10 row\(s\)$")).nth(1).click()` | | | |
| J.7 | Click on the text displaying the current row count and total rows to view detailed information. | `page.get_by_text("Locations 20 rows out of 968").click()` | | | |
```
```markdown
| | **--- LOCATION AND COLUMN VISIBILITY ---** | | | | |
| K.1 | Click on the right-facing chevron icon to expand the collapsed section. | `page.locator(".pointer.chevron.zeb-chevron-right.m-r-12.collapsed").click()` | | | |
| K.2 | Click on the "Locations" tab to navigate to the Locations section. | `page.get_by_text("Locations", exact=True).click()` | | | |
| K.3 | Uncheck the checkbox in the row labeled "Location" to deselect it. | `page.get_by_role("row", name="Location").get_by_role("checkbox").uncheck()` | | | |
| K.4 | Click on the "Columns" button to open the column visibility options. | `page.get_by_role("button", name="columns").nth(1).click()` | | | |
| K.5 | Uncheck the "Toggle All Columns Visibility" checkbox to hide all columns. | `page.get_by_role("checkbox", name="Toggle All Columns Visibility").uncheck()` | | | |
| K.6 | Check the "Store Count Column" checkbox to make the Store Count column visible. | `page.get_by_role("treeitem", name="Store Count Column").get_by_label("Press SPACE to toggle").check()` | | | |
| K.7 | Check the "Product Count Column" checkbox to make the Product Count column visible. | `page.get_by_role("treeitem", name="Product Count Column").get_by_label("Press SPACE to toggle").check()` | | | |
| K.8 | Check the "13W-Fcst Column" checkbox to make the 13W-Fcst column visible. | `page.get_by_role("treeitem", name="13W-Fcst Column").get_by_label("Press SPACE to toggle").check()` | | | |
| K.9 | Click on the "Filter Columns Input" textbox to activate it for typing. | `page.get_by_role("textbox", name="Filter Columns Input").click()` | | | |
| K.10 | Type "Pre" into the "Filter Columns Input" textbox to filter the column list. | `page.get_by_role("textbox", name="Filter Columns Input").fill("Pre")` | | | |
| K.11 | Check the filtered checkbox labeled "Press SPACE to toggle" to make the column visible. | `page.get_by_role("checkbox", name="Press SPACE to toggle").check()` | | | |
| K.12 | Click on the "Columns" button again to close the column visibility options. | `page.get_by_role("button", name="columns").nth(1).click()` | | | |
```
```markdown
| | **--- COLUMN MENU FILTERING ---** | | | | |
| L.1 | Click on the filter icon located in the column header to open the column menu. | `page.locator("#ag-header-cell-menu-button > .filter-icon").click()` | | | |
| L.2 | Click on the "Filter Value" textbox to activate it for typing. | `page.get_by_role("textbox", name="Filter Value").click()` | | | |
| L.3 | Type "CHICAGO" into the "Filter Value" textbox to filter the rows. | `page.get_by_role("textbox", name="Filter Value").fill("CHICAGO")` | | | |
| L.4 | Click on the "Apply" button in the column menu to apply the filter. | `page.get_by_label("Column Menu").get_by_role("button", name="Apply").click()` | | | |
| L.5 | Check the checkbox in the grid cell labeled "00162-1554 E 55TH ST-CHICAGO-" to select the row. | `page.get_by_role("gridcell", name="00162-1554 E 55TH ST-CHICAGO-").get_by_role("checkbox").check()` | | | |
| L.6 | Click on the filter icon in the column header again to reopen the column menu. | `page.locator("#ag-header-cell-menu-button > .filter-icon").click()` | | | |
| L.7 | Click on the "Reset" button in the column menu to clear the applied filter. | `page.get_by_label("Column Menu").get_by_role("button", name="Reset").click()` | | | |
```
```markdown
| | **--- PAGINATION NAVIGATION ---** | | | | |
| M.1 | Select the checkbox in the row labeled "Location" to mark it for pagination testing. | `page.get_by_role("row", name="Location").get_by_role("checkbox").check()` | | | |
| M.2 | Click on the page number "2" link to navigate to the second page of results. | `page.locator("a").filter(has_text="2").nth(1).click()` | | | |
| M.3 | Click on the page number "3" link to navigate to the third page of results. | `page.locator("a").filter(has_text="3").nth(1).click()` | | | |
| M.4 | Click on the "Next" button (right arrow) to move to the next page of results. | `page.locator("div:nth-child(3) > esp-pagination-v2 > .d-flex.w-100 > .pagination-pager > .pagination-next > .zeb-chevron-right").click()` | | | |
| M.5 | Click on the "Previous" button (left arrow) to return to the previous page of results. | `page.locator("div:nth-child(3) > esp-pagination-v2 > .d-flex.w-100 > .pagination-pager > .pagination-previous > .zeb-chevron-left").click()` | | | |
| M.6 | Click on the "First" button to navigate back to the first page of results. | `page.locator("div:nth-child(3) > esp-pagination-v2 > .d-flex.w-100 > .pagination-pager > .pagination-first > .zeb-nav-to-first").click()` | | | |
```
```markdown
| | **--- TIME FILTER INTERACTION ---** | | | | |
| N.1 | Click on the 'Filter' button to expand the filter options. | `page.get_by_text("Filter").nth(2).click()` | | | |
| N.2 | Click on the dropdown for the 'Time' filter to view available time range options. | `page.locator("#time-filterId > .wr-20 > esp-multiselect-dropdown > .multiselect-dropdown > div > .w-100 > .d-flex.align-items-center > .dropdown-caret").click()` | | | |
| N.3 | Select the 'Latest 4 Next 4' option from the 'Time' filter dropdown. | `page.locator("div").filter(has_text=re.compile(r"^Latest 4 Next 4$")).nth(1).click()` | | | |
| N.4 | Click on the dropdown for the 'Time' filter again to change the selection. | `page.locator("#time-filterId > .wr-20 > esp-multiselect-dropdown > .multiselect-dropdown > div > .w-100 > .d-flex.align-items-center > .dropdown-caret").click()` | | | |
| N.5 | Select the 'Latest 4 Next 13' option from the 'Time' filter dropdown. | `page.locator("div").filter(has_text=re.compile(r"^Latest 4 Next 13$")).nth(1).click()` | | | |
| N.6 | Click on the dropdown for the 'Time' filter again to change the selection. | `page.locator("#time-filterId > .wr-20 > esp-multiselect-dropdown > .multiselect-dropdown > div > .w-100 > .d-flex.align-items-center > .dropdown-caret").click()` | | | |
| N.7 | Select the 'Latest 13 Next 13' option from the 'Time' filter dropdown. | `page.locator("div").filter(has_text=re.compile(r"^Latest 13 Next 13$")).nth(1).click()` | | | |
| N.8 | Click on the dropdown for the 'Time' filter again to change the selection. | `page.locator("#time-filterId > .wr-20 > esp-multiselect-dropdown > .multiselect-dropdown > div > .w-100 > .d-flex.align-items-center > .dropdown-caret").click()` | | | |
| N.9 | Select the 'Latest 52 Next 52' option from the 'Time' filter dropdown. | `page.locator("div").filter(has_text=re.compile(r"^Latest 52 Next 52$")).first.click()` | | | |
| N.10 | Click on the dropdown for the 'Time' filter again to change the selection. | `page.locator("#time-filterId > .wr-20 > esp-multiselect-dropdown > .multiselect-dropdown > div > .w-100 > .d-flex.align-items-center > .dropdown-caret").click()` | | | |
| N.11 | Select the 'Latest 104 Next 52' option from the 'Time' filter dropdown. | `page.locator("div").filter(has_text=re.compile(r"^Latest 104 Next 52$")).nth(1).click()` | | | |
| N.12 | Click on the dropdown for the 'Time' filter again to reset the selection. | `page.locator("#time-filterId > .wr-20 > esp-multiselect-dropdown > .multiselect-dropdown > div > .w-100 > .d-flex.align-items-center > .dropdown-caret").click()` | | | |
| N.13 | Select the 'Latest 4 Next 4' option from the 'Time' filter dropdown to reset the filter. | `page.locator("div").filter(has_text=re.compile(r"^Latest 4 Next 4$")).nth(1).click()` | | | |
```
```markdown
| | **--- EVENT FILTER INTERACTION ---** | | | | |
| O.1 | Click on the dropdown for the 'Event' filter to view available event options. | `page.locator("#event-filterId > .wr-20 > esp-multiselect-dropdown > .multiselect-dropdown > div > .w-100 > .d-flex.align-items-center > .dropdown-caret").click()` | | | |
| O.2 | Click on the first element in the list to expand the filter options. | `page.locator(".d-flex.flex-column.justify-content-center").first.click()` | | | |
| O.3 | Click on the 'Search' textbox to focus on it. | `page.get_by_role("textbox", name="Search").click()` | | | |
| O.4 | Fill the 'Search' textbox with the value 'TLC'. | `page.get_by_role("textbox", name="Search").fill("TLC")` | | | |
| O.5 | Click on the close icon to clear the search input. | `page.locator(".icon.d-flex.pointer.zeb-close").click()` | | | |
```
```markdown
| | **--- AD LOCATION FILTER INTERACTION ---** | | | | |
| P.1 | Click on the dropdown caret for the 'Ad Location' filter to expand the options. | `page.locator(".not-allowed > .w-100 > .d-flex.align-items-center > .dropdown-caret").first.click()` | | | |
| P.2 | Click on the dropdown caret for the 'Ad Location' filter again to view the options. | `page.locator("#ad-location-filterId > .wr-20 > esp-multiselect-dropdown > .multiselect-dropdown > div > .w-100 > .d-flex.align-items-center > .dropdown-caret").click()` | | | |
| P.3 | Click on the first element in the list to expand the filter options. | `page.locator(".d-flex.flex-column.justify-content-center").first.click()` | | | |
| P.4 | Click on the first element in the list again to confirm the selection. | `page.locator(".d-flex.flex-column.justify-content-center").first.click()` | | | |
| P.5 | Click on the dropdown caret for the 'Ad Location' filter to collapse the options. | `page.locator("#ad-location-filterId > .wr-20 > esp-multiselect-dropdown > .multiselect-dropdown > div > .w-100 > .d-flex.align-items-center > .dropdown-caret").click()` | | | |
```
```markdown
| | **--- SEGMENT FILTER INTERACTION ---** | | | | |
| Q.1 | Click on the dropdown caret for the 'Segment' filter to expand the options. | `page.locator("#segment-filterId > .wr-20 > esp-multiselect-dropdown > .multiselect-dropdown > div > .w-100 > .d-flex.align-items-center > .dropdown-caret").click()` | | | |
| Q.2 | Click on the first element in the list to expand the filter options. | `page.locator(".d-flex.flex-column.justify-content-center").first.click()` | | | |
| Q.3 | Click on the first element in the list again to confirm the selection. | `page.locator(".d-flex.flex-column.justify-content-center").first.click()` | | | |
| Q.4 | Click on the dropdown caret for the 'Segment' filter to collapse the options. | `page.locator("#segment-filterId > .wr-20 > esp-multiselect-dropdown > .multiselect-dropdown > div > .w-100 > .d-flex.align-items-center > .dropdown-caret").click()` | | | |
```
```markdown
| | **--- VENDOR FILTER INTERACTION ---** | | | | |
| R.1 | Click on the dropdown for the 'Vendor' filter to expand the options. | `page.locator("#vendor-filterId > .wr-20 > esp-multiselect-dropdown > .multiselect-dropdown > div > .w-100").click()` | | | |
| R.2 | Click on the first element in the list to expand the filter options. | `page.locator(".d-flex.flex-column.justify-content-center").first.click()` | | | |
| R.3 | Click on the first option in the 'Vendor' filter dropdown to select it. | `page.locator(".d-flex.dropdown-option.align-items-center.p-v-5.p-l-32 > .d-flex").first.click()` | | | |
| R.4 | Click on the second option in the 'Vendor' filter dropdown to select it. | `page.locator(".overflow-auto > div:nth-child(2) > .d-flex").click()` | | | |
| R.5 | Click on the first element in the list again to confirm the selection. | `page.locator(".d-flex.flex-column.justify-content-center").first.click()` | | | |
| R.6 | Click on the dropdown caret for the 'Vendor' filter again to view the options. | `page.locator("#vendor-filterId > .wr-20 > esp-multiselect-dropdown > .multiselect-dropdown > div > .w-100 > .d-flex.align-items-center > .dropdown-caret").click()` | | | |
| R.7 | Click on the 'Apply' button to apply the selected filters. | `page.locator("button").filter(has_text=re.compile(r"^Apply$")).click()` | | | |
```
```markdown
| | **--- COLUMN VISIBILITY OPTIONS ---** | | | | |
| S.1 | Click on the dropdown caret to expand the column visibility options. | `page.locator(".ellipses > esp-multiselect-dropdown > .multiselect-dropdown > div > .w-100 > .d-flex.align-items-center > .dropdown-caret").click()` | | | |
| S.2 | Click on the first element in the list to expand the filter options. | `page.locator(".d-flex.flex-column.justify-content-center").first.click()` | | | |
| S.3 | Select the first checkbox to make the corresponding column visible. | `page.locator(".d-flex.flex-column.justify-content-center.font-size-10.align-items-center.checkbox-v2.m-r-10.zeb-check").first.click()` | | | |
| S.4 | Select the second checkbox to make the corresponding column visible. | `page.locator(".d-flex.flex-column.justify-content-center.font-size-10.align-items-center.checkbox-v2.m-r-10.zeb-check").first.click()` | | | |
| S.5 | Select the third checkbox to make the corresponding column visible. | `page.locator(".d-flex.flex-column.justify-content-center.font-size-10.align-items-center.checkbox-v2.m-r-10.zeb-check").first.click()` | | | |
| S.6 | Select the fourth checkbox to make the corresponding column visible. | `page.locator(".d-flex.flex-column.justify-content-center.font-size-10.align-items-center.checkbox-v2.m-r-10.zeb-check").first.click()` | | | |
| S.7 | Click on the first element in the list again to confirm the selection. | `page.locator(".d-flex.flex-column.justify-content-center").first.click()` | | | |
| S.8 | Deselect the first checkbox to hide the corresponding column. | `page.locator(".d-flex.flex-column.justify-content-center.font-size-10.align-items-center.checkbox-v2.m-r-10.deselected").first.click()` | | | |
| S.9 | Deselect the second checkbox to hide the corresponding column. | `page.locator(".d-flex.flex-column.justify-content-center.font-size-10.align-items-center.checkbox-v2.m-r-10.deselected").first.click()` | | | |
| S.10 | Deselect the third checkbox to hide the corresponding column. | `page.locator(".d-flex.flex-column.justify-content-center.font-size-10.align-items-center.checkbox-v2.m-r-10.deselected").first.click()` | | | |
| S.11 | Click on the fifth element in the list to select a specific column. | `page.locator(".overflow-auto > div:nth-child(5)").click()` | | | |
| S.12 | Click on the dropdown caret again to collapse the column visibility options. | `page.locator(".ellipses > esp-multiselect-dropdown > .multiselect-dropdown > div > .w-100 > .d-flex.align-items-center > .dropdown-caret").click()` | | | |
| S.13 | Click on the dropdown caret for another section to expand its options. | `page.locator(".wr-20.font-weight-normal > esp-multiselect-dropdown > .multiselect-dropdown > div > .w-100 > .d-flex.align-items-center > .dropdown-caret").click()` | | | |
| S.14 | Click on the first element in the list to expand the filter options. | `page.locator(".d-flex.flex-column.justify-content-center").first.click()` | | | |
| S.15 | Click on the first element in the list again to confirm the selection. | `page.locator(".d-flex.flex-column.justify-content-center").first.click()` | | | |
| S.16 | Click on the dropdown caret for another section again to collapse its options. | `page.locator(".wr-20.font-weight-normal > esp-multiselect-dropdown > .multiselect-dropdown > div > .w-100 > .d-flex.align-items-center > .dropdown-caret").click()` | | | |
| S.17 | Click on the 'Columns' button to open the column visibility settings. | `page.get_by_role("button", name="columns").nth(2).click()` | | | |
| S.18 | Uncheck the 'Toggle All Columns Visibility' checkbox to deselect all columns. | `page.get_by_role("checkbox", name="Toggle All Columns Visibility").uncheck()` | | | |
| S.19 | Click on the first column in the list to make it visible. | `page.locator("#ag-6720 > .ag-column-panel > .ag-column-select > .ag-column-select-list > .ag-virtual-list-viewport > .ag-virtual-list-container > div > .ag-column-select-column").first.click()` | | | |
| S.20 | Check the checkbox for the '/11/2026 Column' to make it visible. | `page.get_by_role("treeitem", name="/11/2026 Column").get_by_label("Press SPACE to toggle").check()` | | | |
| S.21 | Check the checkbox for the '/18/2026 Column' to make it visible. | `page.get_by_role("treeitem", name="/18/2026 Column").get_by_label("Press SPACE to toggle").check()` | | | |
| S.22 | Check the checkbox for the '/25/2026 Column' to make it visible. | `page.get_by_role("treeitem", name="/25/2026 Column").get_by_label("Press SPACE to toggle").check()` | | | |
| S.23 | Check the checkbox for the '02/01/2026 Column' to make it visible. | `page.get_by_role("treeitem", name="02/01/2026 Column").get_by_label("Press SPACE to toggle visibility (hidden)").check()` | | | |
| S.24 | Check the checkbox for the '/08/2026 Column' to make it visible. | `page.get_by_role("treeitem", name="/08/2026 Column").get_by_label("Press SPACE to toggle visibility (hidden)").check()` | | | |
| S.25 | Check the 'Toggle All Columns Visibility' checkbox to select all columns. | `page.get_by_role("checkbox", name="Toggle All Columns Visibility").check()` | | | |
| S.26 | Click on the 'Columns' button again to close the column visibility settings. | `page.get_by_role("button", name="columns").nth(2).click()` | | | |
```
```markdown
| | **--- ADDITIONAL COLUMN VISIBILITY SETTINGS ---** | | | | |
| T.1 | Click on the dropdown caret to expand the additional column visibility options. | `page.locator(".wr-20.font-weight-normal > esp-multiselect-dropdown > .multiselect-dropdown > div > .w-100 > .d-flex.align-items-center > .dropdown-caret").click()` | | | |
| T.2 | Click on the first element in the list to expand the filter options. | `page.locator(".d-flex.flex-column.justify-content-center").first.click()` | | | |
| T.3 | Click on the first element in the list again to confirm the selection. | `page.locator(".d-flex.flex-column.justify-content-center").first.click()` | | | |
| T.4 | Click on the first dropdown option to select it. | `page.locator(".d-flex.dropdown-option.align-items-center.p-v-5.p-l-32 > .d-flex").first.click()` | | | |
| T.5 | Click on the first dropdown option again to confirm the selection. | `page.locator(".d-flex.dropdown-option.align-items-center.p-v-5.p-l-32 > .d-flex").first.click()` | | | |
| T.6 | Click on the first dropdown option once more to finalize the selection. | `page.locator(".d-flex.dropdown-option.align-items-center.p-v-5.p-l-32 > .d-flex").first.click()` | | | |
| T.7 | Click on the fourth element in the list to select a specific column. | `page.locator(".overflow-auto > div:nth-child(4) > .d-flex").click()` | | | |
| T.8 | Click on the fifth element in the list to select another specific column. | `page.locator("div:nth-child(5) > .d-flex").click()` | | | |
| T.9 | Click on the "Maximum User Forecast" option to select it. | `page.get_by_text("Maximum User Forecast").nth(1).click()` | | | |
| T.10 | Click on the "Average User Forecast" option to select it. | `page.get_by_text("Average User Forecast").nth(1).click()` | | | |
| T.11 | Click on the eighth element in the list to select another specific column. | `page.locator(".overflow-auto > div:nth-child(8)").click()` | | | |
| T.12 | Click on the first dropdown option to finalize the selection. | `page.locator(".d-flex.dropdown-option").first.click()` | | | |
| T.13 | Click on the dropdown caret again to collapse the additional column visibility options. | `page.locator(".wr-20.font-weight-normal > esp-multiselect-dropdown > .multiselect-dropdown > div > .w-100 > .d-flex.align-items-center > .dropdown-caret").click()` | | | |
| T.14 | Click on the third element in the list to select a specific column. | `page.locator("div:nth-child(3) > span > .align-middle").click()` | | | |
| T.15 | Click on the filter icon in the header to open the filter settings. | `page.locator(".ag-header-cell.ag-header-parent-hidden.ag-header-cell-sortable.ag-header-background.ag-focus-managed.ag-header-active > .ag-header-cell-comp-wrapper > .ag-cell-label-container > .ag-header-icon > .filter-icon").click()` | | | |
| T.16 | Click on the "Apply" button in the filter settings to apply the changes. | `page.get_by_label("Column Filter").get_by_role("button", name="Apply").click()` | | | |
| T.17 | Click on the 'Columns' button to open the column visibility settings. | `page.get_by_role("button", name="columns").nth(3).click()` | | | |
| T.18 | Uncheck the 'Toggle All Columns Visibility' checkbox to deselect all columns. | `page.get_by_role("checkbox", name="Toggle All Columns Visibility").uncheck()` | | | |
| T.19 | Check the checkbox for the 'Start Week Column' to make it visible. | `page.get_by_role("treeitem", name="Start Week Column").get_by_label("Press SPACE to toggle").check()` | | | |
| T.20 | Check the checkbox for the 'End Week Column' to make it visible. | `page.get_by_role("treeitem", name="End Week Column").get_by_label("Press SPACE to toggle").check()` | | | |
| T.21 | Check the checkbox for the 'Clone Column' to make it visible. | `page.get_by_role("treeitem", name="Clone Column").get_by_label("Press SPACE to toggle").check()` | | | |
| T.22 | Check the checkbox for the 'Event Column' to make it visible. | `page.get_by_role("treeitem", name="Event Column").get_by_label("Press SPACE to toggle visibility (hidden)").check()` | | | |
| T.23 | Check the checkbox for the 'Market Column' to make it visible. | `page.get_by_role("treeitem", name="Market Column").get_by_label("Press SPACE to toggle visibility (hidden)").check()` | | | |
| T.24 | Check the checkbox for the 'Count of Stores Column' to make it visible. | `page.get_by_role("treeitem", name="Count of Stores Column").get_by_label("Press SPACE to toggle visibility (hidden)").check()` | | | |
| T.25 | Check the checkbox for the 'Spot Column' to make it visible. | `page.get_by_role("treeitem", name="Spot Column").get_by_label("Press SPACE to toggle visibility (hidden)").check()` | | | |
| T.26 | Check the 'Toggle All Columns Visibility' checkbox to select all columns. | `page.get_by_role("checkbox", name="Toggle All Columns Visibility").check()` | | | |
| T.27 | Click on the 'Columns' button again to close the column visibility settings. | `page.get_by_role("button", name="columns").nth(3).click()` | | | |
```
```markdown
| | **--- FINAL PAGINATION NAVIGATION ---** | | | | |
| U.1 | Click on the page number "2" link to navigate to the second page of the results. | `page.locator("a").filter(has_text="2").nth(2).click()` | | | |
| U.2 | Click on the page number "3" link to navigate to the third page of the results. | `page.locator("a").filter(has_text="3").nth(2).click()` | | | |
| U.3 | Click on the "First Page" button in the pagination controls to navigate back to the first page of the results. | `page.locator("div:nth-child(7) > div > .componentParentWrapper > esp-grid-container > esp-card-component > .card-container > .card-content > esp-row-dimentional-grid > div > #paginationId > esp-pagination-v2 > .d-flex.w-100 > .pagination-pager > .pagination-first").click()` | | | |
```
