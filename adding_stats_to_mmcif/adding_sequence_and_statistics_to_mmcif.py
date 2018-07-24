import argparse
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
    run_dir = tempfile.mkdtemp()
    temp_cif = os.path.join(run_dir, 'temp.cif')

    worked = True

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

    return worked


if __name__ == '__main__':  # pragma: no cover
    parser = argparse.ArgumentParser()
    parser.add_argument('--xml_file', help='input xml file', type=str)
    parser.add_argument('--output_mmcif', help='output mmcif file', type=str, required=True)
    parser.add_argument('--input_mmcif', help='input mmcif file', type=str, required=True)
    parser.add_argument('--fasta_file', help='input fasta file', type=str)
    parser.add_argument('--sf_file', help='input structure factor file', type=str)
    parser.add_argument('-d', '--debug', help='debugging', action='store_const', dest='loglevel', const=logging.DEBUG,
                        default=logging.INFO)

    args = parser.parse_args()
    logger.setLevel(args.loglevel)

    complete = run_process(input_mmcif=args.input_mmcif, output_mmcif=args.output_mmcif, fasta_file=args.fasta_file,
                    xml_file=args.xml_file, sf_file=args.sf_file)
    logging.info('worked: {}'.format(complete))
