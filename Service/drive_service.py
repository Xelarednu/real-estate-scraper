from Controller.drive_controller import DriveController
import datetime

class DriveService():
    def __init__(self, drive_controller: DriveController):
        self.drive_controller = drive_controller

    def upload_to_drive(self) -> None:
        self.drive_controller.upload_file(f"results/result_{datetime.date.today().strftime('%Y-%m-%d')}.xlsx")