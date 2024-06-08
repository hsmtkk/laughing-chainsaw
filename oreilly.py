import requests
from pydantic import BaseModel, model_validator
from enum import StrEnum
from typing import Optional, Self

URL = "https://learning.oreilly.com/api/v2/search"


class Sort(StrEnum):
    relevance = "relevance"
    popularity = "popularity"
    date_added = "date_added"
    publication_date = "publication_date"
    average_rating = "average_rating"


class Order(StrEnum):
    asc = "asc"
    desc = "desc"


class SearchParams(BaseModel):
    query: str
    sort: Optional[Sort]
    order: Optional[Order]

    def __dict__(self):
        return {"query": self.query, "sort": self.sort, "order": self.order}


MAX_LENGTH = 1024


class SearchResponse(BaseModel):
    class SearchResult(BaseModel):
        id: str
        authors: list[str]
        title: str
        description: str
        url: str

        @model_validator(mode="after")
        def shorten_description(self) -> Self:
            self.description = self.description[:MAX_LENGTH]
            return self

    results: list[SearchResult]


def search(params: SearchParams) -> SearchResponse:
    resp = requests.get(URL, params=dict(params))
    parsed = SearchResponse.model_validate_json(resp.text)
    return parsed


if __name__ == "__main__":
    resp = search(SearchParams(query="python", sort=Sort.relevance, order=Order.desc))
    print(resp.model_dump_json(indent=2))
