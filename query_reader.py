import json
 


def read_search_query_from_json_file() :
    f = open('user_queries.json')
    data = json.load(f)
    return data