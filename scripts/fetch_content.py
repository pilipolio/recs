from datetime import datetime
from elasticsearch import Elasticsearch

es = Elasticsearch()

es.get(index='ap', doc_type='article', id=8209007)

non_empty_body = {'query': {'prefix':{'body':'<div'}}}
response = es.search(index='ap', doc_type='article', fields='_id,categories,published', q='{"prefix":{"body":"<div"}}')


q = {
    "query": {
        "filtered": {
            "query": {
                "query_string": {
                    "query": "div",
                    "analyze_wildcard": True
                }
            },
            "filter": {
                "bool": {
                    "must": [
                        {
                            "range": {
                                "created": {
                                    "gte": 1438470000000,
                                    "lte": 1444950000000
                                }
                            }
                        }
                    ],
                    "must_not": []
                }
            }
        }
    }
}
    
response = es.search(index='ap', doc_type='article', fields='_id,categories,published', body=q, size=10000)

import json
with open('ap_article_content_es.json', 'w') as f:
    json.dump(response, fp=f)
