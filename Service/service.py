from Controller.drive_controller import DriveController
from Controller.city24_controller import City24Controller
from Model.city24_model import Model

class City24Service():
    def __init__(self, drive: DriveController, city24: City24Controller):
        self.drive = drive
        self.city24: City24Controller = city24

    def scrape(self):
        self.city24.get_estates()

    def fill_final_table(self):
        self.city24.fill_final_table()

    def updates(self):
        self.city24.update_entries()
        self.city24.update_sold_status()

    def export(self):
        self.city24.export()