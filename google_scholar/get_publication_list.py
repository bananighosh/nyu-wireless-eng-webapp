# ref: https://serpapi.com/google-scholar-author-articles
# ref dashboard: https://serpapi.com/dashboard
# from serpapi import GoogleSearch
import serpapi
import json
from urllib.parse import urlsplit, parse_qsl

params = {
  "engine": "google_scholar_author",
  "author_id": "fzSHXS8AAAAJ",
  "api_key": "8dc52802ba659bfb88b5c71d32046c2c9bb223793336587621bad33db879e417",
}

author_article_results_data = []

# search = GoogleSearch(params)
search = serpapi.search(params)

articles_is_present = True
next_start = 0

while articles_is_present:

    params["start"] = next_start

    search = serpapi.search(params)

    results = search.as_dict()
    
    articles = results["articles"]

    for article in articles:
         author_article_results_data.append(articles)

    # with open("author_pub_out_paginated.json", "a") as outfile:
    #     json.dump(articles, outfile) 
    
    if "next" in results.get("serpapi_pagination", []):
        print(f"Next link: #{results["serpapi_pagination"]["next"]}")
        search.update(dict(parse_qsl(urlsplit(results.get("serpapi_pagination").get("next")).query)))
    else:
       articles_is_present = False
    
    # if not articles:
    next_start += 20
    # else:
    #    articles_is_present = False
     
with open("author_pub_out_paginated.json", "w") as outfile:
    json.dump(author_article_results_data, outfile) 
print(f"all pages done!!" )
