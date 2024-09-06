from hospital_ops.common.constants import HOSPITAL_DATA_FOLDER_PATH
from hospital_ops.common.utils import get_all_file_names

from crewai_tools import tool

import pandas as pd
from ydata_profiling import ProfileReport
import os

@tool("Get Hospital Data File Path Tool")
def get_hospital_path_tool(name: str, format = 'csv'):
    """Gets the file path to the data for a specific hospital. Provide a single argument as Hospital Name. Optional second argument specifying format type in string like 'csv'."""
    return HOSPITAL_DATA_FOLDER_PATH + name + '.' + format

@tool("Get Hospital Name List Tool")
def list_hospitals_tool():
    """A tool to get a list of Hospital Names"""
    file_names = get_all_file_names(HOSPITAL_DATA_FOLDER_PATH)
    return [f.removesuffix('.csv') for f in file_names if f.endswith('.csv')]

@tool("EDA tool")
def eda_tool(path: str):
    """Analyze a single csv file and saves the report as a json file with the same name in the same directory. Provide a single argument as Path to the csv file."""
    df = pd.read_csv(path)
    profile = ProfileReport(df, title="Profiling Report")
    write_path = path.replace('.csv', '.json')
    try:
        os.remove(write_path)
    except OSError:
        pass
    profile.to_file(write_path)
    
    