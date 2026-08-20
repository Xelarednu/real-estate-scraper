from Controller.city24_controller import City24Controller
from Model.city24_model import Model

class City24Service():
    def __init__(self, city24: City24Controller, model: Model):
        self.city24: City24Controller = city24
        self.model = model

    def process(self):
        self.__wipe_raw_table()
        estates_list: list = self.city24.get_estates()
        self.__add_estates(estates_list)
        self.__updates()
        self.__fill_final_table()

    def __wipe_raw_table(self):
        self.model.delete_all("estates_raw")

    def __add_estates(self, estates: list):
        for estate in estates:
            self.model.insert(estate, "estates_raw")

    def __updates(self):
        self.model.update_estates('estates_raw', 'estates_final')
        self.model.update_sold_status('estates_raw', 'estates_final')

    def __fill_final_table(self):
        self.model.insert_multiple(self.model.get_all("estates_raw"), "estates_final")
