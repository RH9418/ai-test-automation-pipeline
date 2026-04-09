# Feature: Bbu Alerts
**Tab Location:** Main Workspace

## Detailed User Interaction Flows

| Use Case ID | Test Case Description | Exact Locator | Pass/Fail | Notes | Issues |
|:---|:---|:---|:---|:---|:---|
```markdown
| | **--- INITIAL NAVIGATION TO DASHBOARD ---** | | | | |
| C.1 | Navigate to the 'Executive Dashboard' in the demand planning application by entering the specified URL in the browser. | `page.goto("https://stage.bbu.esp.antuit.ai/dp/demand-planning/executive-dashboard?workbookId=4&tabIndex=1")` | | | |
```
```markdown
| | **--- FILTER INTERACTIONS ---** | | | | |
| D.1 | Click on the 'Filter' button to open the filter options in the dashboard. | `page.get_by_text("Filter").click()` | | | |
| D.2 | From the filter dropdown, select the 'Alerts' option to filter by alerts. | `page.locator("#alerts-filterId").get_by_text("Alerts").click()` | | | |
| D.3 | Click on the dropdown caret to expand the filter options. | `page.locator(".dropdown-caret").first.click()` | | | |
| D.4 | From the expanded dropdown, select the 'Over Bias' filter option. | `page.locator("div").filter(has_text=re.compile(r"^Over Bias$")).nth(1).click()` | | | |
| D.5 | Click on the dropdown caret again to expand the filter options. | `page.locator(".dropdown-caret").first.click()` | | | |
| D.6 | From the expanded dropdown, select the 'Under Bias' filter option. | `page.locator("div").filter(has_text=re.compile(r"^Under Bias$")).nth(1).click()` | | | |
| D.7 | Click on the dropdown caret again to expand the filter options. | `page.locator(".dropdown-caret").first.click()` | | | |
| D.8 | From the expanded dropdown, select the 'MAPE' filter option. | `page.locator("div").filter(has_text=re.compile(r"^MAPE$")).nth(1).click()` | | | |
| D.9 | Click on the dropdown caret again to expand the filter options. | `page.locator(".dropdown-caret").first.click()` | | | |
| D.10 | From the expanded dropdown, select the 'Stability' filter option. | `page.locator("div").filter(has_text=re.compile(r"^Stability$")).nth(1).click()` | | | |
| D.11 | Click on the dropdown caret again to expand the filter options. | `page.locator(".dropdown-caret").first.click()` | | | |
| D.12 | From the expanded dropdown, select the 'FVA' filter option. | `page.locator("div").filter(has_text=re.compile(r"^FVA$")).nth(1).click()` | | | |
```
```markdown
| | **--- COLUMN VISIBILITY CONFIGURATION ---** | | | | |
| E.1 | Click on the 'Columns' button to open the column visibility configuration panel. | `page.get_by_role("button", name="columns").click()` | | | |
| E.2 | Check the 'Toggle All Columns Visibility' checkbox to make all columns visible. | `page.get_by_role("checkbox", name="Toggle All Columns Visibility").check()` | | | |
| E.3 | Uncheck the '6W-Actuals Column' checkbox to hide this specific column. | `page.get_by_role("treeitem", name="6W-Actuals Column").get_by_label("Press SPACE to toggle visibility (visible)").uncheck()` | | | |
| E.4 | Uncheck the 'User Bias Column' checkbox to hide this specific column. | `page.get_by_role("treeitem", name="User Bias Column").get_by_label("Press SPACE to toggle visibility (visible)").uncheck()` | | | |
```
```markdown
| | **--- PREFERENCES AND DOWNLOAD HANDLING ---** | | | | |
| F.1 | Click on the 'Adjustments' button to open the preferences menu. | `page.locator(".pointer.zeb-adjustments").click()` | | | |
| F.2 | Click on 'Save Preference' to save the current column visibility settings. | `page.get_by_text("Save Preference").click()` | | | |
| F.3 | Click on the 'Download' button to export the saved preferences. | `page.locator(".icon-color-toolbar-active.zeb-download-underline").click()` | | | |
```
```markdown
| | **--- FILTER AND STATUS DROPDOWN INTERACTIONS ---** | | | | |
| G.1 | Click on the 'Adjustments' button again to reopen the preferences menu. | `page.locator(".pointer.zeb-adjustments").click()` | | | |
| G.2 | Click on 'Reset Preference' to revert to the default column visibility settings. | `page.get_by_text("Reset Preference").click()` | | | |
| G.3 | Click on the filter icon to open the filter menu for the first column. | `page.locator(".ag-icon.ag-icon-filter").first.click()` | | | |
| G.4 | Enter 'WINCO' into the filter text box to filter the data by this value. | `page.get_by_role("textbox", name="Filter Value").fill("WINCO")` | | | |
| G.5 | Click on the 'Apply' button to apply the filter and update the data view. | `page.get_by_role("button", name="Apply").click()` | | | |
| G.6 | Click on the filter icon again to reopen the filter menu for the first column. | `page.locator(".ag-icon.ag-icon-filter").first.click()` | | | |
| G.7 | Click on the 'Reset' button to clear the applied filter and restore the default data view. | `page.get_by_role("button", name="Reset").click()` | | | |
| G.8 | Click on the dropdown caret to open the dropdown menu for selecting a status. | `page.locator(".w-100.p-h-16.p-v-8.dropdown-label.icon-small-dropdown > .d-flex.align-items-center > .dropdown-caret").first.click()` | | | |
| G.9 | Select the 'In progress' option from the dropdown menu. | `page.get_by_text("In progress").click()` | | | |
| G.10 | Click on the dropdown caret again to reopen the dropdown menu for selecting a status. | `page.locator(".w-100.p-h-16.p-v-8.dropdown-label.icon-small-dropdown > .d-flex.align-items-center > .dropdown-caret").first.click()` | | | |
| G.11 | Select the 'Completed' option from the dropdown menu. | `page.get_by_text("Completed").click()` | | | |
| G.12 | Click on the dropdown caret again to reopen the dropdown menu for selecting a status. | `page.locator(".w-100.p-h-16.p-v-8.dropdown-label.icon-small-dropdown > .d-flex.align-items-center > .dropdown-caret").first.click()` | | | |
| G.13 | Select the 'Not started' option from the dropdown menu. | `page.get_by_text("Not started").click()` | | | |
```
```markdown
| | **--- TREEGRID INTERACTIONS ---** | | | | |
| H.1 | Double-click on 'WALMART STORES HQ' in the treegrid to expand its details. | `page.get_by_role("treegrid").get_by_text("WALMART STORES HQ").dblclick()` | | | |
| H.2 | Double-click on the first occurrence of the text 'WALMART' to navigate further. | `page.locator("span").filter(has_text="WALMART").first.dblclick()` | | | |
| H.3 | Double-click on 'WALMART 0906 SC B-0006805-01-' in the treegrid to expand its details. | `page.get_by_role("treegrid").get_by_text("WALMART 0906 SC B-0006805-01-").dblclick()` | | | |
| H.4 | Right-click on 'WALMART 0906 SC B-0006805-01-' to open the context menu. | `page.get_by_text("WALMART 0906 SC B-0006805-01-").click(button="right")` | | | |
| H.5 | Click on 'Drill up' from the context menu to navigate up one level. | `page.get_by_text("Drill up").click()` | | | |
| H.6 | Right-click on the highlighted row in the treegrid to open the context menu. | `page.locator(".ag-row-even.ag-row-focus.ag-row-not-inline-editing.ag-row.ag-row-level-0.ag-row-position-absolute.ag-row-first.ag-row-hover > .ag-cell-value > .ag-cell-wrapper").click(button="right")` | | | |
| H.7 | Click on 'Drill up' from the context menu to navigate up one level. | `page.get_by_text("Drill up").click()` | | | |
| H.8 | Right-click on 'WALMART STORES HQ' in the treegrid to open the context menu. | `page.get_by_role("treegrid").get_by_text("WALMART STORES HQ").click(button="right")` | | | |
| H.9 | Click on 'Drill up' from the context menu to navigate up one level. | `page.get_by_text("Drill up").click()` | | | |
```
```markdown
| | **--- PAGINATION AND GRID INTERACTIONS ---** | | | | |
| I.1 | Click on the column header labeled '6W-Actuals' to sort or interact with the column. | `page.get_by_role("columnheader", name="6W-Actuals").click()` | | | |
| I.2 | Click on the page number '2' in the pagination control to navigate to the second page of the grid. | `page.locator("a").filter(has_text="2").click()` | | | |
| I.3 | Click on the 'First Page' button in the pagination control to navigate to the first page of the grid. | `page.locator(".zeb-nav-to-first").click()` | | | |
| I.4 | Select the row containing 'WALMART STORES HQ' by checking the checkbox in the grid cell. | `page.get_by_role("gridcell", name="Press Space to toggle row selection (unchecked)   WALMART STORES HQ").get_by_label("Press Space to toggle row").check()` | | | |
| I.5 | Uncheck the first checkbox in the grid using the '.checkbox-primary-color' locator. | `page.locator(".checkbox-primary-color").first.uncheck()` | | | |
| I.6 | Check the first checkbox in the grid using the '.checkbox-primary-color' locator. | `page.locator(".checkbox-primary-color").first.check()` | | | |
| I.7 | Uncheck the first checkbox in the grid using the '.d-flex.align-items-center.checkbox-primary-color' locator. | `page.locator(".d-flex.align-items-center.checkbox-primary-color").first.uncheck()` | | | |
| I.8 | Uncheck the first checkbox in the grid using a more specific locator targeting a nested structure within the grid. | `page.locator(".ag-row-odd > .ag-cell-value > .ag-cell-wrapper > .ag-group-value > aeap-group-cell-renderer > .d-flex.align-items-center.w-fit-content > .d-flex").first.uncheck()` | | | |
```
```markdown
| | **--- ADVANCED COLUMN VISIBILITY CONFIGURATION ---** | | | | |
| J.1 | Click on the 'Columns' button to open the column visibility configuration panel. | `page.get_by_role("button", name="columns").nth(1).click()` | | | |
| J.2 | Check the 'Toggle All Columns Visibility' checkbox to make all columns visible. | `page.get_by_role("checkbox", name="Toggle All Columns Visibility").check()` | | | |
| J.3 | Click on the 'Filter Columns Input' textbox to focus on it. | `page.get_by_role("textbox", name="Filter Columns Input").click()` | | | |
| J.4 | Fill the 'Filter Columns Input' textbox with the text 'User Bias' to filter columns by this keyword. | `page.get_by_role("textbox", name="Filter Columns Input").fill("User Bias")` | | | |
| J.5 | Uncheck the checkbox corresponding to the 'User Bias' column to hide it. | `page.get_by_role("checkbox", name="Press SPACE to toggle visibility (visible)").uncheck()` | | | |
| J.6 | Click on the 'Filter Columns Input' textbox again to focus on it. | `page.get_by_role("textbox", name="Filter Columns Input").click()` | | | |
| J.7 | Select all text in the 'Filter Columns Input' textbox using the 'ControlOrMeta+a' keyboard shortcut. | `page.get_by_role("textbox", name="Filter Columns Input").press("ControlOrMeta+a")` | | | |
| J.8 | Clear the 'Filter Columns Input' textbox by filling it with an empty string. | `page.get_by_role("textbox", name="Filter Columns Input").fill("")` | | | |
| J.9 | Check the 'Toggle All Columns Visibility' checkbox again to ensure all columns are visible. | `page.get_by_role("checkbox", name="Toggle All Columns Visibility").check()` | | | |
| J.10 | Click on the 'Columns' button to close the column visibility configuration panel. | `page.get_by_role("button", name="columns").nth(1).click()` | | | |
```
```markdown
| | **--- PREFERENCE AND EXPORT HANDLING ---** | | | | |
| K.1 | Click on the 'Preference' dropdown menu to open the preference options. | `page.locator("div:nth-child(3) > #preference-iconId > .legend-font > .multiselect-dropdown > .pointer").click()` | | | |
| K.2 | Click on the 'Save Preference' option to save the current grid settings. | `page.get_by_text("Save Preference").click()` | | | |
| K.3 | Click on the 'Export' button to export the grid data, triggering a file download. | `page.locator("div:nth-child(2) > #export-iconId > .icon-color-toolbar-active").click()` | | | |
```
```markdown
| | **--- COLUMN FILTERING AND RESET ---** | | | | |
| L.1 | Click on the 'Preference' dropdown menu again to reopen the preference options. | `page.locator("div:nth-child(3) > #preference-iconId > .legend-font > .multiselect-dropdown > .pointer").click()` | | | |
| L.2 | Click on the 'Reset Preference' option to revert the grid settings to their default state. | `page.get_by_text("Reset Preference").click()` | | | |
| L.3 | Click on the filter icon in the column header to open the filter options for the selected column. | `page.locator(".ag-header-cell.ag-header-parent-hidden.ag-header-background.ag-focus-managed.ag-header-active > .ag-header-cell-comp-wrapper > .ag-cell-label-container > .ag-header-icon > .ag-icon").click()` | | | |
| L.4 | Enter the filter value '761' into the filter input field to apply a filter to the column. | `page.get_by_role("spinbutton", name="Filter Value").fill("761")` | | | |
| L.5 | Click on the 'Apply' button in the column filter menu to apply the filter and update the grid data. | `page.get_by_label("Column Filter").get_by_role("button", name="Apply").click()` | | | |
| L.6 | Click on the filter icon again to reopen the column filter menu after applying the filter. | `page.locator(".ag-header-icon.ag-header-cell-filter-button.ag-filter-active > .ag-icon").click()` | | | |
| L.7 | Click on the 'Reset' button in the column filter menu to clear the applied filter and restore the grid data to its original state. | `page.get_by_label("Column Filter").get_by_role("button", name="Reset").click()` | | | |
```
```markdown
| | **--- ROW AND DRILL-DOWN INTERACTIONS ---** | | | | |
| M.1 | Check the first checkbox with the primary color styling to select the corresponding row. | `page.locator(".checkbox-primary-color").first.check()` | | | |
| M.2 | Double-click on the row containing the text 'ENTENMANNS' to drill down into its details. | `page.locator("span").filter(has_text="ENTENMANNS").first.dblclick()` | | | |
| M.3 | Double-click on the row containing the text 'EN BITES' to further drill down into its details. | `page.locator("span").filter(has_text="EN BITES").first.dblclick()` | | | |
| M.4 | Double-click on the row containing the text 'EN LITTLE BITES CP' to navigate deeper into its details. | `page.get_by_text("EN LITTLE BITES CP").first.dblclick()` | | | |
| M.5 | Right-click on the row containing the text 'EN LB CHOCCH MFN 10P-' to open the context menu for additional actions. | `page.get_by_text("EN LB CHOCCH MFN 10P-").first.click(button="right")` | | | |
| M.6 | Click on the 'Drill up' option in the context menu to navigate back to the previous level. | `page.get_by_text("Drill up").click()` | | | |
| M.7 | Right-click on the first grid cell with an empty text value to open the context menu. | `page.get_by_role("gridcell").filter(has_text=re.compile(r"^$")).first.click(button="right")` | | | |
| M.8 | Click on the first grid cell with an empty text value to select it. | `page.get_by_role("gridcell").filter(has_text=re.compile(r"^$")).first.click()` | | | |
```
```markdown
| | **--- PRODUCT NAVIGATION AND TIME FILTER ---** | | | | |
| N.1 | Click on the link within the 'Products' card to navigate to the detailed view of the products. | `page.locator("esp-card-component").filter(has_text="Products10 rows out of 11").locator("a").click()` | | | |
| N.2 | Click on the 'First Page' button in the pagination controls to navigate to the first page of the product list. | `page.locator("div:nth-child(3) > esp-pagination-v2 > .d-flex.w-100 > .pagination-pager > .pagination-first > .zeb-nav-to-first").click()` | | | |
| N.3 | Click on the 'Apply' button to apply the selected filters or changes. | `page.get_by_role("button", name="Apply").click()` | | | |
| N.4 | Click on the 'Filter' section to expand or interact with the filter options. | `page.locator("div").filter(has_text=re.compile(r"^Filter$")).nth(1).click()` | | | |
| N.5 | Click on the dropdown caret in the 'Time' filter to open the dropdown menu. | `page.locator("#time-filterId > .wr-20 > esp-multiselect-dropdown > .multiselect-dropdown > div > .w-100 > .d-flex.align-items-center > .dropdown-caret").click()` | | | |
| N.6 | Select the 'Latest 5 Next 4' option from the 'Time' filter dropdown. | `page.locator("div").filter(has_text=re.compile(r"^Latest 5 Next 4$")).nth(1).click()` | | | |
| N.7 | Click on the dropdown caret in the 'Time' filter again to open the dropdown menu for a new selection. | `page.locator("#time-filterId > .wr-20 > esp-multiselect-dropdown > .multiselect-dropdown > div > .w-100 > .d-flex.align-items-center > .dropdown-caret").click()` | | | |
| N.8 | Select the 'Latest 5 Next 12' option from the 'Time' filter dropdown. | `page.locator("div").filter(has_text=re.compile(r"^Latest 5 Next 12$")).nth(1).click()` | | | |
| N.9 | Click on the dropdown caret in the 'Time' filter again to open the dropdown menu for another selection. | `page.locator("#time-filterId > .wr-20 > esp-multiselect-dropdown > .multiselect-dropdown > div > .w-100 > .d-flex.align-items-center > .dropdown-caret").click()` | | | |
| N.10 | Select the 'Latest 13 Next 4' option from the 'Time' filter dropdown. | `page.locator("div").filter(has_text=re.compile(r"^Latest 13 Next 4$")).nth(1).click()` | | | |
```
```markdown
| | **--- WEEKLY SUMMARY AND COLUMN VISIBILITY ---** | | | | |
| O.1 | Click on the 'Weekly Summary Customer:' card button to expand or interact with the card. | `page.locator("esp-card-component").filter(has_text="Weekly Summary Customer:").get_by_role("button").click()` | | | |
| O.2 | Uncheck the visibility toggle for the column labeled '-11-02 (45) Column'. | `page.get_by_role("treeitem", name="-11-02 (45) Column").get_by_label("Press SPACE to toggle visibility (visible)").uncheck()` | | | |
| O.3 | Uncheck the visibility toggle for the column labeled '-11-09 (46) Column'. | `page.get_by_role("treeitem", name="-11-09 (46) Column").get_by_label("Press SPACE to toggle visibility (visible)").uncheck()` | | | |
| O.4 | Uncheck the visibility toggle for the column labeled '-11-16 (47) Column'. | `page.get_by_role("treeitem", name="-11-16 (47) Column").get_by_label("Press SPACE to toggle visibility (visible)").uncheck()` | | | |
| O.5 | Check the 'Toggle All Columns Visibility' checkbox to make all columns visible. | `page.get_by_role("checkbox", name="Toggle All Columns Visibility").check()` | | | |
| O.6 | Click on the preference dropdown icon to open the preference options. | `page.locator("div:nth-child(4) > #preference-iconId > .legend-font > .multiselect-dropdown > .pointer").click()` | | | |
| O.7 | Click on 'Save Preference' to save the current column visibility settings. | `page.get_by_text("Save Preference").click()` | | | |
| O.8 | Click on the preference dropdown icon again to reopen the preference options. | `page.locator("div:nth-child(4) > #preference-iconId > .legend-font > .multiselect-dropdown > .pointer").click()` | | | |
| O.9 | Click on 'Reset Preference' to reset the column visibility settings to their default state. | `page.get_by_text("Reset Preference").click()` | | | |
```
```markdown
| | **--- EXPORT AND PAGINATION INTERACTIONS ---** | | | | |
| P.1 | Click on the export icon to initiate the download process. | `page.locator("div:nth-child(3) > #export-iconId > .icon-color-toolbar-active").click()` | | | |
| P.2 | Click on the first element with the class 'align-middle' to interact with it. | `page.locator(".align-middle").first.click()` | | | |
| P.3 | Click on the second occurrence of the text 'Event' to navigate or interact with the Event section. | `page.get_by_text("Event").nth(1).click()` | | | |
| P.4 | Click on the button within the 'Event Details columns (0)' card to open column visibility options. | `page.locator("esp-card-component").filter(has_text="Event Details columns (0)").get_by_role("button").click()` | | | |
| P.5 | Uncheck the visibility toggle for the 'Event Column' to hide it. | `page.get_by_role("treeitem", name="Event Column").get_by_label("Press SPACE to toggle visibility (visible)").uncheck()` | | | |
| P.6 | Uncheck the visibility toggle for the 'UPC 12 Column' to hide it. | `page.get_by_role("treeitem", name="UPC 12 Column").get_by_label("Press SPACE to toggle visibility (visible)").uncheck()` | | | |
| P.7 | Uncheck the visibility toggle for the 'Customer Level 2 Column' to hide it. | `page.get_by_role("treeitem", name="Customer Level 2 Column").get_by_label("Press SPACE to toggle visibility (visible)").uncheck()` | | | |
| P.8 | Uncheck the visibility toggle for the 'Start Date Column' to hide it. | `page.get_by_role("treeitem", name="Start Date Column").get_by_label("Press SPACE to toggle visibility (visible)").uncheck()` | | | |
| P.9 | Uncheck the visibility toggle for the 'End Date Column' to hide it. | `page.get_by_role("treeitem", name="End Date Column").get_by_label("Press SPACE to toggle visibility (visible)").uncheck()` | | | |
| P.10 | Uncheck the visibility toggle for the 'Max Promo Price Column' to hide it. | `page.get_by_role("treeitem", name="Max Promo Price Column").get_by_label("Press SPACE to toggle visibility (visible)").uncheck()` | | | |
| P.11 | Uncheck the visibility toggle for the 'Min Promo Price Column' to hide it. | `page.get_by_role("treeitem", name="Min Promo Price Column").get_by_label("Press SPACE to toggle visibility (visible)").uncheck()` | | | |
| P.12 | Check the 'Toggle All Columns Visibility' checkbox to make all columns visible again. | `page.get_by_role("checkbox", name="Toggle All Columns Visibility").check()` | | | |
| P.13 | Click on the 'Filter Columns Input' textbox to focus on it. | `page.get_by_role("textbox", name="Filter Columns Input").click()` | | | |
| P.14 | Fill the 'Filter Columns Input' textbox with the text 'UPC' to filter columns by this keyword. | `page.get_by_role("textbox", name="Filter Columns Input").fill("UPC")` | | | |
| P.15 | Uncheck the visibility toggle for the filtered column matching 'UPC' to hide it. | `page.get_by_role("checkbox", name="Press SPACE to toggle visibility (visible)").uncheck()` | | | |
| P.16 | Click on the 'Preference' icon to open the dropdown menu for saving preferences. | `page.locator("div:nth-child(7) > div > esp-grid-container > esp-card-component > .card-container > .title > .grid-icons-container > esp-grid-icons-component > .display-grid-icons > div:nth-child(2) > #preference-iconId > .legend-font > .multiselect-dropdown > .pointer").click()` | | | |
| P.17 | Click on 'Save Preference' to save the current grid settings or preferences. | `page.get_by_text("Save Preference").click()` | | | |
| P.18 | Click on the 'Export' icon to initiate the export process and trigger the file download. | `page.locator("div:nth-child(7) > div > esp-grid-container > esp-card-component > .card-container > .title > .grid-icons-container > esp-grid-icons-component > .display-grid-icons > div > #export-iconId > .icon-color-toolbar-active").click()` | | | |
| P.19 | Click on the second page link in the pagination to navigate to the second page of the grid. | `page.locator("a").nth(2).click()` | | | |
| P.20 | Click on the page link labeled '3' to navigate to the third page of the grid. | `page.locator("a").filter(has_text="3").click()` | | | |
| P.21 | Click on the 'First Page' button in the pagination controls to navigate back to the first page of the grid. | `page.locator("div:nth-child(7) > div > esp-grid-container > esp-card-component > .card-container > .card-content > esp-row-dimentional-grid > div > #paginationId > esp-pagination-v2 > .d-flex.w-100 > .pagination-pager > .pagination-first").click()` | | | |
```
```markdown
| | **--- ROW DISPLAY AND COLUMN FILTERING ---** | | | | |
| Q.1 | Click on the dropdown labeled 'View 10 row(s)' to open the row display options. | `page.get_by_text("View 10 row(s)").nth(2).click()` | | | |
| Q.2 | Select the option 'View 20 row(s)' from the dropdown to change the number of rows displayed. | `page.locator("div").filter(has_text=re.compile(r"^View 20 row\(s\)$")).nth(1).click()` | | | |
| Q.3 | Click on the column header icon to open the filter options for the column. | `page.locator(".ag-header-cell.ag-header-parent-hidden.ag-header-cell-sortable.ag-header-background.ag-focus-managed.ag-header-active > .ag-header-cell-comp-wrapper > .ag-cell-label-container > .ag-header-icon > .ag-icon").click()` | | | |
| Q.4 | Fill the filter textbox with the value 'Promotion' to filter the column based on this value. | `page.get_by_role("textbox", name="Filter Value").fill("Promotion")` | | | |
| Q.5 | Click the 'Apply' button to apply the column filter. | `page.get_by_label("Column Filter").get_by_role("button", name="Apply").click()` | | | |
| Q.6 | Click on the filtered column header to interact with the column filter settings. | `page.locator(".ag-header-cell.ag-header-parent-hidden.ag-header-cell-sortable.ag-header-background.ag-focus-managed.ag-header-cell-filtered > .ag-header-cell-comp-wrapper > .ag-cell-label-container").click()` | | | |
| Q.7 | Click on the filter icon to open the active filter options for the column. | `page.locator(".ag-header-icon.ag-header-cell-filter-button.ag-filter-active > .ag-icon").click()` | | | |
| Q.8 | Click the 'Reset' button to clear the applied column filter. | `page.get_by_label("Column Filter").get_by_role("button", name="Reset").click()` | | | |
```
```markdown
| | **--- FINAL GRID INTERACTIONS AND CLEANUP ---** | | | | |
| R.1 | Double-click on the grid cell with the name 'Promotion-TH PRO BAGEL ROLLBACK 12/29/25 thru 03/29/' to interact with or edit the cell. | `page.get_by_role("gridcell", name="Promotion-TH PRO BAGEL ROLLBACK 12/29/25 thru 03/29/").dblclick()` | | | |
| R.2 | Close the current page after completing the interaction. | `page.close()` | | | |
| R.3 | Close the browser context to clean up resources and end the session. | `context.close()` | | | |
| R.4 | Close the browser instance to terminate all associated contexts and sessions. | `browser.close()` | | | |
```
