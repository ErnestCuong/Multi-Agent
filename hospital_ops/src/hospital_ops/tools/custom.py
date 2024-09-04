from hospital_ops.common.constants import HOSPITAL_DATA_FOLDER_PATH
from hospital_ops.common.utils import get_all_file_names

from crewai_tools import tool

@tool("Get Hospital Data File Path Tool")
def get_hospital_path_tool(name: str):
    """Gets the file path to the data for a specific hospital. Provide a single argument as Hospital Name."""
    return HOSPITAL_DATA_FOLDER_PATH + name + '.csv'

@tool("Get Hospital Name List Tool")
def list_hospitals_tool():
    """A tool to get a list of Hospital Names"""
    file_names = get_all_file_names(HOSPITAL_DATA_FOLDER_PATH)
    return [f.removesuffix('.csv') for f in file_names if f.endswith('.csv')]