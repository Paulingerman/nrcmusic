from banco import atualizarMusicaSpotify
from banco import buscarMusica
from banco import listarMusicas

from programas.spotify import (
    pesquisarResultadoOficial
)


def mostrarValor(valor):
    if valor is None:
        return "NAO INFORMADO"

    valor = str(valor).strip()

    if not valor:
        return "NAO INFORMADO"

    return valor


def formatarFaixa(faixa):
    if faixa is None:
        return "NAO INFORMADA"

    try:
        return f"{int(faixa):02}"

    except (TypeError, ValueError):
        return str(faixa)


def limparTituloBusca(titulo):
    titulo = str(
        titulo or ""
    ).strip()

    termos = [
        "-corrigido",
        " - corrigido",
        "(official video)",
        "(official audio)",
        "(official music video)",
        "[official video]",
        "[official audio]",
        "(lyrics)",
        "[lyrics]",
        "(visualizer)"
    ]

    tituloLimpo = titulo

    for termo in termos:
        tituloLimpo = tituloLimpo.replace(
            termo,
            ""
        )

        tituloLimpo = tituloLimpo.replace(
            termo.title(),
            ""
        )

        tituloLimpo = tituloLimpo.replace(
            termo.upper(),
            ""
        )

    tituloLimpo = " ".join(
        tituloLimpo.split()
    )

    return tituloLimpo.strip(
        " -_"
    )


def mostrarListaMusicas():
    musicas = listarMusicas()

    print()
    print("=" * 60)
    print(
        "                 "
        "SPOTIFY UPDATE"
    )
    print("=" * 60)
    print()

    if not musicas:
        print(
            "NENHUMA MUSICA CADASTRADA."
        )
        print()

        return []

    print("MUSICAS DA BIBLIOTECA")
    print("-" * 60)

    for musica in musicas:
        idMusica = musica[0]
        titulo = musica[1]
        artista = musica[2]

        print(
            f"{idMusica} - "
            f"{titulo} - "
            f"{artista}"
        )

    print("-" * 60)
    print()

    return musicas


def mostrarDadosAtuais(musica):
    print()
    print("DADOS ATUAIS")
    print("-" * 60)

    print(
        "TITULO  :",
        mostrarValor(
            musica[1]
        )
    )

    print(
        "ARTISTA :",
        mostrarValor(
            musica[2]
        )
    )

    print(
        "ALBUM   :",
        mostrarValor(
            musica[3]
        )
    )

    print(
        "ANO     :",
        mostrarValor(
            musica[4]
        )
    )

    print(
        "FAIXA   :",
        formatarFaixa(
            musica[7]
        )
    )

    print("-" * 60)


def mostrarDadosSpotify(resultado):
    print()
    print(
        "DADOS ENCONTRADOS NO SPOTIFY"
    )
    print("-" * 60)

    print(
        "TITULO  :",
        mostrarValor(
            resultado.get(
                "titulo"
            )
        )
    )

    print(
        "ARTISTA :",
        mostrarValor(
            resultado.get(
                "artista"
            )
        )
    )

    print(
        "ALBUM   :",
        mostrarValor(
            resultado.get(
                "album"
            )
        )
    )

    print(
        "ANO     :",
        mostrarValor(
            resultado.get(
                "ano"
            )
        )
    )

    print(
        "FAIXA   :",
        formatarFaixa(
            resultado.get(
                "faixa"
            )
        )
    )

    print("-" * 60)


def perguntarId():
    escolha = input(
        "ID DA MUSICA "
        "OU 0 PARA CANCELAR > "
    ).strip()

    if escolha == "0":
        return None

    if not escolha.isdigit():
        print()
        print("ID INVALIDO.")
        print()

        return None

    return int(escolha)


def atualizarComSpotify():
    musicas = mostrarListaMusicas()

    if not musicas:
        return

    idMusica = perguntarId()

    if idMusica is None:
        print()
        print(
            "ATUALIZACAO CANCELADA."
        )
        print()

        return

    musica = buscarMusica(
        idMusica
    )

    if musica is None:
        print()
        print(
            "MUSICA NAO ENCONTRADA."
        )
        print()

        return

    mostrarDadosAtuais(
        musica
    )

    tituloAtual = musica[1]
    artistaAtual = musica[2]

    tituloBusca = limparTituloBusca(
        tituloAtual
    )

    print()
    print(
        "PESQUISANDO NO SPOTIFY..."
    )
    print()

    print(
        "TITULO  :",
        tituloBusca
    )

    print(
        "ARTISTA :",
        artistaAtual
    )

    print()

    resultado = (
        pesquisarResultadoOficial(
            tituloBusca,
            artistaAtual
        )
    )

    if not resultado:
        print()
        print(
            "NENHUM RESULTADO "
            "FOI ENCONTRADO."
        )
        print()

        return

    mostrarDadosSpotify(
        resultado
    )

    confirmacao = input(
        "ATUALIZAR REGISTRO? "
        "[S/N]: "
    ).strip().lower()

    if confirmacao not in [
        "s",
        "sim"
    ]:
        print()
        print(
            "ATUALIZACAO CANCELADA."
        )
        print()

        return

    tituloNovo = (
        resultado.get(
            "titulo"
        )
        or musica[1]
    )

    artistaNovo = (
        resultado.get(
            "artista"
        )
        or musica[2]
    )

    albumNovo = (
        resultado.get(
            "album"
        )
        or musica[3]
    )

    anoNovo = (
        resultado.get(
            "ano"
        )
        or musica[4]
    )

    faixaNova = resultado.get(
        "faixa"
    )

    if faixaNova is None:
        faixaNova = musica[7]

    atualizada = (
        atualizarMusicaSpotify(
            idMusica,
            tituloNovo,
            artistaNovo,
            albumNovo,
            anoNovo,
            faixaNova
        )
    )

    print()

    if atualizada:
        print(
            "MUSICA ATUALIZADA "
            "COM SUCESSO."
        )

        print()
        print("NOVOS DADOS")
        print("-" * 60)

        print(
            "TITULO  :",
            tituloNovo
        )

        print(
            "ARTISTA :",
            artistaNovo
        )

        print(
            "ALBUM   :",
            mostrarValor(
                albumNovo
            )
        )

        print(
            "ANO     :",
            mostrarValor(
                anoNovo
            )
        )

        print(
            "FAIXA   :",
            formatarFaixa(
                faixaNova
            )
        )

        print("-" * 60)

    else:
        print(
            "NAO FOI POSSIVEL "
            "ATUALIZAR A MUSICA."
        )

    print()