"""
LRS_Sync syncs xapi statments between two LRSs. Currently the functionality only exists to push
statements from one LRS (Local LRS) to another (Remote LRS)

Enter the correct information for the LRS below and run LRS_Sync.py to push statements
"""

# Source of statements
local_lrs_credentials = {
"endpoint":"<enterLRSendpoint>"
"username":"<enterLRSusername>"
"password":"<enterLRSpassword>"
}

#Destination of statements
remote_lrs_credentials = {
"endpoint":"<enterLRSendpoint>"
"username":"<enterLRSusername>"
"password":"<enterLRSpassword>"
}

#Optional - only collect statements from local LRS if created in local LRS after date (YYYY-MM-DD):
#date = "2015-01-01"
