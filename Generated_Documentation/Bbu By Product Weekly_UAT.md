# Feature: Bbu By Product Weekly
**Tab Location:** Main Workspace

## Detailed User Interaction Flows

| Use Case ID | Test Case Description | Exact Locator | Pass/Fail | Notes | Issues |
|:---|:---|:---|:---|:---|:---|
```markdown
| | **--- NAVIGATE TO EXECUTIVE DASHBOARD ---** | | | | |
| C.1 | Open the 'Executive Dashboard' by navigating to the specified URL in the demand planning application. | `page.goto("https://stage.bbu.esp.antuit.ai/dp/demand-planning/executive-dashboard?workbookId=4&tabIndex=2")` | | | |
```
```markdown
| | **--- COLUMN CONFIGURATION - INITIAL ADJUSTMENTS ---** | | | | |
| D.1 | Click on the 'Product Total columns (0)' button to open the column configuration panel. | `page.locator("esp-card-component").filter(has_text="Product Total columns (0)").get_by_role("button").click()` | | | |
| D.2 | Uncheck the 'System Forecast Total (Plan Week)' column to hide it from the view. | `page.get_by_role("treeitem", name="System Forecast Total (Plan Week) Column").get_by_label("Press SPACE to toggle").uncheck()` | | | |
| D.3 | Uncheck the 'System Forecast Base (Plan)' column to hide it from the view. | `page.get_by_role("treeitem", name="System Forecast Base (Plan").get_by_label("Press SPACE to toggle").uncheck()` | | | |
| D.4 | Uncheck the 'System Forecast Promotion (' column to hide it from the view. | `page.get_by_role("treeitem", name="System Forecast Promotion (").get_by_label("Press SPACE to toggle").uncheck()` | | | |
| D.5 | Click on the third column selector in the configuration panel to modify its settings. | `page.locator("div:nth-child(3) > .ag-column-select-column").click()` | | | |
| D.6 | Uncheck the 'System Forecast Promotion (' column again to ensure it is hidden. | `page.get_by_role("treeitem", name="System Forecast Promotion (").get_by_label("Press SPACE to toggle").uncheck()` | | | |
```
```markdown
| | **--- TOGGLE ALL COLUMNS VISIBILITY ---** | | | | |
| E.1 | Check the 'Toggle All Columns Visibility' checkbox to make all columns visible. | `page.get_by_role("checkbox", name="Toggle All Columns Visibility").check()` | | | |
```
```markdown
| | **--- SAVE PREFERENCES AND DOWNLOAD FILE ---** | | | | |
| F.1 | Click on the first adjustment option to apply changes to the column configuration. | `page.locator(".pointer.zeb-adjustments").first.click()` | | | |
| F.2 | Click on the 'Save Preference' button to save the updated column configuration. | `page.locator("div").filter(has_text=re.compile(r"^Save Preference$")).nth(1).click()` | | | |
| F.3 | Click on the first download button to initiate the file download and capture the downloaded file information for validation. | `page.locator(".icon-color-toolbar-active.zeb-download-underline").first.click()` | | | |
```
```markdown
| | **--- RESET PREFERENCES AND NAVIGATE TO PRODUCTS TAB ---** | | | | |
| G.1 | Click on the first adjustments button to open the adjustments menu. Look for the button identified by the '.pointer.zeb-adjustments' class. | `page.locator(".pointer.zeb-adjustments").first.click()` | | | |
| G.2 | Click on the 'Reset Preference' option to reset the preferences to their default state. Locate the option by its visible text. | `page.get_by_text("Reset Preference").click()` | | | |
| G.3 | Click on the 'Products' tab to navigate to the product configuration section. Locate the tab by its visible text. | `page.get_by_text("Products").click()` | | | |
```
```markdown
| | **--- PRODUCTS COLUMN CONFIGURATION ---** | | | | |
| H.1 | Open the 'Products columns' configuration menu by clicking the button within the 'esp-card-component' element labeled 'Products columns (0)'. | `page.locator("esp-card-component").filter(has_text="Products columns (0)").get_by_role("button").click()` | | | |
| H.2 | Uncheck the 'Toggle All Columns Visibility' checkbox to hide all columns initially. Locate the checkbox by its name. | `page.get_by_role("checkbox", name="Toggle All Columns Visibility").uncheck()` | | | |
| H.3 | Enable visibility for the 'System Forecast Total (Plan Week)' column by checking its corresponding checkbox. Locate the checkbox by its label. | `page.get_by_role("treeitem", name="System Forecast Total (Plan Week) Column").get_by_label("Press SPACE to toggle visibility (hidden)").check()` | | | |
| H.4 | Enable visibility for the 'System Forecast Base (Plan Week)' column by checking its corresponding checkbox. Locate the checkbox by its label. | `page.get_by_role("treeitem", name="System Forecast Base (Plan Week) Column").get_by_label("Press SPACE to toggle visibility (hidden)").check()` | | | |
| H.5 | Enable visibility for the 'System Forecast Promotion (Plan Week)' column by checking its corresponding checkbox. Locate the checkbox by its label. | `page.get_by_role("treeitem", name="System Forecast Promotion (Plan Week) Column").get_by_label("Press SPACE to toggle visibility (hidden)").check()` | | | |
| H.6 | Enable visibility for the 'System Forecast Total (Plan+1)' column by checking its corresponding checkbox. Locate the checkbox by its label. | `page.get_by_role("treeitem", name="System Forecast Total (Plan+1").get_by_label("Press SPACE to toggle visibility (hidden)").check()` | | | |
| H.7 | Enable visibility for the 'System Forecast Base (Plan+1)' column by checking its corresponding checkbox. Locate the checkbox by its label. | `page.get_by_role("treeitem", name="System Forecast Base (Plan+1").get_by_label("Press SPACE to toggle visibility (hidden)").check()` | | | |
| H.8 | Enable visibility for the 'System Forecast Promotion (Plan+1 Week)' column by checking its corresponding checkbox. Locate the checkbox by its label. | `page.get_by_role("treeitem", name="System Forecast Promotion (Plan+1 Week) Column").get_by_label("Press SPACE to toggle visibility (hidden)").check()` | | | |
```
```markdown
| | **--- COLUMN VISIBILITY MANAGEMENT ---** | | | | |
| I.1 | Enable visibility for the 'Week Gross Units Average' column by checking its corresponding checkbox. Locate the checkbox by its label. | `page.get_by_role("treeitem", name="Week Gross Units Average Column").get_by_label("Press SPACE to toggle visibility (hidden)").check()` | | | |
| I.2 | Enable visibility for the '6 Week Aged Net Units Average' column by checking its corresponding checkbox. Locate the checkbox by its label. | `page.get_by_role("treeitem", name="6 Week Aged Net Units Average Column", exact=True).get_by_label("Press SPACE to toggle visibility (hidden)").check()` | | | |
| I.3 | Recheck the 'Toggle All Columns Visibility' checkbox to ensure all selected columns are visible. Locate the checkbox by its name. | `page.get_by_role("checkbox", name="Toggle All Columns Visibility").check()` | | | |
```
```markdown
| | **--- PREFERENCE MANAGEMENT ---** | | | | |
| J.1 | Open the preferences dropdown menu by clicking on the preferences icon to access options for saving or resetting preferences. | `page.locator("div:nth-child(3) > #preference-iconId > .legend-font > .multiselect-dropdown > .pointer").click()` | | | |
| J.2 | Select the 'Save Preference' option from the dropdown menu to save the current column visibility settings. | `page.locator("div").filter(has_text=re.compile(r"^Save Preference$")).nth(1).click()` | | | |
| J.3 | Reopen the preferences dropdown menu by clicking on the preferences icon to access the reset option. | `page.locator("div:nth-child(3) > #preference-iconId > .legend-font > .multiselect-dropdown > .pointer").click()` | | | |
| J.4 | Select the 'Reset Preference' option from the dropdown menu to revert to the default column visibility settings. | `page.get_by_text("Reset Preference").click()` | | | |
```
```markdown
| | **--- COLUMN FILTERING ---** | | | | |
| K.1 | Click on the filter icon in the column header to open the filter options for that column. | `page.locator(".ag-header-icon.ag-header-cell-filter-button > .ag-icon").first.click()` | | | |
| K.2 | Enter the filter value 'BARCEL' into the textbox to filter the column data based on the input. | `page.get_by_role("textbox", name="Filter Value").fill("BARCEL")` | | | |
| K.3 | Click on the 'Apply' button to apply the filter and update the displayed data in the column. | `page.get_by_role("button", name="Apply").click()` | | | |
| K.4 | Click on the filter icon in the column header again to reopen the filter options for further actions. | `page.locator(".ag-header-icon.ag-header-cell-filter-button > .ag-icon").first.click()` | | | |
| K.5 | Click on the 'Reset' button to clear the filter and revert the column data to its default state. | `page.get_by_role("button", name="Reset").click()` | | | |
```
```markdown
| | **--- ROW SELECTION AND PAGINATION ---** | | | | |
| L.1 | Select the row with the name 'ARNOLD-BRWNBRY-OROWT' by toggling the checkbox in the grid cell. | `page.get_by_role("gridcell", name="Press Space to toggle row selection (unchecked)  ARNOLD-BRWNBRY-OROWT").get_by_label("Press Space to toggle row").check()` | | | |
| L.2 | Navigate to the second page of the table by clicking on the pagination link labeled '2'. | `page.locator("a").filter(has_text="2").click()` | | | |
| L.3 | Navigate to the third page of the table by clicking on the pagination link labeled '3'. | `page.locator("a").filter(has_text="3").click()` | | | |
```
```markdown
| | **--- DROPDOWN AND ROW DISPLAY SETTINGS ---** | | | | |
| M.1 | Click on the fourth item in the list to select it. Ensure the correct item is highlighted after selection. | `page.get_by_role("listitem").filter(has_text=re.compile(r"^$")).nth(4).click()` | | | |
| M.2 | Open the dropdown menu by clicking on the first dropdown caret located on the left side of the screen. | `page.locator(".dropdown-caret.p-l-16").first.click()` | | | |
| M.3 | Adjust the number of rows displayed by selecting the 'View 20 row(s)' option from the dropdown menu. | `page.locator("div").filter(has_text=re.compile(r"^View 20 row\(s\)$")).nth(1).click()` | | | |
```
```markdown
| | **--- TIME FILTER SELECTION ---** | | | | |
| N.1 | Click on the 'Filter' button to open the filter options. | `page.get_by_text("Filter").click()` | | | |
| N.2 | Click on the dropdown caret within the filter section to open the time filter options. | `page.locator(".w-100.p-h-16.p-v-8.dropdown-label.background-white > .d-flex.align-items-center > .dropdown-caret").click()` | | | |
| N.3 | Select the 'Latest 5 Next 4' option from the time filter dropdown. | `page.locator("div").filter(has_text=re.compile(r"^Latest 5 Next 4$")).nth(1).click()` | | | |
| N.4 | Click on the dropdown caret within the filter section again to reopen the time filter options. | `page.locator(".w-100.p-h-16.p-v-8.dropdown-label.background-white > .d-flex.align-items-center > .dropdown-caret").click()` | | | |
| N.5 | Select the 'Latest 5 Next 12' option from the time filter dropdown. | `page.locator("div").filter(has_text=re.compile(r"^Latest 5 Next 12$")).nth(1).click()` | | | |
| N.6 | Click on the dropdown caret within the filter section again to reopen the time filter options. | `page.locator(".w-100.p-h-16.p-v-8.dropdown-label.background-white > .d-flex.align-items-center > .dropdown-caret").click()` | | | |
| N.7 | Select the 'Latest 13 Next 4' option from the time filter dropdown. | `page.locator("div").filter(has_text=re.compile(r"^Latest 13 Next 4$")).nth(1).click()` | | | |
| N.8 | Click on the dropdown caret within the filter section again to reopen the time filter options. | `page.locator(".w-100.p-h-16.p-v-8.dropdown-label.background-white > .d-flex.align-items-center > .dropdown-caret").click()` | | | |
| N.9 | Select the 'Latest 13 Next 12' option from the time filter dropdown. | `page.locator("div").filter(has_text=re.compile(r"^Latest 13 Next 12$")).nth(1).click()` | | | |
```
```markdown
| | **--- MULTI-SELECT DROPDOWN INTERACTION ---** | | | | |
| O.1 | Click on the dropdown caret to open the multi-select dropdown menu. | `page.locator(".wr-20.font-weight-normal > esp-multiselect-dropdown > .multiselect-dropdown > div > .w-100 > .d-flex.align-items-center > .dropdown-caret").click()` | | | |
| O.2 | Click on the first option in the dropdown menu to select it. The specific option is not clear from the screenshot. | `page.locator(".d-flex.flex-column.justify-content-center").first.click()` | | | |
| O.3 | Click on the first option under the 'dropdown-option' class to select it. The specific option is not clear from the screenshot. | `page.locator(".d-flex.dropdown-option.align-items-center.p-v-5.p-l-32 > .d-flex").first.click()` | | | |
```
```markdown
| | **--- DROPDOWN MENU OPTION SELECTION ---** | | | | |
| P.1 | Click on the second option in the dropdown menu to select it. The specific option is not clear from the screenshot. | `page.locator(".overflow-auto > div:nth-child(2) > .d-flex").click()` | | | |
| P.2 | Click on the third option in the dropdown menu to select it. The specific option is not clear from the screenshot. | `page.locator(".overflow-auto > div:nth-child(3) > .d-flex").click()` | | | |
| P.3 | Click on the fourth option in the dropdown menu to select it. The specific option is not clear from the screenshot. | `page.locator(".overflow-auto > div:nth-child(4)").click()` | | | |
| P.4 | Click on the fifth option in the dropdown menu to select it. The specific option is not clear from the screenshot. | `page.locator(".overflow-auto > div:nth-child(5)").click()` | | | |
| P.5 | Click on the sixth option in the dropdown menu to select it. The specific option is not clear from the screenshot. | `page.locator(".overflow-auto > div:nth-child(6)").click()` | | | |
| P.6 | Click on the first option in the dropdown menu again to deselect it. The specific option is not clear from the screenshot. | `page.locator(".d-flex.flex-column.justify-content-center").first.click()` | | | |
```
```markdown
| | **--- WEEKLY SUMMARY COLUMN VISIBILITY MANAGEMENT ---** | | | | |
| Q.1 | Click on the dropdown caret to open the multi-select dropdown menu for column visibility options. | `page.locator(".wr-20.font-weight-normal > esp-multiselect-dropdown > .multiselect-dropdown > div > .w-100 > .d-flex.align-items-center > .dropdown-caret").click()` | | | |
| Q.2 | Click on the button within the 'Weekly Summary Product:ARNOLD' card to expand or collapse the product details. | `page.locator("esp-card-component").filter(has_text="Weekly Summary Product:ARNOLD").get_by_role("button").click()` | | | |
| Q.3 | Uncheck the 'Toggle All Columns Visibility' checkbox to hide all columns in the Weekly Summary table. | `page.get_by_role("checkbox", name="Toggle All Columns Visibility").uncheck()` | | | |
| Q.4 | Check the visibility of the column labeled '-10-26 (44)' by toggling its checkbox. | `page.get_by_role("treeitem", name="-10-26 (44) Column").get_by_label("Press SPACE to toggle visibility (hidden)").check()` | | | |
| Q.5 | Check the visibility of the column labeled '-11-02 (45)' by toggling its checkbox. | `page.get_by_role("treeitem", name="-11-02 (45) Column").get_by_label("Press SPACE to toggle visibility (hidden)").check()` | | | |
| Q.6 | Check the visibility of the column labeled '-11-09 (46)' by toggling its checkbox. | `page.get_by_role("treeitem", name="-11-09 (46) Column").get_by_label("Press SPACE to toggle visibility (hidden)").check()` | | | |
| Q.7 | Check the visibility of the column labeled '-11-16 (47)' by toggling its checkbox. | `page.get_by_role("treeitem", name="-11-16 (47) Column").get_by_label("Press SPACE to toggle visibility (hidden)").check()` | | | |
| Q.8 | Recheck the 'Toggle All Columns Visibility' checkbox to make all columns visible again in the Weekly Summary table. | `page.get_by_role("checkbox", name="Toggle All Columns Visibility").check()` | | | |
| Q.9 | Click on the button within the 'Weekly Summary Product:ARNOLD' card again to collapse the product details. | `page.locator("esp-card-component").filter(has_text="Weekly Summary Product:ARNOLD").get_by_role("button").click()` | | | |
```
```markdown
| | **--- PREFERENCE MANAGEMENT AND EXPORT ---** | | | | |
| R.1 | Click on the 'Preference' icon to open the dropdown menu for managing preferences. | `page.locator("div:nth-child(4) > #preference-iconId > .legend-font > .multiselect-dropdown > .pointer").click()` | | | |
| R.2 | Click on the 'Save Preference' button to save the current table preferences. | `page.get_by_text("Save Preference").click()` | | | |
| R.3 | Click on the 'Export' icon to initiate the export process for the table data. | `page.locator("div:nth-child(3) > #export-iconId > .icon-color-toolbar-active").click()` | | | |
```
```markdown
| | **--- RESET PREFERENCES AND DATE SELECTION ---** | | | | |
| S.1 | Click on the 'Preference' dropdown to open the menu for managing preferences. | `page.locator("div:nth-child(4) > #preference-iconId > .legend-font > .multiselect-dropdown > .pointer").click()` | | | |
| S.2 | Select 'Reset Preference' from the dropdown to reset the table preferences to default. | `page.get_by_text("Reset Preference").click()` | | | |
| S.3 | Click on the date '-02-15 (08)' to select it from the available options. | `page.get_by_text("-02-15 (08)").click()` | | | |
```
```markdown
| | **--- EVENT DETAILS COLUMN VISIBILITY MANAGEMENT ---** | | | | |
| T.1 | Click on the fifth image element to open the column visibility settings for 'Event Details'. | `page.get_by_role("img").nth(5).click()` | | | |
| T.2 | Click on the button within the 'Event Details columns (0)' card to access the column visibility options. | `page.locator("esp-card-component").filter(has_text="Event Details columns (0)").get_by_role("button").click()` | | | |
| T.3 | Uncheck the 'Event Column' to hide it from the table. | `page.get_by_role("treeitem", name="Event Column").get_by_label("Press SPACE to toggle visibility (visible)").uncheck()` | | | |
| T.4 | Uncheck the 'UPC 12 Column' to hide it from the table. | `page.get_by_role("treeitem", name="UPC 12 Column").get_by_label("Press SPACE to toggle visibility (visible)").uncheck()` | | | |
| T.5 | Uncheck the 'Customer Level 2 Column' to hide it from the table. | `page.get_by_role("treeitem", name="Customer Level 2 Column").get_by_label("Press SPACE to toggle visibility (visible)").uncheck()` | | | |
| T.6 | Uncheck the 'Start Date Column' to hide it from the table. | `page.get_by_role("treeitem", name="Start Date Column").get_by_label("Press SPACE to toggle visibility (visible)").uncheck()` | | | |
| T.7 | Uncheck the 'End Date Column' to hide it from the table. | `page.get_by_role("treeitem", name="End Date Column").get_by_label("Press SPACE to toggle visibility (visible)").uncheck()` | | | |
```
```markdown
| | **--- TOGGLE ALL COLUMNS VISIBILITY AND SAVE PREFERENCES ---** | | | | |
| U.1 | Check the 'Toggle All Columns Visibility' checkbox to make all columns visible again. | `page.get_by_role("checkbox", name="Toggle All Columns Visibility").check()` | | | |
| U.2 | Click on the 'Preference' icon to open the dropdown menu for saving or resetting preferences. | `page.locator(".col-12.m-t-16 > div > esp-grid-container > esp-card-component > .card-container > .title > .grid-icons-container > esp-grid-icons-component > .display-grid-icons > div:nth-child(2) > #preference-iconId > .legend-font > .multiselect-dropdown > .pointer").click()` | | | |
| U.3 | Click on 'Save Preference' to save the current column visibility settings. | `page.get_by_text("Save Preference").click()` | | | |
```
```markdown
| | **--- EXPORT DATA WITH CURRENT PREFERENCES ---** | | | | |
| V.1 | Click on the 'Export' icon to export the data with the current preferences. | `page.locator("div:nth-child(6) > div > esp-grid-container > esp-card-component > .card-container > .title > .grid-icons-container > esp-grid-icons-component > .display-grid-icons > div > #export-iconId > .icon-color-toolbar-active").click()` | | | |
```
```markdown
| | **--- RESET PREFERENCES TO DEFAULT ---** | | | | |
| W.1 | Click on the 'Preference' icon to open the dropdown menu for resetting preferences. | `page.locator(".col-12.m-t-16 > div > esp-grid-container > esp-card-component > .card-container > .title > .grid-icons-container > esp-grid-icons-component > .display-grid-icons > div:nth-child(2) > #preference-iconId > .legend-font > .multiselect-dropdown > .pointer").click()` | | | |
| W.2 | Click on 'Reset Preference' to revert to the default column visibility settings. | `page.get_by_text("Reset Preference").click()` | | | |
```
```markdown
| | **--- APPLY AND RESET COLUMN FILTERS ---** | | | | |
| X.1 | Click on the filter icon in the column header to open the filter options. | `page.locator(".ag-header-cell.ag-header-parent-hidden.ag-header-cell-sortable.ag-header-background.ag-focus-managed.ag-header-active > .ag-header-cell-comp-wrapper > .ag-cell-label-container > .ag-header-icon > .ag-icon").click()` | | | |
| X.2 | Enter 'Scan Track' into the filter textbox to filter the data based on this value. | `page.get_by_role("textbox", name="Filter Value").fill("Scan Track")` | | | |
| X.3 | Click on the 'Apply' button to apply the filter and update the displayed data. | `page.get_by_role("button", name="Apply").click()` | | | |
| X.4 | Click on the active filter icon to open the filter options for resetting. | `page.locator(".ag-header-icon.ag-header-cell-filter-button.ag-filter-active > .ag-icon").click()` | | | |
| X.5 | Click on the 'Reset' button to clear the applied filter and restore the unfiltered data. | `page.get_by_role("button", name="Reset").click()` | | | |
```
```markdown
| | **--- DRILL DOWN AND DRILL UP NAVIGATION ---** | | | | |
| Y.1 | Click on the 'Products' tab to navigate to the product selection view. | `page.get_by_text("Products").click()` | | | |
| Y.2 | Double-click on the product 'ARNOLD-BRWNBRY-OROWT' to drill down into its details. | `page.locator("span").filter(has_text="ARNOLD-BRWNBRY-OROWT").first.dblclick()` | | | |
| Y.3 | Double-click on 'ABO COUNTRY' to further drill down into its details. | `page.locator("span").filter(has_text="ABO COUNTRY").first.dblclick()` | | | |
| Y.4 | Click on 'ABO COUNTRY' to select it. | `page.locator("span").filter(has_text="ABO COUNTRY").first.click()` | | | |
| Y.5 | Double-click on the second instance of 'ABO COUNTRY' to drill down further. | `page.get_by_text("ABO COUNTRY").nth(1).dblclick()` | | | |
| Y.6 | Right-click on the product 'OR CTY BTRMK WP 24Z-731300012500' to open the context menu. | `page.locator("span").filter(has_text=re.compile(r"^OR CTY BTRMK WP 24Z-731300012500$")).click(button="right")` | | | |
| Y.7 | Click on 'Drill up' from the context menu to navigate back to the previous level. | `page.get_by_text("Drill up").click()` | | | |
| Y.8 | Right-click on 'ABO COUNTRY' to open the context menu again. | `page.locator("span").filter(has_text="ABO COUNTRY").first.click(button="right")` | | | |
| Y.9 | Click on 'Drill up' from the context menu to navigate back another level. | `page.get_by_text("Drill up").click()` | | | |
| Y.10 | Right-click on 'ABO COUNTRY' to open the context menu once more. | `page.locator("span").filter(has_text="ABO COUNTRY").first.click(button="right")` | | | |
| Y.11 | Click on 'Drill up' from the context menu to return to the top level. | `page.get_by_text("Drill up").click()` | | | |
```
```markdown
| | **--- ROW SELECTION AND PAGE CLOSURE ---** | | | | |
| Z.1 | Select the row for the product 'ARNOLD-BRWNBRY-OROWT' by toggling the checkbox in the grid cell. | `page.get_by_role("gridcell", name="Press Space to toggle row selection (unchecked)  ARNOLD-BRWNBRY-OROWT").get_by_label("Press Space to toggle row").check()` | | | |
| Z.2 | Close the current page after completing the row selection. | `page.close()` | | | |
```
