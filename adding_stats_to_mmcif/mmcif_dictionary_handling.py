import os
import json


class SoftwareClassification:

    def __init__(self):
        self.software_dictionary = dict()
        self.software_name_lower_dict = dict()
        self.get_software_data()

    def get_software_data(self):
        software_json_file = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'software_classification.json')
        if not self.software_dictionary:
            if os.path.exists(software_json_file):
                with open(software_json_file) as json_file:
                    self.software_dictionary = json.load(json_file)
        self.software_name_lower_dict = {k.lower(): k for k in self.software_dictionary.keys()}

    def get_software_name_correct_case(self, software_name):
        """
        return software name in the correct case
        :param software_name: name of software
        :return: case corrected software name or original name
        """
        if software_name.lower() in self.software_name_lower_dict:
            return self.software_name_lower_dict[software_name.lower()]
        return software_name

    def get_software_classification(self, software_name):
        """
        return the classification list for a given piece of software
        :param software_name: name of software
        :return: list of the software classification
        """
        classification = list()
        software_name_correct_case = self.get_software_name_correct_case(software_name)
        if software_name_correct_case in self.software_dictionary:
            classification = self.software_dictionary[software_name_correct_case].split(',')
        return classification

    def get_software_row(self, software_name, classification=None, version=None):
        software_row = dict()
        correct_case_software_name = self.get_software_name_correct_case(software_name)
        software_row['name'] = correct_case_software_name
        classification_list = self.get_software_classification(correct_case_software_name)
        if classification_list:
            if classification not in classification_list:
                classification = classification_list[0]
        else:
            if classification is None:
                classification = ''
        software_row['classification'] = classification
        if version:
            software_row['version'] = str(version)

        return software_row
