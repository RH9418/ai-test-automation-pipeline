import re
from playwright.sync_api import Playwright, sync_playwright, expect


def run(playwright: Playwright) -> None:
    # Launch a Chromium browser instance in non-headless mode for visual debugging.
    browser = playwright.chromium.launch(headless=False)
    # Create a new browser context to isolate session data.
    context = browser.new_context()
    # Open a new page within the browser context.
    page = context.new_page()
    # Navigate to the specified URL for the 'Executive Dashboard' in the demand planning module.
    page.goto("https://stage.bbu.esp.antuit.ai/dp/demand-planning/executive-dashboard?workbookId=4&tabIndex=5")
    # Click on the 'Customer Total columns (0)' text to open the column selection menu.
    page.get_by_text("Customer Total columns (0)").click()
    # Click on the 'Customer Total' text to select the corresponding column.
    page.get_by_text("Customer Total").click()
    # Click on the button within the 'Customer Total columns (0)' card to confirm the selection or perform an action.
    page.locator("esp-card-component").filter(has_text="Customer Total columns (0)").get_by_role("button").click()
    # Click on the 'Filter Columns Input' textbox to focus on it for entering a filter value.
    page.get_by_role("textbox", name="Filter Columns Input").click()
    # Fill the 'Filter Columns Input' textbox with the text 'System' to filter columns containing this keyword.
    page.get_by_role("textbox", name="Filter Columns Input").fill("System")
    # Press 'Enter' to apply the filter and display matching columns.
    page.get_by_role("textbox", name="Filter Columns Input").press("Enter")
    # Click on the first column in the filtered list to select it.
    page.locator(".ag-column-select-column").first.click()
    # Check the checkbox for 'System Forecast Base (Plan)' by toggling it using the SPACE key.
    page.get_by_role("treeitem", name="System Forecast Base (Plan").get_by_label("Press SPACE to toggle").check()
    # Click on the third column in the list to select it.
    page.locator("div:nth-child(3) > .ag-column-select-column").click()
    # Click on the 'Filter Columns Input' textbox again to clear or modify the filter.
    page.get_by_role("textbox", name="Filter Columns Input").click()
    # Clear the 'Filter Columns Input' textbox by filling it with an empty string.
    page.get_by_role("textbox", name="Filter Columns Input").fill("")
    # Press 'Enter' to reset the filter and display all columns.
    page.get_by_role("textbox", name="Filter Columns Input").press("Enter")
    # Click on the 'System Forecast Promotion (' label to select the corresponding column.
    page.get_by_label("System Forecast Promotion (").get_by_text("System Forecast Promotion (").click()
    # Click on the 'System Forecast Total (Plan+1)' label to select the corresponding column.
    page.get_by_label("System Forecast Total (Plan+1").get_by_text("System Forecast Total (Plan+1").click()
    # Click on the 'System Forecast Base (Plan+1)' label to select the corresponding column.
    page.get_by_label("System Forecast Base (Plan+1").get_by_text("System Forecast Base (Plan+1").click()
    # Click on the 'System Forecast Promotion (' label again to toggle its selection.
    page.get_by_label("System Forecast Promotion (").get_by_text("System Forecast Promotion (").click()
    # Click on the '6 Week Gross Units Average' column to select it.
    page.get_by_label("6 Week Gross Units Average").get_by_text("Week Gross Units Average").click()
    # Click on the '6 Week Aged Net Units Average Column' to select it, ensuring the exact match is used.
    page.get_by_label("6 Week Aged Net Units Average Column", exact=True).get_by_text("Week Aged Net Units Average").click()
    # Click on the 'LY 6 Week Aged Net Units' column to select it.
    page.get_by_label("LY 6 Week Aged Net Units").get_by_text("LY 6 Week Aged Net Units").click()
    # Click on the '% Change 6 Week Aged Net' column to select it.
    page.get_by_label("% Change 6 Week Aged Net").get_by_text("% Change 6 Week Aged Net").click()
    # Click on the '6 Week Scan Units Average Column' to select it, ensuring the exact match is used.
    page.get_by_label("6 Week Scan Units Average Column", exact=True).get_by_text("Week Scan Units Average").click()
    # Click on the 'LY 6 Week Scan Units Average' column to select it.
    page.get_by_label("LY 6 Week Scan Units Average").get_by_text("LY 6 Week Scan Units Average").click()
    # Click on the '% Change 6 Week Scan Units' column to select it.
    page.get_by_label("% Change 6 Week Scan Units").get_by_text("% Change 6 Week Scan Units").click()
    # Click on the 'Freshness (6 Week Average)' column to select it.
    page.get_by_label("Freshness (6 Week Average)").get_by_text("Freshness (6 Week Average)").click()
    # Click on the '6 Week Aged Returns Units' column to select it.
    page.get_by_label("6 Week Aged Returns Units").get_by_text("6 Week Aged Returns Units").click()
    # Click on the 'System Forecast Total (Plan Week)' column to select it using its locator.
    page.locator("#ag-169").get_by_text("System Forecast Total (Plan Week)").click()
    page.get_by_label("System Forecast Base (Plan").get_by_text("System Forecast Base (Plan").click()
    page.locator("esp-card-component").filter(has_text="Customer Total columns (0)").get_by_role("button").click()
    # Set up an expectation to handle a file download triggered by the subsequent action.
    with page.expect_download() as download_info:
        # Click on the 'Export' icon within the 'esp-grid-icons-component' to initiate the export process.
        page.locator("esp-grid-icons-component").filter(has_text="Export").locator("#export-iconId").click()
    # Retrieve the downloaded file information after the export action is triggered.
    download = download_info.value
    # Click on the first 'Adjustments' icon (identified by the '.pointer.zeb-adjustments' locator) to open the adjustments menu.
    page.locator(".pointer.zeb-adjustments").first.click()
    # Click on the 'Save Preference' option to save the current preferences.
    page.get_by_text("Save Preference").click()
    # Click on the first 'Adjustments' icon again to reopen the adjustments menu.
    page.locator(".pointer.zeb-adjustments").first.click()
    # Click on the 'Reset Preference' option to reset the preferences to their default state.
    page.get_by_text("Reset Preference").click()
    # Click on the first horizontal scroll container to interact with the grid.
    page.locator(".ag-body-horizontal-scroll-container").first.click()
    # Click on the 'Customers columns (0)' text to open the column configuration panel.
    page.get_by_text("Customers columns (0)").click()
    # Click on the 'Customers' text to select the Customers section.
    page.get_by_text("Customers").click()
    # Click on 'Customers columns (0)' again to toggle the column configuration panel.
    page.get_by_text("Customers columns (0)").click()
    # Click on the button within the 'Customers columns (0)' card to expand its options.
    page.locator("esp-card-component").filter(has_text="Customers columns (0)").get_by_role("button").click()
    # Click on the column panel header to access column selection options.
    page.locator("#ag-87 > .ag-column-panel > .ag-column-select > .ag-column-select-header").click()
    # Fill the 'Filter Columns Input' textbox with the text 'Fresh' to filter columns.
    page.get_by_role("textbox", name="Filter Columns Input").fill("Fresh")
    # Press 'Enter' in the 'Filter Columns Input' textbox to apply the filter.
    page.get_by_role("textbox", name="Filter Columns Input").press("Enter")
    # Check the checkbox to make the column with the label 'Press SPACE to toggle visibility (hidden)' visible.
    page.get_by_role("checkbox", name="Press SPACE to toggle visibility (hidden)").check()
    # Uncheck the 'Toggle All Columns Visibility' checkbox to hide all columns.
    page.get_by_role("checkbox", name="Toggle All Columns Visibility").uncheck()
    # Click on the 'Filter Columns Input' textbox to focus on it.
    page.get_by_role("textbox", name="Filter Columns Input").click()
    # Clear the 'Filter Columns Input' textbox by filling it with an empty string.
    page.get_by_role("textbox", name="Filter Columns Input").fill("")
    # Press 'Enter' in the 'Filter Columns Input' textbox to apply the filter.
    page.get_by_role("textbox", name="Filter Columns Input").press("Enter")
    # Click on the column labeled 'System Forecast Total (Plan Week)' to select it.
    page.locator("#ag-87").get_by_text("System Forecast Total (Plan Week)").click()
    # Click on the column labeled 'System Forecast Base (Plan Week)' to select it.
    page.get_by_label("System Forecast Base (Plan Week) Column").get_by_text("System Forecast Base (Plan").click()
    # Click on the column labeled 'System Forecast Promotion (Plan Week)' to select it.
    page.get_by_label("System Forecast Promotion (Plan Week) Column").get_by_text("System Forecast Promotion (").click()
    # Click on the column labeled 'System Forecast Total (Plan+1)' to select it.
    page.get_by_label("System Forecast Total (Plan+1").get_by_text("System Forecast Total (Plan+1").click()
    # Click on the column labeled 'System Forecast Base (Plan+1)' to select it.
    page.get_by_label("System Forecast Base (Plan+1").get_by_text("System Forecast Base (Plan+1").click()
    # Click on the column labeled 'System Forecast Promotion (Plan+1 Week)' to select it.
    page.get_by_label("System Forecast Promotion (Plan+1 Week) Column").get_by_text("System Forecast Promotion (").click()
    # Click on the column labeled '6 Week Gross Units Average' to select it.
    page.get_by_label("6 Week Gross Units Average").get_by_text("Week Gross Units Average").click()
    # Click on the column labeled '6 Week Aged Net Units Average' to select it.
    page.get_by_label("6 Week Aged Net Units Average Column", exact=True).get_by_text("6 Week Aged Net Units Average", exact=True).click()
    # Click on the column labeled 'LY 6 Week Aged Net Units' to select it.
    page.get_by_label("LY 6 Week Aged Net Units").get_by_text("LY 6 Week Aged Net Units").click()
    # Click on the column labeled '% Change 6 Week Aged Net' to select it.
    page.get_by_label("% Change 6 Week Aged Net").get_by_text("% Change 6 Week Aged Net").click()
    # Click on the column labeled 'LY 6 Week Scan Units Average' to select it.
    page.get_by_label("LY 6 Week Scan Units Average").get_by_text("LY 6 Week Scan Units Average").click()
    # Click on the column labeled '6 Week Scan Units Average' to select it.
    page.get_by_label("6 Week Scan Units Average Column", exact=True).get_by_text("Week Scan Units Average").click()
    # Click on the column labeled '% Change 6 Week Scan Units' to select it.
    page.get_by_label("% Change 6 Week Scan Units").get_by_text("% Change 6 Week Scan Units").click()
    # Click on the column labeled 'Freshness (6 Week Average)' to select it.
    page.get_by_label("Freshness (6 Week Average)").get_by_text("Freshness (6 Week Average)").click()
    # Click on the column labeled '6 Week Aged Returns Units' to select it.
    page.get_by_label("6 Week Aged Returns Units").get_by_text("6 Week Aged Returns Units").click()
    # Click on the button within the 'Customers columns (0)' card to expand its options.
    page.locator("esp-card-component").filter(has_text="Customers columns (0)").get_by_role("button").click()
    # Set up an expectation to handle a file download triggered by the next action.
    with page.expect_download() as download1_info:
        # Click on the 'Export' icon to initiate the export process.
        page.locator("div:nth-child(2) > #export-iconId > .icon-color-toolbar-active").click()
    # Capture the downloaded file information after the export action is triggered.
    download1 = download1_info.value
    # Click on the 'Preferences' dropdown menu to view available options.
    page.locator("div:nth-child(3) > #preference-iconId > .legend-font > .multiselect-dropdown > .pointer").click()
    # Select the 'Save Preference' option from the dropdown to save the current preferences.
    page.get_by_text("Save Preference").click()
    # Reopen the 'Preferences' dropdown menu to access additional options.
    page.locator("div:nth-child(3) > #preference-iconId > .legend-font > .multiselect-dropdown > .pointer").click()
    # Select the 'Reset Preference' option from the dropdown to reset preferences to default.
    page.get_by_text("Reset Preference").click()
    # Click on the 'Customer' column header to sort or filter the column.
    page.locator("esp-row-dimentional-grid").get_by_text("Customer").click()
    # Click on the descending sort icon to sort the 'Customer' column in descending order.
    page.locator(".ag-icon.ag-icon-desc").first.click()
    # Click on the descending sort icon again to toggle the sorting order.
    page.locator(".ag-icon.ag-icon-desc").first.click()
    # Open the filter menu for the 'Customer' column.
    page.locator(".ag-filter-body-wrapper").click()
    # Select the 'Contains' filter option from the filter menu.
    page.get_by_text("Contains").click()
    # Click on the 'Select Field' dropdown and choose the 'Contains' option.
    page.get_by_label("Select Field").get_by_text("Contains").click()
    # Re-select the 'Contains' filter option to confirm the selection.
    page.get_by_text("Contains").click()
    # Select the 'Does not contain' filter option from the filter menu.
    page.get_by_text("Does not contain").click()
    # Re-select the 'Does not contain' filter option to confirm the selection.
    page.get_by_text("Does not contain").click()
    # Select the 'Equals' filter option from the filter menu.
    page.get_by_role("option", name="Equals").click()
    # Re-select the 'Equals' filter option to confirm the selection.
    page.get_by_text("Equals").click()
    # Select the 'Does not equal' filter option from the filter menu.
    page.get_by_role("option", name="Does not equal").click()
    # Re-select the 'Does not equal' filter option to confirm the selection.
    page.get_by_text("Does not equal").click()
    # Select the 'Begins with' filter option from the filter menu.
    page.get_by_role("option", name="Begins with").click()
    # Open the filtering operator dropdown to choose a different operator.
    page.get_by_role("combobox", name="Filtering operator").click()
    # Select the 'Ends with' filter option from the filter menu.
    page.get_by_role("option", name="Ends with").click()
    # Re-select the 'Ends with' filter option to confirm the selection.
    page.get_by_text("Ends with").click()
    # Select the 'Blank' filter option from the filter menu.
    page.get_by_role("option", name="Blank", exact=True).click()
    # Re-select the 'Blank' filter option to confirm the selection.
    page.get_by_text("Blank").click()
    # Select the 'Not blank' filter option from the filter menu.
    page.get_by_role("option", name="Not blank").click()
    # Select the 'AND' logical operator for combining filter conditions.
    page.get_by_text("AND", exact=True).click()
    # Select the 'OR' logical operator for combining filter conditions.
    page.get_by_text("OR", exact=True).click()
    # Re-select the 'Contains' filter option to confirm the selection.
    page.get_by_text("Contains").click()
    # Click on the 'Column Filter' dropdown and choose the 'Contains' option.
    page.get_by_label("Column Filter").get_by_text("Contains").click()
    # Click on the 'Filter Value' textbox to input a value for filtering.
    page.get_by_role("textbox", name="Filter Value").click()
    # Click on the 'Clear' button to clear the current filter value.
    page.get_by_role("button", name="Clear").click()
    # Click on the 'Reset' button to reset all filter settings to default.
    page.get_by_role("button", name="Reset").click()
    # Click on the filter icon in the column header to close the filter menu.
    page.locator(".ag-header-icon.ag-header-cell-filter-button > .ag-icon").first.click()
    # Click on the 'Apply' button to apply the selected filter settings.
    page.get_by_role("button", name="Apply").click()
    # Click on the first occurrence of the '3RD PARTY DISTRIB' text to select it.
    page.locator("span").filter(has_text="3RD PARTY DISTRIB").first.click()
    # Click on the '3RD PARTY DISTRIB' text to confirm the selection.
    page.get_by_text("3RD PARTY DISTRIB").click()
    # Click on the first checkbox in the group to select it.
    page.locator(".ag-group-checkbox").first.click()
    # Check the row with the label 'Press Space to toggle row selection (unchecked)' for '99 CENT'.
    page.get_by_role("gridcell", name="Press Space to toggle row selection (unchecked)  99 CENT").get_by_label("Press Space to toggle row").check()
    # Click on the third occurrence of the 'System Forecast Total (Plan' text to select it.
    page.get_by_text("System Forecast Total (Plan").nth(2).click()
    # Click on the descending sort icon in the column header to toggle the sorting order.
    page.locator(".ag-cell-label-container.ag-header-cell-sorted-desc > .ag-header-icon > .ag-icon").click()
    # Open the filter menu by clicking on the filter body wrapper.
    page.locator(".ag-filter-body-wrapper").click()
    # Select the 'Equals' filter option from the filter menu.
    page.get_by_text("Equals").click()
    # Click on the 'Select Field' dropdown and choose the 'Equals' option.
    page.get_by_label("Select Field").get_by_text("Equals").click()
    # Re-select the 'Equals' filter option to confirm the selection.
    page.get_by_text("Equals").click()
    # Select the 'Does not equal' filter option from the filter menu.
    page.get_by_text("Does not equal").click()
    # Re-select the 'Does not equal' filter option to confirm the selection.
    page.get_by_text("Does not equal").click()
    # Select the 'Greater than' filter option from the filter menu.
    page.get_by_text("Greater than", exact=True).click()
    # Re-select the 'Greater than' filter option to confirm the selection.
    page.get_by_text("Greater than").click()
    # Select the 'Greater than or equal to' filter option from the filter menu.
    page.get_by_text("Greater than or equal to").click()
    # Re-select the 'Greater than or equal to' filter option to confirm the selection.
    page.get_by_text("Greater than or equal to").click()
    # Select the 'Less than' filter option from the filter menu.
    page.get_by_role("option", name="Less than", exact=True).click()
    # Re-select the 'Less than' filter option to confirm the selection.
    page.get_by_text("Less than").click()
    # Select the 'Less than or equal to' filter option from the filter menu.
    page.get_by_text("Less than or equal to").click()
    # Re-select the 'Less than or equal to' filter option to confirm the selection.
    page.get_by_text("Less than or equal to").click()
    # Select the 'Between' filter option from the filter menu.
    page.get_by_role("option", name="Between").click()
    # Re-select the 'Between' filter option to confirm the selection.
    page.get_by_text("Between").click()
    # Select the 'Blank' filter option from the filter menu.
    page.get_by_role("option", name="Blank", exact=True).click()
    # Re-select the 'Blank' filter option to confirm the selection.
    page.get_by_text("Blank").click()
    # Select the 'Not blank' filter option from the filter menu.
    page.get_by_role("option", name="Not blank").click()
    # Click on the 'Clear' button to clear the current filter value.
    page.get_by_role("button", name="Clear").click()
    # Click on the 'Reset' button to reset all filter settings to default.
    page.get_by_role("button", name="Reset").click()
    # Click on the descending sort icon in the column header to toggle the sorting order.
    page.locator(".ag-cell-label-container.ag-header-cell-sorted-desc > .ag-header-icon > .ag-icon").click()
    # Click on the 'Apply' button to apply the selected filter settings.
    page.get_by_role("button", name="Apply").click()
    # Click on the descending sort icon in the column header to sort the column in descending order.
    page.locator(".ag-cell-label-container.ag-header-cell-sorted-desc > .ag-header-cell-label > .ag-sort-indicator-container > .ag-sort-indicator-icon.ag-sort-descending-icon > .ag-icon").click()
    # Click on the ascending sort icon in the column header to sort the column in ascending order.
    page.locator(".ag-cell-label-container.ag-header-cell-sorted-asc > .ag-header-cell-label > .ag-sort-indicator-container > .ag-sort-indicator-icon.ag-sort-ascending-icon > .ag-icon").click()
    # Click on the 'System Forecast Base (Plan Week)' column header to select it.
    page.get_by_text("System Forecast Base (Plan Week)").click()
    # Click on the descending sort icon in the column header to sort the column in descending order again.
    page.locator(".ag-cell-label-container.ag-header-cell-sorted-desc > .ag-header-cell-label > .ag-sort-indicator-container > .ag-sort-indicator-icon.ag-sort-descending-icon > .ag-icon").click()
    # Click on the descending sort icon in the column header to toggle the sorting order.
    page.locator(".ag-cell-label-container.ag-header-cell-sorted-desc > .ag-header-cell-label > .ag-sort-indicator-container > .ag-sort-indicator-icon.ag-sort-descending-icon > .ag-icon").click()
    # Click on the filter button in the column header to open the filter menu.
    page.locator(".ag-header-icon.ag-header-cell-filter-button.ag-has-popup-positioned-under > .ag-icon").click()
    # Click on the filter body wrapper to open the advanced filtering options.
    page.locator(".ag-filter-body-wrapper").click()
    # Click on the 'Filtering operator' dropdown to select a filtering condition.
    page.get_by_role("combobox", name="Filtering operator").click()
    # Select the 'Equals' option from the filtering operator dropdown.
    page.get_by_label("Select Field").get_by_text("Equals").click()
    page.get_by_text("Equals").click()
    # Select the 'Does not equal' option from the filtering operator dropdown.
    page.get_by_text("Does not equal").click()
    page.get_by_text("Does not equal").click()
    # Select the 'Greater than' option from the filtering operator dropdown.
    page.get_by_role("option", name="Greater than", exact=True).click()
    page.get_by_text("Greater than").click()
    # Select the 'Less than' option from the filtering operator dropdown.
    page.get_by_role("option", name="Less than", exact=True).click()
    page.get_by_text("Less than").click()
    # Select the 'Greater than or equal to' option from the filtering operator dropdown.
    page.get_by_text("Greater than or equal to").click()
    page.get_by_text("Greater than or equal to").click()
    # Select the 'Less than or equal to' option from the filtering operator dropdown.
    page.get_by_role("option", name="Less than or equal to").click()
    page.get_by_text("Less than or equal to").click()
    # Select the 'Between' option from the filtering operator dropdown.
    page.get_by_role("option", name="Between").click()
    page.get_by_text("Between").click()
    # Select the 'Blank' option from the filtering operator dropdown.
    page.get_by_role("option", name="Blank", exact=True).click()
    page.get_by_text("Blank").click()
    # Select the 'Not blank' option from the filtering operator dropdown.
    page.get_by_role("option", name="Not blank").click()
    # Click on the 'AND' radio button to set the filter condition to 'AND'.
    page.locator(".ag-labeled.ag-label-align-right.ag-radio-button").first.click()
    # Click on the 'OR' radio button to set the filter condition to 'OR'.
    page.locator(".ag-labeled.ag-label-align-right.ag-radio-button.ag-input-field.ag-filter-condition-operator.ag-filter-condition-operator-or").click()
    # Click on the 'Filter Value' input field to enter a value for filtering.
    page.get_by_role("spinbutton", name="Filter Value").click()
    # Fill the 'Filter Value' input field with the value '2'.
    page.get_by_role("spinbutton", name="Filter Value").fill("2")
    # Press 'Enter' to apply the entered filter value.
    page.get_by_role("spinbutton", name="Filter Value").press("Enter")
    page.get_by_role("spinbutton", name="Filter Value").click()
    # Click on the 'Apply' button to apply the selected filter criteria.
    page.get_by_role("button", name="Apply").click()
    # Click on the active filter icon to open the filter options for the column.
    page.locator(".ag-header-icon.ag-header-cell-filter-button.ag-filter-active > .ag-icon").click()
    # Click on the 'Reset' button to reset the filter settings to their default state.
    page.get_by_role("button", name="Reset").click()
    # Click on the column header icon to open sorting or additional options for the column.
    page.locator(".ag-header-cell.ag-header-parent-hidden.ag-header-cell-sortable.ag-header-background.ag-focus-managed.ag-header-active > .ag-header-cell-comp-wrapper > .ag-cell-label-container > .ag-header-icon > .ag-icon").click()
    # Click on the 'Clear' button to remove all applied filters from the column.
    page.get_by_role("button", name="Clear").click()
    # Click on the 'Customers columns (0)' text to open the column options.
    page.get_by_text("Customers columns (0)").click()
    # Click on the pagination element to interact with the pagination controls.
    page.locator("esp-row-dimentional-grid #paginationId").click()
    # Click on the 'Showing 10 out of' text to view the current row display information.
    page.get_by_text("Showing 10 out of").click()
    page.get_by_text("Showing 10 out of 138 12345").click()
    # Click on the 'View 10 row(s)' option to set the number of rows displayed to 10.
    page.get_by_text("View 10 row(s)").first.click()
    page.locator("span").filter(has_text=re.compile(r"^View 10 row\(s\)$")).click()
    # Click on the 'Rows per page' text to open the dropdown for selecting the number of rows displayed per page.
    page.get_by_text("Rows per page").click()
    page.get_by_text("Showing 10 out of 138 12345").click()
    # Click on the list item with the text '1' to navigate to the first page of the pagination.
    page.get_by_role("listitem").filter(has_text=re.compile(r"^1$")).click()
    # Click on the pagination link with the text '2' to navigate to the second page.
    page.locator("a").filter(has_text="2").click()
    # Click on the left chevron icon to navigate to the previous page in the pagination.
    page.locator(".zeb-chevron-left").click()
    page.get_by_text("12345...14").click()
    page.get_by_text("12345...14").click()
    # Click on the right chevron icon to navigate to the next page in the pagination.
    page.locator(".pagination-next > .zeb-chevron-right").click()
    # Click on the 'Last' navigation button to navigate to the last page in the pagination.
    page.locator(".zeb-nav-to-last").click()
    page.locator(".w-100.p-h-16").click()
    # Click on the 'View 20 row(s)' option to set the number of rows displayed to 20.
    page.locator("div").filter(has_text=re.compile(r"^View 20 row\(s\)$")).first.click()
    # Click on the 'Showing 20 out of' text to view the updated row display information.
    page.get_by_text("Showing 20 out of").click()
    # Select the grid cell labeled 'Press Space to toggle row selection (unchecked)' for the row '3RD PARTY DISTRIB'.
    page.get_by_role("gridcell", name="Press Space to toggle row selection (unchecked)  3RD PARTY DISTRIB").get_by_label("Press Space to toggle row").check()
    # Click on the 'FilterTime Latest Order &' text to open the filter options.
    page.get_by_text("FilterTime Latest Order &").click()
    # Click on the 'Filter' button within a div element to apply or modify filters.
    page.locator("div").filter(has_text=re.compile(r"^Filter$")).click()
    # Click on the 'Time' text to select the time filter option.
    page.get_by_text("Time").click()
    # Click on the dropdown labeled '.w-100.p-h-16.p-v-8.dropdown-label.background-white' to open the filter options.
    page.locator(".w-100.p-h-16.p-v-8.dropdown-label.background-white").click()
    # Select the filter option labeled 'Latest Order & Plan Week' from the dropdown.
    page.locator("span").filter(has_text="Latest Order & Plan Week").click()
    # Click on the 'FilterTime Latest Order &' text again to confirm or apply the selected filter.
    page.get_by_text("FilterTime Latest Order &").click()
    # Click on the 'Daily Summary Customer:3RD' text to navigate to the daily summary for the specified customer.
    page.get_by_text("Daily Summary Customer:3RD").click()
    # Click on the 'Daily Summary' text to view the daily summary section.
    page.get_by_text("Daily Summary").click()
    # Click on the 'Customer' text (exact match) to interact with the customer-specific options.
    page.get_by_text("Customer", exact=True).nth(2).click()
    # Click on the 'Customer:3RD PARTY DISTRIB' text to select the specific customer.
    page.get_by_text("Customer:3RD PARTY DISTRIB").first.click()
    # Click on the '3RD PARTY DISTRIB' text (second occurrence) to confirm or refine the selection.
    page.get_by_text("3RD PARTY DISTRIB").nth(1).click()
    # Click on the dropdown to open the list of options for selection.
    page.locator(".wr-20.font-weight-normal > esp-multiselect-dropdown > .multiselect-dropdown > div > .w-100").click()
    # Select the first option from the dropdown list.
    page.locator(".d-flex.dropdown-option").first.click()
    # Re-select the first option from the dropdown list, possibly to confirm the selection.
    page.locator(".d-flex.dropdown-option").first.click()
    # Click on a specific dropdown option with additional alignment and padding styles.
    page.locator(".d-flex.dropdown-option.align-items-center.p-v-5.p-l-32 > .d-flex").first.click()
    # Click on the first checkbox to select it.
    page.locator(".d-flex.flex-column.justify-content-center.font-size-10.align-items-center.checkbox-v2.m-r-10.zeb-check").first.click()
    # Click on the first checkbox again, possibly to toggle or confirm the selection.
    page.locator(".d-flex.flex-column.justify-content-center.font-size-10.align-items-center.checkbox-v2.m-r-10.zeb-check").first.click()
    # Click on the first checkbox again, possibly as part of a repeated action.
    page.locator(".d-flex.flex-column.justify-content-center.font-size-10.align-items-center.checkbox-v2.m-r-10.zeb-check").first.click()
    page.locator(".d-flex.flex-column.justify-content-center.font-size-10.align-items-center.checkbox-v2.m-r-10.zeb-check").first.click()
    page.locator(".d-flex.flex-column.justify-content-center.font-size-10.align-items-center.checkbox-v2.m-r-10.zeb-check").first.click()
    page.locator(".d-flex.flex-column.justify-content-center.font-size-10.align-items-center.checkbox-v2.m-r-10.zeb-check").first.click()
    page.locator(".d-flex.flex-column.justify-content-center.font-size-10.align-items-center.checkbox-v2.m-r-10.zeb-check").first.click()
    page.locator(".d-flex.flex-column.justify-content-center.font-size-10.align-items-center.checkbox-v2.m-r-10.zeb-check").first.click()
    page.locator(".d-flex.flex-column.justify-content-center.font-size-10.align-items-center.checkbox-v2.m-r-10.zeb-check").first.click()
    page.locator(".d-flex.flex-column.justify-content-center.font-size-10.align-items-center.checkbox-v2.m-r-10.zeb-check").first.click()
    page.locator(".d-flex.flex-column.justify-content-center.font-size-10.align-items-center.checkbox-v2.m-r-10.zeb-check").first.click()
    page.locator(".d-flex.flex-column.justify-content-center.font-size-10.align-items-center.checkbox-v2.m-r-10.zeb-check").first.click()
    page.locator(".d-flex.flex-column.justify-content-center.font-size-10.align-items-center.checkbox-v2.m-r-10.zeb-check").first.click()
    # Click on a selected dropdown option to finalize or confirm the selection.
    page.locator(".d-flex.dropdown-option.align-items-center.p-v-5.p-l-32.p-r-16.selected").first.click()
    # Click on the 'Aged Net Units (CW-5)' option to select it from the dropdown.
    page.get_by_text("Aged Net Units (CW-5)", exact=True).click()
    # Click on the 'Aged Net Units (CW-6)' option to select it from the dropdown.
    page.get_by_text("Aged Net Units (CW-6)", exact=True).click()
    # Click on the 'Scan Units (CW-4)' option to select it from the dropdown.
    page.get_by_text("Scan Units (CW-4)", exact=True).click()
    # Click on the second occurrence of the 'Scan Units (CW-3)' option to select it.
    page.get_by_text("Scan Units (CW-3)").nth(1).click()
    # Click on the 'Scan Units (CW-5)' option to select it from the dropdown.
    page.get_by_text("Scan Units (CW-5)", exact=True).click()
    # Click on the 'Scan Units (CW-6)' option within a span element to select it.
    page.locator("span").filter(has_text="Scan Units (CW-6)").click()
    # Click on the 'Daily Summary Customer:3RD' option to select it from the dropdown.
    page.get_by_text("Daily Summary Customer:3RD").click()
    # Click on the button within the 'Daily Summary Customer:3RD' card to open its options.
    page.locator("esp-card-component").filter(has_text="Daily Summary Customer:3RD").get_by_role("button").click()
    # Click on the textbox labeled 'Filter Columns Input' to activate the column filter input field.
    page.get_by_role("textbox", name="Filter Columns Input").click()
    # Uncheck the checkbox labeled 'Toggle All Columns Visibility' to hide all columns.
    page.get_by_role("checkbox", name="Toggle All Columns Visibility").uncheck()
    # Check the checkbox labeled 'Toggle All Columns Visibility' to make all columns visible again.
    page.get_by_role("checkbox", name="Toggle All Columns Visibility").check()
    # Click on the '/01(Sun)' label within the '/01(Sun) Column' to toggle its visibility.
    page.get_by_label("/01(Sun) Column").get_by_text("/01(Sun)").click()
    # Click on the '/02(Mon)' label within the '/02(Mon) Column' to toggle its visibility.
    page.get_by_label("/02(Mon) Column").get_by_text("/02(Mon)").click()
    # Uncheck the checkbox for the '/03(Tue) Column' to hide this column.
    page.get_by_role("treeitem", name="/03(Tue) Column").get_by_label("Press SPACE to toggle visibility (visible)").uncheck()
    # Uncheck the checkbox for the '/05(Thu) Column' to hide this column.
    page.get_by_role("treeitem", name="/05(Thu) Column").get_by_label("Press SPACE to toggle visibility (visible)").uncheck()
    # Uncheck the checkbox for the '/04(Wed) Column' to hide this column.
    page.get_by_role("treeitem", name="/04(Wed) Column").get_by_label("Press SPACE to toggle visibility (visible)").uncheck()
    # Wait for a file download to be triggered when the export icon is clicked.
    with page.expect_download() as download2_info:
        # Click on the export icon to initiate the download of the grid data.
        page.locator("span:nth-child(6) > esp-grid-icons-component > .display-grid-icons > div:nth-child(2) > #export-iconId > .icon-color-toolbar-active").click()
    download2 = download2_info.value
    # Click on the preferences icon to open the preferences dropdown menu.
    page.locator("span:nth-child(6) > esp-grid-icons-component > .display-grid-icons > div:nth-child(3) > #preference-iconId > .legend-font > .multiselect-dropdown > .pointer").click()
    # Select the 'Save Preference' option from the preferences dropdown to save the current grid settings.
    page.get_by_text("Save Preference").click()
    # Click on the preferences icon again to reopen the preferences dropdown menu.
    page.locator("span:nth-child(6) > esp-grid-icons-component > .display-grid-icons > div:nth-child(3) > #preference-iconId > .legend-font > .multiselect-dropdown > .pointer").click()
    # Select the 'Reset Preference' option from the preferences dropdown to reset the grid settings to default.
    page.get_by_text("Reset Preference").click()
    # Click on the preferences icon once more to reopen the preferences dropdown menu.
    page.locator("span:nth-child(6) > esp-grid-icons-component > .display-grid-icons > div:nth-child(3) > #preference-iconId > .legend-font > .multiselect-dropdown > .pointer").click()
    # Click on the button within the 'Daily Summary Customer:3RD' card to open the dropdown menu for further actions.
    page.locator("esp-card-component").filter(has_text="Daily Summary Customer:3RD").get_by_role("button").click()
    # Click on the dropdown field to expand the multiselect options for filtering.
    page.locator(".wr-20.font-weight-normal > esp-multiselect-dropdown > .multiselect-dropdown > div > .w-100").click()
    # Select the 'Select All' option to include all available items in the filter.
    page.get_by_text("Select All").click()
    # Click on the 'Daily Summary Customer:3RD' option to specifically filter by this customer.
    page.get_by_text("Daily Summary Customer:3RD").click()
    # Click on the header cell to interact with the first column in the grid.
    page.locator(".ag-header-cell.ag-column-first.ag-header-parent-hidden.ag-header-background.ag-focus-managed.ag-header-active > .ag-header-cell-comp-wrapper > .ag-cell-label-container > .ag-header-cell-label").click()
    # Click on the 'User Suggested Order Total' column header to sort or interact with this column.
    page.get_by_text("User Suggested Order Total").click()
    # Click on the first icon (likely a dropdown or action button) within the grid.
    page.locator("i").first.click()
    # Click on the 'User Override Total' column header to sort or interact with this column.
    page.get_by_text("User Override Total").click()
    # Click on the third icon (likely a dropdown or action button) within the grid.
    page.locator("i").nth(2).click()
    # Click on the 'Gross Units (CW-3)' column header within the grid to interact with it.
    page.locator("esp-column-dimentional-grid").get_by_text("Gross Units (CW-3)").click()
    # Click on the first 'Gross Units (CW-3)' text element to interact with it.
    page.locator("span").filter(has_text="Gross Units (CW-3)").first.click()
    # Click on the sixth icon (likely a dropdown or action button) within the grid.
    page.locator("i").nth(5).click()
    # Click on the 'Aged Net Units (CW-3)' column header within the grid to interact with it.
    page.locator("esp-column-dimentional-grid").get_by_text("Aged Net Units (CW-3)").click()
    # Click on the expand/collapse icon within the last left-pinned cell of the grid to expand or collapse the row.
    page.locator(".ag-cell-value.ag-cell.ag-cell-not-inline-editing.ag-cell-normal-height.ag-cell-last-left-pinned.ag-column-first.ag-cell-override-normal.notosans-overwrite.no-border.ag-cell-focus > .ag-cell-wrapper > .ag-group-contracted > .zeb-chevron-right").click()
    # Click on the expand icon (chevron) in the first row of the grid to expand the group.
    page.locator(".ag-row-no-focus.ag-row-not-inline-editing.ag-row.ag-row-level-0.ag-row-group.ag-row-group-contracted.ag-row-position-absolute.ag-row-even.ag-row-hover > .ag-cell-value > .ag-cell-wrapper > .ag-group-contracted > .zeb-chevron-right").click()
    # Click on the 'Scan Units (CW-3)' column header within the grid to interact with it.
    page.locator("esp-column-dimentional-grid").get_by_text("Scan Units (CW-3)").click()
    # Click on the 'Daily Trend Customer:3RD' text element to interact with the trend analysis for this customer.
    page.get_by_text("Daily Trend Customer:3RD").click()
    # Click on an SVG element, possibly to interact with a chart or graphical element.
    page.locator("svg").click()
    # Click on the title element to interact with or navigate to a specific section.
    page.locator(".title.d-flex.align-items-center.font-size-16.font-weight-bold.nunito.title-color > .p-l-40").click()
    # Click on the 'Customer' label within the line-bar chart to filter or interact with customer-specific data.
    page.locator("dp-line-bar-chart").get_by_text("Customer", exact=True).click()
    # Click on the 'Customer:3RD PARTY DISTRIB' label within the line-bar chart to filter or interact with this specific customer data.
    page.locator("dp-line-bar-chart").get_by_text("Customer:3RD PARTY DISTRIB").click()
    # Click on a specific path element within the chart, possibly to highlight or interact with a data point.
    page.locator("path:nth-child(79)").click()
    # Click on the first occurrence of the 'User Suggested Order Base' text to interact with it.
    page.get_by_text("User Suggested Order Base,").first.click()
    # Click on the 'User Suggested Order Base' text element to interact with it.
    page.locator("span").filter(has_text="User Suggested Order Base").click()
    # Click on the 'User Suggested Order Promotion' text element to interact with it.
    page.locator("span").filter(has_text="User Suggested Order Promotion").click()
    # Click on the 'User Override Base' text element to interact with it.
    page.locator("span").filter(has_text="User Override Base").click()
    # Click on the 'User Override Promotion' text element to interact with it.
    page.locator("span").filter(has_text="User Override Promotion").click()
    # Click on the 'Gross Units (CW-3)' text element within the line-bar chart to interact with it.
    page.locator("dp-line-bar-chart span").filter(has_text="Gross Units (CW-3)").click()
    # Click on the 'Gross Units (CW-4)' text element within the line-bar chart to interact with it.
    page.locator("dp-line-bar-chart").get_by_text("Gross Units (CW-4)").click()
    # Click on the seventh div element within the overflow container to interact with it.
    page.locator(".overflow-auto > div:nth-child(7)").click()
    # Click on the eighth div element with a flex layout to interact with it.
    page.locator("div:nth-child(8) > .d-flex").click()
    # Click on the ninth div element within the overflow container to interact with it.
    page.locator(".overflow-auto > div:nth-child(9)").click()
    # Click on the tenth div element with a flex layout to interact with it.
    page.locator("div:nth-child(10) > .d-flex").click()
    # Click on the 'Aged Net Units (CW-5)' text element within the line-bar chart to interact with it.
    page.locator("dp-line-bar-chart").get_by_text("Aged Net Units (CW-5)").click()
    # Click on the 'Aged Net Units (CW-6)' text element within the line-bar chart to interact with it.
    page.locator("dp-line-bar-chart").get_by_text("Aged Net Units (CW-6)").click()
    # Click on the 'Scan Units (CW-3)' text element within the line-bar chart to interact with it.
    page.locator("dp-line-bar-chart span").filter(has_text="Scan Units (CW-3)").click()
    # Click on the 'Scan Units (CW-4)' text element within the line-bar chart to interact with it.
    page.locator("dp-line-bar-chart").get_by_text("Scan Units (CW-4)").click()
    # Click on the fifteenth div element within the overflow container to interact with it.
    page.locator(".overflow-auto > div:nth-child(15)").click()
    # Click on the 'Scan Units (CW-6)' text element within the line-bar chart to interact with it.
    page.locator("dp-line-bar-chart").get_by_text("Scan Units (CW-6)").click()
    # Click on the dropdown element within the ellipses container to interact with the multiselect options.
    page.locator(".ellipses > esp-multiselect-dropdown > .multiselect-dropdown > div > .w-100").click()
    # Click on the 'Daily Trend Customer:3RD' text element to interact with the trend analysis for this customer.
    page.get_by_text("Daily Trend Customer:3RD").click()
    # Click on the preference icon within the grid icons container to open the preferences dropdown.
    page.locator(".title.d-flex.align-items-center.font-size-16.font-weight-bold.nunito.title-color > .grid-icons-container > esp-grid-icons-component > .display-grid-icons > div > #preference-iconId > .legend-font > .multiselect-dropdown > .pointer").click()
    # Click on the 'Save Preference' option to save the current preferences.
    page.get_by_text("Save Preference").click()
    # Click on the preference icon again to open the preferences dropdown.
    page.locator(".title.d-flex.align-items-center.font-size-16.font-weight-bold.nunito.title-color > .grid-icons-container > esp-grid-icons-component > .display-grid-icons > div > #preference-iconId > .legend-font > .multiselect-dropdown > .pointer").click()
    # Click on the 'Reset Preference' option to reset the preferences to default.
    page.get_by_text("Reset Preference").click()
    # Click on an SVG element, possibly to interact with a chart or graphical element.
    page.locator("svg").click()
    # Click on the '02/01/' text within the SVG element, likely to select a specific date.
    page.locator("svg").get_by_text("02/01/").click()
    # Click on the '02/02/' text to select another specific date.
    page.get_by_text("02/02/").click()
    # Click on the '02/03/' text to select another specific date.
    page.get_by_text("02/03/").click()
    # Click on an SVG element, possibly to interact with a chart or graphical element again.
    page.locator("svg").click()
    # Click on the 67th path element within the SVG, possibly to interact with a specific data point.
    page.locator("path:nth-child(67)").click()
    # Click on the 'User Override Promotion' text element to interact with it.
    page.get_by_text("User Override Promotion", exact=True).click()
    # Click on the 'User Override Base' text element to interact with it.
    page.get_by_text("User Override Base", exact=True).click()
    # Click on the 79th path element within the SVG, possibly to interact with a specific data point.
    page.locator("path:nth-child(79)").click()
    # Click on the 96th path element within the SVG, possibly to interact with a specific data point.
    page.locator("path:nth-child(96)").click()
    # Click on the 102nd path element within the SVG, possibly to interact with a specific data point.
    page.locator("path:nth-child(102)").click()
    # Click on an SVG element, possibly to interact with a chart or graphical element again.
    page.locator("svg").click()
    # Click on the 102nd path element within the SVG again, possibly to interact with the same data point.
    page.locator("path:nth-child(102)").click()

    # ---------------------
    # Close the browser context to end the session and release resources associated with it.
    context.close()
    # Close the browser instance to terminate the browser process completely.
    browser.close()


# Initialize the Playwright library to start a new automation session.
with sync_playwright() as playwright:
    # Call the 'run' function, passing the Playwright instance to execute the defined automation tasks.
    run(playwright)
