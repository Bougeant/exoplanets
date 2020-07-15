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
    }
}


def read_kepler_data(table, columns=None, where=None, filename=None):
    """
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
    """
    """
    if table in DEFAULT_PARAMS:
        columns = DEFAULT_PARAMS[table]["columns"] if not columns else columns
        where = DEFAULT_PARAMS[table]["where"] if not where else where
    return columns, where


def get_kepler_data(table, columns, where):
    """
    """
    if isinstance(columns, dict):
        columns = [col for col in columns]
    kepler_data = NasaExoplanetArchive.query_criteria(
        table=table, select=",".join(columns), where=where
    )
    return kepler_data


def rename_columns(df, columns):
    """
    """
    if isinstance(columns, dict):
        df = df.rename(columns=columns)
    return df


def record_dataframe(df, filename):
    """
    """
    if filename:
        df.to_csv(filename, index=False)
