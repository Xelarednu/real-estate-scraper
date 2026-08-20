from Controller.export_controller import ExportController
from Model.city24_model import Model

class ExportService():
    def __init__(self, export_controller: ExportController, model: Model):
        self.export_controller = export_controller
        self.model = model

    def export(self) -> None:
        self.export_controller.export_to_excel(self.model.get_all("estates_final"), self.model.get_column_names())