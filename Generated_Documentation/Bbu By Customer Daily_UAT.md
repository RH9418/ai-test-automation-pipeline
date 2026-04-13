# Feature: Bbu By Customer Daily
**Tab Location:** Main Workspace

## Detailed User Interaction Flows

| Use Case ID | Test Case Description | Exact Locator | Pass/Fail | Notes | Issues |
|:---|:---|:---|:---|:---|:---|
| | **--- INITIAL NAVIGATION TO DASHBOARD ---** | | | | |
| C.1 | Navigate to the 'Executive Dashboard' in the demand planning module by entering the specified URL. | `page.goto("https://stage.bbu.esp.antuit.ai/dp/demand-planning/executive-dashboard?workbookId=4&tabIndex=5")` | | | |
```
| | **--- CUSTOMER TOTAL COLUMN SELECTION ---** | | | | |
| D.1 | Click on the 'Customer Total columns (0)' text to open the column selection menu. | `page.get_by_text("Customer Total columns (0)").click()` | | | |
| D.2 | Click on the 'Customer Total' text to select the corresponding column. | `page.get_by_text("Customer Total").click()` | | | |
| D.3 | Click on the button within the 'Customer Total columns (0)' card to confirm the selection or perform an action. | `page.locator("esp-card-component").filter(has_text="Customer Total columns (0)").get_by_role("button").click()` | | | |
```
```
| | **--- FILTER COLUMNS INPUT INTERACTION ---** | | | | |
| E.1 | Click on the 'Filter Columns Input' textbox to focus on it for entering a filter value. | `page.get_by_role("textbox", name="Filter Columns Input").click()` | | | |
| E.2 | Type the text 'System' into the 'Filter Columns Input' textbox to filter columns containing this keyword. | `page.get_by_role("textbox", name="Filter Columns Input").fill("System")` | | | |
| E.3 | Press 'Enter' while focused on the 'Filter Columns Input' textbox to apply the filter and display matching columns. | `page.get_by_role("textbox", name="Filter Columns Input").press("Enter")` | | | |
```
```
| | **--- COLUMN SELECTION AND CHECKBOX TOGGLE ---** | | | | |
| F.1 | Click on the first column in the filtered list to select it. | `page.locator(".ag-column-select-column").first.click()` | | | |
| F.2 | Check the checkbox for 'System Forecast Base (Plan)' by toggling it using the SPACE key. | `page.get_by_role("treeitem", name="System Forecast Base (Plan").get_by_label("Press SPACE to toggle").check()` | | | |
```
```
| | **--- FILTER RESET AND ADDITIONAL COLUMN SELECTION ---** | | | | |
| G.1 | Click on the third column in the list to select it. | `page.locator("div:nth-child(3) > .ag-column-select-column").click()` | | | |
| G.2 | Click on the 'Filter Columns Input' textbox again to clear or modify the filter. | `page.get_by_role("textbox", name="Filter Columns Input").click()` | | | |
| G.3 | Clear the 'Filter Columns Input' textbox by filling it with an empty string. | `page.get_by_role("textbox", name="Filter Columns Input").fill("")` | | | |
| G.4 | Press 'Enter' to reset the filter and display all columns. | `page.get_by_role("textbox", name="Filter Columns Input").press("Enter")` | | | |
```
```
| | **--- SYSTEM FORECAST COLUMN SELECTION ---** | | | | |
| H.1 | Click on the 'System Forecast Promotion (' label to select the corresponding column. | `page.get_by_label("System Forecast Promotion (").get_by_text("System Forecast Promotion (").click()` | | | |
| H.2 | Click on the 'System Forecast Total (Plan+1)' label to select the corresponding column. | `page.get_by_label("System Forecast Total (Plan+1").get_by_text("System Forecast Total (Plan+1").click()` | | | |
| H.3 | Click on the 'System Forecast Base (Plan+1)' label to select the corresponding column. | `page.get_by_label("System Forecast Base (Plan+1").get_by_text("System Forecast Base (Plan+1").click()` | | | |
| H.4 | Click on the 'System Forecast Promotion (' label again to toggle its selection. | `page.get_by_label("System Forecast Promotion (").get_by_text("System Forecast Promotion (").click()` | | | |
```
```
| | **--- 6 WEEK METRICS COLUMN SELECTION ---** | | | | |
| I.1 | Click on the '6 Week Gross Units Average' column to select it. | `page.get_by_label("6 Week Gross Units Average").get_by_text("Week Gross Units Average").click()` | | | |
| I.2 | Click on the '6 Week Aged Net Units Average Column' to select it, ensuring the exact match is used. | `page.get_by_label("6 Week Aged Net Units Average Column", exact=True).get_by_text("Week Aged Net Units Average").click()` | | | |
| I.3 | Click on the 'LY 6 Week Aged Net Units' column to select it. | `page.get_by_label("LY 6 Week Aged Net Units").get_by_text("LY 6 Week Aged Net Units").click()` | | | |
| I.4 | Click on the '% Change 6 Week Aged Net' column to select it. | `page.get_by_label("% Change 6 Week Aged Net").get_by_text("% Change 6 Week Aged Net").click()` | | | |
| I.5 | Click on the '6 Week Scan Units Average Column' to select it, ensuring the exact match is used. | `page.get_by_label("6 Week Scan Units Average Column", exact=True).get_by_text("Week Scan Units Average").click()` | | | |
| I.6 | Click on the 'LY 6 Week Scan Units Average' column to select it. | `page.get_by_label("LY 6 Week Scan Units Average").get_by_text("LY 6 Week Scan Units Average").click()` | | | |
| I.7 | Click on the '% Change 6 Week Scan Units' column to select it. | `page.get_by_label("% Change 6 Week Scan Units").get_by_text("% Change 6 Week Scan Units").click()` | | | |
```
```
| | **--- COLUMN SELECTION ACTIONS ---** | | | | |
| J.1 | Click on the 'Freshness (6 Week Average)' column to select it. | `page.get_by_label("Freshness (6 Week Average)").get_by_text("Freshness (6 Week Average)").click()` | | | |
| J.2 | Click on the '6 Week Aged Returns Units' column to select it. | `page.get_by_label("6 Week Aged Returns Units").get_by_text("6 Week Aged Returns Units").click()` | | | |
| J.3 | Click on the 'System Forecast Total (Plan Week)' column to select it using its locator. | `page.locator("#ag-169").get_by_text("System Forecast Total (Plan Week)").click()` | | | |
| J.4 | Click on the 'System Forecast Base (Plan)' column to select it. | `page.get_by_label("System Forecast Base (Plan").get_by_text("System Forecast Base (Plan").click()` | | | |
| J.5 | Click on the button within the 'Customer Total columns (0)' card to select it. | `page.locator("esp-card-component").filter(has_text="Customer Total columns (0)").get_by_role("button").click()` | | | |
```
```
| | **--- FILE EXPORT HANDLING ---** | | | | |
| K.1 | Click on the 'Export' icon within the 'esp-grid-icons-component' to initiate the export process. | `page.locator("esp-grid-icons-component").filter(has_text="Export").locator("#export-iconId").click()` | | | |
```
```
| | **--- PREFERENCE MANAGEMENT ---** | | | | |
| L.1 | Click on the first 'Adjustments' icon (identified by the '.pointer.zeb-adjustments' locator) to open the adjustments menu. | `page.locator(".pointer.zeb-adjustments").first.click()` | | | |
| L.2 | Click on the 'Save Preference' option to save the current preferences. | `page.get_by_text("Save Preference").click()` | | | |
| L.3 | Click on the first 'Adjustments' icon again to reopen the adjustments menu. | `page.locator(".pointer.zeb-adjustments").first.click()` | | | |
| L.4 | Click on the 'Reset Preference' option to reset the preferences to their default state. | `page.get_by_text("Reset Preference").click()` | | | |
```
```
| | **--- GRID INTERACTION AND COLUMN CONFIGURATION ---** | | | | |
| M.1 | Click on the first horizontal scroll container to interact with the grid. | `page.locator(".ag-body-horizontal-scroll-container").first.click()` | | | |
| M.2 | Click on the 'Customers columns (0)' text to open the column configuration panel. | `page.get_by_text("Customers columns (0)").click()` | | | |
| M.3 | Click on the 'Customers' text to select the Customers section. | `page.get_by_text("Customers").click()` | | | |
| M.4 | Click on 'Customers columns (0)' again to toggle the column configuration panel. | `page.get_by_text("Customers columns (0)").click()` | | | |
| M.5 | Click on the button within the 'Customers columns (0)' card to expand its options. | `page.locator("esp-card-component").filter(has_text="Customers columns (0)").get_by_role("button").click()` | | | |
| M.6 | Click on the column panel header to access column selection options. | `page.locator("#ag-87 > .ag-column-panel > .ag-column-select > .ag-column-select-header").click()` | | | |
```
```
| | **--- COLUMN FILTERING AND VISIBILITY MANAGEMENT ---** | | | | |
| N.1 | Type 'Fresh' into the 'Filter Columns Input' textbox to filter the columns. | `page.get_by_role("textbox", name="Filter Columns Input").fill("Fresh")` | | | |
| N.2 | Press 'Enter' in the 'Filter Columns Input' textbox to apply the filter. | `page.get_by_role("textbox", name="Filter Columns Input").press("Enter")` | | | |
| N.3 | Check the checkbox labeled 'Press SPACE to toggle visibility (hidden)' to make the column visible. | `page.get_by_role("checkbox", name="Press SPACE to toggle visibility (hidden)").check()` | | | |
| N.4 | Uncheck the 'Toggle All Columns Visibility' checkbox to hide all columns. | `page.get_by_role("checkbox", name="Toggle All Columns Visibility").uncheck()` | | | |
| N.5 | Click on the 'Filter Columns Input' textbox to focus on it. | `page.get_by_role("textbox", name="Filter Columns Input").click()` | | | |
| N.6 | Clear the 'Filter Columns Input' textbox by filling it with an empty string. | `page.get_by_role("textbox", name="Filter Columns Input").fill("")` | | | |
| N.7 | Press 'Enter' in the 'Filter Columns Input' textbox to apply the filter after clearing it. | `page.get_by_role("textbox", name="Filter Columns Input").press("Enter")` | | | |
```
```
| | **--- SYSTEM FORECAST COLUMN SELECTION ---** | | | | |
| O.1 | Click on the column labeled 'System Forecast Total (Plan Week)' to select it. | `page.locator("#ag-87").get_by_text("System Forecast Total (Plan Week)").click()` | | | |
| O.2 | Click on the column labeled 'System Forecast Base (Plan Week)' to select it. | `page.get_by_label("System Forecast Base (Plan Week) Column").get_by_text("System Forecast Base (Plan").click()` | | | |
| O.3 | Click on the column labeled 'System Forecast Promotion (Plan Week)' to select it. | `page.get_by_label("System Forecast Promotion (Plan Week) Column").get_by_text("System Forecast Promotion (").click()` | | | |
| O.4 | Click on the column labeled 'System Forecast Total (Plan+1)' to select it. | `page.get_by_label("System Forecast Total (Plan+1").get_by_text("System Forecast Total (Plan+1").click()` | | | |
| O.5 | Click on the column labeled 'System Forecast Base (Plan+1)' to select it. | `page.get_by_label("System Forecast Base (Plan+1").get_by_text("System Forecast Base (Plan+1").click()` | | | |
| O.6 | Click on the column labeled 'System Forecast Promotion (Plan+1 Week)' to select it. | `page.get_by_label("System Forecast Promotion (Plan+1 Week) Column").get_by_text("System Forecast Promotion (").click()` | | | |
```
```
| | **--- COLUMN SELECTION ACTIONS ---** | | | | |
| P.1 | Click on the column labeled '6 Week Gross Units Average' to select it. | `page.get_by_label("6 Week Gross Units Average").get_by_text("Week Gross Units Average").click()` | | | |
| P.2 | Click on the column labeled '6 Week Aged Net Units Average' to select it. | `page.get_by_label("6 Week Aged Net Units Average Column", exact=True).get_by_text("6 Week Aged Net Units Average", exact=True).click()` | | | |
| P.3 | Click on the column labeled 'LY 6 Week Aged Net Units' to select it. | `page.get_by_label("LY 6 Week Aged Net Units").get_by_text("LY 6 Week Aged Net Units").click()` | | | |
| P.4 | Click on the column labeled '% Change 6 Week Aged Net' to select it. | `page.get_by_label("% Change 6 Week Aged Net").get_by_text("% Change 6 Week Aged Net").click()` | | | |
| P.5 | Click on the column labeled 'LY 6 Week Scan Units Average' to select it. | `page.get_by_label("LY 6 Week Scan Units Average").get_by_text("LY 6 Week Scan Units Average").click()` | | | |
| P.6 | Click on the column labeled '6 Week Scan Units Average' to select it. | `page.get_by_label("6 Week Scan Units Average Column", exact=True).get_by_text("Week Scan Units Average").click()` | | | |
| P.7 | Click on the column labeled '% Change 6 Week Scan Units' to select it. | `page.get_by_label("% Change 6 Week Scan Units").get_by_text("% Change 6 Week Scan Units").click()` | | | |
| P.8 | Click on the column labeled 'Freshness (6 Week Average)' to select it. | `page.get_by_label("Freshness (6 Week Average)").get_by_text("Freshness (6 Week Average)").click()` | | | |
| P.9 | Click on the column labeled '6 Week Aged Returns Units' to select it. | `page.get_by_label("6 Week Aged Returns Units").get_by_text("6 Week Aged Returns Units").click()` | | | |
```
```
| | **--- CUSTOMER COLUMNS EXPANSION AND EXPORT ---** | | | | |
| Q.1 | Click on the button within the 'Customers columns (0)' card to expand its options. | `page.locator("esp-card-component").filter(has_text="Customers columns (0)").get_by_role("button").click()` | | | |
| Q.2 | Click on the 'Export' icon to initiate the export process and trigger the file download. | `page.locator("div:nth-child(2) > #export-iconId > .icon-color-toolbar-active").click()` | | | |
```
```
| | **--- PREFERENCES MANAGEMENT ---** | | | | |
| R.1 | Click on the 'Preferences' dropdown menu to view available options. | `page.locator("div:nth-child(3) > #preference-iconId > .legend-font > .multiselect-dropdown > .pointer").click()` | | | |
| R.2 | Select the 'Save Preference' option from the dropdown to save the current preferences. | `page.get_by_text("Save Preference").click()` | | | |
| R.3 | Reopen the 'Preferences' dropdown menu to access additional options. | `page.locator("div:nth-child(3) > #preference-iconId > .legend-font > .multiselect-dropdown > .pointer").click()` | | | |
| R.4 | Select the 'Reset Preference' option from the dropdown to reset preferences to default. | `page.get_by_text("Reset Preference").click()` | | | |
```
```
| | **--- CUSTOMER COLUMN SORTING AND FILTERING ---** | | | | |
| S.1 | Click on the 'Customer' column header to sort or filter the column. | `page.locator("esp-row-dimentional-grid").get_by_text("Customer").click()` | | | |
| S.2 | Click on the descending sort icon to sort the 'Customer' column in descending order. | `page.locator(".ag-icon.ag-icon-desc").first.click()` | | | |
| S.3 | Click on the descending sort icon again to toggle the sorting order. | `page.locator(".ag-icon.ag-icon-desc").first.click()` | | | |
| S.4 | Open the filter menu for the 'Customer' column. | `page.locator(".ag-filter-body-wrapper").click()` | | | |
| S.5 | Select the 'Contains' filter option from the filter menu. | `page.get_by_text("Contains").click()` | | | |
| S.6 | Click on the 'Select Field' dropdown and choose the 'Contains' option. | `page.get_by_label("Select Field").get_by_text("Contains").click()` | | | |
| S.7 | Re-select the 'Contains' filter option to confirm the selection. | `page.get_by_text("Contains").click()` | | | |
| S.8 | Select the 'Does not contain' filter option from the filter menu. | `page.get_by_text("Does not contain").click()` | | | |
| S.9 | Re-select the 'Does not contain' filter option to confirm the selection. | `page.get_by_text("Does not contain").click()` | | | |
| S.10 | Select the 'Equals' filter option from the filter menu. | `page.get_by_role("option", name="Equals").click()` | | | |
| S.11 | Re-select the 'Equals' filter option to confirm the selection. | `page.get_by_text("Equals").click()` | | | |
| S.12 | Select the 'Does not equal' filter option from the filter menu. | `page.get_by_role("option", name="Does not equal").click()` | | | |
| S.13 | Re-select the 'Does not equal' filter option to confirm the selection. | `page.get_by_text("Does not equal").click()` | | | |
```
```
| | **--- FILTER OPTION SELECTION AND CONFIRMATION ---** | | | | |
| T.1 | Select the 'Begins with' filter option from the filter menu. | `page.get_by_role("option", name="Begins with").click()` | | | |
| T.2 | Open the filtering operator dropdown to choose a different operator. | `page.get_by_role("combobox", name="Filtering operator").click()` | | | |
| T.3 | Select the 'Ends with' filter option from the filter menu. | `page.get_by_role("option", name="Ends with").click()` | | | |
| T.4 | Re-select the 'Ends with' filter option to confirm the selection. | `page.get_by_text("Ends with").click()` | | | |
| T.5 | Select the 'Blank' filter option from the filter menu. | `page.get_by_role("option", name="Blank", exact=True).click()` | | | |
| T.6 | Re-select the 'Blank' filter option to confirm the selection. | `page.get_by_text("Blank").click()` | | | |
| T.7 | Select the 'Not blank' filter option from the filter menu. | `page.get_by_role("option", name="Not blank").click()` | | | |
```
```
| | **--- LOGICAL OPERATOR SELECTION ---** | | | | |
| U.1 | Select the 'AND' logical operator for combining filter conditions. | `page.get_by_text("AND", exact=True).click()` | | | |
| U.2 | Select the 'OR' logical operator for combining filter conditions. | `page.get_by_text("OR", exact=True).click()` | | | |
```
```
| | **--- COLUMN FILTER AND VALUE INPUT ---** | | | | |
| V.1 | Re-select the 'Contains' filter option to confirm the selection. | `page.get_by_text("Contains").click()` | | | |
| V.2 | Open the 'Column Filter' dropdown and choose the 'Contains' option. | `page.get_by_label("Column Filter").get_by_text("Contains").click()` | | | |
| V.3 | Click on the 'Filter Value' textbox to input a value for filtering. | `page.get_by_role("textbox", name="Filter Value").click()` | | | |
```
```
| | **--- FILTER RESET AND APPLICATION ---** | | | | |
| W.1 | Click on the 'Clear' button to remove the current filter value from the input field. | `page.get_by_role("button", name="Clear").click()` | | | |
| W.2 | Click on the 'Reset' button to restore all filter settings to their default state. | `page.get_by_role("button", name="Reset").click()` | | | |
| W.3 | Click on the filter icon in the column header to close the filter menu. | `page.locator(".ag-header-icon.ag-header-cell-filter-button > .ag-icon").first.click()` | | | |
| W.4 | Click on the 'Apply' button to confirm and apply the selected filter settings. | `page.get_by_role("button", name="Apply").click()` | | | |
```
```
| | **--- ROW AND CHECKBOX SELECTION ---** | | | | |
| X.1 | Click on the first occurrence of the '3RD PARTY DISTRIB' text to select it. | `page.locator("span").filter(has_text="3RD PARTY DISTRIB").first.click()` | | | |
| X.2 | Click on the '3RD PARTY DISTRIB' text to confirm the selection. | `page.get_by_text("3RD PARTY DISTRIB").click()` | | | |
| X.3 | Click on the first checkbox in the group to select it. | `page.locator(".ag-group-checkbox").first.click()` | | | |
| X.4 | Check the row with the label 'Press Space to toggle row selection (unchecked)' for '99 CENT'. | `page.get_by_role("gridcell", name="Press Space to toggle row selection (unchecked)  99 CENT").get_by_label("Press Space to toggle row").check()` | | | |
```
```
| | **--- SORTING AND FILTER MENU INTERACTION ---** | | | | |
| Y.1 | Click on the third occurrence of the 'System Forecast Total (Plan' text to select it. | `page.get_by_text("System Forecast Total (Plan").nth(2).click()` | | | |
| Y.2 | Click on the descending sort icon in the column header to toggle the sorting order. | `page.locator(".ag-cell-label-container.ag-header-cell-sorted-desc > .ag-header-icon > .ag-icon").click()` | | | |
| Y.3 | Open the filter menu by clicking on the filter body wrapper. | `page.locator(".ag-filter-body-wrapper").click()` | | | |
```
```
| | **--- EQUALITY AND COMPARISON FILTER SELECTION ---** | | | | |
| Z.1 | Select the 'Equals' filter option from the filter menu. | `page.get_by_text("Equals").click()` | | | |
| Z.2 | Click on the 'Select Field' dropdown and choose the 'Equals' option. | `page.get_by_label("Select Field").get_by_text("Equals").click()` | | | |
| Z.3 | Re-select the 'Equals' filter option to confirm the selection. | `page.get_by_text("Equals").click()` | | | |
| Z.4 | Select the 'Does not equal' filter option from the filter menu. | `page.get_by_text("Does not equal").click()` | | | |
| Z.5 | Re-select the 'Does not equal' filter option to confirm the selection. | `page.get_by_text("Does not equal").click()` | | | |
| Z.6 | Select the 'Greater than' filter option from the filter menu. | `page.get_by_text("Greater than", exact=True).click()` | | | |
| Z.7 | Re-select the 'Greater than' filter option to confirm the selection. | `page.get_by_text("Greater than").click()` | | | |
```
```
| | **--- FILTER SELECTION AND CONFIRMATION ---** | | | | |
| [.1 | Select the 'Greater than or equal to' filter option from the filter menu. | `page.get_by_text("Greater than or equal to").click()` | | | |
| [.2 | Re-select the 'Greater than or equal to' filter option to confirm the selection. | `page.get_by_text("Greater than or equal to").click()` | | | |
| [.3 | Select the 'Less than' filter option from the filter menu. | `page.get_by_role("option", name="Less than", exact=True).click()` | | | |
| [.4 | Re-select the 'Less than' filter option to confirm the selection. | `page.get_by_text("Less than").click()` | | | |
| [.5 | Select the 'Less than or equal to' filter option from the filter menu. | `page.get_by_text("Less than or equal to").click()` | | | |
| [.6 | Re-select the 'Less than or equal to' filter option to confirm the selection. | `page.get_by_text("Less than or equal to").click()` | | | |
| [.7 | Select the 'Between' filter option from the filter menu. | `page.get_by_role("option", name="Between").click()` | | | |
| [.8 | Re-select the 'Between' filter option to confirm the selection. | `page.get_by_text("Between").click()` | | | |
| [.9 | Select the 'Blank' filter option from the filter menu. | `page.get_by_role("option", name="Blank", exact=True).click()` | | | |
| [.10 | Re-select the 'Blank' filter option to confirm the selection. | `page.get_by_text("Blank").click()` | | | |
| [.11 | Select the 'Not blank' filter option from the filter menu. | `page.get_by_role("option", name="Not blank").click()` | | | |
```
```
| | **--- FILTER RESET AND APPLICATION ---** | | | | |
| [.1 | Click on the 'Clear' button to remove the current filter value. | `page.get_by_role("button", name="Clear").click()` | | | |
| [.2 | Click on the 'Reset' button to restore all filter settings to their default values. | `page.get_by_role("button", name="Reset").click()` | | | |
| [.3 | Click on the descending sort icon in the column header to toggle the sorting order. | `page.locator(".ag-cell-label-container.ag-header-cell-sorted-desc > .ag-header-icon > .ag-icon").click()` | | | |
| [.4 | Click on the 'Apply' button to confirm and apply the selected filter settings. | `page.get_by_role("button", name="Apply").click()` | | | |
```
```
| | **--- SORTING OPERATIONS ---** | | | | |
| ].1 | Click on the descending sort icon in the column header to sort the column in descending order. | `page.locator(".ag-cell-label-container.ag-header-cell-sorted-desc > .ag-header-cell-label > .ag-sort-indicator-container > .ag-sort-indicator-icon.ag-sort-descending-icon > .ag-icon").click()` | | | |
| ].2 | Click on the ascending sort icon in the column header to sort the column in ascending order. | `page.locator(".ag-cell-label-container.ag-header-cell-sorted-asc > .ag-header-cell-label > .ag-sort-indicator-container > .ag-sort-indicator-icon.ag-sort-ascending-icon > .ag-icon").click()` | | | |
| ].3 | Click on the 'System Forecast Base (Plan Week)' column header to select it. | `page.get_by_text("System Forecast Base (Plan Week)").click()` | | | |
| ].4 | Click on the descending sort icon in the column header to sort the column in descending order again. | `page.locator(".ag-cell-label-container.ag-header-cell-sorted-desc > .ag-header-cell-label > .ag-sort-indicator-container > .ag-sort-indicator-icon.ag-sort-descending-icon > .ag-icon").click()` | | | |
| ].5 | Click on the descending sort icon in the column header to toggle the sorting order. | `page.locator(".ag-cell-label-container.ag-header-cell-sorted-desc > .ag-header-cell-label > .ag-sort-indicator-container > .ag-sort-indicator-icon.ag-sort-descending-icon > .ag-icon").click()` | | | |
```
```
| | **--- FILTER MENU INTERACTION ---** | | | | |
| ^.1 | Click on the filter button in the column header to open the filter menu. | `page.locator(".ag-header-icon.ag-header-cell-filter-button.ag-has-popup-positioned-under > .ag-icon").click()` | | | |
| ^.2 | Click on the filter body wrapper to open the advanced filtering options. | `page.locator(".ag-filter-body-wrapper").click()` | | | |
| ^.3 | Click on the 'Filtering operator' dropdown to select a filtering condition. | `page.get_by_role("combobox", name="Filtering operator").click()` | | | |
```
```markdown
| | **--- FILTERING OPERATOR SELECTION ---** | | | | |
| _.1 | Select the 'Equals' option from the filtering operator dropdown by clicking on the corresponding text. | `page.get_by_label("Select Field").get_by_text("Equals").click()` | | | |
| _.2 | Confirm the selection of the 'Equals' option by clicking on the displayed text again. | `page.get_by_text("Equals").click()` | | | |
| _.3 | Select the 'Does not equal' option from the filtering operator dropdown by clicking on the corresponding text. | `page.get_by_text("Does not equal").click()` | | | |
| _.4 | Confirm the selection of the 'Does not equal' option by clicking on the displayed text again. | `page.get_by_text("Does not equal").click()` | | | |
| _.5 | Select the 'Greater than' option from the filtering operator dropdown by clicking on the exact matching option. | `page.get_by_role("option", name="Greater than", exact=True).click()` | | | |
| _.6 | Confirm the selection of the 'Greater than' option by clicking on the displayed text again. | `page.get_by_text("Greater than").click()` | | | |
| _.7 | Select the 'Less than' option from the filtering operator dropdown by clicking on the exact matching option. | `page.get_by_role("option", name="Less than", exact=True).click()` | | | |
| _.8 | Confirm the selection of the 'Less than' option by clicking on the displayed text again. | `page.get_by_text("Less than").click()` | | | |
| _.9 | Select the 'Greater than or equal to' option from the filtering operator dropdown by clicking on the corresponding text. | `page.get_by_text("Greater than or equal to").click()` | | | |
```
```markdown
| | **--- FILTER OPERATOR SELECTION ---** | | | | |
| _.10 | Confirm the selection of the 'Greater than or equal to' option by clicking on the displayed text again. | `page.get_by_text("Greater than or equal to").click()` | | | |
| _.11 | Select the 'Less than or equal to' option from the filtering operator dropdown by clicking on the exact matching option. | `page.get_by_role("option", name="Less than or equal to").click()` | | | |
| _.12 | Confirm the selection of the 'Less than or equal to' option by clicking on the displayed text again. | `page.get_by_text("Less than or equal to").click()` | | | |
| _.13 | Select the 'Between' option from the filtering operator dropdown by clicking on the exact matching option. | `page.get_by_role("option", name="Between").click()` | | | |
| _.14 | Confirm the selection of the 'Between' option by clicking on the displayed text again. | `page.get_by_text("Between").click()` | | | |
| _.15 | Select the 'Blank' option from the filtering operator dropdown by clicking on the exact matching option. | `page.get_by_role("option", name="Blank", exact=True).click()` | | | |
| _.16 | Confirm the selection of the 'Blank' option by clicking on the displayed text again. | `page.get_by_text("Blank").click()` | | | |
| _.17 | Select the 'Not blank' option from the filtering operator dropdown by clicking on the exact matching option. | `page.get_by_role("option", name="Not blank").click()` | | | |
```
```markdown
| | **--- FILTER CONDITION AND VALUE INPUT ---** | | | | |
| a.1 | Click on the 'AND' radio button to set the filter condition to 'AND'. | `page.locator(".ag-labeled.ag-label-align-right.ag-radio-button").first.click()` | | | |
| a.2 | Click on the 'OR' radio button to set the filter condition to 'OR'. | `page.locator(".ag-labeled.ag-label-align-right.ag-radio-button.ag-input-field.ag-filter-condition-operator.ag-filter-condition-operator-or").click()` | | | |
| a.3 | Click on the 'Filter Value' input field to prepare for entering a value for filtering. | `page.get_by_role("spinbutton", name="Filter Value").click()` | | | |
| a.4 | Enter the value '2' into the 'Filter Value' input field. | `page.get_by_role("spinbutton", name="Filter Value").fill("2")` | | | |
| a.5 | Press 'Enter' to apply the entered filter value. | `page.get_by_role("spinbutton", name="Filter Value").press("Enter")` | | | |
```
```markdown
| | **--- FILTER APPLICATION AND RESET ---** | | | | |
| b.1 | Click on the 'Filter Value' input field to prepare for applying the filter criteria. | `page.get_by_role("spinbutton", name="Filter Value").click()` | | | |
| b.2 | Click on the 'Apply' button to apply the selected filter criteria. | `page.get_by_role("button", name="Apply").click()` | | | |
| b.3 | Click on the active filter icon to open the filter options for the column. | `page.locator(".ag-header-icon.ag-header-cell-filter-button.ag-filter-active > .ag-icon").click()` | | | |
| b.4 | Click on the 'Reset' button to reset the filter settings to their default state. | `page.get_by_role("button", name="Reset").click()` | | | |
```
```markdown
| | **--- COLUMN AND FILTER OPTIONS ---** | | | | |
| c.1 | Click on the column header icon to open sorting or additional options for the column. | `page.locator(".ag-header-cell.ag-header-parent-hidden.ag-header-cell-sortable.ag-header-background.ag-focus-managed.ag-header-active > .ag-header-cell-comp-wrapper > .ag-cell-label-container > .ag-header-icon > .ag-icon").click()` | | | |
| c.2 | Click on the 'Clear' button to remove all applied filters from the column. | `page.get_by_role("button", name="Clear").click()` | | | |
| c.3 | Click on the 'Customers columns (0)' text to open the column options. | `page.get_by_text("Customers columns (0)").click()` | | | |
```
```markdown
| | **--- PAGINATION INTERACTION ---** | | | | |
| d.1 | Click on the pagination element to interact with the pagination controls. | `page.locator("esp-row-dimentional-grid #paginationId").click()` | | | |
| d.2 | Click on the 'Showing 10 out of' text to view the current row display information. | `page.get_by_text("Showing 10 out of").click()` | | | |
| d.3 | Click on the 'Showing 10 out of 138 12345' text to view detailed row display information. | `page.get_by_text("Showing 10 out of 138 12345").click()` | | | |
| d.4 | Click on the 'View 10 row(s)' option to set the number of rows displayed to 10. | `page.get_by_text("View 10 row(s)").first.click()` | | | |
| d.5 | Click on the 'View 10 row(s)' option using a text filter to set the number of rows displayed to 10. | `page.locator("span").filter(has_text=re.compile(r"^View 10 row\(s\)$")).click()` | | | |
| d.6 | Click on the 'Rows per page' text to open the dropdown for selecting the number of rows displayed per page. | `page.get_by_text("Rows per page").click()` | | | |
| d.7 | Click on the list item with the text '1' to navigate to the first page of the pagination. | `page.get_by_role("listitem").filter(has_text=re.compile(r"^1$")).click()` | | | |
| d.8 | Click on the pagination link with the text '2' to navigate to the second page. | `page.locator("a").filter(has_text="2").click()` | | | |
| d.9 | Click on the left chevron icon to navigate to the previous page in the pagination. | `page.locator(".zeb-chevron-left").click()` | | | |
| d.10 | Click on the '12345...14' text to view additional pagination details. | `page.get_by_text("12345...14").click()` | | | |
| d.11 | Click on the '12345...14' text again to confirm pagination details. | `page.get_by_text("12345...14").click()` | | | |
| d.12 | Click on the right chevron icon to navigate to the next page in the pagination. | `page.locator(".pagination-next > .zeb-chevron-right").click()` | | | |
| d.13 | Click on the 'Last' navigation button to navigate to the last page in the pagination. | `page.locator(".zeb-nav-to-last").click()` | | | |
| d.14 | Click on the 'Showing 10 out of 138 12345' text again to verify the current row display information. | `page.get_by_text("Showing 10 out of 138 12345").click()` | | | |
```
```markdown
| | **--- ROW DISPLAY ADJUSTMENT ---** | | | | |
| e.1 | Click on the 'View 20 row(s)' option to set the number of rows displayed to 20. | `page.locator(".w-100.p-h-16").click()` | | | |
```
```markdown
| | **--- ROW DISPLAY AND SELECTION ---** | | | | |
| f.1 | Click on the 'View 20 row(s)' option to set the number of rows displayed to 20. | `page.locator("div").filter(has_text=re.compile(r"^View 20 row\(s\)$")).first.click()` | | | |
| f.2 | Click on the 'Showing 20 out of' text to confirm the updated row display information. | `page.get_by_text("Showing 20 out of").click()` | | | |
| f.3 | Select the grid cell labeled 'Press Space to toggle row selection (unchecked)' for the row '3RD PARTY DISTRIB'. | `page.get_by_role("gridcell", name="Press Space to toggle row selection (unchecked)  3RD PARTY DISTRIB").get_by_label("Press Space to toggle row").check()` | | | |
```
```markdown
| | **--- FILTER OPTIONS INTERACTION ---** | | | | |
| g.1 | Click on the 'FilterTime Latest Order &' text to open the filter options. | `page.get_by_text("FilterTime Latest Order &").click()` | | | |
| g.2 | Click on the 'Filter' button within a div element to apply or modify filters. | `page.locator("div").filter(has_text=re.compile(r"^Filter$")).click()` | | | |
| g.3 | Click on the 'Time' text to select the time filter option. | `page.get_by_text("Time").click()` | | | |
| g.4 | Click on the dropdown labeled '.w-100.p-h-16.p-v-8.dropdown-label.background-white' to open the filter options. | `page.locator(".w-100.p-h-16.p-v-8.dropdown-label.background-white").click()` | | | |
| g.5 | Select the filter option labeled 'Latest Order & Plan Week' from the dropdown. | `page.locator("span").filter(has_text="Latest Order & Plan Week").click()` | | | |
| g.6 | Click on the 'FilterTime Latest Order &' text again to confirm or apply the selected filter. | `page.get_by_text("FilterTime Latest Order &").click()` | | | |
```
```markdown
| | **--- DAILY SUMMARY NAVIGATION ---** | | | | |
| h.1 | Click on the 'Daily Summary Customer:3RD' text to navigate to the daily summary for the specified customer. | `page.get_by_text("Daily Summary Customer:3RD").click()` | | | |
| h.2 | Click on the 'Daily Summary' text to view the daily summary section. | `page.get_by_text("Daily Summary").click()` | | | |
| h.3 | Click on the 'Customer' text (exact match) to interact with the customer-specific options. | `page.get_by_text("Customer", exact=True).nth(2).click()` | | | |
| h.4 | Click on the 'Customer:3RD PARTY DISTRIB' text to select the specific customer. | `page.get_by_text("Customer:3RD PARTY DISTRIB").first.click()` | | | |
| h.5 | Click on the '3RD PARTY DISTRIB' text (second occurrence) to confirm or refine the selection. | `page.get_by_text("3RD PARTY DISTRIB").nth(1).click()` | | | |
```
```markdown
| | **--- DROPDOWN SELECTION AND CONFIRMATION ---** | | | | |
| i.1 | Click on the dropdown to open the list of options for selection. | `page.locator(".wr-20.font-weight-normal > esp-multiselect-dropdown > .multiselect-dropdown > div > .w-100").click()` | | | |
| i.2 | Select the first option from the dropdown list. | `page.locator(".d-flex.dropdown-option").first.click()` | | | |
| i.3 | Re-select the first option from the dropdown list, possibly to confirm the selection. | `page.locator(".d-flex.dropdown-option").first.click()` | | | |
| i.4 | Click on a specific dropdown option with additional alignment and padding styles. | `page.locator(".d-flex.dropdown-option.align-items-center.p-v-5.p-l-32 > .d-flex").first.click()` | | | |
| i.5 | Click on the first checkbox to select it. | `page.locator(".d-flex.flex-column.justify-content-center.font-size-10.align-items-center.checkbox-v2.m-r-10.zeb-check").first.click()` | | | |
| i.6 | Click on the first checkbox again, possibly to toggle or confirm the selection. | `page.locator(".d-flex.flex-column.justify-content-center.font-size-10.align-items-center.checkbox-v2.m-r-10.zeb-check").first.click()` | | | |
| i.7 | Click on the first checkbox again, possibly as part of a repeated action. | `page.locator(".d-flex.flex-column.justify-content-center.font-size-10.align-items-center.checkbox-v2.m-r-10.zeb-check").first.click()` | | | |
| i.8 | Click on the first checkbox again, possibly as part of a repeated action. | `page.locator(".d-flex.flex-column.justify-content-center.font-size-10.align-items-center.checkbox-v2.m-r-10.zeb-check").first.click()` | | | |
| i.9 | Click on the first checkbox again, possibly as part of a repeated action. | `page.locator(".d-flex.flex-column.justify-content-center.font-size-10.align-items-center.checkbox-v2.m-r-10.zeb-check").first.click()` | | | |
| i.10 | Click on the first checkbox again, possibly as part of a repeated action. | `page.locator(".d-flex.flex-column.justify-content-center.font-size-10.align-items-center.checkbox-v2.m-r-10.zeb-check").first.click()` | | | |
| i.11 | Click on the first checkbox again, possibly as part of a repeated action. | `page.locator(".d-flex.flex-column.justify-content-center.font-size-10.align-items-center.checkbox-v2.m-r-10.zeb-check").first.click()` | | | |
| i.12 | Click on the first checkbox again, possibly as part of a repeated action. | `page.locator(".d-flex.flex-column.justify-content-center.font-size-10.align-items-center.checkbox-v2.m-r-10.zeb-check").first.click()` | | | |
| i.13 | Click on the first checkbox again, possibly as part of a repeated action. | `page.locator(".d-flex.flex-column.justify-content-center.font-size-10.align-items-center.checkbox-v2.m-r-10.zeb-check").first.click()` | | | |
| i.14 | Click on the first checkbox again, possibly as part of a repeated action. | `page.locator(".d-flex.flex-column.justify-content-center.font-size-10.align-items-center.checkbox-v2.m-r-10.zeb-check").first.click()` | | | |
| i.15 | Click on the first checkbox again, possibly as part of a repeated action. | `page.locator(".d-flex.flex-column.justify-content-center.font-size-10.align-items-center.checkbox-v2.m-r-10.zeb-check").first.click()` | | | |
| i.16 | Click on the first checkbox again, possibly as part of a repeated action. | `page.locator(".d-flex.flex-column.justify-content-center.font-size-10.align-items-center.checkbox-v2.m-r-10.zeb-check").first.click()` | | | |
| i.17 | Click on the first checkbox again, possibly as part of a repeated action. | `page.locator(".d-flex.flex-column.justify-content-center.font-size-10.align-items-center.checkbox-v2.m-r-10.zeb-check").first.click()` | | | |
| i.18 | Click on a selected dropdown option to finalize or confirm the selection. | `page.locator(".d-flex.dropdown-option.align-items-center.p-v-5.p-l-32.p-r-16.selected").first.click()` | | | |
```
```markdown
| | **--- SPECIFIC OPTION SELECTION ---** | | | | |
| j.1 | Click on the 'Aged Net Units (CW-5)' option to select it from the dropdown. | `page.get_by_text("Aged Net Units (CW-5)", exact=True).click()` | | | |
| j.2 | Click on the 'Aged Net Units (CW-6)' option to select it from the dropdown. | `page.get_by_text("Aged Net Units (CW-6)", exact=True).click()` | | | |
| j.3 | Click on the 'Scan Units (CW-4)' option to select it from the dropdown. | `page.get_by_text("Scan Units (CW-4)", exact=True).click()` | | | |
```
```markdown
| | **--- DROPDOWN SELECTION AND NAVIGATION ---** | | | | |
| k.1 | Click on the 'Scan Units (CW-3)' option to select it from the dropdown. | `page.get_by_text("Scan Units (CW-3)").nth(1).click()` | | | |
| k.2 | Click on the 'Scan Units (CW-5)' option to select it from the dropdown. | `page.get_by_text("Scan Units (CW-5)", exact=True).click()` | | | |
| k.3 | Click on the 'Scan Units (CW-6)' option within a span element to select it. | `page.locator("span").filter(has_text="Scan Units (CW-6)").click()` | | | |
| k.4 | Click on the 'Daily Summary Customer:3RD' option to select it from the dropdown. | `page.get_by_text("Daily Summary Customer:3RD").click()` | | | |
| k.5 | Click on the button within the 'Daily Summary Customer:3RD' card to open its options. | `page.locator("esp-card-component").filter(has_text="Daily Summary Customer:3RD").get_by_role("button").click()` | | | |
```
```markdown
| | **--- COLUMN VISIBILITY MANAGEMENT ---** | | | | |
| l.1 | Click on the textbox labeled 'Filter Columns Input' to activate the column filter input field. | `page.get_by_role("textbox", name="Filter Columns Input").click()` | | | |
| l.2 | Uncheck the checkbox labeled 'Toggle All Columns Visibility' to hide all columns. | `page.get_by_role("checkbox", name="Toggle All Columns Visibility").uncheck()` | | | |
| l.3 | Check the checkbox labeled 'Toggle All Columns Visibility' to make all columns visible again. | `page.get_by_role("checkbox", name="Toggle All Columns Visibility").check()` | | | |
| l.4 | Click on the '/01(Sun)' label within the '/01(Sun) Column' to toggle its visibility. | `page.get_by_label("/01(Sun) Column").get_by_text("/01(Sun)").click()` | | | |
| l.5 | Click on the '/02(Mon)' label within the '/02(Mon) Column' to toggle its visibility. | `page.get_by_label("/02(Mon) Column").get_by_text("/02(Mon)").click()` | | | |
| l.6 | Uncheck the checkbox for the '/03(Tue) Column' to hide this column. | `page.get_by_role("treeitem", name="/03(Tue) Column").get_by_label("Press SPACE to toggle visibility (visible)").uncheck()` | | | |
| l.7 | Uncheck the checkbox for the '/05(Thu) Column' to hide this column. | `page.get_by_role("treeitem", name="/05(Thu) Column").get_by_label("Press SPACE to toggle visibility (visible)").uncheck()` | | | |
| l.8 | Uncheck the checkbox for the '/04(Wed) Column' to hide this column. | `page.get_by_role("treeitem", name="/04(Wed) Column").get_by_label("Press SPACE to toggle visibility (visible)").uncheck()` | | | |
```
```markdown
| | **--- FILE EXPORT AND PREFERENCES MANAGEMENT ---** | | | | |
| m.1 | Click on the export icon to initiate the download of the grid data. | `page.locator("span:nth-child(6) > esp-grid-icons-component > .display-grid-icons > div:nth-child(2) > #export-iconId > .icon-color-toolbar-active").click()` | | | |
| m.2 | Click on the preferences icon to open the preferences dropdown menu. | `page.locator("span:nth-child(6) > esp-grid-icons-component > .display-grid-icons > div:nth-child(3) > #preference-iconId > .legend-font > .multiselect-dropdown > .pointer").click()` | | | |
| m.3 | Select the 'Save Preference' option from the preferences dropdown to save the current grid settings. | `page.get_by_text("Save Preference").click()` | | | |
| m.4 | Click on the preferences icon again to reopen the preferences dropdown menu. | `page.locator("span:nth-child(6) > esp-grid-icons-component > .display-grid-icons > div:nth-child(3) > #preference-iconId > .legend-font > .multiselect-dropdown > .pointer").click()` | | | |
| m.5 | Select the 'Reset Preference' option from the preferences dropdown to reset the grid settings to default. | `page.get_by_text("Reset Preference").click()` | | | |
| m.6 | Click on the preferences icon once more to reopen the preferences dropdown menu. | `page.locator("span:nth-child(6) > esp-grid-icons-component > .display-grid-icons > div:nth-child(3) > #preference-iconId > .legend-font > .multiselect-dropdown > .pointer").click()` | | | |
```
```markdown
| | **--- FILTER AND GRID INTERACTION ---** | | | | |
| n.1 | Click on the button within the 'Daily Summary Customer:3RD' card to open the dropdown menu for further actions. | `page.locator("esp-card-component").filter(has_text="Daily Summary Customer:3RD").get_by_role("button").click()` | | | |
| n.2 | Click on the dropdown field to expand the multiselect options for filtering. | `page.locator(".wr-20.font-weight-normal > esp-multiselect-dropdown > .multiselect-dropdown > div > .w-100").click()` | | | |
| n.3 | Select the 'Select All' option to include all available items in the filter. | `page.get_by_text("Select All").click()` | | | |
| n.4 | Click on the 'Daily Summary Customer:3RD' option to specifically filter by this customer. | `page.get_by_text("Daily Summary Customer:3RD").click()` | | | |
| n.5 | Click on the header cell to interact with the first column in the grid. | `page.locator(".ag-header-cell.ag-column-first.ag-header-parent-hidden.ag-header-background.ag-focus-managed.ag-header-active > .ag-header-cell-comp-wrapper > .ag-cell-label-container > .ag-header-cell-label").click()` | | | |
| n.6 | Click on the 'User Suggested Order Total' column header to sort or interact with this column. | `page.get_by_text("User Suggested Order Total").click()` | | | |
| n.7 | Click on the first icon (likely a dropdown or action button) within the grid. | `page.locator("i").first.click()` | | | |
| n.8 | Click on the 'User Override Total' column header to sort or interact with this column. | `page.get_by_text("User Override Total").click()` | | | |
| n.9 | Click on the third icon (likely a dropdown or action button) within the grid. | `page.locator("i").nth(2).click()` | | | |
| n.10 | Click on the 'Gross Units (CW-3)' column header within the grid to interact with it. | `page.locator("esp-column-dimentional-grid").get_by_text("Gross Units (CW-3)").click()` | | | |
```
```markdown
| | **--- GRID INTERACTION AND EXPANSION ---** | | | | |
| o.1 | Click on the first 'Gross Units (CW-3)' text element to interact with it. | `page.locator("span").filter(has_text="Gross Units (CW-3)").first.click()` | | | |
| o.2 | Click on the sixth icon (likely a dropdown or action button) within the grid. | `page.locator("i").nth(5).click()` | | | |
| o.3 | Click on the 'Aged Net Units (CW-3)' column header within the grid to interact with it. | `page.locator("esp-column-dimentional-grid").get_by_text("Aged Net Units (CW-3)").click()` | | | |
| o.4 | Click on the expand/collapse icon within the last left-pinned cell of the grid to expand or collapse the row. | `page.locator(".ag-cell-value.ag-cell.ag-cell-not-inline-editing.ag-cell-normal-height.ag-cell-last-left-pinned.ag-column-first.ag-cell-override-normal.notosans-overwrite.no-border.ag-cell-focus > .ag-cell-wrapper > .ag-group-contracted > .zeb-chevron-right").click()` | | | |
| o.5 | Click on the expand icon (chevron) in the first row of the grid to expand the group. | `page.locator(".ag-row-no-focus.ag-row-not-inline-editing.ag-row.ag-row-level-0.ag-row-group.ag-row-group-contracted.ag-row-position-absolute.ag-row-even.ag-row-hover > .ag-cell-value > .ag-cell-wrapper > .ag-group-contracted > .zeb-chevron-right").click()` | | | |
```
```markdown
| | **--- COLUMN AND TREND ANALYSIS INTERACTION ---** | | | | |
| p.1 | Click on the 'Scan Units (CW-3)' column header within the grid to interact with it. | `page.locator("esp-column-dimentional-grid").get_by_text("Scan Units (CW-3)").click()` | | | |
| p.2 | Click on the 'Daily Trend Customer:3RD' text element to interact with the trend analysis for this customer. | `page.get_by_text("Daily Trend Customer:3RD").click()` | | | |
```
```markdown
| | **--- CHART AND GRAPHICAL ELEMENT INTERACTION ---** | | | | |
| q.1 | Click on the SVG element within the chart to interact with or highlight a graphical component. | `page.locator("svg").click()` | | | |
| q.2 | Click on the title element with the class 'title-color' to navigate to or interact with a specific section. | `page.locator(".title.d-flex.align-items-center.font-size-16.font-weight-bold.nunito.title-color > .p-l-40").click()` | | | |
| q.3 | Click on the 'Customer' label within the line-bar chart to filter or interact with customer-specific data. | `page.locator("dp-line-bar-chart").get_by_text("Customer", exact=True).click()` | | | |
| q.4 | Click on the 'Customer:3RD PARTY DISTRIB' label within the line-bar chart to filter or interact with this specific customer data. | `page.locator("dp-line-bar-chart").get_by_text("Customer:3RD PARTY DISTRIB").click()` | | | |
| q.5 | Click on the specific path element within the chart to highlight or interact with a particular data point. | `page.locator("path:nth-child(79)").click()` | | | |
```
```markdown
| | **--- USER SUGGESTED AND OVERRIDE INTERACTION ---** | | | | |
| r.1 | Click on the first occurrence of the 'User Suggested Order Base' text to interact with it. | `page.get_by_text("User Suggested Order Base,").first.click()` | | | |
| r.2 | Click on the 'User Suggested Order Base' text element to interact with it. | `page.locator("span").filter(has_text="User Suggested Order Base").click()` | | | |
| r.3 | Click on the 'User Suggested Order Promotion' text element to interact with it. | `page.locator("span").filter(has_text="User Suggested Order Promotion").click()` | | | |
| r.4 | Click on the 'User Override Base' text element to interact with it. | `page.locator("span").filter(has_text="User Override Base").click()` | | | |
| r.5 | Click on the 'User Override Promotion' text element to interact with it. | `page.locator("span").filter(has_text="User Override Promotion").click()` | | | |
```
```markdown
| | **--- LINE-BAR CHART INTERACTION ---** | | | | |
| s.1 | Click on the 'Gross Units (CW-3)' text element within the line-bar chart to interact with it. | `page.locator("dp-line-bar-chart span").filter(has_text="Gross Units (CW-3)").click()` | | | |
| s.2 | Click on the 'Gross Units (CW-4)' text element within the line-bar chart to interact with it. | `page.locator("dp-line-bar-chart").get_by_text("Gross Units (CW-4)").click()` | | | |
| s.3 | Click on the seventh div element within the overflow container to interact with it. | `page.locator(".overflow-auto > div:nth-child(7)").click()` | | | |
| s.4 | Click on the eighth div element with a flex layout to interact with it. | `page.locator("div:nth-child(8) > .d-flex").click()` | | | |
| s.5 | Click on the ninth div element within the overflow container to interact with it. | `page.locator(".overflow-auto > div:nth-child(9)").click()` | | | |
| s.6 | Click on the tenth div element with a flex layout to interact with it. | `page.locator("div:nth-child(10) > .d-flex").click()` | | | |
| s.7 | Click on the 'Aged Net Units (CW-5)' text element within the line-bar chart to interact with it. | `page.locator("dp-line-bar-chart").get_by_text("Aged Net Units (CW-5)").click()` | | | |
| s.8 | Click on the 'Aged Net Units (CW-6)' text element within the line-bar chart to interact with it. | `page.locator("dp-line-bar-chart").get_by_text("Aged Net Units (CW-6)").click()` | | | |
| s.9 | Click on the 'Scan Units (CW-3)' text element within the line-bar chart to interact with it. | `page.locator("dp-line-bar-chart span").filter(has_text="Scan Units (CW-3)").click()` | | | |
| s.10 | Click on the 'Scan Units (CW-4)' text element within the line-bar chart to interact with it. | `page.locator("dp-line-bar-chart").get_by_text("Scan Units (CW-4)").click()` | | | |
| s.11 | Click on the fifteenth div element within the overflow container to interact with it. | `page.locator(".overflow-auto > div:nth-child(15)").click()` | | | |
| s.12 | Click on the 'Scan Units (CW-6)' text element within the line-bar chart to interact with it. | `page.locator("dp-line-bar-chart").get_by_text("Scan Units (CW-6)").click()` | | | |
```
```markdown
| | **--- DROPDOWN INTERACTION ---** | | | | |
| t.1 | Click on the dropdown element within the ellipses container to interact with the multiselect options. | `page.locator(".ellipses > esp-multiselect-dropdown > .multiselect-dropdown > div > .w-100").click()` | | | |
```
```markdown
| | **--- CUSTOMER TREND INTERACTION ---** | | | | |
| u.1 | Click on the 'Daily Trend Customer:3RD' text element to interact with the trend analysis for this customer. | `page.get_by_text("Daily Trend Customer:3RD").click()` | | | |
```
```markdown
| | **--- PREFERENCE MANAGEMENT ---** | | | | |
| v.1 | Click on the preference icon within the grid icons container to open the preferences dropdown. | `page.locator(".title.d-flex.align-items-center.font-size-16.font-weight-bold.nunito.title-color > .grid-icons-container > esp-grid-icons-component > .display-grid-icons > div > #preference-iconId > .legend-font > .multiselect-dropdown > .pointer").click()` | | | |
| v.2 | Click on the 'Save Preference' option to save the current preferences. | `page.get_by_text("Save Preference").click()` | | | |
| v.3 | Click on the preference icon again to open the preferences dropdown. | `page.locator(".title.d-flex.align-items-center.font-size-16.font-weight-bold.nunito.title-color > .grid-icons-container > esp-grid-icons-component > .display-grid-icons > div > #preference-iconId > .legend-font > .multiselect-dropdown > .pointer").click()` | | | |
| v.4 | Click on the 'Reset Preference' option to reset the preferences to default. | `page.get_by_text("Reset Preference").click()` | | | |
```
```markdown
| | **--- DATE SELECTION IN SVG ---** | | | | |
| w.1 | Click on the SVG element to interact with the graphical chart or element. | `page.locator("svg").click()` | | | |
| w.2 | Click on the '02/01/' text within the SVG element to select the specific date. | `page.locator("svg").get_by_text("02/01/").click()` | | | |
| w.3 | Click on the '02/02/' text to select another specific date. | `page.get_by_text("02/02/").click()` | | | |
| w.4 | Click on the '02/03/' text to select another specific date. | `page.get_by_text("02/03/").click()` | | | |
```
```markdown
| | **--- SVG PATH INTERACTION ---** | | | | |
| x.1 | Click on the SVG element to interact with the graphical chart or element. | `page.locator("svg").click()` | | | |
| x.2 | Click on the 67th path element within the SVG to interact with a specific data point. | `page.locator("path:nth-child(67)").click()` | | | |
| x.3 | Click on the 'User Override Promotion' text element to interact with it. | `page.get_by_text("User Override Promotion", exact=True).click()` | | | |
| x.4 | Click on the 'User Override Base' text element to interact with it. | `page.get_by_text("User Override Base", exact=True).click()` | | | |
| x.5 | Click on the 79th path element within the SVG to interact with a specific data point. | `page.locator("path:nth-child(79)").click()` | | | |
| x.6 | Click on the 96th path element within the SVG to interact with a specific data point. | `page.locator("path:nth-child(96)").click()` | | | |
| x.7 | Click on the 102nd path element within the SVG to interact with a specific data point. | `page.locator("path:nth-child(102)").click()` | | | |
| x.8 | Click on the SVG element again to interact with the graphical chart or element. | `page.locator("svg").click()` | | | |
| x.9 | Click on the 102nd path element within the SVG again to interact with the same data point. | `page.locator("path:nth-child(102)").click()` | | | |
```
