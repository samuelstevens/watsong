
import os
from typing import List
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson import DiscoveryV1
from .structures import AlbumDescription, Result

import json
from ibm_watson import NaturalLanguageUnderstandingV1
from ibm_watson.natural_language_understanding_v1 import Features, RelationsOptions, CategoriesOptions, ConceptsOptions, EmotionOptions, EntitiesOptions, KeywordsOptions
from statistics import fmean, mean


apikey = os.getenv("DISCOVERY_API_KEY")
environment_id = "26e276ef-e35e-4076-a190-bab90b5a4521"
collection_id = "a1b2c559-0cbd-4f5e-ad8b-228be6678b8a"
service_url = "https://api.us-south.discovery.watson.cloud.ibm.com/instances/230365e2-48ca-4b2f-8a9e-3dba5fbe20ed"
version = "2019-04-30"

authenticator = IAMAuthenticator(apikey)
discovery = DiscoveryV1(version=version, authenticator=authenticator)
discovery.set_service_url(service_url)

natural_language_understanding = NaturalLanguageUnderstandingV1(
    version='2020-08-01',
    authenticator=authenticator
)

natural_language_understanding.set_service_url('https://api.us-south.natural-language-understanding.watson.cloud.ibm.com/instances/af9781dd-bde5-4aaf-b3f3-2bfa19d9dbca')

def get_albums(query: str) -> Result[List[AlbumDescription]]:
    reqd_fields = "title, author"
    count = 50
    albums = []
    error = None

    # input (query) analysis throu nlu to get query for recommended albumns  
    response = natural_language_understanding.analyze(
        text = query,
        features = Features(
            keywords=KeywordsOptions(emotion=True, sentiment=True, limit=2)
            )).get_result()

    #json response of input 
    dump = json.dumps(response, indent=2)
    print(dump)
    dict_response = json.loads(dump)
    len_keyword = len(dict_response['keywords'])

    # keywords. text
    k_text = []

    # keywords sentiment 
    k_sentiment = []

    # emotion 
    # sad 
    k_sad = []
    # joy
    k_joy = []
    # fear
    k_fear = []
    # disgust
    k_disgust = []
    # anger
    k_anger = []

    for i in range(len_keyword):
        k_text.append(dict_response['keywords'][i]['text'])
        k_sentiment.append(float(dict_response['keywords'][i]['sentiment']['score']))
        k_sad.append(dict_response['keywords'][i]['emotion']['sadness'])
        k_joy.append(dict_response['keywords'][i]['emotion']['joy'])
        k_fear.append(dict_response['keywords'][i]['emotion']['fear'])
        k_disgust.append(dict_response['keywords'][i]['emotion']['disgust'])
        k_anger.append(dict_response['keywords'][i]['emotion']['anger'])

    # sentiment score 
    senti_score = fmean(k_sentiment)

    # sentiment label 
    if senti_score > 0: senti_label = "positive"
    elif senti_score < 0: senti_label = "negative"
    else: senti_label = "neutral"


    # sad score 
    avg_sad = mean(k_sad)
    # joy score 
    avg_joy = mean(k_joy)
    # fear score 
    avg_fear = mean(k_fear)
    # disgust score
    avg_disgust = mean(k_disgust)
    # anger score
    avg_anger = mean(k_anger)

    #query 
    # find albums that enriched_text.concepts.text = k_text,
    #                 enriched_text_.concepts.relevance>0.8
    #                 enriched_text_.sentiment.label = senti_label
    #                 enriched_text_.sentiment.score >?? senti_score
    #                 enriched_text.emotion.document.emotion.anger >?? , 
    #                 enriched_text.emotion.document.emotion.disgust>?? , 
    #                 enriched_text.emotion.document.emotion.joy>?? , 
    #                 enriched_text.emotion.document.emotion.anger>?? , 
    
    real_query = ""

    try:
        response = discovery.query(
            environment_id,
            collection_id,
            # natural_language_query=query,
            
            # not sure we shall use filter or query or aggregate 
            filter = real_query,

            count=count,
            return_=reqd_fields,
            deduplicate_field="title",
            x_watson_logging_opt_out=True,
        )
        results = response.get_result()
        for result in results["results"]:
            album_desc = AlbumDescription(result["title"], result["author"].split(", "))
            albums.append(album_desc)
    except Exception as e:
        error = e

    return albums, error





