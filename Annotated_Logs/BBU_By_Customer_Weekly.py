import re
from playwright.sync_api import Playwright, sync_playwright, expect


def run(playwright: Playwright) -> None:
    # Launch a Chromium browser instance in non-headless mode.
    browser = playwright.chromium.launch(headless=False)
    # Create a new browser context to isolate session data.
    context = browser.new_context()
    # Open a new page within the created browser context.
    page = context.new_page()
    # Navigate to the specified URL for the 'Executive Dashboard' in the demand planning application.
    page.goto("https://stage.bbu.esp.antuit.ai/dp/demand-planning/executive-dashboard?workbookId=4&tabIndex=4")
    # Click on the 'Customer Total columns (0)' text to open the configuration panel for customer total columns.
    page.get_by_text("Customer Total columns (0)").click()
    # Click on the 'Customer Total' text to focus on the customer total section.
    page.get_by_text("Customer Total").click()
    # Click on the button within the 'Customer Total columns (0)' card to open the column visibility settings.
    page.locator("esp-card-component").filter(has_text="Customer Total columns (0)").get_by_role("button").click()
    # Uncheck the 'Toggle All Columns Visibility' checkbox to hide all columns.
    page.get_by_role("checkbox", name="Toggle All Columns Visibility").uncheck()
    # Click on the 'Filter Columns Input' textbox to prepare for filtering specific columns.
    page.get_by_role("textbox", name="Filter Columns Input").click()
    # Check the 'Toggle All Columns Visibility' checkbox to make all columns visible again.
    page.get_by_role("checkbox", name="Toggle All Columns Visibility").check()
    # Click on the 'Filter Columns Input' textbox to focus on it for input.
    page.get_by_role("textbox", name="Filter Columns Input").click()
    # Fill the 'Filter Columns Input' textbox with the text 'System Forecast' to filter columns by this keyword.
    page.get_by_role("textbox", name="Filter Columns Input").fill("System Forecast")
    # Press 'Enter' in the 'Filter Columns Input' textbox to apply the filter.
    page.get_by_role("textbox", name="Filter Columns Input").press("Enter")
    # Click on the first column in the filtered list to select it.
    page.locator(".ag-column-select-column").first.click()
    # Check the checkbox for the 'System Forecast Base (Plan)' column to make it visible.
    page.get_by_role("treeitem", name="System Forecast Base (Plan").get_by_label("Press SPACE to toggle").check()
    # Click on the 'Filter Columns Input' textbox to clear the filter.
    page.get_by_role("textbox", name="Filter Columns Input").click()
    # Clear the 'Filter Columns Input' textbox to reset the filter.
    page.get_by_role("textbox", name="Filter Columns Input").fill("")
    # Press 'Enter' in the 'Filter Columns Input' textbox to confirm clearing the filter.
    page.get_by_role("textbox", name="Filter Columns Input").press("Enter")
    # Click on the 'System Forecast Total (Plan Week)' column to select it.
    page.locator("#ag-839").get_by_text("System Forecast Total (Plan Week)").click()
    # Click on the 'System Forecast Base (Plan)' column to select it.
    page.get_by_label("System Forecast Base (Plan").get_by_text("System Forecast Base (Plan").click()
    # Click on the 'System Forecast Promotion (' column to select it.
    page.get_by_label("System Forecast Promotion (").get_by_text("System Forecast Promotion (").click()
    # Click on the 'System Forecast Total (Plan+1)' column to select it.
    page.get_by_label("System Forecast Total (Plan+1").get_by_text("System Forecast Total (Plan+1").click()
    # Click on the 'System Forecast Base (Plan+1)' column to select it.
    page.get_by_label("System Forecast Base (Plan+1").get_by_text("System Forecast Base (Plan+1").click()
    # Click on the 'System Forecast Base (Plan+1)' column again to confirm selection.
    page.get_by_label("System Forecast Base (Plan+1").get_by_text("System Forecast Base (Plan+1").click()
    # Click on the 'LY 6 Week Aged Net Units' column to select it.
    page.get_by_label("LY 6 Week Aged Net Units").get_by_text("LY 6 Week Aged Net Units").click()
    # Click on the '% Change 6 Week Aged Net' column to select it.
    page.get_by_label("% Change 6 Week Aged Net").get_by_text("% Change 6 Week Aged Net").click()
    # Click on the '6 Week Scan Units Average Column' to select it.
    page.get_by_label("6 Week Scan Units Average Column", exact=True).get_by_text("Week Scan Units Average").click()
    # Click on the 'LY 6 Week Scan Units Average' column to select it.
    page.get_by_label("LY 6 Week Scan Units Average").get_by_text("LY 6 Week Scan Units Average").click()
    # Click on the '% Change 6 Week Scan Units' column to select it.
    page.get_by_label("% Change 6 Week Scan Units").get_by_text("% Change 6 Week Scan Units").click()
    # Click on the 'Freshness (6 Week Average)' column to select it.
    page.get_by_label("Freshness (6 Week Average)").get_by_text("Freshness (6 Week Average)").click()
    # Uncheck the checkbox to toggle visibility for a specific column.
    page.get_by_role("checkbox", name="Press SPACE to toggle visibility (visible)").uncheck()
    # Check the 'Toggle All Columns Visibility' checkbox to make all columns visible again.
    page.get_by_role("checkbox", name="Toggle All Columns Visibility").check()
    # Click on the button within the 'Customer Total columns (0)' card to close the column visibility settings.
    page.locator("esp-card-component").filter(has_text="Customer Total columns (0)").get_by_role("button").click()
    # Set up an expectation to handle a file download triggered by subsequent actions.
    with page.expect_download() as download_info:
        # Click on the download button (identified by '.icon-color-toolbar-active.zeb-download-underline') to initiate the download process.
        page.locator(".icon-color-toolbar-active.zeb-download-underline").first.click()
    # Retrieve the download information after the download is triggered.
    download = download_info.value
    # Click on the adjustments button (identified by '.pointer.zeb-adjustments') to open the preferences menu.
    page.locator(".pointer.zeb-adjustments").first.click()
    # Click on the 'Save Preference' option to save the current settings.
    page.locator("div").filter(has_text=re.compile(r"^Save Preference$")).first.click()
    # Click on the adjustments button again to reopen the preferences menu.
    page.locator(".pointer.zeb-adjustments").first.click()
    # Click on the 'Reset Preference' option to reset the settings to their default values.
    page.get_by_text("Reset Preference").click()
    # Click on the horizontal scroll container to ensure the view is scrolled to the appropriate section.
    page.locator(".ag-body-horizontal-scroll-container").first.click()
    # Click on the 'Customers columns (0)' button to open the configuration panel for customer columns.
    page.get_by_text("Customers columns (0)").click()
    # Click on the 'Customers' section to expand and view its options.
    page.get_by_text("Customers").click()
    # Click on the button within the 'Customers columns (0)' card to access column configuration options.
    page.locator("esp-card-component").filter(has_text="Customers columns (0)").get_by_role("button").click()
    # Click on the 'Filter Columns Input' textbox to focus on it for entering a filter value.
    page.get_by_role("textbox", name="Filter Columns Input").click()
    # Uncheck the 'Toggle All Columns Visibility' checkbox to hide all columns.
    page.get_by_role("checkbox", name="Toggle All Columns Visibility").uncheck()
    # Check the 'Toggle All Columns Visibility' checkbox to make all columns visible again.
    page.get_by_role("checkbox", name="Toggle All Columns Visibility").check()
    # Click on the 'Filter Columns Input' textbox to focus on it for entering a filter value.
    page.get_by_role("textbox", name="Filter Columns Input").click()
    # Enter the value '6' into the 'Filter Columns Input' textbox to filter columns containing '6'.
    page.get_by_role("textbox", name="Filter Columns Input").fill("6")
    # Press 'Enter' in the 'Filter Columns Input' textbox to apply the filter.
    page.get_by_role("textbox", name="Filter Columns Input").press("Enter")
    # Check the checkbox to make the 'Week Gross Units Average Column' visible.
    page.get_by_role("treeitem", name="Week Gross Units Average Column").get_by_label("Press SPACE to toggle visibility (hidden)").check()
    # Check the checkbox to make the '6 Week Aged Net Units Average Column' visible.
    page.get_by_role("treeitem", name="6 Week Aged Net Units Average Column", exact=True).get_by_label("Press SPACE to toggle visibility (hidden)").check()
    # Check the checkbox to make the 'LY 6 Week Aged Net Units' column visible.
    page.get_by_role("treeitem", name="LY 6 Week Aged Net Units").get_by_label("Press SPACE to toggle visibility (hidden)").check()
    # Check the checkbox to make the '% Change 6 Week Aged Net' column visible.
    page.get_by_role("treeitem", name="% Change 6 Week Aged Net").get_by_label("Press SPACE to toggle visibility (hidden)").check()
    # Click on the '6 Week Scan Units Average' column in the column list to select it.
    page.get_by_label("Column List 9 Columns").get_by_text("6 Week Scan Units Average", exact=True).click()
    # Click on the 'LY 6 Week Scan Units Average' column in the column list to select it.
    page.get_by_label("LY 6 Week Scan Units Average").get_by_text("LY 6 Week Scan Units Average").click()
    # Click on the '% Change 6 Week Scan Units' column in the column list to select it.
    page.get_by_label("% Change 6 Week Scan Units").get_by_text("% Change 6 Week Scan Units").click()
    # Click on the '6 Week Aged Returns Units' column in the column list to select it.
    page.get_by_label("6 Week Aged Returns Units").get_by_text("6 Week Aged Returns Units").click()
    # Click on the 'Filter Columns Input' textbox to clear the filter.
    page.get_by_role("textbox", name="Filter Columns Input").click()
    # Clear the 'Filter Columns Input' textbox to remove the filter.
    page.get_by_role("textbox", name="Filter Columns Input").fill("")
    # Press 'Enter' in the 'Filter Columns Input' textbox to confirm clearing the filter.
    page.get_by_role("textbox", name="Filter Columns Input").press("Enter")
    # Click on the first column in the column panel to select it.
    page.locator("#ag-989 > .ag-column-panel > .ag-column-select > .ag-column-select-list > .ag-virtual-list-viewport > .ag-virtual-list-container > div > .ag-column-select-column").first.click()
    # Click on the 'System Forecast Base (Plan Week)' column in the column list to select it.
    page.get_by_label("System Forecast Base (Plan Week) Column").get_by_text("System Forecast Base (Plan").click()
    # Click on the 'System Forecast Promotion (Plan Week)' column in the column list to select it.
    page.get_by_label("System Forecast Promotion (Plan Week) Column").get_by_text("System Forecast Promotion (").click()
    # Click on the 'System Forecast Total (Plan+1)' column in the column list to select it.
    page.get_by_label("System Forecast Total (Plan+1").get_by_text("System Forecast Total (Plan+1").click()
    # Click on the 'System Forecast Base (Plan+1)' column in the column list to select it.
    page.get_by_label("System Forecast Base (Plan+1").get_by_text("System Forecast Base (Plan+1").click()
    # Click on the 'System Forecast Promotion (Plan+1 Week)' column in the column list to select it.
    page.get_by_label("System Forecast Promotion (Plan+1 Week) Column").get_by_text("System Forecast Promotion (").click()
    # Click on the '6 Week Gross Units Average' column in the column list to select it.
    page.get_by_label("6 Week Gross Units Average").get_by_text("Week Gross Units Average").click()
    # Click on the '6 Week Aged Net Units Average Column' in the column list to select it.
    page.get_by_label("6 Week Aged Net Units Average Column", exact=True).get_by_text("6 Week Aged Net Units Average", exact=True).click()
    # Click on the 'LY 6 Week Aged Net Units' column in the column list to select it.
    page.get_by_label("LY 6 Week Aged Net Units").get_by_text("LY 6 Week Aged Net Units").click()
    # Click on the '% Change 6 Week Aged Net' column in the column list to select it.
    page.get_by_label("% Change 6 Week Aged Net").get_by_text("% Change 6 Week Aged Net").click()
    # Click on the '6 Week Scan Units Average Column' in the column list to select it.
    page.get_by_label("6 Week Scan Units Average Column", exact=True).get_by_text("6 Week Scan Units Average", exact=True).click()
    # Click on the 'LY 6 Week Scan Units Average' column in the column list to select it.
    page.get_by_label("LY 6 Week Scan Units Average").get_by_text("LY 6 Week Scan Units Average").click()
    # Click on the '% Change 6 Week Scan Units' column in the column list to select it.
    page.get_by_label("% Change 6 Week Scan Units").get_by_text("% Change 6 Week Scan Units").click()
    # Click on the 'Freshness (6 Week Average)' column in the column list to select it.
    page.get_by_label("Freshness (6 Week Average)").get_by_text("Freshness (6 Week Average)").click()
    # Click on the '6 Week Aged Returns Units' column in the column list to select it.
    page.get_by_label("6 Week Aged Returns Units").get_by_text("6 Week Aged Returns Units").click()
    # Check the 'Toggle All Columns Visibility' checkbox to make all columns visible.
    page.get_by_role("checkbox", name="Toggle All Columns Visibility").check()
    # Set up an expectation to handle a file download triggered by subsequent actions.
    with page.expect_download() as download1_info:
        # Click on the 'Export' icon within the 'esp-grid-icons-component' to initiate the export process.
        page.locator("esp-grid-icons-component").filter(has_text="Export").locator("#export-iconId").click()
    # Capture the downloaded file information after the export action is triggered.
    download1 = download1_info.value
    # Click on the 'Preference' icon within the 'Customers columns (0)' card to open the preferences menu.
    page.locator("esp-card-component").filter(has_text="Customers columns (0)").locator("#preference-iconId").click()
    # Click on the 'Reset Preference' option to reset the preferences to their default state.
    page.locator("div").filter(has_text=re.compile(r"^Reset Preference$")).first.click()
    # Click on the header cell to initiate sorting or selection actions.
    page.locator(".ag-header-cell.ag-column-first > .ag-header-cell-comp-wrapper > .ag-cell-label-container > .ag-header-cell-label").click()
    # Click on the descending sort icon to sort the column in descending order.
    page.locator(".ag-icon.ag-icon-desc").first.click()
    # Click on the ascending sort icon to sort the column in ascending order.
    page.locator(".ag-icon.ag-icon-asc").first.click()
    # Select the '3RD PARTY DISTRIB' column by clicking on its text.
    page.get_by_text("3RD PARTY DISTRIB").click()
    # Click on the first group checkbox to select or deselect a group of columns.
    page.locator(".ag-group-checkbox").first.click()
    # Right-click on the '3RD PARTY DISTRIB' column within the 'esp-row-dimentional-grid' to open a context menu or perform a specific action.
    page.locator("esp-row-dimentional-grid span").filter(has_text=re.compile(r"^3RD PARTY DISTRIB$")).click(button="right")
    # Click on the '3RD PARTY DISTRIB' column within the 'esp-row-dimentional-grid' to select it or perform an action.
    page.locator("esp-row-dimentional-grid").get_by_text("3RD PARTY DISTRIB").click()
    # Click on the filter button in the header to open the filter options.
    page.locator(".ag-header-icon.ag-header-cell-filter-button > .ag-icon").first.click()
    # Click on the filter body wrapper to interact with the filter options.
    page.locator(".ag-filter-body-wrapper").click()
    # Select the 'Contains' filter option from the dropdown.
    page.get_by_text("Contains").click()
    # Click on the 'Contains' option to confirm selection.
    page.get_by_role("option", name="Contains").click()
    page.get_by_text("Contains").click()
    # Select the 'Does not contain' filter option from the dropdown.
    page.get_by_text("Does not contain").click()
    page.get_by_text("Does not contain").click()
    # Select the 'Equals' filter option from the dropdown.
    page.get_by_role("option", name="Equals").click()
    page.get_by_text("Equals").click()
    # Select the 'Does not equal' filter option from the dropdown.
    page.get_by_role("option", name="Does not equal").click()
    page.get_by_text("Does not equal").click()
    # Select the 'Begins with' filter option from the dropdown.
    page.get_by_role("option", name="Begins with").click()
    page.get_by_text("Begins with").click()
    # Select the 'Ends with' filter option from the dropdown.
    page.get_by_role("option", name="Ends with").click()
    page.get_by_text("Ends with").click()
    # Select the 'Blank' filter option from the dropdown.
    page.get_by_role("option", name="Blank", exact=True).click()
    # Click on the 'AND' operator to set the filter condition.
    page.get_by_text("AND", exact=True).click()
    # Click on the 'OR' radio button to change the filter condition operator.
    page.locator(".ag-labeled.ag-label-align-right.ag-radio-button.ag-input-field.ag-filter-condition-operator.ag-filter-condition-operator-or").click()
    # Click on the 'Clear' button to clear all filter settings.
    page.get_by_role("button", name="Clear").click()
    # Click on the 'Reset' button to reset the filter settings to default.
    page.get_by_role("button", name="Reset").click()
    # Click on the filter button in the header again to close the filter options.
    page.locator(".ag-header-icon.ag-header-cell-filter-button > .ag-icon").first.click()
    # Click on the 'Apply' button to apply the selected filter settings.
    page.get_by_role("button", name="Apply").click()
    # Click on the 'System Forecast Total (Plan' text to interact with the corresponding element.
    page.get_by_text("System Forecast Total (Plan").nth(1).click()
    page.get_by_text("System Forecast Total (Plan").nth(1).click()
    page.get_by_text("System Forecast Total (Plan").nth(1).click()
    # Click on the header icon to open the filter options for a specific column.
    page.locator(".ag-header-cell.ag-header-parent-hidden.ag-header-cell-sortable.ag-header-background.ag-focus-managed.ag-header-active > .ag-header-cell-comp-wrapper > .ag-cell-label-container > .ag-header-icon > .ag-icon").click()
    # Click on the filter body wrapper to interact with the filter options again.
    page.locator(".ag-filter-body-wrapper").click()
    # Select the 'Equals' filter option from the dropdown.
    page.get_by_text("Equals").click()
    page.get_by_role("option", name="Equals").click()
    page.get_by_text("Equals").click()
    # Select the 'Does not equal' filter option from the dropdown.
    page.get_by_role("option", name="Does not equal").click()
    page.get_by_text("Does not equal").click()
    # Select the 'Greater than' filter option from the dropdown.
    page.get_by_role("option", name="Greater than", exact=True).click()
    page.get_by_text("Greater than").click()
    # Select the 'Less than' filter option from the dropdown.
    page.get_by_role("option", name="Less than", exact=True).click()
    # Click on the filtering operator combobox to open the operator options.
    page.get_by_role("combobox", name="Filtering operator").click()
    # Select the 'Less than or equal to' filter option from the dropdown.
    page.get_by_text("Less than or equal to").click()
    page.get_by_text("Less than or equal to").click()
    # Select the 'Between' filter option from the dropdown.
    page.get_by_role("option", name="Between").click()
    page.get_by_text("Between").click()
    # Select the 'Blank' filter option from the dropdown again.
    page.get_by_role("option", name="Blank", exact=True).click()
    # Click on the 'AND' operator to set the filter condition again.
    page.get_by_text("AND", exact=True).click()
    # Click on the 'OR' operator to change the filter condition operator again.
    page.get_by_text("OR", exact=True).click()
    # Click on the 'Clear' button to clear all filter settings again.
    page.get_by_role("button", name="Clear").click()
    # Click on the 'Reset' button to reset the filter settings to default again.
    page.get_by_role("button", name="Reset").click()
    # Click on the header icon to close the filter options for the specific column.
    page.locator(".ag-header-cell.ag-header-parent-hidden.ag-header-cell-sortable.ag-header-background.ag-focus-managed.ag-header-active > .ag-header-cell-comp-wrapper > .ag-cell-label-container > .ag-header-icon > .ag-icon").click()
    # Click on the 'Apply' button to apply the selected filter settings again.
    page.get_by_role("button", name="Apply").click()
    # Click on the pagination element to interact with the pagination controls.
    page.locator("esp-row-dimentional-grid #paginationId").click()
    # Click on the text displaying the current row count to open the row display options.
    page.get_by_text("Showing 10 out of").click()
    # Click on the 'Rows per page' text to interact with the row display dropdown.
    page.get_by_text("Rows per page").click()
    # Select the option to view 10 rows per page from the dropdown.
    page.get_by_text("View 10 row(s)").first.click()
    # Select the option to view 20 rows per page from the dropdown.
    page.get_by_text("View 20 row(s)").click()
    # Click on the dropdown caret to expand additional options.
    page.locator(".dropdown-caret.p-l-16").first.click()
    # Click on the text displaying the updated row count and options to confirm the selection.
    page.get_by_text("Showing 20 out of 138 1234567Rows per page View 20 row(s) View 10 row(s)View 20").click()
    # Click on the 'Next' button in the pagination controls to navigate to the next page.
    page.locator(".pagination-next").click()
    # Click on the specific page number '1234567' to navigate to that page.
    page.get_by_text("1234567").click()
    # Click on the 'Last' button in the pagination controls to navigate to the last page.
    page.locator(".zeb-nav-to-last").click()
    # Click on the fifth list item that matches an empty text filter.
    page.get_by_role("listitem").filter(has_text=re.compile(r"^$")).nth(5).click()
    # Click on the 'Navigate to First' button to go to the first page.
    page.locator(".zeb-nav-to-first").click()
    # Click on the text 'FilterTime Latest 13 Next' to interact with the filter options.
    page.get_by_text("FilterTime Latest 13 Next").click()
    # Click on the 'Filter' text within a div element to open filter settings.
    page.locator("div").filter(has_text=re.compile(r"^Filter$")).click()
    # Click on the 'Filter' text to select the filter option.
    page.get_by_text("Filter").click()
    # Click on the 'Time' text to adjust time-related filters.
    page.get_by_text("Time").click()
    # Click on the first occurrence of 'Latest 13 Next' to select this time filter.
    page.get_by_text("Latest 13 Next").first.click()
    # Click on the 'Latest 5 Next 4' text to select this specific time filter.
    page.get_by_text("Latest 5 Next 4").click()
    # Click on the dropdown labeled '.w-100.p-h-16.p-v-8.dropdown-label.background-white' to expand options.
    page.locator(".w-100.p-h-16.p-v-8.dropdown-label.background-white").click()
    # Click on the second occurrence of 'Latest 5 Next 12' within a div element to select this filter.
    page.locator("div").filter(has_text=re.compile(r"^Latest 5 Next 12$")).nth(1).click()
    # Click on the dropdown caret within the '.w-100.p-h-16.p-v-8.dropdown-label.background-white' element to expand additional options.
    page.locator(".w-100.p-h-16.p-v-8.dropdown-label.background-white > .d-flex.align-items-center > .dropdown-caret").click()
    # Click on the second occurrence of 'Latest 13 Next 4' within a div element to select this filter.
    page.locator("div").filter(has_text=re.compile(r"^Latest 13 Next 4$")).nth(1).click()
    # Click on the dropdown caret within the '.w-100.p-h-16.p-v-8.dropdown-label.background-white' element to expand additional options again.
    page.locator(".w-100.p-h-16.p-v-8.dropdown-label.background-white > .d-flex.align-items-center > .dropdown-caret").click()
    # Click on the 'Latest 13 Next 12' text to select this specific filter.
    page.get_by_text("Latest 13 Next 12").click()
    # Click on the dropdown caret within the '.w-100.p-h-16.p-v-8.dropdown-label.background-white' element to expand additional options again.
    page.locator(".w-100.p-h-16.p-v-8.dropdown-label.background-white > .d-flex.align-items-center > .dropdown-caret").click()
    # Click on the second occurrence of 'Latest 26 Next 4' within a div element to select this filter.
    page.locator("div").filter(has_text=re.compile(r"^Latest 26 Next 4$")).nth(1).click()
    # Click on the 'Weekly Summary Customer:3RD' text to view the weekly summary for the specified customer.
    page.get_by_text("Weekly Summary Customer:3RD").click()
    # Click on the 'Weekly Summary' text to navigate to the Weekly Summary section.
    page.get_by_text("Weekly Summary").click()
    # Click on the first occurrence of 'Customer:3RD PARTY DISTRIB' to select this customer.
    page.get_by_text("Customer:3RD PARTY DISTRIB").first.click()
    # Click on the third occurrence of the exact text 'Customer' to refine the selection.
    page.get_by_text("Customer", exact=True).nth(2).click()
    # Click on the second occurrence of '3RD PARTY DISTRIB' to finalize the customer selection.
    page.get_by_text("3RD PARTY DISTRIB").nth(1).click()
    # Click on the dropdown to open the filter options for selection.
    page.locator(".wr-20.font-weight-normal > esp-multiselect-dropdown > .multiselect-dropdown > div > .w-100").click()
    # Select the 'All' option from the dropdown (4th occurrence).
    page.get_by_text("All").nth(4).click()
    # Re-select the 'All' option from the dropdown (4th occurrence) to confirm the selection.
    page.get_by_text("All").nth(4).click()
    # Click on the first element in the list of filter options to apply the filter.
    page.locator(".d-flex.flex-column.justify-content-center").first.click()
    # Re-click on the first element in the list of filter options to ensure the filter is applied.
    page.locator(".d-flex.flex-column.justify-content-center").first.click()
    # Click on the first dropdown option to refine the filter selection.
    page.locator(".d-flex.dropdown-option.align-items-center.p-v-5.p-l-32 > .d-flex").first.click()
    # Click on the first checkbox to enable or select the corresponding filter option.
    page.locator(".d-flex.flex-column.justify-content-center.font-size-10.align-items-center.checkbox-v2.m-r-10.zeb-check").first.click()
    # Re-click on the first checkbox to confirm the selection or toggle the filter option.
    page.locator(".d-flex.flex-column.justify-content-center.font-size-10.align-items-center.checkbox-v2.m-r-10.zeb-check").first.click()
    # Click on the 'User Override Total' option (2nd occurrence) to select it from the dropdown.
    page.get_by_text("User Override Total").nth(1).click()
    # Click on the first selected dropdown option to confirm or refine the selection.
    page.locator(".d-flex.dropdown-option.align-items-center.p-v-5.p-l-32.p-r-16.selected").first.click()
    # Click on the 'User Override Promotion' option (2nd occurrence) to select it from the dropdown.
    page.get_by_text("User Override Promotion").nth(1).click()
    # Click on the 'System Forecast Total' option (6th occurrence) to select it from the dropdown.
    page.get_by_text("System Forecast Total").nth(5).click()
    # Click on the 'System Forecast Base' option (4th occurrence) to select it from the dropdown.
    page.get_by_text("System Forecast Base").nth(3).click()
    # Click on the 'System Forecast Promotion' option (4th occurrence) to select it from the dropdown.
    page.get_by_text("System Forecast Promotion").nth(3).click()
    # Click on the first selected dropdown option again to confirm or refine the selection.
    page.locator(".d-flex.dropdown-option.align-items-center.p-v-5.p-l-32.p-r-16.selected").first.click()
    # Re-click on the first selected dropdown option to ensure the selection is applied.
    page.locator(".d-flex.dropdown-option.align-items-center.p-v-5.p-l-32.p-r-16.selected").first.click()
    # Click on the 'Weekly Forecast Promotion' option (exact match) to select it from the dropdown.
    page.get_by_text("Weekly Forecast Promotion", exact=True).click()
    # Click on the 'Daily Suggested Order Total' option (2nd occurrence) to select it from the dropdown.
    page.get_by_text("Daily Suggested Order Total").nth(1).click()
    # Click on the 'Daily Suggested Order Base' option (exact match) to select it from the dropdown.
    page.get_by_text("Daily Suggested Order Base", exact=True).click()
    # Click on the 18th child element within the '.overflow-auto > div' container to select a specific option.
    page.locator(".overflow-auto > div:nth-child(18)").click()
    # Click on the 'Gross Units' option (3rd occurrence) to select it from the dropdown.
    page.get_by_text("Gross Units").nth(2).click()
    # Click on the 'Raw Forecast' option (2nd occurrence) to select it from the dropdown.
    page.get_by_text("Raw Forecast").nth(1).click()
    # Click on the 'Daily Suggested Order Promotion' option (exact match) to select it from the dropdown.
    page.get_by_text("Daily Suggested Order Promotion", exact=True).click()
    # Click on the '% Change Aged Net Units' option (exact match) to select it from the dropdown.
    page.get_by_text("% Change Aged Net Units", exact=True).click()
    # Click on the 'Aged Net Units LY' option (exact match) to select it from the dropdown.
    page.get_by_text("Aged Net Units LY", exact=True).click()
    # Click on the first selected dropdown option to confirm or refine the selection.
    page.locator(".d-flex.dropdown-option.align-items-center.p-v-5.p-l-32.p-r-16.selected").first.click()
    # Click on the 'Scan Units LY' option (exact match) to select it from the dropdown.
    page.get_by_text("Scan Units LY", exact=True).click()
    # Re-click on the 'Scan Units LY' option (exact match) to ensure the selection is applied.
    page.get_by_text("Scan Units LY", exact=True).click()
    # Re-click on the 'Scan Units LY' option (exact match) again to confirm the selection.
    page.get_by_text("Scan Units LY", exact=True).click()
    # Click on the 'Freshness' option (3rd occurrence) to select it from the dropdown.
    page.get_by_text("Freshness").nth(2).click()
    # Click on the '% Change Scan Units' option (exact match) to select it from the dropdown.
    page.get_by_text("% Change Scan Units", exact=True).click()
    # Click on the 'Aged Return Units' option (2nd occurrence) to select it from the dropdown.
    page.get_by_text("Aged Return Units").nth(1).click()
    # Click on the first selected dropdown option to confirm or refine the selection.
    page.locator(".d-flex.dropdown-option.align-items-center.p-v-5.p-l-32.p-r-16.selected").first.click()
    # Click on the 'System MAPE' option (exact match) to select it from the dropdown.
    page.get_by_text("System MAPE", exact=True).click()
    # Click on the 'Forecast Value Add - MAPE' option (exact match) to select it from the dropdown.
    page.get_by_text("Forecast Value Add - MAPE", exact=True).click()
    # Click on the first selected dropdown option to confirm or refine the selection.
    page.locator(".d-flex.dropdown-option.align-items-center.p-v-5.p-l-32.p-r-16.selected").first.click()
    # Click on the 'System Bias' option (exact match) to select it from the dropdown.
    page.get_by_text("System Bias", exact=True).click()
    # Click on the 'Forecast Value Add - Bias' option (exact match) to select it from the dropdown.
    page.get_by_text("Forecast Value Add - Bias", exact=True).click()
    # Click on the second occurrence of the 'Promo' option to select it from the dropdown.
    page.get_by_text("Promo", exact=True).nth(1).click()
    # Click on the first element within the '.d-flex.dropdown-option' container to select it.
    page.locator(".d-flex.dropdown-option").first.click()
    # Click on the button within the 'esp-card-component' that contains the text 'Weekly Summary Customer:3RD'.
    page.locator("esp-card-component").filter(has_text="Weekly Summary Customer:3RD").get_by_role("button").click()
    # Click on the textbox labeled 'Filter Columns Input' to activate it for input.
    page.get_by_role("textbox", name="Filter Columns Input").click()
    # Fill the 'Filter Columns Input' textbox with the date '2025-07-27' to filter columns.
    page.get_by_role("textbox", name="Filter Columns Input").fill("2025-07-27")
    # Click on the text '-07-27 (31)' to select the corresponding column.
    page.get_by_text("-07-27 (31)").click()
    # Check the checkbox labeled 'Press SPACE to toggle visibility (hidden)' to make the column visible.
    page.get_by_role("checkbox", name="Press SPACE to toggle visibility (hidden)").check()
    # Click on the 'Filter Columns Input' textbox to activate it for further input.
    page.get_by_role("textbox", name="Filter Columns Input").click()
    # Clear the 'Filter Columns Input' textbox by filling it with an empty string.
    page.get_by_role("textbox", name="Filter Columns Input").fill("")
    # Press 'Enter' in the 'Filter Columns Input' textbox to apply the filter.
    page.get_by_role("textbox", name="Filter Columns Input").press("Enter")
    # Check the 'Toggle All Columns Visibility' checkbox to make all columns visible.
    page.get_by_role("checkbox", name="Toggle All Columns Visibility").check()
    # Click on the text '-07-27 (31)' within the label '-07-27 (31) Column' to interact with the column.
    page.get_by_label("-07-27 (31) Column").get_by_text("-07-27 (31)").click()
    # Click on the text '-08-03 (32)' within the label '-08-03 (32) Column' to interact with the column.
    page.get_by_label("-08-03 (32) Column").get_by_text("-08-03 (32)").click()
    # Click on the text '-08-10 (33)' within the label '-08-10 (33) Column' to interact with the column.
    page.get_by_label("-08-10 (33) Column").get_by_text("-08-10 (33)").click()
    # Click on the text '-08-24 (35)' within the label '-08-24 (35) Column' to interact with the column.
    page.get_by_label("-08-24 (35) Column").get_by_text("-08-24 (35)").click()
    # Click on the text '-08-24 (35)' to interact with the column.
    page.get_by_text("-08-24 (35)").click()
    # Click on the text '-10-19 (43)' to interact with the column.
    page.get_by_text("-10-19 (43)").click()
    # Click on the button within the 'esp-card-component' containing the text 'Weekly Summary Customer:3RD' to perform an action.
    page.locator("esp-card-component").filter(has_text="Weekly Summary Customer:3RD").get_by_role("button").click()
    # Start monitoring for a file download triggered by the next action.
    with page.expect_download() as download2_info:
        # Click on the 'Export' icon within the 'esp-grid-icons-component' to initiate the export process.
        page.locator("esp-grid-icons-component").filter(has_text="Export").locator("#export-iconId").click()
    download2 = download2_info.value
    # Click on the dropdown menu under the 'Preference' section to open the options.
    page.locator("div:nth-child(4) > #preference-iconId > .legend-font > .multiselect-dropdown > .pointer").click()
    # Click on the 'Save Preference' option to save the current preferences.
    page.locator("div").filter(has_text=re.compile(r"^Save Preference$")).first.click()
    # Click on the dropdown menu under the 'Preference' section again to reopen the options.
    page.locator("div:nth-child(4) > #preference-iconId > .legend-font > .multiselect-dropdown > .pointer").click()
    # Click on the 'Reset Preference' option to reset the preferences to their default state.
    page.get_by_text("Reset Preference").click()
    # Click on the first column header in the grid to interact with it.
    page.locator(".ag-header-cell.ag-column-first.ag-header-parent-hidden.ag-header-background.ag-focus-managed.ag-header-active > .ag-header-cell-comp-wrapper > .ag-cell-label-container > .ag-header-cell-label").click()
    # Select the 'User Forecast Total' column from the grid.
    page.locator("esp-column-dimentional-grid").get_by_text("User Forecast Total").click()
    # Click on the first icon (likely an expand or action button) in the grid.
    page.locator("i").first.click()
    # Click on the third icon in the grid (possibly another action or expand button).
    page.locator("i").nth(2).click()
    # Select the 'User Override Total' column from the grid.
    page.locator("span").filter(has_text="User Override Total").first.click()
    # Click on the 'System Forecast Total' column header to interact with it.
    page.get_by_text("System Forecast Total", exact=True).click()
    # Click on the fifth icon in the grid (likely another action or expand button).
    page.locator("i").nth(4).click()
    # Select the 'Weekly Forecast Total' column from the grid.
    page.locator("span").filter(has_text="Weekly Forecast Total").first.click()
    # Expand the first group in the grid by clicking the right chevron icon.
    page.locator(".ag-cell-value.ag-cell.ag-cell-not-inline-editing.ag-cell-normal-height.ag-cell-last-left-pinned.ag-column-first.ag-cell-override-normal.notosans-overwrite.no-border.ag-cell-focus > .ag-cell-wrapper > .ag-group-contracted > .zeb-chevron-right").click()
    # Select the 'Daily Suggested Order Total' column from the grid.
    page.locator("span").filter(has_text="Daily Suggested Order Total").first.click()
    # Expand the first group in the grid again by clicking the right chevron icon.
    page.locator(".ag-cell-value.ag-cell.ag-cell-not-inline-editing.ag-cell-normal-height.ag-cell-last-left-pinned.ag-column-first.ag-cell-override-normal.notosans-overwrite.no-border.ag-cell-focus > .ag-cell-wrapper > .ag-group-contracted > .zeb-chevron-right").click()
    # Collapse the expanded group in the grid by clicking the down chevron icon.
    page.locator(".ag-cell-value.ag-cell.ag-cell-not-inline-editing.ag-cell-normal-height.ag-cell-last-left-pinned.ag-column-first.ag-cell-override-normal.notosans-overwrite.no-border.ag-cell-focus > .ag-cell-wrapper > .ag-group-expanded > .zeb-chevron-down").click()
    # Expand another group in the grid by clicking the right chevron icon.
    page.locator(".ag-row-odd.ag-row-no-focus.ag-row-not-inline-editing.ag-row.ag-row-level-0.ag-row-group.ag-row-group-contracted.ag-row-position-absolute.ag-row-hover > .ag-cell-value > .ag-cell-wrapper > .ag-group-contracted > .zeb-chevron-right").click()
    # Select the 'Aged Net Units' column from the grid.
    page.locator("esp-column-dimentional-grid").get_by_text("Aged Net Units", exact=True).click()
    # Select the 'Scan Units' column from the grid.
    page.locator("esp-column-dimentional-grid").get_by_text("Scan Units").click()
    # Expand the first group in the grid again by clicking the right chevron icon.
    page.locator(".ag-cell-value.ag-cell.ag-cell-not-inline-editing.ag-cell-normal-height.ag-cell-last-left-pinned.ag-column-first.ag-cell-override-normal.notosans-overwrite.no-border.ag-cell-focus > .ag-cell-wrapper > .ag-group-contracted > .zeb-chevron-right").click()
    # Expand another group in the grid by clicking the right chevron icon.
    page.locator(".ag-row-odd.ag-row-no-focus.ag-row-not-inline-editing.ag-row.ag-row-level-0.ag-row-group.ag-row-group-contracted.ag-row-position-absolute.ag-row-hover > .ag-cell-value > .ag-cell-wrapper > .ag-group-contracted > .zeb-chevron-right").click()
    # Select the 'User MAPE' column from the grid.
    page.locator("esp-column-dimentional-grid").get_by_text("User MAPE").click()
    # Click on the 'Weekly Trend Customer:3RD' text to select the customer.
    page.get_by_text("Weekly Trend Customer:3RD").click()
    # Click on the 'Weekly Trend' text to navigate to the Weekly Trend section.
    page.get_by_text("Weekly Trend").click()
    # Click on the 'Customer:3RD PARTY DISTRIB' label in the line-bar chart to interact with it.
    page.locator("dp-line-bar-chart").get_by_text("Customer:3RD PARTY DISTRIB").click()
    # Click on the 'Customer:3RD PARTY DISTRIB' label in the line-bar chart again, possibly to toggle or confirm selection.
    page.locator("dp-line-bar-chart").get_by_text("Customer:3RD PARTY DISTRIB").click()
    # Click on the 'Customer' label in the line-bar chart with exact match to interact with it.
    page.locator("dp-line-bar-chart").get_by_text("Customer", exact=True).click()
    # Click on the '3RD PARTY DISTRIB' label in the line-bar chart to interact with it.
    page.locator("dp-line-bar-chart").get_by_text("3RD PARTY DISTRIB").click()
    # Click on the first occurrence of 'User Forecast Total, User' text to select it.
    page.get_by_text("User Forecast Total, User").first.click()
    # Click on the 'User Forecast Total' label within the line-bar chart to interact with it.
    page.locator("dp-line-bar-chart span").filter(has_text="User Forecast Total").click()
    # Click on the 'User Forecast Base' text to select it.
    page.get_by_text("User Forecast Base").click()
    # Click on the third child element within the '.overflow-auto' container, likely to interact with a dropdown or menu.
    page.locator(".overflow-auto > div:nth-child(3)").click()
    # Click on the 'User Override Total' label within the line-bar chart to interact with it.
    page.locator("dp-line-bar-chart span").filter(has_text="User Override Total").click()
    # Click on the 'User Override Base' text to select it.
    page.get_by_text("User Override Base").click()
    # Click on the 'User Override Promotion' text to select it.
    page.get_by_text("User Override Promotion").click()
    # Click on the sixth child element within the '.overflow-auto' container, likely to interact with a dropdown or menu.
    page.locator(".overflow-auto > div:nth-child(6)").click()
    # Click on the 'System Forecast Total' label within the line-bar chart to interact with it.
    page.locator("dp-line-bar-chart").get_by_text("System Forecast Total").click()
    # Click on the 'System Forecast Base' text with exact match to select it.
    page.get_by_text("System Forecast Base", exact=True).click()
    # Click on the 'System Forecast Promotion' text with exact match to select it.
    page.get_by_text("System Forecast Promotion", exact=True).click()
    # Click on the tenth child element within the '.overflow-auto' container, likely to interact with a dropdown or menu.
    page.locator(".overflow-auto > div:nth-child(10)").click()
    # Click on the 'Weekly Forecast Base' label within the line-bar chart to interact with it.
    page.locator("dp-line-bar-chart").get_by_text("Weekly Forecast Base").click()
    # Click on the 'Weekly Forecast Promotion' label within the line-bar chart to interact with it.
    page.locator("dp-line-bar-chart").get_by_text("Weekly Forecast Promotion").click()
    # Click on the 'Weekly Forecast Promotion' label within the line-bar chart again, possibly to toggle or confirm selection.
    page.locator("dp-line-bar-chart").get_by_text("Weekly Forecast Promotion").click()
    # Click on the fifteenth child element within the '.overflow-auto' container, likely to interact with a dropdown or menu.
    page.locator(".overflow-auto > div:nth-child(15)").click()
    # Click on the fourteenth child element within the '.overflow-auto' container, likely to interact with a dropdown or menu.
    page.locator(".overflow-auto > div:nth-child(14)").click()
    # Click on the 'Daily Suggested Order Total' label within the line-bar chart to interact with it.
    page.locator("dp-line-bar-chart").get_by_text("Daily Suggested Order Total").click()
    # Click on the 'Daily Suggested Order Promotion' text to select it.
    page.locator("span").filter(has_text="Daily Suggested Order Promotion").click()
    # Click on the 'Daily Suggested Order Base' text to select it.
    page.locator("span").filter(has_text="Daily Suggested Order Base").click()
    # Click on the 'Daily Suggested Order Base' text again, possibly to toggle or confirm selection.
    page.locator("span").filter(has_text="Daily Suggested Order Base").click()
    # Click on the second occurrence of the 'Aged Net Units' text with an exact match to select it.
    page.get_by_text("Aged Net Units", exact=True).nth(1).click()
    # Click on the fifteenth child element within the '.overflow-auto' container, likely to interact with a dropdown or menu.
    page.locator(".overflow-auto > div:nth-child(15)").click()
    # Click on the fifteenth child element within the '.overflow-auto' container again, possibly to toggle or confirm selection.
    page.locator(".overflow-auto > div:nth-child(15)").click()
    # Click on the seventeenth child element within the '.overflow-auto' container, likely to interact with a dropdown or menu.
    page.locator(".overflow-auto > div:nth-child(17)").click()
    # Click on the 'Aged Net Units' label within the line-bar chart with an exact match to interact with it.
    page.locator("dp-line-bar-chart").get_by_text("Aged Net Units", exact=True).click()
    # Click on the 'Aged Net Units LY' label within the line-bar chart to interact with it.
    page.locator("dp-line-bar-chart").get_by_text("Aged Net Units LY").click()
    # Click on the 'Scan Units LY' label within the line-bar chart to interact with it.
    page.locator("dp-line-bar-chart").get_by_text("Scan Units LY").click()
    # Click on the twenty-second child element within the '.overflow-auto' container, likely to interact with a dropdown or menu.
    page.locator(".overflow-auto > div:nth-child(22)").click()
    # Click on the twenty-third child element within the '.overflow-auto' container, likely to interact with a dropdown or menu.
    page.locator(".overflow-auto > div:nth-child(23)").click()
    # Click on the twenty-fourth child element within the '.overflow-auto' container, likely to interact with a dropdown or menu.
    page.locator(".overflow-auto > div:nth-child(24)").click()
    # Click on the 'Forecast Value Add - MAPE' label within the line-bar chart to interact with it.
    page.locator("dp-line-bar-chart").get_by_text("Forecast Value Add - MAPE").click()
    # Click on the twenty-sixth child element within the parent 'div', likely to interact with a dropdown or menu.
    page.locator("div:nth-child(26)").click()
    # Click on the twenty-seventh child element within the parent 'div', likely to interact with a dropdown or menu.
    page.locator("div:nth-child(27)").click()
    # Click on the 'Forecast Value Add - Bias' label within the line-bar chart to interact with it.
    page.locator("dp-line-bar-chart").get_by_text("Forecast Value Add - Bias").click()
    # Click on the text 'User Forecast Base, User' to select or interact with the corresponding element.
    page.get_by_text("User Forecast Base, User").first.click()
    # Click on the dropdown menu associated with the preference icon to open the preference options.
    page.locator(".title.d-flex.align-items-center.font-size-16.font-weight-bold.nunito.title-color > .grid-icons-container > esp-grid-icons-component > .display-grid-icons > div > #preference-iconId > .legend-font > .multiselect-dropdown > .pointer").click()
    # Click on the 'Save Preference' button to save the current user preferences.
    page.get_by_text("Save Preference").click()
    # Click on the dropdown menu associated with the preference icon again, likely to perform another action.
    page.locator(".title.d-flex.align-items-center.font-size-16.font-weight-bold.nunito.title-color > .grid-icons-container > esp-grid-icons-component > .display-grid-icons > div > #preference-iconId > .legend-font > .multiselect-dropdown > .pointer").click()
    # Click on the 'Reset Preference' option to reset the user preferences to their default state.
    page.locator("div").filter(has_text=re.compile(r"^Reset Preference$")).first.click()
    # Click on a specific SVG path element, likely to interact with a visual component or chart.
    page.locator("path:nth-child(157)").click()
    # Click on the text 'User Forecast Total' within an SVG element, possibly to select or highlight it.
    page.locator("svg").get_by_text("User Forecast Total").click()
    # Click on the text 'User Override Total' within an SVG element, likely to interact with or select it.
    page.locator("svg").get_by_text("User Override Total").click()
    # Click on the text 'Aged Net Units' within a text element, possibly to filter or highlight related data.
    page.locator("text").filter(has_text="Aged Net Units").click()
    # Click on the SVG element, potentially to reset or deselect a previous selection.
    page.locator("svg").click()
    # Click on the exact text '0%' to interact with a specific data point or value.
    page.get_by_text("0%", exact=True).click()
    # Click on the text '20%' to interact with or select a specific percentage value.
    page.get_by_text("20%").click()
    # Click on the text '02/01/' to select or interact with a specific date.
    page.get_by_text("02/01/").click()
    # Click on the text '01/11/' to select or interact with another specific date.
    page.get_by_text("01/11/").click()
    # Click on the text '12/21/' to select or interact with another specific date.
    page.get_by_text("12/21/").click()

    # ---------------------
    # Close the browser context to clean up resources and end the session.
    context.close()
    # Close the browser instance to terminate the automation process completely.
    browser.close()


with sync_playwright() as playwright:
    run(playwright)
