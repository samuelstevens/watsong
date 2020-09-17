import os
import json
import sqlite3
from typing import Any, Tuple
from sqlite3 import Error
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


def get_reviews(conn: Any) -> Tuple[Tuple[str,str,str]]:
    """ 
    Get reviews from database
    """
    cur = conn.cursor()
    query = r"SELECT title, artist, content FROM reviews, content where reviews.reviewid = content.reviewid"
    cur.execute(query)

    return cur.fetchall()

def upload_reviews(reviews: Tuple[Tuple[str,str,str]], apikey: str, service_url: str, environment_id: str, collection_id: str, version: str = "2019-04-30") -> None:
    authenticator = IAMAuthenticator(apikey)
    discovery = DiscoveryV1(
        version=version,
        authenticator=authenticator
    )
    discovery.set_service_url(service_url)

    for review in reviews:
        data = {"title":review[0], "author":review[1], "text":review[2]}
        fname = review[0] + ".json"

        with open(fname,"w+") as fp:
            json.dump(data, fp)
            fp.seek(0)
            add_doc = discovery.add_document(
                environment_id,
                collection_id,
                file = fp).get_result()
        print(add_doc)
        os.remove(fname)
    return




def main():
    database = r"dataset.sqlite"
    apikey = "L8vZ5k9U8L8r8r9YstxDbOml0imvZBYmj7bB_tiVQ2GS"
    environment_id = "26e276ef-e35e-4076-a190-bab90b5a4521"
    collection_id = "f9541bb4-22a0-4762-b7bb-c80bf46d1ee2"
    service_url = "https://api.us-south.discovery.watson.cloud.ibm.com/instances/230365e2-48ca-4b2f-8a9e-3dba5fbe20ed"


    # create a database connection
    conn = create_connection(database)
    with conn:
        reviews = get_reviews(conn)
    conn.close()
    upload_reviews(reviews,apikey, service_url, environment_id, collection_id)

    


if __name__ == '__main__':
    main()





