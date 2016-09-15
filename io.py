__author__ = 'Tom Yan'

import csv

def export_csv(filename, rows):
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
