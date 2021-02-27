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

        data = {"Location": "", "Name": "", 'Last Resume': ''}

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

    def getCompanies(self, category):

        print(category)

        data = self.getSettings()

        com_list = []

        if data['Location']:
            pass
        else:
            return com_list

        work_dir = os.getcwd()

        for dirs, subs, files in os.walk(data['Location']):

            for sub in subs:
                temp = os.path.join(dirs, sub)
                print(temp)

                try:
                    if temp.index(category):
                        item = temp.split("\\")[2]
                        if item in com_list:
                            pass
                        else:
                            com_list.append(sub)
                except:
                    pass

        return com_list

    def getCategories(self):

        data = self.getSettings()

        cat_list = []

        if data['Location']:
            pass
        else:
            return cat_list

        work_dir = os.getcwd()

        for dirs, subs, files in os.walk(data['Location']):

            for sub in subs:
                temp = os.path.join(dirs, sub)
                item = temp.split("\\")[1]
                if item in cat_list:
                    pass
                else:
                    cat_list.append(sub)

        cat_list.insert(0, "No Selection")
        return cat_list


    def getLastResume(self):

        data = self.getSettings()

        return data['Last Resume']

    def updateSettings(self, location, name):

        data = self.readConfigFile()

        data['Location'] = location
        data['Name'] = name

        self.writeConfigFile(data)

        return True

    def updateLocation(self, location):

        data = self.readConfigFile()

        data['Location'] = location

        self.writeConfigFile(data)

        return True

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

        work_dir = os.getcwd()

        os.chdir(data['Location'])
        os.makedirs(category)

        os.chdir(work_dir)

        return True

    def delCategory(self, category):

        data = self.readConfigFile()

        work_dir = os.getcwd()

        os.chdir(data['Location'])
        os.rmdir(category)

        os.chdir(work_dir)

        return True
