# Feature: By Product Daily
**Tab Location:** Main Workspace

## Detailed User Interaction Flows

| Use Case ID | Test Case Description | Exact Locator | Pass/Fail | Notes | Issues |
|:---|:---|:---|:---|:---|:---|
```
| | **--- BROWSER INITIALIZATION AND PAGE NAVIGATION ---** | | | | |
| B.1 | Launch a Chromium browser instance in non-headless mode. | `playwright.chromium.launch(headless=False)` | | | |
| B.2 | Create a new browser context to isolate session data. | `browser.new_context()` | | | |
| B.3 | Open a new page within the created browser context. | `context.new_page()` | | | |
| B.4 | Navigate to the 'Executive Dashboard' in the demand planning application using the specified URL. | `page.goto("https://stage.bbu.esp.antuit.ai/dp/demand-planning/executive-dashboard?workbookId=4&tabIndex=3")` | | | |
```
```
| | **--- PRODUCT TOTAL COLUMNS CONFIGURATION ---** | | | | |
| C.1 | Click on the 'Product Total columns (0)' text to open the configuration panel for product total columns. | `page.get_by_text("Product Total columns (0)").click()` | | | |
| C.2 | Repeat the click on 'Product Total columns (0)' to ensure the panel is opened (possibly redundant or for stability). | `page.get_by_text("Product Total columns (0)").click()` | | | |
| C.3 | Click on the 'Product Total' text to select or focus on the product total section. | `page.get_by_text("Product Total").click()` | | | |
| C.4 | Click on the button within the 'Product Total columns (0)' card component to proceed with further configuration. | `page.locator("esp-card-component").filter(has_text="Product Total columns (0)").get_by_role("button").click()` | | | |
```
```
| | **--- FILTER COLUMNS INPUT INTERACTION ---** | | | | |
| D.1 | Click on the 'Filter Columns Input' textbox to focus on the input field for filtering columns. | `page.get_by_role("textbox", name="Filter Columns Input").click()` | | | |
| D.2 | Uncheck the 'Toggle All Columns Visibility' checkbox to hide all columns initially. | `page.get_by_role("checkbox", name="Toggle All Columns Visibility").uncheck()` | | | |
| D.3 | Click on the 'Filter Columns Input' textbox again to ensure it is focused for input. | `page.get_by_role("textbox", name="Filter Columns Input").click()` | | | |
| D.4 | Fill the 'Filter Columns Input' textbox with the text 'system' to filter columns containing this keyword. | `page.get_by_role("textbox", name="Filter Columns Input").fill("system")` | | | |
| D.5 | Press 'Enter' in the 'Filter Columns Input' textbox to apply the filter. | `page.get_by_role("textbox", name="Filter Columns Input").press("Enter")` | | | |
```
```
| | **--- COLUMN SELECTION AND DESELECTION ---** | | | | |
| E.1 | Click on the first column in the filtered list to select it. | `page.locator(".ag-column-select-column").first.click()` | | | |
| E.2 | Uncheck the checkbox for 'System Forecast Base (Plan' to deselect this column. | `page.get_by_role("treeitem", name="System Forecast Base (Plan").get_by_label("Press SPACE to toggle").uncheck()` | | | |
| E.3 | Click on the 'Filter Columns Input' textbox to clear or modify the filter. | `page.get_by_role("textbox", name="Filter Columns Input").click()` | | | |
| E.4 | Clear the 'Filter Columns Input' textbox by filling it with an empty string. | `page.get_by_role("textbox", name="Filter Columns Input").fill("")` | | | |
| E.5 | Press 'Enter' in the 'Filter Columns Input' textbox to reset the filter. | `page.get_by_role("textbox", name="Filter Columns Input").press("Enter")` | | | |
| E.6 | Click on the 'System Forecast Total (Plan Week) Column' tree item to select it. | `page.get_by_role("treeitem", name="System Forecast Total (Plan Week) Column").click()` | | | |
| E.7 | Uncheck the checkbox for 'System Forecast Base (Plan' again to ensure it is deselected. | `page.get_by_role("treeitem", name="System Forecast Base (Plan").get_by_label("Press SPACE to toggle").uncheck()` | | | |
```
```
| | **--- SPECIFIC COLUMN SELECTION ---** | | | | |
| F.1 | Click on the 'System Forecast Promotion (' label to select this column. | `page.get_by_label("System Forecast Promotion (").get_by_text("System Forecast Promotion (").click()` | | | |
| F.2 | Click on the 'System Forecast Total (Plan+1' label to select this column. | `page.get_by_label("System Forecast Total (Plan+1").get_by_text("System Forecast Total (Plan+1").click()` | | | |
| F.3 | Click on the 'System Forecast Base (Plan+1' label to select this column. | `page.get_by_label("System Forecast Base (Plan+1").get_by_text("System Forecast Base (Plan+1").click()` | | | |
| F.4 | Click on the 'System Forecast Promotion (Plan+1 Week) Column' label to select this column. | `page.get_by_label("System Forecast Promotion (Plan+1 Week) Column").get_by_text("System Forecast Promotion (").click()` | | | |
| F.5 | Click on the '6 Week Gross Units Average' label to select this column. | `page.get_by_label("6 Week Gross Units Average").get_by_text("Week Gross Units Average").click()` | | | |
| F.6 | Click on the '6 Week Aged Net Units Average Column' label to select this column. | `page.get_by_label("6 Week Aged Net Units Average Column", exact=True).get_by_text("Week Aged Net Units Average").click()` | | | |
| F.7 | Click on the 'LY 6 Week Aged Net Units' label to select this column. | `page.get_by_label("LY 6 Week Aged Net Units").get_by_text("LY 6 Week Aged Net Units").click()` | | | |
```
```
| | **--- COLUMN SELECTION AND VISIBILITY TOGGLES ---** | | | | |
| G.1 | Click on the 'LY 6 Week Scan Units Average' label to select this column. | `page.get_by_label("LY 6 Week Scan Units Average").get_by_text("LY 6 Week Scan Units Average").click()` | | | |
| G.2 | Click on the '6 Week Scan Units Average Column' label to select this column. | `page.get_by_label("6 Week Scan Units Average Column", exact=True).get_by_text("Week Scan Units Average").click()` | | | |
| G.3 | Click on the '% Change 6 Week Aged Net' label to select this column. | `page.get_by_label("% Change 6 Week Aged Net").get_by_text("% Change 6 Week Aged Net").click()` | | | |
| G.4 | Click on the '% Change 6 Week Scan Units' label to select this column. | `page.get_by_label("% Change 6 Week Scan Units").get_by_text("% Change 6 Week Scan Units").click()` | | | |
| G.5 | Click on the 'Freshness (6 Week Average)' label to select this column. | `page.get_by_label("Freshness (6 Week Average)").get_by_text("Freshness (6 Week Average)").click()` | | | |
| G.6 | Click on the '6 Week Aged Returns Units' label to select this column. | `page.get_by_label("6 Week Aged Returns Units").get_by_text("6 Week Aged Returns Units").click()` | | | |
| G.7 | Check the 'Toggle All Columns Visibility' checkbox to make all columns visible again. | `page.get_by_role("checkbox", name="Toggle All Columns Visibility").check()` | | | |
```
```
| | **--- DOWNLOAD DATA PROCESS ---** | | | | |
| H.1 | Click on the 'Product Total columns (0)' button to open the column selection menu. | `page.locator("esp-card-component").filter(has_text="Product Total columns (0)").get_by_role("button").click()` | | | |
| H.2 | Click on the download icon to initiate the download of the selected data. | `page.locator(".icon-color-toolbar-active.zeb-download-underline").first.click()` | | | |
```
```
| | **--- PREFERENCE MANAGEMENT ---** | | | | |
| I.1 | Click on the informational message that begins with 'Please note that a maximum of' to acknowledge it. | `page.get_by_text("Please note that a maximum of").click()` | | | |
| I.2 | Click on the adjustments icon to open the settings menu. | `page.locator(".pointer.zeb-adjustments").first.click()` | | | |
| I.3 | Click on the 'Save Preference' button to save the current column visibility settings. | `page.get_by_text("Save Preference").click()` | | | |
| I.4 | Click on the adjustments icon again to reopen the settings menu. | `page.locator(".pointer.zeb-adjustments").first.click()` | | | |
| I.5 | Click on the 'Reset Preference' button to reset the column visibility settings to their default state. | `page.get_by_text("Reset Preference").click()` | | | |
```
```
| | **--- PRODUCT COLUMN CONFIGURATION ---** | | | | |
| J.1 | Click on the horizontal scroll container to ensure the view is scrolled to the appropriate section. | `page.locator(".ag-body-horizontal-scroll-container").first.click()` | | | |
| J.2 | Click on the 'Products columns (0) TopBottom' button to open the column selection menu. | `page.get_by_text("Products columns (0) TopBottom").click()` | | | |
| J.3 | Click on the 'Products' section to focus on the product-related columns. | `page.get_by_text("Products").click()` | | | |
| J.4 | Click on the button within the 'Products columns (0)' card to open the column configuration options. | `page.locator("esp-card-component").filter(has_text="Products columns (0)").get_by_role("button").click()` | | | |
| J.5 | Click on the 'Filter Columns Input' textbox to prepare for entering a filter value. | `page.get_by_role("textbox", name="Filter Columns Input").click()` | | | |
| J.6 | Fill the 'Filter Columns Input' textbox with the value '6' to filter columns containing '6'. | `page.get_by_role("textbox", name="Filter Columns Input").fill("6")` | | | |
| J.7 | Press 'Enter' to apply the filter and display the relevant columns. | `page.get_by_role("textbox", name="Filter Columns Input").press("Enter")` | | | |
```
```
| | **--- COLUMN FILTERING AND SELECTION ---** | | | | |
| K.1 | Check the visibility toggle for the 'Week Gross Units Average Column' to make it visible. | `page.get_by_role("treeitem", name="Week Gross Units Average Column").get_by_label("Press SPACE to toggle visibility (hidden)").check()` | | | |
| K.2 | Click on the '6 Week Aged Net Units Average' column to select it. | `page.get_by_label("Column List 9 Columns").get_by_text("6 Week Aged Net Units Average", exact=True).click()` | | | |
| K.3 | Click on the 'LY 6 Week Aged Net Units' column to select it. | `page.get_by_label("LY 6 Week Aged Net Units").get_by_text("LY 6 Week Aged Net Units").click()` | | | |
| K.4 | Click on the '% Change 6 Week Aged Net' column to select it. | `page.get_by_text("% Change 6 Week Aged Net").click()` | | | |
| K.5 | Click on the 'Filter Columns Input' textbox to clear the filter. | `page.get_by_role("textbox", name="Filter Columns Input").click()` | | | |
| K.6 | Clear the 'Filter Columns Input' textbox by filling it with an empty value. | `page.get_by_role("textbox", name="Filter Columns Input").fill("")` | | | |
| K.7 | Press 'Enter' to reset the filter and display all columns. | `page.get_by_role("textbox", name="Filter Columns Input").press("Enter")` | | | |
```
```
| | **--- TOGGLE ALL COLUMNS VISIBILITY ---** | | | | |
| M.1 | Uncheck the 'Toggle All Columns Visibility' checkbox to hide all columns. | `page.get_by_role("checkbox", name="Toggle All Columns Visibility").uncheck()` | | | |
| M.2 | Check the 'Toggle All Columns Visibility' checkbox to make all columns visible again. | `page.get_by_role("checkbox", name="Toggle All Columns Visibility").check()` | | | |
```
```
| | **--- COLUMN SELECTION AND VISIBILITY MANAGEMENT ---** | | | | |
| N.1 | Click on the first column in the column list to select it. | `page.locator("#ag-87 > .ag-column-panel > .ag-column-select > .ag-column-select-list > .ag-virtual-list-viewport > .ag-virtual-list-container > div > .ag-column-select-column").first.click()` | | | |
| N.2 | Uncheck the visibility toggle for the 'System Forecast Base (Plan Week) Column' to hide it. | `page.get_by_role("treeitem", name="System Forecast Base (Plan Week) Column").get_by_label("Press SPACE to toggle visibility (visible)").uncheck()` | | | |
| N.3 | Uncheck the visibility toggle for the 'System Forecast Promotion (Plan Week) Column' to hide it. | `page.get_by_role("treeitem", name="System Forecast Promotion (Plan Week) Column").get_by_label("Press SPACE to toggle visibility (visible)").uncheck()` | | | |
| N.4 | Uncheck the visibility toggle for the 'System Forecast Total (Plan+1)' column to hide it. | `page.get_by_role("treeitem", name="System Forecast Total (Plan+1").get_by_label("Press SPACE to toggle visibility (visible)").uncheck()` | | | |
| N.5 | Uncheck the visibility toggle for the 'System Forecast Base (Plan+1)' column to hide it. | `page.get_by_role("treeitem", name="System Forecast Base (Plan+1").get_by_label("Press SPACE to toggle visibility (visible)").uncheck()` | | | |
| N.6 | Uncheck the visibility toggle for the 'System Forecast Promotion (Plan+1 Week) Column' to hide it. | `page.get_by_role("treeitem", name="System Forecast Promotion (Plan+1 Week) Column").get_by_label("Press SPACE to toggle visibility (visible)").uncheck()` | | | |
| N.7 | Click on the column selector in the 7th position to interact with its visibility settings. | `page.locator("div:nth-child(7) > .ag-column-select-column").click()` | | | |
| N.8 | Uncheck the visibility toggle for the '6 Week Aged Net Units Average Column' to hide it. | `page.get_by_role("treeitem", name="6 Week Aged Net Units Average Column", exact=True).get_by_label("Press SPACE to toggle visibility (visible)").uncheck()` | | | |
| N.9 | Uncheck the visibility toggle for the 'LY 6 Week Aged Net Units' column to hide it. | `page.get_by_role("treeitem", name="LY 6 Week Aged Net Units").get_by_label("Press SPACE to toggle visibility (visible)").uncheck()` | | | |
| N.10 | Click on the column selector in the 11th position to interact with its visibility settings. | `page.locator("div:nth-child(11) > .ag-column-select-column").click()` | | | |
| N.11 | Uncheck the visibility toggle for the '% Change 6 Week Aged Net' column to hide it. | `page.get_by_role("treeitem", name="% Change 6 Week Aged Net").get_by_label("Press SPACE to toggle visibility (visible)").uncheck()` | | | |
| N.12 | Uncheck the visibility toggle for the 'LY 6 Week Scan Units Average' column to hide it. | `page.get_by_role("treeitem", name="LY 6 Week Scan Units Average").get_by_label("Press SPACE to toggle visibility (visible)").uncheck()` | | | |
| N.13 | Uncheck the visibility toggle for the '% Change 6 Week Scan Units' column to hide it. | `page.get_by_role("treeitem", name="% Change 6 Week Scan Units").get_by_label("Press SPACE to toggle visibility (visible)").uncheck()` | | | |
| N.14 | Click on the column selector in the 14th position to interact with its visibility settings. | `page.locator("div:nth-child(14) > .ag-column-select-column").click()` | | | |
| N.15 | Uncheck the visibility toggle for the column in the 15th position to hide it. | `page.locator("div:nth-child(15) > .ag-column-select-column").uncheck()` | | | |
```
```
| | **--- FINAL VISIBILITY TOGGLE ---** | | | | |
| O.1 | Uncheck the visibility toggle for the checkbox controlling column visibility to hide all columns. | `page.get_by_role("checkbox", name="Press SPACE to toggle visibility (visible)").uncheck()` | | | |
| O.2 | Check the 'Toggle All Columns Visibility' checkbox to make all columns visible. | `page.get_by_role("checkbox", name="Toggle All Columns Visibility").check()` | | | |
```
```
| | **--- EXPORT PROCESS ---** | | | | |
| P.1 | Click on the button within the 'Products columns (0)' card to open its settings. | `page.locator("esp-card-component").filter(has_text="Products columns (0)").get_by_role("button").click()` | | | |
| P.2 | Click on the export icon to initiate the export process and prepare to capture the download event. | `page.locator("div:nth-child(2) > #export-iconId > .icon-color-toolbar-active").click()` | | | |
```
```
| | **--- PREFERENCES MANAGEMENT ---** | | | | |
| Q.1 | Click on the informational text to acknowledge the export limit message. | `page.get_by_text("Please note that a maximum of").click()` | | | |
| Q.2 | Click on the preferences dropdown to open the preferences menu. | `page.locator("div:nth-child(3) > #preference-iconId > .legend-font > .multiselect-dropdown > .pointer").click()` | | | |
| Q.3 | Click on 'Save Preference' to save the current settings. | `page.get_by_text("Save Preference").click()` | | | |
| Q.4 | Click on the preferences dropdown again to reopen the preferences menu. | `page.locator("div:nth-child(3) > #preference-iconId > .legend-font > .multiselect-dropdown > .pointer").click()` | | | |
| Q.5 | Click on 'Reset Preference' to reset the settings to their default state. | `page.get_by_text("Reset Preference").click()` | | | |
```
```
| | **--- GRID INTERACTION ---** | | | | |
| R.1 | Click on the header cell to open the sorting or filtering options for the first column. | `page.locator(".ag-header-cell.ag-column-first.ag-header-parent-hidden.ag-header-cell-sortable > .ag-header-cell-comp-wrapper > .ag-cell-label-container").click()` | | | |
| R.2 | Click on the 'Product' text within the grid to select the 'Product' column. | `page.locator("esp-row-dimentional-grid").get_by_text("Product").click()` | | | |
```
```
| | **--- PRODUCT SELECTION AND FILTER ACTIVATION ---** | | | | |
| S.1 | Select 'Product 1' from the list of available products by clicking on its name in the grid. | `page.get_by_text("Product 1").click()` | | | |
| S.2 | Click on the filter icon in the header to open the filter options for the column. | `page.locator(".ag-header-icon.ag-header-cell-filter-button > .ag-icon").first.click()` | | | |
| S.3 | Click on the filter body wrapper to activate the filter input area for further configuration. | `page.locator(".ag-filter-body-wrapper").click()` | | | |
```
```
| | **--- FILTER OPERATOR SELECTION AND EXPLORATION ---** | | | | |
| T.1 | Open the filtering operator dropdown to select a filter condition. | `page.get_by_role("combobox", name="Filtering operator").click()` | | | |
| T.2 | Select the 'Contains' option from the filtering operator dropdown. | `page.get_by_role("option", name="Contains").click()` | | | |
| T.3 | Click on the 'Contains' text to confirm the selection. | `page.get_by_text("Contains").click()` | | | |
| T.4 | Click on the 'Does not contain' text to explore or select this filter condition. | `page.get_by_text("Does not contain").click()` | | | |
| T.5 | Reopen the filtering operator dropdown to select another filter condition. | `page.get_by_role("combobox", name="Filtering operator").click()` | | | |
| T.6 | Select the 'Equals' option from the filtering operator dropdown. | `page.get_by_role("option", name="Equals").click()` | | | |
| T.7 | Click on the 'Equals' text to confirm the selection. | `page.get_by_text("Equals").click()` | | | |
| T.8 | Click on the 'Does not equal' text to explore or select this filter condition. | `page.get_by_text("Does not equal").click()` | | | |
| T.9 | Click on the 'Does not equal' text again to confirm or toggle the selection. | `page.get_by_text("Does not equal").click()` | | | |
| T.10 | Select the 'Begins with' option from the filtering operator dropdown. | `page.get_by_role("option", name="Begins with").click()` | | | |
| T.11 | Click on the 'Begins with' text to confirm the selection. | `page.get_by_text("Begins with").click()` | | | |
| T.12 | Select the 'Ends with' option from the filtering operator dropdown. | `page.get_by_role("option", name="Ends with").click()` | | | |
| T.13 | Click on the 'Ends with' text to confirm the selection. | `page.get_by_text("Ends with").click()` | | | |
| T.14 | Select the 'Blank' option from the filtering operator dropdown. | `page.get_by_role("option", name="Blank", exact=True).click()` | | | |
```
```
| | **--- LOGICAL OPERATOR AND FILTER RESET ---** | | | | |
| U.1 | Click on the 'AND' text to set the logical operator for combining filter conditions. | `page.get_by_text("AND", exact=True).click()` | | | |
| U.2 | Click on the 'OR' text to set the logical operator for combining filter conditions. | `page.get_by_text("OR", exact=True).click()` | | | |
| U.3 | Click on the 'Clear' button to remove all applied filters. | `page.get_by_role("button", name="Clear").click()` | | | |
| U.4 | Click on the 'Reset' button to reset the filter settings to their default state. | `page.get_by_role("button", name="Reset").click()` | | | |
| U.5 | Click on the filter icon again to close the filter options. | `page.locator(".ag-header-icon.ag-header-cell-filter-button > .ag-icon").first.click()` | | | |
```
```
| | **--- FILTER APPLICATION AND ROW SELECTION ---** | | | | |
| V.1 | Click on the 'Apply' button to apply the selected filter conditions. | `page.get_by_role("button", name="Apply").click()` | | | |
| V.2 | Click on the first occurrence of the text 'ARNOLD-BRWNBRY-OROWT' within a span element to select the row. | `page.locator("span").filter(has_text="ARNOLD-BRWNBRY-OROWT").first.click()` | | | |
| V.3 | Check the checkbox for the row containing 'ARNOLD-BRWNBRY-OROWT' to toggle its selection. | `page.get_by_role("gridcell", name="Press Space to toggle row selection (unchecked)  ARNOLD-BRWNBRY-OROWT").get_by_label("Press Space to toggle row").check()` | | | |
```
```
| | **--- ROW CONTEXT MENU AND SELECTION CONFIRMATION ---** | | | | |
| W.1 | Right-click on the row containing 'ARNOLD-BRWNBRY-OROWT' to open the context menu. | `page.locator("esp-row-dimentional-grid span").filter(has_text=re.compile(r"^ARNOLD-BRWNBRY-OROWT$")).click(button="right")` | | | |
| W.2 | Click on the row containing 'ARNOLD-BRWNBRY-OROWT' to select it. | `page.locator("esp-row-dimentional-grid").get_by_text("ARNOLD-BRWNBRY-OROWT").click()` | | | |
| W.3 | Click on the row containing 'ARNOLD-BRWNBRY-OROWT' again, possibly to confirm or toggle the selection. | `page.locator("esp-row-dimentional-grid").get_by_text("ARNOLD-BRWNBRY-OROWT").click()` | | | |
```
```
| | **--- ADDITIONAL ROW SELECTION ---** | | | | |
| X.1 | Click on the span element containing the text 'ARTESANO' to select the corresponding row. | `page.locator("span").filter(has_text=re.compile(r"^ARTESANO$")).click()` | | | |
| X.2 | Click on the text 'ARTESANO' to confirm or highlight the selection. | `page.get_by_text("ARTESANO").click()` | | | |
```
```
| | **--- ROW SELECTION AND INTERACTION ---** | | | | |
| Y.1 | Check the checkbox for the row containing 'ARTESANO' to toggle its selection. | `page.get_by_role("gridcell", name="Press Space to toggle row selection (unchecked)  ARTESANO").get_by_label("Press Space to toggle row").check()` | | | |
| Y.2 | Double-click on the checkbox within the row to perform an additional action, possibly to confirm selection. | `page.locator(".ag-cell-value.ag-cell.ag-cell-not-inline-editing.ag-cell-normal-height.ag-cell-last-left-pinned.ag-column-first.no-border.ag-cell-focus > .ag-cell-wrapper > .ag-group-checkbox").dblclick()` | | | |
```
```
| | **--- COLUMN HEADER INTERACTION AND SORTING ---** | | | | |
| Z.1 | Click on the text 'System Forecast Total (Plan' to interact with the column header or data. | `page.get_by_text("System Forecast Total (Plan").nth(3).click()` | | | |
| Z.2 | Click on the descending sort icon in the column header to sort the data in descending order. | `page.locator(".ag-cell-label-container.ag-header-cell-sorted-desc > .ag-header-cell-label > .ag-sort-indicator-container > .ag-sort-indicator-icon.ag-sort-descending-icon > .ag-icon").click()` | | | |
| Z.3 | Click on the ascending sort icon in the column header to sort the data in ascending order. | `page.locator(".ag-cell-label-container.ag-header-cell-sorted-asc > .ag-header-cell-label > .ag-sort-indicator-container > .ag-sort-indicator-icon.ag-sort-ascending-icon > .ag-icon").click()` | | | |
| Z.4 | Click on the header icon to interact with the column, possibly to open a menu or perform an action. | `page.locator(".ag-header-cell.ag-header-parent-hidden.ag-header-cell-sortable.ag-header-background.ag-focus-managed.ag-header-active > .ag-header-cell-comp-wrapper > .ag-cell-label-container > .ag-header-icon > .ag-icon").click()` | | | |
```
```
| | **--- FILTER OPTIONS INTERACTION ---** | | | | |
| [.1 | Click on the filter body wrapper to open the filter options. | `page.locator(".ag-filter-body-wrapper").click()` | | | |
| [.2 | Click on the combobox labeled 'Filtering operator' to open the dropdown menu. | `page.get_by_role("combobox", name="Filtering operator").click()` | | | |
| [.3 | Select the 'Equals' option from the dropdown menu. | `page.get_by_role("option", name="Equals").click()` | | | |
| [.4 | Click on the text 'Equals' to confirm the selection. | `page.get_by_text("Equals").click()` | | | |
| [.5 | Select the 'Does not equal' option from the dropdown menu. | `page.get_by_role("option", name="Does not equal").click()` | | | |
| [.6 | Click on the text 'Does not equal' to confirm the selection. | `page.get_by_text("Does not equal").click()` | | | |
| [.7 | Select the 'Greater than' option from the dropdown menu. | `page.get_by_role("option", name="Greater than", exact=True).click()` | | | |
| [.8 | Click on the text 'Greater than' to confirm the selection. | `page.get_by_text("Greater than").click()` | | | |
| [.9 | Click on the text 'Greater than or equal to' to confirm the selection. | `page.get_by_text("Greater than or equal to").click()` | | | |
| [.10 | Click on the text 'Greater than or equal to' again, possibly to confirm or toggle the selection. | `page.get_by_text("Greater than or equal to").click()` | | | |
| [.11 | Select the 'Less than' option from the dropdown menu. | `page.get_by_role("option", name="Less than", exact=True).click()` | | | |
| [.12 | Click on the text 'Less than' to confirm the selection. | `page.get_by_text("Less than").click()` | | | |
| [.13 | Select the 'Between' option from the dropdown menu. | `page.get_by_role("option", name="Between").click()` | | | |
| [.14 | Click on the text 'Between' to confirm the selection. | `page.get_by_text("Between").click()` | | | |
| [.15 | Select the 'Blank' option from the dropdown menu. | `page.get_by_role("option", name="Blank", exact=True).click()` | | | |
| [.16 | Click on the text 'AND' to set the logical operator for the filter. | `page.get_by_text("AND", exact=True).click()` | | | |
| [.17 | Click on the text 'OR' to set the logical operator for the filter. | `page.get_by_text("OR", exact=True).click()` | | | |
```
```
| | **--- FILTER VALUE INPUT AND APPLICATION ---** | | | | |
| [.1 | Click on the spinbutton labeled 'Filter Value' to activate the input field. | `page.get_by_role("spinbutton", name="Filter Value").click()` | | | |
| [.2 | Fill the spinbutton labeled 'Filter Value' with the value '1'. | `page.get_by_role("spinbutton", name="Filter Value").fill("1")` | | | |
| [.3 | Click on the spinbutton labeled 'Filter Value' again, possibly to confirm the input. | `page.get_by_role("spinbutton", name="Filter Value").click()` | | | |
| [.4 | Click on the 'Apply' button to apply the filter settings. | `page.get_by_role("button", name="Apply").click()` | | | |
```
```
| | **--- FILTER CLEARING AND FINAL INTERACTION ---** | | | | |
| ].1 | Click on the header cell to interact with the column, possibly to open a menu or perform an action. | `page.locator(".ag-header-cell.ag-header-parent-hidden.ag-header-cell-sortable.ag-header-background.ag-focus-managed.ag-header-cell-filtered > .ag-header-cell-comp-wrapper > .ag-cell-label-container").click()` | | | |
| ].2 | Click on the filter button in the column header to activate the filter options. | `page.locator(".ag-header-icon.ag-header-cell-filter-button.ag-filter-active > .ag-icon").click()` | | | |
| ].3 | Click on the 'Clear' button to remove any existing filters. | `page.get_by_role("button", name="Clear").click()` | | | |
```
```
| | **--- RESET AND CONFIGURE COLUMN VISIBILITY PART 1 ---** | | | | |
| ^.1 | Click on the 'Reset' button to reset the filter settings to their default state. | `page.get_by_role("button", name="Reset").click()` | | | |
| ^.2 | Click on the button within the 'Products columns (0)' card to open the column visibility configuration. | `page.locator("esp-card-component").filter(has_text="Products columns (0)").get_by_role("button").click()` | | | |
| ^.3 | Click on the 'Filter Columns Input' textbox to activate it for entering a search term. | `page.get_by_role("textbox", name="Filter Columns Input").click()` | | | |
| ^.4 | Uncheck the 'Toggle All Columns Visibility' checkbox to hide all columns. | `page.get_by_role("checkbox", name="Toggle All Columns Visibility").uncheck()` | | | |
| ^.5 | Check the 'Toggle All Columns Visibility' checkbox to make all columns visible. | `page.get_by_role("checkbox", name="Toggle All Columns Visibility").check()` | | | |
| ^.6 | Uncheck the checkbox for the 'System Forecast Total (Plan Week) Column' to hide this specific column. | `page.get_by_role("treeitem", name="System Forecast Total (Plan Week) Column").get_by_label("Press SPACE to toggle visibility (visible)").uncheck()` | | | |
| ^.7 | Uncheck the checkbox for the 'System Forecast Base (Plan Week) Column' to hide this specific column. | `page.get_by_role("treeitem", name="System Forecast Base (Plan Week) Column").get_by_label("Press SPACE to toggle visibility (visible)").uncheck()` | | | |
| ^.8 | Click on the label for the 'System Forecast Promotion (Plan Week) Column' to interact with or highlight it. | `page.get_by_label("System Forecast Promotion (Plan Week) Column").get_by_text("System Forecast Promotion (").click()` | | | |
| ^.9 | Click on the label for the 'System Forecast Total (Plan+1)' column to interact with or highlight it. | `page.get_by_label("System Forecast Total (Plan+1").get_by_text("System Forecast Total (Plan+1").click()` | | | |
| ^.10 | Click on the label for the 'System Forecast Base (Plan+1)' column to interact with or highlight it. | `page.get_by_label("System Forecast Base (Plan+1").get_by_text("System Forecast Base (Plan+1").click()` | | | |
| ^.11 | Click on the label for the 'System Forecast Promotion (Plan+1 Week) Column' to interact with or highlight it. | `page.get_by_label("System Forecast Promotion (Plan+1 Week) Column").get_by_text("System Forecast Promotion (").click()` | | | |
```
```
| | **--- RESET AND CONFIGURE COLUMN VISIBILITY PART 2 ---** | | | | |
| _.1 | Click on the label for the '6 Week Gross Units Average' column to interact with or highlight it. | `page.get_by_label("6 Week Gross Units Average").get_by_text("Week Gross Units Average").click()` | | | |
| _.2 | Click on the label for the 'LY 6 Week Aged Net Units' column to interact with or highlight it. | `page.get_by_label("LY 6 Week Aged Net Units").get_by_text("LY 6 Week Aged Net Units").click()` | | | |
| _.3 | Click on the label for the '6 Week Aged Net Units Average Column' to interact with or highlight it. | `page.get_by_label("6 Week Aged Net Units Average Column", exact=True).get_by_text("Week Aged Net Units Average").click()` | | | |
| _.4 | Click on the label for the '6 Week Aged Net Units Average Column' again, possibly to confirm or toggle the selection. | `page.get_by_label("6 Week Aged Net Units Average Column", exact=True).get_by_text("Week Aged Net Units Average").click()` | | | |
| _.5 | Click on the label for the '% Change 6 Week Aged Net' column to interact with or highlight it. | `page.get_by_label("% Change 6 Week Aged Net").get_by_text("% Change 6 Week Aged Net").click()` | | | |
| _.6 | Click on the label for the '% Change 6 Week Scan Units' column to interact with or highlight it. | `page.get_by_label("% Change 6 Week Scan Units").get_by_text("% Change 6 Week Scan Units").click()` | | | |
| _.7 | Click on the label for the '6 Week Aged Returns Units' column to interact with or highlight it. | `page.get_by_label("6 Week Aged Returns Units").get_by_text("6 Week Aged Returns Units").click()` | | | |
| _.8 | Click on the label for the 'Freshness (6 Week Average)' column to interact with or highlight it. | `page.get_by_label("Freshness (6 Week Average)").get_by_text("Freshness (6 Week Average)").click()` | | | |
| _.9 | Click on the label for the 'LY 6 Week Scan Units Average' column to interact with or highlight it. | `page.get_by_label("LY 6 Week Scan Units Average").get_by_text("LY 6 Week Scan Units Average").click()` | | | |
| _.10 | Click on the label for the '6 Week Scan Units Average Column' to interact with or highlight it. | `page.get_by_label("6 Week Scan Units Average Column", exact=True).get_by_text("Week Scan Units Average").click()` | | | |
| _.11 | Click on the button within the 'Products columns (0)' card again, possibly to close the column visibility configuration. | `page.locator("esp-card-component").filter(has_text="Products columns (0)").get_by_role("button").click()` | | | |
```
```
| | **--- EXPORT DATA ---** | | | | |
| `.1` | Set up an expectation for a file download to occur during the subsequent action. | `with page.expect_download() as download2_info:` | | | |
| `.2` | Click on the export icon to initiate the export process. Locate the export icon within the toolbar and click it to start the export. | `page.locator("div:nth-child(2) > #export-iconId > .icon-color-toolbar-active").click()` | | | |
| `.3` | Capture the downloaded file information after the export action is triggered. | `download2 = download2_info.value` | | | |
```
```
| | **--- MANAGE PREFERENCES ---** | | | | |
| a.1 | Click on the informational message that notifies the user about the export limit. Look for the message text and click to acknowledge it. | `page.get_by_text("Please note that a maximum of").click()` | | | |
| a.2 | Open the preference dropdown menu to view the available options for managing preferences. Locate the dropdown menu icon and click it. | `page.locator("div:nth-child(3) > #preference-iconId > .legend-font > .multiselect-dropdown > .pointer").click()` | | | |
| a.3 | Save the current settings by selecting the 'Save Preference' option from the dropdown menu. | `page.get_by_text("Save Preference").click()` | | | |
| a.4 | Reopen the preference dropdown menu to access the options again. Locate the dropdown menu icon and click it. | `page.locator("div:nth-child(3) > #preference-iconId > .legend-font > .multiselect-dropdown > .pointer").click()` | | | |
| a.5 | Reset the settings to their default state by selecting the 'Reset Preference' option from the dropdown menu. | `page.get_by_text("Reset Preference").click()` | | | |
```
```
| | **--- PAGINATION INTERACTION AND NAVIGATION ---** | | | | |
| b.1 | Click on the text 'Showing 10 out of 28 123Rows' to interact with the pagination display. | `page.get_by_text("Showing 10 out of 28 123Rows").click()` | | | |
| b.2 | Click on the 'Rows per page View 10 row(s)' dropdown to open the options for changing the number of rows displayed. | `page.get_by_text("Rows per page View 10 row(s)").click()` | | | |
| b.3 | Click on the option 'View 10 row(s)' to confirm the selection of 10 rows per page. | `page.locator("span").filter(has_text=re.compile(r"^View 10 row\(s\)$")).click()` | | | |
| b.4 | Click on the text 'Showing 10 out of' to refresh or interact with the pagination display. | `page.get_by_text("Showing 10 out of").click()` | | | |
| b.5 | Click on the first instance of 'View 10 row(s)' to ensure the selection of 10 rows per page. | `page.get_by_text("View 10 row(s)").first.click()` | | | |
| b.6 | Click on the first instance of 'View 20 row(s)' to change the number of rows displayed to 20. | `page.locator("div").filter(has_text=re.compile(r"^View 20 row\(s\)$")).first.click()` | | | |
| b.7 | Click on the text 'Showing 20 out of' to interact with the updated pagination display. | `page.get_by_text("Showing 20 out of").click()` | | | |
| b.8 | Click on the exact text '12' to navigate to page 12 in the pagination. | `page.get_by_text("12", exact=True).click()` | | | |
| b.9 | Click on the link with the text '2' to navigate to page 2 in the pagination. | `page.locator("a").filter(has_text="2").click()` | | | |
| b.10 | Click on the left chevron icon to navigate to the previous page in the pagination. | `page.locator(".zeb-chevron-left").click()` | | | |
| b.11 | Click on the exact text '12' again to navigate back to page 12. | `page.get_by_text("12", exact=True).click()` | | | |
| b.12 | Click on the exact text '12' once more to confirm navigation to page 12. | `page.get_by_text("12", exact=True).click()` | | | |
| b.13 | Click on the 'pagination-last' button to navigate to the last page in the pagination. | `page.locator(".pagination-last").click()` | | | |
| b.14 | Click on the 'zeb-nav-to-first' button to navigate back to the first page in the pagination. | `page.locator(".zeb-nav-to-first").click()` | | | |
```
```
| | **--- ROW SELECTION AND CARD INTERACTION ---** | | | | |
| c.1 | Check the checkbox in the row labeled 'Press Space to toggle row selection (unchecked)' to select the row for 'THOMAS BRANDS'. | `page.get_by_role("row", name="Press Space to toggle row selection (unchecked)  THOMAS BRANDS").get_by_label("Press Space to toggle row").check()` | | | |
| c.2 | Click on the card content area to interact with the main filter and summary section. | `page.locator(".card-content.p-24").click()` | | | |
```
```
| | **--- FILTER APPLICATION AND SUMMARY INTERACTION ---** | | | | |
| d.1 | Click on the text 'FilterTime Latest Order &' to open the filter options. | `page.get_by_text("FilterTime Latest Order &").click()` | | | |
| d.2 | Click on the 'Filter' button to apply or modify the filter settings. | `page.locator("div").filter(has_text=re.compile(r"^Filter$")).click()` | | | |
| d.3 | Click on the 'Time' option to select the time-based filter. | `page.get_by_text("Time").click()` | | | |
| d.4 | Click on 'Latest Order & Plan Week' to apply this specific filter. | `page.get_by_text("Latest Order & Plan Week").first.click()` | | | |
| d.5 | Click on 'Daily Summary Product:THOMAS' to view the daily summary for the product 'THOMAS'. | `page.get_by_text("Daily Summary Product:THOMAS").click()` | | | |
| d.6 | Click on 'Daily Summary' to interact with the summary section. | `page.get_by_text("Daily Summary").click()` | | | |
| d.7 | Click on 'Product:THOMAS BRANDS' to focus on the product-specific summary. | `page.get_by_text("Product:THOMAS BRANDS").first.click()` | | | |
| d.8 | Click on the third instance of the exact text 'Product' to refine the selection. | `page.get_by_text("Product", exact=True).nth(2).click()` | | | |
| d.9 | Click on the second instance of 'THOMAS BRANDS' to confirm the selection of this product. | `page.get_by_text("THOMAS BRANDS").nth(1).click()` | | | |
| d.10 | Click on 'Daily Summary Product:THOMAS' again to refresh or interact with the summary. | `page.get_by_text("Daily Summary Product:THOMAS").click()` | | | |
```
```
| | **--- DROPDOWN INTERACTION AND MEASURE SELECTION ---** | | | | |
| e.1 | Click on the dropdown to open the multiselect options for filtering. | `page.locator(".wr-20.font-weight-normal > esp-multiselect-dropdown > .multiselect-dropdown > div > .w-100").click()` | | | |
| e.2 | Select the first option in the dropdown list. | `page.locator(".d-flex.dropdown-option").first.click()` | | | |
| e.3 | Select the first option in the dropdown list again, possibly to toggle or confirm the selection. | `page.locator(".d-flex.dropdown-option").first.click()` | | | |
| e.4 | Click on 'User Suggested Order Total' to select this measure. | `page.get_by_text("User Suggested Order Total").first.click()` | | | |
```
```
| | **--- MEASURE SELECTION - USER SUGGESTED AND OVERRIDE ---** | | | | |
| f.1 | Click on the second instance of 'User Suggested Order Base' to select this measure. | `page.get_by_text("User Suggested Order Base").nth(1).click()` | | | |
| f.2 | Click on the second instance of 'User Suggested Order Promotion' to select this measure. | `page.get_by_text("User Suggested Order Promotion").nth(1).click()` | | | |
| f.3 | Click on the second instance of 'User Override Total' to select this measure. | `page.get_by_text("User Override Total").nth(1).click()` | | | |
| f.4 | Click on the second instance of 'User Override Base' to select this measure. | `page.get_by_text("User Override Base").nth(1).click()` | | | |
```
```
| | **--- CHECKBOX INTERACTION - INITIAL TOGGLES ---** | | | | |
| g.1 | Click on the first checkbox to select or toggle it. | `page.locator(".d-flex.flex-column.justify-content-center.font-size-10.align-items-center.checkbox-v2.m-r-10.zeb-check").first.click()` | | | |
| g.2 | Click on the first checkbox again, possibly to toggle or confirm the selection. | `page.locator(".d-flex.flex-column.justify-content-center.font-size-10.align-items-center.checkbox-v2.m-r-10.zeb-check").first.click()` | | | |
| g.3 | Click on the first checkbox again, possibly to toggle or confirm the selection. | `page.locator(".d-flex.flex-column.justify-content-center.font-size-10.align-items-center.checkbox-v2.m-r-10.zeb-check").first.click()` | | | |
```
```
| | **--- MEASURE SELECTION - ION SUGGESTED AND GROSS UNITS ---** | | | | |
| h.1 | Click on the second instance of 'ION Suggested Order Promotion' to select this measure. | `page.get_by_text("ION Suggested Order Promotion").nth(1).click()` | | | |
| h.2 | Click on 'Gross Units (CW-4)' to select this measure. | `page.get_by_text("Gross Units (CW-4)", exact=True).click()` | | | |
| h.3 | Click on the second instance of 'Gross Units (CW-3)' to select this measure. | `page.get_by_text("Gross Units (CW-3)").nth(1).click()` | | | |
| h.4 | Click on the second instance of 'Aged Net Units (CW-3)' to select this measure. | `page.get_by_text("Aged Net Units (CW-3)").nth(1).click()` | | | |
```
```markdown
| | **--- DROPDOWN INTERACTION - DESELECT AND MODIFY ---** | | | | |
| i.1 | Click on the first selected dropdown option to deselect or modify the selection. | `page.locator(".d-flex.dropdown-option.align-items-center.p-v-5.p-l-32.p-r-16.selected").first.click()` | | | |
| i.2 | Click on the first selected dropdown option again, possibly to confirm the deselection or modification. | `page.locator(".d-flex.dropdown-option.align-items-center.p-v-5.p-l-32.p-r-16.selected").first.click()` | | | |
```
```markdown
| | **--- CHECKBOX INTERACTION - ADDITIONAL TOGGLES ---** | | | | |
| j.1 | Click on the first checkbox to select or toggle it again. | `page.locator(".d-flex.flex-column.justify-content-center.font-size-10.align-items-center.checkbox-v2.m-r-10.zeb-check").first.click()` | | | |
| j.2 | Click on the first checkbox again, possibly to toggle or confirm the selection. | `page.locator(".d-flex.flex-column.justify-content-center.font-size-10.align-items-center.checkbox-v2.m-r-10.zeb-check").first.click()` | | | |
```
```markdown
| | **--- MEASURE SELECTION - AGED NET UNITS AND SCAN UNITS ---** | | | | |
| k.1 | Click on 'Aged Net Units (CW-6)' to select this measure from the list. | `page.get_by_text("Aged Net Units (CW-6)", exact=True).click()` | | | |
| k.2 | Click on the first selected dropdown option to deselect or modify the current selection. | `page.locator(".d-flex.dropdown-option.align-items-center.p-v-5.p-l-32.p-r-16.selected").first.click()` | | | |
| k.3 | Click on 'Scan Units (CW-4)' to select this measure from the list. | `page.get_by_text("Scan Units (CW-4)", exact=True).click()` | | | |
| k.4 | Click on 'Scan Units (CW-4)' again, possibly to confirm or toggle the selection. | `page.get_by_text("Scan Units (CW-4)", exact=True).click()` | | | |
```
```markdown
| | **--- CHILD ELEMENT SELECTION - OVERFLOW CONTAINER ---** | | | | |
| l.1 | Click on the 21st child element within the overflow container to select a specific option. | `page.locator(".overflow-auto > div:nth-child(21)").click()` | | | |
| l.2 | Click on the 20th child element with the specified class to select another option. | `page.locator("div:nth-child(20) > .d-flex").click()` | | | |
```
```markdown
| | **--- MEASURE SELECTION - SCAN UNITS AND SELECT ALL ---** | | | | |
| m.1 | Click on the first instance of 'Scan Units (CW-4)' to select this measure. | `page.get_by_text("Scan Units (CW-4)").first.click()` | | | |
| m.2 | Click on the first instance of 'Scan Units (CW-4)' again, possibly to confirm or toggle the selection. | `page.get_by_text("Scan Units (CW-4)").first.click()` | | | |
| m.3 | Click on 'Select All' to select all available measures in the dropdown. | `page.get_by_text("Select All").click()` | | | |
```
```markdown
| | **--- INTERACTION WITH 'ALL' AND DAILY SUMMARY CARD ---** | | | | |
| n.1 | Click on the fourth instance of the 'All' text to select or interact with it. | `page.get_by_text("All").nth(4).click()` | | | |
| n.2 | Click on the button within the 'Daily Summary Product:THOMAS' card to expand or interact with it. | `page.locator("esp-card-component").filter(has_text="Daily Summary Product:THOMAS").get_by_role("button").click()` | | | |
```
```markdown
| | **--- FILTER COLUMNS INPUT AND COLUMN SELECTION ---** | | | | |
| o.1 | Click on the 'Filter Columns Input' textbox to focus on it. | `page.get_by_role("textbox", name="Filter Columns Input").click()` | | | |
| o.2 | Fill the 'Filter Columns Input' textbox with the value '02/1' to filter columns based on this input. | `page.get_by_role("textbox", name="Filter Columns Input").fill("02/1")` | | | |
| o.3 | Click on the first column in the filtered list to select it. | `page.locator("#ag-4958 > .ag-column-panel > .ag-column-select > .ag-column-select-list > .ag-virtual-list-viewport > .ag-virtual-list-container > div > .ag-column-select-column").first.click()` | | | |
```
```markdown
| | **--- COLUMN VISIBILITY TOGGLE ---** | | | | |
| p.1 | Uncheck the visibility toggle for the '/11(Wed) Column' to hide it. | `page.get_by_role("treeitem", name="/11(Wed) Column").get_by_label("Press SPACE to toggle visibility (visible)").uncheck()` | | | |
```
```markdown
| | **--- COLUMN VISIBILITY MANAGEMENT ---** | | | | |
| q.1 | Uncheck the visibility toggle for the '/12(Thu) Column' to hide it. | `page.get_by_role("treeitem", name="/12(Thu) Column").get_by_label("Press SPACE to toggle visibility (visible)").uncheck()` | | | |
| q.2 | Check the 'Toggle All Columns Visibility' checkbox to make all columns visible. | `page.get_by_role("checkbox", name="Toggle All Columns Visibility").check()` | | | |
| q.3 | Click on the 'Filter Columns Input' textbox again to focus on it. | `page.get_by_role("textbox", name="Filter Columns Input").click()` | | | |
| q.4 | Clear the 'Filter Columns Input' textbox by filling it with an empty string. | `page.get_by_role("textbox", name="Filter Columns Input").fill("")` | | | |
| q.5 | Press 'Enter' in the 'Filter Columns Input' textbox to apply the filter or finalize the action. | `page.get_by_role("textbox", name="Filter Columns Input").press("Enter")` | | | |
```
```markdown
| | **--- DAILY SUMMARY PRODUCT INTERACTION ---** | | | | |
| r.1 | Locate the 'Daily Summary Product:THOMAS' card and click the button inside it to expand or interact with the card. | `page.locator("esp-card-component").filter(has_text="Daily Summary Product:THOMAS").get_by_role("button").click()` | | | |
| r.2 | Click the button inside the 'Daily Summary Product:THOMAS' card again to toggle or confirm the action. | `page.locator("esp-card-component").filter(has_text="Daily Summary Product:THOMAS").get_by_role("button").click()` | | | |
```
```markdown
| | **--- TOGGLE INDIVIDUAL COLUMN VISIBILITY ---** | | | | |
| s.1 | Locate the visibility toggle for the '/01(Sun) Column' and check it to make the column visible. | `page.get_by_role("treeitem", name="/01(Sun) Column").get_by_label("Press SPACE to toggle visibility (hidden)").check()` | | | |
| s.2 | Locate the visibility toggle for the '/02(Mon) Column' and check it to make the column visible. | `page.get_by_role("treeitem", name="/02(Mon) Column").get_by_label("Press SPACE to toggle visibility (hidden)").check()` | | | |
| s.3 | Locate the visibility toggle for the '/03(Tue) Column' and check it to make the column visible. | `page.get_by_role("treeitem", name="/03(Tue) Column").get_by_label("Press SPACE to toggle visibility (hidden)").check()` | | | |
| s.4 | Locate the visibility toggle for the '/04(Wed) Column' and check it to make the column visible. | `page.get_by_role("treeitem", name="/04(Wed) Column").get_by_label("Press SPACE to toggle visibility (hidden)").check()` | | | |
| s.5 | Locate the visibility toggle for the '/05(Thu) Column' and check it to make the column visible. | `page.get_by_role("treeitem", name="/05(Thu) Column").get_by_label("Press SPACE to toggle visibility (hidden)").check()` | | | |
| s.6 | Locate the visibility toggle for the '/06(Fri) Column' and check it to make the column visible. | `page.get_by_role("treeitem", name="/06(Fri) Column").get_by_label("Press SPACE to toggle visibility (hidden)").check()` | | | |
| s.7 | Locate the visibility toggle for the '/07(Sat) Column' and check it to make the column visible. | `page.get_by_role("treeitem", name="/07(Sat) Column").get_by_label("Press SPACE to toggle visibility (hidden)").check()` | | | |
| s.8 | Locate the visibility toggle for the '/08(Sun) Column' and check it to make the column visible. | `page.get_by_role("treeitem", name="/08(Sun) Column").get_by_label("Press SPACE to toggle visibility (hidden)").check()` | | | |
| s.9 | Locate the visibility toggle for the '/09(Mon) Column' and check it to make the column visible. | `page.get_by_role("treeitem", name="/09(Mon) Column").get_by_label("Press SPACE to toggle visibility (hidden)").check()` | | | |
| s.10 | Click on the column element located at 'div:nth-child(10) > .ag-column-select-column' to interact with it. | `page.locator("div:nth-child(10) > .ag-column-select-column").click()` | | | |
| s.11 | Locate the visibility toggle for the '/11(Wed) Column' and check it to make the column visible. | `page.get_by_role("treeitem", name="/11(Wed) Column").get_by_label("Press SPACE to toggle visibility (hidden)").check()` | | | |
| s.12 | Locate the visibility toggle for the '/12(Thu) Column' and check it to make the column visible. | `page.get_by_role("treeitem", name="/12(Thu) Column").get_by_label("Press SPACE to toggle visibility (hidden)").check()` | | | |
| s.13 | Locate the visibility toggle for the '/13(Fri) Column' and check it to make the column visible. | `page.get_by_role("treeitem", name="/13(Fri) Column").get_by_label("Press SPACE to toggle visibility (hidden)").check()` | | | |
```
```markdown
| | **--- TOGGLE ALL COLUMNS VISIBILITY ---** | | | | |
| t.1 | Locate the 'Toggle All Columns Visibility' checkbox and check it to make all columns visible. | `page.get_by_role("checkbox", name="Press SPACE to toggle visibility (hidden)").check()` | | | |
```
```markdown
| | **--- DAILY SUMMARY PRODUCT RE-INTERACTION ---** | | | | |
| u.1 | Locate the 'Daily Summary Product:THOMAS' card and click the button inside it to expand or interact with the card. | `page.locator("esp-card-component").filter(has_text="Daily Summary Product:THOMAS").get_by_role("button").click()` | | | |
```
```markdown
| | **--- EXPORT PROCESS ---** | | | | |
| v.1 | Click on the export icon located in the toolbar to initiate the export process. | `page.locator("span:nth-child(6) > esp-grid-icons-component > .display-grid-icons > div:nth-child(2) > #export-iconId > .icon-color-toolbar-active").click()` | | | |
| v.2 | Click on the text element that provides information about the export limit to proceed with the export process. | `page.get_by_text("Please note that a maximum of").click()` | | | |
```
```markdown
| | **--- PREFERENCE MANAGEMENT ---** | | | | |
| w.1 | Click on the preference icon located in the toolbar to open the preferences dropdown menu. | `page.locator("span:nth-child(6) > esp-grid-icons-component > .display-grid-icons > div:nth-child(3) > #preference-iconId > .legend-font > .multiselect-dropdown > .pointer").click()` | | | |
| w.2 | Select the 'Save Preference' option from the dropdown menu to save the current preferences. | `page.locator("div").filter(has_text=re.compile(r"^Save Preference$")).first.click()` | | | |
| w.3 | Click on the preference icon again to reopen the preferences dropdown menu. | `page.locator("span:nth-child(6) > esp-grid-icons-component > .display-grid-icons > div:nth-child(3) > #preference-iconId > .legend-font > .multiselect-dropdown > .pointer").click()` | | | |
| w.4 | Select the 'Reset Preference' option from the dropdown menu to reset the preferences to their default values. | `page.locator("div").filter(has_text=re.compile(r"^Reset Preference$")).first.click()` | | | |
```
```markdown
| | **--- GRID HEADER AND COLUMN INTERACTIONS ---** | | | | |
| x.1 | Click on the header cell to interact with the first column in the grid. | `page.locator(".ag-header-cell.ag-column-first.ag-header-parent-hidden.ag-header-background.ag-focus-managed.ag-header-active > .ag-header-cell-comp-wrapper > .ag-cell-label-container > .ag-header-cell-label").click()` | | | |
| x.2 | Click on the 'User Suggested Order Total' text to select or interact with it. | `page.get_by_text("User Suggested Order Total").click()` | | | |
| x.3 | Click on the first icon within the grid, possibly to open a filter or perform an action. | `page.locator("i").first.click()` | | | |
| x.4 | Click on the 'User Override Total' text to select or interact with it. | `page.get_by_text("User Override Total").click()` | | | |
| x.5 | Click on the grid cell labeled 'User Override Total' to interact with it. | `page.get_by_role("gridcell", name=" User Override Total").click()` | | | |
| x.6 | Click on the second icon within the grid, possibly to open a filter or perform an action. | `page.locator("i").nth(2).click()` | | | |
| x.7 | Click on the 'Gross Units (CW-3)' text within the grid to select or interact with it. | `page.locator("esp-column-dimentional-grid").get_by_text("Gross Units (CW-3)").click()` | | | |
```
```markdown
| | **--- GRID CHEVRON AND TEXT INTERACTIONS ---** | | | | |
| y.1 | Click on the fifth icon within the grid, possibly to open a filter or perform an action. | `page.locator("i").nth(5).click()` | | | |
| y.2 | Click on the 'Aged Net Units (CW-3)' text within the grid to select or interact with it. | `page.locator("esp-column-dimentional-grid").get_by_text("Aged Net Units (CW-3)").click()` | | | |
| y.3 | Click on the chevron icon to expand or collapse a group within the grid. | `page.locator(".ag-cell-value.ag-cell.ag-cell-not-inline-editing.ag-cell-normal-height.ag-cell-last-left-pinned.ag-column-first.ag-cell-override-normal.notosans-overwrite.no-border.ag-cell-focus > .ag-cell-wrapper > .ag-group-contracted > .zeb-chevron-right").click()` | | | |
| y.4 | Click on the 'Scan Units (CW-3)' text within the grid to select or interact with it. | `page.locator("esp-column-dimentional-grid").get_by_text("Scan Units (CW-3)").click()` | | | |
| y.5 | Click on the chevron icon again to expand or collapse another group within the grid. | `page.locator(".ag-cell-value.ag-cell.ag-cell-not-inline-editing.ag-cell-normal-height.ag-cell-last-left-pinned.ag-column-first.ag-cell-override-normal.notosans-overwrite.no-border.ag-cell-focus > .ag-cell-wrapper > .ag-group-contracted > .zeb-chevron-right").click()` | | | |
```
```markdown
| | **--- DAILY TREND AND LINE-BAR CHART INTERACTIONS ---** | | | | |
| z.1 | Click on the 'Daily Trend Product:THOMAS' text to navigate or interact with it. | `page.get_by_text("Daily Trend Product:THOMAS").click()` | | | |
| z.2 | Click on the 'Daily Trend' text to navigate or interact with it. | `page.get_by_text("Daily Trend").click()` | | | |
| z.3 | Click on the 'Product:THOMAS BRANDS' text within the line-bar chart to interact with it. | `page.locator("dp-line-bar-chart").get_by_text("Product:THOMAS BRANDS").click()` | | | |
| z.4 | Click on the 'Product' text within the line-bar chart to interact with it. | `page.locator("dp-line-bar-chart").get_by_text("Product", exact=True).click()` | | | |
| z.5 | Click on the 'THOMAS BRANDS' text within the line-bar chart to interact with it. | `page.locator("dp-line-bar-chart").get_by_text("THOMAS BRANDS").click()` | | | |
```
```markdown
| | **--- DROPDOWN AND FILTER SELECTIONS ---** | | | | |
| {.1 | Click on the dropdown caret within the multiselect dropdown to open the filter options. | `page.locator(".ellipses > esp-multiselect-dropdown > .multiselect-dropdown > div > .w-100 > .d-flex.align-items-center > .dropdown-caret").click()` | | | |
| {.2 | Select the 'User Suggested Order Base' option from the dropdown. | `page.locator("span").filter(has_text="User Suggested Order Base").click()` | | | |
| {.3 | Select the 'User Suggested Order Promotion' option from the dropdown. | `page.locator("span").filter(has_text="User Suggested Order Promotion").click()` | | | |
| {.4 | Select the 'User Override Base' option from the dropdown. | `page.locator("span").filter(has_text="User Override Base").click()` | | | |
| {.5 | Select the 'User Override Promotion' option from the dropdown. | `page.locator("span").filter(has_text="User Override Promotion").click()` | | | |
```
```markdown
| | **--- LINE-BAR CHART AND GRID ELEMENT INTERACTIONS ---** | | | | |
| {.1 | Click on the 'Gross Units (CW-3)' text within the line-bar chart to interact with it. | `page.locator("dp-line-bar-chart span").filter(has_text="Gross Units (CW-3)").click()` | | | |
| {.2 | Click on the 'Gross Units (CW-4)' text within the line-bar chart to interact with it. | `page.locator("dp-line-bar-chart").get_by_text("Gross Units (CW-4)").click()` | | | |
| {.3 | Click on the seventh element in the grid, possibly to interact with a specific data point or group. | `page.locator("div:nth-child(7) > .d-flex").click()` | | | |
| {.4 | Click on the eighth element in the grid, possibly to interact with a specific data point or group. | `page.locator("div:nth-child(8) > .d-flex").click()` | | | |
| {.5 | Click on the ninth element in the grid, possibly to interact with a specific data point or group. | `page.locator("div:nth-child(9) > .d-flex").click()` | | | |
| {.6 | Click on the tenth element in the grid, possibly to interact with a specific data point or group. | `page.locator("div:nth-child(10) > .d-flex").click()` | | | |
| {.7 | Click on the eleventh element in the grid, possibly to interact with a specific data point or group. | `page.locator("div:nth-child(11) > .d-flex").click()` | | | |
| {.8 | Click on the twelfth element in the grid, possibly to interact with a specific data point or group. | `page.locator("div:nth-child(12) > .d-flex").click()` | | | |
```
```markdown
| | **--- INTERACTION WITH LINE-BAR CHART ELEMENTS ---** | | | | |
| }.1 | Click on the 'Scan Units (CW-3)' text within the line-bar chart to interact with it. | `page.locator("dp-line-bar-chart span").filter(has_text="Scan Units (CW-3)").click()` | | | |
| }.2 | Click on the 'Scan Units (CW-4)' text within the line-bar chart to interact with it. | `page.locator("dp-line-bar-chart").get_by_text("Scan Units (CW-4)").click()` | | | |
| }.3 | Click on the 'Scan Units (CW-5)' text within the line-bar chart to interact with it. | `page.locator("dp-line-bar-chart").get_by_text("Scan Units (CW-5)").click()` | | | |
| }.4 | Click on the 'Scan Units (CW-6)' text within the line-bar chart to interact with it. | `page.locator("dp-line-bar-chart").get_by_text("Scan Units (CW-6)").click()` | | | |
```
```markdown
| | **--- PREFERENCE MANAGEMENT ACTIONS ---** | | | | |
| ~.1 | Click on the 'Gross Units (CW-4), Gross' text to interact with it, possibly to select or highlight it. | `page.get_by_text("Gross Units (CW-4), Gross").first.click()` | | | |
| ~.2 | Click on the multiselect dropdown within the preference icon container to open the preference options. | `page.locator(".title.d-flex.align-items-center.font-size-16.font-weight-bold.nunito.title-color > .grid-icons-container > esp-grid-icons-component > .display-grid-icons > div > #preference-iconId > .legend-font > .multiselect-dropdown > .pointer").click()` | | | |
| ~.3 | Click on 'Save Preference' to save the current settings or selections. | `page.get_by_text("Save Preference").click()` | | | |
| ~.4 | Click on the multiselect dropdown within the preference icon container again, possibly to access additional options. | `page.locator(".title.d-flex.align-items-center.font-size-16.font-weight-bold.nunito.title-color > .grid-icons-container > esp-grid-icons-component > .display-grid-icons > div > #preference-iconId > .legend-font > .multiselect-dropdown > .pointer").click()` | | | |
| ~.5 | Click on 'Reset Preference' to reset the preferences to their default state. | `page.get_by_text("Reset Preference").click()` | | | |
```
```markdown
| | **--- TABLE ELEMENT INTERACTIONS ---** | | | | |
| .1 | Click on the element identified by 'path:nth-child(81)', possibly to interact with a specific UI component. The exact purpose is unclear from the locator. | `page.locator("path:nth-child(81)").click()` | | | |
| .2 | Click on the 'User Override Base' text to select or highlight this option in the table. | `page.get_by_text("User Override Base", exact=True).click()` | | | |
| .3 | Click on the 'User Suggested Order Promotion' text to select or highlight this option in the table. | `page.get_by_text("User Suggested Order Promotion", exact=True).click()` | | | |
| .4 | Click on the 'User Override Base' text again, possibly to toggle or reselect this option. | `page.get_by_text("User Override Base", exact=True).click()` | | | |
| .5 | Click on the 'User Suggested Order Promotion' text again, possibly to toggle or reselect this option. | `page.get_by_text("User Suggested Order Promotion", exact=True).click()` | | | |
```
```markdown
| | **--- CHART AND GRAPH INTERACTIONS ---** | | | | |
| .1 | Click on the SVG element, possibly to interact with a chart or graph. The exact purpose is unclear from the locator. | `page.locator("svg").click()` | | | |
| .2 | Click on the SVG element again, likely to perform a secondary interaction with the chart or graph. | `page.locator("svg").click()` | | | |
| .3 | Click on the date '02/03/2026' in the chart to select or highlight data associated with this specific date. | `page.get_by_text("02/03/2026", exact=True).click()` | | | |
| .4 | Click on the text '300K', likely to select or highlight data associated with this value in the chart. | `page.get_by_text("300K").click()` | | | |
| .5 | Click on the text '600K', likely to select or highlight data associated with this value in the chart. | `page.get_by_text("600K").click()` | | | |
| .6 | Click on the bar chart element corresponding to 'path:nth-child(57)', likely to highlight or interact with a specific data point in the chart. | `page.locator("path:nth-child(57)").click()` | | | |
| .7 | Repeat the click action on the same bar chart element ('path:nth-child(57)'), possibly to ensure the interaction is registered. | `page.locator("path:nth-child(57)").click()` | | | |
| .8 | Click on the bar chart element corresponding to 'path:nth-child(99)', likely to highlight or interact with another specific data point in the chart. | `page.locator("path:nth-child(99)").click()` | | | |
| .9 | Click on the bar chart element corresponding to 'path:nth-child(98)', likely to highlight or interact with yet another specific data point in the chart. | `page.locator("path:nth-child(98)").click()` | | | |
```
