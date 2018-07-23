from onedep import __apiUrl__
from onedep.api.Validate import Validate
import time
import os
import argparse
import logging

logger = logging.getLogger()
FORMAT = "%(filename)s - %(funcName)s - %(message)s"
logging.basicConfig(format=FORMAT)


def display_status(sD, exitOnError=True):
    if 'onedep_error_flag' in sD and sD['onedep_error_flag']:
        logging.error("OneDep error: %s\n" % sD['onedep_status_text'])
        if exitOnError:
            raise SystemExit()
    else:
        if 'status' in sD:
            logging.info("OneDep status: %s\n" % sD['status'])


def main(model_file_path, sf_file_path, api_input_url=None):
    # Given:
    # modelFilePath contains the path to the model file
    # sfFilePath contains the path to the structure factor file
    if api_input_url:
        api_url = api_input_url
    else:
        api_url = __apiUrl__
    val = Validate(apiUrl=api_url)
    ret = val.newSession()
    display_status(ret)
    ret = val.inputModelXyzFile(model_file_path)
    display_status(ret)
    ret = val.inputStructureFactorFile(sf_file_path)
    display_status(ret)
    ret = val.run()
    display_status(ret)
    #
    #   Poll for service completion -
    #
    it = 0
    sl = 2
    val_status = None
    while True:
        #    Pause -
        it += 1
        pause = it * it * sl
        time.sleep(pause)
        ret = val.getStatus()
        if ret['status'] in ['completed', 'failed']:
            val_status = ret['status']
            logging.info('validation {}'.format(val_status))
            break
        logging.info("[%4d] Pausing for %4d (seconds)\n" % (it, pause))
        #
        #
    lt = time.strftime("%Y%m%d%H%M%S", time.localtime())
    file_name_of_report = "xray-report-{}.pdf".format(lt)
    file_name_of_logfile = "xray-report-{}.log".format(lt)
    if val_status == 'completed':
        logging.info('getting validation report')
        ret = val.getReport(file_name_of_report)
        display_status(ret)
        logging.debug('getting report status: {}'.format(ret))
        if os.path.exists(file_name_of_report):
            return True, file_name_of_report
    else:
        logging.error('validation run status: {}'.format(val_status))
        ret = val.getReportLog(file_name_of_logfile)
    return False, file_name_of_logfile


if '__main__' == __name__:
    parser = argparse.ArgumentParser()
    parser.add_argument('--input_mmcif', help='input mmcif model file', type=str, required=True)
    parser.add_argument('--input_sf_file', help='input sf file', type=str, required=True)
    parser.add_argument('--api_url', help='input api url', type=str)
    parser.add_argument('-d', '--debug', help='debugging', action='store_const', dest='loglevel', const=logging.DEBUG,
                        default=logging.INFO)

    args = parser.parse_args()

    logger.setLevel(args.loglevel)

    worked, report = main(sf_file_path=args.input_sf_file, model_file_path=args.input_mmcif, api_input_url=args.api_url)
    logging.info('worked: {}'.format(worked))
