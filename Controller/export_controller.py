import pandas as pd
import datetime

class ExportController():
    def export_to_excel(self, data, columns) -> None:
        df = pd.DataFrame(data, columns=columns)
        df.to_excel(f"results/result_{datetime.date.today().strftime('%Y-%m-%d')}.xlsx", index=False)