from enum import Enum
HOSPITAL_DATA_FOLDER_PATH = 'src/hospital_ops/data/hospitals/'

THRESHOLD_SLOPE_TO_MIN_RATIO = 0.05
THRESHOLD_RES_STD_TO_MIN_RATIO = 0.05
class Trend(Enum):
    INCREASING = 'Increasing'
    CONSTANT = 'Constant'
    DECREASING = 'Decreasing'
    
class Variability(Enum):
    FLUCTUATING = 'Fluctuating'
    CONSISTENT = 'Consistent'