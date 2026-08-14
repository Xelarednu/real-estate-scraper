from Service.city24_service import City24Service
from Service.drive_service import DriveService
from Controller.city24_controller import City24Controller
from Controller.drive_controller import DriveController
from Model.city24_model import Model
from app import App

def main():
    model = Model()

    city24_controller = City24Controller(model)
    drive_controller = DriveController()

    city24_service = City24Service(city24_controller)
    drive_service = DriveService(drive_controller)

    app = App(city24_service, drive_service)
    app.run()

if __name__ == "__main__":
    main()