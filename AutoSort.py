# Auto Sort Utility
#--------------------------------------------------
# Synopsis: AutoSort will sort and keep sorted a specified directory
#--------------------------------------------------
# Documentation:
# * Parameters
#   > fresh       - False by default. Signifies whether or
#                   not the target_path has been sorted before.
#   > target_path - Defaults to the Downloads folder in Windows.
#                   Can be set to any directory to be sorted.
# * Example
#   > import AutoSort
#   > as = AutoSort(fresh = true, target_path = "c:\Users\Will\Documents\")
#
# * Logging
#   > App logs can be found at C:\Users\[USERNAME]\_AutoSort\AS.log
# * Pickle Module
#   > The pickle module is used to store a list of extensions.
#   > The pickle file can be found at C:\Users\[USERNAME]\_AutoSort\extensions.as   
#
#--------------------------------------------------
# Change Log:
# * 6/22/2020
#   - Finished initial concept design.
#   - Added Logging using the logging module.
#   - Added switch for fresh directories.
#   - Created a Populate method that builds new
#     extensions list. Solves edge-case where there is no
#     pickle file, but the tp as already been sorted.
#   - Added dynamic pathing, as well as, argument for
#     dynamic pathing upon object instantiation.
# * 6/23/2020
#   - Updated comments
# * 10/17/2021
#   - Added error handling
#   - Updated comments
#   - Made it work
#   - Updated logging information and events
#   - Added synopsis section
#
#--------------------------------------------------
# Known Issues:
# 1. Will not handle extensions longer than four chars (.torrent, .vbox-extpack)
# 2.
#--------------------------------------------------
_author_ = "WmBansbach"

import os, time, pickle, shutil, logging
from os import path


class AutoSort:
    
    def __init__(self, fresh = False, target_path = None):
        
        # Load default target path: C:\Users\[Username]\Downloads
        # Define other attributes
        self.target_path = path.join(os.environ['HOME'], 'Downloads')
        self.extensions = []
        self.fresh = fresh
        
        # Check if target_path argument was passed on instantiation
        if target_path != None:
            self.target_path = target_path
            
        # Set name then check program file directory. Create it if needed
        self.util_repo = path.join(os.environ['HOME'], '_AutoSort')
        
        if not os.path.exists(self.util_repo):
            os.mkdir(path.join(os.environ['HOME'], '_AutoSort'))

        # Define extensions file path
        # Define attributes
        self.ext_repo = path.join(self.util_repo, 'extensions.as')
        
        # Setup Logging File
        logging.basicConfig(filename = path.join(os.environ['HOME'], '_AutoSort', 'AS.log'),
                            format = '%(asctime)s - %(levelname)s - %(message)s',
                            level = logging.INFO,
                            datefmt='%d-%b-%y %H:%M:%S')

        # Update Log
        logging.critical('Module Initialization Complete\n')
        
        # Load the extensions file. Runs the Populate function first in some cases
        if os.path.exists(self.ext_repo):       
            with open(self.ext_repo, 'rb') as file:
                self.extensions = pickle.load(file)
        else:
            # A "fresh" directory signifies that it has not yet be sorted by AutoSort
            if self.fresh:
                self.Cleanup()

        # Begin monitoring the file directory
        self.Watch()

    # Directory Monitoring Function
    # Modified from a script found on Tim Golden's Website.
    # http://timgolden.me.uk/python/win32_how_do_i/watch_directory_for_changes.html
    def Watch(self):        
        before = dict([(f, None) for f in os.listdir(self.target_path)])
        while 1:
            time.sleep(10)
            after = dict([(f, None) for f in os.listdir(self.target_path)])
            added = [f for f in after if not f in before]
            if added:
                # Update Log
                logging.info('\tNew File(s) Found: %s\n', added)
                self.Query(added)
            before = after            

    # Standalone sorting utility which can be called independently of the watcher.
    def Cleanup(self):
        # Update Log
        logging.critical('Initial Directory Cleanup Started\n')
        return self.Query(os.listdir(self.target_path))

    # Sorting Function
    def Query(self, nfiles):        
        for i in nfiles:
            ext = path.splitext(i)[1]
            # Passes folders and files with larger exts
            if ext == "" or len(ext[1:]) > 4:    
                continue
            # Folder already exists for file
            elif ext in self.extensions:
                self.Distribute(ext[1:], i)
                continue
            # New extension which needs to be added
            else:
                # Check if extension is an integer, ignore if yes
                try:
                    ext_int = int(ext[1:])
                except ValueError:
                    # Add extension to list, log the event, create the directory, and distribute the new file
                    self.extensions.append(ext)
                    logging.info('New Extension Added: %s\n', ext)
                    os.mkdir(path.join(self.target_path, ext[1:]))
                    self.Distribute(ext[1:], i)
                    
    # Distribution Function
    def Distribute(self, ext, file):      
        root = path.join(self.target_path, ext)
        shutil.move(path.join(self.target_path, file), path.join(root, file))
        logging.warning('File: \"' + file + '\" was distributed to folder \"' + ext + '\" \n')
        self.Update()

    # Update the extension repo with new ext
    def Update(self):       
        with open(self.ext_repo, 'wb') as file:
            pickle.dump(self.extensions, file)
        logging.info('Extensions file has been updated\n')
            
    # Populate a new extensions list. (For some cases)
    def Populate(self):
        for f in os.listdir(self.target_path):
            # Example: .exe
            ext = path.splitext(f)[1]
            if len(ext[1:]) <= 4 and ext not in self.extensions:
                # Ensure no extensions are numbers (weeds out picking up version numbers as extensions)
                try:
                    ext_int = int(ext[1:])
                except ValueError:
                    self.extensions.append(ext)
                
        logging.info('New Extensions File Created\n')
        self.Update()
