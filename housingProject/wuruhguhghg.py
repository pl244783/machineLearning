#https://scrapfly.io/blog/how-to-scrape-zillow/ is nice

from urllib.parse import urlencode
import json
import httpx
import csv

# we should use browser-like request headers to prevent being instantly blocked
BASE_HEADERS = {
    "accept-language": "en-US,en;q=0.9",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36",
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
    "accept-language": "en-US;en;q=0.9",
    "accept-encoding": "gzip, deflate, br",
}


url = "https://www.zillow.com/search/GetSearchPageState.htm?"
parameters = {
    "searchQueryState": {
        #probably can just cycle every like 14 apges using a for loop tbh, i'll implement it in the future if I wasn't feeling lazy and knew that i could do this by hand 
        #urghghr they limit to 20 pages
        "pagination": {},
        "usersSearchTerm": "Port Saint Lucie FL 34987",
        "mapBounds": {
            "west": -80.7211690595703,
            "east": -80.35724694042968,
            "south": 27.12403130845633,
            "north": 27.457818138794696
        },
        "regionSelection": [
            {
                "regionId": 73248,
                "regionType": 7
            }
        ],
        "isMapVisible": False,
        "filterState": {
            "sort": {
                "value": "globalrelevanceex"
            },
            "ah": {
                "value": True
            },
            "rs": {
                "value": True
            },
            "fsba": {
                "value": False
            },
            "fsbo": {
                "value": False
            },
            "nc": {
                "value": False
            },
            "cmsn": {
                "value": False
            },
            "auc": {
                "value": False
            },
            "fore": {
                "value": False
            },
            "doz": {
                "value": "6m"
            }
        },
        "isListVisible": True,
        "mapZoom": 11
    },
    "wants": {
        "cat1": ["listResults", "mapResults"],
        "cat2": ["total"]
    },
    "requestId": 2,
}

response = httpx.get(url + urlencode(parameters), headers=BASE_HEADERS)
assert response.status_code == 200, "request has been blocked"
data = response.json()
results = response.json()["cat1"]["searchResults"]["mapResults"]
#results
print(json.dumps(results, indent=2))

#temp saving lmao
# f = open("housingProject/data/32953PortLucie.txt", "w")
# f.write(json.dumps(results, indent=2))
# f.close()

#brainrot time
headers = ["zpid", "streetAddress", "zipcode", "price", "bathrooms", "bedrooms", "livingArea", "homeType", "lotAreaValue"]

tempFile = "housingProject/data/34987PortLucie.csv"
with open(tempFile, 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    #writer.writerow(headers)
    for item in results:
        zpid = item.get("zpid", "")
        street_address = item.get("hdpData", {}).get("homeInfo", {}).get("streetAddress", "")
        zipcode = item.get("hdpData", {}).get("homeInfo", {}).get("zipcode", "")
        price = item.get("hdpData", {}).get("homeInfo", {}).get("price", "")
        bathrooms = item.get("hdpData", {}).get("homeInfo", {}).get("bathrooms", "")
        bedrooms = item.get("hdpData", {}).get("homeInfo", {}).get("bedrooms", "")
        living_area = item.get("hdpData", {}).get("homeInfo", {}).get("livingArea", "")
        home_type = item.get("hdpData", {}).get("homeInfo", {}).get("homeType", "")
        lot_area_value = item.get("hdpData", {}).get("homeInfo", {}).get("lotAreaValue", "")

        writer.writerow([zpid, street_address, zipcode, price, bathrooms, bedrooms, living_area, home_type, lot_area_value])

print(f"found {len(results)} property results")

# from loguru import logger as log
# from urllib.parse import quote
# import httpx
# import re
# import random

# async def _search(query:str, session: httpx.AsyncClient, filters: dict=None, categories=("cat1", "cat2")):
#     """base search function which is used by sale and rent search functions"""
#     html_response = await session.get(f"https://www.zillow.com/homes/{query}_rb/")
#     # find query data in search landing page
#     print(r'"queryState":(\{.+}),\s*"filter', html_response.text, '\n', "WEEEWOWOOWOWOEOW EOWE OEWO EWO EWO WEO WEO EOOWE OOEWOWEOOWOEOW EWOWE ")
#     query_data = json.loads(re.findall(r'"queryState":(\{.+}),\s*"filter', html_response.text)[0])
#     #why is this saying that list index is out of range :/
#     if filters:
#         query_data["filterState"] = filters

#     # scrape search API
#     url = "https://www.zillow.com/search/GetSearchPageState.htm?"
#     found = []
#     # cat1 - Agent Listings
#     # cat2 - Other Listings
#     for category in categories:
#         full_query = {
#             "searchQueryState": json.dumps(query_data),
#             "wants": json.dumps({category: ["mapResults"]}),
#             "requestId": random.randint(2, 10),
#         }
#         api_response = await session.get(url + urlencode(full_query, quote_via=quote))
#         data = api_response.json()
#         _total = data["categoryTotals"][category]["totalResultCount"]
#         if _total > 500:
#             log.warning(f"query has more results ({_total}) than 500 result limit ")
#         else:
#             log.info(f"found {_total} results for query: {query}")
#         map_results = data[category]["searchResults"]["mapResults"]
#         found.extend(map_results)
#     return found


# async def search_sale(query: str, session: httpx.AsyncClient):
#     """search properties that are for sale"""
#     log.info(f"scraping sale search for: {query}")
#     return await _search(query=query, session=session)


# async def search_rent(query: str, session: httpx.AsyncClient):
#     """search properites that are for rent"""
#     log.info(f"scraping rent search for: {query}")
#     filters = {
#         # "isForSaleForeclosure": {"value": False},
#         # "isMultiFamily": {"value": False},
#         # "isAllHomes": {"value": True},
#         # "isAuction": {"value": False},
#         # "isNewConstruction": {"value": False},
#         # "isForRent": {"value": False},
#         # "isLotLand": {"value": False},
#         # "isManufactured": {"value": False},
#         # "isForSaleByOwner": {"value": False},
#         # "isComingSoon": {"value": False},
#         # "isForSaleByAgent": {"value": False},
#         "doz": {"value": "6m"},
#         "ah": {"value":True},
#         "rs":{"value":True},
#         "fsba":{"value":False},
#         "fsbo":{"value":False},
#         "nc":{"value":False},
#         "cmsn":{"value":False},
#         "auc":{"value":False},
#         "fore":{"value":False}
#     }
#     return await _search(query=query, session=session, filters=filters, categories=["cat1"])

# import asyncio
# async def run():
#     limits = httpx.Limits(max_connections=5)
#     async with httpx.AsyncClient(limits=limits, timeout=httpx.Timeout(15.0), headers=BASE_HEADERS) as session:
#         data = await search_rent("Port Saint Lucie, FL", session)
#         print(json.dumps(data, indent=2))


# if __name__ == "__main__":
#     asyncio.run(run())
