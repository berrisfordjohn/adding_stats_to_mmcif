import logging
import tempfile
import os
import shutil

logger = logging.getLogger()
FORMAT = "%(filename)s - %(funcName)s - %(message)s"
logging.basicConfig(format=FORMAT)

from .add_sequence_to_mmcif import AddSequenceToMmcif
from .add_data_from_aimless_xml import run_process as addDataToMmcif
from .add_software_to_mmcif import AddSoftwareToMmcif


def run_process(input_mmcif, output_mmcif, fasta_file, xml_file=None, software_file=None):

    worked = True

    if os.path.exists(input_mmcif):
        run_dir = tempfile.mkdtemp()
        temp_cif = os.path.join(run_dir, 'temp.cif')
        if xml_file:
            worked = addDataToMmcif(xml_file=xml_file, input_cif=input_mmcif, output_cif=temp_cif)
            if not worked:
                logging.error('adding statistics to mmCIF failed')
        else:
            shutil.copy(input_mmcif, temp_cif)

        if worked:
            worked = AddSequenceToMmcif(input_mmcif=temp_cif,
                                        output_mmcif=output_mmcif,
                                        fasta_file=fasta_file).process_data()
            if not worked:
                logging.error('adding sequence to mmCIF failed')

        if worked:
            if software_file:
                worked = AddSoftwareToMmcif(input_cif=output_mmcif,
                                            output_cif=output_mmcif,
                                            software_file=software_file).run_process()
                if not worked:
                    logging.error('adding software to mmCIF failed')

        if worked:
            shutil.rmtree(run_dir)
    else:
        logging.error('unable to access input mmcif file')
        worked = False

    return worked
