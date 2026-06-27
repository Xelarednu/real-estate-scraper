import requests
from bs4 import BeautifulSoup
import time
import pandas as pd
from pathlib import Path
import Model

model = Model.Model()

url = "https://api.city24.ee/en_GB/search/realties"

headers = {
    "User-Agent": "Leaper/1.0",
    "Accept-Language": "en-US,en;q=0.9",
    "Host": "api.city24.ee",
    "Accept": "application/json,",
    "Accept-Encoding": "gzip, deflate, br, zstd",
    "Referer": "https://www.city24.ee/en/real-estate-search/apartments-for-sale/narva-linn/id=117-parish/sort=price-asc",
    "x-anon-token": "1781732889de3ce6ae-c16f-4f81-8d15-bdcc846a1a52",
    "Origin": "https://www.city24.ee",
    "Sec-GPC": "1",
    "Connection": "keep-alive",
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": 'cors',
    "Sec-Fetch-Site": "same-site",
    "If-None-Match": "W/'09afa4dcb7a2ef9dec228be504eaeefc'",
    "Priority": "u=4",
    "TE": "trailers",
}

def export_to_excel(data: dict):
    data_frame = pd.DataFrame(data)
    data_frame.to_excel("result.xlsx", index=False)

def get_estates():
    wipe_raw_table()

    page_number = 1

    while True:
        params = {"":"","address[cc]":"1","address[parish][]":"117","tsType":"sale","unitType":"Apartment","order[price]":"asc","adReach":"1","itemsPerPage":"100","page":f"{page_number}"}
        time.sleep(2)
        response = requests.get(url, headers=headers, params=params)
        if (response.status_code == 200):
            data = response.json()
            if (data == []):
                break

            for estate in data:
                estate_id = int(estate["id"])
                street_name = estate["address"]["street_name"]
                house_number = estate["address"]["house_number"]
                price = int(estate["price"].split(".")[0])
                price_per_unit = estate["price_per_unit"]
                property_size = float(estate["property_size"])
                room_count = estate["room_count"]
                date_published = estate["date_published"].split("T")[0]
                is_sold = False

                if (street_name == None):
                    street_name = ""
                if (house_number == None):
                    house_number = ""
                
                if (price_per_unit == None):
                    price_per_unit = 0.0
                else:
                    float(price_per_unit)
                
                entry = (estate_id, street_name + " " + house_number, price, price_per_unit, property_size, room_count, date_published, is_sold)

                model.insert(entry, "estates_raw")
            
            page_number += 1
        else:
            print("Failed with: ", response.status_code)

def update_sold_status():
    model.update_sold_status()

def wipe_raw_table() -> None:
    model.delete_all("estates_raw")

get_estates()
model.insert_multiple(model.get_all("estates_raw"), "estates_final")
update_sold_status()
export_to_excel(model.get_all("estates_final"))