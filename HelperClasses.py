class Nodo:
    def __init__(self, data):
        self.data = data
        self.contadordefinicion = 0


class Variables:
    def __init__(self, cad, contexto):
        self.cad = cad
        self.contexto = contexto

    def __repr__(self):
        aux = ("Variable: " + str(self.cad) + " Contexto: " + str(self.context))
        return aux


class Parametros2(Nodo):
    def __init__(self, data, id, tipo):
        Nodo.__init__(self, data)
        self.id = id
        self.tipo = tipo

    def __repr__(self):
        aux = ('Parametros' '\n' + ' Tipo: ' + str(self.data) + ' Id: ' + str(self.id) + ' Funcion: ' + str(self.tipo))
        return aux


class retorno:
    def __init__(self, cad, tipo, context):
        self.cad = cad
        self.tipo = tipo
        self.context = context

    def __repr__(self):
        aux = ("Valor/Variable: " + str(self.cad) + " Tipo: " + str(self.tipo) + " Contexto: " + str(self.context))
        return aux

class variable:
    def __init__(self, tipo, id, contexto):
        self.tipo = tipo
        self.id = id
        self.contexto = contexto

    def __repr__(self):
        aux = ("Tipo: " + str(self.tipo) + " ID: " + str(self.id) + " Contexto:" + str(self.contexto))
        return aux

class Regla:
    def __init__(self, aux, num, elementos, regla):
        self.aux = aux
        self.num = num
        self.elementos = elementos
        self.regla = regla


class elementopila:
    def __init__(self, cadena, tipo, pos):
        self.cad = cadena
        self.tipo = tipo
        self.pos = pos

    def __repr__(self):
        return str(self.__dict__)


class terminal(elementopila):
    def __init__(self, cadena, tipo, pos):
        elementopila.__init__(self, cadena, tipo, pos)


class noterminal(elementopila):
    def __init__(self, cadena, tipo, pos):
        elementopila.__init__(self, cadena, tipo, pos)


class estado(elementopila):
    def __init__(self, cadena, tipo, pos, estado):
        elementopila.__init__(self, cadena, tipo, pos)
        self.estado = estado