import uuid, json, sys, time
from tincan import RemoteLRS
from socket import gethostbyname, gaierror

#Statement classclass Statement:

class Statement:
    def __init__(self,statement):

        self.statement = statement
        self.id = statement['id']
        self.actor = statement['actor']['name']
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
def collect_remote_statements(remote_lrs):
    try:
        response = remote_lrs.query_statements({"format":"exact"})
    except gaierror:
        print "Error connecting to remote LRS at %s. Please check your internet connection." %(rc[endpoint])
        sys.exit()
    if not response.success:
        print ("\nCould not connect to remote LRS at %s.\nPlease check config file for correct details and try again...\nExiting..." %(rc["endpoint"]))
        sys.exit()

    remote_data = json.loads(response.data)
    remote_statement_ids = ()
    for statement in remote_data["statements"]:
        remote_statement_ids += (statement["id"],)
    return remote_statement_ids


def collect_local_statements(local_lrs):
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
    #return response.data


def store_statements(local_statements, remote_statement_ids, remote_lrs):
    saved_staments = 0
    for statement in local_statements["statements"]:
        s = Statement(statement)
        print s.actor, s.verb, s.object
        if statement["id"] in remote_statement_ids:
            print "skip"
        else:
            response = remote_lrs.save_statement(statement)
            if not response:
                raise ValueError("statements failed to save")
            print "...saved"
            saved_staments += 1
        time.sleep(.2)
    print "\nDone! %i statements saved.\n" %(saved_staments)

if __name__ == "__main__":
    local_lrs, remote_lrs, lc, rc = collect_lrs_credentials()
    remote_statement_ids = collect_remote_statements(remote_lrs)
    local_statements = collect_local_statements(local_lrs)
    store_statements(local_statements, remote_statement_ids, remote_lrs)
