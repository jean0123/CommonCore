# libraries
import pandas as pd

class UsuariosBulk:
    # Columnas obligatorias
    columnas = [
        'username',
        'email',
        'first_name',
        'last_name',
        'password',
        'compania',
        'role'
    ]

    def __init__(self, archivo):
        self.archivo = archivo

    def transformar(self):
        df = pd.read_excel(self.archivo)
        df = df[self.columnas]
        df = df.applymap(lambda x: x.strip() if isinstance(x, str) else x)
        df.columns = df.columns.str.strip().str.lower()
        df = df.dropna(subset=self.columnas)
        df = df.drop_duplicates(subset=self.columnas)
        df = df.reset_index(drop=True)
        return df.to_dict(orient='records')