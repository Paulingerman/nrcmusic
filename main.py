from banco import criarBanco

from sistema import desligarSistema
from sistema import iniciarSistema
from sistema import limparTela
from sistema import mostrarAjuda
from sistema import mostrarSobre
from sistema import programaIndisponivel

from programas.biblioteca import adicionarMusica
from programas.biblioteca import abrirBiblioteca
from programas.biblioteca import atualizarBiblioteca
from programas.player import tocarMusica


def executarComando(comando):
    comando = comando.strip().lower()

    if comando == "":
        return True

    if comando == "help":
        mostrarAjuda()

    elif comando in ["library", "ls"]:
        abrirBiblioteca()

    elif comando == "add":
        adicionarMusica()

    elif comando == "play":
        print()
        print("INFORME O ID DA MUSICA.")
        print("EXEMPLO: play 1")
        print()

    elif comando.startswith("play "):
        partes = comando.split()

        if len(partes) != 2:
            print()
            print("USO CORRETO: play ID")
            print("EXEMPLO: play 1")
            print()

            return True

        if not partes[1].isdigit():
            print()
            print("O ID DA MUSICA DEVE SER UM NUMERO.")
            print("EXEMPLO: play 1")
            print()

            return True

        idMusica = int(partes[1])

        tocarMusica(idMusica)

    elif comando == "music":
        print()
        print("USE PLAY SEGUIDO DO ID DA MUSICA.")
        print("EXEMPLO: play 1")
        print()

    elif comando == "scan":
        atualizarBiblioteca()

    elif comando == "search":
        programaIndisponivel(
            "PESQUISAR MUSICA"
        )

    elif comando == "remove":
        programaIndisponivel(
            "REMOVER MUSICA"
        )

    elif comando in ["clear", "cls"]:
        limparTela()

    elif comando == "about":
        mostrarSobre()

    elif comando in ["shutdown", "exit"]:
        desligarSistema()

        return False

    else:
        print()
        print(
            "COMANDO NAO RECONHECIDO:",
            comando
        )
        print("DIGITE HELP PARA VER OS COMANDOS.")
        print()

    return True


def abrirTerminal():
    sistemaLigado = True

    while sistemaLigado:
        try:
            comando = input("music@nrc > ")

            sistemaLigado = executarComando(
                comando
            )

        except KeyboardInterrupt:
            print()
            print()
            print(
                "USE SHUTDOWN PARA DESLIGAR "
                "O SISTEMA."
            )
            print()

        except EOFError:
            print()

            desligarSistema()
            sistemaLigado = False


def iniciarPrograma():
    criarBanco()
    iniciarSistema()
    abrirTerminal()


if __name__ == "__main__":
    iniciarPrograma()