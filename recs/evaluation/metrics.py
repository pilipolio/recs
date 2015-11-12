import numpy as np


def prec_and_recall(test_user_item_df, rec_user_item_df):
    test_user_item_array = test_user_item_df[['user', 'item']].values.copy()
    rec_user_item_array = rec_user_item_df[['user', 'item']].values.copy()
    test_hits = np.in1d(
        as_user_item_tuples(test_user_item_array),
        as_user_item_tuples(rec_user_item_array)
        )
    n_hits = np.sum(test_hits)
    n_recs = rec_user_item_df.shape[0]
    return 1.0 * n_hits / n_recs, 1.0 * n_hits / len(test_hits)


def as_user_item_tuples(user_item_array):
        return user_item_array.view(dtype=[('user', 'int64'), ('item', 'int64')])
