from . import DictCreator
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
        self.precision = 0.1
        
        self.NombreDelEncuestador = NombreDelEncuestador
        self.posiciones = [i for i in range(len(self.Dict['Nombre del encuestador:'])) if self.Dict['Nombre del encuestador:'][i] == self.NombreDelEncuestador]
        self.vectorDePuntuaciones = [self.Dict['Puntuación'][i] for i in self.posiciones]
        self.vectorDePuntuaciones.sort()
        self.vectorDePuntuacionesUnicoValor = list(set(self.vectorDePuntuaciones))
        self.frecuenciaDePuntuaciones = [self.vectorDePuntuaciones.count(i) for i in self.vectorDePuntuacionesUnicoValor]
        self.frecuenciaRelativaDePuntuaciones = [self.frecuenciaDePuntuaciones[i]/len(self.vectorDePuntuaciones) for i in range(len(self.frecuenciaDePuntuaciones))]
        self.frecuenciaRelativaDePuntuacionesAcumulada = [round(sum(self.frecuenciaRelativaDePuntuaciones[:i+1]),2)for i in range(len(self.frecuenciaRelativaDePuntuaciones))]
        self.frecuenciaRelativaDePuntuacionesAcumuladaPorcentual = [self.frecuenciaRelativaDePuntuacionesAcumulada[i]*100 for i in range(len(self.frecuenciaRelativaDePuntuacionesAcumulada))]
        self.casillasClases = [i for i in range(1,round(self.nClase(self.vectorDePuntuaciones)))]
        self.limiteInf = min(self.vectorDePuntuaciones)
        self.limiteSup = round(self.limiteInf + self.amplitud(self.vectorDePuntuaciones)-self.precision,2)
        self.limites = [[self.limiteInf, self.limiteSup]]
        for i in range (len(self.casillasClases)):
            self.limites.append([round(self.limites[len(self.limites)-1][0] + self.amplitud(self.vectorDePuntuaciones),2) if i % 2 == 0 else round(self.limites[len(self.limites)-1][1] + self.amplitud(self.vectorDePuntuaciones),2) for i in range (2)])
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
        self.frecuenciaAgrupadaAcumulada = [sum(self.frecuenciaAgrupada[:i+1])for i in range(len(self.frecuenciaAgrupada))]
        
        self.quartiles = []
        self.Posquartiles = []
        self.rangoIntercuartilico()
        
        
        self.estandarizacion = [(self.vectorDePuntuaciones[i] - self.media(self.vectorDePuntuaciones))/self.desviacionEstandar() for i in range(len(self.vectorDePuntuaciones))]
        self.mediaEstandarizacion = 0
        self.medianaEstandarizacion = self.mediana(self.estandarizacion)
        self.rangoEstandarizacion = self.rango(self.estandarizacion)
        self.rangoIntercuartilicoEstandarizacion = self.quartiles[2] - self.quartiles[0]
        self.coefDeAsimetriaEstandarizacion =  self.coefDeAsimetria(self.estandarizacion)
        self.coefDeApuntamientoEstandarizacion = self.coefDeApuntamiento(self.estandarizacion)
        
        
        
        
        
        
        
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
    
    
    def rangoIntercuartilico(self):
       
        self.Posquartiles = [len(self.vectorDePuntuaciones)//4, len(self.vectorDePuntuaciones)//2, (len(self.vectorDePuntuaciones)//4)*3]
        self.quartiles = [self.vectorDePuntuaciones[self.Posquartiles[0]], self.vectorDePuntuaciones[self.Posquartiles[1]], self.vectorDePuntuaciones[self.Posquartiles[2]]]
        return self.quartiles[len(self.quartiles)-1] - self.quartiles[0]
    
    
    def rangoIntercuartilicoAgrup(self):
        
        posicionesToRango = []
        for i in range (len(self.Posquartiles)):
            for j in range(len(self.frecuenciaAgrupadaAcumulada)):
                if self.Posquartiles[i] <= self.frecuenciaAgrupadaAcumulada[j]:
                    posicionesToRango.append(j)
                    break
        liPos1 = self.limites[posicionesToRango[0]][0]
        lipos3 = self.limites[posicionesToRango[len(posicionesToRango)-1]][0]
        pos1 = self.Posquartiles[0]
        pos3 = self.Posquartiles[len(self.Posquartiles)-1]
        resultado = []
        resultado.append(liPos1 + ((pos1-self.frecuenciaAgrupadaAcumulada[posicionesToRango[0]-1])/(self.frecuenciaAgrupada[posicionesToRango[0]]))*self.amplitudModa(self.vectorDePuntuaciones))
        resultado.append(liPos1 + ((pos3-self.frecuenciaAgrupadaAcumulada[posicionesToRango[len(posicionesToRango)-1]-1])/(self.frecuenciaAgrupada[posicionesToRango[len(posicionesToRango)-1]]))*self.amplitudModa(self.vectorDePuntuaciones))
        return resultado[1] - resultado[0]
    
    def varianza(self):
        return var(self.vectorDePuntuaciones)
    
    def varianzaAgrup(self):
        return sum(self.fimixbarra2)/(sum(self.frecuenciaAgrupada)-1) 
    
    
    def desviacionEstandarAgrup(self):
        return self.varianzaAgrup()**(1/2)  
    
    def desviacionEstandar(self):
        return var(self.vectorDePuntuaciones)**(1/2)
    
    def coefDeVariacionAgrup(self):
        variacion = self.desviacionEstandarAgrup()/self.mediaAgrup()     
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
        return self.rango(vectorAlRealizar)/self.nClase(vectorAlRealizar)
    
    def amplitudModa(self, vectorAlRealizar):
        return self.rango(vectorAlRealizar)/self.nClase(vectorAlRealizar) 
    
class DashBoardGeneral:
    def __init__(self) -> None:
        self.Dict = DictCreator.DictCreator().dict
        self.precision = 0.1
        
        
        self.posiciones = [i for i in range(len(self.Dict['Nombre del encuestador:']))]
        self.vectorDePuntuaciones = [self.Dict['Puntuación'][i] for i in self.posiciones]
        self.vectorDePuntuaciones.sort()
        self.vectorDePuntuacionesUnicoValor = list(set(self.vectorDePuntuaciones))
        self.frecuenciaDePuntuaciones = [self.vectorDePuntuaciones.count(i) for i in self.vectorDePuntuacionesUnicoValor]
        self.frecuenciaRelativaDePuntuaciones = [self.frecuenciaDePuntuaciones[i]/len(self.vectorDePuntuaciones) for i in range(len(self.frecuenciaDePuntuaciones))]
        self.frecuenciaRelativaDePuntuacionesAcumulada = [round(sum(self.frecuenciaRelativaDePuntuaciones[:i+1]),2)for i in range(len(self.frecuenciaRelativaDePuntuaciones))]
        self.frecuenciaRelativaDePuntuacionesAcumuladaPorcentual = [self.frecuenciaRelativaDePuntuacionesAcumulada[i]*100 for i in range(len(self.frecuenciaRelativaDePuntuacionesAcumulada))]
        self.casillasClases = [i for i in range(1,round(self.nClase(self.vectorDePuntuaciones)))]
        self.limiteInf = min(self.vectorDePuntuaciones)
        self.limiteSup = round(self.limiteInf + self.amplitud(self.vectorDePuntuaciones)-self.precision,2)
        self.limites = [[self.limiteInf, self.limiteSup]]
        for i in range (len(self.casillasClases)):
            self.limites.append([round(self.limites[len(self.limites)-1][0] + self.amplitud(self.vectorDePuntuaciones),2) if i % 2 == 0 else round(self.limites[len(self.limites)-1][1] + self.amplitud(self.vectorDePuntuaciones),2) for i in range (2)])
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
        self.frecuenciaAgrupadaAcumulada = [sum(self.frecuenciaAgrupada[:i+1])for i in range(len(self.frecuenciaAgrupada))]
        
        self.quartiles = []
        self.Posquartiles = []
        self.rangoIntercuartilico()
        
        
        self.estandarizacion = [(self.vectorDePuntuaciones[i] - self.media(self.vectorDePuntuaciones))/self.desviacionEstandar() for i in range(len(self.vectorDePuntuaciones))]
        self.mediaEstandarizacion = 0
        self.medianaEstandarizacion = self.mediana(self.estandarizacion)
        self.rangoEstandarizacion = self.rango(self.estandarizacion)
        self.rangoIntercuartilicoEstandarizacion = self.quartiles[2] - self.quartiles[0]
        self.coefDeAsimetriaEstandarizacion =  self.coefDeAsimetria(self.estandarizacion)
        self.coefDeApuntamientoEstandarizacion = self.coefDeApuntamiento(self.estandarizacion)
        
        
        
        
        
        
        
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
    
    
    def rangoIntercuartilico(self):
       
        self.Posquartiles = [len(self.vectorDePuntuaciones)//4, len(self.vectorDePuntuaciones)//2, (len(self.vectorDePuntuaciones)//4)*3]
        self.quartiles = [self.vectorDePuntuaciones[self.Posquartiles[0]], self.vectorDePuntuaciones[self.Posquartiles[1]], self.vectorDePuntuaciones[self.Posquartiles[2]]]
        return self.quartiles[len(self.quartiles)-1] - self.quartiles[0]
    
    
    def rangoIntercuartilicoAgrup(self):
        
        posicionesToRango = []
        for i in range (len(self.Posquartiles)):
            for j in range(len(self.frecuenciaAgrupadaAcumulada)):
                if self.Posquartiles[i] <= self.frecuenciaAgrupadaAcumulada[j]:
                    posicionesToRango.append(j)
                    break
        liPos1 = self.limites[posicionesToRango[0]][0]
        lipos3 = self.limites[posicionesToRango[len(posicionesToRango)-1]][0]
        pos1 = self.Posquartiles[0]
        pos3 = self.Posquartiles[len(self.Posquartiles)-1]
        resultado = []
        resultado.append(liPos1 + ((pos1-self.frecuenciaAgrupadaAcumulada[posicionesToRango[0]-1])/(self.frecuenciaAgrupada[posicionesToRango[0]]))*self.amplitudModa(self.vectorDePuntuaciones))
        resultado.append(liPos1 + ((pos3-self.frecuenciaAgrupadaAcumulada[posicionesToRango[len(posicionesToRango)-1]-1])/(self.frecuenciaAgrupada[posicionesToRango[len(posicionesToRango)-1]]))*self.amplitudModa(self.vectorDePuntuaciones))
        return resultado[1] - resultado[0]
    
    def varianza(self):
        return var(self.vectorDePuntuaciones)
    
    def varianzaAgrup(self):
        return sum(self.fimixbarra2)/(sum(self.frecuenciaAgrupada)) 
    
    
    def desviacionEstandarAgrup(self):
        return self.varianzaAgrup()**(1/2)  
    
    def desviacionEstandar(self):
        return var(self.vectorDePuntuaciones)**(1/2)
    
    def coefDeVariacionAgrup(self):
        variacion = self.desviacionEstandarAgrup()/self.mediaAgrup()     
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
        return self.rango(vectorAlRealizar)/self.nClase(vectorAlRealizar)
    
    def amplitudModa(self, vectorAlRealizar):
        return self.rango(vectorAlRealizar)/self.nClase(vectorAlRealizar) 
    








