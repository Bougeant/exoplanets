# -*- coding: utf-8 -*-

""" Functions to get table and light curves data using astroquery. """

import logging
import os

import pandas as pd
from astroquery.nasa_exoplanet_archive import NasaExoplanetArchive

DEFAULT_PARAMS = {
    "q1_q17_dr25_stellar": {
        "columns": {
            "kepid": "KIC Identification Number",
            "tm_designation": "2MASS Designation",
            "ra": "RA Value [decimal degrees]",
            "dec": "Dec Value [decimal degrees]",
            "teff": "Stellar Effective Temperature Value [K]",
            "logg": "Stellar Surface Gravity Value [log10(cm/s**2)]",
            "feh": "Stellar Metallicity Value [dex]",
            "radius": "Stellar Radius Value [Solar radii]",
            "mass": "Stellar Mass Value [Solar mass]",
            "dens": "Stellar Density Value [g/cm**3]",
            "dist": "Distance Value [pc]",
            "av": "Av Extinction Value [mags]",
            "kepmag": "Kepler-band Magnitude Value [mag]",
            "nconfp": "Number of Associated Confirmed Planets",
            "nkoi": "Number of Associated KOIs",
            "ntce": "Number of Associated TCEs",
            "st_quarters": "Bits of Observed Quarters",
            "st_vet_date": "Vetting Status Date",
        },
        "where": "st_quarters like '%1%'",
    },
    "cumulative": {
        "columns": {
            "kepid": "KIC Identification Number",
            "kepoi_name": "KOI Name",
            "kepler_name": "Kepler Name",
            "ra": "RA Value [decimal degrees]",
            "dec": "Dec Value [decimal degrees]",
            "koi_disposition": "Exoplanet Archive Disposition",
            "koi_score": "Disposition Score",
            "koi_fpflag_nt": "Not Transit-Like Flag",
            "koi_fpflag_ss": "Stellar Eclipse Flag",
            "koi_fpflag_co": "Nearby Star Flag",
            "koi_fpflag_ec": "Contamination Flag",
            "koi_period": "Orbital Period (days)",
            "koi_time0bk": "Transit Epoch",
            "koi_time0": "Transit Epoch in BJD",
            "koi_eccen": "Eccentricity",
            "koi_duration": "Transit Duration (hours)",
            "koi_ingress": "Ingress Duration (hours)",
            "koi_depth": "Transit Depth (parts per million)",
            "koi_ror": "Planet-Star Radius Ratio",
            "koi_srho": "Fitted Stellar Density [g/cm*3]",
            "koi_prad": "Planetary Radius (Earth radii)",
            "koi_incl": "Inclination (deg)",
            "koi_teq": "Equilibrium Temperature (Kelvin)",
            "koi_dor": "Planet-Star Distance over Star Radius",
            "koi_model_snr": "Transit Signal-to-Noise",
            "koi_count": "Number of Planets",
            "koi_num_transits": "Number of Transits",
            "koi_tce_plnt_num": "TCE Planet Number",
            "koi_quarters": "Quarters",
            "koi_kepmag": "Kepler-band (mag)",
            "koi_vet_date": "Vetting Status Date",
        },
        "where": None,
    },
}


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
        df.to_csv(filename, index=False)
