"""
Projeto 1 de FP
Constança Fonseca
ist1106251
constanca.fonseca@tecnico.ulisboa.pt
28/10/2022
"""

#1 Justificação de textos
def limpa_texto(string):
    """cad. caracteres -> cad. caracteres
    Recebe uma string qualquer e remove os carateres brancos presentes nesta,
    devolvendo a string limpa."""
    brancos = {'\t', '\n', '\v', '\f', '\r', ' '}
    resultado = ''
    for p in string:
        if p in brancos:
            resultado += ' '
        else:
            resultado += p

    resultado = ' '.join(resultado.split())
    return resultado

def corta_texto(string, n):
    """cad. carateres x inteiro -> cad. carateres x cad. carateres
    Esta função recebe um texto limpo e o valor da largura da coluna(n), e divide a
    string de forma a devolver duas strings, a primeira com comprimento igual a n
    e a segunda contendo o resto do texto de entrada ."""
    if len(string) <= n:
        return (string, '')
    
    corte = string.rfind(' ', 0, n)

    if corte == -1: corte = n

    str1 = string[:corte]
    str2 = string[corte:].lstrip() 
    
    return (str1, str2)

def insere_espacos(string, n):
    """cad. carateres x inteiro -> cad. carateres
    Recebe um texto limpo e a largura da coluna (n). Se a cadeia tiver duas ou
    mais palavras, são adicionados espaços entre elas até o seu comprimento ser
    igual a n. Se tiver apenas uma palavra, os espaços são adicionados no fim."""
    palavras = string.split()
    if len(palavras) == 1:
        return palavras[0] + ' ' * (n - len(palavras[0]))
    
    num_espacos = len(palavras) - 1
    total_espacos = n - sum(len(p) for p in palavras) 
    espaco_base = total_espacos // num_espacos
    espacos_extra = total_espacos % num_espacos
    resultado = ''
    
    for i, palavra in enumerate(palavras):
        resultado += palavra
        if i < num_espacos:
            resultado += ' ' * (espaco_base + (1 if i < espacos_extra else 0))

    return resultado

def justifica_texto(string, n):
    """ cad. carateres x inteiro -> tuplo
    Recebe um texto e um valor para a largura da coluna e devolve um tuplo com
    strings que estão justificadas."""
    if type(n) != int or type(string) != str or string == '' or n <= 0:
        raise ValueError("justifica_texto: argumentos invalidos")
    
    texto_limpo = limpa_texto(string)
    if any(len(p) > n for p in texto_limpo.split()):
        raise ValueError("justifica_texto: argumentos invalidos")
    
    palavras = texto_limpo.split()
    linhas = []
    linha_atual = []
    
    while palavras:
        palavra = palavras.pop(0)
        # Tenta adicionar palavra na linha atual
        if linha_atual:
            if sum(len(p) for p in linha_atual) + len(linha_atual) + len(palavra) <= n:
                linha_atual.append(palavra)
            else:
                # Justifica linha atual
                linhas.append(insere_espacos(' '.join(linha_atual), n))
                linha_atual = [palavra]
        else:
            if len(palavra) <= n:
                linha_atual.append(palavra)
            else:
                # Palavra maior que n: corta
                linhas.append(palavra[:n])
                resto = palavra[n:]
                palavras.insert(0, resto)
                linha_atual = []
    if linha_atual:
        ultima_linha = ' '.join(linha_atual)
        ultima_linha += ' ' * (n - len(ultima_linha))
        linhas.append(ultima_linha)

    return tuple(linhas)

#2 Método de Hondt
def calcula_quocientes(d, n):
    """ dicionário x inteiro -> dicionário
    Recebe um dicionário com os votos apurados de um círculo e recebe o número
    de deputados. Devolve um dicionário com as mesmas chaves do dicionario de
    entrada(partidos) e os quocientes calculados a partir do Método de Hondt"""
    d_aux = {}
    for key in d:
        list = []
        i = 1
        while i <= n:
            list.append(d[key] / i)
            i += 1
        d_aux[key] = list
    return d_aux

def atribui_mandatos(d, n):
    """ dicionário x inteiro -> lista
    Recebe um dicionário com os votos e um inteiro que representa o número de
    deputados e devolve uma lista ordenada com o mesmo tamanho que o número total de
    deputados."""
    quocientes_dict = calcula_quocientes(d, n)
    quocientes = []
    for partido, lista in quocientes_dict.items():
        for valor in lista:
            quocientes.append((partido, valor))
    quocientes = sorted(quocientes, key=lambda x: (-x[1], d[x[0]]))
    
    escolhidos = quocientes[:n]

    return [partido for partido, _ in escolhidos]

def obtem_partidos(d):
    """ dicionário -> lista
    Recebe um dicionário com informação sobre as eleições, incluindo o nome do
    território, o número de deputados, o nome dos partidos e o número total de
    votos por cada partido. Devolve uma lista por ordem alfabética com o nome
    dos partidos participantes."""
    lista = []
    for valor in d.values(): 
        for key in valor['votos'].keys():
            if key not in lista:
                lista.append(key)
    return sorted(lista)

def obtem_resultado_eleicoes(d):
    """ dicionário -> lista
    Recebe um dicionário com toda a informação das eleiçõess e devolve uma lista
    ordenada constituída por tuplos, de forma a que o primeiro tuplo tenha o maior
    número de deputados e por aí adiante. No caso do número de deputados
    ser igual em vários partidos, a ordenação tem em conta o número total de votos."""
    if type(d) != dict or d == {}:
        raise ValueError('obtem_resultado_eleicoes: argumento invalido')
    
    for key in d:
        '''if type(key) != str or type(d[key]) != dict or 'deputados' not in d[key] \
            or 'votos' not in d[key] or type(d[key]['deputados']) != int or \
                d[key]['deputados'] <= 0 or type(d[key]['votos']) != dict or \
                    d[key]['votos'] == {} or len(d[key]) != 2 or type(d[key]['votos'].values()) != int:'''
        if type(d[key]) != dict or type(key) != str or len(d[key]) > 2:
            raise ValueError('obtem_resultado_eleicoes: argumento invalido')
        if not('votos' in d[key] and 'deputados' in d[key] and \
            type(d[key]['votos']) == dict and type(d[key]['deputados']) == int and \
            d[key]['deputados'] >= 0 and d[key]['votos'] != {}):
            raise ValueError('obtem_resultado_eleicoes: argumento invalido')
        for val in d[key]['votos']:
            if type(val) != str:
                raise ValueError("obtem_resultado_eleicoes: argumento invalido")
            valor = d[key]['votos'][val]
            if not isinstance(valor, int):
                raise ValueError("obtem_resultado_eleicoes: argumento invalido")
            if valor < 0:
                raise ValueError("obtem_resultado_eleicoes: argumento invalido")

    lista = []
    partidos = obtem_partidos(d)
    mandatos = {partido: 0 for partido in partidos}
    votos = {partido: 0 for partido in partidos}

    for valor in d.values():
        deputados = valor['deputados']
        votos_circulo = valor['votos']
        mandatos_circulo = atribui_mandatos(votos_circulo, deputados)
        for partido in mandatos_circulo:
            mandatos[partido] += 1
        for partido, num_votos in votos_circulo.items():
            votos[partido] += num_votos
    for partido in partidos:
        lista.append((partido, mandatos[partido], votos[partido]))
    lista = sorted(lista, key=lambda x: (-x[1], -x[2], x[0]))
        
    return lista

#3 Soluções de Sistemas de Equações
def produto_interno(t1, t2):
    """ tuplo x tuplo -> real
    Recebe dois tuplos de igual dimensão que representam dois vetores, e devolve
    o resultado do produto interno dos dois vetores."""
    i = 0
    soma = 0
    for i in range(len(t1) and len(t2)):
        soma += t1[i]*t2[i]
    return float(soma)

def verifica_convergencia(t1, t2, t3, p):
    """ tuplo x tuplo x tuplo x real -> booleano
    Recebe um tuplo de tuplos que representam as linhas da matriz A; um tuplo
    com os valores do vetor de constantes(c); um tuplo que representa a solução
    atual(x) e um real que indica a precisão pretendida. Devolve True se o erro
    for menor que a precisão e devolve False em caso contrário."""
    for i in range(len(t1)):
        soma = produto_interno(t1[i], t3)
        if abs(soma - t2[i]) >= p:
            return False
    return True

def retira_zeros_diagonal(t1, t2):
    """ tuplo x tuplo -> tuplo x tuplo
    Recebe um tuplo de tuplos que representa a matriz A e um tuplo de números
    que representa o vetor das constantes. Devolve uma matriz nova, em que, se
    existir um 0 na diagonal de uma linha, esta troca com a próxima linha que
    não tenha um 0 na diagonal."""
    A = [list(linha) for linha in t1]
    c = list(t2)
    i = 0
    for i in range(len(t1)):
        if A[i][i] == 0:
            for j in range(len(t1)):
                if j != i and A[j][i] != 0 and A[i][j] != 0:
                    A[i], A[j] = A[j], A[i]
                    c[i], c[j] = c[j], c[i]
                    break
    A = tuple(tuple(linha) for linha in A)
    c = tuple(c)
    return (A, c)

def eh_diagonal_dominante(t1):
    """ tuplo -> booleano
    Recebe um tuplo de tuplos que representa uma matriz quadrada qualquer e
    devolve True se esta matriz for diagonalmente dominante. Devolve false se
    não o for."""
    for i in range(len(t1)):
        soma = 0
        for j in range(len(t1)):
            if i != j:
                soma += abs(t1[i][j])
        if abs(t1[i][i]) < soma:
            return False
    return True


def resolve_sistema(t1, t2, p):
    """ tuplo x tuplo x real -> tuplo
    Recebe um tuplo de tuplos representando uma matriz, um tuplo de números que
    representam o vetor das constantes e um real positivo que representa a
    precisão. Devolve um tuplo com a solução do sistema, que é calculado através
    do método de Jacobi."""
    if not (type(p) == float and type(t1) == tuple and type(t2) == tuple and p > 0 \
        and len(t1) == len(t1[0]) and len(t1[0]) == len(t2)):
        raise ValueError('resolve_sistema: argumentos invalidos')
    
    for linha in t1:
        if type(linha) != tuple or len(linha) != len(t1):
            raise ValueError('resolve_sistema: argumentos invalidos')
        for valor in linha:
            if type(valor) not in (int, float):
                raise ValueError('resolve_sistema: argumentos invalidos')

    for valor in t2:
        if type(valor) not in (int, float):
            raise ValueError('resolve_sistema: argumentos invalidos')

    
    A, c = retira_zeros_diagonal(t1, t2)

    if not eh_diagonal_dominante(A):
        raise ValueError('resolve_sistema: matriz nao diagonal dominante')
    
    t3 = tuple(0.0 for _ in range(len(A)))
    while not verifica_convergencia(A, c, t3, p):
        x = []
        for i in range(len(A)):
            soma = sum(A[i][j] * t3[j] for j in range(len(A[i])) if j != i)
            x.append((c[i] - soma) / A[i][i])
        t3 = tuple(x)
    return t3
