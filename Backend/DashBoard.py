import DictCreator
from statistics import mean, median, mode
from numpy import var
import numpy as np
from scipy.stats import kurtosis, skew
class DashBoard:
    def __init__(self, NombreDelEncuestador) -> None:
        self.Dict = DictCreator.DictCreator().dict
        self.precision = 1
        self.NombreDelEncuestador = NombreDelEncuestador
        self.posiciones = [i for i in range(len(self.Dict['Nombre del encuestador:'])) if self.Dict['Nombre del encuestador:'][i] == self.NombreDelEncuestador]
        self.vectorDePuntuaciones = [self.Dict['Puntuación'][i] for i in self.posiciones]
        self.vectorDePuntuaciones.sort()
        self.casillasClases = [i for i in range(1,round(self.nClase()))]
        self.limiteInf = min(self.vectorDePuntuaciones)
        self.limiteSup = self.limiteInf + self.amplitud()-1
        self.limites = [[self.limiteInf, self.limiteSup]]
        for i in range (len(self.casillasClases)):
            self.limites.append([(self.limites[len(self.limites)-1][0]+self.amplitud()) if i % 2 == 0 else self.limites[len(self.limites)-1][1]+self.amplitud() for i in range (2)])
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
        self.fimixbarra2 = [self.frecuenciaAgrupada[i]*(self.marcasDeClase[i]-self.media())**2 for i in range(len(self.marcasDeClase))]
        
        
    def media(self):
        return sum(self.vectorDePuntuaciones)/len(self.vectorDePuntuaciones)
    
    def mediana(self):
        vectorDePuntuaciones= self.vectorDePuntuaciones.copy().sort()
        if len(vectorDePuntuaciones)%2 == 0:
            return (vectorDePuntuaciones[len(vectorDePuntuaciones)//2] + vectorDePuntuaciones[len(vectorDePuntuaciones)//2 - 1])/2
        else:
            return vectorDePuntuaciones[len(vectorDePuntuaciones)//2]
        
        
    def moda(self):
        return mode(self.vectorDePuntuaciones)
    
    
    def rango(self):
        return max(self.vectorDePuntuaciones) - min(self.vectorDePuntuaciones)
    
    
    def rangoIntercuartilico(self):
        vectorDePuntuaciones= self.vectorDePuntuaciones.copy().sort()
        quartiles = [vectorDePuntuaciones[len(vectorDePuntuaciones)//4], vectorDePuntuaciones[len(vectorDePuntuaciones)//2], vectorDePuntuaciones[len(vectorDePuntuaciones)*3//4]]
        return quartiles[len(quartiles)-1] - quartiles[0]
    
    
    def varianza(self):
        return var(self.vectorDePuntuaciones)
    
    
    def desviacionEstandar(self):
        return np.std(self.vectorDePuntuaciones)
    
    
    def coefDeVariacion(self):
        variacion = self.desviacionEstandar(self.NombreDelEncuestador)/self.media(self.NombreDelEncuestador)     
        return variacion
    
    
    def coefDeAsimetria(self):
        return skew(self.vectorDePuntuaciones)
    
    
    def coefDeApuntamiento(self):
        return kurtosis(self.vectorDePuntuaciones)
    
    def nClase(self):
        return 3.3*np.log10(len(self.vectorDePuntuaciones)) + 1
    
    def amplitud(self):
        return round(self.rango()/self.nClase())
    
    
dashboard = DashBoard('Jorge Bolivar')
print(dashboard.frecuenciaRelativaAcumuladaPorcentual)

