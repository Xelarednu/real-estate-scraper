from Service.city24_service import City24Service
from Service.drive_service import DriveService
from Service.export_service import ExportService

class App():
    def __init__(self, city24_service: City24Service, drive_service: DriveService, export_service: ExportService):
        self.city24_service = city24_service
        self.drive_service = drive_service
        self.export_service = export_service

    def run(self):
        self.city24_service.scrape()
        self.city24_service.fill_final_table()
        self.city24_service.updates()
        self.export_service.export()
        self.drive_service.upload_to_drive()