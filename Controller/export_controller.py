import pandas as pd
import datetime
from Model.city24_model import Model

class ExportController():
    def __init__(self, model: Model):
        self.model = model

    def export_to_excel(self, data):
        columns = self.model.get_column_names()
        df = pd.DataFrame(data, columns=columns)
        df.to_excel(f"results/result_{datetime.date.today().strftime('%Y-%m-%d')}.xlsx", index=False)