import re
from playwright.sync_api import Playwright, sync_playwright, expect

def run(playwright: Playwright) -> None:
    # Launch a Chromium browser instance in non-headless mode for debugging purposes.
    browser = playwright.chromium.launch(headless=False)
    # Create a new browser context to isolate cookies, storage, and other session data.
    context = browser.new_context()
    # Open a new page within the created browser context.
    page = context.new_page()
        # Navigate to the main executive dashboard for the demand planning application.

    # Navigate to the main executive dashboard URL for the demand planning application.
    page.goto("https://stage.wba.esp.antuit.ai/dp/demand-planning/executive-dashboard?workbookId=6&tabIndex=1")
    # --- Active Toolbar Filter Interactions ---
    # Click on the "Product All" filter pill at the top of the page.
    # Click on the 'Product All' filter pill at the top of the page to interact with the product filter.
    page.locator("aeap-active-toolbar-pill").filter(has_text="Product All").click()
    # Click on the "Location All" filter pill.
    # Click on the 'Location All' filter pill to interact with the location filter.
    page.locator("aeap-active-toolbar-pill").filter(has_text="Location All").click()
    # Click on the "User" filter pill.
    # Click on the 'User' filter pill to interact with the user filter.
    page.locator("aeap-active-toolbar-pill").filter(has_text="User").click()

    # --- Main Filter Panel Configuration --
    # Within the panel, click the "Filter" option to reveal filter criteria.
    # Click on the 'Filter' option within the main filter panel to reveal filter criteria.
    page.get_by_text("Filter").first.click()
    # Within the filter options, select the "Alerts" category.
    # Select the 'Alerts' category within the filter options by clicking on it.
    page.locator("#alerts-filterId").get_by_text("Alerts").click()
    #----------------------Selecting Different Filters from the dropdown-----------------------
    # Click on the dropdown caret to expand the dropdown menu, revealing the available filters.
    # Click on the the dropdown caret to expand the dropdown menu which shows the Different Filters.
    page.locator(".w-100.p-h-16.p-v-8.dropdown-label.background-white > .d-flex.align-items-center > .dropdown-caret").click()
    # Let us select each filter one by one now that the dropdown is expanded:
    # Select the 'MAPE' filter from the expanded dropdown menu by clicking on it.
    page.locator("div").filter(has_text=re.compile(r"^MAPE$")).first.click() # click MAPE from the dropdown menu
    # Re-expand the dropdown menu to select the next filter.
    page.locator(".w-100.p-h-16.p-v-8.dropdown-label.background-white > .d-flex.align-items-center > .dropdown-caret").click() # Expand the dropdown menu again'
    # Repeating the same steps for all different Filters in DropDown Menu:
    # Select the 'Under Bias' filter from the dropdown menu by clicking on it.
    page.locator("div").filter(has_text=re.compile(r"^Under Bias$")).nth(1).click()
    # Re-expand the dropdown menu to select the next filter.
    page.locator(".w-100.p-h-16.p-v-8.dropdown-label.background-white > .d-flex.align-items-center > .dropdown-caret").click()
    # Select the 'Over Bias' filter from the dropdown menu by clicking on it.
    page.locator("div").filter(has_text=re.compile(r"^Over Bias$")).nth(1).click()
    # Re-expand the dropdown menu to select the next filter.
    page.locator(".w-100.p-h-16.p-v-8.dropdown-label.background-white > .d-flex.align-items-center > .dropdown-caret").click()
    # Select the 'PVA' filter from the dropdown menu by clicking on it.
    page.locator("div").filter(has_text=re.compile(r"^PVA$")).nth(1).click()
    # Re-expand the dropdown menu to select the next filter.
    page.locator(".w-100.p-h-16.p-v-8.dropdown-label.background-white > .d-flex.align-items-center > .dropdown-caret").click()
    # Select the 'SSIS' filter from the dropdown menu by clicking on it.
    page.locator("div").filter(has_text=re.compile(r"^SSIS$")).nth(1).click()
    # Menu collapses automatically after selecting a filter.    

    #-----------Using the Searchbox to find a specific Filter from the DropDown-----------------
    # Click the dropdown caret to expand the dropdown menu.
    # Click the dropdown caret to expand the dropdown menu.
    page.locator(".w-100.p-h-16.p-v-8.dropdown-label.background-white > .d-flex.align-items-center > .dropdown-caret").click()
    # Fill the search box with "MAPE".
    # Click on the search box to activate it for input.
    page.get_by_role("textbox", name="Search").click()
    # Fill the search box with the text 'MAPE' to filter the dropdown options.
    page.get_by_role("textbox", name="Search").fill("MAPE")
    # Press 'Enter' to confirm the search and apply the filter.
    page.get_by_role("textbox", name="Search").press("Enter")
    # Click on the filtered 'MAPE' option from the dropdown menu to select it.
    page.locator("div").filter(has_text=re.compile(r"^MAPE$")).nth(2).click()
    #----------Click Main Header to navigate to the Alerts Summary Grid section----------------
    # Click on the 'Alerts Summary' header to navigate to the Alerts Summary Grid section.
    page.get_by_text("Alerts Summary").click()
    # Click on the 'Alerts Summary columns (0)' element, possibly to interact with or expand the grid view.
    page.get_by_text("Alerts Summary columns (0)").click()
    # **SUBSECTION 1: Columns:**
    #-----------Click The columns button to expand a drop down menu that contains all the columns that can be viewed in the grid----------------
    # Click the 'columns' button to expand a dropdown menu containing all the columns that can be viewed in the grid.
    page.get_by_role("button", name="columns").click()
    #------------Checkbox to toggle visibility of all columns in the grid----------------
    # Uncheck the 'Toggle All Columns Visibility' checkbox to hide all columns in the grid.
    page.get_by_role("checkbox", name="Toggle All Columns Visibility").uncheck()
    # Check the 'Toggle All Columns Visibility' checkbox to make all columns visible again.
    page.get_by_role("checkbox", name="Toggle All Columns Visibility").check()
    #------------Locate the Search bar and search for specific column----------------
    # Click on the 2nd column element in the dropdown to toggle its visibility.
    page.locator("div:nth-child(2) > .ag-column-select-column").click()
    # Click on the 3rd column element in the dropdown to toggle its visibility.
    page.locator("div:nth-child(3) > .ag-column-select-column").click()
    # Click on the 4th column element in the dropdown to toggle its visibility.
    page.locator("div:nth-child(4) > .ag-column-select-column").click()
    # Click on the 5th column element in the dropdown to toggle its visibility.
    page.locator("div:nth-child(5) > .ag-column-select-column").click()
    # Click on the 6th column element in the dropdown to toggle its visibility.
    page.locator("div:nth-child(6) > .ag-column-select-column").click()
    # Click on the 7th column element in the dropdown to toggle its visibility.
    page.locator("div:nth-child(7) > .ag-column-select-column").click()
    # Click on the 8th column element in the dropdown to toggle its visibility.
    page.locator("div:nth-child(8) > .ag-column-select-column").click()
    # Click on the 9th column element in the dropdown to toggle its visibility.
    page.locator("div:nth-child(9) > .ag-column-select-column").click()
    # Click on the 10th column element in the dropdown to toggle its visibility.
    page.locator("div:nth-child(10) > .ag-column-select-column").click()
    # Check the 'Toggle All Columns Visibility' checkbox again to ensure all columns are selected by default.
    page.get_by_role("checkbox", name="Toggle All Columns Visibility").check() # Check this again to select all columns by default, IMPORTANT
    # Use the Searchbox inside the columns drop down menu to locate a specific column: Example: SSIS
    # Click on the search box inside the columns dropdown menu to focus on it.
    page.get_by_role("textbox", name="Filter Columns Input").click() # Locate Searchbox
    # Type 'SSIS' into the search box to filter columns by this keyword.
    page.get_by_role("textbox", name="Filter Columns Input").fill("SSIS") # Type SSIS
    # Click on the 'SSIS' column to toggle its selection (unselecting it in this case).
    page.get_by_label("SSIS Column").get_by_text("SSIS").click() # This was selected by default earlier, we are unselecting it now.
    # Let us clear the Searchbox now:
    # Click on the search box again to focus on it for clearing the input.
    page.get_by_role("textbox", name="Filter Columns Input").click() # Locate searchbox again
    # Select all text in the search box using 'ControlOrMeta+a'.
    page.get_by_role("textbox", name="Filter Columns Input").press("ControlOrMeta+a") # Select all text in it
    # Clear the search box by filling it with an empty string.
    page.get_by_role("textbox", name="Filter Columns Input").fill("") # Clear Searchbox.
    # Click the 'columns' button again to collapse the dropdown menu, marking the end of the Columns Configuration section.
    page.get_by_role("button", name="columns").click() # Collapse Column Section. This is the end of the Columns Section
    # **End of Subsection**

    # Start of the 'Filter Grid Rows' subsection, which focuses on filtering rows in the grid.
    # **SUBSECTION 2: Filter Grid Rows:**
    # So far we have seen how to select the columns shown in the Grid, Now let us look at how to filter Rows.
    # Every row in the grid has a checkbox. Select THIS PARTICULAR ROW:
    # Select the row with the name '002-SPIRITS' by checking its associated radio button. Note: A long wait time may be required here.
    page.get_by_role("row", name=" 002-SPIRITS").get_by_role("radio").check() # Long wait time is needed here. 
    # Now let us search for a specific row in the grid: 003-WINE:
    # Click the filter icon to open the filtering section, which allows filtering rows by product name or number.
    page.get_by_title("Filter").first.click() # Locate this filter Icon which lets you filter by product name. Clicking this pops open a filtering section.
    # Click the combobox to select a filtering operator (e.g., Contains, Does not contain, etc.).
    page.get_by_role("combobox", name="Filtering operator").click() # This combobox will be visible once the filtering section is expanded. It lets you select the filtering measure. Ex: Contains, Does not contain, etc.
    # Select the 'Contains' option from the filtering operator dropdown to filter rows containing a specific value.
    page.get_by_role("option", name="Contains").click() # Select the "Contains" option here to find rows that Contain a specific product name or number.
    # Click the textbox inside the filtering section to focus on it for entering the filter value.
    page.get_by_role("textbox", name="Filter Value").click() # Locate The textbox inside the filtering menu to type the product name or number you're looking for.
    # Type '003-WINE' into the filter value textbox to search for rows containing this value.
    page.get_by_role("textbox", name="Filter Value").fill("003-WINE") # Type "003-WINE" in the textbox
    # Click the 'Apply' button to apply the filter and display matching rows in the grid. Note: This action also closes the filtering section.
    page.get_by_label("Column Filter").get_by_role("button", name="Apply").click() # Click the apply button here which will locate any matches in the grid and display them. IMPORTANT: This also closes the filtering section.
    # Reopen the filtering section by clicking the filter icon again to clear and reset the filter.
    page.get_by_title("Filter").first.click() # Once your search is successfull, reopen the filtering section by clicking this icon so we can clear and reset. Very Important.
    # Click the 'Clear' button to clear the current filter value.
    page.get_by_role("button", name="Clear").click() # Once reopened, click the "Clear" button.
    # Click the 'Reset' button to reset the filtering section to its default state.
    page.get_by_role("button", name="Reset").click() # After clearing, click the "Reset" button.
    # End of the 'Filter Grid Rows' subsection.
    # **End of Subsection**

    # Start of the 'Drill Operations' subsection, which focuses on navigating the product hierarchy in the grid.
    # **SUBSECTION 3: Drill Operations:**
    # The grid shows product details. Products are arranged in a hierarchy. Here we will explore the product Hierarchy
    # Let us first move downward towards the lowest level in the Product Hierarchy, the drill down operation:
    # Drill Down can be done by double clicking on a particular row in the grid:
    # Double-click on the row with the name '002-SPIRITS' to drill down to the next level in the product hierarchy.
    page.locator("div").filter(has_text=re.compile(r"^002-SPIRITS$")).first.dblclick() # Double click on "002-SPIRITS"
    # Drill Down further:
    # Double-click on the row with the name '002-001-SPIRITS - 50ML VODKA' to drill down further to the lowest level in the product hierarchy.
    page.locator("div").filter(has_text=re.compile(r"^002-001-SPIRITS - 50ML VODKA$")).first.dblclick() # Double Click on "002-001-SPIRITS - 50ML VODKA"
    # After these two drill downs, we are now on the lowest level in the Product Hierarchy.
    # Now let us move back up the Product Hierarchy, the Drill Up operation:
    # Drill Up can be done by right-clicking on a particular row in the grid which opens up a menu of options, from where we can find the option to Drill Up:
    # Right-click on the row with the name ' 40000107173-ABSOLUT CITRON' to open the context menu for drill-up options.
    page.get_by_role("gridcell", name=" 40000107173-ABSOLUT CITRON").click(button="right") # Right click on a particular row
    # Click on the 'Drill up' option in the context menu to move one level up in the product hierarchy.
    page.get_by_text("Drill up").click() # Drill up
    # Drilling Up once more to return back to the Default Grid (Since we drilled down twice, we need to drill up twice):
    # Right-click on the row with the name ' 002-001-SPIRITS - 50ML VODKA' to open the context menu for drill-up options again.
    page.get_by_role("gridcell", name=" 002-001-SPIRITS - 50ML VODKA").click(button="right")
    # Click on the 'Drill up' option in the context menu to move back to the default grid level.
    page.get_by_text("Drill up").click()
    # CRUCIAL Section: After Drill operations, ensure to select a row from the grid:
    # Select the row with the name ' 002-SPIRITS' by checking its associated radio button. Note: A long wait time may be required here.
    page.get_by_role("row", name=" 002-SPIRITS").get_by_role("radio").check() # LONG Wait needed here.
    # End of the 'Drill Operations' subsection.
    # **End of Subsection**

    # Start of the 'Pagination' subsection, which focuses on navigating between pages and modifying rows per page in the grid.
    # **SUBSECTION 4: Pagination**
    # The Grid is loaded in pages where each page displays a fixed number of rows. Here we will navigate between the pages of the grid:
    # Start with page number 1:
    # Click on page number 1 to start navigation from the first page of the grid.
    page.get_by_role("listitem").filter(has_text="1").first.click() # Page 1
    # Click on the first 'a' element to navigate to page 2. Note: This action may not work if the grid has only one page.
    page.locator("a").first.click() # Navigate to Page 2. IMPORTANT: Some grids may have only a single page so this might not always work. That does not necessarily make it a failure.
    # Click on the left chevron button to navigate to the previous set of 5 pages in the grid.
    page.locator(".zeb-chevron-left").first.click() # This button lets you navigate between the previous set of 5 pages in the grid.
    # Click on the right chevron button to navigate to the next set of 5 pages in the grid.
    page.locator(".pagination-next > .zeb-chevron-right").first.click() # This button shifts to the next set of 5 pages between the grid.
    # Click on the 'navigate to first' button to select the first set of 5 pages in the grid.
    page.locator(".zeb-nav-to-first").first.click() # This button let you select between the first 5 pages of the grid.
    # Click on the 'navigate to last' button to select the last set of 5 pages in the grid.
    page.locator(".zeb-nav-to-last").first.click() # This button lets you select between the last 5 pages of the grid.
    # IMPORTANT: After making these actions, always navigate back to the first 5 pages and go back to page 1.
    # Navigate back to the first set of 5 pages in the grid.
    page.locator(".zeb-nav-to-first").first.click()
    # Click on page number 1 again to return to the first page of the grid.
    page.get_by_role("listitem").filter(has_text="1").first.click()
    # Now let's see the rows per page. By default, 10 rows are displayed on each page, but we can modify this:
    # Use the specific caret icon to expand a dropdown and select the number of rows per page you want:
    # Click on the specific caret icon to expand the dropdown for selecting the number of rows per page.
    page.locator(".d-flex > esp-multiselect-dropdown > .multiselect-dropdown > div > .w-100 > .d-flex.align-items-center > .dropdown-caret").first.click() # This specific caret expands the dropdown
    # Select the option to view 10 rows per page. Note: A wait time may be required here.
    page.locator("div").filter(has_text=re.compile(r"^View 10 row\(s\)$")).first.click() # Select 10 rows, Wait time is needed here.
    # Expand the dropdown again to modify the rows per page setting.
    page.locator(".d-flex > esp-multiselect-dropdown > .multiselect-dropdown > div > .w-100 > .d-flex.align-items-center > .dropdown-caret").first.click()
    # Select the option to view 20 rows per page.
    page.locator("div").filter(has_text=re.compile(r"^View 20 row\(s\)$")).first.click() # Repeating for 20 rows per page
    # Expand the dropdown again to modify the rows per page setting.
    page.locator(".d-flex > esp-multiselect-dropdown > .multiselect-dropdown > div > .w-100 > .d-flex.align-items-center > .dropdown-caret").first.click()
    # Select the option to view 50 rows per page.
    page.locator("div").filter(has_text=re.compile(r"^View 50 row\(s\)$")).first.click() # Repeating for 50 rows
    # IMPORTANT, always ensure to select 10 rows per page after exploring the options:
    # Expand the dropdown again to reset the rows per page setting to 10 rows.
    page.locator(".d-flex > esp-multiselect-dropdown > .multiselect-dropdown > div > .w-100 > .d-flex.align-items-center > .dropdown-caret").first.click()
    # Select the option to view 10 rows per page again to ensure the default setting is restored.
    page.locator("div").filter(has_text=re.compile(r"^View 10 row\(s\)$")).first.click()
    # End of the 'Pagination' subsection.
    # **End of Subsection**


    # Start of the 'Product Markers' subsection, which focuses on marking products with specific statuses.
    # **SUBSECTION 5: Product Markers:**
    # The grid shows Product data, and lets you mark specific products as Not Started, In Progress or Completed:
    # Locate and click on the row in the grid that corresponds to the product '013-SNACK BARS'.
    page.locator("div").filter(has_text=re.compile(r"^013-SNACK BARS$")).first.click() # First Locate a specific row on the Grid
    # Click on the dropdown caret to expand the menu for selecting a status marker for the product.
    page.locator(".ag-cell-value.ag-cell-focus > .ag-cell-wrapper > .ag-group-value > aeap-group-cell-renderer > .cellLabel > #statusDropdownId > esp-multiselect-dropdown > .multiselect-dropdown > div > .w-100 > .d-flex.align-items-center > .dropdown-caret").click() # This caret expands the menu to choose a marker
    # Select the 'Not started' status from the expanded dropdown menu. Note: A wait time may be required here.
    page.locator("div").filter(has_text=re.compile(r"^Not started$")).first.click() # Once the menu is expanded, select "Not started". # Wait time needed
    # Repeat for "In Progress and Completed"
    # Click on the dropdown caret again to expand the menu for selecting a new status marker.
    page.locator(".ag-cell-value.ag-cell-focus > .ag-cell-wrapper > .ag-group-value > aeap-group-cell-renderer > .cellLabel > #statusDropdownId > esp-multiselect-dropdown > .multiselect-dropdown > div > .w-100 > .d-flex.align-items-center > .dropdown-caret").click()
    # Select the 'In progress' status from the expanded dropdown menu. Note: A wait time may be required here.
    page.locator("div").filter(has_text=re.compile(r"^In progress$")).first.click() # Wait time needed.
    # Click on the dropdown caret again to expand the menu for selecting a new status marker.
    page.locator(".ag-cell-value.ag-cell-focus > .ag-cell-wrapper > .ag-group-value > aeap-group-cell-renderer > .cellLabel > #statusDropdownId > esp-multiselect-dropdown > .multiselect-dropdown > div > .w-100 > .d-flex.align-items-center > .dropdown-caret").click()
    # Select the 'Completed' status from the expanded dropdown menu. Note: A wait time may be required here.
    page.locator("div").filter(has_text=re.compile(r"^Completed$")).first.click() # Wait time needed.
    # Reminder: Always return the status to the default 'Not Started' after testing other statuses.
    # IMPORTANT: The default is Not Started, so always return to the default after exploring
    # Click on the dropdown caret to expand the menu for selecting a status marker.
    page.locator(".ag-cell-value.ag-cell-focus > .ag-cell-wrapper > .ag-group-value > aeap-group-cell-renderer > .cellLabel > #statusDropdownId > esp-multiselect-dropdown > .multiselect-dropdown > div > .w-100 > .d-flex.align-items-center > .dropdown-caret").click()
    # Select the 'Not started' status from the expanded dropdown menu. Note: A wait time may be required here.
    page.locator("div").filter(has_text=re.compile(r"^Not started$")).first.click() # Wait time needed.
    # **End of Subsection**

    # **SUBSECTION 6: Exports and Preferences:**
    # This section of the grid is used after exploring the grid, when we want to save our preferences or export grid data:
    # Preferences section:
    # Click on the Preferences icon to expand the Preferences Menu, which contains options for saving or resetting preferences.
    page.locator("esp-grid-icons-component").filter(has_text="Preference").locator("#preference-iconId").click() # This button expands the Preferences Menu with 2 options: Save preferences or Reset Preferences
    # Click on 'Save Preference' to save the current grid preferences. Note: This action involves a heavy wait time.
    page.locator("div").filter(has_text=re.compile(r"^Save Preference$")).first.click() # Save Preferences. HEAVY wait time here.
    # Click on the Preferences icon again to re-expand the Preferences Menu.
    page.locator("esp-grid-icons-component").filter(has_text="Preference").locator("#preference-iconId").click()
    # Click on 'Reset Preference' to reset the grid preferences to default. Note: This action involves a heavy wait time.
    page.locator("div").filter(has_text=re.compile(r"^Reset Preference$")).first.click() # Rest Preference. HEAVY wait time.

    # Export section: HEAVY Wait time here.
    # Initiate a download action by clicking the export icon. This action is wrapped in an 'expect_download' block to handle the file download process.
    with page.expect_download() as download_info:
        page.locator(".icon-color-toolbar-active.zeb-download-underline").first.click()
    download = download_info.value
    # **End of Subsection**

    #CRITICAL STEP: Always select one row from the Grid:
    # Select the row with the name '002-SPIRITS' in the grid by checking its associated radio button. Note: This action involves an extra heavy wait time of approximately 2 minutes.
    page.get_by_role("row", name=" 002-SPIRITS").get_by_role("radio").check() # EXTRA HEAVY Wait time. (2 min)
    #-------In Order to Load the Locations Section we need to select a product from the Alerts Grid. This step is crucial and cannot be skipped------------------------
    # Select the row with the name '002-SPIRITS' again in the grid by checking its associated radio button. This step is necessary to load the locations section, as the data is dependent on the selected product in the alerts grid.
    page.get_by_role("row", name=" 002-SPIRITS").get_by_role("radio").check()# Selecting the product "008-LIGHTERS" from the alerts grid to load the locations section. This is necessary as locations data is loaded based on the selected product in the alerts grid.
    #-----------Click the chevron icon to expand the Location Section since by default it will be collapsed. This step is crucial.----------------
    # Click on the chevron icon (with the class '.pointer.chevron.zeb-chevron-right.m-r-12.collapsed') to expand the Location Section, which is collapsed by default. This step is critical for accessing location-related data.
    page.locator(".pointer.chevron.zeb-chevron-right.m-r-12.collapsed").click()
    #-----------Now let's interact with the filters available in the Location section----------------
    # Click on the columns icon to open the list of available columns in the Locations grid.
    page.get_by_role("button", name="columns").nth(1).click()# Click on the columns icon to view the list of columns available in the Locations grid
    #------------------Locate the text box that lets you search for columns and use it to search for "Store Count" column----------------
    # Click on the search text box to focus on it for filtering columns.
    page.get_by_role("textbox", name="Filter Columns Input").click()
    # Type 'Store Count' into the search text box to filter the columns list.
    page.get_by_role("textbox", name="Filter Columns Input").fill("Store Count")
    # Press 'Enter' to apply the filter and display only the 'Store Count' column in the list.
    page.get_by_role("textbox", name="Filter Columns Input").press("Enter")
    #------------------After hitting "Enter", the "Store Count" column should be the only option in the list of columns. Select the Store Count option from here and then clear the Search box----------------
    # Select the 'Store Count' column by checking its associated checkbox to add it to the Locations grid.
    page.get_by_role("checkbox", name="Press SPACE to toggle").check() # Selecting the Store Count column from the columns dropdown to add it to the Locations grid
    #------------------Clearing the search box to view all columns again in the columns dropdown----------------
    # Clear the search box by selecting all text using 'ControlOrMeta+a'.
    page.get_by_role("textbox", name="Filter Columns Input").press("ControlOrMeta+a")
    # Clear the search box by replacing its content with an empty string.
    page.get_by_role("textbox", name="Filter Columns Input").fill("")
    #----------------Deselecting the desired columns from the Columns dropdown to display in the Locations grid. Here we are selecting Store Count, Product Count and 13W-Fcst columns to be displayed in the grid----------------
    # Deselect the 'Prev 13W Sell-Thru (TY)' column by unchecking its associated checkbox.
    page.get_by_role("treeitem", name="Prev 13W Sell-Thru (TY) Column").get_by_label("Press SPACE to toggle").uncheck()
    # Deselect the '13W-Fcst' column by unchecking its associated checkbox.
    page.get_by_role("treeitem", name="13W-Fcst Column").get_by_label("Press SPACE to toggle").uncheck()
    # Deselect the 'Product Count' column by unchecking its associated checkbox.
    page.get_by_role("treeitem", name="Product Count Column").get_by_label("Press SPACE to toggle").uncheck()
    # Click on the 'Store Count' column to ensure it is selected in the grid.
    page.get_by_role("treeitem", name="Store Count Column").click()
    # Select all columns in the Locations grid by checking the 'Toggle All Columns Visibility' option. Ensure at least one column is selected to avoid an empty grid.
    page.get_by_role("checkbox", name="Toggle All Columns Visibility").check() # Finally Selecting all columns using the "Toggle All Columns" option to display all columns in the Locations grid. Always Ensure that atleast one column is selected to avoid having an empty grid which can cause issues with test execution.
    # Click the columns button again to collapse the columns section.
    page.get_by_role("button", name="columns").nth(1).click() # Click the columns button again to collapse the column section.
    #-----------------Click the Main Grid Header-------------------------
    # Click on the main grid header labeled 'Location' to focus on the Location grid.
    page.locator("div").filter(has_text=re.compile(r"^Location$")).first.click()
    #------------------By Default, all Entries in the Location grid are selected. Let's deselect all entries using the header checkbox and then select a few specific locations----------------
    # Deselect all entries in the Location grid by unchecking the header checkbox.
    page.get_by_role("columnheader", name="Location").get_by_role("checkbox").uncheck() # Deselecting all locations using the header checkbox
    #------------------Selecting a specific location from the Grid----------------------
    # Select a specific location, '00023-5001 MONTGOMERY BLVD NE', by checking its associated checkbox in the grid.
    page.get_by_role("gridcell", name="00023-5001 MONTGOMERY BLVD NE").get_by_role("checkbox").check()
    #-----------------Locate the Location Filter to Search for a specific grid row based on its Location-------------------------
    # Click on the filter icon in the Location column header to open the filter options.
    page.locator("#ag-header-cell-menu-button > .filter-icon").click() # Click on the filter icon in the Location column header to open the filter options
    # -----------------Expand the Dropdown to view the different filter options available------------------------
    # Expand the dropdown menu to view the available filter options.
    page.locator(".ag-filter-select > esp-multiselect-dropdown > .multiselect-dropdown > div > .w-100").click()
    #-----------------From the list of filter options, select "Contains" and use it to search for locations that contain "NEW YORK" in their name------------------------
    # Select the 'Contains' filter option to search for locations containing specific text.
    page.get_by_text("Contains").first.click()
    # Click on the search box labeled 'Filter Value' to focus on it for entering filter criteria.
    page.get_by_role("textbox", name="Filter Value").click()# Locate the Search box
    # Type 'New York' into the search box to filter locations containing this text.
    page.get_by_role("textbox", name="Filter Value").fill("New York")# Type "New York"
    # Click the 'Apply' button in the column menu to apply the filter and view the filtered results.
    page.get_by_label("Column Menu").get_by_role("button", name="Apply").click()# Locate the Apply button to apply the filter and view the results
    # Select a location, '-755 BROADWAY-BROOKLYN-New York', by checking its associated checkbox in the grid after filtering.
    page.get_by_role("gridcell", name="-755 BROADWAY-BROOKLYN-New York").get_by_role("checkbox").check() # We found a location with "New York" in its name. Let's select it using the checkbox in the grid.
    #-----------------Now Trying with "Does Not Contain"---------------------------
    # Select the 'Does Not Contain' filter option to search for locations excluding specific text.
    page.locator("div").filter(has_text=re.compile(r"^Does Not Contain$")).nth(1).click()
    # Click on the search box labeled 'Filter Value' to focus on it for entering filter criteria.
    page.get_by_role("textbox", name="Filter Value").click()
    # Type 'New York' into the search box to filter locations that do not contain this text.
    page.get_by_role("textbox", name="Filter Value").fill("New York")
    # Click the 'Apply' button in the column menu to apply the filter and view the filtered results.
    page.get_by_label("Column Menu").get_by_role("button", name="Apply").click()
    # Select a location, '00023-5001 MONTGOMERY BLVD NE', by checking its associated checkbox in the grid after applying the 'Does Not Contain' filter.
    page.get_by_role("gridcell", name="00023-5001 MONTGOMERY BLVD NE").get_by_role("checkbox").check() # Found an Entry that does not contain New York

    #-----------------Saving our preference of Columns in the Locations grid using the "Save Preference" option in the grid icons------------------------
    # Click on the dropdown menu icon in the grid to open the options for saving preferences.
    page.locator(".position-relative > .legend-font > .multiselect-dropdown > .pointer").click()
    # Click on 'Save Preference' to save the current column configuration in the Locations grid.
    page.get_by_text("Save Preference").click()
    #-----------------Resetting the preference of Columns in the Locations grid using the "Reset Preference" option in the grid icons------------------------
    # Click on the dropdown menu icon in the grid to open the options for resetting preferences.
    page.locator(".position-relative > .legend-font > .multiselect-dropdown > .pointer").click()
    # Click on 'Reset Preference' to reset the column configuration in the Locations grid to its default state.
    page.get_by_text("Reset Preference").click()
    # Begin the pagination section for navigating and configuring the Locations grid.
    #---------Pagination Section of the Locations Grid--------------------
    #----------Navigate to the Second page of the Grid--------------------
    # Click on the link labeled '2' to navigate to the second page of the grid.
    page.locator("a").filter(has_text="2").nth(1).click()
    #----------Navigate back to the First page of the Grid-----------------
    # Click on the link labeled '1' to navigate back to the first page of the grid.
    page.locator("a").filter(has_text=re.compile(r"^1$")).click()
    #-----------Click this button the Fetch the Next grid page--------------------
    # Click the button with a right-chevron icon to fetch the next page of the grid.
    page.locator("li:nth-child(5) > .zeb-chevron-right").click()
    #------------Click this button to fetch the previous page--------------------
    # Click the button with a left-chevron icon to fetch the previous page of the grid.
    page.locator("div:nth-child(3) > esp-pagination-v2 > .d-flex.w-100 > .pagination-pager > .pagination-previous > .zeb-chevron-left").click()
    #-----------Click this button to view the last set of Grid pages
    # Click the button labeled 'Last' to navigate to the last set of pages in the grid.
    page.locator("li:nth-child(6) > .zeb-nav-to-last").click()
    #-----------Click this button to view the First set of Grid Pages
    # Click the button labeled 'First' to navigate to the first set of pages in the grid.
    page.locator("div:nth-child(3) > esp-pagination-v2 > .d-flex.w-100 > .pagination-pager > .pagination-first > .zeb-nav-to-first").click()
    #---------------Now Selecting the number of Rows we want to view on each Grid page
    # Click on 'Rows per page' to initiate the selection of the number of rows displayed per grid page.
    page.get_by_text("Rows per page").nth(1).click()
    # Expand the dropdown menu to view options for selecting the number of rows per page.
    page.locator("div:nth-child(3) > esp-pagination-v2 > .d-flex.w-100 > span:nth-child(3) > esp-multiselect-dropdown > .multiselect-dropdown > div > .w-100").click()# Expand a Dropdown menu showing us how many rows we can select
    # Select the option to view 10 rows per page from the dropdown menu.
    page.locator("span").filter(has_text=re.compile(r"^View 10 row\(s\)$")).click() # Selecting 10 rows per page
    # Begin the process of exporting the Locations grid data as an Excel sheet.
    #----------------Now Exporting the Grid as an Excel Sheet--------------------
    # Set up an expectation to handle the file download triggered by the export action.
    with page.expect_download() as download_info:
        # Click on the export icon (specific locator provided) to initiate the download of the grid data.
        page.locator("div:nth-child(3) > div > .componentParentWrapper > esp-grid-container > esp-card-component > .card-container > .title > .grid-icons-container > esp-grid-icons-component > .display-grid-icons > div > #export-iconId > .icon-color-toolbar-active").click()
    # Capture the download information after the export action is triggered.
    download = download_info.value
    # Begin the process of resetting all filters and checks to ensure a clean slate for further actions.
    #-------------Reset All our Filters and Checks, this is mandatory.
    # Click the 'Reset' button within the Alerts tab to clear all filters and settings.
    page.locator("#AlertsTab").get_by_role("button", name="Reset").click()
    # Open the dropdown menu to access reset preferences.
    page.locator(".position-relative > .legend-font > .multiselect-dropdown > .pointer").click()
    # Click on 'Reset Preference' to reset specific settings within the dropdown menu.
    page.get_by_text("Reset Preference").click()
    # Prepare to apply changes after resetting filters. Ensure at least one checkbox is selected before clicking 'Apply' to avoid loading issues.
    #------------Click the "Apply" button. The MOST CRUCIAL STEP, because other sections of the page cannot load unless you click this button. Note that the reset button clears everything. So Select atleast one Checkbox before clicking Apply.
    # Reopen the dropdown menu to perform another reset action.
    page.locator(".position-relative > .legend-font > .multiselect-dropdown > .pointer").click() # Open this menu to do a reset first.
    # Click on 'Reset Preference' again to ensure all settings are cleared before proceeding.
    page.get_by_text("Reset Preference").click() # Reset
    # Select the checkbox for 'Location' to meet the requirement of having at least one selection before applying changes.
    page.get_by_role("row", name="Location ").get_by_role("checkbox").check() # Select this checkbox before clicking apply 
    # Click the 'Apply' button to finalize changes and reload the necessary sections of the page.
    page.get_by_role("button", name="Apply", exact=True).click() # Click "Apply"
    #------------Precursor Steps. THESE ARE VERY IMPORTANT. Elements will not load without them------------
    page.get_by_role("row", name=" 002-SPIRITS").get_by_role("radio").check() # First Select this product from the Alerts Summary Grid. This action is incredibly HEAVY(2 min wait time needed.)
    page.get_by_role("row", name=" 006-GROCERIES").get_by_role("radio").check() # Back up Selection in case "002-SPIRITS" is not working (This also needs 2 min of wait time)


    #----------------------Complex Filter Section Needed to make the graph----------------------
    # Click on the main header of the filter section to expand or access the filter options.
    page.get_by_text("Filter columns (0) TopBottom").nth(1).click()#-------------Main Header of the Filter Section--------------------

    #--------------First Filter: Time ----------------------------------
    # Click on the 'Time' filter heading to begin configuring the time filter.
    page.get_by_text("Time").click()# Locate Filter Heading
    # Click to expand the dropdown menu for selecting different time ranges.
    page.locator("#time-filterId > .wr-20 > esp-multiselect-dropdown > .multiselect-dropdown > div > .w-100").click()# Click this top expand the Dropdown menu for selecting different time ranges
    # Select the 'Latest 4 Next 4' time range option from the dropdown menu.
    page.locator("div").filter(has_text=re.compile(r"^Latest 4 Next 4$")).nth(1).click()# Option to Select a specific time range from the Dropdown Time menu
    # Reopen the dropdown menu to select another time range.
    page.locator("#time-filterId > .wr-20 > esp-multiselect-dropdown > .multiselect-dropdown > div > .w-100").click()# Reopen the Dropdown menu to choose another time range
    # Select the 'Latest 4 Next 13' time range option from the dropdown menu.
    page.locator("div").filter(has_text=re.compile(r"^Latest 4 Next 13$")).nth(1).click()# Choose another time range
    # Reopen the dropdown menu by clicking on the dropdown caret to select another time range.
    page.locator("#time-filterId > .wr-20 > esp-multiselect-dropdown > .multiselect-dropdown > div > .w-100 > .d-flex.align-items-center > .dropdown-caret").click()# Reopen the Dropdown menu to choose another time range
    # Select the 'Latest 13 Next' time range option from the dropdown menu.
    page.get_by_text("Latest 13 Next").click()# Choose another time range
    # Reopen the dropdown menu to select another time range.
    page.locator("#time-filterId > .wr-20 > esp-multiselect-dropdown > .multiselect-dropdown > div > .w-100").click()# Reopen the Dropdown menu to choose another time range
    # Select the 'Latest 52 Next 52' time range option from the dropdown menu.
    page.locator("div").filter(has_text=re.compile(r"^Latest 52 Next 52$")).nth(1).click()# Choose another time range

    #------------------Second Filter: Event-----------------------------
    # Click on the 'Event' filter header to expand or access the event filter options.
    page.get_by_text("Event", exact=True).click()#Locate Filter Header
    # Click to expand the dropdown menu for selecting different events.
    page.locator("#event-filterId > .wr-20 > esp-multiselect-dropdown > .multiselect-dropdown > div > .w-100").click()# Click this top expand the Dropdown menu for selecting different Events
    # Select the first option in the dropdown menu.
    page.locator(".d-flex.dropdown-option").first.click()# Selecting the First option in the Dropdown menu
    # Reopen the dropdown menu to select another event.
    page.locator(".d-flex.dropdown-option.align-items-center.p-v-5.p-l-32 > .d-flex").first.click()# Reopening the Dropdown menu
    # Select the second option in the dropdown menu.
    page.locator(".overflow-auto > div:nth-child(2) > .d-flex").click()#Clicking the Second option in the menu
    # Select the third option in the dropdown menu.
    page.locator(".overflow-auto > div:nth-child(3) > .d-flex").click()# Clicking the third option
    # Close the dropdown menu after selecting events.
    page.locator("#event-filterId > .wr-20 > esp-multiselect-dropdown > .multiselect-dropdown > div > .w-100").click()# Closing the dropdown menu
    # Reopen the dropdown menu to perform further actions.
    page.locator("#event-filterId > .wr-20 > esp-multiselect-dropdown > .multiselect-dropdown > div > .w-100").click()# Reopening the Dropdown meny
    # Click on the search box to search for a specific event.
    page.get_by_role("textbox", name="Search").click()# Locate the Searchbox to search for a particular event
    # Type 'ROT' in the search box to filter the dropdown menu for events containing 'ROT'.
    page.get_by_role("textbox", name="Search").fill("ROT")# Type "ROT" in the Search box, then only the "ROT" event will be available in the Dropdown menu
    # Select the 'ROT - ROTO AD - CORPORATE' option from the filtered dropdown menu.
    page.get_by_text("ROT - ROTO AD - CORPORATE").click()# Select the "ROT" option from the Dropdown menu
    # Close the dropdown menu after selecting the 'ROT' event.
    page.locator(".icon.d-flex.pointer.zeb-close").click()# Click this to close the Dropdown menu after using the Search bar
    # Reopen the dropdown menu to perform further actions.
    page.locator("#event-filterId > .wr-20 > esp-multiselect-dropdown > .multiselect-dropdown > div > .w-100").click()
    # Click on the first element in the list of options within the dropdown menu.
    page.locator(".d-flex.flex-column.justify-content-center").first.click()
    # Click on the first element in the list of options again, possibly to confirm or toggle the selection.
    page.locator(".d-flex.flex-column.justify-content-center").first.click()

    #------------------Third Filter: Ad RTl-----------------
    # Click on the 'Ad Rtl' header to access the filter options.
    page.get_by_text("Ad Rtl").click()# Locate Ad Rtl Header
    # Click on the first element with the locator '.not-allowed > .w-100', indicating no options are available in this filter.
    page.locator(".not-allowed > .w-100").first.click()# There are no options in this filter.

    #-----------------Fourth Filter: Ad Location-------------------
    # Click on the 'Ad Location' header to access the filter options.
    page.get_by_text("Ad Location", exact=True).click()#Locate the Ad Location Header
    # Expand the dropdown menu for the 'Ad Location' filter.
    page.locator("#ad-location-filterId > .wr-20 > esp-multiselect-dropdown > .multiselect-dropdown > div > .w-100").click()# Expand the Dropdown menu for Ad Location
    # Select the first option from the 'Ad Location' dropdown menu.
    page.locator(".d-flex.flex-column.justify-content-center").first.click()# Select the first option from the Dropdown menu
    # Reopen the Dropdown Menu, Locate the Search box, Enter "B" in the Search box and Select an option from the Dropdown menu, Then close the Menu
    # Reopen the dropdown menu for 'Ad Location' to perform further actions.
    page.locator("#ad-location-filterId > .wr-20 > esp-multiselect-dropdown > .multiselect-dropdown > div > .w-100 > .d-flex.align-items-center > .dropdown-caret").click()
    # Click on the search box within the 'Ad Location' dropdown menu.
    page.get_by_role("textbox", name="Search", exact=True).click()
    # Enter the letter 'B' into the search box to filter options.
    page.get_by_role("textbox", name="Search", exact=True).fill("B")
    # Select an option from the filtered results in the 'Ad Location' dropdown menu.
    page.locator(".d-flex.dropdown-option.align-items-center.p-v-5.p-l-32").click()
    # Close the 'Ad Location' dropdown menu after making a selection.
    page.locator(".icon.d-flex.pointer.zeb-close").click()# Close after making a selection from the Dropdown menu

    #----------Fifth Filter: Segment---------------------
    # Click on the 'Segment' filter header to access its options.
    page.get_by_text("Segment", exact=True).click()# Locate Segment Filter Header
    # Click on the 'Segment' filter header again to ensure it is activated.
    page.get_by_text("Segment", exact=True).click()
    # Open the dropdown menu for the 'Segment' filter.
    page.locator("#segment-filterId > .wr-20 > esp-multiselect-dropdown > .multiselect-dropdown > div > .w-100").click()# Open the Dropdown menu for Segment Filter
    # Select the first option from the 'Segment' dropdown menu.
    page.locator(".d-flex.flex-column.justify-content-center").first.click()# Select the first option
    # Select some more options
    # Select an additional option from the 'Segment' dropdown menu.
    page.locator(".d-flex.dropdown-option.align-items-center.p-v-5.p-l-32 > .d-flex").first.click()
    # Select the second option from the 'Segment' dropdown menu.
    page.locator(".overflow-auto > div:nth-child(2) > .d-flex").click()
    # Select the third option from the 'Segment' dropdown menu.
    page.locator(".overflow-auto > div:nth-child(3) > .d-flex").click()
    # Select the fourth option from the 'Segment' dropdown menu.
    page.locator(".overflow-auto > div:nth-child(4) > .d-flex").click()
    # Use the Search bar to find a particular Option from the Dropdown. Type "A1" in the Search bar, Select the First option from the Dropdown and exit the Segments Dropdown Menu:
    # Click on the search bar dropdown caret within the 'Segment' filter to enable searching.
    page.locator("#segment-filterId > .wr-20 > esp-multiselect-dropdown > .multiselect-dropdown > div > .w-100 > .d-flex.align-items-center > .dropdown-caret").click()
    # Click on the search box within the 'Segment' filter dropdown menu.
    page.get_by_role("textbox", name="Search", exact=True).click()
    # Type 'A1' into the search box to filter options in the 'Segment' dropdown menu.
    page.get_by_role("textbox", name="Search", exact=True).fill("A1")
    # Select the first option from the filtered results in the 'Segment' dropdown menu.
    page.locator(".d-flex.dropdown-option.align-items-center.p-v-5.p-l-32 > .d-flex").click()
    # Close the 'Segment' dropdown menu after making a selection.
    page.locator(".icon.d-flex.pointer.zeb-close").click()# Close after Section


    #------------------Sixth Filter: Vendor---------------------
    # Click on the 'Vendor' filter header to access its options.
    page.get_by_text("Vendor", exact=True).click()# Locate Vendor Filter Header
    # Expand the dropdown menu for the 'Vendor' filter.
    page.locator("#vendor-filterId > .wr-20 > esp-multiselect-dropdown > .multiselect-dropdown > div > .w-100").click() # Expand the Dropdown menu for Vendor Filter
    # Select the first option from the 'Vendor' dropdown menu.
    page.locator(".d-flex.flex-column.justify-content-center").first.click() # Click the first option from the Dropdown Menu
    # Selecting some more options from the Menu
    # Select an additional option from the 'Vendor' dropdown menu.
    page.locator(".d-flex.dropdown-option.align-items-center.p-v-5.p-l-32 > .d-flex").first.click() 
    # Select the second option from the 'Vendor' dropdown menu.
    page.locator(".overflow-auto > div:nth-child(2) > .d-flex").click()
    # Select the third option from the 'Vendor' dropdown menu.
    page.locator(".overflow-auto > div:nth-child(3) > .d-flex").click()
    # Select the fourth option from the 'Vendor' dropdown menu.
    page.locator(".overflow-auto > div:nth-child(4) > .d-flex").click()
    # Select the fifth option from the 'Vendor' dropdown menu.
    page.locator(".overflow-auto > div:nth-child(5) > .d-flex").click()
    # Locate The Searchbox, Type "BIC CORP". Then Select an option from the Menu, and close the Menu:
    # Click on the search box within the 'Vendor' filter dropdown menu.
    page.get_by_role("textbox", name="Search", exact=True).click()# Locate Search box
    # Type 'BIC CORP' into the search box to filter options in the 'Vendor' dropdown menu.
    page.get_by_role("textbox", name="Search", exact=True).fill("BIC CORP")# Type BIC CORP
    # Select an option from the filtered results in the 'Vendor' dropdown menu.
    page.locator(".d-flex.dropdown-option.align-items-center.p-v-5.p-l-32 > .d-flex").click()# Click an option from Menu
    # Close the 'Vendor' dropdown menu after making a selection.
    page.locator(".icon.d-flex.pointer.zeb-close").click()# Collapse the Menu

    #----------Seventh Filter: Season--------------
    # Click on the 'Season' filter header to access its options.
    page.get_by_text("Season", exact=True).click() # Locate the Season Filter Header
    # Expand the dropdown menu for the 'Season' filter.
    page.locator("#season-filterId > .wr-20 > esp-multiselect-dropdown > .multiselect-dropdown > div > .w-100").click()# Expand the Dropdown Menu for Season Filter
    # Select the first option from the 'Season' dropdown menu.
    page.locator(".d-flex.flex-column.justify-content-center").first.click()# Select the First option
    # Selecting other options
    # Select an additional option from the 'Season' dropdown menu.
    page.locator(".d-flex.dropdown-option.align-items-center.p-v-5.p-l-32 > .d-flex").click()
    # Use the Search box to find a particular option from the Menu, Select it, and collapse the Menu
    # Click on the search box within the 'Season' filter dropdown menu.
    page.get_by_role("textbox", name="Search", exact=True).click()
    # Type 'BASIC' into the search box to filter options in the 'Season' dropdown menu.
    page.get_by_role("textbox", name="Search", exact=True).fill("BASIC")
    # Select an option from the filtered results in the 'Season' dropdown menu.
    page.locator(".d-flex.dropdown-option.align-items-center.p-v-5.p-l-32").click()
    # Close the 'Season' dropdown menu after making a selection.
    page.locator(".icon.d-flex.pointer.zeb-close").click()# Collapse after Selecting an option

    #----------------Eighth Filter: Season Category-----------------
    # Click on the 'Season Category' header to access its options.
    page.get_by_text("Season Category").click() # Locate the Season Category Header
    # Click on the third 'None' option under the 'Season Category' filter.
    page.get_by_text("None").nth(2).click() # No options Here.


    #---------------Final Section After using all Filters: Apply them-------------------------
    # Click on the 'Apply' button to finalize and apply all selected filters.
    page.locator("button").filter(has_text=re.compile(r"^Apply$")).click() # Most Crucial Action. Always apply at the end.


    #----------------------Weekly Trend Graph Section based on the complex filters----------------------
    # Click on 'Weekly Trend' to navigate to the Weekly Trend Graph section.
    page.get_by_text("Weekly Trend").click() # Locate the Main Header
    # Expand the Main Drop down menu to display the measures you want to be shown on the graph
    # Expand the dropdown menu to display available measures for the Weekly Trend Graph.
    page.locator(".ellipses > esp-multiselect-dropdown > .multiselect-dropdown > div > .w-100 > .d-flex.align-items-center > .dropdown-caret").click()# Expand the Menu
    # Select Multiple options from the Dropdown Menu Here
    # Select the first option from the dropdown menu.
    page.locator(".d-flex.flex-column.justify-content-center").first.click()
    # Click on the first checkbox to select a measure (repeated for multiple measures).
    page.locator(".d-flex.flex-column.justify-content-center.font-size-10.align-items-center.checkbox-v2.m-r-10.deselected").first.click()
    page.locator(".d-flex.flex-column.justify-content-center.font-size-10.align-items-center.checkbox-v2.m-r-10.deselected").first.click()
    page.locator(".d-flex.flex-column.justify-content-center.font-size-10.align-items-center.checkbox-v2.m-r-10.deselected").first.click()
    page.locator(".d-flex.flex-column.justify-content-center.font-size-10.align-items-center.checkbox-v2.m-r-10.deselected").first.click()
    # Click on the 6th div element within the overflow container to select a measure.
    page.locator(".overflow-auto > div:nth-child(6)").click()
    page.locator("div:nth-child(7) > .d-flex").click()
    page.locator("div:nth-child(8) > .d-flex").click()
    page.locator(".overflow-auto > div:nth-child(7)").click()
    page.locator("div:nth-child(8) > .d-flex").click()
    page.locator(".overflow-auto > div:nth-child(9)").click()
    page.locator(".overflow-auto > div:nth-child(10)").click()
    page.locator(".overflow-auto > div:nth-child(11)").click()
    page.locator("div:nth-child(12) > .d-flex").click()
    # Click on 'Weekly Summary' to navigate to the Weekly Summary grid section.
    page.get_by_text("Weekly Summary").click() # Main Header for the Weekly Summary grid
    # Locate the Dropdown Menu, Expand and Select the measures you want to see:
    # Expand the dropdown menu to display available measures for the Weekly Summary grid.
    page.locator(".wr-20.font-weight-normal > esp-multiselect-dropdown > .multiselect-dropdown > div > .w-100").click()
    # Select the first option from the dropdown menu (repeated for multiple measures).
    page.locator(".d-flex.flex-column.justify-content-center").first.click()
    page.locator(".d-flex.flex-column.justify-content-center").first.click()
    page.locator(".d-flex.dropdown-option.align-items-center.p-v-5.p-l-32 > .d-flex").first.click()
    page.locator(".d-flex.flex-column.justify-content-center.font-size-10.align-items-center.checkbox-v2.m-r-10.zeb-check").first.click()
    page.locator(".d-flex.flex-column.justify-content-center.font-size-10.align-items-center.checkbox-v2.m-r-10.zeb-check").first.click()
    page.locator(".d-flex.flex-column.justify-content-center.font-size-10.align-items-center.checkbox-v2.m-r-10.zeb-check").first.click()
    page.locator(".d-flex.flex-column.justify-content-center.font-size-10.align-items-center.checkbox-v2.m-r-10.zeb-check").first.click()
    page.locator(".d-flex.flex-column.justify-content-center.font-size-10.align-items-center.checkbox-v2.m-r-10.zeb-check").first.click()
    page.locator(".d-flex.flex-column.justify-content-center.font-size-10.align-items-center.checkbox-v2.m-r-10.zeb-check").first.click()
    page.locator(".d-flex.flex-column.justify-content-center.font-size-10.align-items-center.checkbox-v2.m-r-10.zeb-check").first.click()
    page.locator(".d-flex.flex-column.justify-content-center.font-size-10.align-items-center.checkbox-v2.m-r-10.zeb-check").first.click()
    page.locator("div:nth-child(40) > .d-flex").click()
    page.locator("div:nth-child(39) > .d-flex").click()
    page.locator("div:nth-child(39) > .d-flex").click()
    page.locator("div:nth-child(35) > .d-flex").click()
    page.locator("div:nth-child(34) > .d-flex").click()
    page.locator("div:nth-child(33) > .d-flex").click()
    # Select all possible measures using the first option in the dropdown menu.
    # I am Selecting All Possible Measures using this action:
    page.locator(".d-flex.flex-column.justify-content-center").first.click()
    # Collapse the Menu After Selection:
    # Collapse the dropdown menu after selecting measures.
    page.locator(".wr-20.font-weight-normal > esp-multiselect-dropdown > .multiselect-dropdown > div > .w-100 > .d-flex.align-items-center > .dropdown-caret").click()
    # Columns Section to Select Particular Dates:
    # Click on the 'Columns' button to expand the dropdown menu for column configuration.
    page.get_by_role("button", name="columns").nth(2).click() # Click this button and expand the Dropdown menu
    # By Default, all Dates will be Selected, so we will unselect all of them and select a few specific dates:
    # Unselect all columns by unchecking the 'Toggle All Columns Visibility' checkbox.
    page.get_by_role("checkbox", name="Toggle All Columns Visibility").uncheck() # Unselect all Dates First
    # Now Select a few options from the Dropdown Menu
    # Select the column corresponding to '/02/2025' by checking its checkbox.
    page.get_by_role("treeitem", name="/02/2025 Column").get_by_label("Press SPACE to toggle").check()
    # Select the column corresponding to '/09/2025' by checking its checkbox.
    page.get_by_role("treeitem", name="/09/2025 Column").get_by_label("Press SPACE to toggle").check()
    # Select the column corresponding to '/16/2025' by checking its checkbox.
    page.get_by_role("treeitem", name="/16/2025 Column").get_by_label("Press SPACE to toggle").check()
    # Select the column corresponding to '/23/2025' by checking its checkbox.
    page.get_by_role("treeitem", name="/23/2025 Column").get_by_label("Press SPACE to toggle").check()
    # Select the column corresponding to '/30/2025' by checking its checkbox (initially hidden).
    page.get_by_role("treeitem", name="/30/2025 Column").get_by_label("Press SPACE to toggle visibility (hidden)").check()
    # Select the column corresponding to '/07/2025' by checking its checkbox (initially hidden).
    page.get_by_role("treeitem", name="/07/2025 Column").get_by_label("Press SPACE to toggle visibility (hidden)").check()
    # Select the column corresponding to '/14/2025' by checking its checkbox (initially hidden).
    page.get_by_role("treeitem", name="/14/2025 Column").get_by_label("Press SPACE to toggle visibility (hidden)").check()
    # Use the Search box to Search for a specific date. This will reduce the options in the Menu to only that specific Date. Select it.
    # Click on the search box to filter columns by a specific date.
    page.get_by_role("textbox", name="Filter Columns Input").click()
    # Enter '01/11/2026' in the search box to filter the columns.
    page.get_by_role("textbox", name="Filter Columns Input").fill("01/11/2026")
    # Select the filtered column corresponding to '01/11/2026' by checking its checkbox.
    page.get_by_role("checkbox", name="Press SPACE to toggle").check()
    # I am now Clearing the Searchbox, Selecting all Dates again and closing Columns section
    # Clear the search box by selecting all text and deleting it.
    page.get_by_role("textbox", name="Filter Columns Input").press("ControlOrMeta+a")
    page.get_by_role("textbox", name="Filter Columns Input").fill("")
    # Re-select all columns by checking the 'Toggle All Columns Visibility' checkbox.
    page.get_by_role("checkbox", name="Toggle All Columns Visibility").check()
    # Click on the 'Columns' button again to close the dropdown menu for column configuration.
    page.get_by_role("button", name="columns").nth(2).click()# Click this to close
    # Preference Section, We can Save Preference or Reset Preference
    # Click to expand the Preference Section to access options like Save or Reset Preference.
    page.locator("div:nth-child(4) > #preference-iconId > .legend-font > .multiselect-dropdown > .pointer").click() # Click to expand the Preference Section
    # Click on 'Save Preference' to save the current grid configuration or settings.
    page.get_by_text("Save Preference").click() # Saving Preference
    # Resetting Preference
    # Click on the notification circle, possibly to acknowledge or clear notifications before resetting preferences.
    page.locator(".notification-circle").click()
    # Click to expand the Preference Section again, likely to access the Reset Preference option.
    page.locator(".position-relative > .legend-font > .multiselect-dropdown > .pointer").click()
    # Click on 'Reset Preference' to revert the grid configuration or settings to their default state.
    page.get_by_text("Reset Preference").click()
    # Exporting the Grid as an Excel Sheet
    # Prepare to handle a file download event triggered by the next action.
    with page.expect_download() as download1_info:
        # Click on the Export button to download the grid data as an Excel sheet.
        page.locator("div:nth-child(3) > #export-iconId > .icon-color-toolbar-active").click()
    download1 = download1_info.value
    # Ensure the 'Toggle All Columns Visibility' checkbox is checked in the Columns Section before expanding measures in the grid, as actions may fail otherwise.
    #------Expanding Some Measures in the Grid by clicking on Chevron Icon. Note, only do this if you have Selected  page.get_by_role("checkbox", name="Toggle All Columns Visibility").check() From the Columns Section, otherwise they may fail
    # Click on the 'Forecast Alerts - SSIS' text to select or focus on this section in the grid.
    page.locator("span").filter(has_text="Forecast Alerts - SSIS").first.click()
    # Click on the chevron icon within the last left-pinned cell to expand a measure in the grid.
    page.locator(".ag-cell-value.ag-cell.ag-cell-not-inline-editing.ag-cell-normal-height.ag-cell-last-left-pinned.ag-column-first.ag-cell-override-normal.notosans-overwrite.no-border.ag-cell-focus > .ag-cell-wrapper > .ag-group-contracted > .zeb-chevron-right").click()
    # Click on the first chevron icon within expandable cells to expand a measure in the grid.
    page.locator(".ag-cell-wrapper.ag-cell-expandable > .ag-group-contracted > .zeb-chevron-right").first.click()
    # Click on the 'Digital Sales' text to select or focus on this section in the grid.
    page.locator("span").filter(has_text="Digital Sales").first.click()
    # Click on the chevron icon within an expandable cell at indentation level 1 to expand a measure in the grid.
    page.locator(".ag-cell-wrapper.ag-cell-expandable.ag-row-group.ag-row-group-indent-1 > .ag-group-contracted > .zeb-chevron-right").click()
    # Click on the first chevron icon within expandable cells to expand another measure in the grid.
    page.locator(".ag-cell-wrapper.ag-cell-expandable > .ag-group-contracted > .zeb-chevron-right").first.click()
    # Click on the first chevron icon within a top-level row group to expand a measure in the grid.
    page.locator(".ag-row-no-focus.ag-row-not-inline-editing.ag-row.ag-row-level-0.ag-row-group > .ag-cell-value > .ag-cell-wrapper > .ag-group-contracted > .zeb-chevron-right").first.click()
    # Click on the chevron icon within a contracted top-level row group to expand a measure in the grid.
    page.locator(".ag-row-no-focus.ag-row-not-inline-editing.ag-row.ag-row-level-0.ag-row-group.ag-row-group-contracted > .ag-cell-value > .ag-cell-wrapper > .ag-group-contracted > .zeb-chevron-right").click()
    #---------------------Interacting with the Global Filters and applying filters on Product, Location and User hierarchies----------------------
    # Click on the Global Filters Icon to open the filter panel on the left side of the screen.
    page.locator("#filter-toggle-iconId").click()#-----------This is the main Global Filters Icon which opens the filter panel on the left side of the screen.
    #---------There are 3 main sections in the global filters - Product, Location and User------------
    #-----------------Product Hierarchy Filters-----------------
    # Expand the Product section in the global filters by clicking on 'Product'.
    page.locator("esp-simple-side-filter-panel-v1").get_by_text("Product").click()#Locate Product section in the global filters and click to expand
    #-----------Inside Product section we have  2 main filter categories - Hierarchy and Attribute. Let's expand the Hierarchy section first and apply some filters----------------
    # Expand the Hierarchy section within the Product filters by clicking on 'Hierarchy'.
    page.locator("div").filter(has_text=re.compile(r"^Hierarchy$")).nth(2).click() # Locate and click Hierarchy
    #-----------In Hierarchy we have multiple levels of filters - Merchandise Division, OpStudy, Product Category, PLN.------------------------------------
    # Click on 'Merchandise Division' to select this filter category within the Hierarchy section.
    page.get_by_text("Merchandise Division").click()# Locate and click Merchandise Division filter
    # Click on 'Select All' to select all options under Merchandise Division.
    page.locator("div").filter(has_text=re.compile(r"^Select All$")).click()
    # Click on '00000-NO DIV NAME' to select this specific option under Merchandise Division.
    page.locator("div").filter(has_text=re.compile(r"^00000-NO DIV NAME$")).click()
    # Click on 'Apply Filters' to apply the selected filters for Merchandise Division.
    page.get_by_role("button", name="Apply Filters").click()# Applying filters of Merchandise Division
    # Click on 'OpStudy' to select this filter category within the Hierarchy section.
    page.get_by_text("OpStudy").click()# Locate and click OpStudy filter
    # Click on 'Select All' to select all options under OpStudy.
    page.locator("div").filter(has_text=re.compile(r"^Select All$")).click()
    # Click on '-PPD DEBIT LOAD CARD' to select this specific option under OpStudy.
    page.locator("#SideFilterproducthierarchyId").get_by_text("-PPD DEBIT LOAD CARD").click()
    # Click on 'Apply Filters' to apply the selected filters for OpStudy.
    page.get_by_role("button", name="Apply Filters").click()# Applying filters of OpStudy
    # Click on 'Product Category' to select this filter category within the Hierarchy section.
    page.get_by_text("Product Category").click()# Locate and click Product Category filter
    # Click on 'Select All' to select all options under Product Category.
    page.locator("div").filter(has_text=re.compile(r"^Select All$")).click()
    # Click on '155-001-GC_TRN AMNT - NONRLD TRN' to select this specific option under Product Category.
    page.locator("div").filter(has_text=re.compile(r"^155-001-GC_TRN AMNT - NONRLD TRN$")).click()
    # Click on 'Apply Filters' to apply the selected filters for Product Category.
    page.get_by_role("button", name="Apply Filters").click()# Applying filters of Product Category
    # Click on 'PLN' to select this filter category within the Hierarchy section.
    page.get_by_text("PLN", exact=True).click()# Locate and click PLN filter
    # Click on 'Select All' to select all options under PLN.
    page.locator("div").filter(has_text=re.compile(r"^Select All$")).click()
    # Click on '-VNLA VISA SHNY HX BX VGC $20-$500' to select this specific option under PLN.
    page.get_by_text("-VNLA VISA SHNY HX BX VGC $20-$500").click()
    # Click on 'Apply Filters' to apply the selected filters for PLN.
    page.get_by_role("button", name="Apply Filters").click()# Applying filters of PLN
    #-----------Now let's expand the Attribute section and apply some filters----------------
    # Expand the Attribute section within the Product filters by clicking on 'Attribute'.
    page.locator("div").filter(has_text=re.compile(r"^Attribute$")).nth(2).click()# Locate and click Attribute section under Product hierarchy
    # Click to expand the first attribute filter under the Attribute section.
    page.locator(".d-flex.p-l-32").first.click()# Click to expand the first attribute filter
    # Click on 'Select All' to select all options under the first attribute filter.
    page.locator("div").filter(has_text=re.compile(r"^Select All$")).click()
    # Click on 'AMEX' to select this specific option under the first attribute filter.
    page.locator("div").filter(has_text=re.compile(r"^AMEX$")).click()
    # Click on 'Apply Filters' to apply the selected filters for the first attribute filter.
    page.get_by_role("button", name="Apply Filters").click()# Applying filters of the first attribute
    # Click to expand the second attribute filter under the Attribute section.
    page.locator("div:nth-child(3) > esp-filter-sub-accordion-v1 > .sub-accordion-element > .d-flex").click()# Click to expand the second attribute filter
    # Click on 'Select All' to select all options under the second attribute filter.
    page.locator("div").filter(has_text=re.compile(r"^Select All$")).click()
    # Click on 'N' to select this specific option under the second attribute filter.
    page.locator("div").filter(has_text=re.compile(r"^N$")).click()
    # Click on 'Select All' again to reselect all options under the second attribute filter.
    page.locator("div").filter(has_text=re.compile(r"^Select All$")).click()
    # Click on 'Apply Filters' to apply the selected filters for the second attribute filter.
    page.get_by_role("button", name="Apply Filters").click()# Applying filters of the second attribute
    # Click on 'Import' to select the third attribute filter under the Attribute section.
    page.get_by_text("Import").click()# Click and Locate the Import section which is the third attribute filter
    # Click on 'Select All' to select all options under the Import attribute filter.
    page.locator("div").filter(has_text=re.compile(r"^Select All$")).click()
    # Click on 'Apply Filters' to apply the selected filters for the Import attribute filter.
    page.get_by_role("button", name="Apply Filters").click()# Applying filters of the Import attribute
    # Click on the Aggregate panel at the bottom of the filter panel.
    page.locator(".aggrigate-panel").click()# Aggregate panel at the bottom
    # Click on the checkbox to include aggregated values in the graphs and tables.
    page.locator(".custom-checkbox-wrapper.overflow-hidden.d-flex.justify-content-center.m-r-8.background-primary-color > .pointer").click()# Checkbox to include the aggregated values in the graphs and tables
    # Click on 'Reset' to clear all the applied filters.
    page.get_by_role("button", name="Reset").click()# Perform reset action to clear all the applied filters
    #-----------------Location Hierarchy Filters-----------------
    # Click on 'Location' to expand the Location section in the global filters.
    page.locator("esp-simple-side-filter-panel-v1").get_by_text("Location").click()# Locate Location section in the global filters and click to expand
    # ...Inside Location Section, We have 2 major filter categories under Location hierarchy - Hierarchy and Attribute. Let's expand the Hierarchy section first and apply some filters----------------
    # Click on 'Hierarchy' to expand the Hierarchy section under the Location filters.
    page.locator("div").filter(has_text=re.compile(r"^Hierarchy$")).nth(2).click()# Locate and click Hierarchy under Location section
    #-----------Inside Hierarchy We have 3 main levels: Region, Area and Store. Let's expand Region and apply some filters----------------
    # Click on the Region filter under the Location hierarchy to expand it.
    page.locator(".d-flex.p-l-32").first.click()# Locator for Region filter under Location hierarchy
    # Click on 'Select All' to select all options under the Region filter.
    page.locator("div").filter(has_text=re.compile(r"^Select All$")).click()
    # Click on '00005-Mountain West' to select this specific option under the Region filter.
    page.locator("div").filter(has_text=re.compile(r"^00005-Mountain West$")).click()
    # Click on 'Apply Filters' to apply the selected filters for the Region filter.
    page.get_by_role("button", name="Apply Filters").click()# Applying filters of Region
    # Click on the Area filter under the Location hierarchy to expand it.
    page.locator("div:nth-child(3) > esp-filter-sub-accordion-v1 > .sub-accordion-element > .d-flex").click()# Locator for Area filter under Location hierarchy
    # Click on 'Select All' to select all options under the Area filter.
    page.locator("div").filter(has_text=re.compile(r"^Select All$")).click()
    # Click on '006-Seattle/Oregon' to select this specific option under the Area filter.
    page.locator("div").filter(has_text=re.compile(r"^006-Seattle/Oregon$")).click()
    # Click on 'Apply Filters' to apply the selected filters for the Area filter.
    page.get_by_role("button", name="Apply Filters").click()# Applying filters of Area
    # Click on the Store filter under the Location hierarchy to expand it.
    page.get_by_text("Store", exact=True).click()# Locator for Store filter under Location hierarchy
    # Click on 'Select All' to select all options under the Store filter.
    page.locator("div").filter(has_text=re.compile(r"^Select All$")).click()
    # Click on '00809-8911 N 7TH ST-PHOENIX-Arizona' to select this specific option under the Store filter.
    page.locator("div").filter(has_text=re.compile(r"^00809-8911 N 7TH ST-PHOENIX-Arizona$")).click()
    # Click on 'Apply Filters' to apply the selected filters for the Store filter.
    page.get_by_role("button", name="Apply Filters").click()# Applying filters of Store
    #-----------Now let's expand the Attribute section and apply some filters----------------
    # Click on 'Attribute' to expand the Attribute section under the Location filters.
    page.locator("div").filter(has_text=re.compile(r"^Attribute$")).nth(2).click()# Locate and click Attribute section under Location hierarchy
    # Under Attribute section we have 4 filters - DC, MDG and State and Exclude Billing Stores. Let's apply some filters under each of these attributes----------------
    # Click on 'DC' to expand the DC filter under the Attribute section of the Location hierarchy.
    page.get_by_text("DC").click()# Locate and click DC filter under Attribute section of Location hierarchy
    # Click on 'Select All' to select all options under the DC filter.
    page.locator("div").filter(has_text=re.compile(r"^Select All$")).click()
    # Click on '88006-WOODLAND' to select this specific option under the DC filter.
    page.locator("div").filter(has_text=re.compile(r"^88006-WOODLAND$")).click()
    # Click on 'Apply Filters' to apply the selected filters for the DC filter.
    page.get_by_role("button", name="Apply Filters").click()# Applying filters of DC attribute
    # Click on 'MDG' to expand the MDG filter under the Attribute section of the Location hierarchy.
    page.get_by_text("MDG").click()# Locate and click MDG filter under Attribute section of Location hierarchy
    # Click on 'Select All' to select all options under the MDG filter.
    page.locator("div").filter(has_text=re.compile(r"^Select All$")).click()
    # Click on '290-IDAHO, BOISE' to select this specific option under the MDG filter.
    page.locator("div").filter(has_text=re.compile(r"^290-IDAHO, BOISE$")).click()
    # Click on 'Apply Filters' to apply the selected filters for the MDG filter.
    page.get_by_role("button", name="Apply Filters").click()# Applying filters of MDG attribute
    # Click on 'State' to expand the State filter under the Attribute section of the Location hierarchy.
    page.get_by_text("State").click()# Locate and click State filter under Attribute section of Location hierarchy
    # Click on 'Select All' to select all options under the State filter.
    page.locator("div").filter(has_text=re.compile(r"^Select All$")).click()
    # Click on 'Montana' to select this specific option under the State filter.
    page.locator("div").filter(has_text=re.compile(r"^Montana$")).click()
    # Click on 'Apply Filters' to apply the selected filters for the State filter.
    page.get_by_role("button", name="Apply Filters").click()# Applying filters of State attribute
    # Click on 'Exclude Billing Stores' to expand the Exclude Billing Stores filter under the Attribute section of the Location hierarchy.
    page.get_by_text("Exclude Billing Stores").click()# Locate and click Exclude Billing Stores filter under Attribute section of Location hierarchy
    # Click on 'Select All' to select all options under the Exclude Billing Stores filter.
    page.locator("div").filter(has_text=re.compile(r"^Select All$")).click()
    # Click on 'Apply Filters' to apply the selected filters for the Exclude Billing Stores filter.
    page.get_by_role("button", name="Apply Filters").click()# Applying filters of Exclude Billing Stores attribute
    # Click on 'Reset' to clear all the applied filters under the Location hierarchy.
    page.get_by_role("button", name="Reset").click()# Perform reset action to clear all the applied filters under Location hierarchy
    #-----------------User Hierarchy Filters-----------------
    # Click on 'User' to expand the User section in the global filters.
    page.locator("esp-simple-side-filter-panel-v1").get_by_text("User").click()# Locate User section in the global filters and click to expand
    # ... In User Section we only have Hierarchy category, let's expand and apply some filters----------------
    # Click on 'Hierarchy' under the User section to expand the hierarchy filters.
    page.locator("div").filter(has_text=re.compile(r"^Hierarchy$")).nth(3).click()# Locate and click Hierarchy under User section
    # Click on 'User' within the User hierarchy filters to select it.
    page.locator("#SideFilteruserhierarchyId").get_by_text("User").click()
    # Click on 'Select All' to select all options under the User hierarchy filters.
    page.locator("div").filter(has_text=re.compile(r"^Select All$")).click()
    # Click on '701' to select this specific option under the User hierarchy filters.
    page.locator("div").filter(has_text=re.compile(r"^701$")).click()
    # Click on '701' again to toggle the selection for this specific option under the User hierarchy filters.
    page.locator("div").filter(has_text=re.compile(r"^701$")).click()
    # Click on the first checkbox element under the User hierarchy filters to select it.
    page.locator(".filter-values.d-flex.align-items-center.p-l-32.p-r-24 > .custom-checkbox-wrapper > .pointer").first.click()
    # Click on 'Apply Filters' to apply the selected filters for the User hierarchy.
    page.get_by_role("button", name="Apply Filters").click()# Applying filters of User hierarchy
    # Click on 'Reset' to clear all the applied filters under the User hierarchy.
    page.get_by_role("button", name="Reset").click()# Perform reset action to clear all the applied filters under User hierarchy
    # Close the filter panel after completing all interactions.
    page.close()# Closing the filter panel after interactions. End.
    # ---------------------
    # ---------------------
    # Close the context to end the session and release resources associated with it.
    context.close()
    # Close the browser to terminate the web automation process completely.
    browser.close()


with sync_playwright() as playwright:
    run(playwright)
