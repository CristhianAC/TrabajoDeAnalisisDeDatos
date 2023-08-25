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
        self.histo = self.histograma(datos)
        self.poligoFre = self.poligonoDeFrecuencia(datos)
        self.Ojiva = self.Ojiva()
        self.boxP = self.boxPlot()
        self.boxA = self.boxPlotAgrupado()
        self.tabla = self.tablaFrecuenciaAgrupada()
    def histograma(self, datos):
        
        
        df = pd.DataFrame(datos)
        fig = px.bar(df, y="Frecuencias", category_orders={"Agrupacion":self.vector1}, x="Agrupacion", color="Agrupacion", color_discrete_sequence=px.colors.qualitative.Plotly)
        return fig.to_html()
        
        
    def poligonoDeFrecuencia(self,datos):
        df = pd.DataFrame(datos)
        trace1 = go.Bar(x=df.Agrupacion, y=df.Frecuencias, name='Frecuencias', marker_color='rgb(102, 185, 191)')
        trace2 = go.Scatter(x=df.Agrupacion, y=df.Frecuencias, mode='lines', name='Frecuencias', marker_color = 'rgb(244, 167, 185)')  # Cambiado a Scatter para crear una línea
        
        data = [trace1, trace2]

        # Configurar el diseño (layout)
        layout = go.Layout(
            plot_bgcolor='rgba(0,0,0,0)',  # Color de fondo transparente
            paper_bgcolor='rgba(0,0,0,0)'  # Color del papel (margen) transparente
        )

        fig = go.Figure(data=data, layout=layout)
        return fig.to_html()
    def Ojiva(self):
        
        fig = px.line(x=self.vector1, y=self.dashboard.frecuenciaAgrupadaAcumulada,markers=True)
        fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", 
                            font=dict(
                                        family="Courier New, monospace",
                                        size=18,
                                        color="White"
                                ))
        return fig.to_html()
        
    def boxPlot(self):
        fig = px.box(self.dashboard.vectorDePuntuaciones)
        fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", 
                            font=dict(
                                        family="Courier New, monospace",
                                        size=18,
                                        color="White"
                                ))
        return fig.to_html()
        
    def boxPlotAgrupado(self):
        fig = px.box(self.dashboard.frecuenciaAgrupada)
        fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", 
                            font=dict(
                                        family="Courier New, monospace",
                                        size=18,
                                        color="White"
                                ))
        return fig.to_html()
            
    def tablaFrecuenciaAgrupada(self):
        fig = go.Figure(data=[go.Table(header=dict(values=['Intervalos', 'Frecuencias']),
                 cells=dict(values=[self.vector1, self.vector2]))
                     ])
        return fig.to_html()
        
    def boxPlotEstandarizado(self):
        fig = px.box(self.dashboard.estandarizacion)
        fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", 
                            font=dict(
                                        family="Courier New, monospace",
                                        size=18,
                                        color="White"
                                ))
        return fig.to_html()
graphic = Graphics("Jorge Bolivar")
