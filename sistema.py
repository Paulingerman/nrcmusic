import os
import time
from datetime import datetime


def limparTela():
    if os.name == "nt":
        os.system("cls")

    else:
        os.system("clear")


def esperar(tempo):
    time.sleep(tempo)


def mostrarLinha():
    print(
        "═" * 60
    )


def mostrarCabecalho(titulo):
    largura = 58

    print(
        "╔"
        + "═" * largura
        + "╗"
    )

    print(
        "║"
        + titulo.center(largura)
        + "║"
    )

    print(
        "╚"
        + "═" * largura
        + "╝"
    )


def iniciarSistema():
    limparTela()

    print(
        "NRC MUSIC BIOS V1.0"
    )
    print()

    esperar(0.3)
    print(
        "CPU.........................OK"
    )

    esperar(0.3)
    print(
        "MEMORIA.....................OK"
    )

    esperar(0.3)
    print(
        "VIDEO.......................OK"
    )

    esperar(0.3)
    print(
        "AUDIO.......................OK"
    )

    esperar(0.3)
    print(
        "BANCO DE DADOS..............OK"
    )

    print()
    print(
        "INICIANDO NRC MUSIC OS..."
    )

    esperar(1.2)

    limparTela()

    mostrarCabecalho(
        "NRC MUSIC OS"
    )

    print()
    print(
        "VERSAO : 1.0"
    )
    print(
        "USUARIO: PAULO"
    )
    print(
        "DATA   :",
        datetime.now().strftime(
            "%d/%m/%Y"
        )
    )
    print(
        "HORA   :",
        datetime.now().strftime(
            "%H:%M"
        )
    )
    print()

    print(
        "SISTEMA PRONTO."
    )
    print(
        "DIGITE HELP PARA "
        "VER OS COMANDOS."
    )
    print()


def mostrarAjuda():
    print()

    mostrarCabecalho(
        "COMANDOS DO NRC MUSIC"
    )

    print()

    print(
        "help             "
        "Mostrar comandos"
    )

    print(
        "library          "
        "Ver biblioteca"
    )

    print(
        "ls               "
        "Ver biblioteca"
    )

    print(
        "add              "
        "Cadastrar musica"
    )

    print(
        "play ID          "
        "Reproduzir musica"
    )

    print(
        "remove ID        "
        "Remover musica"
    )

    print(
        "scan             "
        "Atualizar duracoes"
    )

    print(
        "spotify update   "
        "Atualizar pelo Spotify"
    )

    print(
        "search           "
        "Pesquisar musica"
    )

    print(
        "clear            "
        "Limpar a tela"
    )

    print(
        "cls              "
        "Limpar a tela"
    )

    print(
        "about            "
        "Informacoes do sistema"
    )

    print(
        "shutdown         "
        "Encerrar o sistema"
    )

    print(
        "exit             "
        "Encerrar o sistema"
    )

    print()


def mostrarSobre():
    print()

    mostrarCabecalho(
        "INFORMACOES DO SISTEMA"
    )

    print()

    print(
        "NOME..............."
        "NRC MUSIC OS"
    )

    print(
        "VERSAO............."
        "1.0"
    )

    print(
        "LINGUAGEM.........."
        "PYTHON"
    )

    print(
        "DESENVOLVEDOR......"
        "PAULO"
    )

    print(
        "INTERFACE..........."
        "TERMINAL"
    )

    print(
        "PLATAFORMAS........."
        "LINUX E WINDOWS"
    )

    print()


def programaIndisponivel(nome):
    print()

    mostrarCabecalho(
        nome
    )

    print()

    print(
        "PROGRAMA AINDA "
        "NAO IMPLEMENTADO."
    )

    print()


def desligarSistema():
    print()

    print(
        "ENCERRANDO PROGRAMAS..."
    )

    esperar(0.5)

    print(
        "SALVANDO DADOS..."
    )

    esperar(0.5)

    print(
        "DESLIGANDO SISTEMA..."
    )

    esperar(1)

    limparTela()

    mostrarCabecalho(
        "SISTEMA DESLIGADO"
    )

    print()

    print(
        "AGORA VOCE PODE "
        "FECHAR O TERMINAL."
    )

    print()