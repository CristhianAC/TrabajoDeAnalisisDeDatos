from DashBoard import DashBoard
import pandas as pd
import plotly.express as px
class Graphics:
    def __init__(self, nombreDelEncuestador) -> None:
        self.dashboard = DashBoard(nombreDelEncuestador)
        self.vector1 = self.dashboard.limites.copy()
        self.vector2 = self.dashboard.frecuenciaAgrupada.copy()
        for i in range(len(self.vector1)):
            self.vector1[i] = str(self.vector1[i][0]) + '-' + str(self.vector1[i][1])
        datos = {
            "Agrupacion": self.vector1,
            "Frecuencias": self.vector2
        }
        self.histograma(datos)
        self.poligonoDeFrecuencia(datos)
        
    def histograma(self, datos):
        
        
        df = pd.DataFrame(datos)
        fig = px.bar(df, y="Frecuencias", category_orders={"Agrupacion":self.vector1}, x="Agrupacion", color="Agrupacion", color_discrete_sequence=px.colors.qualitative.Plotly)
        
    def poligonoDeFrecuencia(self,datos):
        
        df = pd.DataFrame(datos)
        fig = px.line(df, y="Frecuencias",markers=True)
        
        fig.show()
graphic = Graphics("Jorge Bolivar")
