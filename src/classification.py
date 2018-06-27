#!/usr/bin/env python
# encoding: utf-8

import sys
import os
import re
import traceback
import logging
from itertools import groupby
import lxml
from lxml import etree
import urllib2
#from Bio import pairwise2
from mmcif_helper import MMCIF_Poly
from mmcif_helper import residue_map_1to3

from Bio import AlignIO
from Bio.Emboss.Applications import NeedleCommandline
import cStringIO

import argparse

logger = logging.getLogger()

needle_cline = NeedleCommandline()
#needle_cline.gapopen = 0.5
#needle_cline.gapextend = 0.1
needle_cline.gapopen = 10
needle_cline.gapextend = 0.5
#needle_cline.stdout = True
needle_cline.outfile = "stdout"

def do_alignment_emboss(seq1, seq2):
    needle_cline.asequence = "asis:" + seq1
    needle_cline.bsequence = "asis:" + seq2
    stdout, stderr = needle_cline()
    
    return [AlignIO.read(cStringIO.StringIO(stdout), "emboss")]

def get_score(seq1, seq2):
    return sum(aa1 == aa2 for aa1, aa2 in zip(seq1, seq2))

def dnarna(seq):
    return set(seq).issubset(set("AUGC")) or set(seq).issubset(set("ATGC"))

def get_refmac(root):
    return root.xpath("//refmac/file/text()")[0]

def get_sequences(xml_root):
    seqs = []
    elem = xml_root.xpath("//sequences/sequence")

    for e in elem:
        seq_file = e.xpath("file/text()")[0]
        seq_alias = e.xpath("seq_alias/text()")[0]
        with open(os.path.join(SRC_PATH, seq_file), "r") as f_seq:
            seq = f_seq.read()
        seq = seq[seq.find("\n"):].replace("\n", "").replace(" ", "")
        seqs.append((seq_alias, seq))

    return seqs

def assign_fasta_seq(entities):
    for e in entities:
        best_seq = (None, [None, None, 0])

        for alias, fasta in fasta_seqs:
            # They have to be the same thing before trying alignment
            if dnarna(fasta) != dnarna(e.seq):
                continue

            alns = do_alignment_emboss(fasta, e.seq)[0]

            score = get_score(alns[0].seq, alns[1].seq)

            # buggy implementation. Useless!
            #alns = pairwise2.align.globalxx(fasta, e.seq)[0]

            if score > best_seq[1][2]:
                best_seq = (alias, (alns[0].seq, alns[1].seq, score))

        if best_seq[1][2] == 0:
            logging.info("The sequence:\n%s\nWas impossible to align" % e.seq)
            continue

        e.fasta_seq = best_seq[1][0]
        e.seq_alias = best_seq[0]

        for chain in e.chains:
            chain.identity_global = (float(best_seq[1][2]) / len(best_seq[1][0]))
            chain.identity_local = (float(best_seq[1][2]) / len(best_seq[1][1].strip("-")))

def rename_dup_chains(entities):
    for e in entities:
        sorted_input = sorted(e.chains, key=lambda x: x.chain_id)

        for _, g in groupby(sorted_input, key=lambda x: x.chain_id):
            g = list(g)

            if len(g) > 1:
                for ch in g[1:]:
                    curr = set([x.chain_id for x in e.chains])

                    while ch.chain_id in curr:
                        ch.chain_id += 'X'

def unify_entities(mmcif):
    """ Unifies entities and chains within the MMCIF_Poly object

    @param mmcif The MMCIF_Poly object

    """
    sorted_input = sorted([e for e in mmcif.entities if e.seq_alias is not None], key=lambda x: x.seq_alias)
    # Add the ones that couldn't be aligned 
    replacement = [e for e in mmcif.entities if e.seq_alias is None]


    for _, g in groupby(sorted_input, key=lambda x: x.seq_alias):
        g = list(g)
        ent0 = g[0]
        ent0.old_entity_id = [x.entity_id for x in g]
        ent0.entity_id = str(min([int(x.entity_id) for x in g]))
        ent0.seq = ent0.fasta_seq

        for ent in g[1:]:
            ent0.chains += ent.chains

        for ch in ent0.chains:
            ch.entity_id = ent0.entity_id

        replacement.append(ent0)

    rename_dup_chains(replacement)
    mmcif.entities = replacement

def complete_xml(xml, entities):
    """ Appends both entities and chains to a xml file

    @param xml A lxml ElementTree object
    @param entities A list of Entity objects

    """
    xml_entities = etree.SubElement(xml, "entities")

    for ent in entities:
        xml_ent = etree.SubElement(xml_entities, "entity")
        xml_ent.attrib["entity_id"] = ent.entity_id
        xml_ent.attrib["old_entity_id"] = ",".join(ent.old_entity_id)
        xml_ent.attrib["seq_alias"] = ent.seq_alias if ent.seq_alias is not None else "None"

        xml_chains = etree.SubElement(xml_ent, "chains")
        for chain in ent.chains:
            xml_ch = etree.SubElement(xml_chains, "chain")
            xml_ch.attrib["chain_id"] = chain.chain_id
            xml_ch.attrib["old_chain_id"] = chain.old_chain_id
            xml_ch.attrib["struct_asym_id"] = chain.struct_asym_id
            xml_ch.attrib["old_entity_id"] = chain.old_entity_id
            xml_ch.attrib["identity_local"] = "%.2f" % chain.identity_local
            xml_ch.attrib["identity_global"] = "%.2f" % chain.identity_global

def fix_entity(mmcif_poly):
    cat = mmcif_poly.get_category("entity")

    if cat is None:
        return False

    for it in [it for it in cat.getItemNames() if it not in ("type", "id")]:
        cat.removeChild(it)

    idx = 0

    while idx < len(cat.getItem("type").value):
        if cat.getItem("type").value[idx] == "polymer":
            del cat.getItem("type").value[idx]
            del cat.getItem("id").value[idx]
        else:
            idx += 1

    for e in mmcif_poly.entities:
        cat.getItem("type").setValue("polymer")
        cat.getItem("id").setValue(e.entity_id)

    return True

def fix_entity_poly_seq(mmcif_poly):
    category = 'entity_poly_seq'
    #cat = mmcif_poly.get_category("entity_poly_seq")

    mmcif_poly.remove_category(category=category)

    #if cat is None:
    #    return False

    #db = cat.parent
    #cat.remove()
    cat_dict = dict()
    for item in ['entity_id', 'num', 'mon_id', 'hetero']:
        cat_dict.setdefault(category, {})[item] = [] * len(mmcif_poly.entities)


    #cat = db.setCategory("entity_poly_seq")
    #cat.setItem("entity_id")
    #cat.setItem("num")
    #cat.setItem("mon_id")
    #cat.setItem("hetero")

    for e in mmcif_poly.entities:
        dnarna = e.dnarna()

        idx = 1

        for r in e.seq:
            if r == 'X':
                cat.getItem("mon_id").setValue("UNK")
                cat.getItem("hetero").setValue("y")
                cat.getItem("entity_id").setValue(e.entity_id)
                cat.getItem("num").setValue(idx)
            elif dnarna:
                cat.getItem("mon_id").setValue(r)
                cat.getItem("hetero").setValue("n")
                cat.getItem("entity_id").setValue(e.entity_id)
                cat.getItem("num").setValue(idx)
            elif r in residue_map_1to3:
                cat.getItem("mon_id").setValue(residue_map_1to3[r])
                cat.getItem("hetero").setValue("n")
                cat.getItem("entity_id").setValue(e.entity_id)
                cat.getItem("num").setValue(idx)
            else:
                traceback.print_stack()
                logging.info("Residue UNKNOWN!: |%s|" % r)
                sys.exit(1)

            idx += 1

    return True

def fix_atom_site(mmcif_poly):
    category = 'atom_site'
    cat = mmcif_poly.get_category(category)

    if cat is None:
        return False

    for e in mmcif_poly.entities:
        if not e.modified():
            continue

        #entities = cat.getItem("label_entity_id").value
        entities = mmcif_poly.get_category_items(category=category, item='label_entity_id')

        idx = 0

        while idx < len(entities):
            if entities[idx] in e.old_entity_id:
                entities[idx] = e.entity_id
            idx += 1
        

        for ch in e.chains:
            if not ch.modified():
                continue

            chains = cat.getItem("auth_asym_id").value
            labels = cat.getItem("label_asym_id").value

            idx = 0

            while idx < len(chains):
                if labels[idx] == ch.struct_asym_id:
                    chains[idx] = ch.chain_id
                idx += 1

    return True

def add_entity_poly(mmcif_poly):
    entities = mmcif_poly.entities

    category = "entity_poly"
    #cat = mmcif_poly.get_category("entity_poly")

    # Remove if it exists
    mmcif_poly.remove_category("entity_poly")
    
    # Add in the same block as entity
    #db = mmcif_poly.get_category("entity").parent
    #cat = db.setCategory("entity_poly")
    #cat.setItem("entity_id")
    #cat.setItem("pdbx_seq_one_letter_code_can")
    #cat.setItem("pdbx_seq_one_letter_code")

    cat_dict = dict()
    for item in ['entity_id', 'pdbx_seq_one_letter_code_can', 'pdbx_seq_one_letter_code']:
        cat_dict.setdefault(category, {})[item] = [''] * len(entities)

    for i, value in enumerate(entities):
        cat_dict[category]['entity_id'][i] = entities[i].entity_id
        #cat.getItem("entity_id").setValue(entities[i].entity_id)
        noncan = ""
        dnarna = entities[i].dnarna()

        for r in entities[i].seq:
            if r == 'X':
                # TODO: Residue library needed
                noncan += "(X)"
            elif dnarna:
                noncan += r
            elif r in residue_map_1to3:
                noncan += r
            else:
                traceback.print_stack()
                logging.error("Residue UNKNOWN!")
                sys.exit(1)

        #cat.getItem("pdbx_seq_one_letter_code").setValue("\n".join(re.findall(".{80}|.+$", noncan)))
        #cat.getItem("pdbx_seq_one_letter_code_can").setValue("\n".join(re.findall(".{80}|.+$", str(entities[i].seq))))
        cat_dict[category]['pdbx_seq_one_letter_code'][i] = "\n".join(re.findall(".{80}|.+$", noncan))
        cat_dict[category]['pdbx_seq_one_letter_code_can'][i] = "\n".join(re.findall(".{80}|.+$", str(entities[i].seq)))
    mmcif_poly.set_category(data_dictionary=cat_dict)

def add_pdbx_non_poly_scheme(mmcif_poly):
    cat = mmcif_poly.get_category("pdbx_non_poly_scheme")

    # Remove if it exists
    if cat is not None:
        cat.remove()

    # Add in the same block as entity
    db = mmcif_poly.get_category("entity").parent
    cat = db.setCategory("pdbx_non_poly_scheme")
    cat.setItem("asym_id")
    cat.setItem("entity_id")
    cat.setItem("mon_id")
    cat.setItem("ndb_seq_num")
    cat.setItem("pdb_seq_num")
    cat.setItem("auth_seq_num")
    cat.setItem("pdb_mon_id")
    cat.setItem("auth_mon_id")
    cat.setItem("pdb_strand_id")
    cat.setItem("pdb_ins_code")

    atom = mmcif_poly.get_category("atom_site")
    ent = atom.getItem("label_entity_id")

    for idx, e in enumerate(ent.value):
        if e in mmcif_poly.nonpolymers:
            cat.getItem("asym_id").setValue(atom.getItem("label_asym_id").value[idx])
            cat.getItem("entity_id").setValue(atom.getItem("label_entity_id").value[idx])
            cat.getItem("mon_id").setValue(atom.getItem("label_comp_id").value[idx])
            cat.getItem("ndb_seq_num").setValue(atom.getItem("label_seq_id").value[idx])
            cat.getItem("pdb_seq_num").setValue(atom.getItem("pdbx_PDB_residue_no").value[idx])
            cat.getItem("auth_seq_num").setValue(atom.getItem("auth_seq_id").value[idx])
            cat.getItem("pdb_mon_id").setValue(atom.getItem("pdbx_PDB_residue_name").value[idx])
            cat.getItem("auth_mon_id").setValue(atom.getItem("auth_comp_id").value[idx])
            cat.getItem("pdb_strand_id").setValue(atom.getItem("auth_asym_id").value[idx])
            cat.getItem("pdb_ins_code").setValue(atom.getItem("pdbx_PDB_ins_code").value[idx])


def download_fasta(acc, output_dir):
    url = "http://www.uniprot.org/uniprot/%s.fasta" % acc

    logging.info("Downloading FASTA file for %s" % acc)

    try:
        raw = urllib2.urlopen(url).read()
    except Exception as e:
        logging.info(e)
        logging.info("Can't download the FASTA file for %s" % acc)
        return False

    try:
        f = open(os.path.join(output_dir, "%s.fasta" % acc), 'w')
        f.write(raw)
        f.close()
    except Exception as e:
        logging.info(e)
        logging.info("Can't write the FASTA file for %s" % acc)
        return False

    return True


def create_xml(mmcif, accessions, output_dir):
    merge = etree.Element("merging")
    doc = etree.ElementTree(merge)
    refmac = etree.SubElement(merge, "refmac")
    fi = etree.SubElement(refmac, "file")
    fi.text = mmcif

    seqs = etree.SubElement(merge, "sequences")

    f = open(accessions, 'r')

    for acc in f.readlines():
        acc = acc.strip()

        if download_fasta(acc.strip(), output_dir):
            seq = etree.SubElement(seqs, "sequence")
            alias = etree.SubElement(seq, "seq_alias")
            alias.text = acc
            fi = etree.SubElement(seq, "file")
            fi.text = acc + ".fasta"
            fo = etree.SubElement(seq, "file")
            fo.text = "fasta"

    f.close()

    xml_file = mmcif.rsplit(os.path.extsep, 1)[0] + ".xml"
    doc.write(os.path.join(output_dir, xml_file), pretty_print=True)

    return xml_file

parser = argparse.ArgumentParser()
group = parser.add_mutually_exclusive_group(required=True)
group.add_argument("-x", "--xml", nargs=1, required=False, help='The input XML file.')
group.add_argument("-m", "--mmcif", nargs=1, required=False, help='The input mmCIF file.')
parser.add_argument("-l", "--list", nargs=1, help='The file with the list of UniProt accessions or gene names. It is required when using -m/--mmcif')
parser.add_argument('-d', '--debug', help='debugging', action='store_const', dest='loglevel', const=logging.DEBUG,
                        default=logging.INFO)

args = parser.parse_args()
logger.setLevel(args.loglevel)

if args.xml:
    logging.info("Running in XML mode")
    xml_file = args.xml[0]
# if --xml doesn't exist then --mmcif does
elif args.list:
    logging.info("Running in mmCIF mode")
    mmcif_fname = os.path.basename(args.mmcif[0])
    output_dir = os.path.dirname(os.path.realpath(args.mmcif[0]))
    xml_file = create_xml(mmcif_fname, args.list[0], output_dir)
    xml_file = os.path.join(output_dir, xml_file)
else:
    logging.info("The flag -l is required when using mmCIF mode (-m/--mmcif).")
    parser.print_help()
    sys.exit(1)

XML_OUT = os.path.basename(xml_file).rsplit(os.path.extsep, 1)[0] + "_out.xml"

parser = etree.XMLParser(ns_clean=True, remove_blank_text=True)

try:
    xml = etree.parse(xml_file, parser).getroot()
except lxml.etree.XMLSyntaxError as e:
    logging.info("Problem parsing the XML file")
    logging.info(e)
    sys.exit(1)

# this path is relative to the location of the XML file
mmcif_file = get_refmac(xml)

# dirname of the abspath of the XML file
SRC_PATH = os.path.dirname(os.path.abspath(xml_file))
mmcif_file = os.path.join(SRC_PATH, mmcif_file)

CIF_OUT = os.path.join(
    SRC_PATH,
    os.path.basename(mmcif_file).rsplit(os.path.extsep, 1)[0] + "_out.cif"
    )

mmcif = MMCIF_Poly(mmcif_file)

fasta_seqs = get_sequences(xml)

assign_fasta_seq(mmcif.entities)

for e in mmcif.entities:
    logging.info(e)

unify_entities(mmcif)

logging.info("*" * 50)
logging.info("AFTER")
logging.info("*" * 50)

for e in mmcif.entities:
    logging.info(e)

complete_xml(xml, mmcif.entities)

f = open("%s" % (os.path.join(SRC_PATH, XML_OUT)), "w")
f.write(
    etree.tostring(
        xml,
        xml_declaration=True,
        standalone='Yes',
        encoding="UTF-8",
        pretty_print=True
        )
    )
f.close()

fix_entity(mmcif)
#fix_entity_poly_seq(mmcif)
add_entity_poly(mmcif)
#add_pdbx_non_poly_scheme(mmcif)
fix_atom_site(mmcif)

mmcif.write(CIF_OUT)

