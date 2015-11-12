from collections import namedtuple
import pandas as pd
import numpy as np
from datetime import timedelta


class PopModel(namedtuple('PopModel', ['item_probs'])):
    
    @staticmethod
    def last_day_only_decay(user_item_df):
        max_date = user_item_df.ts.max().date()
        return 1.0 * np.logical_and(user_item_df.ts >= max_date, user_item_df.ts < max_date + timedelta(days=1))
    
    @classmethod
    def fit(cls, user_item_df, time_decay_function=last_day_only_decay):
        time_decayed_user_items = user_item_df.copy()
        time_decayed_user_items.loc[:, 'time_decays'] = time_decay_function(user_item_df)
        item_counts = time_decayed_user_items.groupby('item')['time_decays'].sum()
        item_probs = (item_counts / item_counts.sum()).sort_values(ascending=False)

        return cls(item_probs)
    
    def recs(self, users, topn=10):
        topn_items = self.item_probs.index[:topn]
        return pd.DataFrame.from_dict({
                'user': np.repeat(users, topn),
                'item': np.tile(topn_items, len(users))
            })
