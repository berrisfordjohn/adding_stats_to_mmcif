#!/usr/bin/env python

import cif_handling
from Entity import Entity
from Chain import Chain
import os
import cPickle as pickle

residue_map_1to3 = {
    'A': 'ALA', 'C': 'CYS', 'D': 'ASP', 'E': 'GLU', 'F': 'PHE', 'G': 'GLY',\
    'H': 'HIS', 'I': 'ILE', 'K': 'LYS', 'L': 'LEU', 'M': 'MET', 'N': 'ASN',\
    'P': 'PRO', 'Q': 'GLN', 'R': 'ARG', 'S': 'SER', 'T': 'THR', 'V': 'VAL',\
    'W': 'TRP', 'X': 'UNK', 'Y': 'TYR',
}

residue_map_3to1 = {v: k for k, v in residue_map_1to3.items()}
residue_map_3to1['A'] = 'A'
residue_map_3to1['G'] = 'G'
residue_map_3to1['C'] = 'C'
residue_map_3to1['T'] = 'T'
residue_map_3to1['U'] = 'U'

class MMCIF_Poly(object):
    """Docstring for MMCIF_Poly. """

    def __init__(self, mmcif_file):
        self.__mmcif_file = mmcif_file
        self.__get_mmcif()
        self.entities = []
        self.polymers, self.nonpolymers = self.__split_entities()

        for p in self.polymers:
            seq = self.__get_atom_site_seq(p)
            entity = Entity(p, seq)
            self.entities.append(entity)
            self.__get_chains(entity)

    def __get_mmcif(self):
        self.mmcif = cif_handling.mmcifHandling(fileName=self.__mmcif_file)
        parsed = self.mmcif.parse_mmcif()
        #infile = mmcifIO.CifFileReader(input="data", preserve_order=True)
        #f = infile.read(self.__mmcif_file, output="cif_file", ignore=[])
        return parsed

    def __split_entities(self):
        cat = self.get_category("entity")
        types = self.get_category_items(category=cat, item="type")
        poly = []
        nonpoly = []

        for idx, t in enumerate(types):
            if t == "polymer":
                poly.append(self.get_category_items(category=cat, item="id")[idx])
            else:
                nonpoly.append(self.get_category_items(category=cat, item="id")[idx])

        return (poly, nonpoly)

    def __get_chains(self, entity):
        cat = self.get_category("atom_site")
        entities = self.get_category_items(category=cat, item="label_entity_id")
        chains = []

        for idx, e in enumerate(entities):
            if e == entity.entity_id:
                asym = self.get_category_items(category=cat, item="label_asym_id")[idx]
                auth = self.get_category_items(category=cat, item="auth_asym_id")[idx]

                if (asym, auth) not in chains:
                    chains.append((asym, auth))

        for asym, auth in chains:
            c = Chain(auth, asym, entity.entity_id, None)
            c.seq = entity.seq
            entity.chains.append(c)

        return

    def __get_atom_site_seq(self, entity):
        cat = self.get_category("atom_site")
        entities = self.get_category_items(category=cat, item="label_entity_id")
        seq = {}

        for idx, e in enumerate(entities):
            if e != entity:
                continue

            seq_id = int(self.get_category_items(category=cat, item="label_seq_id")[idx])

            if seq_id not in seq.keys():
                threeL = self.get_category_items(category=cat, item="label_comp_id")[idx]
                if threeL in residue_map_3to1:
                    seq[seq_id] = residue_map_3to1[threeL]
                else:
                    seq[seq_id] = "X"

        return "".join([seq[key] for key in sorted(seq.keys())])

    def get_category(self, category):
        return self.mmcif.getCategory(category=category)
        #for db in self.mmcif.getDataBlocks():
        #    if category in db.getCategoryIds():
        #        return db.getCategory(category)
        #return None

    def get_category_items(self, category, item):
        return self.mmcif.getCatItemValues(category=category, item=item)

    def set_category(self, data_dictionary):
        self.mmcif.addToCif(data_dictionary=data_dictionary)

    #def set_category_items(self, category, item, values):
    #    self.mmcif.addValuesToCategory

    def remove_category(self, category):
        self.mmcif.removeCategory(category=category)

    def write(self, fname):
        self.mmcif.writeCif(fileName=fname)
        #outfile = mmcifIO.CifFileWriter(fname)
        #outfile.write(self.mmcif)

def first_available(entities):
    for idx in range(1, 100000):
        if idx not in entities:
            return idx

    return None

def get_seq_alias_map(aliases, mmcif):
    out = {}

    # get non-polymers only
    _, entities = split_entities(mmcif)

    for a in aliases:
        if a not in out:
            ent = first_available(entities)
            entities.append(ent)
            out[a] = ent

    return out

def pretty_print(data):
    padding = 2
    col_width = max(len(word) for row in data for word in row) + padding

    for row in data:
        print("".join(word.ljust(col_width) for word in row))

