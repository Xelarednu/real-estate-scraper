from Service.service import City24Service
from Controller.drive_controller import DriveController
from Controller.city24_controller import City24Controller
from Model.city24_model import Model
import datetime

city24 = City24Service(DriveController(), City24Controller(Model()))
drive = DriveController()

city24.scrape()
city24.fill_final_table()
city24.updates()
city24.export()
drive.upload_file(f"results/result_{datetime.date.today().strftime('%Y-%m-%d')}.xlsx")