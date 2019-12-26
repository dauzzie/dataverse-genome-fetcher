import pytest
import pandas as pd
from pathlib import Path

import check_update as cu



def test_get_response():
    df = cu.get_response()
    assert df != None

def test_get_update():
    needs_update = None
    df = cu.get_response()
    cu.format_response(df)
    curr = cu.get_current()
    needs_update = cu.needs_update(df, curr)
    assert needs_update != None

def test_download():
    curr = cu.get_current()
    f_list = cu.set_files(curr)
    df_f = cu.get_files(f_list)
    assert df_f != None

def test_meta_update():
    test = cu.update_data()
    assert test == "Success"
