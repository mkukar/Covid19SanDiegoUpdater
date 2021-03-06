# main file
# Sends updates and analysis on current state of COVID-19 in San Diego 
# Copyright Michael Kukar 2020. MIT License.

import sys, os, json, threading, argparse, time

from web_reader import WebReader
from email_texter import EmailTexter
from data_analyzer import DataAnalyzer

class Covid19Updater:

    configData = {}
    phoneNumberEmails = []

    # constructor
    # sets up objects and reads config file
    # configFile : json configuration file
    # dbFile     : sqlite database file
    def __init__(self, configFile, dbFile):
        self.wr = WebReader(dbFile)
        self.et = EmailTexter()
        self.da = DataAnalyzer(dbFile)
        if not self.parseConfig(configFile):
            # fail construction as the config is invalid
            raise Exception("Invalid config file") 
        for phoneData in self.configData["phone_credentials"]:
            self.phoneNumberEmails.append(self.et.getPhoneNumberEmailAddress(phoneData['number'], phoneData['carrier']))


    # reads json config file into configData dict
    # configFile : json configuration file
    # return     : True on success, false on fail
    def parseConfig(self, configFile):
        try:
            with open(configFile) as f:
                self.configData = json.load(f)
        except:
            return False
        # ensures all required aspects of the file are present
        if 'phone_credentials' not in self.configData.keys():
            return False
        if 'email_credentials' not in self.configData.keys():
            return False
        phone_credentials_req_fields = ['number', 'carrier']
        email_credentials_req_fields = ['user', 'pass', 'url']
        for phoneData in self.configData['phone_credentials']:
            for req_field in phone_credentials_req_fields:
                if req_field not in phoneData.keys():
                    return False
        for req_field in email_credentials_req_fields:
            if req_field not in self.configData['email_credentials'].keys():
                return False
        return True


    # checks for an update and sends message if one is available
    # forceSend : (optional) always sends the update
    # return    : None
    def checkForUpdateAndSend(self, forceSend=False):
        if self.wr.isNewDataAvailable() or forceSend:
            # gets new data
            latestWebData = self.wr.readLatestEntryFromWeb()

            # calculates new cases from previous data entry and this one
            latestDbData = self.wr.readLatestEntryFromDatabase()
            if latestDbData is not None:
                latestWebData['new_cases'] = int(latestWebData['total_cases']) - int(latestDbData['total_cases'])
            else:
                latestWebData['new_cases'] = int(latestWebData['total_cases'])

            # saves to database
            if not self.wr.addEntryToDatabase(latestWebData):
                print("failed to add entry to database?")

            # sends update using text to email
            # initializes email server now since otherwise may time out over several hours
            emailserver = self.et.initializeEmailServer(
                self.configData['email_credentials']['user'],
                self.configData['email_credentials']['pass'],
                self.configData['email_credentials']['url']
            )
            # generates the text message to send
            textMessage = "LATEST SD COVID19 UPDATE:\n"
            textMessage += "New Cases: " + str(latestWebData['new_cases']) + "\n"
            textMessage += "Total Cases: " + str(latestWebData['total_cases']) + "\n"

            for email in self.phoneNumberEmails:
                # t-mobile does not allow website link, so only add if that is not the number
                messageToSend = textMessage
                if not "tmomail.net" in email:
                    messageToSend += "https://bit.ly/2W8uQJM" # shortened URL to SD Covid19 Website
                self.et.sendMessage(
                    email,
                    messageToSend,
                    emailserver
                )
            time.sleep(1) # prevents messages from being sent out of order

            # generates a second message that is analysis
            analysisTextMessage = self.getAnalysisMessage()
            for email in self.phoneNumberEmails:
                self.et.sendMessage(
                    email,
                    analysisTextMessage,
                    emailserver
                )

            emailserver.close()
    

    # generates an analysis message based on the latest data
    # return : string of analysis data in text message format
    def getAnalysisMessage(self):
        factBlurbs = ["Analysis:"]
        # format is up to 3 facts, ranked by importance
        # first up is if latest cases is max of all time
        if self.da.checkIfLatestIsMaxNewCases():
            factBlurbs.append("- Today is the highest number of new cases yet")
        # now gets the 3-day trend to see if we're going up or down
        dayTrend = self.da.getNewCasesTrend(days=3)
        if dayTrend != 0:
            factBlurbs.append(f'- The 3-day trend of new cases is {dayTrend:.2f}/day')
        # now gets the 7-day average to see what most days are
        weekAverage = self.da.getLatestNewCasesAverage(days=7)
        if weekAverage != 0:
            factBlurbs.append(f'- The 7-day average of new cases is {weekAverage:.2f}/day')

        outputMessage = '\n'.join(factBlurbs)
        return outputMessage


    # daemon that runs the check update every X seconds
    # frequencySecs : number of seconds between calls to checkForUpdateAndSend()
    def checkUpdateDaemon(self, frequencySecs):
        self.checkForUpdateAndSend()
        threading.Timer(frequencySecs, self.checkUpdateDaemon, [frequencySecs]).start()


if __name__ == "__main__":
    # parses in command line input
    parser = argparse.ArgumentParser(
        description='Sends updates and analysis on current state of COVID-19 in San Diego',
        epilog='Copyright Michael Kukar 2020. MIT License.'
        )
    parser.add_argument("-c", "--config", dest="config", default="config.json", help="json configuration file")
    parser.add_argument("-d", "--database", dest="db", default="covid19.db", help="sqlite databse file")
    parser.add_argument("-i", "--interval", type=int, dest="interval", default=60, help="interval in seconds to check for updates")
    args = parser.parse_args()

    print("COVID-19 Updater")
    print("\tConfig File           : " + args.config)
    print("\tDB File               : " + args.db)
    print("\tCheck Interval (secs) : " + str(args.interval))

    # checks files exist
    if not os.path.exists(args.config):
        print("ERROR: Config file not found.")
        sys.exit(1)
    if not os.path.exists(args.db):
        print("ERROR: SQLite database file not found.")
        sys.exit(1)

    cu = None
    try:
        cu = Covid19Updater(args.config, args.db)
    except Exception as e:
        print("ERROR: " + str(e))
        sys.exit(2)

    # starts daemon (will never end!)
    cu.checkUpdateDaemon(frequencySecs=args.interval)
