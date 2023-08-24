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
    def mediaAgrup(self):
        return sum([(self.marcasDeClase[i]*self.frecuenciaAgrupada[i]) for i in range(len(self.marcasDeClase))])/sum(self.frecuenciaAgrupada)
    def mediana(self, vectorAlRealizar):
        
        if len(vectorAlRealizar)%2 == 0:
            return (vectorAlRealizar[len(vectorAlRealizar)//2] + vectorAlRealizar[len(vectorAlRealizar)//2 - 1])/2
        else:
            return vectorAlRealizar[len(vectorAlRealizar)//2]
        
        
    def moda(self, vectorAlRealizar):
        return mode(vectorAlRealizar)
    
    def modaAgrup(self):
        value_to_search = max(self.frecuenciaAgrupada)
        fi = [indice for indice, dato in enumerate(self.frecuenciaAgrupada) if dato == value_to_search]
        mo = []
        
        for i in range(len(fi)):
            
            temporal = self.limites[fi[i]][0] + ((self.frecuenciaAgrupada[fi[i]] - self.frecuenciaAgrupada[fi[i]-1])/((self.frecuenciaAgrupada[fi[i]]-self.frecuenciaAgrupada[fi[i]-1]) + (self.frecuenciaAgrupada[fi[i]]-self.frecuenciaAgrupada[fi[i]+1])))*self.amplitudModa(self.vectorDePuntuaciones)
            
            mo.append(temporal)
        
        return mo 
    
    def rango(self, vectorAlRealizar):
        return max(vectorAlRealizar) - min(vectorAlRealizar)
    
    
    def rangoIntercuartilico(self, vectorAlRealizar):
        quartiles = [vectorAlRealizar[len(vectorAlRealizar)//4], vectorAlRealizar[len(vectorAlRealizar)//2], vectorAlRealizar[len(vectorAlRealizar)*3//4]]
        return quartiles[len(quartiles)-1] - quartiles[0]
    
    def varianza(self):
        return var(self.vectorDePuntuaciones)
    
    def varianzaAgrup(self):
        return sum(self.fimixbarra2)/(sum(self.frecuenciaAgrupada)-1) 
    
    
    def desviacionEstandarAgrup(self):
        return self.varianza()**(1/2)  
    
    def desviacionEstandar(self):
        return var(self.vectorDePuntuaciones)**(1/2)
    
    def coefDeVariacionAgrup(self):
        variacion = self.desviacionEstandar()/self.mediaAgrup()     
        return variacion
    
    def coefDeVariacion(self):
        variacion = self.desviacionEstandar()/self.media(self.vectorDePuntuaciones)     
        return variacion
    
    def coefDeAsimetria(self, vectorAlRealizar):
        return skew(vectorAlRealizar)
    
    
    def coefDeApuntamiento(self, vectorAlRealizar):
        return kurtosis(vectorAlRealizar)
    
    def nClase(self, vectorAlRealizar):
        return 3.3*np.log10(len(vectorAlRealizar)) + 1
    
    def amplitud(self, vectorAlRealizar):
        return round(self.rango(vectorAlRealizar)/self.nClase(vectorAlRealizar))
    def amplitudModa(self, vectorAlRealizar):
        return self.rango(vectorAlRealizar)/self.nClase(vectorAlRealizar) 
    





dashboard = DashBoard('Jorge Bolivar')
print("Datos NO agrupados")
print("Medidas de Centralización")
print(dashboard.media(dashboard.vectorDePuntuaciones))
print(dashboard.mediana(dashboard.vectorDePuntuaciones))
print(dashboard.moda(dashboard.vectorDePuntuaciones))
#print(dashboard.amplitudModa(dashboard.vectorDePuntuaciones))
print("\n ")
print("Medidas de variabilidad o dispersión")
print(dashboard.rango(dashboard.vectorDePuntuaciones))
print(dashboard.rangoIntercuartilico(dashboard.vectorDePuntuaciones))
print(dashboard.varianza())
print(dashboard.desviacionEstandar())
print(dashboard.coefDeVariacion())
print("\n ")
print("Medidas de forma")
print(dashboard.coefDeAsimetria(dashboard.vectorDePuntuaciones))
print(dashboard.coefDeApuntamiento(dashboard.vectorDePuntuaciones))
print("\n ")
print("\n ")



print("Datos agrupados")
print(dashboard.limites)
print(dashboard.frecuenciaAgrupada)
print(dashboard.media(dashboard.frecuenciaAgrupada))
print(dashboard.mediana(dashboard.vectorDePuntuaciones))
print(dashboard.modaAgrup())
print(dashboard.rango(dashboard.frecuenciaAgrupada))
print(dashboard.rangoIntercuartilico(dashboard.frecuenciaAgrupada))
print(var(dashboard.vectorDePuntuaciones))
print(dashboard.desviacionEstandar())
print(dashboard.coefDeVariacion())
print("\n ")




#print(dashboard.frecuenciaRelativaAcumuladaPorcentual)

