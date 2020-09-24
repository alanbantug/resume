#! python3

import json
import os

class config(object):

    def __init__(self):

        self.configFile = "data\config.json"

        if os.path.exists(self.configFile):
            pass
        else:
            self.initConfigFile()

    def initConfigFile(self):

        data = {"Directory": "", "Location": "", "Name": "", "Categories": ["No Selection"], 'Last Resume': ''}

        # this code will create the data subdirectory the first time the program runs
        try:
            config_file = open(self.configFile, "w")
        except:
            os.makedirs("data")
            config_file = open(self.configFile, "w")

        config_file.close()

        # call the writeConfigFile function to write the JSON file
        self.writeConfigFile(data)

    def writeConfigFile(self, data):

        with open(self.configFile, 'w') as o_file:
            json.dump(data, o_file)

        o_file.close()

    def readConfigFile(self):

        with open(self.configFile, 'r') as i_file:
            for data_line in i_file:
                data = json.loads(data_line)

        i_file.close()

        return data

    def getSettings(self):

        return self.readConfigFile()

    def getWorkDirectory(self):

        data = self.getSettings()

        return data['Directory']

    def getLocation(self):

        data = self.getSettings()

        return data['Location']

    def getName(self):

        data = self.getSettings()

        return data['Name']

    def getCompanies(self):

        data = self.getSettings()

        data_sort = sorted(data['Companies'][1:])
        data_sort.insert(0, data['Companies'][0])

        return data_sort

    def getCategories(self):

        data = self.getSettings()

        data_sort = sorted(data['Categories'][1:])
        data_sort.insert(0, data['Categories'][0])

        return data_sort

    def getLastResume(self):

        data = self.getSettings()

        return data['Last Resume']

    def updateSettings(self, directory, location, name):

        data = self.readConfigFile()

        data['Directory'] = directory
        data['Location'] = location
        data['Name'] = name

        self.writeConfigFile(data)

        return True

    def updateLocation(self, location):

        data = self.readConfigFile()

        data['Location'] = location

        self.writeConfigFile(data)

        return True

    # def updateName(self, name):
    #
    #     data = self.readConfigFile()
    #
    #     data['Name'] = name
    #
    #     self.writeConfigFile(data)
    #
    #     return True
    #
    def updateLastResume(self, name):

        data = self.readConfigFile()

        data['Last Resume'] = name

        self.writeConfigFile(data)

        return True

    def addCompany(self, company):

        data = self.readConfigFile()

        data['Companies'].append(company)

        self.writeConfigFile(data)

        return True

    def delCompany(self, company):

        data = self.readConfigFile()

        # get the index
        idx = data['Companies'].index(company)

        # pop the index out
        data['Companies'].pop(idx)

        self.writeConfigFile(data)

        return True

    def addCategory(self, category):

        data = self.readConfigFile()

        data['Categories'].append(category)

        self.writeConfigFile(data)

        return True

    def delCategory(self, category):

        data = self.readConfigFile()

        # get the index
        idx = data['Categories'].index(category)

        # pop the index out
        data['Categories'].pop(idx)

        self.writeConfigFile(data)

        return True
