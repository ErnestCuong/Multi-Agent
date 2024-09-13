from enum import Enum
HOSPITAL_DATA_FOLDER_PATH = 'src/hospital_ops/data/hospitals/'

THRESHOLD_SLOPE_TO_MIN_RATIO = 0.01
THRESHOLD_RES_STD_TO_MIN_RATIO = 0.01
class Trend(Enum):
    INCREASING = 'Increasing'
    INCREASING_SLIGHTLY = 'Increasing Slightly'
    CONSTANT = 'Constant'
    DECREASING_SLIGHTLY = 'Decreasing Slightly'
    DECREASING = 'Decreasing'
    
class Variability(Enum):
    FLUCTUATING = 'Fluctuating'
    SLIGHTLY_FLUCTUATING = 'Slightly Fluctuating'
    GENERALLY_CONSISTENT = 'Generally Consistent'
    CONSISTENT = 'Consistent'