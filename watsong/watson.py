"""
This file is a starter for any Watson stuff that needs to happen.
"""

import os
from typing import List

from ibm_cloud_sdk_core.authenticators import IAMAuthenticator  # type: ignore
from ibm_watson import DiscoveryV1  # type: ignore

from .structures import AlbumDescription, Result

apikey = os.getenv("DISCOVERY_API_KEY")
environment_id = "26e276ef-e35e-4076-a190-bab90b5a4521"
collection_id = "3789d265-dda2-465a-98fb-e804f1435317"
service_url = "https://api.us-south.discovery.watson.cloud.ibm.com/instances/230365e2-48ca-4b2f-8a9e-3dba5fbe20ed"
version = "2019-04-30"

authenticator = IAMAuthenticator(apikey)
discovery = DiscoveryV1(version=version, authenticator=authenticator)
discovery.set_service_url(service_url)


def get_albums(query: str) -> Result[List[AlbumDescription]]:
    """
    Given a natural language query, use watson to return the best albums for that query.
    """
    reqd_fields = "title, author"
    count = 50
    albums = []
    error = None

    try:
        response = discovery.query(
            environment_id,
            collection_id,
            natural_language_query=query,
            count=count,
            return_=reqd_fields,
            x_watson_logging_opt_out=True,
        )
        results = response.get_result()
        for result in results["results"]:
            album_desc = AlbumDescription(result["title"], result["author"].split(", "))
            albums.append(album_desc)
    except Exception as e:
        error = e

    return albums, error
