import requests
from abc import ABCMeta
from tenacity import (
    retry,
    wait_random,
    stop_after_attempt,
)

class RestClient:
   
    def __init__(self):
        ...
        
    def build_url(self, params:dict):
        ...
    
    @retry(stop=stop_after_attempt(3), wait=wait_random(min=1, max=2))
    def request(self, params:dict):
        url = self.build_url(url_params)
        response = request.get(url)
        response.raise_for_status()
        return response
