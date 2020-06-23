# Auto Sort Utility
#--------------------------------------------------
# Documentation:
# * Parameters
#   > fresh       - False by default. Signifies whether or
#                   not the target_path has been sorted before.
#   > target_path - Defaults to the Downloads folder in Windows.
#                   Can be set to any directory to be sorted.
# * Logging
#   > App logs can be found at C:\Users\[USERNAME]\_AutoSort\AS.log
# * Pickle Module
#   > The pickle module is used to store a list of extensions.
#     The pickle file can be found at C:\Users\[USERNAME]\_AutoSort\extensions.as   
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
#     selecting different paths upon object instantiation.
#   - 
#--------------------------------------------------
# Known Issues:
#
#--------------------------------------------------

_author_ = "WmBansbach"

import os, time, pickle, shutil, logging
from os import path


class AutoSort:
    
    def __init__(self, fresh = False, target_path = None):
        # Load initial parameters
        self.target_path = path.join(os.environ['HOME'], 'Downloads')
        if target_path != None:
            self.target_path = target_path
        self.ext_repo = path.join(os.environ['HOME'], '_AutoSort', 'extensions.as')
        self.extensions = []
        self.fresh = fresh
        
        logging.basicConfig(filename = path.join(os.environ['HOME'], '_AutoSort', 'AS.log'),
                            format = '%(asctime)s - %(levelname)s - %(message)s',
                            level = logging.INFO,
                            datefmt='%d-%b-%y %H:%M:%S')
        
        if os.path.exists(self.ext_repo):       # Load the extensions file
            with open(self.ext_repo, 'rb') as file:
                self.extensions = pickle.load(file)
        else:
            if not self.fresh: self.Populate()
            
        # A "fresh" directory signifies that it has not yet be sorted by AutoSort yet. 
        if self.fresh: self.Cleanup()
            
        # Update Log
        logging.info('Application Initialized')
        
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
                logging.critical('New File(s) Found: %s', added)
                self.Query(added)
            before = after            

    # Sorter utility which can be called independently of the automated watcher.
    def Cleanup(self):
        # Update Log
        logging.warning('Directory Cleanup Initiated')
        return self.Query(os.listdir(self.target_path))

    # Sorting Function
    def Query(self, nfiles):        
        pfiles = dict
        for i in nfiles:
            trunc = path.splitext(i)[1]
            if trunc == "" or len(trunc) > 4:
                continue
            if trunc[1:] in self.extensions:
                self.Distribute(trunc[1:], i)
                continue
            self.extensions.append(trunc)
            os.mkdir(path.join(self.target_path, trunc[1:]))
            # Update Log
            logging.critical('New Extension Added: %s', trunc)

    # Distribution Function
    def Distribute(self, ext, file):      
        root = path.join(self.target_path, ext)
        shutil.move(path.join(self.target_path, file), path.join(root, file))
        self.Update()

    # Update the extension repo with new ext
    def Update(self):       
        with open(self.ext_repo, 'wb') as file:
            pickle.dump(self.extensions, file)
    # Update new extensions list in some cases
    def Populate(self):
        for f in os.listdir(self.target_path):
            if len(f) <= 4:
                self.extensions.append(f)
        self.Update()
