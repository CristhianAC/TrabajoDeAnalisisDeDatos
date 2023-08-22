import DictCreator
from statistics import mean, median, mode
from numpy import var
import numpy as np
from scipy.stats import kurtosis, skew
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
class DashBoard:
    def __init__(self, NombreDelEncuestador) -> None:
        self.Dict = DictCreator.DictCreator().dict
        self.precision = 1
        self.NombreDelEncuestador = NombreDelEncuestador
        self.posiciones = [i for i in range(len(self.Dict['Nombre del encuestador:'])) if self.Dict['Nombre del encuestador:'][i] == self.NombreDelEncuestador]
        self.vectorDePuntuaciones = [self.Dict['Puntuación'][i] for i in self.posiciones]
        self.vectorDePuntuaciones.sort()
        self.casillasClases = [i for i in range(1,round(self.nClase(self.vectorDePuntuaciones)))]
        self.limiteInf = min(self.vectorDePuntuaciones)
        self.limiteSup = self.limiteInf + self.amplitud(self.vectorDePuntuaciones)-1
        self.limites = [[self.limiteInf, self.limiteSup]]
        for i in range (len(self.casillasClases)):
            self.limites.append([(self.limites[len(self.limites)-1][0]+self.amplitud(self.vectorDePuntuaciones)) if i % 2 == 0 else self.limites[len(self.limites)-1][1]+self.amplitud(self.vectorDePuntuaciones) for i in range (2)])
        self.frecuenciaAgrupada = [0 for i in range(len(self.limites))]
        for i in range(len(self.vectorDePuntuaciones)):
            for j in range(len(self.limites)):
                if self.vectorDePuntuaciones[i] >= self.limites[j][0] and self.vectorDePuntuaciones[i] <= self.limites[j][1]:
                    self.frecuenciaAgrupada[j] += 1
        self.frecuenciaRelativa = [self.frecuenciaAgrupada[i]/len(self.vectorDePuntuaciones) for i in range(len(self.frecuenciaAgrupada))]
        self.frecuenciaRelativaAcumulada = [sum(self.frecuenciaRelativa[:i+1])for i in range(len(self.frecuenciaRelativa))]
        self.frecuenciaRelativaAcumuladaPorcentual = [self.frecuenciaRelativaAcumulada[i]*100 for i in range(len(self.frecuenciaRelativaAcumulada))]
        self.fronteraInferior = [self.limites[i][0]-(self.precision/2) for i in range(len(self.limites))]
        self.fronteraSuperior = [self.limites[i][1]+(self.precision/2) for i in range(len(self.limites))]
        self.marcasDeClase = [(self.fronteraInferior[i]+self.fronteraSuperior[i])/2 for i in range(len(self.fronteraInferior))]
        self.marcaDeClasePorFrecuencia = [self.marcasDeClase[i]*self.frecuenciaAgrupada[i] for i in range(len(self.marcasDeClase))]
        self.fimixbarra2 = [self.frecuenciaAgrupada[i]*(self.marcasDeClase[i]-self.media(self.frecuenciaAgrupada))**2 for i in range(len(self.marcasDeClase))]
        
        
    def media(self, vectorAlRealizar):
        return sum(vectorAlRealizar)/len(vectorAlRealizar)
    
    def mediana(self, vectorAlRealizar):
        
        if len(vectorAlRealizar)%2 == 0:
            return (vectorAlRealizar[len(vectorAlRealizar)//2] + vectorAlRealizar[len(vectorAlRealizar)//2 - 1])/2
        else:
            return vectorAlRealizar[len(vectorAlRealizar)//2]
        
        
    def moda(self, vectorAlRealizar):
        return mode(vectorAlRealizar)
    
    
    def rango(self, vectorAlRealizar):
        return max(vectorAlRealizar) - min(vectorAlRealizar)
    
    
    def rangoIntercuartilico(self, vectorAlRealizar):
        quartiles = [vectorAlRealizar[len(vectorAlRealizar)//4], vectorAlRealizar[len(vectorAlRealizar)//2], vectorAlRealizar[len(vectorAlRealizar)*3//4]]
        return quartiles[len(quartiles)-1] - quartiles[0]
    
    
    def varianza(self, vectorAlRealizar):
        return var(vectorAlRealizar)
    
    
    def desviacionEstandar(self, vectorAlRealizar):
        return np.std(vectorAlRealizar)
    
    
    def coefDeVariacion(self , vectorAlRealizar):
        variacion = self.desviacionEstandar(vectorAlRealizar)/self.media(vectorAlRealizar)     
        return variacion
    
    
    def coefDeAsimetria(self, vectorAlRealizar):
        return skew(vectorAlRealizar)
    
    
    def coefDeApuntamiento(self, vectorAlRealizar):
        return kurtosis(vectorAlRealizar)
    
    def nClase(self, vectorAlRealizar):
        return 3.3*np.log10(len(vectorAlRealizar)) + 1
    
    def amplitud(self, vectorAlRealizar):
        return round(self.rango(vectorAlRealizar)/self.nClase(vectorAlRealizar))
    
    def modaAgrup(self,vectorAlRealizar):
        return  self.limiteInf + (self.frecuenciaRelativaAcumulada)
    
class Graphics:
    def __init__(self) -> None:
        self.Jorge = DashBoard('Jorge Bolivar')
        self.histograma(self.Jorge, self.Jorge.limites, self.Jorge.frecuenciaAgrupada)
    def histograma(self, dashboard:DashBoard, vector1, vector2):
        for i in range(len(vector1)):
            vector1[i] = str(vector1[i][0]) + '-' + str(vector1[i][1])
        datos = {
            "vector1": vector1,
            "vector2": vector2
        }
        
        df = pd.DataFrame(datos)
        fig = px.bar(df, x="vector1", y="vector2")
        fig.show()

#graphic = Graphics()


dashboard = DashBoard('Cristhian Agamez')
print("Medidas de Centralización")
print(dashboard.media(dashboard.vectorDePuntuaciones))
print(dashboard.mediana(dashboard.vectorDePuntuaciones))
print(dashboard.moda(dashboard.vectorDePuntuaciones))
print("\n ")
print("Medidas de variabilidad o dispersión")
print(dashboard.rango(dashboard.vectorDePuntuaciones))
print(dashboard.rangoIntercuartilico(dashboard.vectorDePuntuaciones))
print(dashboard.varianza(dashboard.vectorDePuntuaciones))
print(dashboard.desviacionEstandar(dashboard.vectorDePuntuaciones))
print(dashboard.coefDeVariacion(dashboard.vectorDePuntuaciones))
print("\n ")
print("Medidas de forma")
print(dashboard.coefDeAsimetria(dashboard.vectorDePuntuaciones))
print(dashboard.coefDeApuntamiento(dashboard.vectorDePuntuaciones))
print("\n ")
print("\n ")



print("Datos no agrupados")
print(dashboard.frecuenciaAgrupada)
print(dashboard.media(dashboard.frecuenciaAgrupada))
print(dashboard.mediana(dashboard.vectorDePuntuaciones))
print(dashboard.moda(dashboard.frecuenciaAgrupada))
print(dashboard.rango(dashboard.frecuenciaAgrupada))
print(dashboard.rangoIntercuartilico(dashboard.frecuenciaAgrupada))
print(dashboard.varianza(dashboard.fimixbarra2))
print(dashboard.desviacionEstandar(dashboard.fimixbarra2))
print(dashboard.coefDeVariacion(dashboard.fimixbarra2))
print("\n ")


#print(dashboard.frecuenciaRelativaAcumuladaPorcentual)

