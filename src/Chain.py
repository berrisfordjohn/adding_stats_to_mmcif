#!/usr/bin/env python

#from mmcif_helper import *

class Chain(object):
    def __init__(self, chain_id, struct_asym_id, entity_id, seq_alias):
        super(Chain, self).__init__()
        self.chain_id = chain_id
        self.old_chain_id = self.chain_id
        self.struct_asym_id = struct_asym_id
        self.entity_id = entity_id
        self.old_entity_id = self.entity_id
        self.seq_alias = seq_alias
        self.seq_file = None
        self.seq_format = None
        self.seq = None
        self.identity_local = 0.0
        self.identity_global = 0.0

    def __repr__(self):
        out = ("chain_id: %s\n"
               "old_chain_id: %s\n"
               "entity_id: %s\n"
               "old_entity_id: %s\n"
               "struct_asym_id: %s\n"
               "seq_alias: %s\n"
               "seq_file: %s\n"
               "seq_format: %s\n"
               "seq: %s\n"
               "identity_local: %f\n"
               "identity_global: %f\n"
               % (self.chain_id,\
               self.old_chain_id,\
               self.entity_id,\
               self.old_entity_id,\
               self.struct_asym_id,\
               self.seq_alias,\
               self.seq_file,\
               self.seq_format,\
               self.seq,\
               self.identity_local,\
               self.identity_global))

        return out

    def read_fasta(self, xml_root):
        # Find the sequence with the same alias and extract all the good stuff
        seq = xml_root.xpath("//sequences/sequence/seq_alias[text()='"+self.seq_alias+"']/..")[0]
        self.seq_file = seq.xpath("file/text()")[0]
        self.seq_format = seq.xpath("format/text()")[0]

        self.seq = open(self.seq_file, "r").read()
        self.seq = self.seq[self.seq.find("\n"):].replace("\n", "").replace(" ", "")

    #def get_entity(self, cif_file):
    #    cat = get_category(cif_file, "atom_site")
    #    auth = cat.getItem("auth_asym_id")
    #    ent = cat.getItem("label_entity_id")

    #    for i in range(len(auth.value)):
    #        if auth.value[i] == self.chain_id:
    #            self.entity_id = ent.value[i]
    #            break
    #    return

    def modified(self):
        return (
                self.chain_id != self.old_chain_id
                or
                self.entity_id != self.old_entity_id
                )
