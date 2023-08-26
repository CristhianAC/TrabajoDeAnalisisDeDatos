from .DashBoard import DashBoard, DashBoardGeneral
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go



class Graphics:
    def __init__(self, nombreDelEncuestador) -> None:
        self.dashboard = DashBoard(nombreDelEncuestador)
        self.dashboardGeneral = DashBoardGeneral()
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
        self.ojiva = self.Ojiva()
        self.boxP = self.boxPlot()
        self.boxA = self.boxPlotAgrupado()
        self.tabla = self.tablaFrecuenciaAgrupada()
        
    def histograma(self, datos):
        
        
        df = pd.DataFrame(datos)
        fig = px.bar(df, y="Frecuencias", category_orders={"Agrupacion":self.vector1}, x="Agrupacion", color="Agrupacion", color_discrete_sequence=px.colors.qualitative.Plotly, title="Histograma")
        fig.update_layout(paper_bgcolor="rgba(0,0,0,0)")
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
        
        fig = px.line(x=self.vector1, y=self.dashboard.frecuenciaAgrupadaAcumulada,markers=True, title="Ojiva")
        fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", 
                            font=dict(
                                        family="Courier New, monospace",
                                        size=18,
                                        
                                ))
        return fig.to_html()
        
    def boxPlot(self):
        fig = px.box(x=self.dashboard.vectorDePuntuaciones, title="Caja y Bigote con datos individuales")
        fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", 
                            font=dict(
                                        family="Courier New, monospace",
                                        size=18,
                                        
                                ))
        return fig.to_html()
        
    def boxPlotAgrupado(self):
        fig = px.box(x=self.dashboard.frecuenciaAgrupada, title="Caja y Bigote Con conjunto de datos agrupados")
        fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", 
                            font=dict(
                                        family="Courier New, monospace",
                                        size=18,
                                        
                                ))
        return fig.to_html()
            
    def tablaFrecuenciaAgrupada(self):
        fig = go.Figure(data=[go.Table(header=dict(values=['Intervalos', 'Frecuencias', 'Frecuencia Relativa', 'Frecuencia Relativa Acumulada', 'Frecuencia Relativa Acumulada Porcentual']),
                 cells=dict(values=[self.vector1, self.vector2, self.dashboard.frecuenciaRelativa, self.dashboard.frecuenciaRelativaAcumulada, self.dashboard.frecuenciaRelativaAcumuladaPorcentual]))
                     ])
        fig.update_layout(paper_bgcolor="rgba(0,0,0,0)") 
                            
        return fig.to_html()
        
    def boxPlotEstandarizado(self):
        fig = px.box(x=self.dashboard.estandarizacion, title="Caja y bigote Estandarizado")
        fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", 
                            font=dict(
                                        family="Courier New, monospace",
                                        size=18,
                                        
                                ))
        return fig.to_html()
    def tablaDeFrecuencia(self):
        fig = go.Figure(data=[go.Table(header=dict(values=['valores', 'Frecuencias', 'Frecuencia Relativa', 'Frecuencia Relativa Acumulada', 'Frecuencia Relativa Acumulada Porcentual']),
                 cells=dict(values=[self.dashboard.vectorDePuntuacionesUnicoValor, self.dashboard.frecuenciaDePuntuaciones, self.dashboard.frecuenciaRelativaDePuntuaciones, self.dashboard.frecuenciaRelativaDePuntuacionesAcumulada, self.dashboard.frecuenciaRelativaDePuntuacionesAcumuladaPorcentual]))
                     ])
        fig.update_layout(paper_bgcolor="rgba(0,0,0,0)") 
                            
        return fig.to_html()
    def tablaDeFrecuenciaEstandarizada(self):
        fig = go.Figure(data=[go.Table(header=dict(values=['Valores Estandarizados']),
                 cells=dict(values=[self.dashboard.estandarizacion]))
                     ])
        fig.update_layout(paper_bgcolor="rgba(0,0,0,0)") 
                            
        return fig.to_html()
    def tablaFrecuenciaGeneral(self):
        fig = go.Figure(data=[go.Table(header=dict(values=['Intervalos', 'Frecuencias', 'Frecuencia Relativa', 'Frecuencia Relativa Acumulada', 'Frecuencia Relativa Acumulada Porcentual']),
                 cells=dict(values=[self.dashboardGeneral.vectorDePuntuacionesUnicoValor, self.dashboardGeneral.frecuenciaDePuntuaciones, self.dashboardGeneral.frecuenciaRelativaDePuntuaciones, self.dashboardGeneral.frecuenciaRelativaDePuntuacionesAcumulada, self.dashboardGeneral.frecuenciaRelativaDePuntuacionesAcumuladaPorcentual]))
                     ])
        fig.update_layout(paper_bgcolor="rgba(0,0,0,0)") 
                            
        return fig.to_html()
    def tablaFrecuenciaAgrupadaGeneral(self):
        fig = go.Figure(data=[go.Table(header=dict(values=['Intervalos', 'Frecuencias', 'Frecuencia Relativa', 'Frecuencia Relativa Acumulada', 'Frecuencia Relativa Acumulada Porcentual']),
                 cells=dict(values=[self.dashboardGeneral.limites, self.dashboardGeneral.frecuenciaAgrupada, self.dashboardGeneral.frecuenciaRelativaAcumulada, self.dashboardGeneral.frecuenciaRelativaAcumulada, self.dashboardGeneral.frecuenciaRelativaAcumuladaPorcentual]))
                     ])
        fig.update_layout(paper_bgcolor="rgba(0,0,0,0)") 
                            
        return fig.to_html()
    
    def boxPlotGeneral(self):
        fig = px.box(x=self.dashboardGeneral.vectorDePuntuaciones, title="Caja y Bigote con datos individuales")
        fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", 
                            font=dict(
                                        family="Courier New, monospace",
                                        size=18,
                                        
                                ))
        return fig.to_html()
    def boxPlotAgrupadoGeneral(self):
        fig = px.box(x=self.dashboardGeneral.frecuenciaAgrupada, title="Caja y Bigote Con conjunto de datos agrupados")
        fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", 
                            font=dict(
                                        family="Courier New, monospace",
                                        size=18,
                                        
                                ))
        return fig.to_html()
    