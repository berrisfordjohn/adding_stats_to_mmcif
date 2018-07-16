#!/usr/bin/env python

import re 
import requests 
from requests.packages.urllib3.util.retry import Retry 
from requests.adapters import HTTPAdapter 
import logging 
import argparse 

logger = logging.getLogger()
FORMAT = "%(filename)s - %(funcName)s - %(message)s"
logging.basicConfig(format=FORMAT)


BASE_URL = 'https://www.ebi.ac.uk/pdbe/api/'
API_END_POINTS = {'compounds': 'pdb/compound/summary/'}

class GetDataFromPdbeAPi:

    def __init__(self, entry_id, end_point, server_root=BASE_URL):
        self.url = None
        self.entry_id = entry_id
        self.suffix = end_point
        self.server_root = server_root
        self.data = {}

        self.url_from_suffix()
        self.get_data()

    def url_from_suffix(self):
        if self.suffix in API_END_POINTS and self.entry_id and self.server_root:
            suffix = API_END_POINTS[self.suffix]
            self.url = self.server_root + suffix + self.entry_id
        else:
            logging.error('unknown PDBe API call')

    def get_data(self):
        if self.url:
            try:
                self.encode_url()

                s = requests.Session() # start a requests session
                retries = Retry(total=5, # number of retries
                                backoff_factor=1.0, # the factor time in seconds is multiplied by before a retry is tried again
                                status_forcelist=[500, 502, 503, 504]) # retry for these status codes
                s.mount('http://', HTTPAdapter(max_retries=retries)) # retry for these protocols.
                s.mount('https://', HTTPAdapter(max_retries=retries))

                r = s.get(url=self.url, timeout=60)
                # r = requests.get(url=self.url, timeout=60)

                if r.status_code == 200:
                    json_data = r.json()
                    if self.entry_id in json_data:
                        self.data = json_data[self.entry_id]
                    else:
                        self.data = json_data
                elif r.status_code == 404:
                    self.data = {}

                else:
                    logging.error(r.status_code, r.reason)
                    self.data = {}

            except Exception as e:
                logging.error(e)
                self.data = {}

    def return_data(self):
        return self.data

    def encode_url(self):
        self.url = re.sub(" ", "%20", self.url)


class GetSpecificDataFromPdbeAPI:

    def get_one_letter_code_for_compound(self, compound):
        one_letter_code = 'X'
        if compound:        
            compound = compound.upper()
            pdbe_api_data = GetDataFromPdbeAPi(entry_id=compound, end_point='compounds').return_data()
            if pdbe_api_data:
                for data in pdbe_api_data:
                    one_letter_code = data['one_letter_code']
        return one_letter_code

if __name__ == '__main__': 
    parser = argparse.ArgumentParser()
    parser.add_argument('--entry_id', help='the entry to query', type=str, required=True)
    parser.add_argument('--api_end_point', help='the api end point', type=str, required=True)
    parser.add_argument('-d', '--debug', help='debugging', action='store_const', dest='loglevel', const=logging.DEBUG,
                        default=logging.INFO)
    args = parser.parse_args()

    logger.setLevel(args.loglevel)

    pdbe_api_data = GetDataFromPdbeAPi(entry_id=args.entry_id, end_point=args.api_end_point).return_data()
    logging.info(pdbe_api_data)
