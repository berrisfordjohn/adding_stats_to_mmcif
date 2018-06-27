#!/usr/bin/env python

class Entity(object):
    def __init__(self, entity_id, seq, chains=None):
        super(Entity, self).__init__()
        self.entity_id = entity_id
        self.old_entity_id = [self.entity_id]
        self.seq = seq
        self.fasta_seq = None
        self.seq_alias = None

        if chains:
            if isinstance(chains, list):
                self.chains = chains
            else:
                self.chains = [chains]
        else:
            self.chains = []

    def __repr__(self):
        out = ("entity_id: %s\n"
               "old_entity_id: %s\n"
               "seq_alias: %s\n"
               "fasta_seq: %s\n\t"
               % (self.entity_id, self.old_entity_id, self.seq_alias, self.fasta_seq))

        for c in self.chains:
            out += "-" * 50 + "\n\t"
            out += str(c).replace("\n", "\n\t")

        # Remove the last \t
        return out[:-1]

    def modified(self):
        return self.entity_id != self.old_entity_id

    def dnarna(self):
        return set(self.seq).issubset(set("AUGC")) or set(self.seq).issubset(set("ATGC"))
