import logging
import tempfile
import os
import shutil

logger = logging.getLogger()
FORMAT = "%(filename)s - %(funcName)s - %(message)s"
logging.basicConfig(format=FORMAT)

from .add_sequence_to_mmcif import AddSequenceToMmcif
from .add_data_from_aimless_xml import run_process as addDataToMmcif
from .wwpdb_validation_api import run_validation_api


def run_process(input_mmcif, output_mmcif, fasta_file, xml_file=None, sf_file=None, validation_report=None):

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

            if sf_file and validation_report:
                worked, output_file = run_validation_api(model_file_path=output_mmcif, sf_file_path=sf_file,
                                                         output_file_name=validation_report)
                if not worked:
                    logging.error('validation run failed, see: {}'.format(output_file))

        if worked:
            shutil.rmtree(run_dir)
    else:
        logging.error('unable to access input mmcif file')
        worked = False

    return worked
