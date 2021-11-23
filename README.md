# TamilWriterIRSystem

Implemented as part of the CS4642 - Data Mining & Information Retrieval. 

Task : Creating an information retrieval system on famous people. This system is based on famous writers made using the native language **Tamil**.

**_Dataset_**
Dataset : **227** records on famous writers (in Tamil)

__Pre-requisites__

  1. Wikipedia and BeautifulSoup python modules for scraping data
  2. Nltk library for cleaning data
  3. ElasticSearch for indexing data

**_Project Components_** 
  1. Scraping 
  2. Preprocessing
  3. Indexing
  4. Querying 

**_Directory Structure_**

```
Project
│   │   README.md
│   │   scraper.py - Scraping functions and saving raw data
|   │   pre-processing.py - Preprocessing functions and saving pre-processed data 
|   │   upload_data.py  - Indexing data into Elasticsearch 
│   │   search.py - Queries executed on the indexed data
└───dataset
│   │   famous_writer_raw.json - Raw scraped data from scraper.py
│   │   famous_writer_preprocessed.json - Cleaned data from preeprocessing.py
│   
└───image - Architecture and Pipeline diagrams
    │   Architecture_IR_System image

```

**_Project Architecture_**

    
![ArchitectureIRSystem](https://github.com/KrishPraba/TamilWriterIRSystem/blob/master/image/Architecture_IR_System.PNG)




## Data Scraping

Data was scraped using [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/) and [wikipedia](https://pypi.org/project/wikipedia/) python libraries used for web scraping. 

Scraping was done in two phases :

_Phase 1 :_

List of famous writers was scraped from two Tamil Wikipedia pages using BeautifulSoup

1. [First List of Tamil Writers from Wikipedia](https://ta.wikipedia.org/wiki/%E0%AE%A4%E0%AE%AE%E0%AE%BF%E0%AE%B4%E0%AF%8D_%E0%AE%8E%E0%AE%B4%E0%AF%81%E0%AE%A4%E0%AF%8D%E0%AE%A4%E0%AE%BE%E0%AE%B3%E0%AE%B0%E0%AF%8D%E0%AE%95%E0%AE%B3%E0%AF%8D_%E0%AE%AA%E0%AE%9F%E0%AF%8D%E0%AE%9F%E0%AE%BF%E0%AE%AF%E0%AE%B2%E0%AF%8D) 

2. [Second List of Tamil Writers from Wikipedia](https://ta.wikipedia.org/wiki/%E0%AE%AA%E0%AE%95%E0%AF%81%E0%AE%AA%E0%AF%8D%E0%AE%AA%E0%AF%81:%E0%AE%A4%E0%AE%AE%E0%AE%BF%E0%AE%B4%E0%AF%8D_%E0%AE%8E%E0%AE%B4%E0%AF%81%E0%AE%A4%E0%AF%8D%E0%AE%A4%E0%AE%BE%E0%AE%B3%E0%AE%B0%E0%AF%8D%E0%AE%95%E0%AE%B3%E0%AF%8D)

_Phase 2 :_

Using the writer list information on the writers was scraped from their respective wikipedia pages using BeautifulSoup and wikipedia. The collected data contained information on the following **13** metafields on each writer. One field is an integer and the rest are text. Of the 12 text fields 2 text fields are full text with over 50 tokens. 

- பெயர் - Name (Text)
- சுருக்கம் - Introduction (Full Text)
- தகவல் - Content (Text)
- இறப்பு - Date and Place of death(Full Text)
- தேசியம் - Nationality (Text)
- பிறப்பு = Date of Birth (Text)
- எழுதிய நூல்கள் - Novels written (Text)
- பட்டம் - Honorary titles recieved (Text)
- இருப்பிடம் - Place of residence (Text)
- அறியப்படுவது - Achievements (Text)
- முக்கிய வார்த்தைகள் - Keywords that can be used to identify writers (Text)
- வயது - Age lived (Number)
- பிறந்த இடம் - Place of birth (Text)



## Data Preprocessing

Significant preprocessing was done on most of the text fields. Especially on the two full text fields. Major preprocessing tasks carried out were as follows:
1. Removing punctuations from the text fields
2. Removing english alphabet letters from the text fields
3. Extracting the age from the Date of Birth and Date of Death
4. Spliting the Date of Birth and Place of Birth into separate fields
5. Listing the novels written by writer from the extracted data as an array





## Indexing

Cleaned data was indexed in Elasticsearch using the Bulk API of Elasticsearch python client. 

A custom analyzer was created with on the text fields with appropriate custom filters. The custom filter contained tamil_stopper, indic_normalizer and tamil_stemmer for removing stopwords, normalizing Unicode representation of text and stemming the text. The custom analyzer was added when creating the index.

 ```json
{
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

```

Full text fields and fields that need to be analyzed when querying was set when mapping properties. The fields that was set to be analyzed were :

- சுருக்கம் - Introduction (Full Text)
- தகவல் - Content (Text)
- தேசியம் - Nationality (Text)
- இருப்பிடம் - Place of residence (Text)
- அறியப்படுவது - Achievements (Text)
- முக்கிய வார்த்தைகள் - Keywords that can be used to identify writers (Text)
- பிறந்த இடம் - Place of birth (Text)




## Querying

The queries queried on the dataset to retrieve information :

1. Basic Search Query
Performs basic searches on the query string across all fields that are eligible for term queries

2. Bool Query
Matches documents matching boolean combinations given in the query

3. Match Query
Performs a full-text search on the query text after analyzing text using custom analyzer. Includes options for fuzzy matching where maximum edit distance for spell correction can be specified.

4. Match_Bool_Prefix Query
Performs a boolean search from the terms.Each term except the last is used in a term query.The last term is used in a prefix query.

5. Match_Phrase Query
Similar to Bool Prefix query but searches for the phrase instead of separate terms.

6. Wildcard Query
Searches documents that contain terms matching a wildcard pattern as specified in the query text

7. Range Query
Searches documents that contain terms within a provided range specified in the query using lte (less than or equal to ) and gte (greater than or equal to)

8. More Like This Query
searches documents contains terms that are "like" the terms specified in the query

9. Multi Match Query with Term Aggregation
The multi_match query builds on the match query to allow multi-field to be searched on the query text. The results of this query are aggregated into buckets of unique terms in the fields specified

10. Multi Match Query with Range Aggregation
A multi match query results are aggregated into buckets with a set of ranges each representing a bucket


The query examples for each of this type of query is given in the **_search.py_** file
