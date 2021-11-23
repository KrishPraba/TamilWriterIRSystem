from elasticsearch import Elasticsearch, helpers
import json
import pprint



es = Elasticsearch([{'host': 'localhost', 'port':9200}])

# 'இறப்பு', 'தேசியம்', 'பிறப்பு', 'எழுதிய நூல்கள்', 'பட்டம்', 'இருப்பிடம்', 'அறியப்படுவது','முக்கிய வார்த்தைகள்',
# 'தகவல்','சுருக்கம்','பெயர்','வயது', 'பிறந்த இடம்']

def create_custom_analyzer():
    return {
            "settings" : {
                "analysis" : {
                    "analyzer" : {
                        "text_analyzer" : {
                            "tokenizer" : "standard",
                            "filter" : ["tamil_stopper","indic_normalization","tamil_stemmer"]
                        }
                    },
                    "filter" : {
                        "tamil_stemmer" : {
                            "type" : "hunspell",
                            "locale" : "ta_IN"
                        },
                        "tamil_stopper" : {
                            "type" : "stop",
                            "stopwords_path" : "tamilstop/stopwords.txt"
                        }
                    }
                }
            },
            "mappings" : {
                "properties" : {
                    "சுருக்கம்": {
                        "type" : "text",
                        "analyzer" : "text_analyzer"
                    },
                    "தகவல்" : {
                        "type" : "text",
                        "analyzer" : "text_analyzer"
                    },
                    "வயது" : {
                        "type" : "integer"
                    },
                    "முக்கிய வார்த்தைகள்" : {
                        "type" : "text",
                        "fielddata": true,
                        "analyzer": "text_analyzer"
                    },
                    "அறியப்படுவது" : {
                        "type" : "text",
                        "fielddata": true,
                        "analyzer": "text_analyzer"
                    },
                    "பிறந்த இடம்": {
                        "type" : "text",
                        "analyzer" : "text_analyzer",
                        "fielddata": true
                    },
                "தேசியம்": {
                        "type" : "text",
                        "analyzer" : "text_analyzer",
                        "fielddata": true
                    },
                    "இருப்பிடம்":{
                    "type" : "text",
                    "analyzer" : "text_analyzer",
                    "fielddata": true
                    }
                }
            }
        }

def read_data():
    with open('dataset/famous_writer_preprocessed.json') as f:
        data = json.load(f)
    return data

def genData(data_array):

    for data in data_array:
        பெயர் = data.get("பெயர்", None)
        இறப்பு = data.get("இறப்பு",None)
        தேசியம் = data.get("தேசியம்", None)
        பிறப்பு = data.get("பிறப்பு", None)
        எழுதிய_நூல்கள் = data.get("எழுதிய நூல்கள்", None)
        பட்டம் = data.get("பட்டம்", None)
        இருப்பிடம் = data.get("இருப்பிடம்", None)
        அறியப்படுவது = data.get("அறியப்படுவது", None)
        முக்கிய_வார்த்தைகள் = data.get("முக்கிய வார்த்தைகள்",None)
        தகவல் = data.get("தகவல்", None)
        சுருக்கம் = data.get("சுருக்கம்", None)
        வயது = data.get("வயது", None)
        பிறந்த_இடம் = data.get("பிறந்த இடம்", None)

        yield {
            "_index": "famous-writers",
            "_source": {
                "பெயர்": பெயர்,
                "இறப்பு": இறப்பு,
                "தேசியம்": தேசியம்,
                "பிறப்பு": பிறப்பு,
                "எழுதிய நூல்கள்": எழுதிய_நூல்கள்,
                "பட்டம்": பட்டம்,
                "இருப்பிடம்": இருப்பிடம்,
                "அறியப்படுவது": அறியப்படுவது,
                "முக்கிய வார்த்தைகள்": முக்கிய_வார்த்தைகள்,
                "தகவல்" : தகவல்,
                "சுருக்கம்" : சுருக்கம்,
                "வயது" : வயது,
                "பிறந்த இடம்" : பிறந்த_இடம்
            },
        }

final_data = read_data()

helpers.bulk(es, genData(final_data))