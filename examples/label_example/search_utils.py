'''
this file defines search functions for searching data in elasticsearch.
'''


def all_search(es, index: str) -> dict:
    """
    Args:
        es: Elasticsearch client instance.
        index: Name of the index we are going to use.
        size: Number of results returned in each search.
    """
    # search query
    body = {"query": {"match_all": {}}}

    res = es.search(index=index, body=body)

    return res


def index_search(es, index: str, keywords: str) -> dict:
    """
    Args:
        es: Elasticsearch client instance.
        index: Name of the index we are going to use.
        keywords: Search keywords.
        from_i: Start index of the results for pagination.
        size: Number of results returned in each search.
    """
    # search query
    body = {
        "query": {
            "bool": {
                "must": [
                    {
                        "query_string": {
                            "query": keywords,
                            "fields": ["content"],
                            "default_operator": "AND",
                        }
                    }
                ],
            }
        },
        "highlight": {
            "pre_tags": [' <font color = "#dc3023">'],
            "post_tags": ["</font>"],
            "fields": {"content": {}},
        },
        "aggs": {"match_count": {"value_count": {"field": "_id"}}},
    }

    res = es.search(index=index, body=body)

    return res
