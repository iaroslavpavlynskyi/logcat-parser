import os
import datetime
from termcolor import colored

class Parser:

    def __init__(self, logFile, serviceFile):
        self.records = []
        self.services = []
        self.logFile = logFile
        self.serviceFile = serviceFile
        self.__load__()
        self.__load_services__()
        self.commonErrorCounter = 0
        self.__create_report_directory__()

    def __load_services__(self):
        f = open(self.serviceFile, 'r')
        lines = f.readlines()
        for line in lines:
            service = line.split('\n')[0]
            self.services.append(service)

    def __load__(self):
        f = open(self.logFile, 'r')
        lines = f.readlines()
        for line in lines:
            data = line.split('\n')[0]
            if data.startswith('-', 0, 8):
                continue
            else:
                scratch = data.split(' ')
                record = {'pid': scratch[5], 
                   'flag': scratch[6], 
                   'service': scratch[7].strip(':'), 
                   'text': (' ').join(scratch[7:])}
                self.records.append(record)

    def __pretty_print__(self,service ,errors, warnings):
            errors = colored("{0} errors".format(errors), 'red')
            warnings = colored("{0} warnings".format(warnings), 'yellow')
            print(str(service) + ' contains ' + errors + ', ' + warnings)

    def __create_report_directory__(self):
        if not os.path.exists('reports/'):
            os.mkdir('reports/')
    
    def __create_report_subdir__(self):
        dir_name = 'reports/' + str(datetime.datetime.now())
        if not os.path.exists(dir_name):
            os.mkdir(dir_name)
        return dir_name + '/'

    def create_reports_fro_each_service(self):
        dir_name = self.__create_report_subdir__()
        for service in self.services:
            errorCounter = 0
            warningCounter = 0
            f = open(dir_name + service + '.report', 'w+')
            for record in self.records:
                if str(record['text']).__contains__(service):
                    f.write('[' + record['flag'] + ']' + record['service'] + ' ' + record['text'] + '\n')

                    if str(record['flag']).__eq__('E'):
                        errorCounter += 1
                        self.commonErrorCounter += 1
                    if str(record['flag'].__eq__('W')):
                        warningCounter += 1
            self.__pretty_print__(service,errorCounter, warningCounter)

        print ('Total error: ' + str(self.commonErrorCounter))