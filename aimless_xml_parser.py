#!/usr/bin/env python
import xml.etree.ElementTree as ET
import logging
import pprint

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

extra_cif_items = {'pdbx_diffrn_id': '1',
                   'pdbx_ordinal': ''}

class aimlessReport:
    def __init__(self, xml_file):
        self.xml_file = xml_file
        self.tree = None
        self.root = None
        self.stats_dict = dict()

    def parse_xml(self):
        self.tree = ET.parse(self.xml_file)
        self.root = self.tree.getroot()

    def get_data(self):
        datasetresultnodes = self.root.findall(".//Result/Dataset")
        for datasetresultnode in datasetresultnodes:
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
        cif_cat = 'anisotropy'
        ccp4tables = self.root.findall(".//CCP4Table")
        logging.debug(ccp4tables)
        for table in ccp4tables:
            logging.debug(table.attrib)
            if 'id' in table.attrib:
                if table.attrib['id'] == 'AnisotropyAnalysis':
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


if __name__ == '__main__':
    logger.setLevel(logging.DEBUG)
    xml_file = 'test_data/gam-pipe.xml'
    ar = aimlessReport(xml_file=xml_file)
    ar.parse_xml()
    #ar.get_data()
    ar.get_data_from_table()
    pprint.pprint(ar.stats_dict)
