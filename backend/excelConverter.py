import pandas as pd


class CreateExcel():
    def __init__(self, data):
        self.data = data

    def createExl(self):
        df = pd.DataFrame(self.data)
        df_transpuesto = df.transpose()
        archivo_excel = 'resultadosExcel.xlsx'
        df_transpuesto.style.set_properties(**{'text-align': 'center'}).to_excel(archivo_excel)
        return archivo_excel
