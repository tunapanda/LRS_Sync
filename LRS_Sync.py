import uuid, json, sys, time
from tincan import RemoteLRS
from socket import gethostbyname, gaierror
import requests
#Statement classclass Statement:

class Statement:
    def __init__(self,statement):

        self.statement = statement
        self.id = statement['id']
        if 'name' in statement['actor']:
            self.actor = statement['actor']['name']
        else:
            self.actor = 'Unknown User'
        self.verb = statement['verb']['id']
        self.object = statement['object']['definition']['name']['en-US']

#Collect LRS data from config file
def collect_local_lrs_credentials():
    try:
        from LRS_config import local_lrs_credentials as lc
    except ImportError:
        print ("Error: LRS_config.py does not exist or cannot be read")
        sys.exit()

    local_lrs = RemoteLRS(
        endpoint=lc["endpoint"],
        username=lc["username"],
        password=lc["password"],
    )

    return local_lrs, lc

def collect_remote_lrs_credentials():
    try:
        from LRS_config import remote_lrs_credentials as rc
    except ImportError:
        print ("Error: LRS_config.py does not exist or cannot be read")
        sys.exit()

    remote_lrs = RemoteLRS(
        endpoint=rc["endpoint"],
        username=rc["username"],
        password=rc["password"],
    )
    return remote_lrs, rc



#Collect all statements currently in remote LRS to avoid duplicates
def collect_remote_statements(remote_lrs, rc):
    print ("Checking statements in remote LRS...")
    if rc["LRS"] == "learninglocker":
        try:
            response = remote_lrs.query_statements({"format":"exact"})
        except gaierror:
            print ("Error connecting to remote LRS at %s. Please check your internet connection." %(rc[endpoint]))
            sys.exit()
        if not response.success:
            print ("\nCould not connect to remote LRS at %s.\nPlease check config file for correct details and try again...\nExiting..." %(rc["endpoint"]))
            sys.exit()

        remote_data = json.loads(response.data)
    elif rc["LRS"] == "wordpress":
        url  = rc["endpoint"] + "/statements/"
        un = rc["username"]
        pw = rc["password"]

        try:
            r = requests.get(url, auth = (un,pw))
            r.raise_for_status()
            remote_data =  r.json()
        except requests.exceptions.RequestException as e:
            print (e)
            sys.exit()
    remote_statement_ids = ()
    for statement in remote_data["statements"]:
        remote_statement_ids += (statement["id"],)
    return remote_statement_ids


def collect_local_statements(local_lrs,lc):
    print ("Connecting to local LRS...")
    if lc["LRS"] == "learninglocker":
        querySettings = {"format":"exact"}

        try:
            from LRS_config import date
        except ImportError:
            date = None
        if date is not None:
            querySettings["since"] = date + "T00:00:00.000000+00:00"

        response = local_lrs.query_statements(querySettings)
        if not response.success:
            print ("\nCould not connect to local LRS at %s.\nPlease check config file for correct details and try again...\nExiting..." %(lc["endpoint"]))
            sys.exit()
        return json.loads(response.data)
    elif lc["LRS"] == "wordpress":
        url  = lc["endpoint"] + "/statements/"
        un = lc["username"]
        pw = lc["password"]

        try:
            r = requests.get(url, auth = (un,pw))
            r.raise_for_status()
            if len(r.json()["statements"]) <= 1:
                print ("Could not find any statements in local LRS at %s.\nPlease check config file for correct details and try again...\nExiting..." %(lc["endpoint"]))
                sys.exit()
            return r.json()
        except requests.exceptions.RequestException as e:
            print (e)
            sys.exit()
    else:
        print (lc["LRS"] + " is not a valid LRS type.")
        sys.exit()

    #return response.data


def store_statements(local_statements, remote_statement_ids, remote_lrs):
    saved_statements = 0
    skipped_statements = 0
    for statement in local_statements["statements"]:
        s = Statement(statement)
        print (s.actor, s.verb, s.object)
        if statement["id"] in remote_statement_ids:
            print ("skip")
            skipped_statements += 1
        else:
            response = remote_lrs.save_statement(statement)
            if not response:
                raise ValueError("statements failed to save")
            print ("...saved")
            saved_statements += 1
        time.sleep(.2)
    print ("\nDone! %i statements saved and %i statements skipped. \n" %(saved_statements, skipped_statements))

if __name__ == "__main__":
    local_lrs, lc = collect_local_lrs_credentials()
    remote_lrs, rc = collect_remote_lrs_credentials()
    remote_statement_ids = collect_remote_statements(remote_lrs, rc)
    local_statements = collect_local_statements(local_lrs, lc)
    store_statements(local_statements, remote_statement_ids, remote_lrs)
