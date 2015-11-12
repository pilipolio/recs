import pandas as pd

from recs.evaluation import metrics

def test_prec_and_recall():
    test = pd.DataFrame.from_dict({'user': [1, 1, 2], 'item': [2, 3, 3]})
    recs = pd.DataFrame.from_dict({'user': [1, 1, 2, 2], 'item': [1, 2, 3, 1]})

    prec_recall = 1/2., 2/3.
    
    assert metrics.prec_and_recall(test, recs) == prec_recall
