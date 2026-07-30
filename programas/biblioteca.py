import os
import re
import time
import subprocess

from banco import cadastrarMusica
from banco import listarMusicas


PASTA_MUSICAS = "musicas"


def formatarDuracao(segundos):
    try:
        segundos = int(segundos)
    except (TypeError, ValueError):
        segundos = 0

    minutos = segundos // 60
    segundosRestantes = segundos % 60

    return f"{minutos:02}:{segundosRestantes:02}"


def mostrarCarregamento():
    print()
    print("ESCANEANDO PASTA MUSICAS...")
    print()

    tamanho = 30

    for posicao in range(tamanho + 1):
        preenchido = "█" * posicao
        vazio = "░" * (tamanho - posicao)

        porcentagem = int((posicao / tamanho) * 100)

        print(
            f"\r[{preenchido}{vazio}] {porcentagem}%",
            end="",
            flush=True
        )

        time.sleep(0.02)

    print()
    print()


def buscarArquivos():
    if not os.path.isdir(PASTA_MUSICAS):
        os.makedirs(PASTA_MUSICAS)

    arquivos = []

    for nomeArquivo in os.listdir(PASTA_MUSICAS):
        caminhoCompleto = os.path.join(
            PASTA_MUSICAS,
            nomeArquivo
        )

        if not os.path.isfile(caminhoCompleto):
            continue

        extensao = os.path.splitext(nomeArquivo)[1].lower()

        if extensao in [".mp3", ".wav", ".ogg", ".flac"]:
            arquivos.append(nomeArquivo)

    arquivos.sort()

    return arquivos


def mostrarArquivos(arquivos):
    print("ARQUIVOS ENCONTRADOS")
    print("-" * 60)

    for numero, arquivo in enumerate(arquivos, start=1):
        print(f"{numero}. {arquivo}")

    print("-" * 60)
    print()


def escolherArquivo(arquivos):
    while True:
        escolha = input(
            "ESCOLHA O NUMERO DO ARQUIVO OU 0 PARA CANCELAR: "
        ).strip()

        if escolha == "0":
            return None

        if not escolha.isdigit():
            print()
            print("DIGITE UM NUMERO VALIDO.")
            print()
            continue

        indice = int(escolha) - 1

        if indice < 0 or indice >= len(arquivos):
            print()
            print("ARQUIVO NAO ENCONTRADO.")
            print()
            continue

        return arquivos[indice]


def limparTitulo(titulo):
    termos = [
        r"\(official video\)",
        r"\(official audio\)",
        r"\(official music video\)",
        r"\(lyrics\)",
        r"\(lyric video\)",
        r"\(visualizer\)",
        r"\(hd\)",
        r"\(4k\)",
        r"\[official video\]",
        r"\[official audio\]",
        r"\[lyrics\]",
        r"kissvk\.com",
        r"www\."
    ]

    tituloLimpo = titulo

    for termo in termos:
        tituloLimpo = re.sub(
            termo,
            "",
            tituloLimpo,
            flags=re.IGNORECASE
        )

    tituloLimpo = re.sub(
        r"\s+",
        " ",
        tituloLimpo
    )

    tituloLimpo = tituloLimpo.strip(" -_")

    return tituloLimpo


def separarNome(nomeArquivo):
    nomeSemExtensao = os.path.splitext(nomeArquivo)[0]

    if " - " in nomeSemExtensao:
        partes = nomeSemExtensao.split(" - ", 1)

    elif "-" in nomeSemExtensao:
        partes = nomeSemExtensao.split("-", 1)

    else:
        return "DESCONHECIDO", limparTitulo(nomeSemExtensao)

    artista = partes[0].strip()
    titulo = limparTitulo(partes[1].strip())

    if not artista:
        artista = "DESCONHECIDO"

    if not titulo:
        titulo = nomeSemExtensao

    return artista, titulo


def buscarDuracao(caminho):
    try:
        resultado = subprocess.run(
            [
                "ffprobe",
                "-v",
                "error",
                "-show_entries",
                "format=duration",
                "-of",
                "default=noprint_wrappers=1:nokey=1",
                caminho
            ],
            capture_output=True,
            text=True,
            check=True
        )

        duracaoTexto = resultado.stdout.strip()

        if not duracaoTexto:
            return 0

        duracao = float(duracaoTexto)

        if duracao <= 0:
            return 0

        return round(duracao)

    except FileNotFoundError:
        print()
        print("ERRO: FFPROBE NAO FOI ENCONTRADO.")
        print("INSTALE O FFMPEG PARA LER A DURACAO.")
        return 0

    except subprocess.CalledProcessError as erro:
        print()
        print("ERRO AO ANALISAR O ARQUIVO DE AUDIO.")

        mensagem = erro.stderr.strip()

        if mensagem:
            print(mensagem)

        return 0

    except ValueError:
        print()
        print("A DURACAO RETORNADA PELO FFPROBE E INVALIDA.")
        return 0


def adicionarMusica():
    mostrarCarregamento()

    arquivos = buscarArquivos()

    if not arquivos:
        print("NENHUM ARQUIVO DE AUDIO FOI ENCONTRADO.")
        print()
        print(
            "COLOQUE AS MUSICAS DENTRO DA PASTA:",
            PASTA_MUSICAS
        )
        print()
        return

    mostrarArquivos(arquivos)

    arquivoEscolhido = escolherArquivo(arquivos)

    if arquivoEscolhido is None:
        print()
        print("CADASTRO CANCELADO.")
        print()
        return

    caminho = os.path.join(
        PASTA_MUSICAS,
        arquivoEscolhido
    )

    caminho = os.path.abspath(caminho)

    artistaSugerido, tituloSugerido = separarNome(
        arquivoEscolhido
    )

    print()
    print("INFORMACOES SUGERIDAS")
    print("-" * 60)
    print("TITULO  :", tituloSugerido)
    print("ARTISTA :", artistaSugerido)
    print("-" * 60)
    print()
    print("PRESSIONE ENTER PARA ACEITAR A SUGESTAO.")
    print()

    titulo = input(
        f"TITULO [{tituloSugerido}]: "
    ).strip()

    if not titulo:
        titulo = tituloSugerido

    artista = input(
        f"ARTISTA [{artistaSugerido}]: "
    ).strip()

    if not artista:
        artista = artistaSugerido

    album = input("ALBUM: ").strip()

    print()
    print("ANALISANDO DURACAO DO ARQUIVO...")

    duracao = buscarDuracao(caminho)

    if duracao <= 0:
        print()
        print("NAO FOI POSSIVEL IDENTIFICAR A DURACAO.")
        print("A MUSICA NAO FOI CADASTRADA.")
        print()
        return

    cadastrarMusica(
        titulo,
        artista,
        album,
        caminho,
        duracao
    )

    print()
    print("MUSICA CADASTRADA COM SUCESSO.")
    print("TITULO  :", titulo)
    print("ARTISTA :", artista)

    if album:
        print("ALBUM   :", album)

    print("TEMPO   :", formatarDuracao(duracao))
    print()


def abrirBiblioteca():
    musicas = listarMusicas()

    print()
    print("=" * 60)
    print("                    BIBLIOTECA NRC MUSIC")
    print("=" * 60)
    print()

    if not musicas:
        print("NENHUMA MUSICA CADASTRADA.")
        print()
        return

    for musica in musicas:
        idMusica = musica[0]
        titulo = musica[1]
        artista = musica[2]
        album = musica[3]
        duracao = musica[5]

        print("ID      :", idMusica)
        print("TITULO  :", titulo)
        print("ARTISTA :", artista)

        if album:
            print("ALBUM   :", album)
        else:
            print("ALBUM   : NAO INFORMADO")

        print("TEMPO   :", formatarDuracao(duracao))
        print("-" * 60)

    print()