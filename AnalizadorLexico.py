from HelperClasses import *
import globalVars


class analyzer:
    def __init__(self, cadena_para_analizar):
        self.cadena_analizada = cadena_para_analizar + "~"
        self.edo = 0
        self.i = 0
        self.tmp = ""
        self.continua = True
        self.tipo = list()
        self.aux = 0

    def anlexico(self, listalexico, listaerroreslex):

        while self.continua:
            char = self.cadena_analizada[self.i]

            if self.edo == 0:
                if "0" <= char <= "9":
                    self.edo = 1
                    self.tmp += char

                elif char == "E":
                    self.tmp += char
                    self.tipo.append(3)
                    objlex = noterminal("E", "E", self.tipo[-1])
                    listalexico.append(objlex)
                    self.continua = False

                elif "a" <= char <= "z" or "A" <= char <= "Z" or char == "_":
                    self.edo = 4
                    self.tmp += char
                elif char == " ":
                    self.edo = 0

                elif char == "'" or char == '"':
                    self.edo = 9
                    self.tmp += char

                elif (char == "*") or (char == "/"):
                    self.edo = 0
                    self.tmp += char
                    self.tipo.append(6)
                    objlex = terminal(self.tmp, 'Op. Mul', self.tipo[-1])
                    listalexico.append(objlex)
                    self.cleanup()

                elif (char == "=") or (char == "!"):
                    self.cleanup()
                    self.edo = 5
                    self.tmp += char

                elif (char == "<") or (char == ">"):
                    self.cleanup()
                    self.edo = 6
                    self.tmp += char
                elif char == "|":
                    self.cleanup()
                    self.edo = 7
                    self.tmp += char
                elif char == "&":
                    self.cleanup()
                    self.edo = 8
                    self.tmp += char

                elif (char == "+") or (char == "-"):
                    if self.aux == 1:
                        self.tipo.append(5)
                        objlex = terminal(self.tmp, 'Op. Suma', self.tipo[-1])
                        listalexico.append(objlex)
                        self.cleanup()

                    elif self.aux == 2:

                        self.cleanup()
                    if char == "+":
                        self.tmp += char
                        self.tipo.append(5)
                        objlex = terminal(self.tmp, 'Op. Suma', self.tipo[-1])
                        listalexico.append(objlex)
                        self.cleanup()
                        self.edo = 0
                    else:
                        self.tmp += char
                        self.tipo.append(5)
                        objlex = terminal(self.tmp, 'Op. Suma', self.tipo[-1])
                        listalexico.append(objlex)
                        self.cleanup()
                        self.edo = 0

                elif char == ";":
                    self.tmp += char
                    self.tipo.append(12)
                    objlex = terminal(self.tmp, 'Punto y coma', self.tipo[-1])
                    listalexico.append(objlex)
                    self.cleanup()
                    self.edo = 0

                elif char == ",":
                    self.tmp += char
                    self.tipo.append(13)
                    objlex = terminal(self.tmp, 'Coma', self.tipo[-1])
                    listalexico.append(objlex)
                    self.cleanup()
                    self.edo = 0

                elif char == "$":
                    self.tmp += char
                    self.tipo.append(23)
                    objlex = terminal(self.tmp, 'Op. $', self.tipo[-1])
                    listalexico.append(objlex)
                    self.edo = 0
                elif char == "(":
                    self.tmp += char
                    self.tipo.append(14)
                    objlex = terminal(self.tmp, 'Parentesis', self.tipo[-1])
                    listalexico.append(objlex)
                    self.edo = 0

                    globalVars.banderap += 1
                    self.cleanup()
                elif char == ")":
                    self.tmp += char
                    self.tipo.append(15)
                    objlex = terminal(self.tmp, 'Parentesis', self.tipo[-1])
                    listalexico.append(objlex)
                    self.cleanup()
                    if globalVars.banderap != 0:
                        globalVars.banderap -= 1
                    else:
                        listaerroreslex.append('Error, parentesis sin cerrar ')

                    self.edo = 0

                elif char == "{":
                    self.tmp += char
                    self.tipo.append(16)
                    objlex = terminal(self.tmp, 'Corchete', self.tipo[-1])
                    listalexico.append(objlex)
                    self.edo = 0
                    globalVars.banderac += 1
                    self.cleanup()
                elif char == "}":
                    self.tmp += char
                    self.tipo.append(17)
                    objlex = terminal(self.tmp, 'Corchete', self.tipo[-1])
                    listalexico.append(objlex)
                    self.cleanup()
                    if globalVars.banderac != 0:
                        globalVars.banderac -= 1
                    else:
                        listaerroreslex.append('Error, corchetes sin cerrar ')
                    self.edo = 0

                elif char == "~":
                    self.continua = False

            elif self.edo == 1:
                if "0" <= char <= "9":
                    self.edo = 1
                    self.tmp += char

                elif char == ".":
                    self.edo = 2
                    self.tmp += char

                elif char == " ":
                    self.edo = 0
                    self.tipo.append(1)
                    objlex = terminal(self.tmp, 'Entero', self.tipo[-1])
                    listalexico.append(objlex)
                    self.cleanup()

                elif char == "~":
                    self.tipo.append(1)
                    objlex = terminal(self.tmp, 'Entero', self.tipo[-1])
                    listalexico.append(objlex)
                    self.continua = False
                else:
                    self.tipo.append(1)
                    objlex = terminal(self.tmp, 'Entero', self.tipo[-1])
                    listalexico.append(objlex)
                    self.cleanup()
                    self.edo = 0
                    self.aux = 1
                    self.i -= 1

            elif self.edo == 2:
                if "0" <= char <= "9":
                    self.edo = 3
                    self.tmp += char

            elif self.edo == 3:
                if "0" <= char <= "9":
                    self.edo = 3
                    self.tmp += char

                elif char == " ":
                    self.edo = 0
                    # self.tmp +=c

                elif char == "~":
                    self.tipo.append(2)
                    objlex = terminal(self.tmp, 'Real', self.tipo[-1])
                    listalexico.append(objlex)
                    self.cleanup()
                    self.continua = False
                else:
                    self.tipo.append(1)
                    objlex = terminal(self.tmp, 'Real', self.tipo[-1])
                    listalexico.append(objlex)
                    self.cleanup()
                    self.edo = 0
                    self.i -= 1

            elif self.edo == 4:  # Letras
                if "a" <= char <= "z" or "A" <= char <= "Z" or char == "_" or "0" <= char <= "9":
                    self.edo = 4
                    self.tmp += char
                elif char == " ":
                    self.reserved(listalexico, listaerroreslex)
                    self.cleanup()
                    self.edo = 0
                    # self.tmp +=c

                elif char == "~":
                    self.reserved(listalexico, listaerroreslex)
                    self.continua = False
                else:
                    self.reserved(listalexico, listaerroreslex)
                    self.edo = 0
                    self.cleanup()
                    self.i -= 1
                    self.aux = 2

            elif self.edo == 5:
                if char == "=":
                    self.edo = 0
                    self.tmp += char
                    self.tipo.append(11)
                    objlex = terminal(self.tmp, 'Op. Igualdad', self.tipo[-1])
                    listalexico.append(objlex)
                    self.cleanup()

                elif char == " ":
                    self.edo = 0
                    # self.tmp +=c

                elif char == "~":
                    if self.cadena_analizada[self.i - 1] == "=":
                        self.edo = 0
                        self.tipo.append(18)
                        objlex = terminal(self.tmp, 'Op. Igual', self.tipo[-1])
                        listalexico.append(objlex)
                        self.cleanup()
                    else:
                        self.cleanup()
                    self.continua = False
                else:
                    if self.cadena_analizada[self.i - 1] == "=":
                        self.edo = 0
                        self.tipo.append(18)
                        objlex = terminal(self.tmp, 'Op. Igual', self.tipo[-1])
                        listalexico.append(objlex)
                        self.cleanup()
                    else:
                        self.cleanup()
                    self.i -= 1

            elif self.edo == 6:
                if char == "=":
                    self.edo = 0
                    self.tmp += char
                    self.tipo.append(7)
                    objlex = terminal(self.tmp, 'Op. Relacional', self.tipo[-1])
                    listalexico.append(objlex)
                    self.cleanup()

                elif char == " ":
                    self.edo = 0

                elif char == "~":
                    self.edo = 0
                    self.tipo.append(7)
                    objlex = terminal(self.tmp, 'Op. Relacional', self.tipo[-1])
                    listalexico.append(objlex)
                    self.continua = False
                else:
                    self.edo = 0
                    # self.tmp +=c
                    self.tipo.append(7)
                    objlex = terminal(self.tmp, 'Op. Relacional', self.tipo[-1])
                    listalexico.append(objlex)
                    self.cleanup()
                    self.i -= 1

            elif self.edo == 7:
                if char == "|":
                    self.edo = 0
                    self.tmp += char
                    self.tipo.append(8)
                    objlex = terminal(self.tmp, 'Op. Or', self.tipo[-1])
                    listalexico.append(objlex)
                    self.cleanup()

                elif char == " ":
                    self.edo = 0

                elif char == "~":

                    self.continua = False
                else:
                    self.edo = 0
                    self.cleanup()
                    self.i -= 1

            elif self.edo == 8:
                if char == "&":
                    self.edo = 0
                    self.tmp += char
                    self.tipo.append(9)
                    objlex = terminal(self.tmp, 'Op. And', self.tipo[-1])
                    listalexico.append(objlex)
                    self.cleanup()

                elif char == " ":
                    self.edo = 0

                elif char == "~":

                    self.continua = False
                else:
                    self.edo = 0
                    self.cleanup()
                    self.i -= 1

            elif self.edo == 9:
                if char == "'" or char == '"':
                    self.edo = 0
                    self.tmp += char
                    self.tipo.append(3)
                    objlex = terminal(self.tmp, 'Cadena', self.tipo[-1])
                    listalexico.append(objlex)
                    self.cleanup()

                elif char == "~":

                    self.continua = False
                else:
                    self.edo = 9
                    self.tmp += char

            self.i += 1

        self.edo = 0
        self.i = 0
        self.tmp = ""
        self.continua = True

    def reserved(self, listalexico, listaerroreslex):
        strid = self.tmp
        if "while" == strid:
            self.tipo.append(20)
            objlex = terminal(self.tmp, 'Ciclo', self.tipo[-1])
            listalexico.append(objlex)

        elif "if" == strid:
            self.tipo.append(19)
            objlex = terminal(self.tmp, 'Condicional', self.tipo[-1])
            listalexico.append(objlex)
        elif "return" == strid:
            self.tipo.append(21)
            objlex = terminal(self.tmp, 'Retorno', self.tipo[-1])
            listalexico.append(objlex)

        elif "else" == strid:
            self.tipo.append(22)
            objlex = terminal(self.tmp, 'Condicional', self.tipo[-1])
            listalexico.append(objlex)

        elif "int" == strid:
            self.tipo.append(4)
            objlex = terminal(self.tmp, 'Tipo', self.tipo[-1])
            listalexico.append(objlex)

        elif "float" == strid:
            self.tipo.append(4)
            objlex = terminal(self.tmp, 'Tipo', self.tipo[-1])
            listalexico.append(objlex)

        elif "void" == strid:
            self.tipo.append(4)
            objlex = terminal(self.tmp, 'Tipo', self.tipo[-1])
            listalexico.append(objlex)

        elif "print" == strid:
            self.tipo.append(0)
            objlex = terminal(self.tmp, 'Impresion', self.tipo[-1])
            listalexico.append(objlex)

        else:
            self.tipo.append(0)
            objlex = terminal(self.tmp, 'Identificador', self.tipo[-1])
            listalexico.append(objlex)
            if globalVars.banderalexico == 0:
                flag = 0
                try:
                    if listalexico[-2].tipo == 'Tipo':

                        try:
                            if (self.cadena_analizada[self.i]) == ';':

                                pass
                            elif (self.cadena_analizada[self.i]) == ',':

                                pass
                            elif len(listalexico) > 2:
                                # if (listalexico[2].cad) == '(' and ')' in self.cadena_analizada:
                                if listalexico[2].cad == '(' and ')' in self.cadena_analizada:

                                    pass
                                elif ')' in self.cadena_analizada:
                                    pass
                                else:
                                    flag = 1

                            if flag == 1:
                                if (self.cadena_analizada[self.i]) == '(':

                                    pass

                                else:

                                    listaerroreslex.append(
                                        'Falta punto y coma despues de: ' + str(listalexico[-2].cad) + ' ' + self.tmp)

                        except:
                            pass

                except:
                    pass
                aumento = 2
                aux = 0
                if listalexico[-1].tipo == 'Identificador':
                    if globalVars.divcad[globalVars.actual + 1] == '=':
                        if ';' in globalVars.divcad[globalVars.actual + 2]:
                            pass
                        else:
                            aumento += 1
                            if globalVars.divcad[globalVars.actual + aumento] == '+' or globalVars.divcad[
                                globalVars.actual + aumento] == '-' or globalVars.divcad[
                                globalVars.actual + aumento] == '*' or globalVars.divcad[
                                globalVars.actual + aumento] == '/':
                                while aux == 0:

                                    if globalVars.divcad[globalVars.actual + aumento] == '+' or globalVars.divcad[
                                        globalVars.actual + aumento] == '-' or globalVars.divcad[
                                        globalVars.actual + aumento] == '*' or globalVars.divcad[
                                        globalVars.actual + aumento] == '/':
                                        aumento += 1
                                        if ';' in globalVars.divcad[globalVars.actual + aumento]:
                                            globalVars.banderalexico = 0
                                            break

                                        cadena2 = analyzer(globalVars.divcad[globalVars.actual + aumento])
                                        globalVars.banderalexico = 1
                                        cadena2.anlexico()
                                        if listalexico[-1].pos == 0 or listalexico[-1].pos == 1 or listalexico[
                                            -1].pos == 2:
                                            aumento += 1
                                            listalexico.pop()
                                        else:

                                            listalexico.pop()
                                            listaerroreslex.append(
                                                'Falta punto y coma despues de: ' + str(
                                                    globalVars.divcad[globalVars.actual]) + str(
                                                    globalVars.divcad[globalVars.actual + 1]) + str(
                                                    globalVars.divcad[globalVars.actual + 2]))
                                            break
                                    else:

                                        listalexico.pop()
                                        listaerroreslex.append(
                                            'Falta punto y coma despues de: ' + str(
                                                globalVars.divcad[globalVars.actual]) + str(
                                                globalVars.divcad[globalVars.actual + 1]) + str(
                                                globalVars.divcad[globalVars.actual + 2]))
                                        break
                            else:
                                temp = globalVars.actual + 1

                                while True:
                                    if ');' in globalVars.divcad[temp]:
                                        error = 0
                                        break
                                    if ')' in globalVars.divcad[temp]:
                                        error = 1
                                        break
                                    else:
                                        temp += 1

                                if error == 1:
                                    listaerroreslex.append(
                                        'Falta punto y coma despues de: ' + str(
                                            globalVars.divcad[globalVars.actual]) + str(
                                            globalVars.divcad[globalVars.actual + 1]) + str(
                                            globalVars.divcad[globalVars.actual + 2]))
            else:
                pass

    def cleanup(self):
        self.edo = 0

        self.tmp = ""
        self.continua = True
