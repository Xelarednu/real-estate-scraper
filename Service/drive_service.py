from Controller.drive_controller import DriveController
import datetime

class DriveService():
    def __init__(self, drive: DriveController):
        self.drive = drive

    def upload_to_drive(self) -> None:
        self.drive.upload_file(f"results/result_{datetime.date.today().strftime('%Y-%m-%d')}.xlsx")