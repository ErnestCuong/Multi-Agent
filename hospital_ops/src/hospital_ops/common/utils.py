from os import listdir
from os.path import isfile, join
from hospital_ops.common.constants import (
    THRESHOLD_SLOPE_TO_MIN_RATIO,
    THRESHOLD_RES_STD_TO_MIN_RATIO,
    Trend,
    Variability,
)
import numpy as np
from sklearn.linear_model import LinearRegression


def get_all_file_names(folder_path):
    return [f for f in listdir(folder_path) if isfile(join(folder_path, f))]


def get_trend_analysis(slope, min_value):
    # Start as constant trend then check for slope
    trend = Trend.CONSTANT.value

    if slope / min_value > THRESHOLD_SLOPE_TO_MIN_RATIO:
        # Slightly positive slope
        trend = Trend.INCREASING_SLIGHTLY.value
    if slope / min_value > 2 * THRESHOLD_SLOPE_TO_MIN_RATIO:
        # Positive enough slope
        trend = Trend.INCREASING.value
    if slope / min_value < -THRESHOLD_SLOPE_TO_MIN_RATIO:
        # Slightly negative slope
        trend = Trend.DECREASING_SLIGHTLY.value
    if slope / min_value < -2 * THRESHOLD_SLOPE_TO_MIN_RATIO:
        # Negative enough slope
        trend = Trend.DECREASING.value

    return trend


def get_variability_analysis(std_dev_against_trend, min_value):
    # Start as consistent then check for fluctuation
    variability = Variability.CONSISTENT.value

    # Large enough deviation from trend relative to min_value
    if std_dev_against_trend / min_value > THRESHOLD_RES_STD_TO_MIN_RATIO:
        variability = Variability.GENERALLY_CONSISTENT.value
    if std_dev_against_trend / min_value > 2 * THRESHOLD_RES_STD_TO_MIN_RATIO:
        variability = Variability.SLIGHTLY_FLUCTUATING.value
    if std_dev_against_trend / min_value > 4 * THRESHOLD_RES_STD_TO_MIN_RATIO:
        variability = Variability.FLUCTUATING.value

    return variability


def get_latest_trend(list_of_values):
    # Check for the most recent trends
    total_length = len(list_of_values)
    if total_length < 2:
        return "No Trend"
    latest_trend = None
    count = 2
    is_consistent = True

    while count <= total_length:
        value_pair = list_of_values[total_length - count : total_length - count + 2]

        slope = value_pair[1] - value_pair[0]  # This is the trend (slope)
        if (
            latest_trend == None
            and slope / value_pair[0] > 2*THRESHOLD_SLOPE_TO_MIN_RATIO
        ):
            latest_trend = Trend.INCREASING
        elif (
            latest_trend == None
            and slope / value_pair[0] < -2*THRESHOLD_SLOPE_TO_MIN_RATIO
        ):
            latest_trend = Trend.DECREASING
        elif latest_trend == None:
            latest_trend = Trend.CONSTANT
        elif latest_trend == Trend.CONSTANT and (
            abs(slope / value_pair[0]) > 2*THRESHOLD_SLOPE_TO_MIN_RATIO
        ):
            break
        elif (
            latest_trend == Trend.DECREASING
            and slope / value_pair[0] > 2*THRESHOLD_SLOPE_TO_MIN_RATIO
        ):
            break
        elif latest_trend == Trend.DECREASING and slope >= 0:
            is_consistent = False
        elif (
            latest_trend == Trend.INCREASING
            and slope / value_pair[0] < -2*THRESHOLD_SLOPE_TO_MIN_RATIO
        ):
            break
        elif latest_trend == Trend.INCREASING and slope <= 0:
            is_consistent = False

        count += 1

    return (
        "FLUCTUATING for the past 3 months"
        if count <= 3
        else f"{'CONSISTENTLY ' if is_consistent else 'GENERALLY '}{str(latest_trend).replace('Trend.','')} for the last {count-1} months"
    )


def get_goal_analysis(list_of_months, list_of_values, target_pair):
    target_value = target_pair[1]
    target_comparison = target_pair[0]
    if target_comparison == "Lower":
        mask = list_of_values > target_value
        list_of_bad_months = [s for s, b in zip(list_of_months, mask) if b]
        return f"{len(list_of_bad_months)} months higher than the target {target_value}, the months are {list_of_bad_months}"
    elif target_comparison == "Higher":
        mask = list_of_values < target_value
        list_of_bad_months = [s for s, b in zip(list_of_months, mask) if b]
        return f"{len(list_of_bad_months)} months lower than the target {target_value}, the months are {list_of_bad_months}"
    elif target_comparison == "Around":
        mask = list_of_values > 1.03 * target_value
        list_of_higher_months = [s for s, b in zip(list_of_months, mask) if b]
        mask = list_of_values < 0.97 * target_value
        list_of_lower_months = [s for s, b in zip(list_of_months, mask) if b]

        return f"{len(list_of_higher_months)} months higher than the target {target_value}, the higher months are {list_of_higher_months}, {len(list_of_lower_months)} months lower than the target {target_value}, the lowermonths are {list_of_lower_months}"
    return "No target specified"
