from elasticsearch import Elasticsearch, helpers

es = Elasticsearch([{'host': 'localhost', 'port':9200}])

query_string = ""

#basic search query
def basic_search_query():
    return {
            "query": {
                "query_string": {
                    "query": "1896 பிறப்பு"
                }
            }
        }

#bool query
def bool_query():
    return {
            "query": {
                "bool" : {
                    "must" : [
                       {"match": { "பெயர்": "பாலகுமாரன்" }},
                       {"match": { "பிறந்த இடம்": "பழமானேரி தஞ்சாவூர் மாவட்டம் தமிழ்நாடு"}}
                    ],
                    "must_not" : {
                        "range" : {
                        "வயது" : { "gte" : 50, "lte" : 30 }
                        }
                    }
                }
            }
        }

#simple match query
def match_query():
    return {
            "query": {
                "match": {
                    "பெயர்": {
                        "query": "கனகலிங்கம்",
                        "fuzziness": "AUTO"
                    }
                }
            }
        }

#match bool prefix query
def match_bool_prefix_query():
    return {
        "query": {
            "match_bool_prefix" : {
                "சுருக்கம்" : "பிஏ பட்டம் பெற்று*"
                }
            }
        }

#match phrase query
def match_phrase_query():
    return {
        "query": {
            "match_phrase": {
                "தகவல்": "தமிழ் எழுத்தாளர்"
                }
            }
        }


#wildcard query
def wildcard_query(query):
    return {
        "query": {
            "query_string": {
                "query": "ஸ்ரீ இராமகிருஷ்ண மட*"
            }
        }
    }

#range query
def range_query(date, range):
    return{
        "query":{
            "range": {
                "வயது": {
                    "lte": 50
                }
            }
        }
    }

#more like this query
def more_like_this_query(field_array, query ):
    return {
            "query":{
                "more_like_this":{
                    "fields":["தகவல்", "சுருக்கம்", "முக்கிய வார்த்தைகள்"],
                    "like":"சிறுவர் இதழில் சேர்ந்து 42 ஆண்டுகள் குமுதம் இதழில் ஆசிரியர் குழுவி",
                    "min_term_freq":1,
                    "max_query_terms":20
                }
            }
        }

#agg_ multimatch
def agg_term_multimatch_query():
    return {
        "_source":{
        "excludes":["முக்கிய வார்த்தைகள்","அறியப்படுவது", "தகவல்"]
        },
        "size":10,
        "sort" : [
            { "வயது" : {"order" : "desc"}}
        ],
        "query": {
            "multi_match": {
                "fields":["பட்டம்", "தகவல்", "சுருக்கம்", "முக்கிய வார்த்தைகள்"],
                "query" : "சாகித்திய அகாதமி விருது",
                "fuzziness": "AUTO"
            }
        },
        "aggs": {
            "பிறந்த இடம்": {
                "terms": {
                    "field": "பிறந்த இடம்",
                    "size" : 20    
                }        
            },
            "இருப்பிடம்": {
                "terms": {
                    "field":"இருப்பிடம்",
                    "size" : 20
                }             
            }
        }
    }

#agg_range_query
def agg_range_multimatch_query():
    return {
        "_source":{
        "excludes":["முக்கிய வார்த்தைகள்","அறியப்படுவது", "தகவல்"]
        },
        "query": {
            "multi_match": {
                "fields":["பட்டம்", "தகவல்", "சுருக்கம்", "முக்கிய வார்த்தைகள்"],
                "query" : "கலைமாமணி விருது",
                "fuzziness": "AUTO"
            }
        },
        "aggs": {
            "age_ranges": {
            "range": {
                "field": "வயது",
                "ranges": [
                    { "to": 30 },
                    { "from": 30, "to": 50 },
                    { "from": 50 }
                ]
            }
            }
        }
    }
        





