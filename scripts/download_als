from boto.s3.connection import S3Connection, Bucket, Key
from itertools import chain, imap
import json

conn = S3Connection("AKIAJYJVSRAXJ6KD6UTQ", "9JStbyXf7pqrk+YIX/ktnNvT0WfKY61EEdCmqyjR")
b = Bucket(conn, "spt-analytics-curate-dev")

model = "topics.site=no_site.topics=200.iter=100.optimizer=em.lm=tfidf.lda"
article_key_prefix = "fredrik/lda/item-profiles/aftenposten/" + model

model = "topics.site=aftenposten.topics=200.iter=100.optimizer=em.lm=tf.lda"
article_key_prefix = "fredrik/lda/item-profiles/aftenposten/2015/" + model

article_features_keys = filter(lambda k: '_SUCCESS' not in k.name, b.list(article_key_prefix))

def get_lines(key):
    print(key.name)
    return key.get_contents_as_string().split('\n')

all_article_features_lines = list(chain.from_iterable(imap(get_lines, article_features_keys)))
all_article_features = map(json.loads, filter(len, all_article_features_lines))
article_features_by_ids = {a['id']:a['topics'] for a in all_article_features if all(f != 0.0 for f in a['topics'])}

with open('/Users/Gui/Data/ap_article_topics_weights.json', 'w') as f:
    json.dump(article_features_by_ids, f)

tags_prefix = "fredrik/lda/models/2015/" + model + "/tagclouds"
tags_keys = [key for key in b.list(tags_prefix) if '_SUCCESS' not in key.name]
all_topics_lines = chain.from_iterable(map(get_lines, tags_keys))
all_topics_tags = list(map(json.loads, filter(len, all_topics_lines)))

with open('/Users/Gui/Data/ap_topics_tags.json', 'w') as f:
    json.dump(all_topics_tags, f)

