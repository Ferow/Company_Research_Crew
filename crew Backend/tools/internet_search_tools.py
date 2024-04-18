import json
import os
from pydantic import BaseModel, Field
import requests

from langchain_community.tools import tool

class SearchInput(BaseModel):
    query: str = Field(description="Should be a search query")

class InternetSearchTool():
    @tool
    def searchInternet(query: str) -> str:
        """Search the internet tool"""
        top_ressults_to_return = 4
        
        url = "https://google.serper.dev/search"
        payload = json.dumps({
            "q": query
        })
        headers = {
            'X-API-KEY': os.environ.get("SERPER_API_KEY"),
            'Content-Type': 'application/json'
        }
        
        response = requests.request("POST", url, headers=headers, data=payload)
        #check if there is an organic key
        if "organic" not in response.json():
            return "Sorry I could not find anything about that, there could be an error in your serper api key"
        else:
            results = response.json()["organic"]
            string = []
            for result in results[:top_ressults_to_return]:
                try:
                    string.append('\n'.join([
                        f"Title: {result['title']}", f"Link: {result['link']}",
                        f"Snippet: {result['snippet']}", "\n-----------------"
                    ]))
                except KeyError:
                    next
            return '\n'.join(string)