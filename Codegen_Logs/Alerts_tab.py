import re
from playwright.sync_api import Playwright, sync_playwright, expect

def run(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
        # Navigate to the main executive dashboard for the demand planning application.

    page.goto("https://stage.wba.esp.antuit.ai/dp/demand-planning/executive-dashboard?workbookId=6&tabIndex=1")
    # --- Active Toolbar Filter Interactions ---
    # Click on the "Product All" filter pill at the top of the page.
    page.locator("aeap-active-toolbar-pill").filter(has_text="Product All").click()
    # Click on the "Location All" filter pill.
    page.locator("aeap-active-toolbar-pill").filter(has_text="Location All").click()
    # Click on the "User" filter pill.
    page.locator("aeap-active-toolbar-pill").filter(has_text="User").click()

    # --- Main Filter Panel Configuration --
    # Within the panel, click the "Filter" option to reveal filter criteria.
    page.get_by_text("Filter").first.click()
    # Within the filter options, select the "Alerts" category.
    page.locator("#alerts-filterId").get_by_text("Alerts").click()
    #----------------------Selecting Different Filters from the dropdown-----------------------
    # Click on the the dropdown caret to expand the dropdown menu which shows the Different Filters.
    page.locator(".w-100.p-h-16.p-v-8.dropdown-label.background-white > .d-flex.align-items-center > .dropdown-caret").click()
    # Let us select each filter one by one now that the dropdown is expanded:
    page.locator("div").filter(has_text=re.compile(r"^MAPE$")).first.click() # click MAPE from the dropdown menu
    page.locator(".w-100.p-h-16.p-v-8.dropdown-label.background-white > .d-flex.align-items-center > .dropdown-caret").click() # Expand the dropdown menu again'
    # Repeating the same steps for all different Filters in DropDown Menu:
    page.locator("div").filter(has_text=re.compile(r"^Under Bias$")).nth(1).click()
    page.locator(".w-100.p-h-16.p-v-8.dropdown-label.background-white > .d-flex.align-items-center > .dropdown-caret").click()
    page.locator("div").filter(has_text=re.compile(r"^Over Bias$")).nth(1).click()
    page.locator(".w-100.p-h-16.p-v-8.dropdown-label.background-white > .d-flex.align-items-center > .dropdown-caret").click()
    page.locator("div").filter(has_text=re.compile(r"^PVA$")).nth(1).click()
    page.locator(".w-100.p-h-16.p-v-8.dropdown-label.background-white > .d-flex.align-items-center > .dropdown-caret").click()
    page.locator("div").filter(has_text=re.compile(r"^SSIS$")).nth(1).click()
    # Menu collapses automatically after selecting a filter.    

    #-----------Using the Searchbox to find a specific Filter from the DropDown-----------------
    # Click the dropdown caret to expand the dropdown menu.
    page.locator(".w-100.p-h-16.p-v-8.dropdown-label.background-white > .d-flex.align-items-center > .dropdown-caret").click()
    # Fill the search box with "MAPE".
    page.get_by_role("textbox", name="Search").click()
    page.get_by_role("textbox", name="Search").fill("MAPE")
    page.get_by_role("textbox", name="Search").press("Enter")
    page.locator("div").filter(has_text=re.compile(r"^MAPE$")).nth(2).click()
    #----------Click Main Header to navigate to the Alerts Summary Grid section----------------
    page.get_by_text("Alerts Summary").click()
    page.get_by_text("Alerts Summary columns (0)").click()
    # **SUBSECTION 1: Columns:**
    #-----------Click The columns button to expand a drop down menu that contains all the columns that can be viewed in the grid----------------
    page.get_by_role("button", name="columns").click()
    #------------Checkbox to toggle visibility of all columns in the grid----------------
    page.get_by_role("checkbox", name="Toggle All Columns Visibility").uncheck()
    page.get_by_role("checkbox", name="Toggle All Columns Visibility").check()
    #------------Locate the Search bar and search for specific column----------------
    page.locator("div:nth-child(2) > .ag-column-select-column").click()
    page.locator("div:nth-child(3) > .ag-column-select-column").click()
    page.locator("div:nth-child(4) > .ag-column-select-column").click()
    page.locator("div:nth-child(5) > .ag-column-select-column").click()
    page.locator("div:nth-child(6) > .ag-column-select-column").click()
    page.locator("div:nth-child(7) > .ag-column-select-column").click()
    page.locator("div:nth-child(8) > .ag-column-select-column").click()
    page.locator("div:nth-child(9) > .ag-column-select-column").click()
    page.locator("div:nth-child(10) > .ag-column-select-column").click()
    page.get_by_role("checkbox", name="Toggle All Columns Visibility").check() # Check this again to select all columns by default, IMPORTANT
    # Use the Searchbox inside the columns drop down menu to locate a specific column: Example: SSIS
    page.get_by_role("textbox", name="Filter Columns Input").click() # Locate Searchbox
    page.get_by_role("textbox", name="Filter Columns Input").fill("SSIS") # Type SSIS
    page.get_by_label("SSIS Column").get_by_text("SSIS").click() # This was selected by default earlier, we are unselecting it now.
    # Let us clear the Searchbox now:
    page.get_by_role("textbox", name="Filter Columns Input").click() # Locate searchbox again
    page.get_by_role("textbox", name="Filter Columns Input").press("ControlOrMeta+a") # Select all text in it
    page.get_by_role("textbox", name="Filter Columns Input").fill("") # Clear Searchbox.
    page.get_by_role("button", name="columns").click() # Collapse Column Section. This is the end of the Columns Section
    # **End of Subsection**

    # **SUBSECTION 2: Filter Grid Rows:**
    # So far we have seen how to select the columns shown in the Grid, Now let us look at how to filter Rows.
    # Every row in the grid has a checkbox. Select THIS PARTICULAR ROW:
    page.get_by_role("row", name=" 002-SPIRITS").get_by_role("radio").check() # Long wait time is needed here. 
    # Now let us search for a specific row in the grid: 003-WINE:
    page.get_by_title("Filter").first.click() # Locate this filter Icon which lets you filter by product name. Clicking this pops open a filtering section.
    page.get_by_role("combobox", name="Filtering operator").click() # This combobox will be visible once the filtering section is expanded. It lets you select the filtering measure. Ex: Contains, Does not contain, etc.
    page.get_by_role("option", name="Contains").click() # Select the "Contains" option here to find rows that Contain a specific product name or number.
    page.get_by_role("textbox", name="Filter Value").click() # Locate The textbox inside the filtering menu to type the product name or number you're looking for.
    page.get_by_role("textbox", name="Filter Value").fill("003-WINE") # Type "003-WINE" in the textbox
    page.get_by_label("Column Filter").get_by_role("button", name="Apply").click() # Click the apply button here which will locate any matches in the grid and display them. IMPORTANT: This also closes the filtering section.
    page.get_by_title("Filter").first.click() # Once your search is successfull, reopen the filtering section by clicking this icon so we can clear and reset. Very Important.
    page.get_by_role("button", name="Clear").click() # Once reopened, click the "Clear" button.
    page.get_by_role("button", name="Reset").click() # After clearing, click the "Reset" button.
    # **End of Subsection**

    # **SUBSECTION 3: Drill Operations:**
    # The grid shows product details. Products are arranged in a hierarchy. Here we will explore the product Hierarchy
    # Let us first move downward towards the lowest level in the Product Hierarchy, the drill down operation:
    # Drill Down can be done by double clicking on a particular row in the grid:
    page.locator("div").filter(has_text=re.compile(r"^002-SPIRITS$")).first.dblclick() # Double click on "002-SPIRITS"
    # Drill Down further:
    page.locator("div").filter(has_text=re.compile(r"^002-001-SPIRITS - 50ML VODKA$")).first.dblclick() # Double Click on "002-001-SPIRITS - 50ML VODKA"
    # After these two drill downs, we are now on the lowest level in the Product Hierarchy.
    # Now let us move back up the Product Hierarchy, the Drill Up operation:
    # Drill Up can be done by right-clicking on a particular row in the grid which opens up a menu of options, from where we can find the option to Drill Up:
    page.get_by_role("gridcell", name=" 40000107173-ABSOLUT CITRON").click(button="right") # Right click on a particular row
    page.get_by_text("Drill up").click() # Drill up
    # Drilling Up once more to return back to the Default Grid (Since we drilled down twice, we need to drill up twice):
    page.get_by_role("gridcell", name=" 002-001-SPIRITS - 50ML VODKA").click(button="right")
    page.get_by_text("Drill up").click()
    # CRUCIAL Section: After Drill operations, ensure to select a row from the grid:
    page.get_by_role("row", name=" 002-SPIRITS").get_by_role("radio").check() # LONG Wait needed here.
    # **End of Subsection**

    # **SUBSECTION 4: Pagination**
    # The Grid is loaded in pages where each page displays a fixed number of rows. Here we will navigate between the pages of the grid:
    # Start with page number 1:
    page.get_by_role("listitem").filter(has_text="1").first.click() # Page 1
    page.locator("a").first.click() # Navigate to Page 2. IMPORTANT: Some grids may have only a single page so this might not always work. That does not necessarily make it a failure.
    page.locator(".zeb-chevron-left").first.click() # This button lets you navigate between the previous set of 5 pages in the grid.
    page.locator(".pagination-next > .zeb-chevron-right").first.click() # This button shifts to the next set of 5 pages between the grid.
    page.locator(".zeb-nav-to-first").first.click() # This button let you select between the first 5 pages of the grid.
    page.locator(".zeb-nav-to-last").first.click() # This button lets you select between the last 5 pages of the grid.
    # IMPORTANT: After making these actions, always navigate back to the first 5 pages and go back to page 1.
    page.locator(".zeb-nav-to-first").first.click()
    page.get_by_role("listitem").filter(has_text="1").first.click()
    # Now let's see the rows per page. By default, 10 rows are displayed on each page, but we can modify this:
    # Use the specific caret icon to expand a dropdown and select the number of rows per page you want:
    page.locator(".d-flex > esp-multiselect-dropdown > .multiselect-dropdown > div > .w-100 > .d-flex.align-items-center > .dropdown-caret").first.click() # This specific caret expands the dropdown
    page.locator("div").filter(has_text=re.compile(r"^View 10 row\(s\)$")).first.click() # Select 10 rows, Wait time is needed here.
    page.locator(".d-flex > esp-multiselect-dropdown > .multiselect-dropdown > div > .w-100 > .d-flex.align-items-center > .dropdown-caret").first.click()
    page.locator("div").filter(has_text=re.compile(r"^View 20 row\(s\)$")).first.click() # Repeating for 20 rows per page
    page.locator(".d-flex > esp-multiselect-dropdown > .multiselect-dropdown > div > .w-100 > .d-flex.align-items-center > .dropdown-caret").first.click()
    page.locator("div").filter(has_text=re.compile(r"^View 50 row\(s\)$")).first.click() # Repeating for 50 rows
    # IMPORTANT, always ensure to select 10 rows per page after exploring the options:
    page.locator(".d-flex > esp-multiselect-dropdown > .multiselect-dropdown > div > .w-100 > .d-flex.align-items-center > .dropdown-caret").first.click()
    page.locator("div").filter(has_text=re.compile(r"^View 10 row\(s\)$")).first.click()
    # **End of Subsection**


    # **SUBSECTION 5: Product Markers:**
    # The grid shows Product data, and lets you mark specific products as Not Started, In Progress or Completed:
    page.locator("div").filter(has_text=re.compile(r"^013-SNACK BARS$")).first.click() # First Locate a specific row on the Grid
    page.locator(".ag-cell-value.ag-cell-focus > .ag-cell-wrapper > .ag-group-value > aeap-group-cell-renderer > .cellLabel > #statusDropdownId > esp-multiselect-dropdown > .multiselect-dropdown > div > .w-100 > .d-flex.align-items-center > .dropdown-caret").click() # This caret expands the menu to choose a marker
    page.locator("div").filter(has_text=re.compile(r"^Not started$")).first.click() # Once the menu is expanded, select "Not started". # Wait time needed
    # Repeat for "In Progress and Completed"
    page.locator(".ag-cell-value.ag-cell-focus > .ag-cell-wrapper > .ag-group-value > aeap-group-cell-renderer > .cellLabel > #statusDropdownId > esp-multiselect-dropdown > .multiselect-dropdown > div > .w-100 > .d-flex.align-items-center > .dropdown-caret").click()
    page.locator("div").filter(has_text=re.compile(r"^In progress$")).first.click() # Wait time needed.
    page.locator(".ag-cell-value.ag-cell-focus > .ag-cell-wrapper > .ag-group-value > aeap-group-cell-renderer > .cellLabel > #statusDropdownId > esp-multiselect-dropdown > .multiselect-dropdown > div > .w-100 > .d-flex.align-items-center > .dropdown-caret").click()
    page.locator("div").filter(has_text=re.compile(r"^Completed$")).first.click() # Wait time needed.
    # IMPORTANT: The default is Not Started, so always return to the default after exploring
    page.locator(".ag-cell-value.ag-cell-focus > .ag-cell-wrapper > .ag-group-value > aeap-group-cell-renderer > .cellLabel > #statusDropdownId > esp-multiselect-dropdown > .multiselect-dropdown > div > .w-100 > .d-flex.align-items-center > .dropdown-caret").click()
    page.locator("div").filter(has_text=re.compile(r"^Not started$")).first.click() # Wait time needed.
    # **End of Subsection**

    # **SUBSECTION 6: Exports and Preferences:**
    # This section of the grid is used after exploring the grid, when we want to save our preferences or export grid data:
    # Preferences section:
    page.locator("esp-grid-icons-component").filter(has_text="Preference").locator("#preference-iconId").click() # This button expands the Preferences Menu with 2 options: Save preferences or Reset Preferences
    page.locator("div").filter(has_text=re.compile(r"^Save Preference$")).first.click() # Save Preferences. HEAVY wait time here.
    page.locator("esp-grid-icons-component").filter(has_text="Preference").locator("#preference-iconId").click()
    page.locator("div").filter(has_text=re.compile(r"^Reset Preference$")).first.click() # Rest Preference. HEAVY wait time.

    # Export section: HEAVY Wait time here.
    with page.expect_download() as download_info:
        page.locator(".icon-color-toolbar-active.zeb-download-underline").first.click()
    download = download_info.value
    # **End of Subsection**

    #CRITICAL STEP: Always select one row from the Grid:
    page.get_by_role("row", name=" 002-SPIRITS").get_by_role("radio").check() # EXTRA HEAVY Wait time. (2 min)
    #-------In Order to Load the Locations Section we need to select a product from the Alerts Grid. This step is crucial and cannot be skipped------------------------
    page.get_by_role("row", name=" 002-SPIRITS").get_by_role("radio").check()# Selecting the product "008-LIGHTERS" from the alerts grid to load the locations section. This is necessary as locations data is loaded based on the selected product in the alerts grid.
    #-----------Click the chevron icon to expand the Location Section since by default it will be collapsed. This step is crucial.----------------
    page.locator(".pointer.chevron.zeb-chevron-right.m-r-12.collapsed").click()
    #-----------Now let's interact with the filters available in the Location section----------------
    page.get_by_role("button", name="columns").nth(1).click()# Click on the columns icon to view the list of columns available in the Locations grid
    #------------------Locate the text box that lets you search for columns and use it to search for "Store Count" column----------------
    page.get_by_role("textbox", name="Filter Columns Input").click()
    page.get_by_role("textbox", name="Filter Columns Input").fill("Store Count")
    page.get_by_role("textbox", name="Filter Columns Input").press("Enter")
    #------------------After hitting "Enter", the "Store Count" column should be the only option in the list of columns. Select the Store Count option from here and then clear the Search box----------------
    page.get_by_role("checkbox", name="Press SPACE to toggle").check() # Selecting the Store Count column from the columns dropdown to add it to the Locations grid
    #------------------Clearing the search box to view all columns again in the columns dropdown----------------
    page.get_by_role("textbox", name="Filter Columns Input").press("ControlOrMeta+a")
    page.get_by_role("textbox", name="Filter Columns Input").fill("")
    #----------------Deselecting the desired columns from the Columns dropdown to display in the Locations grid. Here we are selecting Store Count, Product Count and 13W-Fcst columns to be displayed in the grid----------------
    page.get_by_role("treeitem", name="Prev 13W Sell-Thru (TY) Column").get_by_label("Press SPACE to toggle").uncheck()
    page.get_by_role("treeitem", name="13W-Fcst Column").get_by_label("Press SPACE to toggle").uncheck()
    page.get_by_role("treeitem", name="Product Count Column").get_by_label("Press SPACE to toggle").uncheck()
    page.get_by_role("treeitem", name="Store Count Column").click()
    page.get_by_role("checkbox", name="Toggle All Columns Visibility").check() # Finally Selecting all columns using the "Toggle All Columns" option to display all columns in the Locations grid. Always Ensure that atleast one column is selected to avoid having an empty grid which can cause issues with test execution.
    page.get_by_role("button", name="columns").nth(1).click() # Click the columns button again to collapse the column section.
    #-----------------Click the Main Grid Header-------------------------
    page.locator("div").filter(has_text=re.compile(r"^Location$")).first.click()
    #------------------By Default, all Entries in the Location grid are selected. Let's deselect all entries using the header checkbox and then select a few specific locations----------------
    page.get_by_role("columnheader", name="Location").get_by_role("checkbox").uncheck() # Deselecting all locations using the header checkbox
    #------------------Selecting a specific location from the Grid----------------------
    page.get_by_role("gridcell", name="00023-5001 MONTGOMERY BLVD NE").get_by_role("checkbox").check()
    #-----------------Locate the Location Filter to Search for a specific grid row based on its Location-------------------------
    page.locator("#ag-header-cell-menu-button > .filter-icon").click() # Click on the filter icon in the Location column header to open the filter options
    # -----------------Expand the Dropdown to view the different filter options available------------------------
    page.locator(".ag-filter-select > esp-multiselect-dropdown > .multiselect-dropdown > div > .w-100").click()
    #-----------------From the list of filter options, select "Contains" and use it to search for locations that contain "NEW YORK" in their name------------------------
    page.get_by_text("Contains").first.click()
    page.get_by_role("textbox", name="Filter Value").click()# Locate the Search box
    page.get_by_role("textbox", name="Filter Value").fill("New York")# Type "New York"
    page.get_by_label("Column Menu").get_by_role("button", name="Apply").click()# Locate the Apply button to apply the filter and view the results
    page.get_by_role("gridcell", name="-755 BROADWAY-BROOKLYN-New York").get_by_role("checkbox").check() # We found a location with "New York" in its name. Let's select it using the checkbox in the grid.
    #-----------------Now Trying with "Does Not Contain"---------------------------
    page.locator("div").filter(has_text=re.compile(r"^Does Not Contain$")).nth(1).click()
    page.get_by_role("textbox", name="Filter Value").click()
    page.get_by_role("textbox", name="Filter Value").fill("New York")
    page.get_by_label("Column Menu").get_by_role("button", name="Apply").click()
    page.get_by_role("gridcell", name="00023-5001 MONTGOMERY BLVD NE").get_by_role("checkbox").check() # Found an Entry that does not contain New York

    #-----------------Saving our preference of Columns in the Locations grid using the "Save Preference" option in the grid icons------------------------
    page.locator(".position-relative > .legend-font > .multiselect-dropdown > .pointer").click()
    page.get_by_text("Save Preference").click()
    #-----------------Resetting the preference of Columns in the Locations grid using the "Reset Preference" option in the grid icons------------------------
    page.locator(".position-relative > .legend-font > .multiselect-dropdown > .pointer").click()
    page.get_by_text("Reset Preference").click()
    #---------Pagination Section of the Locations Grid--------------------
    #----------Navigate to the Second page of the Grid--------------------
    page.locator("a").filter(has_text="2").nth(1).click()
    #----------Navigate back to the First page of the Grid-----------------
    page.locator("a").filter(has_text=re.compile(r"^1$")).click()
    #-----------Click this button the Fetch the Next grid page--------------------
    page.locator("li:nth-child(5) > .zeb-chevron-right").click()
    #------------Click this button to fetch the previous page--------------------
    page.locator("div:nth-child(3) > esp-pagination-v2 > .d-flex.w-100 > .pagination-pager > .pagination-previous > .zeb-chevron-left").click()
    #-----------Click this button to view the last set of Grid pages
    page.locator("li:nth-child(6) > .zeb-nav-to-last").click()
    #-----------Click this button to view the First set of Grid Pages
    page.locator("div:nth-child(3) > esp-pagination-v2 > .d-flex.w-100 > .pagination-pager > .pagination-first > .zeb-nav-to-first").click()
    #---------------Now Selecting the number of Rows we want to view on each Grid page
    page.get_by_text("Rows per page").nth(1).click()
    page.locator("div:nth-child(3) > esp-pagination-v2 > .d-flex.w-100 > span:nth-child(3) > esp-multiselect-dropdown > .multiselect-dropdown > div > .w-100").click()# Expand a Dropdown menu showing us how many rows we can select
    page.locator("span").filter(has_text=re.compile(r"^View 10 row\(s\)$")).click() # Selecting 10 rows per page
    #----------------Now Exporting the Grid as an Excel Sheet--------------------
    with page.expect_download() as download_info:
        page.locator("div:nth-child(3) > div > .componentParentWrapper > esp-grid-container > esp-card-component > .card-container > .title > .grid-icons-container > esp-grid-icons-component > .display-grid-icons > div > #export-iconId > .icon-color-toolbar-active").click()
    download = download_info.value
    #-------------Reset All our Filters and Checks, this is mandatory.
    page.locator("#AlertsTab").get_by_role("button", name="Reset").click()
    page.locator(".position-relative > .legend-font > .multiselect-dropdown > .pointer").click()
    page.get_by_text("Reset Preference").click()
    #------------Click the "Apply" button. The MOST CRUCIAL STEP, because other sections of the page cannot load unless you click this button. Note that the reset button clears everything. So Select atleast one Checkbox before clicking Apply.
    page.locator(".position-relative > .legend-font > .multiselect-dropdown > .pointer").click() # Open this menu to do a reset first.
    page.get_by_text("Reset Preference").click() # Reset
    page.get_by_role("row", name="Location ").get_by_role("checkbox").check() # Select this checkbox before clicking apply 
    page.get_by_role("button", name="Apply", exact=True).click() # Click "Apply"
    #------------Precursor Steps. THESE ARE VERY IMPORTANT. Elements will not load without them------------
    page.get_by_role("row", name=" 002-SPIRITS").get_by_role("radio").check() # First Select this product from the Alerts Summary Grid. This action is incredibly HEAVY(2 min wait time needed.)
    page.get_by_role("row", name=" 006-GROCERIES").get_by_role("radio").check() # Back up Selection in case "002-SPIRITS" is not working (This also needs 2 min of wait time)


    #----------------------Complex Filter Section Needed to make the graph----------------------
    page.get_by_text("Filter columns (0) TopBottom").nth(1).click()#-------------Main Header of the Filter Section--------------------

    #--------------First Filter: Time ----------------------------------
    page.get_by_text("Time").click()# Locate Filter Heading
    page.locator("#time-filterId > .wr-20 > esp-multiselect-dropdown > .multiselect-dropdown > div > .w-100").click()# Click this top expand the Dropdown menu for selecting different time ranges
    page.locator("div").filter(has_text=re.compile(r"^Latest 4 Next 4$")).nth(1).click()# Option to Select a specific time range from the Dropdown Time menu
    page.locator("#time-filterId > .wr-20 > esp-multiselect-dropdown > .multiselect-dropdown > div > .w-100").click()# Reopen the Dropdown menu to choose another time range
    page.locator("div").filter(has_text=re.compile(r"^Latest 4 Next 13$")).nth(1).click()# Choose another time range
    page.locator("#time-filterId > .wr-20 > esp-multiselect-dropdown > .multiselect-dropdown > div > .w-100 > .d-flex.align-items-center > .dropdown-caret").click()# Reopen the Dropdown menu to choose another time range
    page.get_by_text("Latest 13 Next").click()# Choose another time range
    page.locator("#time-filterId > .wr-20 > esp-multiselect-dropdown > .multiselect-dropdown > div > .w-100").click()# Reopen the Dropdown menu to choose another time range
    page.locator("div").filter(has_text=re.compile(r"^Latest 52 Next 52$")).nth(1).click()# Choose another time range

    #------------------Second Filter: Event-----------------------------
    page.get_by_text("Event", exact=True).click()#Locate Filter Header
    page.locator("#event-filterId > .wr-20 > esp-multiselect-dropdown > .multiselect-dropdown > div > .w-100").click()# Click this top expand the Dropdown menu for selecting different Events
    page.locator(".d-flex.dropdown-option").first.click()# Selecting the First option in the Dropdown menu
    page.locator(".d-flex.dropdown-option.align-items-center.p-v-5.p-l-32 > .d-flex").first.click()# Reopening the Dropdown menu
    page.locator(".overflow-auto > div:nth-child(2) > .d-flex").click()#Clicking the Second option in the menu
    page.locator(".overflow-auto > div:nth-child(3) > .d-flex").click()# Clicking the third option
    page.locator("#event-filterId > .wr-20 > esp-multiselect-dropdown > .multiselect-dropdown > div > .w-100").click()# Closing the dropdown menu
    page.locator("#event-filterId > .wr-20 > esp-multiselect-dropdown > .multiselect-dropdown > div > .w-100").click()# Reopening the Dropdown meny
    page.get_by_role("textbox", name="Search").click()# Locate the Searchbox to search for a particular event
    page.get_by_role("textbox", name="Search").fill("ROT")# Type "ROT" in the Search box, then only the "ROT" event will be available in the Dropdown menu
    page.get_by_text("ROT - ROTO AD - CORPORATE").click()# Select the "ROT" option from the Dropdown menu
    page.locator(".icon.d-flex.pointer.zeb-close").click()# Click this to close the Dropdown menu after using the Search bar
    page.locator("#event-filterId > .wr-20 > esp-multiselect-dropdown > .multiselect-dropdown > div > .w-100").click()
    page.locator(".d-flex.flex-column.justify-content-center").first.click()
    page.locator(".d-flex.flex-column.justify-content-center").first.click()

    #------------------Third Filter: Ad RTl-----------------
    page.get_by_text("Ad Rtl").click()# Locate Ad Rtl Header
    page.locator(".not-allowed > .w-100").first.click()# There are no options in this filter.

    #-----------------Fourth Filter: Ad Location-------------------
    page.get_by_text("Ad Location", exact=True).click()#Locate the Ad Location Header
    page.locator("#ad-location-filterId > .wr-20 > esp-multiselect-dropdown > .multiselect-dropdown > div > .w-100").click()# Expand the Dropdown menu for Ad Location
    page.locator(".d-flex.flex-column.justify-content-center").first.click()# Select the first option from the Dropdown menu
    # Reopen the Dropdown Menu, Locate the Search box, Enter "B" in the Search box and Select an option from the Dropdown menu, Then close the Menu
    page.locator("#ad-location-filterId > .wr-20 > esp-multiselect-dropdown > .multiselect-dropdown > div > .w-100 > .d-flex.align-items-center > .dropdown-caret").click()
    page.get_by_role("textbox", name="Search", exact=True).click()
    page.get_by_role("textbox", name="Search", exact=True).fill("B")
    page.locator(".d-flex.dropdown-option.align-items-center.p-v-5.p-l-32").click()
    page.locator(".icon.d-flex.pointer.zeb-close").click()# Close after making a selection from the Dropdown menu

    #----------Fifth Filter: Segment---------------------
    page.get_by_text("Segment", exact=True).click()# Locate Segment Filter Header
    page.get_by_text("Segment", exact=True).click()
    page.locator("#segment-filterId > .wr-20 > esp-multiselect-dropdown > .multiselect-dropdown > div > .w-100").click()# Open the Dropdown menu for Segment Filter
    page.locator(".d-flex.flex-column.justify-content-center").first.click()# Select the first option
    # Select some more options
    page.locator(".d-flex.dropdown-option.align-items-center.p-v-5.p-l-32 > .d-flex").first.click()
    page.locator(".overflow-auto > div:nth-child(2) > .d-flex").click()
    page.locator(".overflow-auto > div:nth-child(3) > .d-flex").click()
    page.locator(".overflow-auto > div:nth-child(4) > .d-flex").click()
    # Use the Search bar to find a particular Option from the Dropdown. Type "A1" in the Search bar, Select the First option from the Dropdown and exit the Segments Dropdown Menu:
    page.locator("#segment-filterId > .wr-20 > esp-multiselect-dropdown > .multiselect-dropdown > div > .w-100 > .d-flex.align-items-center > .dropdown-caret").click()
    page.get_by_role("textbox", name="Search", exact=True).click()
    page.get_by_role("textbox", name="Search", exact=True).fill("A1")
    page.locator(".d-flex.dropdown-option.align-items-center.p-v-5.p-l-32 > .d-flex").click()
    page.locator(".icon.d-flex.pointer.zeb-close").click()# Close after Section


    #------------------Sixth Filter: Vendor---------------------
    page.get_by_text("Vendor", exact=True).click()# Locate Vendor Filter Header
    page.locator("#vendor-filterId > .wr-20 > esp-multiselect-dropdown > .multiselect-dropdown > div > .w-100").click() # Expand the Dropdown menu for Vendor Filter
    page.locator(".d-flex.flex-column.justify-content-center").first.click() # Click the first option from the Dropdown Menu
    # Selecting some more options from the Menu
    page.locator(".d-flex.dropdown-option.align-items-center.p-v-5.p-l-32 > .d-flex").first.click() 
    page.locator(".overflow-auto > div:nth-child(2) > .d-flex").click()
    page.locator(".overflow-auto > div:nth-child(3) > .d-flex").click()
    page.locator(".overflow-auto > div:nth-child(4) > .d-flex").click()
    page.locator(".overflow-auto > div:nth-child(5) > .d-flex").click()
    # Locate The Searchbox, Type "BIC CORP". Then Select an option from the Menu, and close the Menu:
    page.get_by_role("textbox", name="Search", exact=True).click()# Locate Search box
    page.get_by_role("textbox", name="Search", exact=True).fill("BIC CORP")# Type BIC CORP
    page.locator(".d-flex.dropdown-option.align-items-center.p-v-5.p-l-32 > .d-flex").click()# Click an option from Menu
    page.locator(".icon.d-flex.pointer.zeb-close").click()# Collapse the Menu

    #----------Seventh Filter: Season--------------
    page.get_by_text("Season", exact=True).click() # Locate the Season Filter Header
    page.locator("#season-filterId > .wr-20 > esp-multiselect-dropdown > .multiselect-dropdown > div > .w-100").click()# Expand the Dropdown Menu for Season Filter
    page.locator(".d-flex.flex-column.justify-content-center").first.click()# Select the First option
    # Selecting other options
    page.locator(".d-flex.dropdown-option.align-items-center.p-v-5.p-l-32 > .d-flex").click()
    # Use the Search box to find a particular option from the Menu, Select it, and collapse the Menu
    page.get_by_role("textbox", name="Search", exact=True).click()
    page.get_by_role("textbox", name="Search", exact=True).fill("BASIC")
    page.locator(".d-flex.dropdown-option.align-items-center.p-v-5.p-l-32").click()
    page.locator(".icon.d-flex.pointer.zeb-close").click()# Collapse after Selecting an option

    #----------------Eighth Filter: Season Category-----------------
    page.get_by_text("Season Category").click() # Locate the Season Category Header
    page.get_by_text("None").nth(2).click() # No options Here.


    #---------------Final Section After using all Filters: Apply them-------------------------
    page.locator("button").filter(has_text=re.compile(r"^Apply$")).click() # Most Crucial Action. Always apply at the end.


    #----------------------Weekly Trend Graph Section based on the complex filters----------------------
    page.get_by_text("Weekly Trend").click() # Locate the Main Header
    # Expand the Main Drop down menu to display the measures you want to be shown on the graph
    page.locator(".ellipses > esp-multiselect-dropdown > .multiselect-dropdown > div > .w-100 > .d-flex.align-items-center > .dropdown-caret").click()# Expand the Menu
    # Select Multiple options from the Dropdown Menu Here
    page.locator(".d-flex.flex-column.justify-content-center").first.click()
    page.locator(".d-flex.flex-column.justify-content-center.font-size-10.align-items-center.checkbox-v2.m-r-10.deselected").first.click()
    page.locator(".d-flex.flex-column.justify-content-center.font-size-10.align-items-center.checkbox-v2.m-r-10.deselected").first.click()
    page.locator(".d-flex.flex-column.justify-content-center.font-size-10.align-items-center.checkbox-v2.m-r-10.deselected").first.click()
    page.locator(".d-flex.flex-column.justify-content-center.font-size-10.align-items-center.checkbox-v2.m-r-10.deselected").first.click()
    page.locator(".overflow-auto > div:nth-child(6)").click()
    page.locator("div:nth-child(7) > .d-flex").click()
    page.locator("div:nth-child(8) > .d-flex").click()
    page.locator(".overflow-auto > div:nth-child(7)").click()
    page.locator("div:nth-child(8) > .d-flex").click()
    page.locator(".overflow-auto > div:nth-child(9)").click()
    page.locator(".overflow-auto > div:nth-child(10)").click()
    page.locator(".overflow-auto > div:nth-child(11)").click()
    page.locator("div:nth-child(12) > .d-flex").click()
    page.get_by_text("Weekly Summary").click() # Main Header for the Weekly Summary grid
    # Locate the Dropdown Menu, Expand and Select the measures you want to see:
    page.locator(".wr-20.font-weight-normal > esp-multiselect-dropdown > .multiselect-dropdown > div > .w-100").click()
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
    # I am Selecting All Possible Measures using this action:
    page.locator(".d-flex.flex-column.justify-content-center").first.click()
    # Collapse the Menu After Selection:
    page.locator(".wr-20.font-weight-normal > esp-multiselect-dropdown > .multiselect-dropdown > div > .w-100 > .d-flex.align-items-center > .dropdown-caret").click()
    # Columns Section to Select Particular Dates:
    page.get_by_role("button", name="columns").nth(2).click() # Click this button and expand the Dropdown menu
    # By Default, all Dates will be Selected, so we will unselect all of them and select a few specific dates:
    page.get_by_role("checkbox", name="Toggle All Columns Visibility").uncheck() # Unselect all Dates First
    # Now Select a few options from the Dropdown Menu
    page.get_by_role("treeitem", name="/02/2025 Column").get_by_label("Press SPACE to toggle").check()
    page.get_by_role("treeitem", name="/09/2025 Column").get_by_label("Press SPACE to toggle").check()
    page.get_by_role("treeitem", name="/16/2025 Column").get_by_label("Press SPACE to toggle").check()
    page.get_by_role("treeitem", name="/23/2025 Column").get_by_label("Press SPACE to toggle").check()
    page.get_by_role("treeitem", name="/30/2025 Column").get_by_label("Press SPACE to toggle visibility (hidden)").check()
    page.get_by_role("treeitem", name="/07/2025 Column").get_by_label("Press SPACE to toggle visibility (hidden)").check()
    page.get_by_role("treeitem", name="/14/2025 Column").get_by_label("Press SPACE to toggle visibility (hidden)").check()
    # Use the Search box to Search for a specific date. This will reduce the options in the Menu to only that specific Date. Select it.
    page.get_by_role("textbox", name="Filter Columns Input").click()
    page.get_by_role("textbox", name="Filter Columns Input").fill("01/11/2026")
    page.get_by_role("checkbox", name="Press SPACE to toggle").check()
    # I am now Clearing the Searchbox, Selecting all Dates again and closing Columns section
    page.get_by_role("textbox", name="Filter Columns Input").press("ControlOrMeta+a")
    page.get_by_role("textbox", name="Filter Columns Input").fill("")
    page.get_by_role("checkbox", name="Toggle All Columns Visibility").check()
    page.get_by_role("button", name="columns").nth(2).click()# Click this to close
    # Preference Section, We can Save Preference or Reset Preference
    page.locator("div:nth-child(4) > #preference-iconId > .legend-font > .multiselect-dropdown > .pointer").click() # Click to expand the Preference Section
    page.get_by_text("Save Preference").click() # Saving Preference
    # Resetting Preference
    page.locator(".notification-circle").click()
    page.locator(".position-relative > .legend-font > .multiselect-dropdown > .pointer").click()
    page.get_by_text("Reset Preference").click()
    # Exporting the Grid as an Excel Sheet
    with page.expect_download() as download1_info:
        page.locator("div:nth-child(3) > #export-iconId > .icon-color-toolbar-active").click()
    download1 = download1_info.value
    #------Expanding Some Measures in the Grid by clicking on Chevron Icon. Note, only do this if you have Selected  page.get_by_role("checkbox", name="Toggle All Columns Visibility").check() From the Columns Section, otherwise they may fail
    page.locator("span").filter(has_text="Forecast Alerts - SSIS").first.click()
    page.locator(".ag-cell-value.ag-cell.ag-cell-not-inline-editing.ag-cell-normal-height.ag-cell-last-left-pinned.ag-column-first.ag-cell-override-normal.notosans-overwrite.no-border.ag-cell-focus > .ag-cell-wrapper > .ag-group-contracted > .zeb-chevron-right").click()
    page.locator(".ag-cell-wrapper.ag-cell-expandable > .ag-group-contracted > .zeb-chevron-right").first.click()
    page.locator("span").filter(has_text="Digital Sales").first.click()
    page.locator(".ag-cell-wrapper.ag-cell-expandable.ag-row-group.ag-row-group-indent-1 > .ag-group-contracted > .zeb-chevron-right").click()
    page.locator(".ag-cell-wrapper.ag-cell-expandable > .ag-group-contracted > .zeb-chevron-right").first.click()
    page.locator(".ag-row-no-focus.ag-row-not-inline-editing.ag-row.ag-row-level-0.ag-row-group > .ag-cell-value > .ag-cell-wrapper > .ag-group-contracted > .zeb-chevron-right").first.click()
    page.locator(".ag-row-no-focus.ag-row-not-inline-editing.ag-row.ag-row-level-0.ag-row-group.ag-row-group-contracted > .ag-cell-value > .ag-cell-wrapper > .ag-group-contracted > .zeb-chevron-right").click()
    #---------------------Interacting with the Global Filters and applying filters on Product, Location and User hierarchies----------------------
    page.locator("#filter-toggle-iconId").click()#-----------This is the main Global Filters Icon which opens the filter panel on the left side of the screen.
    #---------There are 3 main sections in the global filters - Product, Location and User------------
    #-----------------Product Hierarchy Filters-----------------
    page.locator("esp-simple-side-filter-panel-v1").get_by_text("Product").click()#Locate Product section in the global filters and click to expand
    #-----------Inside Product section we have  2 main filter categories - Hierarchy and Attribute. Let's expand the Hierarchy section first and apply some filters----------------
    page.locator("div").filter(has_text=re.compile(r"^Hierarchy$")).nth(2).click() # Locate and click Hierarchy
    #-----------In Hierarchy we have multiple levels of filters - Merchandise Division, OpStudy, Product Category, PLN.------------------------------------
    page.get_by_text("Merchandise Division").click()# Locate and click Merchandise Division filter
    page.locator("div").filter(has_text=re.compile(r"^Select All$")).click()
    page.locator("div").filter(has_text=re.compile(r"^00000-NO DIV NAME$")).click()
    page.get_by_role("button", name="Apply Filters").click()# Applying filters of Merchandise Division
    page.get_by_text("OpStudy").click()# Locate and click OpStudy filter
    page.locator("div").filter(has_text=re.compile(r"^Select All$")).click()
    page.locator("#SideFilterproducthierarchyId").get_by_text("-PPD DEBIT LOAD CARD").click()
    page.get_by_role("button", name="Apply Filters").click()# Applying filters of OpStudy
    page.get_by_text("Product Category").click()# Locate and click Product Category filter
    page.locator("div").filter(has_text=re.compile(r"^Select All$")).click()
    page.locator("div").filter(has_text=re.compile(r"^155-001-GC_TRN AMNT - NONRLD TRN$")).click()
    page.get_by_role("button", name="Apply Filters").click()# Applying filters of Product Category
    page.get_by_text("PLN", exact=True).click()# Locate and click PLN filter
    page.locator("div").filter(has_text=re.compile(r"^Select All$")).click()
    page.get_by_text("-VNLA VISA SHNY HX BX VGC $20-$500").click()
    page.get_by_role("button", name="Apply Filters").click()# Applying filters of PLN
    #-----------Now let's expand the Attribute section and apply some filters----------------
    page.locator("div").filter(has_text=re.compile(r"^Attribute$")).nth(2).click()# Locate and click Attribute section under Product hierarchy
    page.locator(".d-flex.p-l-32").first.click()# Click to expand the first attribute filter
    page.locator("div").filter(has_text=re.compile(r"^Select All$")).click()
    page.locator("div").filter(has_text=re.compile(r"^AMEX$")).click()
    page.get_by_role("button", name="Apply Filters").click()# Applying filters of the first attribute
    page.locator("div:nth-child(3) > esp-filter-sub-accordion-v1 > .sub-accordion-element > .d-flex").click()# Click to expand the second attribute filter
    page.locator("div").filter(has_text=re.compile(r"^Select All$")).click()
    page.locator("div").filter(has_text=re.compile(r"^N$")).click()
    page.locator("div").filter(has_text=re.compile(r"^Select All$")).click()
    page.get_by_role("button", name="Apply Filters").click()# Applying filters of the second attribute
    page.get_by_text("Import").click()# Click and Locate the Import section which is the third attribute filter
    page.locator("div").filter(has_text=re.compile(r"^Select All$")).click()
    page.get_by_role("button", name="Apply Filters").click()# Applying filters of the Import attribute
    page.locator(".aggrigate-panel").click()# Aggregate panel at the bottom
    page.locator(".custom-checkbox-wrapper.overflow-hidden.d-flex.justify-content-center.m-r-8.background-primary-color > .pointer").click()# Checkbox to include the aggregated values in the graphs and tables
    page.get_by_role("button", name="Reset").click()# Perform reset action to clear all the applied filters
    #-----------------Location Hierarchy Filters-----------------
    page.locator("esp-simple-side-filter-panel-v1").get_by_text("Location").click()# Locate Location section in the global filters and click to expand
    # ...Inside Location Section, We have 2 major filter categories under Location hierarchy - Hierarchy and Attribute. Let's expand the Hierarchy section first and apply some filters----------------
    page.locator("div").filter(has_text=re.compile(r"^Hierarchy$")).nth(2).click()# Locate and click Hierarchy under Location section
    #-----------Inside Hierarchy We have 3 main levels: Region, Area and Store. Let's expand Region and apply some filters----------------
    page.locator(".d-flex.p-l-32").first.click()# Locator for Region filter under Location hierarchy
    page.locator("div").filter(has_text=re.compile(r"^Select All$")).click()
    page.locator("div").filter(has_text=re.compile(r"^00005-Mountain West$")).click()
    page.get_by_role("button", name="Apply Filters").click()# Applying filters of Region
    page.locator("div:nth-child(3) > esp-filter-sub-accordion-v1 > .sub-accordion-element > .d-flex").click()# Locator for Area filter under Location hierarchy
    page.locator("div").filter(has_text=re.compile(r"^Select All$")).click()
    page.locator("div").filter(has_text=re.compile(r"^006-Seattle/Oregon$")).click()
    page.get_by_role("button", name="Apply Filters").click()# Applying filters of Area
    page.get_by_text("Store", exact=True).click()# Locator for Store filter under Location hierarchy
    page.locator("div").filter(has_text=re.compile(r"^Select All$")).click()
    page.locator("div").filter(has_text=re.compile(r"^00809-8911 N 7TH ST-PHOENIX-Arizona$")).click()
    page.get_by_role("button", name="Apply Filters").click()# Applying filters of Store
    #-----------Now let's expand the Attribute section and apply some filters----------------
    page.locator("div").filter(has_text=re.compile(r"^Attribute$")).nth(2).click()# Locate and click Attribute section under Location hierarchy
    # Under Attribute section we have 4 filters - DC, MDG and State and Exclude Billing Stores. Let's apply some filters under each of these attributes----------------
    page.get_by_text("DC").click()# Locate and click DC filter under Attribute section of Location hierarchy
    page.locator("div").filter(has_text=re.compile(r"^Select All$")).click()
    page.locator("div").filter(has_text=re.compile(r"^88006-WOODLAND$")).click()
    page.get_by_role("button", name="Apply Filters").click()# Applying filters of DC attribute
    page.get_by_text("MDG").click()# Locate and click MDG filter under Attribute section of Location hierarchy
    page.locator("div").filter(has_text=re.compile(r"^Select All$")).click()
    page.locator("div").filter(has_text=re.compile(r"^290-IDAHO, BOISE$")).click()
    page.get_by_role("button", name="Apply Filters").click()# Applying filters of MDG attribute
    page.get_by_text("State").click()# Locate and click State filter under Attribute section of Location hierarchy
    page.locator("div").filter(has_text=re.compile(r"^Select All$")).click()
    page.locator("div").filter(has_text=re.compile(r"^Montana$")).click()
    page.get_by_role("button", name="Apply Filters").click()# Applying filters of State attribute
    page.get_by_text("Exclude Billing Stores").click()# Locate and click Exclude Billing Stores filter under Attribute section of Location hierarchy
    page.locator("div").filter(has_text=re.compile(r"^Select All$")).click()
    page.get_by_role("button", name="Apply Filters").click()# Applying filters of Exclude Billing Stores attribute
    page.get_by_role("button", name="Reset").click()# Perform reset action to clear all the applied filters under Location hierarchy
    #-----------------User Hierarchy Filters-----------------
    page.locator("esp-simple-side-filter-panel-v1").get_by_text("User").click()# Locate User section in the global filters and click to expand
    # ... In User Section we only have Hierarchy category, let's expand and apply some filters----------------
    page.locator("div").filter(has_text=re.compile(r"^Hierarchy$")).nth(3).click()# Locate and click Hierarchy under User section
    page.locator("#SideFilteruserhierarchyId").get_by_text("User").click()
    page.locator("div").filter(has_text=re.compile(r"^Select All$")).click()
    page.locator("div").filter(has_text=re.compile(r"^701$")).click()
    page.locator("div").filter(has_text=re.compile(r"^701$")).click()
    page.locator(".filter-values.d-flex.align-items-center.p-l-32.p-r-24 > .custom-checkbox-wrapper > .pointer").first.click()
    page.get_by_role("button", name="Apply Filters").click()# Applying filters of User hierarchy
    page.get_by_role("button", name="Reset").click()# Perform reset action to clear all the applied filters under User hierarchy
    page.close()# Closing the filter panel after interactions. End.
    # ---------------------
    # ---------------------
    context.close()
    browser.close()


with sync_playwright() as playwright:
    run(playwright)
