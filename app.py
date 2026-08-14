from Service.city24_service import City24Service
from Service.drive_service import DriveService
from Controller.drive_controller import DriveController
from Controller.city24_controller import City24Controller
from Model.city24_model import Model

city24 = City24Service(City24Controller(Model()))
drive = DriveService(DriveController())

city24.scrape()
city24.fill_final_table()
city24.updates()
city24.export()
drive.upload_file()