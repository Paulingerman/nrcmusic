import os
import time
from mutagen.mp3 import MP3
from banco import cadastrarMusica
from banco import listarMusicas
from sistema import mostrarCabecalho


def formatarDuracao(duracao):
    minutos = duracao // 60
    segundos = duracao % 60

    return f"{minutos:02}:{segundos:02}"


def mostrarCarregamento():
    print("ESCANEANDO PASTA MUSICAS...")
    print()

    barras = [
        "██░░░░░░░░░░░░░░░░░░ 10%",
        "██████░░░░░░░░░░░░░░ 30%",
        "██████████░░░░░░░░░░ 50%",
        "██████████████░░░░░░ 70%",
        "████████████████████ 100%"
    ]

    for barra in barras:
        print("\r" + barra, end="", flush=True)
        time.sleep(0.2)

    print()
    print()


def buscarArquivos():
    pasta = "musicas"

    if not os.path.isdir(pasta):
        os.makedirs(pasta)

    arquivos = os.listdir(pasta)

    musicas = []

    for arquivo in arquivos:
        nome = arquivo.lower()

        if nome.endswith(".mp3"):
            caminho = os.path.join(pasta, arquivo)
            musicas.append(caminho)

    musicas.sort()

    return musicas


def mostrarArquivos(musicas):
    print("ARQUIVOS ENCONTRADOS")
    print("-" * 60)

    for numero in range(len(musicas)):
        caminho = musicas[numero]
        nome = os.path.basename(caminho)

        print(numero + 1, "-", nome)

    print()


def separarNome(caminho):
    nome = os.path.basename(caminho)
    nome = os.path.splitext(nome)[0]

    partes = nome.split("-")

    artista = ""
    titulo = ""

    if len(partes) >= 2:
        artista = partes[0].strip()
        titulo = partes[1].strip()

    else:
        titulo = nome.strip()

    return artista, titulo


def escolherArquivo(musicas):
    while True:
        escolha = input("SELECIONE O ARQUIVO > ").strip()

        if escolha.lower() == "cancel":
            return ""

        if not escolha.isdigit():
            print("DIGITE O NUMERO DO ARQUIVO.")
            print()
            continue

        numero = int(escolha)

        if numero < 1 or numero > len(musicas):
            print("ARQUIVO NAO ENCONTRADO.")
            print()
            continue

        return musicas[numero - 1]


def adicionarMusica():
    print()
    mostrarCabecalho("CADASTRAR MUSICA")
    print()

    mostrarCarregamento()

    musicas = buscarArquivos()

    if len(musicas) == 0:
        print("NENHUM ARQUIVO MP3 ENCONTRADO.")
        print("COLOQUE SUAS MUSICAS NA PASTA MUSICAS.")
        print()
        return

    print(len(musicas), "ARQUIVO(S) ENCONTRADO(S)")
    print()

    mostrarArquivos(musicas)

    caminho = escolherArquivo(musicas)

    if caminho == "":
        print()
        print("CADASTRO CANCELADO.")
        print()
        return

    artistaSugerido, tituloSugerido = separarNome(caminho)

    print()
    print("DADOS DA MUSICA")
    print("-" * 60)
    print("PRESSIONE ENTER PARA ACEITAR A SUGESTAO.")
    print()

    titulo = input("TITULO [" + tituloSugerido + "] : ").strip()

    if titulo == "":
        titulo = tituloSugerido

    artista = input("ARTISTA [" + artistaSugerido + "] : ").strip()

    if artista == "":
        artista = artistaSugerido

    album = input("ALBUM : ").strip()

    if titulo == "":
        print()
        print("O TITULO NAO PODE FICAR VAZIO.")
        print()
        return

    if artista == "":
        print()
        print("O ARTISTA NAO PODE FICAR VAZIO.")
        print()
        return

    duracao = buscarDuracao(caminho)

    cadastrarMusica(
        titulo,
        artista,
        album,
        caminho,
        duracao
    )

    print()
    print("MUSICA CADASTRADA COM SUCESSO.")
    print()


def abrirBiblioteca():
    musicas = listarMusicas()

    print()
    mostrarCabecalho("BIBLIOTECA DE MUSICAS")
    print()

    if len(musicas) == 0:
        print("NENHUMA MUSICA CADASTRADA.")
        print()
        return

    for musica in musicas:
        idMusica = musica[0]
        titulo = musica[1]
        artista = musica[2]
        album = musica[3]
        duracao = musica[5]

        tempo = formatarDuracao(duracao)

        print("ID      :", idMusica)
        print("TITULO  :", titulo)
        print("ARTISTA :", artista)

        if album != "":
            print("ALBUM   :", album)

        print("TEMPO   :", tempo)
        print("-" * 60)

def buscarDuracao(caminho):
    try:
        audio = MP3(caminho)
        duracao = int(audio.info.length)

        return duracao

    except:
        return 0

    print("TOTAL DE MUSICAS:", len(musicas))
    print()