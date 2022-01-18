import json
import datetime
import uuid

from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel
import requests
from bs4 import BeautifulSoup
import pandas as pd

router = APIRouter()


############################################################
# Data Access Object
class OverviewClass:

    def __init__(self):

        self.clean_urls = []
        self.link = "https://www.eia.gov/dnav/ng/ng_prod_shalegas_s1_a.htm"
        self.DATA_HTML = ''
        self.DATA_JSON = {}

        try:
            page = requests.get(self.link)
        except Exception as err:
            raise Exception(err)

        else:
            if page.status_code == 200:

                # extract links from page using BeautifulSoup
                soup = BeautifulSoup(page.content, 'html.parser')
                el = soup.find_all(href=True)

                # cleaning and transforming urls in required format
                for e in el:
                    if './hist/' in e['href']:
                        self.clean_urls.append(
                            e['href'].split('/')[2].split('.')[0]
                            .upper()[:-1] + '.A')
            else:
                print('Unable to retrieve page. Status Code {}'
                      .format(page.status_code))

        try:
            tables = pd.read_html(self.link)
        except Exception as err:
            self.Error = err
            raise Exception(self.Error)

        else:

            # selecting required table
            df = tables[4]

            # performing dataframe operations to make table in required format
            df.rename(columns={'Unnamed: 0_level_1': 'Area'}, inplace=True)
            df = df['Download Series History Definitions, Sources & Notes'][
                ['Area', '2015', '2016', '2017', '2018', '2019', '2020']]
            df['series_id'] = self.clean_urls

            # Replacing N/A values with 0 and 'W' withheld values with -9
            df = df.fillna(0)

            df['2017'] = df['2017'].replace('W', -9)
            df['2019'] = df['2019'].replace('W', -9)

            df['2017'] = pd.to_numeric(df['2017'])
            df['2019'] = pd.to_numeric(df['2019'])

            # storing formatted object in html and json format
            self.DATA_HTML = df.to_html()

            l = {}
            for index, row in df.iterrows():
                l[row[0]] = row[1:].to_json()

            self.DATA_JSON = json.dumps(l)

    def get_data(self, format):

        if format == "html":
            return self.DATA_HTML

        if format == "json":
            return self.DATA_JSON

    def get_data_by_area(self, area):
        data = json.loads(self.DATA_JSON)
        response_data = {}

        area_ = data.get(area, None)

        if area_ is None:
            return json.dumps({"Error": "Area '{}' not found".format(area)})

        response_data[area] = area_

        return json.dumps(response_data)


# Initializing Data Access Object
DB = OverviewClass()


# Data Models
class MarketResponseModel(BaseModel):
    timestamp: str
    uuid: str
    data: str


@router.get("/v1/shale/overview/", tags=["overview"],
            response_model=MarketResponseModel)
def get_market_overview(format: str = "html"):
    payload = dict()
    payload['uuid'] = str(uuid.uuid4())
    payload['timestamp'] = str(datetime.datetime.now())
    payload['data'] = DB.get_data(format)

    return payload


@router.get("/v1/shale/overview/{format}", tags=["overview"],
            response_model=MarketResponseModel)
def get_market_overview(format: str):
    payload = dict()
    payload['uuid'] = str(uuid.uuid4())
    payload['timestamp'] = str(datetime.datetime.now())
    payload['data'] = DB.get_data(format)

    return payload


@router.get("/v1/shale/overview/area/{area}", tags=["overview"],
            response_model=MarketResponseModel)
def get_market_overview_by_area(area: str):
    payload = dict()
    payload['uuid'] = str(uuid.uuid4())
    payload['timestamp'] = str(datetime.datetime.now())
    payload['data'] = DB.get_data_by_area(area)

    return payload
