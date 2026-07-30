import os
import time
import pygame

from banco import buscarMusica
from sistema import limparTela
from sistema import mostrarCabecalho


pygame.mixer.init()


def formatarDuracao(segundos):
    segundos = int(segundos)

    minutos = segundos // 60
    segundos = segundos % 60

    return f"{minutos:02}:{segundos:02}"


def criarBarra(atual, total):
    tamanho = 30

    if total <= 0:
        preenchido = 0
    else:
        preenchido = int((atual / total) * tamanho)

    if preenchido > tamanho:
        preenchido = tamanho

    barra = "█" * preenchido
    barra += "░" * (tamanho - preenchido)

    return barra


def mostrarTela(musica, tempoAtual, pausada):
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
    print("[P] PAUSAR/CONTINUAR")
    print("[S] PARAR")
    print("[Q] SAIR DO PLAYER")
    print()


def tocarMusica(idMusica):
    musica = buscarMusica(idMusica)

    if musica is None:
        print()
        print("MUSICA NAO ENCONTRADA.")
        print()
        return

    caminho = musica[4]
    duracao = musica[5]

    if not os.path.isfile(caminho):
        print()
        print("ARQUIVO DE AUDIO NAO ENCONTRADO:")
        print(caminho)
        print()
        return

    try:
        pygame.mixer.music.load(caminho)
        pygame.mixer.music.play()

    except pygame.error as erro:
        print()
        print("NAO FOI POSSIVEL REPRODUZIR A MUSICA.")
        print("ERRO:", erro)
        print()
        return

    inicio = time.time()
    tempoPausado = 0
    inicioPausa = 0
    pausada = False

    while True:
        if pausada:
            tempoAtual = inicioPausa - inicio - tempoPausado
        else:
            tempoAtual = time.time() - inicio - tempoPausado

        if tempoAtual < 0:
            tempoAtual = 0

        if duracao > 0 and tempoAtual > duracao:
            tempoAtual = duracao

        mostrarTela(musica, tempoAtual, pausada)

        if not pygame.mixer.music.get_busy() and not pausada:
            break

        comando = input("PLAYER > ").strip().lower()

        if comando == "p":
            if pausada:
                pygame.mixer.music.unpause()
                tempoPausado += time.time() - inicioPausa
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

    print()
    print("PLAYER ENCERRADO.")
    print()