import pandas as pd
from datetime import datetime

def test_last_day_only_decay_return_ones_for_last_date():
    last_datetime = datetime(2015, 2, 1)
    other_datetime = datetime(2015, 1, 31)
    
    timestamps_df = pd.DataFrame.from_dict({'ts': [last_datetime, other_datetime]})
