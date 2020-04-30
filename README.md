# Covid19SanDiegoUpdater
 Sends updates and analysis on current state of COVID-19 in San Diego.

# Dependencies
- Python 3
- BeautifulSoup (pip install beautifulsoup4)
- lxml (pip install lxml)
- Verizon or T-Mobile Phone Number
- Email address (only tested with gmail)

# Setup
1. Install all dependencies (see dependencies section)
2. Copy config_template.json to config.json and populate it with your information
3. Edit the dataset_up_to_4_25.json to reflect the data you want to import
Note - This step is optional but will give you a starting point to populate your database if you chose
3. Run `initialize_db_file.py --data dataset_up_to_4_25.json`
This will create a data file covid19.db that will be used to store the historical dataset
3. Run `covid19_updater.py`
Note - This program will run continuously in the background until you close it. If running in a terminal on linux, you may want to add "nohup" before to prevent it from closing.

# Usage
## covid19_updater
```
covid19_updater.py [-h] [-c CONFIG] [-d DB] [-i INTERVAL]

-h, --help                       : shows help and exit
-c CONFIG, --config CONFIG       : json configuration file. Default is config.json
-d DB, --database DB             : sqlite database file. Default is covid19.db
-i INTERVAL, --interval INTERVAL : interval in seconds to check for updates. Default is 60.

example_config.json
{
    "email_credentials" : {
        "user" : "example@gmail.com",
        "pass" : "Password1!",
        "url" : "smtp.gmail.com"
    },
    "phone_credentials" : [
        {
            "number" : "123456789",
            "carrier" : "VERIZON"
        }
    ]
}
```

## initialize_db_file
```
initialize_db_file.py [-h] [--file FILENAME] [--overwrite] [--data DATASET]

-h, --help                   : shows help and exit
-f FILENAME, --file FILENAME : name of sqlite database file to create. Default is covid19.db
--overwrite                  : if set will overwrite any existing db file of the same name
-d DATASET, --data DATASET   : if given will prepopulate this json data into the database. See below for example formatting:

example_dataset.json
{
    "data" : [
        {
            "date" : "04252020",
            "total_cases" : 3043,
            "new_cases" : 100,
            "new_tests" : 1297,
            "hospitalizations" : null,
            "intensive_care" : null,
            "deaths" : null
        },
        {
            ...
        }
    ]
}

```

# Converting to another data source
NOTE - You will need some experience with Python to make this change.

Since you likely do not live in San Diego, with some small edits you can make this script work in your city instead.
The main feature you must locate is a single website page that at minimum contains the latest date the dataset was updated and the total number of cases.
Finding another site that has the historical total cases per day will also be useful if you want to backfill your data.
Once you have found this website, do the following:

1. Open web_reader.py in your favorite text editor
2. Edit SD_COVID19_URL to instead point to the website you found (around Line 17)
3. Edit the isNewDataAvailable function to extract the date from this website using BeautifulSoup (around lines 98 - 105). You can use the existing code as a starting point.
4. Edit the readLatestEntryFromWeb function to extract the date and other pertinent fields using BeautifulSoup (around lines 134-153). If you do not have all the fields you can leave them as None.
5. To test your changes, use the test_web_reader.py test suite. You will have to replace the test_valid_data_website.html with a copy of your local website (cntrl-S in firefox/chrome)

If you have made this change, please submit a pull request with a seperate branch or upload your code seperately to your own GitHub!

# Author
Michael Kukar

# License
MIT License

Copyright (c) 2020 Michael Kukar

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
