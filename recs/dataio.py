import json
import numpy as np
import pandas as pd
from itertools import chain


def load_article_categories_df(path="/Users/gui/Data/ap_article_content_es_no_utf.json"):
    with open(path) as file:
        articles = json.load(file)['hits']['hits']

    unique_categories = set(chain(*[a['fields']['categories'] for a in articles]))
    vocabulary = {c:i for i, c in enumerate(unique_categories)}

    def to_binary_variables(category):
        return np.asarray(np.in1d(list(unique_categories), category), dtype=int) 

    article_ids = [int(a['_id']) for a in articles]
    article_categories = np.array(
        [to_binary_variables(a['fields']['categories']) for a in articles]
    )

    article_categories_df = pd.DataFrame(
        index=article_ids, data=article_categories, columns=unique_categories)
    return article_categories_df
