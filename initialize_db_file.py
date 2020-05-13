# creates a new empty db file with all tables, etc.
# NOTE - Use as your own risk! Data is not backed up or restorable.
# Copyright Michael Kukar 2020. MIT License.

import sys, os, json
import argparse, sqlite3

# for reference on how dataset JSON should be stored:
# unknown fields can be left as empty ''
JSON_DATASET_EXAMPLE = {
    'data' : [
        {
            'date' : 'YYYY-MM-DD',
            'total_cases' : '1',
            'new_cases' : '0',
            'new_tests' : '0',
            'hospitalizations' : '1',
            'intensive_care' : '1',
            'deaths' : '1'
        }
    ]
}

CREATE_DATA_TABLE_CMD = ("CREATE TABLE DATA "
    "(ID INTEGER PRIMARY KEY,"
    "DATE CHAR(10) NOT NULL UNIQUE,"
    "TOTAL_CASES INTEGER,"
    "NEW_CASES INTEGER,"
    "NEW_TESTS INTEGER,"
    "HOSPITALIZATIONS INTEGER,"
    "INTENSIVE_CARE INTEGER,"
    "DEATHS INTEGER"
    ");"
    )

ENTRY_QUERY = "SELECT DATE, TOTAL_CASES, NEW_CASES, NEW_TESTS, HOSPITALIZATIONS, INTENSIVE_CARE, DEATHS from DATA"


# creates the database file
# args   : input arguments
# return : n/a - will call sys.exit()
def createFile(args):
    print("Creating database with the following parameters:")
    print("\tFilename   : " + str(args.filename))
    print("\tOverwrite? : " + str(args.overwrite))
    print("\tDataset    : " + str(args.dataset))

    # checks if file already exists
    if os.path.exists(args.filename):
        if args.overwrite:
            print("Deleting existing file to overwrite it.")
            os.remove(args.filename)
        else:
            print("ERROR: File already exists. Use --overwrite flag to overwrite it.")
            sys.exit(1)

    # creates database
    conn = sqlite3.connect(args.filename)

    # creates tables
    conn.execute(CREATE_DATA_TABLE_CMD)

    # if dataset given, will populate database with it
    if args.dataset:
        try:
            jsondata = None
            with open(args.dataset) as f:
                jsondata = json.load(f)
            for entry in jsondata['data']:
                # changes date to YYYY-MM-DD FROM MMDDYYYY
                entry['date'] = entry['date'][4:] + '-'+ entry['date'][0:2] + '-' + entry['date'][2:4]
                # executes query to entry data into database
                insertCommand = ("INSERT INTO DATA (DATE, TOTAL_CASES, NEW_CASES, NEW_TESTS, HOSPITALIZATIONS, INTENSIVE_CARE, DEATHS) "
                    "VALUES ("
                    ":date, :total_cases, :new_cases, :new_tests, :hospitalizations, :intensive_care, :deaths)"
                    )
                conn.execute(insertCommand, entry)
            conn.commit()
        except Exception as e:
            print("ERROR: Problem reading your JSON data file.")
            print("ERROR: " + str(e))
            sys.exit(2)

    print("Done! Database file created: \'" + str(args.filename) + "\'")
    sys.exit(0)

# dumps database file to json
# args   : input arguments
# return : n/a - will call sys.exit()
def dumpToJson(args):
    # if dataset not given, we just use a default JSON name
    if not args.dataset:
        args.dataset = "dataset.json"
    print("Dumping database file to json with the following parameters:")
    print("\tJSON Filename : " + str(args.dataset))
    print("\tDB Filename   : " + str(args.filename))
    print("\tOverwrite?    : " + str(args.overwrite))

    # checks if JSON file already exists
    if os.path.exists(args.dataset):
        if args.overwrite:
            print("Deleting existing file to overwrite it.")
            os.remove(args.dataset)
        else:
            print("ERROR: File already exists. Use --overwrite flag to overwrite it.")
            sys.exit(1)
    
    # connects to database and reads tables into a dict
    jsonData = {
        'data' : []
    }

    conn = sqlite3.connect(args.filename)
    c = conn.cursor()
    entries = c.execute(ENTRY_QUERY)
    for entry in entries:
        # fixes date into json format (annoying, shouldn't have done this initially)
        fixedDate = entry[0][5:7] + entry[0][8:] + entry[0][0:4]
        newEntryDict = {
            'date' : fixedDate,
            'total_cases' : entry[1],
            'new_cases' : entry[2],
            'new_tests' : entry[3],
            'hospitalizations' : entry[4],
            'intensive_care' : entry[5],
            'deaths' : entry[6]
        }
        jsonData['data'].append(newEntryDict)
    conn.close()

    # writes dict into JSON file
    with open(args.dataset, 'w') as f:
        json.dump(jsonData, f)

    print("Done! JSON file created: \'" + str(args.dataset) + "\'")
    sys.exit(0)

if __name__ == "__main__":
    # reads in command line arguments
    parser = argparse.ArgumentParser(
        description='Creates a new sqlite database file for Covid19Updater',
        epilog="Copyright Michael Kukar 2020. MIT License."
        )
    parser.add_argument('--file', '-f', default='covid19.db', dest='filename',
                        help='name of database file')
    parser.add_argument('--overwrite', action='store_true', dest='overwrite',
                        help='forcibly overwrites any file with the same name')
    parser.add_argument('--data', '-d', dest='dataset',
                        help='JSON dataset to prepopulate tables')
    parser.add_argument('--dump_to_json', action='store_true', dest='dump',
                        help='Dumps the dataset (if it exists) to a JSON so you can use it to edit/prepopulate different databases')
    args = parser.parse_args()

    if not args.dump:
        createFile(args)
    else:
        dumpToJson(args)
    sys.exit(0)
