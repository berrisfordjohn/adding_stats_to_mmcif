import logging
import tempfile
import os
import shutil

logger = logging.getLogger()
FORMAT = "%(filename)s - %(funcName)s - %(message)s"
logging.basicConfig(format=FORMAT)

from .add_sequence_to_mmcif import AddSequenceToMmcif
from .add_data_from_aimless_xml import run_process as addAimlessDataToMmcif
from .add_data_from_mmcif import AddToMmcif


def run_process(input_mmcif, output_mmcif, fasta_file, xml_file=None, input_mmcif_to_get_data_from=None):

    worked = True

    if os.path.exists(input_mmcif):
        run_dir = tempfile.mkdtemp()
        temp_cif = os.path.join(run_dir, 'temp.cif')
        if xml_file:
            worked = addAimlessDataToMmcif(xml_file=xml_file, input_cif=input_mmcif, output_cif=temp_cif)
            if not worked:
                logging.error('adding statistics to mmCIF failed')
        elif input_mmcif_to_get_data_from:
            ac = AddToMmcif()
            data = ac.get_data(input_mmcif_to_get_data_from)
            if data:
                worked = ac.add_to_cif(input_mmcif_file=input_mmcif, output_mmcif_file=temp_cif, data_dictionary=data)
        else:
            shutil.copy(input_mmcif, temp_cif)

        if worked:
            worked = AddSequenceToMmcif(input_mmcif=temp_cif,
                                        output_mmcif=output_mmcif,
                                        fasta_file=fasta_file).process_data()
            if not worked:
                logging.error('adding sequence to mmCIF failed')

        if worked:
            shutil.rmtree(run_dir)
    else:
        logging.error('unable to access input mmcif file')
        worked = False

    return worked
