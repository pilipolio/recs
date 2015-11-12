import pandas as pd
import numpy as np

from datetime import datetime
from recs.models.history import MixtureOfCategoryModel, per_user_topn_indexes
from numpy.testing import assert_array_equal
from pandas.util.testing import assert_frame_equal

first_user, second_user = 1, 2
first_item, second_item, third_item = 10, 20, 30
first_cat, second_cat = 'first_cat', 'second_cat'


def test_to_user_category_probs():

    any_item = 10
    
    user_item_df = pd.DataFrame.from_dict({
        'user': [first_user, first_user, second_user],
        'item': [any_item, any_item, any_item],
        first_cat: [1, 0, 0],
        second_cat: [0, 1, 1]
    })

    user_category_probs = MixtureOfCategoryModel.to_user_category_probs(user_item_df)
    expected_probs = pd.DataFrame.from_records([
        {'user': first_user, first_cat: .5, second_cat: .5},
    {'user': second_user, first_cat: 0, second_cat: 1.0}], index='user')

    assert_frame_equal(expected_probs, user_category_probs)

def test_to_item_category_probs():
        
    any_user = 1
    
    user_item_df = pd.DataFrame.from_dict({
        'user': [any_user, any_user, any_user],
        'item': [first_item, second_item, third_item],
        first_cat: [1, 1, 0],
        second_cat: [0, 1, 1]
    })

    item_category_probs = MixtureOfCategoryModel.to_item_category_probs(user_item_df)
    expected_probs = pd.DataFrame.from_records([
        {'item': first_item, first_cat: 1, second_cat: 0},
        {'item': second_item, first_cat: .5, second_cat: .5},
        {'item': third_item, first_cat: 0, second_cat: 1},
    ],
        index='item')

    assert_frame_equal(expected_probs, item_category_probs)

def test_user_item_probs():

    third_item_without_probs = 'third'
    user_without_probs = 3
    
    user_cat_probs = pd.DataFrame.from_records([
        {'user': first_user, first_cat: 0, second_cat: 1},
        {'user': second_user, first_cat: .5, second_cat: .5},
    ], index='user')
    
    item_cat_probs = pd.DataFrame.from_records([
        {'item': second_item, first_cat: .5, second_cat: .5},
        {'item': first_item, first_cat: 1, second_cat: 0},
    ], index='item')

    item_probs = pd.DataFrame(pd.Series(index=[first_item, second_item], data=[.75, .25]))

    expected_probs = pd.DataFrame.from_records([
        {'user': first_user, first_item: 0 + 0 * .5 * .75, second_item: 0 + 1 * .5 * .25},
        {'user': second_user, first_item: .5 * 1 * .75, second_item: .5 * .5 * .25 + .5 * .5 * .25},
    ], index='user')

    model = MixtureOfCategoryModel(item_probs, user_cat_probs, item_cat_probs)

    user_item_probs = model.user_item_probs(users=[first_user, second_user])

    assert_frame_equal(expected_probs, user_item_probs, check_names=False)

def test_recs():

    user_cat_probs = pd.DataFrame.from_records([
        {'user': first_user, first_cat: 0, second_cat: 1},
        {'user': second_user, first_cat: .5, second_cat: .5},
    ], index='user')
    
    item_cat_probs = pd.DataFrame.from_records([
        {'item': second_item, first_cat: .5, second_cat: .5},
        {'item': first_item, first_cat: 1, second_cat: 0},
    ], index='item')

    item_probs = pd.DataFrame(pd.Series(index=[first_item, second_item], data=[.75, .25]))

    expected_top_items = pd.DataFrame.from_records([
        {'user': first_user, 'item': second_item, 'score': 1 * .5 * .25},
        {'user': second_user, 'item': first_item, 'score': .5 * 1 * .75}
    ])

    model = MixtureOfCategoryModel(item_probs, user_cat_probs, item_cat_probs)

    topn_user_items = model.recs(users=[first_user, second_user], topn=1)

    assert_frame_equal(expected_top_items, topn_user_items, check_names=False)


def test_per_user_topn_indexes():
    user_scores = np.array([
        [3, 1, 2],
        [1, 3, 2]])
    expected_indexes = [
        [0, 2],
        [1, 2]]
    actual_topn_indexes = per_user_topn_indexes(user_scores, topn=2)
    assert_array_equal(actual_topn_indexes, expected_indexes)
