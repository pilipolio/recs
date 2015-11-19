from boto.s3.connection import S3Connection, Bucket, Key
from itertools import chain
import json

model = "topics.site=no_site.topics=75.iter=100.optimizer=em.lm=tfidf.lda"
key_prefix = "fredrik/lda/item-profiles/aftenposten/" + model

conn = S3Connection("AKIAJYJVSRAXJ6KD6UTQ", "9JStbyXf7pqrk+YIX/ktnNvT0WfKY61EEdCmqyjR")
b = Bucket(conn, "spt-analytics-curate-dev")

article_features_keys = list(b.list(key_prefix))
all_article_features = [json.loads(key.get_contents_as_string()) for key in article_features_keys]

article_features_by_ids = {a['id']:a['features'] for a in article_features if all(f != 0.0 for f in a['features'])}

tags_prefix = "fredrik/lda/models/201510/" + model + "/tagclouds"


tags_keys = [key for key in b.list(tags_prefix) if '_SUCCESS' not in key.name]

def parse_part_file(part_content):
    return [json.loads(line) for line in part_content.split('\n') if line != '']


all_topics_tags = list(chain(*[parse_part_file(key.get_contents_as_string()) for key in tags_keys]))

with open('/Users/Gui/Data/ap_topics_tags.json', 'w') as f:
    json.dump(all_topics_tags, f)

with open('/Users/Gui/Data/ap_article_topics_weights.json', 'w') as f:
    json.dump(article_features_by_ids, f)
