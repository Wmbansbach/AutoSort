# Auto Sort Utility
--------------------------------------------------
# Synopsis: Sorts a targeted directory by file extension
--------------------------------------------------
# Documentation:
* Parameters
  > fresh       - False by default. Signifies whether or
                  not the target_path has been sorted before.</br>
  > target_path - Defaults to the Downloads folder in Windows.
                  Can be set to any directory to be sorted.
* Example
  > import AutoSort</br>
  > as = AutoSort(fresh = true, target_path = "c:\Users\Will\Documents\")

* Logging
  > App logs can be found at C:\Users\[USERNAME]\_AutoSort\AS.log

* Pickle Module
  > The pickle module is used to store a list of extensions.</br>
  > The pickle file can be found at C:\Users\[USERNAME]\_AutoSort\extensions.as   
--------------------------------------------------
# Change Log:
* 6/22/2020
  - Finished initial concept design.
  - Added Logging using the logging module.
  - Added switch for fresh directories.
  - Created a Populate method that builds new
    extensions list. Solves edge-case where there is no
    pickle file, but the tp as already been sorted.
  - Added dynamic pathing, as well as, argument for
    dynamic pathing upon object instantiation.
* 6/23/2020
  - Updated comments
* 10/17/2021
  - Added error handling
  - Updated comments
  - Made it work
  - Updated logging information and events
  - Added synopsis section

--------------------------------------------------
# Known Issues:
1. Will not handle extensions longer than four chars (.torrent, .vbox-extpack)
2.
--------------------------------------------------
