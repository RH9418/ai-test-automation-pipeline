# Feature: Bbu By Product Weekly
**Tab Location:** Main Workspace

## Detailed User Interaction Flows

| Use Case ID | Test Case Description | Exact Locator | Pass/Fail | Notes | Issues |
|:---|:---|:---|:---|:---|:---|
```markdown
| | **--- INITIAL NAVIGATION TO EXECUTIVE DASHBOARD ---** | | | | |
| C.1 | Navigate to the 'Executive Dashboard' in the demand planning application by entering the specified URL. | `page.goto("https://stage.bbu.esp.antuit.ai/dp/demand-planning/executive-dashboard?workbookId=4&tabIndex=2")` | | | |
```
```markdown
| | **--- COLUMN CONFIGURATION - PRODUCT TOTAL ---** | | | | |
| D.1 | Click on the 'Product Total columns (0)' button to open the column configuration panel. | `page.locator("esp-card-component").filter(has_text="Product Total columns (0)").get_by_role("button").click()` | | | |
| D.2 | Uncheck the 'System Forecast Total (Plan Week)' column to hide it from the view. | `page.get_by_role("treeitem", name="System Forecast Total (Plan Week) Column").get_by_label("Press SPACE to toggle").uncheck()` | | | |
| D.3 | Uncheck the 'System Forecast Base (Plan)' column to hide it from the view. | `page.get_by_role("treeitem", name="System Forecast Base (Plan").get_by_label("Press SPACE to toggle").uncheck()` | | | |
| D.4 | Uncheck the 'System Forecast Promotion (' column to hide it from the view. | `page.get_by_role("treeitem", name="System Forecast Promotion (").get_by_label("Press SPACE to toggle").uncheck()` | | | |
| D.5 | Click on the third column selector in the configuration panel to modify its settings. | `page.locator("div:nth-child(3) > .ag-column-select-column").click()` | | | |
| D.6 | Uncheck the 'System Forecast Promotion (' column again to ensure it is hidden. | `page.get_by_role("treeitem", name="System Forecast Promotion (").get_by_label("Press SPACE to toggle").uncheck()` | | | |
| D.7 | Check the 'Toggle All Columns Visibility' checkbox to make all columns visible. | `page.get_by_role("checkbox", name="Toggle All Columns Visibility").check()` | | | |
| D.8 | Click on the first adjustment option to apply changes to the column configuration. | `page.locator(".pointer.zeb-adjustments").first.click()` | | | |
| D.9 | Click on the 'Save Preference' button to save the updated column configuration. | `page.locator("div").filter(has_text=re.compile(r"^Save Preference$")).nth(1).click()` | | | |
```
```markdown
| | **--- FILE DOWNLOAD - EXECUTIVE DASHBOARD ---** | | | | |
| E.1 | Click on the first download button (identified by the '.icon-color-toolbar-active.zeb-download-underline' class) to initiate the file download. | `page.locator(".icon-color-toolbar-active.zeb-download-underline").first.click()` | | | |
```
```markdown
| | **--- RESET PREFERENCES AND NAVIGATE TO PRODUCTS TAB ---** | | | | |
| F.1 | Click on the first adjustments button (identified by the '.pointer.zeb-adjustments' class) to open the adjustments menu. | `page.locator(".pointer.zeb-adjustments").first.click()` | | | |
| F.2 | Select the 'Reset Preference' option from the menu to reset all preferences to their default state. | `page.get_by_text("Reset Preference").click()` | | | |
| F.3 | Navigate to the 'Products' tab by clicking on the 'Products' option to access the product configuration section. | `page.get_by_text("Products").click()` | | | |
```
```markdown
| | **--- COLUMN CONFIGURATION - PRODUCTS ---** | | | | |
| G.1 | Open the 'Products columns' configuration menu by clicking the button within the 'esp-card-component' element labeled 'Products columns (0)'. | `page.locator("esp-card-component").filter(has_text="Products columns (0)").get_by_role("button").click()` | | | |
| G.2 | Uncheck the 'Toggle All Columns Visibility' checkbox to hide all columns initially. | `page.get_by_role("checkbox", name="Toggle All Columns Visibility").uncheck()` | | | |
| G.3 | Enable visibility for the 'System Forecast Total (Plan Week)' column by checking its corresponding checkbox. | `page.get_by_role("treeitem", name="System Forecast Total (Plan Week) Column").get_by_label("Press SPACE to toggle visibility (hidden)").check()` | | | |
| G.4 | Enable visibility for the 'System Forecast Base (Plan Week)' column by checking its corresponding checkbox. | `page.get_by_role("treeitem", name="System Forecast Base (Plan Week) Column").get_by_label("Press SPACE to toggle visibility (hidden)").check()` | | | |
| G.5 | Enable visibility for the 'System Forecast Promotion (Plan Week)' column by checking its corresponding checkbox. | `page.get_by_role("treeitem", name="System Forecast Promotion (Plan Week) Column").get_by_label("Press SPACE to toggle visibility (hidden)").check()` | | | |
| G.6 | Enable visibility for the 'System Forecast Total (Plan+1)' column by checking its corresponding checkbox. | `page.get_by_role("treeitem", name="System Forecast Total (Plan+1").get_by_label("Press SPACE to toggle visibility (hidden)").check()` | | | |
| G.7 | Enable visibility for the 'System Forecast Base (Plan+1)' column by checking its corresponding checkbox. | `page.get_by_role("treeitem", name="System Forecast Base (Plan+1").get_by_label("Press SPACE to toggle visibility (hidden)").check()` | | | |
| G.8 | Enable visibility for the 'System Forecast Promotion (Plan+1 Week)' column by checking its corresponding checkbox. | `page.get_by_role("treeitem", name="System Forecast Promotion (Plan+1 Week) Column").get_by_label("Press SPACE to toggle visibility (hidden)").check()` | | | |
| G.9 | Enable visibility for the 'Week Gross Units Average' column by checking its corresponding checkbox. | `page.get_by_role("treeitem", name="Week Gross Units Average Column").get_by_label("Press SPACE to toggle visibility (hidden)").check()` | | | |
| G.10 | Enable visibility for the '6 Week Aged Net Units Average' column by checking its corresponding checkbox. | `page.get_by_role("treeitem", name="6 Week Aged Net Units Average Column", exact=True).get_by_label("Press SPACE to toggle visibility (hidden)").check()` | | | |
| G.11 | Recheck the 'Toggle All Columns Visibility' checkbox to ensure all selected columns are visible. | `page.get_by_role("checkbox", name="Toggle All Columns Visibility").check()` | | | |
| G.12 | Click on the preferences dropdown menu to access options for saving or resetting preferences. | `page.locator("div:nth-child(3) > #preference-iconId > .legend-font > .multiselect-dropdown > .pointer").click()` | | | |
| G.13 | Select the 'Save Preference' option to save the current column visibility settings. | `page.locator("div").filter(has_text=re.compile(r"^Save Preference$")).nth(1).click()` | | | |
| G.14 | Reopen the preferences dropdown menu to access the reset option. | `page.locator("div:nth-child(3) > #preference-iconId > .legend-font > .multiselect-dropdown > .pointer").click()` | | | |
| G.15 | Select the 'Reset Preference' option to revert to the default column visibility settings. | `page.get_by_text("Reset Preference").click()` | | | |
```
```markdown
| | **--- FILTER AND PAGINATION ACTIONS ---** | | | | |
| H.1 | Click on the filter icon in the header to open the filter options for the column. | `page.locator(".ag-header-icon.ag-header-cell-filter-button > .ag-icon").first.click()` | | | |
| H.2 | Enter the filter value 'BARCEL' into the textbox to filter the column data. | `page.get_by_role("textbox", name="Filter Value").fill("BARCEL")` | | | |
| H.3 | Click on the 'Apply' button to apply the filter and update the displayed data. | `page.get_by_role("button", name="Apply").click()` | | | |
| H.4 | Click on the filter icon in the header again to reopen the filter options. | `page.locator(".ag-header-icon.ag-header-cell-filter-button > .ag-icon").first.click()` | | | |
| H.5 | Click on the 'Reset' button to clear the filter and revert the column data to its default state. | `page.get_by_role("button", name="Reset").click()` | | | |
| H.6 | Select the row with the name 'ARNOLD-BRWNBRY-OROWT' by toggling the checkbox in the grid cell. | `page.get_by_role("gridcell", name="Press Space to toggle row selection (unchecked)  ARNOLD-BRWNBRY-OROWT").get_by_label("Press Space to toggle row").check()` | | | |
| H.7 | Navigate to the second page of the table by clicking on the pagination link labeled '2'. | `page.locator("a").filter(has_text="2").click()` | | | |
| H.8 | Navigate to the third page of the table by clicking on the pagination link labeled '3'. | `page.locator("a").filter(has_text="3").click()` | | | |
```
```markdown
| | **--- DROPDOWN AND MULTI-SELECT ACTIONS ---** | | | | |
| I.1 | Click on the fourth item in the list to select it. | `page.get_by_role("listitem").filter(has_text=re.compile(r"^$")).nth(4).click()` | | | |
| I.2 | Click on the first dropdown caret to open the dropdown menu. | `page.locator(".dropdown-caret.p-l-16").first.click()` | | | |
| I.3 | Select the option 'View 20 row(s)' from the dropdown menu to adjust the number of rows displayed. | `page.locator("div").filter(has_text=re.compile(r"^View 20 row\(s\)$")).nth(1).click()` | | | |
| I.4 | Click on the 'Filter' button to open the filter options. | `page.get_by_text("Filter").click()` | | | |
| I.5 | Click on the dropdown caret within the filter section to open the time filter options. | `page.locator(".w-100.p-h-16.p-v-8.dropdown-label.background-white > .d-flex.align-items-center > .dropdown-caret").click()` | | | |
| I.6 | Select the 'Latest 5 Next 4' option from the time filter dropdown. | `page.locator("div").filter(has_text=re.compile(r"^Latest 5 Next 4$")).nth(1).click()` | | | |
| I.7 | Click on the dropdown caret within the filter section again to reopen the time filter options. | `page.locator(".w-100.p-h-16.p-v-8.dropdown-label.background-white > .d-flex.align-items-center > .dropdown-caret").click()` | | | |
| I.8 | Select the 'Latest 5 Next 12' option from the time filter dropdown. | `page.locator("div").filter(has_text=re.compile(r"^Latest 5 Next 12$")).nth(1).click()` | | | |
| I.9 | Click on the dropdown caret within the filter section again to reopen the time filter options. | `page.locator(".w-100.p-h-16.p-v-8.dropdown-label.background-white > .d-flex.align-items-center > .dropdown-caret").click()` | | | |
| I.10 | Select the 'Latest 13 Next 4' option from the time filter dropdown. | `page.locator("div").filter(has_text=re.compile(r"^Latest 13 Next 4$")).nth(1).click()` | | | |
| I.11 | Click on the dropdown caret within the filter section again to reopen the time filter options. | `page.locator(".w-100.p-h-16.p-v-8.dropdown-label.background-white > .d-flex.align-items-center > .dropdown-caret").click()` | | | |
| I.12 | Select the 'Latest 13 Next 12' option from the time filter dropdown. | `page.locator("div").filter(has_text=re.compile(r"^Latest 13 Next 12$")).nth(1).click()` | | | |
| I.13 | Click on the dropdown caret to open the multi-select dropdown menu. | `page.locator(".wr-20.font-weight-normal > esp-multiselect-dropdown > .multiselect-dropdown > div > .w-100 > .d-flex.align-items-center > .dropdown-caret").click()` | | | |
| I.14 | Click on the first option in the dropdown menu to select it. | `page.locator(".d-flex.flex-column.justify-content-center").first.click()` | | | |
| I.15 | Click on the first option under the 'dropdown-option' class to select it. | `page.locator(".d-flex.dropdown-option.align-items-center.p-v-5.p-l-32 > .d-flex").first.click()` | | | |
| I.16 | Click on the second option in the dropdown menu to select it. | `page.locator(".overflow-auto > div:nth-child(2) > .d-flex").click()` | | | |
| I.17 | Click on the third option in the dropdown menu to select it. | `page.locator(".overflow-auto > div:nth-child(3) > .d-flex").click()` | | | |
| I.18 | Click on the fourth option in the dropdown menu to select it. | `page.locator(".overflow-auto > div:nth-child(4)").click()` | | | |
| I.19 | Click on the fifth option in the dropdown menu to select it. | `page.locator(".overflow-auto > div:nth-child(5)").click()` | | | |
| I.20 | Click on the sixth option in the dropdown menu to select it. | `page.locator(".overflow-auto > div:nth-child(6)").click()` | | | |
| I.21 | Click on the first option in the dropdown menu again to deselect it. | `page.locator(".d-flex.flex-column.justify-content-center").first.click()` | | | |
```
```markdown
| | **--- WEEKLY SUMMARY PRODUCT CONFIGURATION ---** | | | | |
| J.1 | Click on the dropdown caret to open the multi-select dropdown menu for column visibility options. | `page.locator(".wr-20.font-weight-normal > esp-multiselect-dropdown > .multiselect-dropdown > div > .w-100 > .d-flex.align-items-center > .dropdown-caret").click()` | | | |
| J.2 | Click on the button within the 'Weekly Summary Product:ARNOLD' card to expand or collapse the product details. | `page.locator("esp-card-component").filter(has_text="Weekly Summary Product:ARNOLD").get_by_role("button").click()` | | | |
| J.3 | Uncheck the 'Toggle All Columns Visibility' checkbox to hide all columns in the Weekly Summary table. | `page.get_by_role("checkbox", name="Toggle All Columns Visibility").uncheck()` | | | |
| J.4 | Check the visibility of the column labeled '-10-26 (44)' by toggling its checkbox. | `page.get_by_role("treeitem", name="-10-26 (44) Column").get_by_label("Press SPACE to toggle visibility (hidden)").check()` | | | |
| J.5 | Check the visibility of the column labeled '-11-02 (45)' by toggling its checkbox. | `page.get_by_role("treeitem", name="-11-02 (45) Column").get_by_label("Press SPACE to toggle visibility (hidden)").check()` | | | |
| J.6 | Check the visibility of the column labeled '-11-09 (46)' by toggling its checkbox. | `page.get_by_role("treeitem", name="-11-09 (46) Column").get_by_label("Press SPACE to toggle visibility (hidden)").check()` | | | |
| J.7 | Check the visibility of the column labeled '-11-16 (47)' by toggling its checkbox. | `page.get_by_role("treeitem", name="-11-16 (47) Column").get_by_label("Press SPACE to toggle visibility (hidden)").check()` | | | |
| J.8 | Recheck the 'Toggle All Columns Visibility' checkbox to make all columns visible again in the Weekly Summary table. | `page.get_by_role("checkbox", name="Toggle All Columns Visibility").check()` | | | |
| J.9 | Click on the button within the 'Weekly Summary Product:ARNOLD' card again to collapse the product details. | `page.locator("esp-card-component").filter(has_text="Weekly Summary Product:ARNOLD").get_by_role("button").click()` | | | |
```
```markdown
| | **--- PREFERENCE MANAGEMENT AND EXPORT ACTIONS ---** | | | | |
| K.1 | Click on the 'Preference' icon to open the dropdown menu for managing preferences. | `page.locator("div:nth-child(4) > #preference-iconId > .legend-font > .multiselect-dropdown > .pointer").click()` | | | |
| K.2 | Click on the 'Save Preference' button to save the current table preferences. | `page.get_by_text("Save Preference").click()` | | | |
| K.3 | Click on the 'Export' icon to initiate the export process for the table data. | `page.locator("div:nth-child(3) > #export-iconId > .icon-color-toolbar-active").click()` | | | |
| K.4 | Click on the 'Preference' dropdown to open the menu for managing preferences. | `page.locator("div:nth-child(4) > #preference-iconId > .legend-font > .multiselect-dropdown > .pointer").click()` | | | |
| K.5 | Select 'Reset Preference' from the dropdown to reset the table preferences to default. | `page.get_by_text("Reset Preference").click()` | | | |
| K.6 | Click on the date '-02-15 (08)' to select it from the available options. | `page.get_by_text("-02-15 (08)").click()` | | | |
| K.7 | Click on the fifth image element to initiate the column visibility settings. | `page.get_by_role("img").nth(5).click()` | | | |
| K.8 | Click on the button within the 'Event Details columns (0)' card to open the column visibility options. | `page.locator("esp-card-component").filter(has_text="Event Details columns (0)").get_by_role("button").click()` | | | |
| K.9 | Uncheck the 'Event Column' to hide it from the table. | `page.get_by_role("treeitem", name="Event Column").get_by_label("Press SPACE to toggle visibility (visible)").uncheck()` | | | |
| K.10 | Uncheck the 'UPC 12 Column' to hide it from the table. | `page.get_by_role("treeitem", name="UPC 12 Column").get_by_label("Press SPACE to toggle visibility (visible)").uncheck()` | | | |
| K.11 | Uncheck the 'Customer Level 2 Column' to hide it from the table. | `page.get_by_role("treeitem", name="Customer Level 2 Column").get_by_label("Press SPACE to toggle visibility (visible)").uncheck()` | | | |
| K.12 | Uncheck the 'Start Date Column' to hide it from the table. | `page.get_by_role("treeitem", name="Start Date Column").get_by_label("Press SPACE to toggle visibility (visible)").uncheck()` | | | |
| K.13 | Uncheck the 'End Date Column' to hide it from the table. | `page.get_by_role("treeitem", name="End Date Column").get_by_label("Press SPACE to toggle visibility (visible)").uncheck()` | | | |
| K.14 | Check the 'Toggle All Columns Visibility' checkbox to make all columns visible again. | `page.get_by_role("checkbox", name="Toggle All Columns Visibility").check()` | | | |
| K.15 | Click on the 'Preference' icon to open the dropdown menu for saving or resetting preferences. | `page.locator(".col-12.m-t-16 > div > esp-grid-container > esp-card-component > .card-container > .title > .grid-icons-container > esp-grid-icons-component > .display-grid-icons > div:nth-child(2) > #preference-iconId > .legend-font > .multiselect-dropdown > .pointer").click()` | | | |
| K.16 | Click on 'Save Preference' to save the current column visibility settings. | `page.get_by_text("Save Preference").click()` | | | |
| K.17 | Click on the 'Export' icon to export the data with the current preferences. | `page.locator("div:nth-child(6) > div > esp-grid-container > esp-card-component > .card-container > .title > .grid-icons-container > esp-grid-icons-component > .display-grid-icons > div > #export-iconId > .icon-color-toolbar-active").click()` | | | |
```
```markdown
| | **--- EVENT DETAILS COLUMN CONFIGURATION ---** | | | | |
| L.1 | Click on the 'Preference' icon to open the dropdown menu for resetting preferences. | `page.locator(".col-12.m-t-16 > div > esp-grid-container > esp-card-component > .card-container > .title > .grid-icons-container > esp-grid-icons-component > .display-grid-icons > div:nth-child(2) > #preference-iconId > .legend-font > .multiselect-dropdown > .pointer").click()` | | | |
| L.2 | Click on 'Reset Preference' to revert to the default column visibility settings. | `page.get_by_text("Reset Preference").click()` | | | |
```
```markdown
| | **--- FILTER ACTIONS - SCAN TRACK ---** | | | | |
| M.1 | Click on the filter icon in the column header to open the filter options. | `page.locator(".ag-header-cell.ag-header-parent-hidden.ag-header-cell-sortable.ag-header-background.ag-focus-managed.ag-header-active > .ag-header-cell-comp-wrapper > .ag-cell-label-container > .ag-header-icon > .ag-icon").click()` | | | |
| M.2 | Enter 'Scan Track' into the filter textbox to filter the data based on this value. | `page.get_by_role("textbox", name="Filter Value").fill("Scan Track")` | | | |
| M.3 | Click on the 'Apply' button to apply the filter and update the displayed data. | `page.get_by_role("button", name="Apply").click()` | | | |
| M.4 | Click on the active filter icon to open the filter options for resetting. | `page.locator(".ag-header-icon.ag-header-cell-filter-button.ag-filter-active > .ag-icon").click()` | | | |
| M.5 | Click on the 'Reset' button to clear the applied filter and restore the unfiltered data. | `page.get_by_role("button", name="Reset").click()` | | | |
```
```markdown
| | **--- PRODUCT DRILL-DOWN AND CONTEXT MENU ACTIONS ---** | | | | |
| N.1 | Click on the 'Products' tab to navigate to the product selection view. | `page.get_by_text("Products").click()` | | | |
| N.2 | Double-click on the product 'ARNOLD-BRWNBRY-OROWT' to drill down into its details. | `page.locator("span").filter(has_text="ARNOLD-BRWNBRY-OROWT").first.dblclick()` | | | |
| N.3 | Double-click on 'ABO COUNTRY' to further drill down into its details. | `page.locator("span").filter(has_text="ABO COUNTRY").first.dblclick()` | | | |
| N.4 | Click on 'ABO COUNTRY' to select it. | `page.locator("span").filter(has_text="ABO COUNTRY").first.click()` | | | |
| N.5 | Double-click on the second instance of 'ABO COUNTRY' to drill down further. | `page.get_by_text("ABO COUNTRY").nth(1).dblclick()` | | | |
| N.6 | Right-click on the product 'OR CTY BTRMK WP 24Z-731300012500' to open the context menu. | `page.locator("span").filter(has_text=re.compile(r"^OR CTY BTRMK WP 24Z-731300012500$")).click(button="right")` | | | |
| N.7 | Click on 'Drill up' from the context menu to navigate back to the previous level. | `page.get_by_text("Drill up").click()` | | | |
| N.8 | Right-click on 'ABO COUNTRY' to open the context menu again. | `page.locator("span").filter(has_text="ABO COUNTRY").first.click(button="right")` | | | |
| N.9 | Click on 'Drill up' from the context menu to navigate back another level. | `page.get_by_text("Drill up").click()` | | | |
| N.10 | Right-click on 'ABO COUNTRY' to open the context menu once more. | `page.locator("span").filter(has_text="ABO COUNTRY").first.click(button="right")` | | | |
| N.11 | Click on 'Drill up' from the context menu to return to the top level. | `page.get_by_text("Drill up").click()` | | | |
```
```markdown
| | **--- ROW SELECTION AND CLEANUP ---** | | | | |
| O.1 | Select the row for the product 'ARNOLD-BRWNBRY-OROWT' by toggling the checkbox in the grid cell. | `page.get_by_role("gridcell", name="Press Space to toggle row selection (unchecked)  ARNOLD-BRWNBRY-OROWT").get_by_label("Press Space to toggle row").check()` | | | |
| O.2 | Close the current page after completing the row selection. | `page.close()` | | | |
| O.3 | Close the browser context to clean up resources. | `context.close()` | | | |
| O.4 | Close the browser to end the session. | `browser.close()` | | | |
```
