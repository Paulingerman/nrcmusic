import os

os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "1"

import time
from pathlib import Path

import pygame

from banco import buscarMusica
from sistema import limparTela
from sistema import mostrarCabecalho


PASTA_PROJETO = Path(__file__).resolve().parent.parent


def formatarDuracao(segundos):
    try:
        segundos = int(segundos)

    except (TypeError, ValueError):
        segundos = 0

    if segundos < 0:
        segundos = 0

    minutos = segundos // 60
    segundosRestantes = segundos % 60

    return f"{minutos:02}:{segundosRestantes:02}"


def criarCaminhoCompleto(caminho):
    caminhoRecebido = Path(caminho)

    if caminhoRecebido.is_absolute():
        return caminhoRecebido

    return PASTA_PROJETO / caminhoRecebido


def criarBarra(atual, total):
    tamanho = 30

    if total <= 0:
        preenchido = 0

    else:
        preenchido = int(
            (atual / total) * tamanho
        )

    if preenchido < 0:
        preenchido = 0

    if preenchido > tamanho:
        preenchido = tamanho

    barra = "█" * preenchido
    barra += "░" * (tamanho - preenchido)

    return barra


def mostrarTela(
    musica,
    tempoAtual,
    pausada
):
    titulo = musica[1]
    artista = musica[2]
    album = musica[3]
    duracao = musica[5]

    limparTela()
    mostrarCabecalho("NRC MUSIC PLAYER")
    print()

    print("♪", titulo)
    print()
    print("ARTISTA :", artista)

    if album:
        print("ALBUM   :", album)

    else:
        print("ALBUM   : NAO INFORMADO")

    print()
    print(criarBarra(tempoAtual, duracao))
    print()
    print(
        formatarDuracao(tempoAtual),
        "/",
        formatarDuracao(duracao)
    )
    print()

    if pausada:
        print("STATUS  : PAUSADO")

    else:
        print("STATUS  : TOCANDO")

    print()
    print("[P] PAUSAR OU CONTINUAR")
    print("[S] PARAR")
    print("[Q] SAIR DO PLAYER")
    print()


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


def tocarMusica(idMusica):
    musica = buscarMusica(idMusica)

    if musica is None:
        print()
        print("MUSICA NAO ENCONTRADA.")
        print()

        return

    caminhoSalvo = musica[4]
    caminhoCompleto = criarCaminhoCompleto(
        caminhoSalvo
    )

    duracao = musica[5]

    if not caminhoCompleto.is_file():
        print()
        print("ARQUIVO DE AUDIO NAO ENCONTRADO:")
        print(caminhoCompleto)
        print()
        print("REMOVA O REGISTRO ANTIGO E")
        print("CADASTRE A MUSICA NOVAMENTE.")
        print()

        return

    if not iniciarAudio():
        return

    try:
        pygame.mixer.music.load(
            str(caminhoCompleto)
        )

        pygame.mixer.music.play()

    except pygame.error as erro:
        print()
        print("NAO FOI POSSIVEL REPRODUZIR")
        print("A MUSICA.")
        print("ERRO:", erro)
        print()

        return

    inicio = time.time()
    tempoPausado = 0
    inicioPausa = 0
    pausada = False

    while True:
        if pausada:
            tempoAtual = (
                inicioPausa
                - inicio
                - tempoPausado
            )

        else:
            tempoAtual = (
                time.time()
                - inicio
                - tempoPausado
            )

        if tempoAtual < 0:
            tempoAtual = 0

        if duracao > 0 and tempoAtual > duracao:
            tempoAtual = duracao

        mostrarTela(
            musica,
            tempoAtual,
            pausada
        )

        if (
            not pygame.mixer.music.get_busy()
            and not pausada
        ):
            break

        comando = input(
            "PLAYER > "
        ).strip().lower()

        if comando == "p":
            if pausada:
                pygame.mixer.music.unpause()

                tempoPausado += (
                    time.time()
                    - inicioPausa
                )

                pausada = False

            else:
                pygame.mixer.music.pause()

                inicioPausa = time.time()
                pausada = True

        elif comando == "s":
            pygame.mixer.music.stop()
            break

        elif comando == "q":
            pygame.mixer.music.stop()
            break

        elif comando == "":
            continue

        else:
            print()
            print("COMANDO DO PLAYER INVALIDO.")
            time.sleep(1)

    print()
    print("PLAYER ENCERRADO.")
    print()