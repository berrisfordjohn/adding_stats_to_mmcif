import argparse
import logging
from adding_stats_to_mmcif import run_process

logger = logging.getLogger()
FORMAT = "%(filename)s - %(funcName)s - %(message)s"
logging.basicConfig(format=FORMAT)

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
