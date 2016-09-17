__author__ = 'Tom Yan'

import csv
import json
from collections import OrderedDict

def csv_export(filename, rows):
    """
    Export given rows to csv file
    :param filename:
    :param rows:
    :return:
    """
    if not filename or not rows:
        return

    with open(filename, 'wb') as f:
        f_writer = csv.writer(f)
        f_writer.writerows(rows)

def json_load(fname):
    """ JSON ordered load
    """
    try:
        with open(fname, 'r') as fstream:
            # return json.load(fstream, object_pairs_hook=OrderedDictStr, encoding="utf-8")
            return json.load(fstream, object_pairs_hook=OrderedDict, encoding="utf-8")

    except EnvironmentError:
        print 'JSON file load error:', fname
        return None

def json_export(data, fname, **kwds):
    """
    Export to json format
    """
    try:
        with open(fname, 'w') as fstream:
            if kwds and 'indent' in kwds:
                json.dump(data, fstream, **kwds)
            else:
                json.dump(data, fstream, indent=2, **kwds)
            return 0
    except (EnvironmentError, ValueError, TypeError) as xcp1:
        print 'JSON file export error:', str(xcp1), ' in', fname
        return -1
