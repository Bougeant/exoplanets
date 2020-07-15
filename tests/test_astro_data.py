# -*- coding: utf-8 -*-

""" Tests for exoplanets.astro_data """

import astropy

from exoplanets import astro_data


class TestAstroDataTable:
    def test_get_default_params(self):
        columns, where = astro_data.get_default_params(
            table="q1_q17_dr25_stellar", columns=None, where=None
        )
        assert isinstance(columns, dict)
        assert "kepid" in columns
        assert isinstance(where, str)
        assert where == "st_quarters like '%1%'"

    def test_get_default_params_with_values(self):
        columns, where = astro_data.get_default_params(
            table="q1_q17_dr25_stellar", columns=["col1", "col2"], where="kepid=12345"
        )
        assert isinstance(columns, list)
        assert columns == ["col1", "col2"]
        assert isinstance(where, str)
        assert where == "kepid=12345"

    def test_get_kepler_data(self):
        kepler_data = astro_data.get_kepler_data(
            table="q1_q17_dr25_stellar", columns=["kepid"], where="kepid=8113154"
        )
        assert isinstance(kepler_data, astropy.table.QTable)
        assert kepler_data.keys() == ["kepid"]
        assert kepler_data["kepid"].tolist() == [8113154]
