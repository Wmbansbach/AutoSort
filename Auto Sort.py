# Auto Sort Utility
#--------------------------------------------------
# To Do
# 1. Add logging for events, dates, and times
# 2. 
#--------------------------------------------------
# Change Log:
# * 6/22/2020 - Finished initial concept design
# ** 6/22/2020 - Added Logging using the logging module
#--------------------------------------------------
# Known Issues:
# 1. The Query method catches any "extension" longer than 4 chars
#       * This fix is not tested yet
# 2. Files that do not match can be placed in a Needs Checking file? (Query Method)
# 3. Application will crash if a pickle file is not found and sorted directories already exist

_author_ = "WmBansbach"

import os, time, pickle, shutil, logging
from os import path


class AutoSort:
    
    def __init__(self):
        # Load initial parameters
        self.target_path = "C:\\Users\\William\\Downloads"
        self.ext_repo = "C:\\Users\\William\\_AutoSort\\extensions.as"
        self.extensions = []
        
        logging.basicConfig(filename = "C:\\Users\\William\\_AutoSort\\AS.log",
                                          format = '%(asctime)s - %(message)s',
                                          level = logging.INFO)
        # LOG
        logging.info('Application Initialized')
        
        # Load the extensions file
        if os.path.exists(self.ext_repo):
            with open(self.ext_repo, 'rb') as file:
                self.extensions = pickle.load(file)

        # Run initial directory check
        self.Query(os.listdir(self.target_path))
        
        # Begin monitoring the file directory
        self.Watch()
        
    def Watch(self):        # Directory Monitoring Function
        before = dict([(f, None) for f in os.listdir(self.target_path)])
        while 1:
            time.sleep(10)
            after = dict([(f, None) for f in os.listdir(self.target_path)])
            added = [f for f in after if not f in before]
            if added:
                # LOG
                logging.critical('New File(s) Found: %s', added)
                #print("Added: ", ", ".join (added))
                self.Query(added)
            before = after            

    def Query(self, nfiles):        # Sorting Function
        #print(nfiles)
        pfiles = dict
        for i in nfiles:
            trunc = path.splitext(i)[1]
            #print(trunc[1:])
            if trunc == "" or len(trunc) > 4:
                continue
            if trunc[1:] in self.extensions:
                self.Distribute(trunc[1:], i)
                continue
            self.extensions.append(trunc)
            #print("New Extension: " + trunc)
            os.mkdir(path.join(self.target_path, trunc[1:]))
            # LOG
            logging.critical('New Extension Added: %s', trunc)
    
    def Distribute(self, ext, file):      # Distribution Function
        root = path.join(self.target_path, ext)
        shutil.move(path.join(self.target_path, file), path.join(root, file))
        self.Update()

    def Update(self):       # Update the extension repo with new ext
        with open(self.ext_repo, 'wb') as file:
            pickle.dump(self.extensions, file)

AS = AutoSort()



