from LRS_Sync import collect_remote_lrs_credentials , collect_remote_statements, store_statements
import os, sys, json

def import_statements_from_file(filename):
    try:
        statements = open(filename)
    except ImportError:
        print ("\n%s does not exist. Please check the settings in LRS_config.py\n" %(filename))
        sys.exit()

    return json.loads(statements.read())

if __name__ == "__main__":
    try:
        from LRS_config import readfile as filename
    except ImportError:
        print ('\nCould not read input filename. Edit LRS_config.py and add the line\
        \nreadfile = "yourfilenamehere.json"\n')
        sys.exit()

    remote_lrs, rc = collect_remote_lrs_credentials()
    statements = import_statements_from_file(filename)
    remote_statement_ids = collect_remote_statements(remote_lrs, rc)
    store_statements(statements, remote_statement_ids, remote_lrs)
