# Import the 're' module for regular expression operations.
import re
# Import necessary components from the Playwright library for browser automation and assertions.
from playwright.sync_api import Playwright, sync_playwright, expect


# Define the main function 'run' which will execute the Playwright automation script.
def run(playwright: Playwright) -> None:
    # Launch a Chromium browser instance in non-headless mode for visual debugging.
    browser = playwright.chromium.launch(headless=False)
    # Create a new browser context to isolate cookies, storage, and other session data.
    context = browser.new_context()
    # Open a new page within the created browser context for interaction.
    page = context.new_page()
    # Navigate to the Executive Dashboard page by opening the specified URL.
    page.goto("https://stage.wba.esp.antuit.ai/dp/demand-planning/executive-dashboard?workbookId=6&tabIndex=1")
    # Click on the 'Alerts' filter dropdown to expand the filter options.
    page.locator("#alerts-filterId").click()
    # Select the 'MAPE' option from the dropdown list.
    page.locator("div").filter(has_text=re.compile(r"^MAPE$")).nth(1).click()
    # Click on the dropdown caret to open the filter options again.
    page.locator(".w-100.p-h-16.p-v-8.dropdown-label.background-white > .d-flex.align-items-center > .dropdown-caret").click()
    # Select the 'Under Bias' option from the dropdown list.
    page.locator("div").filter(has_text=re.compile(r"^Under Bias$")).nth(1).click()
    # Click on the dropdown caret to open the filter options again.
    page.locator(".w-100.p-h-16.p-v-8.dropdown-label.background-white > .d-flex.align-items-center > .dropdown-caret").click()
    # Select the 'Over Bias' option from the dropdown list.
    page.locator("div").filter(has_text=re.compile(r"^Over Bias$")).nth(1).click()
    # Click on the dropdown caret to open the filter options again.
    page.locator(".w-100.p-h-16.p-v-8.dropdown-label.background-white > .d-flex.align-items-center > .dropdown-caret").click()
    # Select the 'PVA' option from the dropdown list.
    page.locator("div").filter(has_text=re.compile(r"^PVA$")).nth(1).click()
    # Click on the dropdown caret to open the filter options again.
    page.locator(".w-100.p-h-16.p-v-8.dropdown-label.background-white > .d-flex.align-items-center > .dropdown-caret").click()
    # Select the 'SSIS' option from the dropdown list.
    page.locator("div").filter(has_text=re.compile(r"^SSIS$")).first.click()
    # Click on the 'Columns' button to open the column visibility configuration panel.
    page.get_by_role("button", name="columns").click()
    # Uncheck the 'Toggle All Columns Visibility' checkbox to hide all columns initially.
    page.get_by_role("checkbox", name="Toggle All Columns Visibility").uncheck()
    # Check the 'Store Count Column' checkbox to make the 'Store Count' column visible.
    page.get_by_role("treeitem", name="Store Count Column").get_by_label("Press SPACE to toggle").check()
    # Check the 'Product Count Column' checkbox to make the 'Product Count' column visible.
    page.get_by_role("treeitem", name="Product Count Column").get_by_label("Press SPACE to toggle").check()
    # Check the 'Stability Column' checkbox to make the 'Stability' column visible.
    page.get_by_role("treeitem", name="Stability Column").get_by_label("Press SPACE to toggle").check()
    # Check the 'SSIS Column' checkbox to make the 'SSIS' column visible.
    page.get_by_role("treeitem", name="SSIS Column").get_by_label("Press SPACE to toggle").check()
    # Check the 'User Bias Column' checkbox to make the 'User Bias' column visible.
    page.get_by_role("treeitem", name="User Bias Column").get_by_label("Press SPACE to toggle").check()
    # Check the 'System Bias Column' checkbox to make the 'System Bias' column visible.
    page.get_by_role("treeitem", name="System Bias Column").get_by_label("Press SPACE to toggle").check()
    # Check the 'User MAPE Column' checkbox to make the 'User MAPE' column visible.
    page.get_by_role("treeitem", name="User MAPE Column").get_by_label("Press SPACE to toggle visibility (hidden)").check()
    # Check the 'System MAPE Column' checkbox to make the 'System MAPE' column visible.
    page.get_by_role("treeitem", name="System MAPE Column").get_by_label("Press SPACE to toggle visibility (hidden)").check()
    # Check the 'Planner Value Add Column' checkbox to make the 'Planner Value Add' column visible.
    page.get_by_role("treeitem", name="Planner Value Add Column").get_by_label("Press SPACE to toggle visibility (hidden)").check()
    # Check the '13W-Fcst Column' checkbox to make the '13W-Fcst' column visible.
    page.get_by_role("treeitem", name="13W-Fcst Column").get_by_label("Press SPACE to toggle visibility (hidden)").check()
    # Click on the column selector element to open the column selection panel.
    page.locator("div:nth-child(11) > .ag-column-select-column").click()
    # Click on the 'Filter Columns Input' textbox to focus on it for entering a filter value.
    page.get_by_role("textbox", name="Filter Columns Input").click()
    # Fill the 'Filter Columns Input' textbox with the value 'Store Count' to filter the columns.
    page.get_by_role("textbox", name="Filter Columns Input").fill("Store Count")
    # Press 'Enter' to apply the filter and display the filtered column options.
    page.get_by_role("textbox", name="Filter Columns Input").press("Enter")
    # Check the checkbox for the filtered column to make it visible.
    page.get_by_role("checkbox", name="Press SPACE to toggle").check()
    # Click on the 'Columns' button to close the column selection panel.
    page.get_by_role("button", name="columns").click()
    # Select the radio button for the row with the name '002-SPIRITS' to apply row selection.
    page.get_by_role("row", name=" 002-SPIRITS").get_by_role("radio").check()
    # Click on the first 'Filter' button to open the filter configuration for the selected column.
    page.get_by_title("Filter").first.click()
    # Fill the 'Filter Value' textbox with '002-SPIRITS' to filter rows based on this value.
    page.get_by_role("textbox", name="Filter Value").fill("002-SPIRITS")
    # Click on the 'Apply' button to apply the column filter and update the displayed rows.
    page.get_by_label("Column Filter").get_by_role("button", name="Apply").click()
    # Click on the first 'Filter' button to open the filter configuration for the selected column.
    page.get_by_title("Filter").first.click()
    # Click on the dropdown icon to open the filter condition options.
    page.locator(".ag-icon.ag-icon-small-down").first.click()
    # Select the 'Does not contain' option from the filter condition dropdown.
    page.get_by_role("option", name="Does not contain").click()
    # Click on the dropdown icon again to open the filter condition options.
    page.locator(".ag-icon.ag-icon-small-down").first.click()
    # Select the 'Equals' option from the filter condition dropdown.
    page.get_by_role("option", name="Equals").click()
    # Click on the dropdown icon again to open the filter condition options.
    page.locator(".ag-icon.ag-icon-small-down").first.click()
    # Select the 'Does not equal' option from the filter condition dropdown.
    page.get_by_role("option", name="Does not equal").click()
    # Click on the dropdown icon again to open the filter condition options.
    page.locator(".ag-icon.ag-icon-small-down").first.click()
    # Select the 'Begins with' option from the filter condition dropdown.
    page.get_by_role("option", name="Begins with").click()
    # Click on the dropdown icon again to open the filter condition options.
    page.locator(".ag-icon.ag-icon-small-down").first.click()
    # Select the 'Ends with' option from the filter condition dropdown.
    page.get_by_role("option", name="Ends with").click()
    # Click on the dropdown icon again to open the filter condition options.
    page.locator(".ag-icon.ag-icon-small-down").first.click()
    # Select the 'Does not contain' option from the filter condition dropdown again.
    page.get_by_role("option", name="Does not contain").click()
    # Click on the 'Apply' button to apply the selected filter condition.
    page.get_by_label("Column Filter").get_by_role("button", name="Apply").click()
    # Click on the first 'Filter' button to reopen the filter configuration.
    page.get_by_title("Filter").first.click()
    # Click on the 'Reset' button to clear the applied filter and reset the filter configuration.
    page.get_by_role("button", name="Reset").click()
    # Click on the first pagination link to navigate to the first page of the table.
    page.locator("a").first.click()
    # Click on the second pagination link to navigate to the second page of the table.
    page.locator("a").nth(1).click()
    # Click on the 'Next' button to navigate to the next page in the pagination.
    page.locator(".pagination-next > .zeb-chevron-right").first.click()
    # Click on the 'Previous' button to navigate to the previous page in the pagination.
    page.locator(".zeb-chevron-left").first.click()
    # Click on the 'First' button to navigate to the first page in the pagination.
    page.locator(".zeb-nav-to-first").first.click()
    # Click on the dropdown to open the row view options.
    page.locator(".d-flex > esp-multiselect-dropdown > .multiselect-dropdown > div > .w-100 > .d-flex.align-items-center > .dropdown-caret").first.click()
    # Select the option to view 20 rows per page.
    page.locator("div").filter(has_text=re.compile(r"^View 20 row\(s\)$")).first.click()
    # Click on the dropdown again to open the row view options.
    page.locator(".d-flex > esp-multiselect-dropdown > .multiselect-dropdown > div > .w-100 > .d-flex.align-items-center > .dropdown-caret").first.click()
    # Select the option to view 50 rows per page.
    page.locator("div").filter(has_text=re.compile(r"^View 50 row\(s\)$")).first.click()
    # Click on the dropdown again to open the row view options.
    page.locator(".d-flex > esp-multiselect-dropdown > .multiselect-dropdown > div > .w-100 > .d-flex.align-items-center > .dropdown-caret").first.click()
    # Select the option to view 10 rows per page.
    page.locator("div").filter(has_text=re.compile(r"^View 10 row\(s\)$")).nth(1).click()
    # Click on the text displaying the current row count and total rows to view detailed information.
    page.get_by_text("Locations 20 rows out of 968").click()
    page.locator(".pointer.chevron.zeb-chevron-right.m-r-12.collapsed").click()
    page.get_by_text("Locations", exact=True).click()
    page.get_by_role("row", name="Location").get_by_role("checkbox").uncheck()
    page.get_by_role("button", name="columns").nth(1).click()
    page.get_by_role("checkbox", name="Toggle All Columns Visibility").uncheck()
    page.get_by_role("treeitem", name="Store Count Column").get_by_label("Press SPACE to toggle").check()
    page.get_by_role("treeitem", name="Product Count Column").get_by_label("Press SPACE to toggle").check()
    page.get_by_role("treeitem", name="13W-Fcst Column").get_by_label("Press SPACE to toggle").check()
    page.get_by_role("textbox", name="Filter Columns Input").click()
    page.get_by_role("textbox", name="Filter Columns Input").fill("Pre")
    page.get_by_role("checkbox", name="Press SPACE to toggle").check()
    page.get_by_role("button", name="columns").nth(1).click()
    page.locator("#ag-header-cell-menu-button > .filter-icon").click()
    page.get_by_role("textbox", name="Filter Value").click()
    page.get_by_role("textbox", name="Filter Value").fill("CHICAGO")
    page.get_by_label("Column Menu").get_by_role("button", name="Apply").click()
    page.get_by_role("gridcell", name="00162-1554 E 55TH ST-CHICAGO-").get_by_role("checkbox").check()
    page.locator("#ag-header-cell-menu-button > .filter-icon").click()
    page.get_by_label("Column Menu").get_by_role("button", name="Reset").click()
    page.get_by_role("row", name="Location").get_by_role("checkbox").check()
    page.locator("a").filter(has_text="2").nth(1).click()
    page.locator("a").filter(has_text="3").nth(1).click()
    page.locator("div:nth-child(3) > esp-pagination-v2 > .d-flex.w-100 > .pagination-pager > .pagination-next > .zeb-chevron-right").click()
    page.locator("div:nth-child(3) > esp-pagination-v2 > .d-flex.w-100 > .pagination-pager > .pagination-previous > .zeb-chevron-left").click()
    page.locator("div:nth-child(3) > esp-pagination-v2 > .d-flex.w-100 > .pagination-pager > .pagination-first > .zeb-nav-to-first").click()
    page.get_by_role("button", name="Apply").click()
    # Click on the 'Filter' button to expand the filter options.
    page.get_by_text("Filter").nth(2).click()
    # Click on the dropdown for the 'Time' filter to view available time range options.
    page.locator("#time-filterId > .wr-20 > esp-multiselect-dropdown > .multiselect-dropdown > div > .w-100 > .d-flex.align-items-center > .dropdown-caret").click()
    # Select the 'Latest 4 Next 4' option from the 'Time' filter dropdown.
    page.locator("div").filter(has_text=re.compile(r"^Latest 4 Next 4$")).nth(1).click()
    # Click on the dropdown for the 'Time' filter again to change the selection.
    page.locator("#time-filterId > .wr-20 > esp-multiselect-dropdown > .multiselect-dropdown > div > .w-100 > .d-flex.align-items-center > .dropdown-caret").click()
    # Select the 'Latest 4 Next 13' option from the 'Time' filter dropdown.
    page.locator("div").filter(has_text=re.compile(r"^Latest 4 Next 13$")).nth(1).click()
    # Click on the dropdown for the 'Time' filter again to change the selection.
    page.locator("#time-filterId > .wr-20 > esp-multiselect-dropdown > .multiselect-dropdown > div > .w-100 > .d-flex.align-items-center > .dropdown-caret").click()
    # Select the 'Latest 13 Next 13' option from the 'Time' filter dropdown.
    page.locator("div").filter(has_text=re.compile(r"^Latest 13 Next 13$")).nth(1).click()
    # Click on the dropdown for the 'Time' filter again to change the selection.
    page.locator("#time-filterId > .wr-20 > esp-multiselect-dropdown > .multiselect-dropdown > div > .w-100 > .d-flex.align-items-center > .dropdown-caret").click()
    # Select the 'Latest 52 Next 52' option from the 'Time' filter dropdown.
    page.locator("div").filter(has_text=re.compile(r"^Latest 52 Next 52$")).first.click()
    # Click on the dropdown for the 'Time' filter again to change the selection.
    page.locator("#time-filterId > .wr-20 > esp-multiselect-dropdown > .multiselect-dropdown > div > .w-100 > .d-flex.align-items-center > .dropdown-caret").click()
    # Select the 'Latest 104 Next 52' option from the 'Time' filter dropdown.
    page.locator("div").filter(has_text=re.compile(r"^Latest 104 Next 52$")).nth(1).click()
    # Click on the dropdown for the 'Time' filter again to reset the selection.
    page.locator("#time-filterId > .wr-20 > esp-multiselect-dropdown > .multiselect-dropdown > div > .w-100 > .d-flex.align-items-center > .dropdown-caret").click()
    # Select the 'Latest 4 Next 4' option from the 'Time' filter dropdown to reset the filter.
    page.locator("div").filter(has_text=re.compile(r"^Latest 4 Next 4$")).nth(1).click()
    # Click on the dropdown for the 'Event' filter to view available event options.
    page.locator("#event-filterId > .wr-20 > esp-multiselect-dropdown > .multiselect-dropdown > div > .w-100 > .d-flex.align-items-center > .dropdown-caret").click()
    # Click on the first element in the list to expand the filter options.
    page.locator(".d-flex.flex-column.justify-content-center").first.click()
    # Click on the 'Search' textbox to focus on it.
    page.get_by_role("textbox", name="Search").click()
    # Fill the 'Search' textbox with the value 'TLC'.
    page.get_by_role("textbox", name="Search").fill("TLC")
    # Click on the close icon to clear the search input.
    page.locator(".icon.d-flex.pointer.zeb-close").click()
    # Click on the dropdown caret for the 'Ad Location' filter to expand the options.
    page.locator(".not-allowed > .w-100 > .d-flex.align-items-center > .dropdown-caret").first.click()
    # Click on the dropdown caret for the 'Ad Location' filter again to view the options.
    page.locator("#ad-location-filterId > .wr-20 > esp-multiselect-dropdown > .multiselect-dropdown > div > .w-100 > .d-flex.align-items-center > .dropdown-caret").click()
    page.locator(".d-flex.flex-column.justify-content-center").first.click()
    page.locator(".d-flex.flex-column.justify-content-center").first.click()
    page.locator("#ad-location-filterId > .wr-20 > esp-multiselect-dropdown > .multiselect-dropdown > div > .w-100 > .d-flex.align-items-center > .dropdown-caret").click()
    # Click on the dropdown caret for the 'Segment' filter to expand the options.
    page.locator("#segment-filterId > .wr-20 > esp-multiselect-dropdown > .multiselect-dropdown > div > .w-100 > .d-flex.align-items-center > .dropdown-caret").click()
    page.locator(".d-flex.flex-column.justify-content-center").first.click()
    page.locator(".d-flex.flex-column.justify-content-center").first.click()
    page.locator("#segment-filterId > .wr-20 > esp-multiselect-dropdown > .multiselect-dropdown > div > .w-100 > .d-flex.align-items-center > .dropdown-caret").click()
    # Click on the dropdown for the 'Vendor' filter to expand the options.
    page.locator("#vendor-filterId > .wr-20 > esp-multiselect-dropdown > .multiselect-dropdown > div > .w-100").click()
    page.locator(".d-flex.flex-column.justify-content-center").first.click()
    # Click on the first option in the 'Vendor' filter dropdown to select it.
    page.locator(".d-flex.dropdown-option.align-items-center.p-v-5.p-l-32 > .d-flex").first.click()
    # Click on the second option in the 'Vendor' filter dropdown to select it.
    page.locator(".overflow-auto > div:nth-child(2) > .d-flex").click()
    page.locator(".d-flex.flex-column.justify-content-center").first.click()
    # Click on the dropdown caret for the 'Vendor' filter again to view the options.
    page.locator("#vendor-filterId > .wr-20 > esp-multiselect-dropdown > .multiselect-dropdown > div > .w-100 > .d-flex.align-items-center > .dropdown-caret").click()
    # Click on the 'Apply' button to apply the selected filters.
    page.locator("button").filter(has_text=re.compile(r"^Apply$")).click()
    # Click on the dropdown caret to expand the column visibility options.
    page.locator(".ellipses > esp-multiselect-dropdown > .multiselect-dropdown > div > .w-100 > .d-flex.align-items-center > .dropdown-caret").click()
    page.locator(".d-flex.flex-column.justify-content-center").first.click()
    page.locator(".d-flex.flex-column.justify-content-center.font-size-10.align-items-center.checkbox-v2.m-r-10.zeb-check").first.click()
    page.locator(".d-flex.flex-column.justify-content-center.font-size-10.align-items-center.checkbox-v2.m-r-10.zeb-check").first.click()
    page.locator(".d-flex.flex-column.justify-content-center.font-size-10.align-items-center.checkbox-v2.m-r-10.zeb-check").first.click()
    page.locator(".d-flex.flex-column.justify-content-center.font-size-10.align-items-center.checkbox-v2.m-r-10.zeb-check").first.click()
    page.locator(".d-flex.flex-column.justify-content-center").first.click()
    page.locator(".d-flex.flex-column.justify-content-center.font-size-10.align-items-center.checkbox-v2.m-r-10.deselected").first.click()
    page.locator(".d-flex.flex-column.justify-content-center.font-size-10.align-items-center.checkbox-v2.m-r-10.deselected").first.click()
    page.locator(".d-flex.flex-column.justify-content-center.font-size-10.align-items-center.checkbox-v2.m-r-10.deselected").first.click()
    page.locator(".overflow-auto > div:nth-child(5)").click()
    page.locator(".ellipses > esp-multiselect-dropdown > .multiselect-dropdown > div > .w-100 > .d-flex.align-items-center > .dropdown-caret").click()
    page.locator(".wr-20.font-weight-normal > esp-multiselect-dropdown > .multiselect-dropdown > div > .w-100 > .d-flex.align-items-center > .dropdown-caret").click()
    page.locator(".d-flex.flex-column.justify-content-center").first.click()
    page.locator(".d-flex.flex-column.justify-content-center").first.click()
    page.locator(".wr-20.font-weight-normal > esp-multiselect-dropdown > .multiselect-dropdown > div > .w-100 > .d-flex.align-items-center > .dropdown-caret").click()
    # Click on the 'Columns' button to open the column visibility settings.
    page.get_by_role("button", name="columns").nth(2).click()
    # Uncheck the 'Toggle All Columns Visibility' checkbox to deselect all columns.
    page.get_by_role("checkbox", name="Toggle All Columns Visibility").uncheck()
    page.locator("#ag-6720 > .ag-column-panel > .ag-column-select > .ag-column-select-list > .ag-virtual-list-viewport > .ag-virtual-list-container > div > .ag-column-select-column").first.click()
    # Check the checkbox for the '/11/2026 Column' to make it visible.
    page.get_by_role("treeitem", name="/11/2026 Column").get_by_label("Press SPACE to toggle").check()
    # Check the checkbox for the '/18/2026 Column' to make it visible.
    page.get_by_role("treeitem", name="/18/2026 Column").get_by_label("Press SPACE to toggle").check()
    # Check the checkbox for the '/25/2026 Column' to make it visible.
    page.get_by_role("treeitem", name="/25/2026 Column").get_by_label("Press SPACE to toggle").check()
    # Check the checkbox for the '02/01/2026 Column' to make it visible.
    page.get_by_role("treeitem", name="02/01/2026 Column").get_by_label("Press SPACE to toggle visibility (hidden)").check()
    # Check the checkbox for the '/08/2026 Column' to make it visible.
    page.get_by_role("treeitem", name="/08/2026 Column").get_by_label("Press SPACE to toggle visibility (hidden)").check()
    # Check the 'Toggle All Columns Visibility' checkbox to select all columns.
    page.get_by_role("checkbox", name="Toggle All Columns Visibility").check()
    # Click on the 'Columns' button again to close the column visibility settings.
    page.get_by_role("button", name="columns").nth(2).click()
    page.locator(".wr-20.font-weight-normal > esp-multiselect-dropdown > .multiselect-dropdown > div > .w-100 > .d-flex.align-items-center > .dropdown-caret").click()
    page.locator(".d-flex.flex-column.justify-content-center").first.click()
    page.locator(".d-flex.flex-column.justify-content-center").first.click()
    page.locator(".d-flex.dropdown-option.align-items-center.p-v-5.p-l-32 > .d-flex").first.click()
    page.locator(".d-flex.dropdown-option.align-items-center.p-v-5.p-l-32 > .d-flex").first.click()
    page.locator(".d-flex.dropdown-option.align-items-center.p-v-5.p-l-32 > .d-flex").first.click()
    page.locator(".overflow-auto > div:nth-child(4) > .d-flex").click()
    page.locator("div:nth-child(5) > .d-flex").click()
    page.get_by_text("Maximum User Forecast").nth(1).click()
    page.get_by_text("Average User Forecast").nth(1).click()
    page.locator(".overflow-auto > div:nth-child(8)").click()
    page.locator(".d-flex.dropdown-option").first.click()
    page.locator(".wr-20.font-weight-normal > esp-multiselect-dropdown > .multiselect-dropdown > div > .w-100 > .d-flex.align-items-center > .dropdown-caret").click()
    page.locator("div:nth-child(3) > span > .align-middle").click()
    page.locator(".ag-header-cell.ag-header-parent-hidden.ag-header-cell-sortable.ag-header-background.ag-focus-managed.ag-header-active > .ag-header-cell-comp-wrapper > .ag-cell-label-container > .ag-header-icon > .filter-icon").click()
    page.get_by_label("Column Filter").get_by_role("button", name="Apply").click()
    page.get_by_role("button", name="columns").nth(3).click()
    page.get_by_role("checkbox", name="Toggle All Columns Visibility").uncheck()
    page.get_by_role("treeitem", name="Start Week Column").get_by_label("Press SPACE to toggle").check()
    page.get_by_role("treeitem", name="End Week Column").get_by_label("Press SPACE to toggle").check()
    page.get_by_role("treeitem", name="Clone Column").get_by_label("Press SPACE to toggle").check()
    page.get_by_role("treeitem", name="Event Column").get_by_label("Press SPACE to toggle visibility (hidden)").check()
    page.get_by_role("treeitem", name="Market Column").get_by_label("Press SPACE to toggle visibility (hidden)").check()
    page.get_by_role("treeitem", name="Count of Stores Column").get_by_label("Press SPACE to toggle visibility (hidden)").check()
    page.get_by_role("treeitem", name="Spot Column").get_by_label("Press SPACE to toggle visibility (hidden)").check()
    page.get_by_role("checkbox", name="Toggle All Columns Visibility").check()
    page.get_by_role("button", name="columns").nth(3).click()
    page.locator("a").filter(has_text="2").nth(2).click()
    page.locator("a").filter(has_text="3").nth(2).click()
    page.locator("div:nth-child(7) > div > .componentParentWrapper > esp-grid-container > esp-card-component > .card-container > .card-content > esp-row-dimentional-grid > div > #paginationId > esp-pagination-v2 > .d-flex.w-100 > .pagination-pager > .pagination-first").click()

    # ---------------------
    # Close the browser context to clean up session-specific data.
    context.close()
    # Close the browser to terminate the automation session.
    browser.close()


# Initialize Playwright's synchronous context to start automation.
with sync_playwright() as playwright:
    # Call the 'run' function, passing the Playwright instance to execute the defined automation steps.
    run(playwright)
