"""
Projeto 2 de FP
Constanca Fonseca
ist1106251
constanca.fonseca@tecnico.ulisboa.pt
11/11/2022
"""

# Tipos abstratos de dados
# TAD gerador: representa o estado de um gerador de numeros pseudoaleatorios xorshift.


def cria_gerador(b, s):
    """ int x int -> gerador
    Recebe o numero de bits do gerador e o estado inicial e devolve o gerador correspondente. """
    if type(b) != int or type(s) != int or s <= 0 or s > ((2** b)-1) or not (b == 32 or b == 64):
        raise ValueError('cria_gerador: argumentos invalidos') 
    g = [b, s]
    return g

def cria_copia_gerador(g):
    """ gerador -> gerador
    Recebe um gerador e devolve uma copia deste."""
    return g.copy()

def obtem_estado(g):
    """ gerador -> int
    Recebe um gerador e devolve o seu estado atual sem o alterar."""
    return g[1]

def define_estado(g, s):
    """ gerador x int -> int
    Recebe um gerador e uma seed e devolve a nova seed atualizada. """
    g[1] = s
    return g[1]

def atualiza_estado(g):
    """ gerador -> int
    Recebe um gerador e atualiza o seu estado segundo o algoritmo xorshift,
    devolvendo a seed."""
    if g[0] == 32:
        g[1] = g[1]^((g[1] << 13) & 0xFFFFFFFF ) 
        g[1] = g[1]^((g[1] >> 17) & 0xFFFFFFFF ) 
        g[1] = g[1]^((g[1] << 5) & 0xFFFFFFFF ) 
        return g[1]
    elif g[0] == 64:
        g[1] = g[1]^((g[1] << 13) & 0xFFFFFFFFFFFFFFFF ) 
        g[1] = g[1]^((g[1] >> 7) & 0xFFFFFFFFFFFFFFFF ) 
        g[1] = g[1]^((g[1] << 17) & 0xFFFFFFFFFFFFFFFF ) 
        return g[1]

def eh_gerador(arg):
    """ universal -> booleano
    Recebe um argumento e devolve True se este for um gerador, caso contrario
    devolve False"""
    if type(arg) == list and len(arg) == 2 and type(arg[0]) == int and \
            type(arg[1]) == int and (arg[0] == 32 or arg[0] == 64) and arg[1] > 0 \
                and arg[1] <= (2**arg[0])-1:
        return True
    return False

def geradores_iguais(g1, g2):
    """gerador x gerador -> booleano
    Recebe dois geradores e devolve True se estes forem geradores e iguais."""
    if eh_gerador(g1) == True and eh_gerador(g2) == True and (g1 == g2):
        return True
    return False

def gerador_para_str(g):
    """ gerador -> str
    Recebe um gerador e devolve o seu argumento em forma de string."""
    p = "xorshift" + str(g[0]) + "(s=" + str(g[1]) + ")"
    return p

def gera_numero_aleatorio(g, n):
    """ gerador x int -> int
    Devolve um numero maior que 0 e menor ou igual a n, depois do gerador
    recebido ter sido atualizado e a operacao "1 + mod(seed, n)" ter sido feita. """
    ger = atualiza_estado(g)
    s = 1 + (ger % n)
    if 1 <= s <= n:
        return s

def gera_carater_aleatorio(g, c):
    """ gerador x int -> int
    Devolve um carater entre 'A' e c. Este carater e obtido atraves do novo
    estado do gerador e esta na posicao mod(s, l) da string de tamanho l."""
    ger = atualiza_estado(g)
    l = ord(c) - ord('A') + 1
    s = ger % l
    p = ord('A') + s
    if ord('A') <= p <= ord(c):
        return chr(p)


# TAD coordenada: representa a coordenada que ocupa uma parcela no campo de minas.

def cria_coordenada(s, n):
    """ str x int -> coordenada
    Recebe o valor da coluna em string e o valor da linha em inteiro e devolve
    a coordenada respetiva."""
    if type(n) != int or not (0 < int(n) <= 99) or not ('A' <= str(s) <= 'Z') or len(s) != 1:
        raise ValueError('cria_coordenada: argumentos invalidos')
    coordenada = (s, n)
    return coordenada

def obtem_coluna(c):
    """ coordenada -> str
    Devolve o valor respetivo a coluna."""
    return c[0]

def obtem_linha(c):
    """ coordenada -> int
    Devolve o valor respetivo a linha."""
    return c[1]

def eh_coordenada(arg):
    """ universal -> booleano
    Recebe um argumento e devolve True se este for um TAD coordenada, caso
    contrario devolve False."""
    return isinstance(arg, tuple) and len(arg) == 2 and type(arg[0]) == str \
        and type(arg[1]) == int and arg[1] > 0 and arg[1] <= 99 and 'A' <= arg[0] <= 'Z' \
        and len(arg[0]) == 1
        
def coordenadas_iguais(c1, c2):
    """ coordenada x coordenada -> booleano
    Recebe duas coordenadas e devolve True se estas forem coordeandas e iguais."""
    if eh_coordenada(c1) == True and eh_coordenada(c2) == True and c1 == c2:
        return True
    return False

def coordenada_para_str(c):
    """ coordenada -> str
    Devolve a string que representa o seu argumento."""
    if c[1] < 10:
        s = str(c[0]) + str(0) + str(c[1])
        return s
    else:
        s = str(c[0]) + str(c[1])
        return s

def str_para_coordenada(s):
    """ str -> coordenada
    Devolve a coordenada reapresentada pelo seu argumento."""
    a = cria_coordenada(s[0], int(s[1:])) 
    return a

def obtem_coordenadas_vizinhas(c):
    """ coordenada -> tuplo
    Recebe uma coordenada e devolve, na forma de tuplo, as coordenadas vizinhas desta."""
    l = []
    if c[1] != 1:
        if c[0] != 'A':
            l.append(cria_coordenada(chr(ord(c[0])-1), c[1]-1))
        l.append(cria_coordenada(c[0], c[1]-1))
        if c[0] != 'Z':
            l.append(cria_coordenada(chr(ord(c[0])+1), c[1]-1))
    
    if c[0] != 'Z':
        l.append(cria_coordenada(chr(ord(c[0])+1), c[1]))
        if c[1] < 99:
            l.append(cria_coordenada(chr(ord(c[0])+1), c[1]+1))
    if c[1] < 99:
        l.append(cria_coordenada(c[0], c[1]+1))

    if c[0] != 'A':
        if c[1] < 99:
            l.append(cria_coordenada(chr(ord(c[0])-1), c[1]+1))
        l.append(cria_coordenada(chr(ord(c[0])-1), c[1]))
    
    return tuple(l)

def obtem_coordenada_aleatoria(c, g):
    """ coordenada x gerador -> coordenada
    Recebe uma coordenada que define a maior coluna e linha do campo e um
    gerador e devolve uma coordenada aleatorio dentro deste campo."""
    b = gera_carater_aleatorio(g, c[0])
    a = gera_numero_aleatorio(g, c[1])
    return (b, a)


# TAD parcela: representa as parcelas de um campo de jogo de minas, onde cada 
# parcela pode ser tapada, limpa ou marcada ou ate esconder uma mina.

def cria_parcela():
    """ {} -> parcela
    Devolve uma parcela tapada sem uma mina escondida."""
    p = ['#', False]
    return p

def cria_copia_parcela(p):
    """ parcela -> parcela
    Cria uma copia da parcela."""
    par = p
    parcela = par.copy()
    return parcela

def limpa_parcela(p):
    """ parcela -> parcela
    Modifica a parcela recebida de forma destrutiva, devolvendo a mesma parcela
    limpa."""
    p[0] = '&'
    return p

def marca_parcela(p):
    """ parcela -> parcela
    Modifica a parcela recebida de forma destrutiva, devolvendo a mesma parcela,
    mas marcada com uma bandeira."""
    p[0] = '*'
    return p

def desmarca_parcela(p):
    """ parcela -> parcela
    Modifica a parcela recebida de forma destrutiva, devolvendo a mesma parcela
    como o seu estado modificado para "tapada"."""
    p[0] = '#'
    return p

def esconde_mina(p):
    """ parcela -> parcela
    Modifica a parcela recebida de forma destrutiva, devolvendo a mesma parcela
    como uma mina escondida."""
    p[1] = True
    return p

def eh_parcela(arg):
    """ universal -> booleano
    Recebe um argumento e devolve True se este for um TAD parcela, se nao for,
    devolve False."""
    if arg == []:
        return False
    if type(arg) == list and (arg[0] == '#' or arg[0] == '&' or arg[0] == '*') \
        and (type(arg[1]) == bool):
        return True
    return False

def eh_parcela_tapada(p):
    """ parcela -> booleano
    Recebe uma parcela e devolve True se esta estiver tapada, senao devolve False."""
    if p[0] == '#':
        return True
    return False

def eh_parcela_marcada(p):
    """ parcela -> booleano
    Recebe uma parcela e devolve True se esta estiver marcada, senao devolve False."""
    if p[0] == '*':
        return True
    return False

def eh_parcela_limpa(p):
    """ parcela -> booleano
    Recebe uma parcela e devolve True se esta estiver limpa, senao devolve False."""
    if p[0] == '&':
        return True
    return False

def eh_parcela_minada(p):
    """ parcela -> booleano
    Recebe uma parcela e devolve True se esta estiver minada, senao devolve False."""
    if p[1] == True:
        return True
    return False

def parcelas_iguais(p1, p2):
    """ parcela x parcela -> booleano
    Recebe duas parcelas e devolve True se estas forem."""
    if eh_parcela(p1) == True and eh_parcela(p2) == True and p1[0] == p2[0] and p1[1] == p2[1]:
        return True
    return False

def parcela_para_str(p):
    """ parcela -> str
    Recebe uma parcela e devolve, em string, o seu estado."""
    if p[0] == '#':
        return '#'
    elif p[0] == '*':
        return '@'
    elif p[0] == '&' and p[1] == False:
        return '?'
    elif p[0] == '&' and p[1] == True:
        return 'X' 
    
def alterna_bandeira(p):
    """ parcela -> booleano
    Rece uma parcela e, modificando-a destrutivamente, desmarca-a se for marcada
    e marca-a se for tapada."""
    if p[0] == '*':
        desmarca_parcela(p)
        return True
    elif p[0] == '#':
        marca_parcela(p)
        return True
    return False


# TAD campo: representa o campo do jogo de minas

def cria_campo(c, l):
    """ str x int -> campo
    Recebe uma string e um inteiro e devolve um campo de minas, onde a
    ultima coluna corresponde a string recebida e a ultima linha corresponde ao
    inteiro recebido."""
    if type(c) != str or len(c) != 1 or ord(c) <= 64 or ord(c) >= 94 or type(l) != int or not (0 < l <= 99):
        raise ValueError("cria_campo: argumentos invalidos")
    m = {}
    var = ord('A')
    while var <= ord(c):
        lista = []
        for i in range(l):
            lista.append(cria_parcela())
        m[chr(var)] = lista
        var = var + 1
    return m

def cria_copia_campo(m):
    """ campo -> campo
    Recebe um campo e devolve a sua copia."""
    mc = {}
    for key, lista in m.items():
        nova_lista = []
        for parcela in lista:
            nova_lista.append(parcela.copy())  
        mc[key] = nova_lista
    return mc

def obtem_ultima_coluna(m):
    """ campo -> str
    Recebe um campo e devolve a string correspondente a ultima coluna dele."""
    k = list(m.keys())
    return k[-1]

def obtem_ultima_linha(m):
    """ campo -> int
    Recebe um campo e devolve o inteiro correspondente a ultima linha dele."""
    k = list(m.values())
    return len(k[-1])

def obtem_parcela(m, c):
    """ Recebe um campo e uma coordenada e devolve a parcela do campo
    correspondente a essa coordenada."""
    a = m[obtem_coluna(c)][obtem_linha(c)-1]
    return a

def obtem_coordenadas(m, s):
    """ campo x str -> tuplo
    Recebe um campo e uma string e devolve um tuplo composto pelas coordenadas
    ordenadas de forma ascendente das parcelas dependendo do valor da string."""
    l = []
    n = obtem_ultima_linha(m)
    le = obtem_ultima_coluna(m)
    for col in range(1, n + 1):
        for lin in range(ord('A'), ord(le) + 1):
            coord = cria_coordenada(chr(lin), col)
            p = obtem_parcela(m, coord)
            if s == 'limpas' and eh_parcela_limpa(p):
                l.append(coord)
            elif s == 'tapadas' and eh_parcela_tapada(p):
                l.append(coord)
            elif s == 'marcadas' and eh_parcela_marcada(p):
                l.append(coord)
            elif s == 'minadas' and eh_parcela_minada(p):
                l.append(coord)
    return tuple(l)

def obtem_numero_minas_vizinhas(m, c):
    """ campo x coordenada -> int
    Recebe um campo e uma coordenada e devolve o numero de parcelas vizinhas
    que estao minadas."""
    i = 0
    t = obtem_coordenadas(m, 'minadas')
    v = obtem_coordenadas_vizinhas(c)
    for p in v:
        if p in t:
            i = i + 1
    return i

def eh_campo(arg):
    """ universal -> booleano
    Recebe um argumento e devolve True se este for um TAD campo, senao devolve False."""
    if(arg == {}):
        return False
    if type(arg) == dict:
        for key in arg.keys():
            if 'A' > key or key > 'Z':
                return False
        for value in arg.values():
            if not list:
                return False
            for i in range(len(value)):
                if not eh_parcela(value[i]):
                    return False
        return True

def eh_coordenada_do_campo(m, c):
    """ campo x coordenada -> booleano
    Recebe um campo e uma coordenada e devolve True se a coordenada for valida
    neste campo, se nao for, devolve False."""
    if obtem_coluna(c) in m.keys() and 0 < obtem_linha(c) <= obtem_ultima_linha(m) and eh_coordenada(c):
        return True
    return False

def campos_iguais(m1, m2):
    """ campo x campo -> booleano
    Recebe dois campos e devolve True se forem iguais e considerados campos,
    caso contrario, devovle False."""
    if m1 == m2 and eh_campo(m1) == True and eh_campo(m2) == True:
        return True
    return False

def campo_para_str(m):
    """ campo -> str
    Recebe um campo e devolve-o em forma de string."""
    s = "   "
    for key in m.keys():
        s = s + key
    s = s + "\n"
    s1 = "  +"
    for i in range(len(m.keys())):
        s1 = s1 + "-"
    s1 = s1 + "+"
    s =  s + s1 + "\n"
    for i in range(obtem_ultima_linha(m)):
        if i < 9:
            s = s + str(0) + str(i + 1) + "|"
        else:
            s = s + str(i + 1) + "|"
        for key in m.keys():
            c = cria_coordenada(key, i + 1)
            p = obtem_parcela(m, c)
            if eh_parcela_tapada(p):
                s = s + "#"
            elif eh_parcela_marcada(p):
                s = s + "@"
            elif eh_parcela_limpa(p):
                n = obtem_numero_minas_vizinhas(m, c)
                if eh_parcela_minada(p):
                    s = s + "X"
                else:
                    if n == 0:
                        s = s + " "
                    else:
                        s = s + str(n)
        s = s + "|\n"
    s = s + s1
    return s

def coloca_minas(m, c, g, n):
    """ campo x coordenada x gerador x int -> campo
    Com os dados recebidos, o gerador gera n coordenadas e estas sao escondidas
    no campo."""
    i = 1
    coordenada = cria_coordenada(obtem_ultima_coluna(m), obtem_ultima_linha(m))
    while i <= n:
        coord = obtem_coordenada_aleatoria(coordenada, g)
        t = obtem_coordenadas(m, 'minadas')
        if coord != c and coord not in obtem_coordenadas_vizinhas(c) \
            and eh_coordenada_do_campo(m, coord) and coord not in t:
            p = obtem_parcela(m, coord)
            i = i + 1
            esconde_mina(p)
    return m

def limpa_campo(m, c):
    """ campo x coordenada -> campo
    Recebe um campo e uma coordenada e modifica o campo, de forma destrutiva,
    limpando a parcela na coordenada c."""
    l = []
    t = obtem_coordenadas_vizinhas(c)
    for j in t:
        if eh_coordenada_do_campo(m, j):
            l.append(j)
    p = obtem_parcela(m, c)
    if not eh_parcela_limpa(p):
        limpa_parcela(p)
        if obtem_numero_minas_vizinhas(m, c) == 0 and not eh_parcela_minada(p):
            for i in l:
                q = obtem_parcela(m, i)
                if not eh_parcela_limpa(q) and not eh_parcela_marcada(q):
                    limpa_campo(m, i)
    return m    

# Funcoes adicionais

def jogo_ganho(m): # funcao auxiliar
    """ campo -> booleano
    Recebe um campo e devolve True se todas as parcelas com minas estiverem
    limpas, caso contrario devolve False."""
    todas = {c for estado in ('limpas', 'tapadas', 'marcadas') 
                for c in obtem_coordenadas(m, estado)}
    minadas = set(obtem_coordenadas(m, 'minadas'))
    return set(obtem_coordenadas(m, 'limpas')) == todas - minadas

def turno_jogador(m): # funcao auxiliar
    """ campo -> booleano
    Recebe um campo e pede ao jogador para escolher entre as acoes Limpas ou
    Marcar, pede tambem uma coordenada e modifica, de forma destrutiva, o campo
    de acordo com as acoes escolhidas pelo jogador. Devolve False se foi limpa
    uma parcela minada, senao devolve True."""
    a = input('Escolha uma ação, [L]impar ou [M]arcar:')
    while not (a == 'L' or a == 'M'):
        a = input('Escolha uma ação, [L]impar ou [M]arcar:')
    b = input('Escolha uma coordenada:')
    while not (len(b) == 3 and 'A' <= b[0] <= 'Z' and b[1:].isdigit() \
        and eh_coordenada_do_campo(m, str_para_coordenada(b))):
        b = input('Escolha uma coordenada:')
    c = str_para_coordenada(b)
    if a == 'L':
        p = obtem_parcela(m, c)
        if eh_parcela_minada(p):
            limpa_parcela(p)
            return False
        limpa_campo(m, c)
        return True   
    elif a == 'M':
        p = obtem_parcela(m, c)
        if eh_parcela_marcada(p):
            desmarca_parcela(p)
        elif eh_parcela_limpa(p):
            return True
        else:
            marca_parcela(p)
    return True

def minas(c, l, n, d, s): # funcao principal
    """ str x int  x int x int x int -> booleano
    Recebe a ultima coluna(c) e linha(l), o numero de parcelas com minas(n), a
    dimensao(d) e o estado(s) do gerador. Devolve True se o jogador ganhar o
    jogo, caso contrario devolve False."""
    try:
        g = cria_gerador(d, s)
        m = cria_campo(c, l)
    except:
        raise ValueError('minas: argumentos invalidos')
    if not (isinstance(n, int) and n > 0 and n < (l * (ord(c) - ord('A')))):
        raise ValueError('minas: argumentos invalidos')
    if not (isinstance(d, int) and (d == 32 or d == 64) and isinstance(s, int) \
        and 0 < s <= (2**d -1)):
        raise ValueError('minas: argumentos invalidos')
    if ((ord(c) - ord('A') + 1) * l) - 9 < n:
        raise ValueError('minas: argumentos invalidos')
    print('   [Bandeiras ' + str(len(obtem_coordenadas(m, 'marcadas'))) + '/' + str(n) + ']')
    print(campo_para_str(m))
    b = input('Escolha uma coordenada:')
    c = str_para_coordenada(b)
    while not eh_coordenada_do_campo(m, c) or len(b) != 3 or not b[1:].isdigit():
        b = input('Escolha uma coordenada:')
        c = str_para_coordenada(b)
    coloca_minas(m, c, g, n)
    limpa_campo(m, c)
    while not jogo_ganho(m):
        print('   [Bandeiras ' + str(len(obtem_coordenadas(m, 'marcadas'))) + '/' + str(n) + ']')
        print(campo_para_str(m))
        a = turno_jogador(m)
        if a == False:
            print('   [Bandeiras ' + str(len(obtem_coordenadas(m, 'marcadas'))) + '/' + str(n) + ']')
            print(campo_para_str(m))
            print('BOOOOOOOM!!!')
            return False
    print('   [Bandeiras ' + str(len(obtem_coordenadas(m, 'marcadas'))) + '/' + str(n) + ']')
    print(campo_para_str(m))
    print('VITORIA!!!')
    return True

