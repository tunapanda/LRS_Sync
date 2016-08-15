from LRS_Sync import collect_local_lrs_credentials , collect_local_statements
import os, sys, json
def statementsToFile(filename, statements):
    writeFile = open(filename,'w')
    writeFile.write(json.dumps(statements, filename))
    writeFile.close()


if __name__ == "__main__":

    try:
        from LRS_config import writefile as filename
    except ImportError:
        print ('\nCould not read output filename. Edit LRS_config.py and add the line\
        \nwritefile = "yourfilenamehere.json"\n')
        sys.exit()

    if os.path.isfile(filename):
        if raw_input("Are you sure you want to overwrite %s? (y/n)" %(filename)) not in ('y','Y','yes','Yes'):
            print "\nAborting. You can change the name of the file to be written in LRS_config.py\n"
            sys.exit()

    local_lrs, lc = collect_local_lrs_credentials()

    local_statements = collect_local_statements(local_lrs)

    statementsToFile(filename, local_statements)
