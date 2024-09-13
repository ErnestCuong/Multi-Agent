from os import listdir
from os.path import isfile, join
from hospital_ops.common.constants import (
    THRESHOLD_SLOPE_TO_MIN_RATIO,
    THRESHOLD_RES_STD_TO_MIN_RATIO,
    Trend,
    Variability,
)


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
