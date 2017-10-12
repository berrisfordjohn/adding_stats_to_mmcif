#!/usr/bin/env python
import logging
import basestring
import mmCif.mmcifIO as mmcif

class mmcifHandling:

    def __init__(self, fileName, datablock=0, atom_site=False):
        self.f = fileName
        self.cifObj = None
        self.datablock = datablock

    def parse_mmcif_all(self):
        '''parse the mmcif and return a dictionary file'''
        cfr = mmcif.CifFileReader()
        try:
            # parse the cif file
            if atom_site == False:
                self.cifObj = cfr.read(self.f, output='cif_dictionary', ignore=["_atom_site", "_atom_site_anisotrop"]).values()
            else:
                self.cifObj = cfr.read(self.f, output='cif_dictionary').values()

        except Exception as e:
            logging.error("unable to parse mmcif file: %s" % (self.f))
            logging.error(e)

        return self.cifObj

    def getCategory(self, category):
        if category in self.cifObj:
            logging.debug('Category %s found' % category)
            for item in self.cifObj[self.datablock][category]:
                value = self.cifObj[self.datablock][category][item]
                if isinstance(value, basestring):
                    self.cifObj[self.datablock][category][item] = [value]
            return self.cifObj[self.datablock][category]
        else:
            logging.debug('Category %s not found' % category)
            return None

    def addToCif(self, mmcif_dictionary):
        for cat in mmcif_dictionary:
            self.cifObj[self.datablock][cat] = mmcif_dictionary[cat]

    def writeCif(self, fileName):
        cfd1 = mmcif.CifFileWriter(fileName)
        cfd1.write(self.cifObj, preserve_order=True)
