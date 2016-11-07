# -*- coding: utf-8 -*-

import pandas as pd
import logging
import os

def resample_sequences(seq_base_file=None, output_path=None,
                       samples=None, file_prefix=None):
    """
    This function is for resampling the sequence csv-data file. The files are
    read  from the specified directory, resampled and, written back to the
    directory. Note that the sequence files are expected to have a timeindex
    column that can be parsed by pandas, with entries like:
    '2014-01-01 00:00:00+00:00'


    Parameters
    ----------
    seq_path : string
        Path of the directory with sequence files. NOTE: Only files with
        *seq.csv are considere for resampling.
    output_path : string
        File for resampled seq-files. If no path is specified, attr:`seq_path`
        will be used.
    samples : list
        List of strings with the resampling rate e.g. ['4H', '2H']. See
        `pandas.DataFrame.resample` method for more information on format.
    file_prefix : string
        String that is put as prefix of the file name, i.e. filename is created
        by: file_prefix+freq+'_seq.csv'
    """
    if samples is None :
        raise ValueError('Missing sample attribute. Please specifiy!')
    if output_path is None:
        logging.info("No output_path specified, setting output_path to seq_path!")
        output_path = seq_base_file

    if not os.path.exists(output_path):
            os.makedirs(output_path, exist_ok=True)

    seq_path, seq_file = os.path.split(seq_base_file)

    # read the file and parse the dates from the first column (index 0)
    seq = pd.read_csv(os.path.join(seq_path, seq_file),
                      header=[0, 1, 2, 3, 4], parse_dates=[0])

    # store the first column name for reuse
    first_col = seq.columns[0]
    # set the index as datetimeindex from column with parsed dates
    seq.index = seq[first_col]
    # set timeindex

    # convert columns to numeric values, except the datetimecolumn, but!
    # which we keep for reuse
    for col in seq:
        if col == first_col:
            seq[col] = -999999
        else:
            seq[col] = seq[col].astype(float)

    #pdb.set_trace()
    for s in samples:
    # resample dataframes
        seq_sampled = seq.resample(s).mean()
        # assign the resampled datetimeindex values to the first columns,
        # replacing the -999999
        seq_sampled[first_col] = seq_sampled.index
        if file_prefix is None:
            file_prefix = seq_file.split('seq')[0]
            logging.info('Setting filename prefix to: {}'.format(file_prefix))

        filename = os.path.join(output_path, file_prefix+s+'_seq.csv')
        logging.info('Writing sample file to {0}.'.format(filename))
        seq_sampled.to_csv(filename, index=False)
    return seq_sampled

if  __name__ == "__main__":
    samples = ['2H', '3H']
    resample_sequences(samples=samples)
