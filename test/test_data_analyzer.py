# tests data_analyzer.py
# CB: Michael Kukar
# Copyright Michael Kukar 2020.

import unittest, shutil
import sys, os

sys.path.append('..')
from data_analyzer import *
from web_reader import WebReader

class UnitTestCases(unittest.TestCase):

    TEST_DB_FILE = "basic_populated_database.db"

    # 10-10 is much later than the test database (april 25th)
    MAX_NEW_CASES_ENTRY = {
        'date' : '2020-10-10',
        'total_cases' : None,
        'new_cases' : 10000,
        'new_tests' : None,
        'hospitalizations' : None,
        'intensive_care' : None,
        'deaths' : None
    }

    NONE_NEW_CASES_ENTRY = {
        'date' : '2020-10-10',
        'total_cases' : None,
        'new_cases' : None,
        'new_tests' : None,
        'hospitalizations' : None,
        'intensive_care' : None,
        'deaths' : None
    }

    ZERO_NEW_CASES_ENTRY = {
        'date' : '2020-10-10',
        'total_cases' : None,
        'new_cases' : 0,
        'new_tests' : None,
        'hospitalizations' : None,
        'intensive_care' : None,
        'deaths' : None
    }

    def setUp(self):
        # copies dummy database that is empty
        shutil.copyfile(self.TEST_DB_FILE, "temp_" + self.TEST_DB_FILE)

        self.da = DataAnalyzer("temp_" + self.TEST_DB_FILE)
        # uses web reader to add entries to database
        self.wr = WebReader("temp_" + self.TEST_DB_FILE)

    def tearDown(self):
        # deletes our dummy database file
        os.remove("temp_" + self.TEST_DB_FILE)

    def test_checkIfLatestIsMaxNewCasesReturnsTrueIfLatestNewCasesAreHighestInDataset(self):
        # adds a large new_cases entry into the database
        self.wr.addEntryToDatabase(self.MAX_NEW_CASES_ENTRY)
        self.assertTrue(self.da.checkIfLatestIsMaxNewCases())

    def test_checkIfLatestIsMaxNewCasesReturnsFalseIfLatestNewCasesIsNone(self):
        self.wr.addEntryToDatabase(self.NONE_NEW_CASES_ENTRY)
        self.assertFalse(self.da.checkIfLatestIsMaxNewCases())
    
    def test_checkIfLatestIsMaxNewCasesReturnsFalseIfLatestIsNotMax(self):
        self.wr.addEntryToDatabase(self.ZERO_NEW_CASES_ENTRY)
        self.assertFalse(self.da.checkIfLatestIsMaxNewCases())

    def test_getNewCasesTrendReturnsCorrectTrendAcrossThreeDays(self):
        daysData = []
        for x in range(3):
            daysData.append(dict(self.MAX_NEW_CASES_ENTRY))
        daysData[0]['new_cases'], daysData[0]['date'] = 1, '2020-10-10'
        daysData[1]['new_cases'], daysData[1]['date'] = 3, '2020-10-11' 
        daysData[2]['new_cases'], daysData[2]['date'] = 4, '2020-10-12'   
        for data in daysData:     
            self.wr.addEntryToDatabase(data)
        self.assertEqual(1.5, self.da.getNewCasesTrend(days=3))
    
    def test_getNewCasesTrendReturnsCorrectTrendSkippingEntriesThatAreNone(self):
        daysData = []
        for x in range(3):
            daysData.append(dict(self.MAX_NEW_CASES_ENTRY))
        daysData[0]['new_cases'], daysData[0]['date'] = 1, '2020-10-10'
        daysData[1]['new_cases'], daysData[1]['date'] = 3, '2020-10-11' 
        daysData[2]['new_cases'], daysData[2]['date'] = None, '2020-10-12'   
        for data in daysData:     
            self.wr.addEntryToDatabase(data)
        self.assertEqual(2.0, self.da.getNewCasesTrend(days=3))    

    def test_getNewCasesTrendReturnsZeroIfDaysIsNotGreaterThanTwo(self):
        self.assertEqual(0.0, self.da.getNewCasesTrend(days=-1))
        self.assertEqual(0.0, self.da.getNewCasesTrend(days=0))
        self.assertEqual(0.0, self.da.getNewCasesTrend(days=1))
    
    def test_getLatestNewCasesAverageReturnsCorrectAverageAcrossSevenDays(self):
        daysData = []
        for x in range(3):
            daysData.append(dict(self.MAX_NEW_CASES_ENTRY))
        daysData[0]['new_cases'], daysData[0]['date'] = 15, '2020-10-10'
        daysData[1]['new_cases'], daysData[1]['date'] = 30, '2020-10-11' 
        daysData[2]['new_cases'], daysData[2]['date'] = 45, '2020-10-12'   
        for data in daysData:     
            self.wr.addEntryToDatabase(data)
        self.assertEqual(30.0, self.da.getLatestNewCasesAverage(days=3))

    
    def test_getLatestNewCasesAverageReturnsCorrectAverageSkippingEntriesThatAreNone(self):
        daysData = []
        for x in range(3):
            daysData.append(dict(self.MAX_NEW_CASES_ENTRY))
        daysData[0]['new_cases'], daysData[0]['date'] = 1, '2020-10-10'
        daysData[1]['new_cases'], daysData[1]['date'] = 10, '2020-10-11' 
        daysData[2]['new_cases'], daysData[2]['date'] = None, '2020-10-12'   
        for data in daysData:     
            self.wr.addEntryToDatabase(data)
        self.assertEqual(5.5, self.da.getLatestNewCasesAverage(days=3))
    
    def test_getLatestNewCasesAverageReturnsZeroIfDaysIsNotPositive(self):
        self.assertEqual(0.0, self.da.getLatestNewCasesAverage(days=-1))
        self.assertEqual(0.0, self.da.getLatestNewCasesAverage(days=0))


if __name__ == "__main__":
    unittest.main()