# -*- coding: utf-8 -*-

""" Tests for exoplanets.astro_data """

import astropy
import pandas as pd

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

    def test_rename_columns(self):
        df = pd.DataFrame({"A": [1, 2, 3]})
        df = astro_data.rename_columns(df, columns={"A": "B"})
        expected_df = pd.DataFrame({"B": [1, 2, 3]})
        assert df.equals(expected_df)

    def test_rename_columns_list(self):
        df = pd.DataFrame({"A": [1, 2, 3]})
        expected_df = df.copy()
        df = astro_data.rename_columns(df, columns=["A"])
        assert df.equals(expected_df)

    def test_record_dataframe(self, tmp_path):
        filename = tmp_path / "my_file.csv"
        df = pd.DataFrame({"A": [1, 2, 3]})
        astro_data.record_dataframe(df, filename=filename)
        with open(filename, "r") as csv_file:
            csv_contents = csv_file.read()
        assert csv_contents == "A\n1\n2\n3\n"

    def test_read_kepler_data(self, tmp_path):
        filename = tmp_path / "my_file.csv"
        columns = {"kepid": "Kepler ID", "tm_designation": "2MASS ID"}
        where = "kepid=8113154"
        filename = tmp_path / "my_file.csv"
        df = astro_data.read_kepler_data(
            "q1_q17_dr25_stellar", columns, where, filename
        )
        expected_df = pd.DataFrame(
            {"Kepler ID": [8113154], "2MASS ID": "2MASS J19473063+4356298"}
        )
        assert df.equals(expected_df)
        with open(filename, "r") as csv_file:
            csv_contents = csv_file.read()
        assert csv_contents == "kepid,tm_designation\n8113154,2MASS J19473063+4356298\n"

    def test_read_kepler_data(self, tmp_path):
        filename = tmp_path / "my_file.csv"
        pd.DataFrame({"A": [1, 2, 3]}).to_csv(filename, index=False)
        df = astro_data.read_kepler_data(
            table="q1_q17_dr25_stellar",
            columns=["kepid"],
            where="filter",
            filename=filename,
        )
        expected_df = pd.DataFrame({"A": [1, 2, 3]})
        assert df.equals(expected_df)
