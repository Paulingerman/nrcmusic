import os
import time
from datetime import datetime


def limparTela():
    os.system("clear")


def esperar(tempo):
    time.sleep(tempo)


def mostrarLinha():
    print("═" * 60)


def mostrarCabecalho(titulo):
    largura = 58

    print("╔" + "═" * largura + "╗")
    print("║" + titulo.center(largura) + "║")
    print("╚" + "═" * largura + "╝")


def iniciarSistema():
    limparTela()

    print("NOVA BIOS V1.0")
    print()

    esperar(0.5)
    print("CPU.........................OK")

    esperar(0.5)
    print("MEMORIA.....................640 KB")

    esperar(0.5)
    print("VIDEO.......................OK")

    esperar(0.5)
    print("AUDIO.......................OK")

    esperar(0.5)
    print("BANCO DE DADOS..............OK")

    print()
    print("INICIANDO NOVA OS...")
    esperar(1.5)

    limparTela()

    mostrarCabecalho("OPERATING SYSTEM")

    print()
    print("VERSAO 1.0")
    print("USUARIO: PAULO")
    print("DATA:", datetime.now().strftime("%d/%m/%Y"))
    print("HORA:", datetime.now().strftime("%H:%M"))
    print()

    print("SISTEMA PRONTO.")
    print("DIGITE HELP PARA VER OS COMANDOS.")
    print()


def mostrarAjuda():
    print()
    mostrarCabecalho("COMANDOS DE MUSICA")
    print()

    print("help        Mostrar comandos")
    print("music       Abrir o player")
    print("library     Ver biblioteca")
    print("add         Cadastrar musica")
    print("search      Pesquisar musica")
    print("remove      Remover musica")
    print("clear       Limpar a tela")
    print("about       Informacoes do sistema")
    print("shutdown    Encerrar o sistema")
    print()


def mostrarSobre():
    print()
    mostrarCabecalho("INFORMACOES DO SISTEMA")
    print()

    print("NOME...............NOVA OS")
    print("VERSAO.............1.0")
    print("LINGUAGEM..........PYTHON")
    print("DESENVOLVEDOR......PAULO")
    print("INTERFACE...........TERMINAL")
    print()


def programaIndisponivel(nome):
    print()
    mostrarCabecalho(nome)
    print()
    print("PROGRAMA AINDA NAO INSTALADO.")
    print()


def desligarSistema():
    print()
    print("ENCERRANDO PROGRAMAS...")
    esperar(0.8)

    print("SALVANDO DADOS...")
    esperar(0.8)

    print("DESLIGANDO SISTEMA...")
    esperar(1.5)

    limparTela()

    mostrarCabecalho("SISTEMA DESLIGADO")
    print()
    print("AGORA VOCE PODE FECHAR O TERMINAL.")
    print()