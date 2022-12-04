**SEMINARIO DE SOLUCION DE PROBLEMAS DE TRADUCTORES DE LENGUAJES II**



**Proyecto Final Lucas Oliva**

El proyecto fue escrito en Python usando el IDE PyCharm: aprendí mucho sobre compiladores y lenguajes de programación en general durante este proyecto. En la universidad en Suiza usamos principalmente Java y Javascript. Por esta razón nunca había hecho un proyecto grande usando Python. 

Durante este proyecto mi comprensión de Python ha mejorado mucho y estoy contento con los resultados.



**Analizador Lexico**

La entrada se analiza carácter por carácter en un bucle while

Dependiendo del tipo de entrada se le asignan "números" según la Léxica

![image-20221204100411676](https://user-images.githubusercontent.com/71500507/205504802-d9ec9408-22db-4e66-889e-f7f99d3c2c02.png)

También hay un caso de conmutación if-else que comprueba si el "Char" es una de las palabras clave reservadas

![image-20221204100735617](https://user-images.githubusercontent.com/71500507/205504824-b983cf02-a9ee-4b80-9855-5c35500eea74.png)

Output:


![image-20221204095804178](https://user-images.githubusercontent.com/71500507/205504829-9b41d79a-9c26-4e4c-b516-793a0ce18e64.png)


**Analizador Sintactico**

Primero se cargan las reglas gramaticales desde 2 archivos de texto.
Con la ayuda de la gramática, el analizador puede empezar a analizar la entrada


![image-20221204101146803](https://user-images.githubusercontent.com/71500507/205504841-914ba1f4-4032-4974-9bd7-1c1310278bed.png)


Aquí, por ejemplo, se lleva a cabo la acción ruduce. Este es uno de los muchos pasos para analizar la entrada y averiguar si la entrada es válida en la gramática dada:

![image-20221204101355415](https://user-images.githubusercontent.com/71500507/205504860-e06a2ecb-d9b0-4262-a186-3ea53dcb3bc0.png)



Resultado:

![image-20221204100927725](https://user-images.githubusercontent.com/71500507/205504864-6b118afb-70b6-4135-9063-de2c3bbd6c87.png)


**Analizador Semantico**


El Árbol de Sintaxis se "dibuja" con ellp de la Clase RenderTree. Durante el análisis toda la información se almacena en la "raíz" y luego se recorre en bucle y se dibuja. 

![image-20221204102216668](https://user-images.githubusercontent.com/71500507/205504892-104885bc-65ce-4a54-9e32-7dfaec006d4c.png)


La tabla de símbolos se muestra así:

![image-20221204102349380](https://user-images.githubusercontent.com/71500507/205504901-05e36f6f-1ee0-4585-a236-98a8395033ea.png)


Resultado:

![image-20221204101441514](https://user-images.githubusercontent.com/71500507/205504912-35ad745b-804f-410d-8544-8855bc0aa6d2.png)


**Generacion de Codigo**

La generación de código en ensamblador tiene el objetivo de traducir nuestra gramática válida a ensamblador, para que los ordenadores puedan ejecutar realmente el código.

En esta sección, por ejemplo, comprobamos qué operador se está utilizando y, en función de ello, lo traducimos a ensamblador.

Por ejemplo, si el operador es un "+" lo traducimos a "ADD".

![image-20221204103232414](https://user-images.githubusercontent.com/71500507/205504924-4be8df55-c06d-4fbb-ba75-474e0041b19a.png)


Resultado

```
section .data  
   primr: db  "La impresion es := %lf",10,0 
section .bss 
   resp: resq 2
section .text 

extern printf
global sum
, main
sum:
   PUSH rbp 
   MOV rbp, rsp 
   SUB rsp, 48 
   MOV QWORD [rbp -24], rdi 
MOV QWORD [rbp -28], rsi 
   MOV rax, QWORD [rbp -28]
   MOV rdi, QWORD [rbp -24]
   ADD rax, rdi

   ADD rsp, 48 
   MOV rsp, rbp 
   POP rbp 
   ret 
   
main:
   PUSH rbp 
   MOV rbp, rsp 
   SUB rsp, 48 
      MOV WORD [rbp -4] , 8
   MOV WORD [rbp -8] , 4
   MOV rax, QWORD [rbp -4]
   MOV rdi, rax 
   MOV rax, QWORD [rbp -8]
   MOV rsi, rax
   call sum
   MOV QWORD [rbp -8], rax
   
   PUSH qword[rbp -8]
   FILD dword[rsp]
   FSTP qword[rel resp]
   ADD rsp, 8
   MOVSD xmm0,qword[rel resp]
   MOV rdi, primr
   MOV al, 1
   call printf WRT ..plt 
   
   ADD rsp, 48 
   MOV rsp, rbp 
   MOV rax, 60 
   MOV rdi, 0 
   syscall 
   
```

**Estructura del proyecto**

Global Vars:

Utilicé un archivo separado para definir todas las variables globales que necesitaría tanto en el Analizador Léxico como en las otras partes del Proyecto:

![image-20221204103825358](https://user-images.githubusercontent.com/71500507/205504937-8dfa7d13-4d03-4a6f-b0c6-c34594669606.png)

HelperClasses:

Utilicé un archivo separado para definir todas las variables globales que necesitaría tanto en el Analizador Léxico como en las otras partes del Proyecto.

Las clases que se utilizaron para todas las partes del proyecto se definieron en el archivo HelperClasses con la idea de hacer el proyecto más legible.

![image-20221204103849175](https://user-images.githubusercontent.com/71500507/205504941-a681e2bf-e1ba-4df0-b6f3-f41d59a16537.png)


**FileStructure**

Tanto la Generacion como el léxico del analizador fueron escritos en sus propios archivos.

![image-20221204104118026](https://user-images.githubusercontent.com/71500507/205504951-18131e68-d981-44f3-b69d-f1d9187c5664.png)
