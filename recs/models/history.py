import pandas as pd
import numpy as np
from collections import namedtuple

from recs.models.pop import PopModel


class MixtureOfCategoryModel(namedtuple('MixtureOfPopCategoryModel', ['item_probs', 'user_category_probs', 'item_category_probs'])):
    
    @staticmethod
    def to_user_category_probs(user_events_with_cat_df):
        only_cat_columns = user_events_with_cat_df.columns[~user_events_with_cat_df.columns.isin(["user", "item", "index"])]
        user_category_counts = user_events_with_cat_df.groupby('user')[only_cat_columns].sum()

        return user_category_counts.div(user_category_counts.sum(axis=1), axis=0)

    @staticmethod
    def to_item_category_probs(user_events_with_cat_df):
        only_cat_columns = user_events_with_cat_df.columns[~user_events_with_cat_df.columns.isin(["user", "item", "index"])]
        item_cat_counts = user_events_with_cat_df.groupby('item')[only_cat_columns].sum()

        return item_cat_counts.div(item_cat_counts.sum(axis=1), axis=0)

    @staticmethod
    def align_item_probs(item_category_probs, item_probs=1.0):
        item_joined_probs_df = item_category_probs.join(other=item_probs, how='inner')
        return item_joined_probs_df.iloc[:,:-1], item_joined_probs_df.iloc[:,-1]
            
    @classmethod
    def fit(cls, user_item_df, user_cat_power):
        item_probs = pd.DataFrame(PopModel.fit(user_item_df).item_probs)
        user_category_probs = cls.to_user_category_probs(user_item_df)

        user_category_probs = user_category_probs.apply(lambda x: np.power(x, user_cat_power))
        user_category_probs = user_category_probs.div(user_category_probs.sum(1), 0)
        
        item_category_probs = cls.to_item_category_probs(user_item_df)
        return cls(item_probs, user_category_probs, item_category_probs)

    def user_item_probs(self, users):
        have_user_recs = self.user_category_probs.index.isin(users)
        users_with_recs = self.user_category_probs.index.values[have_user_recs]

        item_category_probs, item_probs = self.align_item_probs(
            self.item_category_probs, self.item_probs)
        
        user_item_probs = np.dot(
            self.user_category_probs.values[have_user_recs, :],
            item_category_probs.values.T) * item_probs.values.ravel()

        return pd.DataFrame(
            index=users_with_recs,
            data=user_item_probs,
            columns=item_probs.index
        )
    
    def recs(self, users, topn=10):
        
        user_item_probs = self.user_item_probs(users)
        users_with_recs = user_item_probs.index.values
        user_topn_indexes = per_user_topn_indexes(user_item_probs, topn)
        user_topn_items = user_item_probs.columns[user_topn_indexes]
        user_topn_scores = user_item_probs.values[
            np.repeat(np.arange(len(users_with_recs)), topn), user_topn_indexes.ravel()]
        
        return pd.DataFrame.from_dict({
                'user': np.repeat(users_with_recs, topn),
                'item': user_topn_items[:, :topn].ravel(),
                'score': user_topn_scores.ravel()
            })
        return user_topn_articles


def per_user_topn_indexes(user_scores, topn=10):
    user_ranks = np.argsort(np.argsort(-np.array(user_scores), axis=1), axis=1) + 1
    item_indexes = np.where(user_ranks <= topn)[1]
    n_users = user_scores.shape[0]
    return np.reshape(item_indexes, (n_users, -1))
