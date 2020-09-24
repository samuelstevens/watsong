"""
This file is a starter for any Watson stuff that needs to happen.
"""

from typing import List
from .structures import AlbumDescription, Result
import os
from ibm_watson import DiscoveryV1  # type: ignore
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator  # type: ignore


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
    return [], None
