from django.shortcuts import render
from Backend.Graphics import Graphics
# Create your views here.
def index(request):
    return render(request, "index.html")
def DashBoard(request):
    CristhianAgamez = Graphics("Cristhian Agamez")
    JorgeBolivar = Graphics("Jorge Bolivar")
    JesusDeLaCruz = Graphics("Jesús De la Cruz")
    context = {
        "HistoCris" : CristhianAgamez.histo,
        "HistoJorge" : JorgeBolivar.histo,
        "HistoJesus" : JesusDeLaCruz.histo,
        "PoligonoCris" : CristhianAgamez.poligoFre,
        "PoligonoJorge" : JorgeBolivar.poligoFre,
        "PoligonoJesus" : JesusDeLaCruz.poligoFre,
        "OjivaCris" : CristhianAgamez.ojiva,
        "OjivaJorge" : JorgeBolivar.ojiva,
        "OjivaJesus" : JesusDeLaCruz.ojiva,
        "BoxPlotCris" : CristhianAgamez.boxP,
        "BoxPlotJorge" : JorgeBolivar.boxP,
        "BoxPlotJesus" : JesusDeLaCruz.boxP,
        "BoxPlotAgrupadoCris" : CristhianAgamez.boxA,
        "BoxPlotAgrupadoJorge" : JorgeBolivar.boxA,
        "BoxPlotAgrupadoJesus" : JesusDeLaCruz.boxA,
        "TablaCris" : CristhianAgamez.tabla,
        "TablaJorge" : JorgeBolivar.tabla,
        "TablaJesus" : JesusDeLaCruz.tabla,
        "BoxPlotEstandarCris" : CristhianAgamez.boxPlotEstandarizado,
        "tablaFrecuenciaCris" : CristhianAgamez.tablaDeFrecuencia,
        "BoxPlotEstandarJorge" : JorgeBolivar.boxPlotEstandarizado,
        "tablaFrecuenciaJorge" : JorgeBolivar.tablaDeFrecuencia,
        "BoxPlotEstandarJesus" : JesusDeLaCruz.boxPlotEstandarizado,
        "tablaFrecuenciaJesus" : JesusDeLaCruz.tablaDeFrecuencia,
        "tablaFrecuenciaEstandarCris" : CristhianAgamez.tablaDeFrecuenciaEstandarizada,
        "tablaFrecuenciaEstandarJorge" : JorgeBolivar.tablaDeFrecuenciaEstandarizada,
        "tablaFrecuenciaEstandarJesus" : JesusDeLaCruz.tablaDeFrecuenciaEstandarizada,
    }
    
    return render(request, "dashboard.html", context)