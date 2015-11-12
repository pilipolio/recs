import pandas as pd
import numpy as np

from datetime import datetime
from recs.models.pop import PopModel
from numpy.testing import assert_array_equal
from pandas.util.testing import assert_frame_equal, assert_series_equal


def test_last_day_only_decay_return_ones_for_last_date():
    last_datetime = datetime(2015, 2, 1)
    other_datetime = datetime(2015, 1, 31, 23, 59, 59)
    timestamps_df = pd.DataFrame.from_dict({'ts': [last_datetime, other_datetime]})
    expected_weights = [1.0, 0.0]
    
    actual_weights = PopModel.last_day_only_decay(timestamps_df)
    
    assert_array_equal(expected_weights, actual_weights)


def test_fit_return_model_items_probs():
    any_user = 1.0
    top_item, second_item = 'top', 'second'
    no_time_decay = lambda df: np.ones(df.shape[0])
    
    user_item_df = pd.DataFrame.from_dict({
        'user': [any_user, any_user, any_user],
        'item': [second_item, top_item, top_item]
    })

    model = PopModel.fit(user_item_df, no_time_decay)
    expected_item_probs = pd.Series(index=[top_item, second_item], data=[2./3, 1./3], name='item')    
    assert_series_equal(model.item_probs, expected_item_probs, check_names=False)
    

def test_recs_returns_topn_items_repeated():
    top_item, second_item = 'top', 'second'
    first_user, second_user = 1, 10

    model = PopModel(pd.Series(index=[top_item, second_item], data=[2./3, 1./3]))
    expected_recs = pd.DataFrame.from_dict({
        'user': [first_user, second_user],
        'item': [top_item, top_item]})
    
    actual_recs = model.recs(users = [first_user, second_user], topn=1)

    print actual_recs
    print expected_recs
    assert_frame_equal(expected_recs, actual_recs)
