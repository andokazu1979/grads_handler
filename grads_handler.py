#! /usr/bin/env python

import sys
import logging
import subprocess
import datetime

from toml_parser import TOMLParser
from script_maker import ScriptMakerGrADS
from list_stream import ListStream

def execute_cmd(lst_cmd, shell=False):
    try:
        ret = subprocess.check_output(lst_cmd, shell)
        logger.debug(ret)
    except subprocess.CalledProcessError as e:
        print("*** Error occured in processing command! ***")
        print("Return code: {0}".format(e.returncode))
        print("Command: {0}".format(e.cmd))
        print("Output: {0}".format(e.output))
        raise e

parser = TOMLParser()
args = sys.argv
if len(args) == 1:
    raise Exception("Specify configuration file!")
elif len(args) >= 3:
    raise Exception("Too many configuration files is specified!")
parser.parse(sys.argv[1])
conf = parser.dict_root
calc_pattern = conf['global']['calc_pattern']
loglevel = conf['global']['loglevel']

if loglevel == 'DEBUG':
    level_ = logging.DEBUG
elif loglevel == 'INFO':
    level_ = logging.INFO
elif loglevel == 'WARNING':
    level_ = logging.WARNING
elif loglevel == 'ERROR':
    level_ = logging.ERROR
elif loglevel == 'CRITCAL':
    level_ = logging.CRITCAL

logging.basicConfig(level = level_)
logger = logging.getLogger(__name__)
logger.info(calc_pattern)

calc = conf[calc_pattern]
exec_cond = calc['exec_cond']
figure_cond = calc['figure_cond']

dirpath_in = figure_cond['dirpath_in']
dirpath_out = figure_cond['dirpath_out']
header = figure_cond['header']

lst_exec_cond = exec_cond.values()

for lst in ListStream.get_comb(lst_exec_cond):
    logger.info(lst)

    lev = lst[-1].replace('hPa', '')
    varname = lst[-2]

    script_maker = ScriptMakerGrADS(calc, './mk_figure.gs', lev, varname)
    stringitem = figure_cond[lev][varname][0]['stringitem']

    indir = '{0}/'.format(dirpath_in)
    outdir = '{0}/'.format(dirpath_out)
    for item in lst[:-2]:
        indir += '{0}/'.format(item)
    for item in lst:
        outdir += '{0}/'.format(item)

    logger.debug('indir = {0}'.format(indir))
    logger.debug('outdir = {0}'.format(outdir))
    
    execute_cmd(['mkdir', '-p', outdir])
    
    dt_sta = datetime.datetime.strptime(calc['dt_sta'], '%Y%m%d%H')
    dt_end = datetime.datetime.strptime(calc['dt_end'], '%Y%m%d%H')
    delta_in_hour = calc['delta_in_hour']
    dt = dt_sta
    while dt <= dt_end:
        logger.info(dt)
        script_maker.output(indir, outdir, string='[{0}]'.format(stringitem), tstr=dt.strftime('%HZ%d%b%Y'))
        execute_cmd(['grads', '-blc', 'mk_figure.gs'])
        dt += datetime.timedelta(hours=delta_in_hour)
