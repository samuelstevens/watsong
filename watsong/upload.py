import os
import json
import sqlite3
import random
import training
from spotify import get_playlist_features, get_playlist_ids
from typing import Any, Tuple, Dict
from sqlite3 import Error
from sqlite3 import OperationalError
from ibm_watson import DiscoveryV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator


def create_connection(db_path: str) -> Any:
    """
    Create a database connection to the SQLite database specified by the db_file
    """
    conn = None
    try:
        conn = sqlite3.connect(db_path)
    except Error as e:
        print(e)

    return conn


def get_reviews(conn: Any) -> Tuple[Tuple[int, str, str, str]]:
    """
    Get reviews from database
    """
    cur = conn.cursor()
    query = r"SELECT reviews.reviewid, title, artist, content FROM reviews, content where reviews.reviewid = content.reviewid AND reviews.score > 8 limit 950"
    cur.execute(query)

    return cur.fetchall()

def insert_mapping(conn: Any, document_mapping: Dict[int, str]) -> None:
    cur = conn.cursor()
    clear_col_query = r"UPDATE reviews SET documentID = NULL"
    add_col_query = r"ALTER TABLE reviews add documentID varchar(255)"
    print(len(document_mapping))
    try:
        cur.execute(add_col_query)
    except OperationalError as e:
        print(e)
        print("Updating column")
    cur.execute(clear_col_query)
    for review_id in document_mapping:
        query = f"UPDATE reviews SET documentID = \'{document_mapping[review_id]}\' WHERE reviews.reviewid = {review_id}"
        cur.execute(query)
    return


def train(conn, query, apikey: str, service_url: str, environment_id: str, collection_id: str, version: str = "2019-04-30"):
    cur = conn.cursor()
    docs_query= r"SELECT documentID, title, artist from reviews where documentID is not null"
    docs = cur.execute(docs_query)

    authenticator = IAMAuthenticator(apikey)
    discovery = DiscoveryV1(version=version, authenticator=authenticator)
    discovery.set_service_url(service_url)

    examples = []
    while True:
        try:
            features = get_playlist_features(get_playlist_ids(query,3))
            break
        except Exception:
            continue

    print(features)
    sample = random.sample(list(docs),200)
    count = 0

    for doc in sample:
        if count == 100:
            break
        example_obj = {}
        try:
            score = training.gen_proc(features,doc[1:])
            count += 1
        except Exception as e:
            print(e)
            continue
        if score>=.8:
            example_obj["relevance"] = 2
        elif score>.5:
            example_obj["relevance"] = 1
        else:
            example_obj["relevance"] = 0
        example_obj["document_id"] = doc[0]
        print(example_obj)
        examples.append(example_obj)
    print(examples)
    discovery.add_training_data(environment_id, collection_id, natural_language_query=query, filter=None, examples=examples)



def upload_reviews(
    reviews: Tuple[Tuple[int, str, str, str]],
    apikey: str,
    service_url: str,
    environment_id: str,
    collection_id: str,
    version: str = "2019-04-30",
) -> Dict[int, str]:
    """
    Upload reviews to Watson Discovery
    """
    document_mapping = {}
    try:
        authenticator = IAMAuthenticator(apikey)
        discovery = DiscoveryV1(version=version, authenticator=authenticator)
        discovery.set_service_url(service_url)

        for review in reviews:
            data = {"title": review[1], "author": review[2], "text": review[3]}
            fname = str(review[0]) + ".json"

            with open(fname, "w+") as fp:
                json.dump(data, fp)
                fp.seek(0)
                add_doc = discovery.add_document(
                    environment_id, collection_id, file=fp
                ).get_result()
            document_mapping[review[0]] = add_doc["document_id"]
            print(add_doc)
            os.remove(fname)
    except Exception as e:
        print(e)
    return document_mapping


def main():
    database = r"dataset.sqlite"
    apikey = os.getenv("DISCOVERY_API_KEY")
    environment_id = "26e276ef-e35e-4076-a190-bab90b5a4521"
    collection_id = "8a0447cb-01c3-48a1-8f5c-d9150f001975"
    service_url = "https://api.us-south.discovery.watson.cloud.ibm.com/instances/230365e2-48ca-4b2f-8a9e-3dba5fbe20ed"
    inp = input("Enter your query - ")
    # create a database connection
    conn = create_connection(database)
    with conn:
        train(conn,inp,apikey,service_url,environment_id,collection_id)
        # reviews = get_reviews(conn)
    conn.close()
    # document_mapping = upload_reviews(reviews, apikey, service_url, environment_id, collection_id)
    # conn = create_connection(database)
    # with conn:
    #     insert_mapping(conn, document_mapping)
    # conn.close()



if __name__ == "__main__":
    main()