import os

os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "1"

import curses
import locale
import time
from pathlib import Path

import pygame

from banco import buscarMusica


locale.setlocale(locale.LC_ALL, "")

PASTA_PROJETO = Path(__file__).resolve().parent.parent

LARGURA_PLAYER = 64
TAMANHO_BARRA_PROGRESSO = 42
TAMANHO_BARRA_VOLUME = 20
INTERVALO_ATUALIZACAO = 0.1


def formatarDuracao(segundos):
    try:
        segundos = int(segundos)

    except (TypeError, ValueError):
        segundos = 0

    segundos = max(0, segundos)

    minutos = segundos // 60
    segundosRestantes = segundos % 60

    return f"{minutos:02}:{segundosRestantes:02}"


def criarCaminhoCompleto(caminho):
    caminhoRecebido = Path(caminho)

    if caminhoRecebido.is_absolute():
        return caminhoRecebido

    return PASTA_PROJETO / caminhoRecebido


def limitarTexto(texto, tamanho):
    texto = str(texto or "")

    if len(texto) <= tamanho:
        return texto

    return texto[: tamanho - 3] + "..."


def criarBarraProgresso(tempoAtual, duracao):
    if duracao <= 0:
        progresso = 0

    else:
        progresso = tempoAtual / duracao

    progresso = max(0, min(progresso, 1))

    preenchido = int(
        progresso * TAMANHO_BARRA_PROGRESSO
    )

    vazio = (
        TAMANHO_BARRA_PROGRESSO
        - preenchido
    )

    return (
        "█" * preenchido
        + "░" * vazio
    )


def criarBarraVolume(volume):
    volume = max(0, min(volume, 1))

    preenchido = int(
        volume * TAMANHO_BARRA_VOLUME
    )

    vazio = (
        TAMANHO_BARRA_VOLUME
        - preenchido
    )

    return (
        "█" * preenchido
        + "░" * vazio
    )


def iniciarAudio():
    try:
        if not pygame.mixer.get_init():
            pygame.mixer.init()

        return True

    except pygame.error as erro:
        print()
        print("NAO FOI POSSIVEL INICIAR O AUDIO.")
        print("ERRO:", erro)
        print()

        return False


def escreverSeguro(
    tela,
    linha,
    coluna,
    texto,
    atributo=0
):
    alturaTerminal, larguraTerminal = (
        tela.getmaxyx()
    )

    if linha < 0 or linha >= alturaTerminal:
        return

    if coluna < 0 or coluna >= larguraTerminal:
        return

    espacoDisponivel = (
        larguraTerminal
        - coluna
        - 1
    )

    if espacoDisponivel <= 0:
        return

    texto = str(texto)
    texto = texto[:espacoDisponivel]

    try:
        tela.addstr(
            linha,
            coluna,
            texto,
            atributo
        )

    except curses.error:
        pass


def linhaComBordas(conteudo=""):
    larguraInterna = LARGURA_PLAYER - 2

    conteudo = limitarTexto(
        conteudo,
        larguraInterna
    )

    return (
        "║"
        + conteudo.ljust(larguraInterna)
        + "║"
    )


def desenharPlayer(
    tela,
    musica,
    tempoAtual,
    pausada,
    volume
):
    tela.erase()

    alturaTerminal, larguraTerminal = (
        tela.getmaxyx()
    )

    alturaPlayer = 25

    if (
        larguraTerminal < LARGURA_PLAYER
        or alturaTerminal < alturaPlayer
    ):
        escreverSeguro(
            tela,
            1,
            2,
            "AUMENTE O TAMANHO DO TERMINAL."
        )

        escreverSeguro(
            tela,
            3,
            2,
            (
                f"MINIMO: "
                f"{LARGURA_PLAYER} COLUNAS "
                f"X {alturaPlayer} LINHAS"
            )
        )

        tela.refresh()
        return

    colunaInicial = max(
        0,
        (
            larguraTerminal
            - LARGURA_PLAYER
        ) // 2
    )

    linhaInicial = max(
        0,
        (
            alturaTerminal
            - alturaPlayer
        ) // 2
    )

    titulo = limitarTexto(
        musica[1],
        47
    )

    artista = limitarTexto(
        musica[2],
        46
    )

    album = musica[3]

    if album:
        album = limitarTexto(
            album,
            48
        )

    else:
        album = "NAO INFORMADO"

    duracao = musica[6]

    barraProgresso = criarBarraProgresso(
        tempoAtual,
        duracao
    )

    barraVolume = criarBarraVolume(
        volume
    )

    porcentagemVolume = round(
        volume * 100
    )

    if pausada:
        status = "|| PAUSADO"

    else:
        status = "> TOCANDO"

    larguraInterna = LARGURA_PLAYER - 2

    linhas = [
        "╔" + "═" * larguraInterna + "╗",
        linhaComBordas(
            "NRC MUSIC PLAYER".center(
                larguraInterna
            )
        ),
        "╠" + "═" * larguraInterna + "╣",
        linhaComBordas(),
        linhaComBordas("  TOCANDO AGORA"),
        linhaComBordas(),
        linhaComBordas(
            f"  TITULO  : {titulo}"
        ),
        linhaComBordas(
            f"  ARTISTA : {artista}"
        ),
        linhaComBordas(
            f"  ALBUM   : {album}"
        ),
        linhaComBordas(),
        linhaComBordas(
            f"  [{barraProgresso}]"
        ),
        linhaComBordas(),
        linhaComBordas(
            "  "
            + formatarDuracao(tempoAtual)
            + " / "
            + formatarDuracao(duracao)
        ),
        linhaComBordas(
            f"  STATUS  : {status}"
        ),
        linhaComBordas(),
        linhaComBordas(
            f"  VOLUME  : [{barraVolume}] "
            f"{porcentagemVolume:3}%"
        ),
        linhaComBordas(),
        "╠" + "═" * larguraInterna + "╣",
        linhaComBordas(
            "  [P] PAUSAR OU CONTINUAR"
        ),
        linhaComBordas(
            "  [+] AUMENTAR VOLUME"
        ),
        linhaComBordas(
            "  [-] DIMINUIR VOLUME"
        ),
        linhaComBordas(
            "  [S] PARAR"
        ),
        linhaComBordas(
            "  [Q] SAIR DO PLAYER"
        ),
        "╚" + "═" * larguraInterna + "╝"
    ]

    for indice, linha in enumerate(linhas):
        atributo = curses.A_NORMAL

        if indice == 1:
            atributo = curses.A_BOLD

        escreverSeguro(
            tela,
            linhaInicial + indice,
            colunaInicial,
            linha,
            atributo
        )

    tela.refresh()


def calcularTempoAtual(
    inicioMusica,
    tempoTotalPausado,
    inicioPausa,
    pausada
):
    if pausada:
        instanteAtual = inicioPausa

    else:
        instanteAtual = time.monotonic()

    tempoAtual = (
        instanteAtual
        - inicioMusica
        - tempoTotalPausado
    )

    return max(0, tempoAtual)


def executarPlayer(
    tela,
    musica,
    volumeInicial
):
    curses.curs_set(0)

    tela.nodelay(True)
    tela.keypad(True)

    try:
        curses.use_default_colors()

    except curses.error:
        pass

    volume = volumeInicial
    pausada = False
    inicioPausa = None
    tempoTotalPausado = 0
    inicioMusica = time.monotonic()
    playerAberto = True

    duracao = musica[6]

    while playerAberto:
        tempoAtual = calcularTempoAtual(
            inicioMusica,
            tempoTotalPausado,
            inicioPausa,
            pausada
        )

        if duracao > 0:
            tempoAtual = min(
                tempoAtual,
                duracao
            )

        desenharPlayer(
            tela,
            musica,
            tempoAtual,
            pausada,
            volume
        )

        if (
            not pausada
            and not pygame.mixer.music.get_busy()
        ):
            break

        tecla = tela.getch()

        if tecla in [
            ord("p"),
            ord("P")
        ]:
            if pausada:
                pygame.mixer.music.unpause()

                tempoTotalPausado += (
                    time.monotonic()
                    - inicioPausa
                )

                inicioPausa = None
                pausada = False

            else:
                pygame.mixer.music.pause()

                inicioPausa = time.monotonic()
                pausada = True

        elif tecla in [
            ord("+"),
            ord("=")
        ]:
            volume = min(
                1.0,
                round(volume + 0.1, 1)
            )

            pygame.mixer.music.set_volume(
                volume
            )

        elif tecla == ord("-"):
            volume = max(
                0.0,
                round(volume - 0.1, 1)
            )

            pygame.mixer.music.set_volume(
                volume
            )

        elif tecla in [
            ord("s"),
            ord("S"),
            ord("q"),
            ord("Q")
        ]:
            pygame.mixer.music.stop()
            playerAberto = False

        time.sleep(
            INTERVALO_ATUALIZACAO
        )


def tocarMusica(idMusica):
    musica = buscarMusica(idMusica)

    if musica is None:
        print()
        print("MUSICA NAO ENCONTRADA.")
        print()

        return

    caminhoSalvo = musica[5]

    caminhoCompleto = criarCaminhoCompleto(
        caminhoSalvo
    )

    if not caminhoCompleto.is_file():
        print()
        print("ARQUIVO DE AUDIO NAO ENCONTRADO.")
        print()
        print("CAMINHO:")
        print(caminhoCompleto)
        print()

        return

    if not iniciarAudio():
        return

    volumeInicial = 0.7

    try:
        pygame.mixer.music.load(
            str(caminhoCompleto)
        )

        pygame.mixer.music.set_volume(
            volumeInicial
        )

        pygame.mixer.music.play()

    except pygame.error as erro:
        print()
        print("NAO FOI POSSIVEL TOCAR A MUSICA.")
        print("ERRO:", erro)
        print()

        return

    try:
        curses.wrapper(
            executarPlayer,
            musica,
            volumeInicial
        )

    except KeyboardInterrupt:
        pygame.mixer.music.stop()

    except curses.error as erro:
        pygame.mixer.music.stop()

        print()
        print("ERRO AO ABRIR A INTERFACE DO PLAYER.")
        print("ERRO:", erro)
        print()
        print("EXECUTE O PROGRAMA EM UM TERMINAL REAL.")
        print()

        return

    finally:
        pygame.mixer.music.stop()

    print()
    print("REPRODUCAO ENCERRADA.")
    print()