from typing import Dict

from googlesearch import search


def execute_search(parameters: Dict):
    query = parameters.get("query", "")
    search_type = parameters.get("type", "value")
    count = int(parameters.get("count", 10))

    results = []

    for j in search(query, num_results=count):
        if search_type == "link":
            results.append(j.url)
        elif search_type == "value":
            results.append(j.title)

    return results

# Example usage
# parameters = {
#     "query": "AI at home article",
#     "type": "link",
#     "count": 3
# }
# print(execute_search(parameters))
