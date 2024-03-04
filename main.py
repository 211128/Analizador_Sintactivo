import ply.lex as lex
import ply.yacc as yacc
import tkinter as tk
from tkinter import ttk

variables_string = []
variables_int = []
nombre_classe = ''

# ANALIZADOR LEXICO
tokens = (
    'INT',
    'STRING',
    'MAIN',
    'FUNN',
    'IF',
    'IFELSE',
    'RETURN',
    'REPITE',
    'CONTENIDO',
    'DESDE',
    'HASTA',
    'VAR',
    'PLUS',
    'LPAREN',
    'RPAREN',
    'LBRACE',
    'RBRACE',
    'SEMI',
    'NUMBER',
    'ASSIGN',
    'ID',
    'GT',
    'LT',
    'DOUBLESTRING'     # STRING = CUALQUIER COSA QUE ESTE ENTRE COMILLAS
)

t_INT = r'int'
t_STRING = r'asd'
t_MAIN = r'inn'
t_FUNN = r'funn'
t_IF = r'si'
t_IFELSE = r'sino'
t_RETURN = r'return'
t_REPITE = r'repite'
t_CONTENIDO = r'contenido'
t_DESDE = r'desde'
t_HASTA = r'hasta'
t_VAR = r'var'
t_GT = r','
t_PLUS = r'\+'
t_LT = r'<'
t_NUMBER = r'\d+'
t_DOUBLESTRING = r'"[^"]*"'
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_LBRACE = r'\{'
t_RBRACE = r'\}'
t_SEMI = r';'
t_ASSIGN = r'='


def t_STRINGG(t):
    r'"([^"\\]*(?:\\.[^"\\]*)*)"'
    t.value = t.value[1:-1]  # Eliminar las comillas alrededor de la cadena
    return t


def t_ID(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    if t.value == 'system':
        t.type = 'SYSTEM'
    if t.value == 'break':
        t.type = 'BREAK'
    if t.value == 'default':
        t.type = 'DEFAULT'
    if t.value == 'var':
        t.type = 'VAR'
    if t.value == 'int':
        t.type = 'INT'
    if t.value == 'asd':
        t.type = 'STRING'
    if t.value == 'inn':
        t.type = 'MAIN'
    if t.value == 'funn':
        t.type = 'FUNN'
    if t.value == 'si':
        t.type = 'IF'
    if t.value == 'sino':
        t.type = 'IFELSE'
    if t.value == 'return':
        t.type = 'RETURN'
    if t.value == 'repite':
        t.type = 'REPITE'
    if t.value == 'contenido':
        t.type = 'CONTENIDO'
    if t.value == 'desde':
        t.type = 'DESDE'
    if t.value == 'hasta':
        t.type = 'HASTA'
    else:
        t.value = str(t.value)
    return t

# Regla para ignorar espacios y tabulaciones
t_ignore = ' \t\n'

# Función de error para caracteres inválidos
def t_error(t):
    if t.value == '\n':
        t.lexer.lineno += 1
    mensaje = f"Carácter ilegal: '{t.value[0]}' en la posición {t.lexpos}\n"
    print(f"Carácter ilegal: '{t.value[0]}' en la posición {t.lexpos}")
    t.lexer.skip(1)
    return


def restaurar_todo():
    global variables_declaradas
    global variables_string
    global variables_int
    global nombre_classe
    # Lógica para restaurar o reiniciar la aplicación
    # Aquí puedes agregar el código para reiniciar los valores de la tabla y el cuadro de texto, por ejemplo:
    table.delete(*table.get_children())
    text_input.delete("1.0", "end")
    text_sintactico.delete("1.0", "end")
    label2.destroy()
    label3.destroy()
    label4.destroy()
    label5.destroy()
    variables_declaradas = []
    variables_string = []
    variables_int = []
    nombre_classe = ''


lexer = lex.lex()


def classify_tokens():
    # Limpiar la tabla
    global contenido
    contenido = text_input.get("1.0", "end-1c")
    table.delete(*table.get_children())
    global count_reserved, count_tokens, count_simbolos, count_numero
    count_reserved = 0
    count_tokens = 0
    count_simbolos = 0
    count_numero = 0

    # Clasificar los tokens y mostrarlos en la tabla
    lexer.input(contenido)
    while True:
        token = lexer.token()
        if not token:
            break
        table.insert("", "end", values=(token.value, token.type))
        if token.type == 'STRINGG':
            print(f'String encontrado: {token.value}')
        if token.type in ('INICIA', 'TERMINA', 'INT'):
            count_reserved += 1
        elif token.type == 'ID':
            count_tokens += 1
        elif token.type in ('PA', 'PC', 'LLAVEA', 'LLAVEC', 'IGUAL', 'PUNTO_COMA'):
            count_simbolos += 1
        elif token.type == 'NUMBER':
            count_numero += 1
    mostrar_reservadas()


# DEFINIR STRUCTURA _(ANALIZADOR SEMANTICO)

def p_completo(p):
    '''completo : funtions
                | declarations
                | program
                | if_clause
                | expression'''


def p_funtions(p):
    'funtions : FUNN ID LPAREN INT ID GT INT ID RPAREN LBRACE RETURN ID PLUS ID SEMI RBRACE'


def p_declarations(p):
    '''declarations : VAR INT ID SEMI 
                    | VAR STRING ID SEMI'''


def p_program(p):
    'program : FUNN MAIN LPAREN RPAREN LBRACE VAR INT ID SEMI ID ASSIGN ID LPAREN NUMBER GT NUMBER RPAREN SEMI RBRACE'


def p_if_clause(p):
    '''if_clause : VAR INT ID SEMI ID ASSIGN NUMBER SEMI IF ID LT NUMBER LBRACE CONTENIDO RBRACE IFELSE LBRACE CONTENIDO RBRACE'''


def p_expression(p):
    '''expression : VAR INT ID SEMI REPITE ID DESDE NUMBER HASTA NUMBER LBRACE CONTENIDO RBRACE'''


def p_condition(p):
    '''condition :  LT 
                 |  GT 
                 |  GT GT '''

    print("end do")

# Manejo de errores de sintaxis
def p_error(p):
    if p:
        text_sintactico.insert(tk.END, f"Error de sintaxis en '{p.value}'", p.lineno, '\n')
    else:
        text_sintactico.insert(tk.END, "Metodo incompleta")


parser = yacc.yacc()

def parse_code():
    parser.parse(contenido, lexer=lexer)


def cargar_archivo():
    global contenido
    archivo = filedialog.askopenfile(mode='r')
    if archivo is not None:
        contenido = archivo.read()
        archivo.close()
        contenido = contenido.replace('\n', ' ')
        text_input.config(state='normal')
        text_input.delete('1.0', 'end')
        text_input.insert('end', contenido)
        print(contenido)


def mostrar_reservadas():
    global label2, label3, label4, label5
    aux = "palabras reservadas: " + str(count_reserved)
    aux1 = 'palabras ID: ' + str(count_tokens)
    aux2 = 'palabras simbolos: ' + str(count_simbolos)
    aux3 = 'palabras numeros: ' + str(count_numero)
    label2 = tk.Label(window, text=aux)
    label2.pack(padx=10, pady=5)

    label3 = tk.Label(window, text=aux1)
    label3.pack(padx=10, pady=5)

    label4 = tk.Label(window, text=aux2)
    label4.pack(padx=10, pady=5)

    label5 = tk.Label(window, text=aux3)
    label5.pack(padx=10, pady=5)

# Crear la ventana principal
window = tk.Tk()

label = tk.Label(window, text="Ingrese el código fuente:")
label.pack(padx=10, pady=5)


text_input = tk.Text(window, height=10, width=40)
text_input.pack(padx=10, pady=5)

# Crear la tabla
table = ttk.Treeview(window, columns=("Token", "Clasificación"), show="headings")
table.heading("Token", text="Token")
table.heading("Clasificación", text="Clasificación")
table.pack(padx=10, pady=10)

# Etiqueta y cuadro de texto para ingresar el código fuente


# Botón para clasificar los tokens
classify_button = tk.Button(window, text="Clasificar Tokens", command=classify_tokens)
classify_button.pack(padx=10, pady=5)

classify_button1 = tk.Button(window, text="Analizar", command=parse_code)
classify_button1.pack(padx=10, pady=5)

text_sintactico = tk.Text(window, height=10, width=40)
text_sintactico.pack(padx=10, pady=5)


# Definición de la gramática para el análisis sintáctico



# Botón para restaurar todo
restaurar_button = tk.Button(window, text="Restaurar Todo", command=restaurar_todo)
restaurar_button.pack(padx=10, pady=5)

# Ejecutar la interfaz gráfica
window.mainloop()
