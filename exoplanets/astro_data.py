# -*- coding: utf-8 -*-

""" Functions to get table and light curves data using astroquery. """

import logging
import os

import pandas as pd
from astroquery.nasa_exoplanet_archive import NasaExoplanetArchive


def read_kepler_data(table, columns=None, where=None, filename=None):
    """ Returns a pandas DataFrame containing the requested data from the
        NasaExoplanetArchive API described in [1].

        :param str table:
            The name of the table in the NasaExoplanetArchive API. The list of tables
            is provided in [1].
        :type columns: list or dict
        :param columns:
            The list, or dict containing the name of the columns to read from the table.
            It is possible to select all columns from the table (columns=["*"]), or
            a subset of the columns (e.g. columns=["dist", "mass"]). If columns is
            None, then the default subset of columns for the table is used if defined
            in DEFAULT_PARAMS. If columns is a dictionary, the keys are pulled from
            the table and are rename into the values in the dictionary.
        :param str where:
            The where filter by which to filter the query (e.g. where="kepid=12345"
            or "st_quarters like '%1%'"). If where is None, then the default
            'where' filter for the table is used if defined in DEFAULT_PARAMS,
            else no filter is applied.
        :param str filename:
            If a filename is provided, the pandas DataFrame is saved in .csv format if
            the file does not exist, and is directly read from the file if it already
            exists.

        :returns pandas.DataFrame:
            The pandas DataFrame containing the requested NasaExoplanetArchive table.

        [1]: https://exoplanetarchive.ipac.caltech.edu/docs/program_interfaces.html
    """
    columns, where = get_default_params(table, columns, where)
    if not filename or not os.path.isfile(filename):
        logging.info("Reading Kepler data from table {}".format(table))
        kepler_data = get_kepler_data(table, columns, where)
        df = kepler_data.to_pandas()
        df = rename_columns(df, columns)
        record_dataframe(df, filename)
    else:
        logging.info("Reading Kepler data from {}".format(filename))
        df = pd.read_csv(filename)
    return df


def get_default_params(table, columns, where):
    """ Returns the default columns and where parameters for the table if specified in
        DEFAULT_PARAMS and if 'columns' and/or 'where' are None.

        :param str table:
            The name of the table.
        :type columns: list or dict
        :param columns:
            The columns to read from the table.
        :param str where:
            The 'where' filter to apply to the table.

        :returns tuple:
            A tuple containing the columns and where parameters.
    """
    if table in DEFAULT_PARAMS:
        columns = DEFAULT_PARAMS[table]["columns"] if not columns else columns
        where = DEFAULT_PARAMS[table]["where"] if not where else where
    return columns, where


def get_kepler_data(table, columns, where):
    """ Returns an astropy table containing the requested data from the
        NasaExoplanetArchive API.

        :param str table:
            The name of the table in the NasaExoplanetArchive API.
        :type columns: list or dict
        :param columns:
            The columns to read from the table.
        :param str where:
            The 'where' filter to apply to the table.

        :returns astropy.table.QTable:
            The astropy table containing the requested data.
    """
    if isinstance(columns, dict):
        columns = [col for col in columns]
    kepler_data = NasaExoplanetArchive.query_criteria(
        table=table, select=",".join(columns), where=where
    )
    return kepler_data


def rename_columns(df, columns):
    """ Renames the pandas DataFrame columns if the 'columns' parameters is a
        dictionary.

        :param pandas.DataFrame df:
            A pandas DataFrame to rename.
        :type columns: list or dict
        :param columns:
            The columns to rename if provided in the form of a dictionary. In this
            cases, the DataFrame columns which are keys in the dictionary are renamed
            by the dictionary values.

        :returns pandas.DataFrame:
            The renamed pandas DataFrame.
    """
    if isinstance(columns, dict):
        df = df.rename(columns=columns)
    return df


def record_dataframe(df, filename):
    """ Saves the pandas DataFrame into a .csv format if a filename is provided.

        :param pandas.DataFrame df:
            A pandas DataFrame to save into a .csv format.
        :param str filename:
            The location in which to save the DataFrame into a .csv format.
    """
    if filename:
        path = os.path.dirname(filename)
        if not os.path.exists(path):
            os.makedirs(path, exist_ok=True)
        df.to_csv(filename, index=False)
