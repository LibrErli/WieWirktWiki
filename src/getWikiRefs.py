#!/usr/bin/env python
import re
import sys
from SPARQLWrapper import SPARQLWrapper, JSON

def get_results(endpoint_url, query):
    user_agent = "WDQS-example Python/%s.%s" % (sys.version_info[0], sys.version_info[1])
    # TODO adjust user agent; see https://w.wiki/CX6
    sparql = SPARQLWrapper(endpoint_url, agent=user_agent)
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    return sparql.query().convert()

def getMobileUrl(urlStr):
    regex = r"(.*)\.(.*wik.*)\.org"
    subst = r"\1.m.\2.org"
    result = re.sub(regex, subst, urlStr, 0, re.MULTILINE)
    return result

def getWikiUrlReferer():
    endpoint_url = "https://query.wikidata.org/sparql"

    query = """SELECT DISTINCT (REPLACE(REPLACE(STR(?url), "https://|http://", ""), "/$", "") AS ?wikiUrl) WHERE {
      ?wikiProject wdt:P1800 ?wikiKennung;
        wdt:P856 ?url.
    }"""
    resultSet = []
    results = get_results(endpoint_url, query)
    for result in results["results"]["bindings"]:
        resultSet.append(result["wikiUrl"]["value"])
        resultSet.append(getMobileUrl(result["wikiUrl"]["value"]))
    return resultSet
