from sistema import iniciarSistema
from sistema import mostrarAjuda
from sistema import mostrarSobre
from sistema import limparTela
from sistema import desligarSistema
from sistema import programaIndisponivel

from banco import criarBanco

from programas.biblioteca import adicionarMusica
from programas.biblioteca import abrirBiblioteca


def executarComando(comando):
    if comando == "help":
        mostrarAjuda()

    elif comando == "clear":
        limparTela()

    elif comando == "about":
        mostrarSobre()

    elif comando == "music":
        programaIndisponivel("MUSIC PLAYER")

    elif comando == "library":
        abrirBiblioteca()

    elif comando == "add":
        adicionarMusica()

    elif comando == "search":
        programaIndisponivel("PESQUISA DE MUSICA")

    elif comando == "remove":
        programaIndisponivel("REMOVER MUSICA")

    elif comando == "shutdown":
        desligarSistema()
        return False

    elif comando == "":
        pass

    else:
        print()
        print("COMANDO NAO RECONHECIDO:", comando)
        print("DIGITE HELP PARA VER OS COMANDOS.")
        print()

    return True


def abrirTerminal():
    criarBanco()
    iniciarSistema()

    sistemaLigado = True

    while sistemaLigado:
        comando = input("music@nova > ")

        comando = comando.lower()
        comando = comando.strip()

        sistemaLigado = executarComando(comando)


abrirTerminal()