# creates a new empty db file with all tables, etc.
# NOTE - Use as your own risk! Data is not backed up or restorable.
# CB: Michael Kukar
# Copyright Michael Kukar 2020.

import sys, os, json
import argparse, sqlite3

# for reference on how dataset JSON should be stored:
# unknown fields can be left as empty ''
JSON_DATASET_EXAMPLE = {
    'data' : [
        {
            'date' : 'MMDDYYYY',
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
    "DATE CHAR(8) NOT NULL,"
    "TOTAL_CASES INTEGER,"
    "NEW_CASES INTEGER,"
    "NEW_TESTS INTEGER,"
    "HOSPITALIZATIONS INTEGER,"
    "INTENSIVE_CARE INTEGER,"
    "DEATHS INTEGER"
    ");"
    )

if __name__ == "__main__":
    # reads in command line arguments
    parser = argparse.ArgumentParser(
        description='Creates a new database file for Covid19Updater',
        epilog="Copyright Michael Kukar 2020."
        )
    parser.add_argument('--file', '-f', default='covid19.db', dest='filename',
                        help='name of database file')
    parser.add_argument('--overwrite', action='store_true', dest='overwrite',
                        help='forcibly overwrites any file with the same name')
    parser.add_argument('--data', '-d', dest='dataset',
                        help='JSON dataset to prepopulate tables')
    args = parser.parse_args()

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
                # executes query to entry data into database
                insertCommand = ("INSERT INTO DATA (DATE, TOTAL_CASES, NEW_CASES, NEW_TESTS, HOSPITALIZATIONS, INTENSIVE_CARE, DEATHS) "
                    "VALUES ("
                    ":date, :total_cases, :new_cases, :new_tests, :hospitalizations, :intensive_care, :deaths)"
                    )
                conn.execute(insertCommand, entry)
        except Exception as e:
            print("ERROR: Problem reading your JSON data file.")
            print("ERROR: " + str(e))
            sys.exit(2)

    print("Done! Database file created: \'" + str(args.filename) + "\'")
    sys.exit(0)