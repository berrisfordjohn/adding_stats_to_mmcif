#!/usr/bin/env python
import xml.etree.ElementTree as ET
import logging
import pprint
import os
import argparse

logger = logging.getLogger()

stats_remap = {
    'reflns': {'pos_list': ['Overall'],
               'cif_to_xml':
                   {'d_resolution_low': 'ResolutionLow',
                    'd_resolution_high': 'ResolutionHigh',
                    'pdbx_Rmerge_I_obs': 'Rmerge',
                    'pdbx_Rrim_I_all': 'Rmeas',
                    'pdbx_Rpim_I_all': 'Rpim',
                    'number_measured_obs': 'NumberReflections',
                    'pdbx_netI_over_sigmaI': 'MeanIoverSD',
                    'pdbx_CC_half': 'CChalf',
                    'percent_possible_obs': 'Completeness',
                    'pdbx_redundancy': 'Multiplicity'}},
    'reflns_shell': {'pos_list': ['Inner', 'Outer'],
                     'cif_to_xml':
                         {'d_res_low': 'ResolutionLow',
                          'd_res_high': 'ResolutionHigh',
                          'Rmerge_I_obs': 'Rmerge',
                          'pdbx_Rrim_I_all': 'Rmeas',
                          'pdbx_Rpim_I_all': 'Rpim',
                          'number_measured_obs': 'NumberReflections',
                          'pdbx_netI_over_sigmaI': 'MeanIoverSD',
                          'pdbx_CC_half': 'CChalf',
                          'percent_possible_obs': 'Completeness',
                          'pdbx_redundancy': 'Multiplicity'}}
}

extra_cif_items = {'pdbx_ordinal': ''}

table_keys = {'deposition': 'reflns'}

class aimlessReport:
    def __init__(self, xml_file):
        self.xml_file = xml_file
        self.tree = None
        self.root = None
        self.stats_dict = dict()

    def parse_xml(self):
        try:
            if os.path.exists(xml_file):
                self.tree = ET.parse(self.xml_file)
                self.root = self.tree.getroot()
                if self.root:
                    if self.root.tag == 'AIMLESS_PIPE':
                        logging.debug('is an aimless xml file')
                        return True
            logging.debug('not an aimless xml file')
            return False

        except Exception as e:
            logging.error(e)
            return False

    def get_data(self):
        datasetresultnodes = self.root.findall(".//Result/Dataset")
        data_set_counter = 0
        for datasetresultnode in datasetresultnodes:
            data_set_counter += 1
            for cif_cat in stats_remap:

                location_list = stats_remap[cif_cat]['pos_list']
                number_of_values = len(location_list)

                for instance, location in enumerate(location_list):
                    for cif_item in stats_remap[cif_cat]['cif_to_xml']:
                        logging.debug(cif_item)
                        xml_item = stats_remap[cif_cat]['cif_to_xml'][cif_item]

                        xml_node = datasetresultnode.find(xml_item)
                        xml_item_for_location = xml_node.find(location)

                        logging.debug(xml_item_for_location)
                        xml_value = xml_item_for_location.text.strip()
                        logging.debug(xml_value)

                        self.stats_dict.setdefault(cif_cat, {}).setdefault(cif_item, ['']*number_of_values)[instance] = xml_value
                    for cif_item in extra_cif_items:
                        if extra_cif_items[cif_item]:
                            value = extra_cif_items[cif_item]
                        else:
                            value = instance + 1
                        self.stats_dict.setdefault(cif_cat, {}).setdefault(cif_item, [''] * number_of_values)[instance] = str(value)

        return self.stats_dict

    def get_data_from_table(self):
        ccp4tables = self.root.findall(".//CCP4Table")
        logging.debug(ccp4tables)
        for table in ccp4tables:
            logging.debug(table.attrib)
            if 'id' in table.attrib:
                if table.attrib['id'] in table_keys:
                    # need to set cif category based on the table name.
                    cif_cat = table_keys[table.attrib['id']]
                    headers = table.find('headers')
                    separator = headers.attrib['separator']
                    logging.debug('separator: "%s"' % separator)
                    if separator == ' ':
                        header_list = headers.text.split()
                    else:
                        header_list = headers.text.split(separator)
                    data = table.find('data').text
                    logging.debug(data)
                    data_lines = data.strip().split('\n')
                    logging.debug(data_lines)
                    number_of_data_values = len(data_lines)
                    logging.debug('number of data items: %s' % number_of_data_values)
                    for instance, d in enumerate(data_lines):
                        if separator == ' ':
                            d = d.strip().split()
                        else:
                            d = d.strip().split(separator)
                        logging.debug(d)
                        for header_pos, item in enumerate(header_list):
                            logging.debug('%s - position %s' % (item, header_pos))
                            value = d[header_pos]
                            self.stats_dict.setdefault(cif_cat, {}).setdefault(item, ['']*number_of_data_values)[instance] = value
        return self.stats_dict


    def return_data(self):
        is_aimless_file = self.parse_xml()
        if is_aimless_file:
            self.get_data_from_table()
            if not self.stats_dict:
                self.get_data()

        return self.stats_dict

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--xml_file', help='input xml file', type=str, required=True)
    parser.add_argument('-d', '--debug', help='debugging', action='store_const', dest='loglevel', const=logging.DEBUG,
                        default=logging.INFO)

    args = parser.parse_args()
    logger.setLevel(args.loglevel)

    xml_file = args.xml_file
    ar = aimlessReport(xml_file=xml_file)
    xml_data = ar.return_data()
    pprint.pprint(xml_data)
