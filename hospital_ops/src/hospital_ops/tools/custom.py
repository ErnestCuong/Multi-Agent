from hospital_ops.common.constants import (
    HOSPITAL_DATA_FOLDER_PATH,
    THRESHOLD_SLOPE_TO_MIN_RATIO,
    THRESHOLD_RES_STD_TO_MIN_RATIO,
    Trend,
    Variability,
)
from hospital_ops.common.utils import get_all_file_names

from crewai_tools import tool

import pandas as pd
from ydata_profiling import ProfileReport
import os
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression


@tool("Get Hospital Data File Path Tool")
def get_hospital_path_tool(name: str, format="csv"):
    """Gets the file path to the data for a specific hospital. Provide a single argument as Hospital Name. Optional second argument specifying format type in string like 'csv'."""
    return HOSPITAL_DATA_FOLDER_PATH + name + "." + format


@tool("Get Hospital Name List Tool")
def list_hospitals_tool():
    """A tool to get a list of Hospital Names"""
    file_names = get_all_file_names(HOSPITAL_DATA_FOLDER_PATH)
    return [f.removesuffix(".csv") for f in file_names if f.endswith(".csv")]


# @tool("EDA tool")
# def eda_tool(path: str):
#     """Analyze a single csv file and saves the report as a json file with the same name in the same directory. Provide a single argument as Path to the csv file."""
#     df = pd.read_csv(path)
#     profile = ProfileReport(df, title="Profiling Report")
#     write_path = path.replace('.csv', '.json')
#     try:
#         os.remove(write_path)
#     except OSError:
#         pass
#     profile.to_file(write_path)


@tool("Fetch-and-Analyze Tool")
def fetch_and_analyze_tool(path: str):
    """A tool to fetch a hospital's data and perform simple data observations. Provide a single argument as the PATH to the hospital csv data file."""
    # Step 1: Load the dataset
    df = pd.read_csv(path)

    # Step 2: Drop the two columns you don't want to analyze
    non_time_columns = ["Setting", "Measure"]
    df_filtered = df.drop(columns=non_time_columns)

    # Step 4: List of month names (column names)
    months = df_filtered.columns.tolist()

    # Step 5: Iterate through each row and perform trend, variability, min, and max analysis
    results = []

    for index, row in df_filtered.iterrows():
        row_values = row.values  # Get the row as an array of values

        # Linear Regression (Trend)
        X = np.arange(len(row_values)).reshape(
            -1, 1
        )  # X is just the indices (representing time/position)
        y = row_values  # y is the actual row data (monthly values)
        
        # Create a mask to ignore NaN values in the last column
        mask = ~np.isnan(y)  # This mask will ignore any NaN values

        # Use only non-NaN values for the regression
        X_clean = X[mask]
        y_clean = y[mask]
    
        # Perform linear regression
        model = LinearRegression()
        model.fit(X_clean, y_clean)
        slope = model.coef_[0]  # This is the trend (slope)

        # Predict values based on the trend (linear regression line)
        predicted_values = model.predict(X_clean)

        # Calculate Residuals (Difference between actual values and predicted trend)
        residuals = y_clean - predicted_values

        # Variability (Standard Deviation) of Residuals (Against the Trend)
        std_dev_against_trend = np.std(residuals)

        # Min, Max, and their corresponding months
        min_value = np.min(y_clean)
        min_when = months[np.argmin(y_clean)]  # Corresponding month for min value

        max_value = np.max(y_clean)
        max_when = months[np.argmax(y_clean)]  # Corresponding month for max value

        # Determine trend
        trend = Trend.CONSTANT.value  # Start as constant trend then check for slope
        if slope / min_value > THRESHOLD_SLOPE_TO_MIN_RATIO:  # Positive enough slope
            trend = Trend.INCREASING.value
        elif slope / min_value < -THRESHOLD_SLOPE_TO_MIN_RATIO:  # Negative enough slope
            trend = Trend.DECREASING.value

        # Determine variability
        variability = (
            Variability.CONSISTENT.value
        )  # Start as consistent then check for fluctuation
        if (
            std_dev_against_trend / min_value > THRESHOLD_RES_STD_TO_MIN_RATIO
        ):  # Large enough deviation from trend relative to min_value
            variability = Variability.FLUCTUATING.value

        # Store the results for the current row
        results.append(
            {
                "Trend": trend,
                "Variability": variability,
                "Min Value": min_value,
                "Min When": min_when,
                "Max Value": max_value,
                "Max When": max_when,
            }
        )
    
    # Step 5: Create a new dataset report
    new_df = df[non_time_columns]
    new_df['Trend'] = [item['Trend'] for item in results]
    new_df['Variability'] = [item['Variability'] for item in results]
    new_df['Min Value'] = [item['Min Value'] for item in results]
    new_df['Min When'] = [item['Min When'] for item in results]
    new_df['Max Value'] = [item['Max Value'] for item in results]
    new_df['Max When'] = [item['Max When'] for item in results]
    
    # Save the report
    new_df.to_csv(path.replace('.csv', '.report.csv'), index=False)
    
    # Step 6: Return the report
    return new_df