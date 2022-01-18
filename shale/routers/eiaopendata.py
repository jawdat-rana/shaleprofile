import json
from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel
import requests
import datetime
import uuid
from typing import List, Optional

router = APIRouter()


############################################################
# Data Access Object
class OpenDataClass:

    def __init__(self):

        self.API_KEY = "496gcFK6q6e2WNkXYFQD12wWNzTLYR3FqzyDdNlc"

    def get_series(self, series_id):

        url = "https://api.eia.gov/series/?api_key={0}&series_id=NG.{1}".\
            format(self.API_KEY, series_id)

        try:
            page = requests.get(url)
        except Exception as err:
            raise Exception(err)

        else:
            if page.status_code == 200:

                return page.text

            else:
                print('Unable to retrieve page. Status Code {}'
                      .format(page.status_code))


DB = OpenDataClass()


# Data Models

class RequestResponseModel(BaseModel):
    command: str
    series_id: str


class SeriesResponseModel(BaseModel):
    series_id: str
    name: str
    units: str
    f: str
    unitsshort: str
    description: str
    copyright: str
    source: str
    iso3166: str
    geography: str
    start: str
    end: str
    updated: str
    data: List[List]


class OpenDataResponseModel(BaseModel):
    timestamp: str = '2008-09-15T15:53:00+05:00'
    uuid: str = 'bd65600d-8669-4903-8a14-af88203add38'
    request: Optional[RequestResponseModel]
    series: Optional[List[SeriesResponseModel]]


@router.get("/v1/shale/series/{series_id}", tags=["opendata"],
            response_model=OpenDataResponseModel)
def get_series(series_id: str):

    payload = json.loads(DB.get_series(series_id))

    payload['uuid'] = str(uuid.uuid4())
    payload['timestamp'] = str(datetime.datetime.now())

    return payload

