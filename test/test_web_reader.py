# tests web_reader.py
# CB: Michael Kukar
# Copyright Michael Kukar 2020.

import unittest
import sys, os, shutil

sys.path.append('..')
from web_reader import *

class WebTestCases(unittest.TestCase):

    EMPTY_DB_FILE = "empty_test_database.db"

    DB_OLDER_TIMESTAMP = {
        'date' : '01012020',
        'total_cases' : 1,
        'new_cases' : 1,
        'new_tests' : 1,
        'hospitalizations' : 0,
        'intensive_care' : 5,
        'deaths' : 0
    }
    DB_SAME_TIMESTAMP = {
        'date' : '04242020',
        'total_cases' : 1,
        'new_cases' : 1,
        'new_tests' : 1,
        'hospitalizations' : 0,
        'intensive_care' : 5,
        'deaths' : 0
    }
    DB_NEWER_TIMESTAMP = {
        'date' : '04252020',
        'total_cases' : 1,
        'new_cases' : 1,
        'new_tests' : 1,
        'hospitalizations' : 0,
        'intensive_care' : 5,
        'deaths' : 0
    }
    VALID_WEBSITE_FILENAME = "test_valid_data_website.html"

    def setUp(self):
        # copies dummy database that is empty
        shutil.copyfile(self.EMPTY_DB_FILE, "temp_" + self.EMPTY_DB_FILE)

        # constructs urls from filenames and path
        self.valid_website_url = "file:///" + os.path.dirname(os.path.abspath(__file__)) + '/' + self.VALID_WEBSITE_FILENAME

        self.wr = WebReader("temp_" + self.EMPTY_DB_FILE)

    def tearDown(self):
        # deletes our dummy database file
        os.remove("temp_" + self.EMPTY_DB_FILE)

    def test_isNewDataAvailableReturnsFalseIfWebTimestampOlderThanLatestDbTimestamp(self):
        self.wr.addEntryToDatabase(self.DB_NEWER_TIMESTAMP)
        self.assertFalse(self.wr.isNewDataAvailable(url=self.valid_website_url))
    
    def test_isNewDataAvailableReturnsTrueIfWebTimestampNewerThanLatestDbTimestamp(self):
        self.wr.addEntryToDatabase(self.DB_OLDER_TIMESTAMP)
        self.assertTrue(self.wr.isNewDataAvailable(url=self.valid_website_url))
    
    def test_isNewDataAvailableReturnsFalseIfCannotReadWebsite(self):
        self.wr.addEntryToDatabase(self.DB_OLDER_TIMESTAMP)
        self.assertFalse(self.wr.isNewDataAvailable(url="invalid"))
    
    def test_isNewDataAvailableReturnsFalseIfWebTimestampMatchesDbTimestamp(self):
        self.wr.addEntryToDatabase(self.DB_SAME_TIMESTAMP)
        self.assertFalse(self.wr.isNewDataAvailable(url=self.valid_website_url))
    
    def test_isNewDataAvailableReturnsTrueIfNoDataInDatabase(self):
        self.assertTrue(self.wr.isNewDataAvailable())

    def test_readLatestEntryFromWebReturnsValidDatasetOnValidWebsite(self):
        self.assertTrue(False)
    
    def test_readLatestEntryFromWebReturnsNoneIfInvalidWebsiteData(self):
        self.assertTrue(False)
    
    def test_readLatestEntryFromWebReturnsNoneIfWebsiteInaccessible(self):
        self.assertTrue(False)


class DatabaseTestCases(unittest.TestCase):

    EMPTY_DB_FILE = "empty_test_database.db"

    VALID_DB_ENTRY = {
        'date' : '01022020',
        'total_cases' : 1,
        'new_cases' : 1,
        'new_tests' : 1,
        'hospitalizations' : 0,
        'intensive_care' : 5,
        'deaths' : 0
    }
    VALID_DB_ENTRY_OLDER = {
        'date' : '01012020',
        'total_cases' : 1,
        'new_cases' : 1,
        'new_tests' : 1,
        'hospitalizations' : 0,
        'intensive_care' : 5,
        'deaths' : 0
    }

    INCOMPLETE_DB_ENTRY = {
        'date' : '01022020',
        'total_cases' : 1,
        'new_cases' : 1
    }

    BAD_RANGES_DB_ENTRY = {
        'date' : '01022020',
        'total_cases' : -1,
        'new_cases' : -1,
        'new_tests' : -1,
        'hospitalizations' : 0,
        'intensive_care' : -5,
        'deaths' : 0
    }

    def setUp(self):
        # copies dummy database that is empty
        shutil.copyfile(self.EMPTY_DB_FILE, "temp_" + self.EMPTY_DB_FILE)

        self.wr = WebReader("temp_" + self.EMPTY_DB_FILE)

    def tearDown(self):
        # deletes our dummy database file
        os.remove("temp_" + self.EMPTY_DB_FILE)

    def test_addEntryToDatabaseSucceedsWhenDatasetIsValid(self):
        self.assertTrue(self.wr.addEntryToDatabase(self.VALID_DB_ENTRY))
        conn = sqlite3.connect("temp_" + self.EMPTY_DB_FILE)
        dataset = conn.execute("select * from DATA")
        self.assertEqual(1, len(dataset.fetchall()))
        conn.close()
    
    def test_addEntryToDatabaseFailsWhenDatasetIsCorrupted(self):
        self.assertFalse(self.wr.addEntryToDatabase(None))
    
    def test_addEntryToDatabaseFailsWhenDatasetIsIncomplete(self):
        self.assertFalse(self.wr.addEntryToDatabase(self.INCOMPLETE_DB_ENTRY))
    
    def test_addEntryToDatabaseFailsWhenDatasetIsOutOfValidRanges(self):
        self.assertFalse(self.wr.addEntryToDatabase(self.BAD_RANGES_DB_ENTRY))

    def test_addEntryToDatabaseFailsWhenDatasetTimestampAlreadyExists(self):
        self.assertTrue(self.wr.addEntryToDatabase(self.VALID_DB_ENTRY))
        self.assertFalse(self.wr.addEntryToDatabase(self.VALID_DB_ENTRY))
        conn = sqlite3.connect("temp_" + self.EMPTY_DB_FILE)
        dataset = conn.execute("select * from DATA")
        self.assertEqual(1, len(dataset.fetchall()))
        conn.close()

    def test_readLatestEntryFromDatabaseReturnsMostRecentTimestampFromDatabase(self):
        self.wr.addEntryToDatabase(self.VALID_DB_ENTRY)
        self.wr.addEntryToDatabase(self.VALID_DB_ENTRY_OLDER)
        self.assertDictEqual(self.VALID_DB_ENTRY, self.wr.readLatestEntryFromDatabase())
    
    def test_readLatestEntryFromDatabaseReturnsNoneIfNoDataPresent(self):
        self.assertIsNone(self.wr.readLatestEntryFromDatabase())

if __name__ == "__main__":
    unittest.main()