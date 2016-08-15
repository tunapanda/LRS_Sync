# LRS_Sync
Small Python program that syncs xapi (tincan api) statements between two Learning Record Stores.

Requires [TinCanPython](https://github.com/RusticiSoftware/TinCanPython):

**pip install tincan**

LRS_Sync can sync statements between multiple LRSs. LRS_Sync.py will push statements from a local LRS to a remote LRS (while avoiding duplicates.)

For servers with limited internet access, LRS_Save.py can store all statements in a json file. That file can then be uploaded from another machinge using LRS_Upload.py.

Add LRS authentication information, filenames, etc. to LRS_config_template.py and rename to LRS_config.py to run the syncing programs.

Has only been tested with LearningLocker.
