import json
from hospital_ops.common.constants import (
    HOSPITAL_DATA_FOLDER_PATH,
    HOSPITAL_CRITERIA_PATH,
    HOSPITAL_GENERATED_COMMENTS_FOLDER_PATH,
    HOSPITAL_GOLD_COMMENTS_FOLDER_PATH,
    HOSPITAL_REPORT_FOLDER_PATH,
)
from hospital_ops.common.utils import (
    get_all_file_names,
    get_goal_analysis,
)

from crewai_tools import tool

import pandas as pd

import os
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
import csv


@tool("Get Hospital Data File Path Tool")
def get_hospital_path_tool(name: str, format="csv"):
    """Gets the file path to the data for a specific hospital. Provide a single argument as Hospital Name. Optional second argument specifying format type in string like 'csv'."""
    return HOSPITAL_DATA_FOLDER_PATH + name + "." + format


@tool("Get Hospital Name List Tool")
def list_hospitals_tool():
    """A tool to get a list of Hospital Names"""
    file_names = get_all_file_names(HOSPITAL_DATA_FOLDER_PATH)
    return [f.removesuffix(".csv") for f in file_names if f.endswith(".csv")]

@tool("Get Observations Tool")
def get_observation_tool(name: str):
    """A tool to fetch a hospital's preliminary observations. Provide a single argument as the name of the hospital."""
    path = HOSPITAL_REPORT_FOLDER_PATH + name + ".report.csv"
    df = pd.read_csv(path)
    
    return df

@tool("Fetch-and-Observation Tool")
def fetch_and_observation_tool(path: str):
    """A tool to fetch a hospital's data and perform simple data observations. Provide a single argument as the PATH to the hospital csv data file."""
    # Step 1: Load the dataset
    df = pd.read_csv(path)
    df_for_targets = pd.read_csv(HOSPITAL_CRITERIA_PATH)

    # Step 2: Drop the two columns you don't want to analyze
    non_use_columns = ["Setting", "Measure"]
    df_filtered = df.drop(columns=non_use_columns)
    df_for_targets = df_for_targets.drop(columns=non_use_columns)

    # Step 3: Analyse last 4 months
    num_of_months = 4

    # List of month names (column names)
    months = df_filtered.columns.tolist()[-num_of_months:]

    new_df = df[non_use_columns]
    # new_df = df

    # Iterate through each row and calculate slope and R-squared
    results = []

    for index, row in df_filtered.iterrows():
        row_values = row.values[-num_of_months:]  # Get the row as an array of values
        target_pair = df_for_targets.iloc[index]

        # Linear Regression (Trend)
        X = np.arange(len(row_values)).reshape(-1, 1)
        y = row_values  # y is the actual row data (monthly values)

        # Create a mask to ignore NaN values in the last column
        mask = ~np.isnan(y)  # This mask will ignore any NaN values

        # Use only non-NaN values for the regression
        X_clean = X[mask]
        y_clean = y[mask]

        # Store initial value
        initial_value = y_clean[0]

        # Perform linear regression
        model = LinearRegression()
        model.fit(X_clean, y_clean)
        
        # This is the trend (slope)
        slope = round(model.coef_[0], 2)

        # Calculate R-squared
        r_squared = round(model.score(X_clean, y_clean), 2)

        # Analyze against hospital targets
        goal_analysis = get_goal_analysis(months, y_clean, target_pair)

        # Calculate the mean
        mean = np.mean(y_clean)
        
        # Check if last month value is min or max
        last_month_observation = ""
        if (y_clean[-1] == np.min(y_clean) and np.sum(y_clean == y_clean[-1]) == 1):
            last_month_observation = f"Dip in {months[-1]}"
        if (y_clean[-1] == np.max(y_clean) and np.sum(y_clean == y_clean[-1]) == 1):
            last_month_observation = f"Rose in {months[-1]}"
            
        # Store the results for the current row
        results.append(
            {
                f"Last-{num_of_months}-Month Slope": slope,
                f"Last-{num_of_months}-Month R-squared": r_squared,
                f"Last-{num_of_months}-Month Target Analysis": goal_analysis,
                f"Last-{num_of_months}-Month Mean": mean,
                f"Last Month Observation": last_month_observation,
            }
        )

    new_df[f"Last Month Observation"] = [item[f"Last Month Observation"] for item in results]

    new_df[f"Last-{num_of_months}-Month R-squared"] = [
        item[f"Last-{num_of_months}-Month R-squared"] for item in results
    ]
    
    new_df[f"Last-{num_of_months}-Month Slope"] = [
        item[f"Last-{num_of_months}-Month Slope"] for item in results
    ]

    new_df[f"Last-{num_of_months}-Month Target Analysis"] = [item[f"Last-{num_of_months}-Month Target Analysis"] for item in results]
    new_df[f"Last-{num_of_months}-Month Mean"] = [item[f"Last-{num_of_months}-Month Mean"] for item in results]

    # Step 4: Analyse last 6 months
    num_of_months = 6

    # List of month names (column names)
    months = df_filtered.columns.tolist()[-num_of_months:]

    # Iterate through each row and calculate slope and R-squared
    results = []

    for index, row in df_filtered.iterrows():
        row_values = row.values[-num_of_months:]  # Get the row as an array of values
        target_pair = df_for_targets.iloc[index]

        # Linear Regression (Trend)
        X = np.arange(len(row_values)).reshape(-1, 1)
        y = row_values  # y is the actual row data (monthly values)

        # Create a mask to ignore NaN values in the last column
        mask = ~np.isnan(y)  # This mask will ignore any NaN values

        # Use only non-NaN values for the regression
        X_clean = X[mask]
        y_clean = y[mask]

        # Store initial value
        initial_value = y_clean[0]

        # Perform linear regression
        model = LinearRegression()
        model.fit(X_clean, y_clean)
        
        # This is the trend (slope)
        slope = round(model.coef_[0],2)  

        # Calculate R-squared
        r_squared = round(model.score(X_clean, y_clean),2)
        
        # Store the results for the current row
        results.append(
            {
                f"{num_of_months}-Month Slope": slope,
                f"{num_of_months}-Month R-squared": r_squared,
            }
        )

    new_df[f"Last-{num_of_months}-Month R-squared"] = [
        item[f"{num_of_months}-Month R-squared"] for item in results
    ]
    
    new_df[f"Last-{num_of_months}-Month Slope"] = [
        item[f"{num_of_months}-Month Slope"] for item in results
    ]


    # Save the report
    new_df.to_csv(
        path.replace(".csv", ".report.csv").replace(HOSPITAL_DATA_FOLDER_PATH, HOSPITAL_REPORT_FOLDER_PATH),
        index=False,
    )

    # Step 6: Return the report
    return new_df


@tool("Save Comments Tool")
def save_comments_tool(comments: str, name: str):
    """
    A tool to save comments in a txt file.
    :param comments: string, the comments you want to save.
    :param name: string, the name of the hospital, example: 'A'.
    """
    folder_path = "src/hospital_ops/comments/"
    if not os.path.exists(folder_path):
        # Create the folder
        os.makedirs(folder_path)
    with open(folder_path + name + '.txt', "w") as file:
        file.write(comments)
        return "Comments saved successfully"

@tool("Save Test Result Tool")
def save_test_result_tool(result: str, name: str):
    """
    A tool to save test result in a csv file.
    :param result: string, the result which is a json string of an array of rows in a csv format where first row is column names
    :param name: string, the hospital name like 'A'
    """
    folder_path = "src/hospital_ops/tests/"
    if not os.path.exists(folder_path):
        # Create the folder
        os.makedirs(folder_path)
    with open(folder_path + name + '.csv', "w") as file:
        writer = csv.writer(file)
        # Writing each row
        writer.writerows(json.loads(result))
        return "Test Result saved successfully"
    
@tool("Get Gold Standard Comments Tool")
def get_gold_standard_comments_tool(name: str):
    """
    A tool to retrieve the gold standard comments.
    :param name: string, the name of the hospital, example: 'A'.
    """
    with open(HOSPITAL_GOLD_COMMENTS_FOLDER_PATH + name + '.txt', "r") as file:
        return file.read()
    
@tool("Get Generated Comments Tool")
def get_generated_comments_tool(name: str):
    """
    A tool to retrieve the generated comments.
    :param name: string, the name of the hospital, example: 'A'.
    """
    with open(HOSPITAL_GENERATED_COMMENTS_FOLDER_PATH + name + '.txt', "r") as file:
        return file.read()