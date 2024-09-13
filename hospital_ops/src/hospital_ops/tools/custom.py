from hospital_ops.common.constants import HOSPITAL_DATA_FOLDER_PATH
from hospital_ops.common.utils import (
    get_all_file_names,
    get_trend_analysis,
    get_variability_analysis,
)

from crewai_tools import tool

import pandas as pd
# from ydata_profiling import ProfileReport
# import os
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


@tool("Fetch-and-Observation Tool")
def fetch_and_observation_tool(path: str, num_of_months = 4):
    """A tool to fetch a hospital's data and perform simple data observations. Provide a single argument as the PATH to the hospital csv data file."""
    # Step 1: Load the dataset
    df = pd.read_csv(path)

    # Step 2: Drop the two columns you don't want to analyze
    non_time_columns = ["Setting", "Measure"]
    df_filtered = df.drop(columns=non_time_columns)

    # Step 4: List of month names (column names)
    months = df_filtered.columns.tolist()[-num_of_months:]

    # Step 5: Iterate through each row and perform trend, variability, min, and max analysis
    results = []

    for index, row in df_filtered.iterrows():
        row_values = row.values[-num_of_months:]  # Get the row as an array of values

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
        
        # # Check and remove anomaly
        # mask = (abs(residuals) < 1.5 * std_dev_against_trend)
        # anomalies = X_clean[~mask]
        # if anomalies.size > 0:
        #     print('ANOMALY DETECTED')
        #     X_clean = X_clean[mask]
        #     y_clean = y_clean[mask]
            
        #     # Perform linear regression again
        #     model = LinearRegression()
        #     model.fit(X_clean, y_clean)
        #     slope = model.coef_[0]  # This is the trend (slope)

        #     # Predict values based on the trend (linear regression line)
        #     predicted_values = model.predict(X_clean)

        #     # Calculate Residuals (Difference between actual values and predicted trend)
        #     residuals = y_clean - predicted_values

        #     # Variability (Standard Deviation) of Residuals (Against the Trend)
        #     std_dev_against_trend = np.std(residuals)
        

        # Determine trend
        trend = get_trend_analysis(slope, min_value)

        # Determine variability
        variability = get_variability_analysis(std_dev_against_trend, min_value)

        # Store the results for the current row
        results.append(
            {
                "Trend": trend,
                "Variability": variability,
                "Min Value": min_value,
                "Min When": min_when,
                "Max Value": max_value,
                "Max When": max_when,
                # "Anomalies": [months[anomaly[0]] for anomaly in anomalies]
            }
        )

    # Step 5: Create a new dataset report
    new_df = df[non_time_columns]
    new_df["Trend"] = [item["Trend"] for item in results]
    new_df["Variability"] = [item["Variability"] for item in results]
    new_df["Min Value"] = [item["Min Value"] for item in results]
    new_df["Min When"] = [item["Min When"] for item in results]
    new_df["Max Value"] = [item["Max Value"] for item in results]
    new_df["Max When"] = [item["Max When"] for item in results]
    # new_df["Anomalies"] = [item["Anomalies"] for item in results]

    # Save the report
    new_df.to_csv(path.replace(".csv", ".report.csv"), index=False)

    # Step 6: Return the report
    return new_df

@tool("Save Comments Tool")
def save_comments_tool(comments: str, name: str):
    """
    A tool to save comments in a txt file. 
    :param comments: string, the comments you want to save.
    :param name: string, the name of the saved file, format it like this '<hospital name>_comments.txt'.
    """
    with open("src/hospital_ops/comments/" + name, "w") as file:
        file.write(comments)