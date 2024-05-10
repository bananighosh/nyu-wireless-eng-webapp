# ref: https://serpapi.com/google-scholar-author-articles
# ref dashboard: https://serpapi.com/dashboard

from serpapi import GoogleSearch
import json
from urllib.parse import urlsplit, parse_qsl

params = {
  "engine": "google_scholar_author",
  "author_id": "aLOSzWwAAAAJ",
  "api_key": "",  # Replace with your actual API key
}

author_article_results_data = []

articles_is_present = True
next_start = 0

while articles_is_present:

    params["start"] = next_start

    search = GoogleSearch(params)

    results = search.get_dict()
    
    articles = results.get("articles", [])

    for article in articles:
        cleaned_article = {
            "title": article.get("title"),
            "link": article.get("link"),
            "citation_id": article.get("citation_id"),
            "authors": article.get("authors"),
            "publication": article.get("publication"),
            "year": article.get("year")
        }
        author_article_results_data.append(cleaned_article)

    if "next" in results.get("serpapi_pagination", {}):
        print(f"Next link: {results['serpapi_pagination']['next']}")
        query_params = dict(parse_qsl(urlsplit(results['serpapi_pagination']['next']).query))
        params.update(query_params)
    else:
        articles_is_present = False

    next_start += 20

# Sort the list by year, from most recent to oldest
author_article_results_data_sorted = sorted(author_article_results_data, key=lambda x: x.get("year", "0"), reverse=True)

# Write the sorted list to a file
with open("author_pub_out_sorted.json", "w") as outfile:
    json.dump(author_article_results_data_sorted, outfile, indent=4)  # Using indent for better readability

print("All pages done with sorting by year!")
