from enum import Enum
HOSPITAL_DATA_FOLDER_PATH = 'src/hospital_ops/data/hospitals/'
HOSPITAL_REPORT_FOLDER_PATH = 'src/hospital_ops/data/reports/'
HOSPITAL_CRITERIA_PATH = 'src/hospital_ops/data/criteria.csv'
HOSPITAL_GENERATED_COMMENTS_FOLDER_PATH = 'src/hospital_ops/comments/'
HOSPITAL_GOLD_COMMENTS_FOLDER_PATH = 'src/hospital_ops/gold_comments/'
HOSPITAL_TEST_RESULT_FOLDER_PATH = 'src/hospital_ops/tests/'
THRESHOLD_SLOPE_TO_MIN_RATIO = 0.01
THRESHOLD_RES_STD_TO_MIN_RATIO = 0.01
class Trend(Enum):
    INCREASING = 'Increasing'
    GENERALLY_INCREASING = 'Generally Increasing'
    CONSTANT = 'Constant'
    GENERALLY_CONSTANT = 'Generally Constant'
    DECREASING = 'Decreasing'
    GENERALLY_DECREASING = 'Generally Decreasing'
    FLUCTUATING = 'Fluctuating'
        
class Variability(Enum):
    FLUCTUATING = 'Fluctuating'
    SLIGHTLY_FLUCTUATING = 'Slightly Fluctuating'
    GENERALLY_CONSISTENT = 'Generally Consistent'
    CONSISTENT = 'Consistent'