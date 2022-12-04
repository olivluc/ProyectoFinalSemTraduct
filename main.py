from anytree import Node, RenderTree
import AnalizadorLexico
from generacion import generator
from HelperClasses import *
import globalVars

#Main Class -- This class includes the Analizador Sintactico.
# It draws the Syntax Tree and executes "Generacion de Codigo" and "Analizador Lexico".



code = generator()
listalexico = list()
listaerroreslex = list()
listaerrores = list()
pila = list()
lisreglas = list()
auxregl = list()
matrizreglas = list()
listavariables = list()
listavar = list()
listafunciones = list()
listadefiniciones = list()
listadefinicion = list()
listadefinicionarbol = list()
listaparametros = list()
listaterminos = list()
listaterminosaux = list()
listaexpresiones = list()
listasentencias = list()
listalocal = list()
listaparametrosid = list()
listallamadas = list()
listaretorno = list()
listasentenciasbloque = list()
listasenifelse = list()
listaoperaciones = list()


globalVars.init()

def reglas():
    file = open('compilador.lr', 'r')
    line = file.readlines()
    for l in line:
        l = l.rstrip()
        matrizreglas.append(l.split('\t'))

    for i in range(len(matrizreglas)):
        for j in range(len(matrizreglas[i])):
            matrizreglas[i][j] = int(matrizreglas[i][j])
    file.close()


def auxreglas():
    n = 1
    file = open('rgl.txt', 'r')
    line = file.readlines()
    for l in line:
        l = l.rstrip()
        auxregl.append(l.split('\t'))

    for obj in auxregl:
        obj = Regla(n, int(obj[0]), int(obj[1]), str(obj[2]))
        n += 1
        lisreglas.append(obj)
    file.close()


def buscar(str):
    for objlex in listalexico:
        if objlex.cad == str:
            return objlex
        else:
            pass


root = Node(10)


class DefVar(Nodo):
    def __init__(self, data, tipo, lv):
        Nodo.__init__(self, data)
        self.tipo = tipo
        self.lv = lv

    def eliminaVar(self):
        pila.pop()
        pila.pop()
        pila.pop()
        self.lv = pila.pop()
        pila.pop()
        self.data = pila.pop()
        pila.pop()
        self.tipo = pila.pop()
        self.lv = globalVars.contexto
        if self.lv == '':
            self.lv = 'Global'
        listavariables.append(DefVar(self.tipo, self.data, self.lv))
        globals()['actual'] = Node(DefVar(self.tipo, self.data, self.lv), parent=root)
        globalVars.banderavar2 += 1

        if len(listavar) != 0:
            for i in range(len(listavar)):
                auxiliar = listavar.pop(0)
                auxiliar.data = self.tipo
                auxiliar.lv = self.lv
                listavar.append(auxiliar)
                listavariables.append(auxiliar)

    def eliminalistaVar(self):
        pila.pop()
        pila.pop()
        pila.pop()
        self.data = pila.pop()
        pila.pop()
        pila.pop()
        # listavariables.append(DefVar('Unknown ', self.data, self.lv))
        listavar.append(DefVar('Unknown ', self.data, self.lv))

    def __repr__(self):
        aux = ("Variable""\n \t \t \t" "Tipo: " + str(self.data.cad) + " ID: " + str(
            self.tipo.cad) + " Contexto: " + str(self.lv))
        return aux


class DefFunc(Nodo):
    def __init__(self, data, id, tipo):
        Nodo.__init__(self, data)
        self.id = id
        self.tipo = tipo

    def eliminaFunc(self):
        aux = globalVars.contexto
        globalVars.contexto = ''
        pila.pop()
        pila.pop()
        pila.pop()
        pila.pop()
        pila.pop()
        pila.pop()
        pila.pop()
        pila.pop()
        pila.pop()
        id = pila.pop()
        pila.pop()
        tipo = pila.pop()
        if globalVars.tiporetorno != tipo.cad:
            # Agregue cambio en el tipo de retorno
            if globalVars.tiporetorno == '':
                pass
            else:
                listaerrores.append('Error en el retorno de la funcion ' + aux + ' O tipos de datos diferentes')
        globalVars.tiporetorno = ""
        listafunciones.append(DefFunc(self.data, id, tipo))
        if len(listaparametros) != 0:
            globals()['auxiliarFunc'] = Node(DefFunc(self.data, id, tipo), parent=root)
            for i in range(len(listaparametros)):
                auxiliar = listaparametros.pop()
                auxiliar.parent = globals()['auxiliarFunc']
            # globals()['parametro'].parent = globals()['auxiliarFunc']
            # globals()['auxiliarBlo'].parent =globals()['parametro']
            globals()['auxiliarBlo'].parent = auxiliar
        else:
            globals()['auxiliarFunc'] = Node(DefFunc(self.data, id, tipo), parent=root)
            globals()['auxiliarBlo'].parent = globals()['auxiliarFunc']
        code.traductorfunc()
        listaoperaciones.clear()

    def __repr__(self):
        aux = ("DefFunc""\n" "Tipo: " + str(self.tipo.cad) + " ID: " + str(self.id.cad))
        return aux


class Parametros(Nodo):
    def __init__(self, data, id, tipo):
        Nodo.__init__(self, data)
        self.id = id
        self.tipo = tipo

    def eliminaPara(self):

        pila.pop()
        pila.pop()
        pila.pop()
        self.id = pila.pop()
        pila.pop()
        self.tipo = pila.pop()
        globals()['parametro'] = Node(Parametros(self.data, self.id, self.tipo), parent=root)
        listaparametros.append(globals()['parametro'])
        contexto = ""
        i = 0
        posi = 2
        posfi = 6
        if pila[2] == 'Definicion':
            while i == 0:
                posi = posi + 2
                if pila[posi] == 'Definicion':
                    posfi = posfi + 2
                else:
                    contexto = pila[posfi].cad

                    break
        else:
            contexto = pila[4].cad
        listaparametrosid.append(Parametros2(self.tipo.cad, self.id.cad, contexto))

        code.parameters(1, self.id.cad)

    def eliminalistaPara(self):
        pila.pop()
        pila.pop()
        pila.pop()
        self.id = pila.pop()
        pila.pop()
        self.tipo = pila.pop()
        pila.pop()
        pila.pop()
        globals()['parametro'] = Node(Parametros(self.data, self.id, self.tipo), parent=root)
        listaparametros.append(globals()['parametro'])
        i = 0
        posi = 2
        posfi = 6
        contexto = ''
        if pila[2] == 'Definicion':
            while i == 0:
                posi = posi + 2
                if pila[posi] == 'Definicion':
                    posfi = posfi + 2
                else:
                    contexto = pila[posfi].cad

                    break
        else:
            contexto = pila[4].cad
        listaparametrosid.append(Parametros2(self.tipo.cad, self.id.cad, contexto))
        code.parameters(1, self.id.cad)
        # actual = Node(DefLocal(self.data), parent = root)

    def __repr__(self):
        aux = ('Parametros' '\n' + ' Tipo: ' + str(self.tipo.cad) + ' Id: ' + str(self.id.cad))
        return aux


class DefLocal(Nodo):
    def __init__(self, data):
        Nodo.__init__(self, data)
        self.banderalocal = 0

    def eliminaVar(self):
        pila.pop()
        pila.pop()
        if self.banderalocal == 0:
            globals()['auxiliarLocal'] = Node(DefLocal(self.data), parent=root)

            globals()['actual'].parent = globals()['auxiliarLocal']
            if len(listavar) != 0:
                for i in range(len(listavar)):
                    auxiliar = listavar.pop(0)
                    globals()['actual'] = Node(auxiliar, parent=globals()['auxiliarLocal'])

            self.banderalocal = 1
        else:
            globals()['actual'].parent = globals()['auxiliarLocal']

    def flagreset(self):
        self.banderalocal = 0

    def eliminaSen(self):
        pila.pop()
        pila.pop()
        globals()['auxiliarLocalSen'] = Node(DefLocal(self.data), parent=root)
        if len(listasenifelse) != 0:
            for obj in listasenifelse:
                obj.parent = globals()['auxiliarLocalSen']
            listasenifelse.clear()
        else:
            globals()['sentencia'].parent = globals()['auxiliarLocalSen']

        listalocal.append(globals()['auxiliarLocalSen'])
        if globalVars.banderaprint == 1:
            code.funcionprint(globalVars.valorprint)
            globalVars.banderaprint = 0

    def __repr__(self):
        aux = 'DefLocal'
        return aux


class DefLocales(Nodo):
    def __init__(self, data):
        Nodo.__init__(self, data)
        self.banderalocal = 0

    def eliminaDef(self):
        pila.pop()
        pila.pop()
        pila.pop()
        pila.pop()
        if self.banderalocal == 0:
            globals()['auxiliarLocales'] = Node(DefLocales(self.data), parent=root)
            if len(listalocal) != 0:
                aux = listalocal.pop()
                aux.parent = globals()['auxiliarLocales']
            else:
                globals()['auxiliarLocal'].parent = globals()['auxiliarLocales']
            self.banderalocal = 1
        else:
            if len(listalocal) != 0:
                aux = listalocal.pop()
                aux.parent = globals()['auxiliarLocales']
            else:
                globals()['auxiliarLocal'].parent = globals()['auxiliarLocales']

            # Expresiones como asigna las var

    def __repr__(self):
        aux = 'DefLocales'
        return aux


class BloqFunc(Nodo):
    def __init__(self, data, bandera):
        Nodo.__init__(self, data)
        self.bandera = bandera

    def eliminaBlo(self):
        # Agregue un clear
        listaterminos.clear()
        pila.pop()
        pila.pop()
        pila.pop()
        pila.pop()
        pila.pop()
        pila.pop()
        self.bandera = 0
        globals()['auxiliarBlo'] = Node(BloqFunc(self.data, self.bandera), parent=root)
        # globals()['sentencias'].parent = globals()['auxiliarBlo']
        globals()['auxiliarLocales'].parent = globals()['auxiliarBlo']

    def eliminaBloque(self):
        pila.pop()
        pila.pop()
        pila.pop()
        pila.pop()
        pila.pop()
        pila.pop()
        self.bandera = 1
        globals()['auxiliarBlo'] = Node(BloqFunc(self.data, self.bandera), parent=root)
        try:
            globals()['sentencias'].parent = globals()['auxiliarBlo']
        except:
            globals()['expresionRel'].parent = globals()['auxiliarBlo']

    def __repr__(self):
        if self.bandera == 1:
            aux = 'Bloque'
        else:
            aux = 'BloqueFunc'
        return aux


class Argumentos(Nodo):
    def __init__(self, data):
        Nodo.__init__(self, data)

    def eliminaarg(self):
        pila.pop()
        pila.pop()
        pila.pop()
        pila.pop()
        globals()['argumentos'] = Node(Argumentos(self.data), parent=root)
        globals()['expresion'].parent = globals()['argumentos']

    def eliminalistaarg(self):
        pila.pop()
        pila.pop()
        pila.pop()
        pila.pop()
        pila.pop()
        pila.pop()

    def __repr__(self):
        aux = 'Argumentos'
        return aux


class LlamadaFunc(Nodo):
    def __init__(self, data, funcion):
        Nodo.__init__(self, data)
        self.funcion = funcion
        self.listanum = list()

    def eliminallamada(self):
        # Agregue aqui
        globalVars.llamadafuncion = 1
        pila.pop()
        pila.pop()
        pila.pop()
        pila.pop()
        pila.pop()
        pila.pop()
        pila.pop()
        self.data = pila.pop()
        bandera = 0
        bandera2 = 0
        bandera3 = 0
        contexto = ''
        i = 0
        posi = 2
        posfi = 6
        if pila[2] == 'Definicion':
            while i == 0:
                posi = posi + 2
                if pila[posi] == 'Definicion':
                    posfi = posfi + 2
                else:
                    contexto = pila[posfi].cad

                    break
        else:
            contexto = pila[4].cad
        entre = 0
        if len(listaparametrosid) != 0:
            for obj in listaparametrosid:
                if self.data.cad == obj.tipo:
                    self.funcion = obj.tipo

                    try:
                        print(listaterminos[-1].cad)
                    except:
                        bandera = 1
                        break
                    for obj2 in listavariables:

                        if listaterminos[-1].cad == obj2.tipo.cad and obj2.lv == contexto:

                            if obj.data == obj2.data.cad:
                                bandera = 0
                                bandera2 = 0
                                if entre == 0:
                                    code.llamadafuncion(listaterminos, pila[-4].cad, self.data.cad)
                                    entre += 1

                                if bandera3 == 0:
                                    globals()['llamadafunc'] = Node(LlamadaFunc(self.data, self.funcion), parent=root)
                                    globals()['argumentos'].parent = globals()['llamadafunc']
                                    bandera3 += 1
                                else:
                                    pass
                                num = listaparametrosid.index(obj)
                                self.listanum.append(num)
                                listaterminos.pop()
                                break
                            else:
                                bandera = 1

                        else:
                            bandera2 = 1

                    if bandera2 == 1:
                        tipo = ''
                        if listaterminos[-1].tipo == 'Entero':
                            tipo = 'int'
                        elif listaterminos[-1].tipo == 'Real':
                            tipo = 'float'
                        if tipo == obj.data:
                            globals()['llamadafunc'] = Node(LlamadaFunc(self.data, self.funcion), parent=root)
                            globals()['argumentos'].parent = globals()['llamadafunc']
                            code.llamadafuncionnum(listaterminos, pila[-4].cad, self.data.cad)
                            break
                        else:
                            bandera = 1


                    else:
                        pass

                else:
                    pass
            tipo = ''
            tipo2 = ''
            if len(listaretorno) > 0:
                for obj in listaretorno:
                    if self.funcion == obj.context:
                        tipo = obj.tipo
            else:
                tipo = 'void'

            for obj in listavariables:
                if obj.tipo.cad == pila[-4].cad and obj.lv == contexto:
                    tipo2 = obj.data.cad
            if tipo != tipo2:
                if tipo == 'void':
                    pass
                else:
                    listaerrores.append(
                        'Error en el retorno de la funcion ' + self.data.cad + ' O tipos de datos diferentes')

            if bandera == 1:
                listaerrores.append(
                    'Error en la llamada a la funcion ' + self.data.cad + ' O tipos de datos diferentes')
                globals()['llamadafunc'] = Node(LlamadaFunc(self.data, self.funcion), parent=root)
                globals()['argumentos'].parent = globals()['llamadafunc']
            globalVars.llamada = 1

    def __repr__(self):
        aux = ('LlamadaFunc' + ' ID: ' + str(self.funcion))
        return aux


class Definicion(Nodo):
    def __init__(self, data, ultima):
        Nodo.__init__(self, data)
        self.ultima = ultima

    def eliminaDefVar(self):
        pila.pop()
        pila.pop()
        for obj in listavariables:
            if obj == self.ultima:
                globals()['auxiliarVar'] = Node(Definicion(self.data, obj), parent=root)
                globals()['actual'].parent = globals()['auxiliarVar']
                listadefinicionarbol.append(globals()['auxiliarVar'])

                listadefinicion.append(obj)

    def eliminaDef(self):
        pila.pop()
        pila.pop()
        for obj in listafunciones:
            if obj == self.ultima:
                globals()['auxiliarDefinicion'] = Node(Definicion(self.data, obj), parent=root)
                globals()['auxiliarFunc'].parent = globals()['auxiliarDefinicion']
                listadefinicionarbol.append(globals()['auxiliarDefinicion'])
                # -------------------------------
                listadefinicion.append(obj)

                self.contadordefinicion += 1
                # USar 4 variables, solo esas
                # un if en las definiciones, por cada momento solo se podran manejar de a 4

    def __repr__(self):
        aux = "Definicion"
        return aux


class Definiciones(Nodo):
    def __init__(self, data, ultimadef):
        Nodo.__init__(self, data)
        self.ultimadef = ultimadef

    def eliminaDefiniciones(self):
        pila.pop()
        pila.pop()
        pila.pop()
        pila.pop()
        definicion = self.ultimadef
        listadefiniciones.append(definicion)
        globals()['auxiliarDefiniciones'] = Node(Definiciones(self.data, definicion), parent=root)
        auxiliar = listadefinicionarbol.pop()
        auxiliar.parent = globals()['auxiliarDefiniciones']

    def __repr__(self):
        aux = "Definiciones"
        return aux


class Programa(Nodo):
    def __init__(self, data):
        Nodo.__init__(self, data)

    def programaexitoso(self):
        pila.pop()
        pila.pop()
        root.name = "Programa"


class Termino(Nodo):
    def __init__(self, data, tipo, lv):
        Nodo.__init__(self, data)
        self.tipo = tipo
        self.lv = lv

    def eliminaTerminoEntero(self):
        pila.pop()
        self.data = pila.pop()
        self.lv = globalVars.contexto
        try:
            if pila[14].cad == 'return':

                i = 0
                contexto = ''
                posi = 2
                posfi = 6
                if pila[2] == 'Definicion':
                    while i == 0:
                        posi = posi + 2
                        if pila[posi] == 'Definicion':
                            posfi = posfi + 2
                        else:
                            contexto = pila[posfi].cad

                            break
                    globals()['termino'] = Node(Termino(self.data, self.tipo, 'Retorno ' + contexto), parent=root)
                else:
                    globals()['termino'] = Node(Termino(self.data, self.tipo, 'Retorno ' + pila[4].cad), parent=root)

            else:
                globals()['termino'] = Node(Termino(self.data, self.tipo, self.lv), parent=root)
        except:
            globals()['termino'] = Node(Termino(self.data, self.tipo, self.lv), parent=root)
        listaterminos.append(self.data)

    def eliminaTerminoFloat(self):
        pila.pop()
        self.data = pila.pop()
        try:
            if pila[14].cad == 'return':
                i = 0
                contexto = ''
                posi = 2
                posfi = 6
                if pila[2] == 'Definicion':
                    while i == 0:
                        posi = posi + 2
                        if pila[posi] == 'Definicion':
                            posfi = posfi + 2
                        else:
                            contexto = pila[posfi].cad

                            break
                    globals()['termino'] = Node(Termino(self.data, self.tipo, 'Retorno ' + contexto), parent=root)
                else:
                    globals()['termino'] = Node(Termino(self.data, self.tipo, 'Retorno ' + pila[4].cad), parent=root)
            else:
                globals()['termino'] = Node(Termino(self.data, self.tipo, self.lv), parent=root)
        except:
            globals()['termino'] = Node(Termino(self.data, self.tipo, self.lv), parent=root)
        listaterminos.append(self.data)

    def eliminaTerminoId(self):
        pila.pop()
        self.data = pila.pop()

        i = globalVars.banderavar1
        largo = len(listavariables)
        correcto = 0
        while i < globalVars.banderavar2:
            if self.data.cad == listavariables[i].tipo.cad:
                self.tipo = listavariables[i].data
                self.lv = listavariables[i].lv
                correcto = 1
                break
            i += 1
            largo -= 1
            correcto = 0
        flagencontrado = 0
        if largo <= 0 and correcto == 0:
            for obj in listaparametrosid:
                if obj.id == self.data.cad:
                    flagencontrado = 0
                    break
                else:
                    flagencontrado = 1
        if flagencontrado == 1:
            listaerrores.append('Error en la variable ' + str(self.data.cad) + ' No existe')
        try:
            if pila[-2].cad == 'return' or pila[16].cad == 'return':
                contexto = ""
                i = 0
                posi = 2
                posfi = 6
                if pila[2] == 'Definicion':
                    while i == 0:
                        posi = posi + 2
                        if pila[posi] == 'Definicion':
                            posfi = posfi + 2
                        else:
                            contexto = pila[posfi].cad

                            break
                else:
                    contexto = pila[4].cad
                globals()['termino'] = Node(Termino(self.data, self.tipo, 'Retorno ' + contexto), parent=root)
            else:
                globals()['termino'] = Node(Termino(self.data, self.tipo, self.lv), parent=root)
        except:
            globals()['termino'] = Node(Termino(self.data, self.tipo, self.lv), parent=root)

        listaterminos.append(self.data)

    def eliminaTerminoLlamada(self):
        pila.pop()
        pila.pop()
        globals()['termino'] = Node(Termino('LLamada', 'Llamada', 'Llamada'), parent=root)
        try:

            globals()['llamadafunc'].parent = globals()['termino']
        except:
            globals()['llamadafunc'] = Node(Termino('LLamada', 'Llamada', 'Llamada'), parent=root)
            globals()['llamadafunc'].parent = globals()['termino']
            listaerrores.append('Error en la llamada')
        auxiliar = listadefexpresion[-1]
        auxiliar.flagreset()
        listallamadas.append('Llamada')

    def __repr__(self):
        try:
            aux = ('Termino' + ' Id: ' + str(self.data.cad) + ' Contexto: ' + str(self.lv))

        except:
            aux = 'Termino'
            globalVars.banderatermino = 0
        return aux


class Sentencia(Nodo):
    def __init__(self, data, aux):
        Nodo.__init__(self, data)
        self.listateraux = list()
        self.aux = aux

    def eliminaIf(self):
        pila.pop()
        pila.pop()
        pila.pop()
        pila.pop()
        pila.pop()
        pila.pop()
        pila.pop()
        pila.pop()
        pila.pop()
        pila.pop()
        pila.pop()
        pila.pop()
        globals()['sentencia'] = Node(Sentencia(self.data, self.aux), parent=root)
        aux = listasentenciasbloque.pop()
        aux.parent = globals()['sentencia']

        self.aux = 'Sentencia If'
        code.traductorif(globalVars.expresionif, listaterminosaux, globalVars.banderaelse)
        listasenifelse.append(globals()['sentencia'])
        listaterminosaux.clear()
        globalVars.expresionif = ''

    def eliminaElse(self):
        globalVars.banderaelse = 1
        pila.pop()
        pila.pop()
        pila.pop()
        pila.pop()
        globals()['sentencia'] = Node(Sentencia(self.data, self.aux), parent=root)
        aux = listasentenciasbloque.pop()
        aux.parent = globals()['sentencia']
        self.aux = 'Sentencia Else'
        listasenifelse.append(globals()['sentencia'])


    def eliminaWhile(self):
        pila.pop()
        pila.pop()
        pila.pop()
        pila.pop()
        pila.pop()
        pila.pop()
        pila.pop()
        pila.pop()
        pila.pop()
        pila.pop()
        globals()['sentencia'] = Node(Sentencia(self.data, self.aux), parent=root)
        globals()['auxiliarBlo'].parent = globals()['sentencia']
        self.aux = 'Sentencia While'

    def eliminaSen(self):
        pila.pop()
        pila.pop()
        pila.pop()
        pila.pop()
        pila.pop()
        pila.pop()
        pila.pop()
        self.data = pila.pop()
        globals()['sentencia'] = Node(Sentencia(self.data, self.aux), parent=root)
        listasentencias.append(globals()['sentencia'])
        cont = 0

        for obj in listaexpresiones:
            obj.parent = globals()['sentencia']
        listaexpresiones.clear()
        anadidos = 0
        x = 0

        if listaexpresiones != 0:

            for obj in listavariables:

                if self.data.cad == obj.tipo.cad and obj.lv == globalVars.contexto:
                    aux = obj.data.cad
                    aux2 = obj
                    cont = 0
                    while x < anadidos:
                        listaerrores.pop()
                        x += 1
                    break
                else:
                    if cont == 0:
                        cont = 1
                        listaerrores.append(
                            'Error al asignar ' + str(self.data.cad) + ' Variable no existe o no en este contexto')
                        aux = 'mmm'
                        aux2 = 'mmm'
                        anadidos += 1
                    else:
                        pass

            for obj in listaterminos:
                self.listateraux.append(obj)
            i = 0
            coincidencias = len(self.listateraux)
            coincidenciasobj = 0
            variables = list()
            bandera = 0
            correcto = 0
            largo = len(listavariables)
            for obj in listavariables:
                if bandera == 1:
                    break
                if coincidenciasobj == coincidencias:
                    break
                for obj2 in self.listateraux:
                    if obj.tipo.cad == self.listateraux[i].cad:

                        bandera = 0
                        correcto = 1
                        coincidenciasobj += 1
                        if obj.data.cad != aux:
                            if cont == 0:
                                listaerrores.append(
                                    'Error al asignar ' + str(aux2.tipo.cad) + ' tipos de datos diferentes')
                                bandera = 1
                                cont += 1
                        else:

                            pass

                    else:
                        largo -= 1
                        correcto = 0
                        pass

                    i += 1

                i = 0
            if largo <= 0 and correcto == 0 and coincidenciasobj != coincidencias:
                if len(listavariables) == 0:
                    listaerrores.append(
                        'Error al asignar ' + str(self.data.cad) + ' No existe o no dentro de este contexto')
                    cont += 1
                else:
                    bandera = 1
            contador = 0
            esparametro = 0
            # espa
            if bandera == 1:
                if obj2.tipo == 'Real':
                    obj2.tipo = 'float'
                elif obj2.tipo == 'Entero':
                    obj2.tipo = 'int'
                elif obj2.tipo == 'Identificador':
                    esparametro = 1
                    for objeto in listaparametrosid:
                        if objeto.id == self.listateraux[contador].cad:
                            obj2.tipo = objeto.data
                            break
                        else:
                            pass

                if obj2.tipo != aux:

                    if globalVars.llamada != 0:
                        pass
                    else:
                        if cont == 0:
                            listaerrores.append('Error al asignar ' + str(aux2.tipo.cad) + ' tipos de datos diferentes')
                            cont += 1
                else:
                    if len(listaoperaciones) == 0:
                        if globalVars.llamadafuncion == 0:
                            if esparametro == 0:

                                code.traductor21(21, obj2.cad, aux2.tipo.cad)
                            else:
                                code.traductor21(22, obj2.cad, aux2.tipo.cad)
                        else:
                            globalVars.llamadafuncion = 0
                    else:
                        pass

            if cont == 0 and len(listaoperaciones) != 0:
                for obj5 in listaterminos:
                    variables.append(Variables(obj5.cad, globals()['contexto']))
                partederecha = len(variables)
                if listaoperaciones[0] == '+' or listaoperaciones[0] == '*':
                    code.operation(listaoperaciones, obj.tipo.cad, variables, globals()['contexto'],
                                   partederecha)
            for ter in listaterminos:
                listaterminosaux.append(ter)
            listaterminos.clear()
            listaoperaciones.clear()
            globalVars.llamada = 0

            if globalVars.banderaprint == 1:
                code.funcionprint(globalVars.valorprint)
            globalVars.banderaprint = 0
            globalVars.valorprint = ''
        else:
            pass
        self.aux = 'Sentencia'

    def eliminavalor(self):
        pila.pop()
        pila.pop()
        pila.pop()
        pila.pop()
        # listaterminos[-1].cad)
        self.data = listaterminos.pop()
        globals()['sentencia'] = Node(Sentencia(self.data, self.aux), parent=root)
        listasentencias.append(globals()['sentencia'])
        globals()['expresion'].parent = globals()['sentencia']
        pila.pop()
        pila.pop()
        self.aux = 'Sentencia'

    def eliminaSentencias(self):
        pila.pop()
        pila.pop()
        pila.pop()
        self.data = pila.pop()
        globals()['sentencias'] = Node(Sentencia(self.data, self.aux), parent=root)
        listasentencias.append(globals()['sentencias'])
        try:
            if listaexpresiones[-1] == globals()['expresionSum']:
                globals()['expresionSum'].parent = globals()['sentencias']
            else:
                pass
        except:
            pass
        try:
            if listaexpresiones[-1] == globals()['expresionRel']:
                globals()['expresionRel'].parent = globals()['sentencias']
            else:
                pass
        except:
            pass

        globals()['sentencia'].parent = globals()['sentencias']
        listallamadas.clear()

        self.aux = 'Sentencias'

    def eliminaSentenciaBloque(self):
        pila.pop()
        pila.pop()
        globals()['SentenciaBloque'] = Node(Sentencia(self.data, self.aux), parent=root)
        globals()['auxiliarBlo'].parent = globals()['SentenciaBloque']
        listasentenciasbloque.append(globals()['SentenciaBloque'])
        self.aux = 'Sentencia Bloque'

    def __repr__(self):
        return self.aux


class Expresion(Nodo):
    def __init__(self, data):
        Nodo.__init__(self, data)
        self.banderalocal = 0

    def eliminaTer(self):
        pila.pop()
        self.data = pila.pop()
        if self.banderalocal == 0:
            globals()['expresion'] = Node(Expresion(self.data), parent=root)
            listaexpresiones.append(globals()['expresion'])
            globals()['termino'].parent = globals()['expresion']
            self.banderalocal = 1

        else:
            globals()['termino'].parent = globals()['expresion']

        listaexpresiones.append(globals()['expresion'])

    def eliminaMul(self):
        listaterminosaux.clear()
        listaoperaciones.append('*')
        pila.pop()
        self.data = pila.pop()
        pila.pop()
        pila.pop()
        pila.pop()
        pila.pop()
        globals()['expresionMul'] = Node(Expresion(self.data), parent=root)
        globals()['expresion'].parent = globals()['expresionMul']
        listaexpresiones.append(globals()['expresionMul'])

    def eliminaSum(self):
        listaterminosaux.clear()
        listaoperaciones.append(str(pila[-4].cad))
        pila.pop()
        self.data = pila.pop()
        pila.pop()
        pila.pop()
        pila.pop()
        pila.pop()
        globals()['expresionSum'] = Node(Expresion(self.data), parent=root)
        globals()['expresion'].parent = globals()['expresionSum']
        listaexpresiones.append(globals()['expresionSum'])

    def eliminarelacional(self):
        globalVars.expresionif = pila[-4]

        pila.pop()
        self.data = pila.pop()
        pila.pop()
        pila.pop()
        pila.pop()
        pila.pop()
        globals()['expresionRel'] = Node(Expresion(self.data), parent=root)
        globals()['expresion'].parent = globals()['expresionRel']
        listaexpresiones.append(globals()['expresionRel'])
        globalVars.relacional = 1
        listaterminosaux.clear()

    def eliminaigualdad(self):
        globalVars.expresionif = pila[-4]

        pila.pop()
        self.data = pila.pop()
        pila.pop()
        pila.pop()
        pila.pop()
        pila.pop()
        globals()['expresionIgu'] = Node(Expresion(self.data), parent=root)
        globals()['expresion'].parent = globals()['expresionIgu']
        listaexpresiones.append(globals()['expresionIgu'])
        globalVars.igualdad = 1
        listaterminosaux.clear()

    def flagreset(self):
        self.banderalocal = 0

    def __repr__(self):
        aux = 'Expresion'
        return aux

listadeflocal = list()
listadeflocales = list()
listadefexpresion = list()


class analyzer:
    def __init__(self, cadena_para_analizar):
        self.cadena_analizada = cadena_para_analizar + "~"
        self.edo = 0
        self.i = 0
        self.tmp = ""
        self.continua = True
        self.tipo = list()
        self.aux = 0

    def analizadorsintactico(self, i, divcad2):
        while True:
            for obj in pila:
                try:
                    print(obj.cad, end='')
                except:
                    print(obj, end='')
            print(end='\t |')
            if divcad2[i] == 'print':
                globalVars.valorprint = globalVars.divcad[i + 2]
                globalVars.banderaprint = 1

                i += 4

            fila = pila[-1].pos

            columna = buscar(divcad2[i])
            accion = matrizreglas[fila][columna.pos]
            accion = estado(str(accion), accion, accion, accion)
            if accion.estado == 0:
                print('Error')
                break
            elif accion.estado > 0:
                i += 1
                pila.append(columna)
                pila.append(accion)
                print('Desplazamiento', accion.cad)
            elif accion.estado < 0:
                if accion.estado == -1:
                    print('R0')
                    break
                else:
                    for obj in lisreglas:
                        if accion.estado == (obj.aux + 1) * -1:
                            print('R' + str(obj.aux), obj.regla)
                            accion = matrizreglas[fila][obj.num]
                            accion = estado(str(accion), accion, accion, accion)
                            if obj.elementos != 0:
                                eliminar = obj.elementos * 2
                                self.buscaregla(obj.aux, eliminar)
                                fila = pila[-1].pos
                                accion = matrizreglas[fila][obj.num]
                                pila.append(obj.regla)
                                accion = estado(str(accion), accion, accion, accion)
                                pila.append(accion)
                            else:
                                if obj.aux == 10:
                                    globalVars.contexto = pila[-4].cad
                                    code.translater(10, globalVars.contexto)
                                elif obj.aux == 12:
                                    z = 0
                                    posi = 2
                                    posfi = 6
                                    if pila[2] == 'Definicion':
                                        while z == 0:
                                            posi = posi + 2
                                            if pila[posi] == 'Definicion':
                                                posfi = posfi + 2
                                            else:
                                                globalVars.contexto = pila[posfi].cad

                                                break
                                    else:
                                        globalVars.contexto = pila[4].cad
                                    code.translater(12, globalVars.contexto)
                                pila.append(obj.regla)
                                pila.append(accion)
                            break

    def buscaregla(self, num, cantidad):
        if num == 1:
            programa = Programa('Data')
            programa.programaexitoso()
        elif num == 3:
            if len(listadefiniciones) == 0:
                definiciones = Definiciones('Data', 'Data')
                definiciones.eliminaDefiniciones()
            else:
                definiciones = Definiciones('Data', listadefinicion[-1])
                definiciones.eliminaDefiniciones()
        elif num == 4:
            definicion = Definicion('Data', listavariables[-1])
            definicion.eliminaDefVar()
        elif num == 5:
            if len(listafunciones) == 0:
                print('Vacia')
                definicion = Definicion('Data')
                definicion.eliminaDef()
            else:
                definicion = Definicion('Data', listafunciones[-1])
                definicion.eliminaDef()
            listadeflocal.clear()
            listadeflocales.clear()

        elif num == 6:
            defvar = DefVar('Data', 'Data', 'Data')
            defvar.eliminaVar()
        elif num == 8:
            defvar = DefVar('Data', 'Data', 'Data')
            defvar.eliminalistaVar()
        elif num == 9:
            deffun = DefFunc('Data', 'ID', 'Tipo')
            deffun.eliminaFunc()
        elif num == 11:
            defpara = Parametros('Data', 'Id', 'Tipo')
            defpara.eliminaPara()
        elif num == 12:
            pass
        elif num == 13:
            defpara = Parametros('Data', 'Id', 'Tipo')
            defpara.eliminalistaPara()
        elif num == 14:
            # listadeflocal.clear()
            bloquefun = BloqFunc('Data', 0)
            bloquefun.eliminaBlo()
        elif num == 16:
            if len(listadeflocales) == 0:
                deflocales = DefLocales('Data')
                deflocales.eliminaDef()
                listadeflocales.append(deflocales)
            else:
                auxiliar = listadeflocales[-1]
                auxiliar.eliminaDef()
        elif num == 17:
            if len(listadeflocal) == 0:
                deflocal = DefLocal('Data')
                deflocal.eliminaVar()
                listadeflocal.append(deflocal)
            else:
                auxiliar = listadeflocal[-1]
                auxiliar.eliminaVar()
        elif num == 18:
            deflocal = DefLocal('Data')
            deflocal.eliminaSen()
            listadefexpresion.clear()
        elif num == 20:
            sentencia = Sentencia('Data', 'Sentencias')
            sentencia.eliminaSentencias()
        elif num == 21:
            sentencia = Sentencia('Data', 'Sentencia')
            sentencia.eliminaSen()
        elif num == 22:
            sentencia = Sentencia('Data', 'Sentencia If')
            sentencia.eliminaIf()
        elif num == 23:
            sentencia = Sentencia('Data', 'Sentencia While')
            sentencia.eliminaWhile()
        elif num == 24:
            sentencia = Sentencia('Data', 'Sentencia')
            sentencia.eliminavalor()
        elif num == 27:
            sentencia = Sentencia('Data', 'Sentencia Else')
            sentencia.eliminaElse()
        elif num == 28:
            bloquefun = BloqFunc('Data', 1)
            bloquefun.eliminaBloque()
        elif num == 30:
            pila.pop()
            pila.pop()
            tipo = ''
            contexto = ''
            i = 0
            posi = 2
            posfi = 6
            if pila[2] == 'Definicion':
                while i == 0:
                    posi = posi + 2
                    if pila[posi] == 'Definicion':
                        posfi = posfi + 2
                    else:
                        contexto = pila[posfi].cad

                        break
            else:
                contexto = pila[4].cad
            if listaterminos[-1].tipo == 'Real':
                tipo = 'float'
            elif listaterminos[-1].tipo == 'Entero':
                tipo = 'int'
            elif listaterminos[-1].tipo == 'Identificador':
                for obj in listaparametrosid:
                    if listaterminos[-1].cad == obj.id and contexto == obj.tipo:
                        tipo = obj.data
                if tipo == '':
                    for obj in listavariables:
                        if listaterminos[-1].cad == obj.tipo.cad and contexto == obj.lv:
                            tipo = obj.data.cad
                            break

            else:
                tipo = listaterminos[-1].tipo
            globalVars.tiporetorno = tipo
            variables = list()
            if len(listaoperaciones) != 0:
                for obj5 in listaterminos:
                    variables.append(Variables(obj5.cad, globalVars.contexto))
                partederecha = len(variables)
                code.returnOperation(listaoperaciones, variables, globalVars.contexto, partederecha)
                listaoperaciones.clear()
            else:
                code.traductorretorno(listaterminos[-1].cad, contexto)
            listaretorno.append(retorno(listaterminos[-1].cad, tipo, contexto))

        elif num == 32:
            argumento = Argumentos('Data')
            argumento.eliminaarg()

        elif num == 34:
            argumento = Argumentos('Data')
            argumento.eliminalistaarg()
        elif num == 35:
            terminoid = Termino('Data', 'Tipo', 'Lv')
            terminoid.eliminaTerminoLlamada()
        elif num == 36:

            terminoid = Termino('Data', 'Tipo', 'Lv')
            terminoid.eliminaTerminoId()
        elif num == 37:
            terminoid = Termino('Data', 'Tipo', 'Lv')
            terminoid.eliminaTerminoEntero()

        elif num == 38:
            terminoid = Termino('Data', 'Tipo', 'Lv')
            terminoid.eliminaTerminoFloat()
        elif num == 40:
            llamada = LlamadaFunc('Data', 'Funcion')
            llamada.eliminallamada()
        elif num == 42:
            sentencia = Sentencia('Data', 'Sentencia Bloque')
            sentencia.eliminaSentenciaBloque()
            # Agregue un clear
            listadefexpresion.clear()
        elif num == 46:
            expresion = Expresion('Data')
            expresion.eliminaMul()
        elif num == 47:
            expresion = Expresion('Data')
            expresion.eliminaSum()

        elif num == 48:
            expresion = Expresion('Data')
            expresion.eliminarelacional()

        elif num == 49:
            expresion = Expresion('Data')
            expresion.eliminaigualdad()
        elif num == 52:
            if len(listadefexpresion) == 0:
                expresion = Expresion('Data')
                expresion.eliminaTer()
                listadefexpresion.append(expresion)
            else:
                auxiliar = listadefexpresion[-1]
                auxiliar.eliminaTer()
        else:
            while cantidad != 0:
                pila.pop()
                cantidad -= 1

    def limpieza(self):
        self.edo = 0

        self.tmp = ""
        self.continua = True

cad = " int a;\
        int sum(int a, int b){\
        return a + b;\
        }\
        int main(){\
        int a;\
        int b;\
        a = 8;\
        b = 4;\
        b = sum(a, b);\
        print(b)\
        }"

print("Cadena ingresada: ", cad)

globalVars.divcad = cad.split()
globalVars.divcad.append("$")

for i in range(len(globalVars.divcad)):
    globalVars.actual = i
    cadena = AnalizadorLexico.analyzer(globalVars.divcad[i])
    cadena.anlexico(listalexico, listaerroreslex)
if globalVars.banderap != 0:
    listaerroreslex.append('Error, parentesis sin cerrar ')
if globalVars.banderap != 0:
    listaerroreslex.append('Error, corchetes sin cerrar ')
divcad2 = list()

print('#####################################')

print('Leido', f"{'':>9}", 'Tipo', f"{'':>9}", 'Pos', f"{'':<9}")
for objlex in listalexico:
    print(objlex.cad, f"{'|':>11}", objlex.tipo, f"{'|':>9}", objlex.pos)
    divcad2.append(objlex.cad)
globalVars.divcad.clear()
globalVars.divcad = divcad2
auxelimna = (len(globalVars.divcad) - 2) * 2
fila = 0
columna = 0
accion = 0
acept = False
print(len(listaerroreslex))
print('#####################################')
if len(listaerroreslex) != 0:
    for obj in listaerroreslex:
        print(obj)
else:
    pila.append(buscar("$"))
    pila.append(estado("0", 0, 0, 0))

    reglas()
    auxreglas()
    cadena = analyzer(globalVars.divcad[i])
    cadena.analizadorsintactico(0, globalVars.divcad)
print('#####################################')

if len(listaerrores) != 0:
    for obj in listaerrores:
        print(obj)
else:
    for pre, fill, node in RenderTree(root):
        print("%s%s" % (pre, node.name))


    print('#####################################')
    print('Tabla de símbolos')
    print('Tipo', f"{'':>9}", 'ID', f"{'':>9}", 'Ambito', f"{'':<9}")

    for obj in listavariables:
        print(obj.data.cad, f"{'|':>11}", obj.tipo.cad, f"{'|':>9}", obj.lv)


    print('#####################################')
    code.codigotraducido()
