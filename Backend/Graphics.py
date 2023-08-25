from DashBoard import DashBoard
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
class Graphics:
    def __init__(self, nombreDelEncuestador) -> None:
        self.dashboard = DashBoard(nombreDelEncuestador)
        self.vector1 = self.dashboard.limites.copy()
        self.vector2 = self.dashboard.frecuenciaAgrupada.copy()
        for i in range(len(self.vector1)):
            self.vector1[i] = '[' +  str(self.vector1[i][0]) + ',' + str(self.vector1[i][1]) + ')'
        datos = {
            "Agrupacion": self.vector1,
            "Frecuencias": self.vector2
        }
        self.histograma(datos)
        self.poligonoDeFrecuencia(datos)
        self.Ojiva()
        self.boxPlot()
        self.tablaFrecuenciaAgrupada()
    def histograma(self, datos):
        
        
        df = pd.DataFrame(datos)
        fig = px.bar(df, y="Frecuencias", category_orders={"Agrupacion":self.vector1}, x="Agrupacion", color="Agrupacion", color_discrete_sequence=px.colors.qualitative.Plotly)
        
        
    def poligonoDeFrecuencia(self,datos):
        
        df = pd.DataFrame(datos)
        fig = px.line(df, y="Frecuencias",x=self.vector1,markers=True)
        
        
    def Ojiva(self):
        
        fig = px.line(x=self.vector1, y=self.dashboard.frecuenciaAgrupadaAcumulada,markers=True)
        
    def boxPlot(self):
        fig = px.box(self.dashboard.vectorDePuntuaciones)
        print(self.dashboard.amplitud(self.dashboard.vectorDePuntuaciones))
        
        
    def tablaFrecuenciaAgrupada(self):
        fig = go.Figure(data=[go.Table(header=dict(values=['Intervalos', 'Frecuencias']),
                 cells=dict(values=[self.vector1, self.vector2]))
                     ])
        fig.show()
graphic = Graphics("Jorge Bolivar")
