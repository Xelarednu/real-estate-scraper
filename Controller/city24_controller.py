import requests
# from bs4 import BeautifulSoup
import time
import pandas as pd
import datetime
from pathlib import Path
from Model.city24_model import Model

class City24Controller():
    URL = "https://api.city24.ee/en_GB/search/realties"

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

    def __init__(self, model: Model):
        self.model = model

    def export_to_excel(self, data: dict):
        columns = self.model.get_column_names()
        data_frame = pd.DataFrame(data, columns=columns)
        data_frame.to_excel(f"results/result_{datetime.date.today().strftime('%Y-%m-%d')}.xlsx", index=False)

    def get_estates(self):
        self.__wipe_raw_table()

        page_number = 1

        while True:
            params = {"":"","address[cc]":"1","address[parish][]":"117","tsType":"sale","unitType":"Apartment","order[price]":"asc","adReach":"1","itemsPerPage":"100","page":f"{page_number}"}
            time.sleep(2)
            response = requests.get(self.URL, headers=self.headers, params=params)
            if (response.status_code == 200):
                data = response.json()
                if (data == []):
                    break

                for estate in data:
                    estate_id = int(estate["id"])
                    street_name = estate["address"]["street_name"]
                    parish_name = estate["address"]["parish_name"]
                    city_name = estate["address"]["city_name"]
                    house_number = estate["address"]["house_number"]
                    price = int(estate["price"].split(".")[0])
                    price_per_unit = estate["price_per_unit"]
                    property_size = float(estate["property_size"])
                    room_count = estate["room_count"]
                    date_published = estate["date_published"].split("T")[0]

                    if (parish_name == None):
                        parish_name = ""
                    if (city_name == None):
                        city_name = ""
                    if (street_name == None):
                        street_name = ""
                    if (house_number == None):
                        house_number = ""
                    if (price_per_unit == None):
                        price_per_unit = 0.0
                    else:
                        float(price_per_unit)
                    
                    link = self.__link_builder(parish_name, city_name, street_name, estate["friendly_id"])

                    entry = (estate_id, street_name + " " + house_number, price, price_per_unit, property_size, room_count, date_published, link)

                    self.model.insert(entry, "estates_raw")
                
                page_number += 1
            else:
                print("Failed with: ", response.status_code)

    def __wipe_raw_table(self) -> None:
        self.model.delete_all("estates_raw")

    def __link_builder(self, parish_name: str, city_name: str, street_name: str, friendly_id: str) -> str:
        link = "https://www.city24.ee/en/real-estate/apartments-for-sale/"

        names_list = self.__est_letters_check([parish_name, city_name, street_name])

        # Parish name
        link += names_list[0].lower() + " "
        # City name
        link += names_list[1].lower() + " "
        # Street name
        link += names_list[2].lower() + "/"
        link += friendly_id

        formatted_link = link.replace(" ", "-")

        return formatted_link

    def __est_letters_check(self, names_list: list) -> list:
        names_list_formatted = []

        for name in names_list:
            if ("ä" in name):
                name = name.replace("ä", "a")
            if "ö" in name:
                name = name.replace("ö", "o")
            if "ü" in name:
                name = name.replace("ü", "u")
            if "õ" in name:
                name = name.replace("õ", "o")
            names_list_formatted.append(name)
        return names_list_formatted

    def update_sold_status(self):
        self.model.update_sold_status('estates_raw', 'estates_final')

    def update_entries(self):
        self.model.update_estates('estates_raw', 'estates_final')

    def fill_final_table(self) -> None:
        self.model.insert_multiple(self.model.get_all("estates_raw"), "estates_final")

    def export(self) -> None:
        self.export_to_excel(self.model.get_all("estates_final"))
