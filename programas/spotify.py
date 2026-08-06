import os
import time
import unicodedata

import requests
from dotenv import load_dotenv


load_dotenv()


URLTOKEN = "https://accounts.spotify.com/api/token"
URLPESQUISA = "https://api.spotify.com/v1/search"

tokenAtual = None
tokenExpiraEm = 0


def lerCredenciais():
    clientId = os.getenv(
        "SPOTIFYCLIENTID"
    )

    clientSecret = os.getenv(
        "SPOTIFYCLIENTSECRET"
    )

    if not clientId or not clientSecret:
        return None, None

    return clientId, clientSecret


def obterToken():
    global tokenAtual
    global tokenExpiraEm

    agora = time.time()

    if (
        tokenAtual
        and agora < tokenExpiraEm
    ):
        return tokenAtual

    clientId, clientSecret = lerCredenciais()

    if not clientId or not clientSecret:
        print()
        print(
            "CREDENCIAIS DO SPOTIFY "
            "NAO ENCONTRADAS."
        )
        print("VERIFIQUE O ARQUIVO .env.")
        print()

        return None

    try:
        resposta = requests.post(
            URLTOKEN,
            data={
                "grant_type":
                "client_credentials"
            },
            auth=(
                clientId,
                clientSecret
            ),
            timeout=15
        )

        resposta.raise_for_status()

        dados = resposta.json()

        tokenAtual = dados.get(
            "access_token"
        )

        tempoValidade = dados.get(
            "expires_in",
            3600
        )

        tokenExpiraEm = (
            agora
            + tempoValidade
            - 60
        )

        return tokenAtual

    except requests.exceptions.Timeout:
        print()
        print(
            "O SPOTIFY DEMOROU MUITO "
            "PARA RESPONDER."
        )
        print()

    except requests.exceptions.ConnectionError:
        print()
        print(
            "NAO FOI POSSIVEL CONECTAR "
            "AO SPOTIFY."
        )
        print("VERIFIQUE SUA INTERNET.")
        print()

    except requests.exceptions.HTTPError:
        print()
        print(
            "O SPOTIFY RECUSOU "
            "AS CREDENCIAIS."
        )

        try:
            erro = resposta.json()

            mensagem = erro.get(
                "error_description",
                erro.get(
                    "error",
                    ""
                )
            )

            if mensagem:
                print(
                    "DETALHES:",
                    mensagem
                )

        except ValueError:
            pass

        print()

    except requests.exceptions.RequestException as erro:
        print()
        print("ERRO AO ACESSAR O SPOTIFY.")
        print("DETALHES:", erro)
        print()

    return None


def removerAcentos(texto):
    texto = str(texto or "")

    textoNormalizado = unicodedata.normalize(
        "NFD",
        texto
    )

    caracteres = []

    for caractere in textoNormalizado:
        if not unicodedata.combining(
            caractere
        ):
            caracteres.append(
                caractere
            )

    return "".join(caracteres)


def normalizarTexto(texto):
    texto = removerAcentos(texto)
    texto = texto.lower().strip()

    texto = texto.replace(
        "’",
        "'"
    )

    texto = texto.replace(
        "–",
        "-"
    )

    texto = texto.replace(
        "—",
        "-"
    )

    texto = " ".join(
        texto.split()
    )

    return texto


def criarPesquisa(titulo, artista):
    titulo = str(
        titulo or ""
    ).strip()

    artista = str(
        artista or ""
    ).strip()

    if titulo and artista:
        return (
            f'track:"{titulo}" '
            f'artist:"{artista}"'
        )

    if titulo:
        return f'track:"{titulo}"'

    return artista


def obterArtistas(item):
    artistas = item.get(
        "artists",
        []
    )

    nomes = []

    for artista in artistas:
        nome = artista.get(
            "name"
        )

        if nome:
            nomes.append(
                nome
            )

    return ", ".join(nomes)


def obterAno(item):
    album = item.get(
        "album",
        {}
    )

    data = album.get(
        "release_date",
        ""
    )

    if not data:
        return ""

    return data[:4]


def tratarResultado(item):
    album = item.get(
        "album",
        {}
    )

    popularidade = item.get(
        "popularity"
    )

    return {
        "titulo": item.get(
            "name",
            ""
        ),
        "artista": obterArtistas(
            item
        ),
        "album": album.get(
            "name",
            ""
        ),
        "tipoAlbum": album.get(
            "album_type",
            ""
        ),
        "ano": obterAno(
            item
        ),
        "faixa": item.get(
            "track_number"
        ),
        "disco": item.get(
            "disc_number"
        ),
        "popularidade": popularidade
    }


def contemTermo(texto, termos):
    texto = normalizarTexto(texto)

    for termo in termos:
        termoNormalizado = normalizarTexto(
            termo
        )

        if termoNormalizado in texto:
            return True

    return False


def calcularPontuacao(
    musica,
    tituloBuscado,
    artistaBuscado
):
    pontos = 0

    titulo = normalizarTexto(
        musica.get("titulo")
    )

    artista = normalizarTexto(
        musica.get("artista")
    )

    album = normalizarTexto(
        musica.get("album")
    )

    tipoAlbum = normalizarTexto(
        musica.get("tipoAlbum")
    )

    tituloEsperado = normalizarTexto(
        tituloBuscado
    )

    artistaEsperado = normalizarTexto(
        artistaBuscado
    )

    if titulo == tituloEsperado:
        pontos += 150

    elif titulo.startswith(
        tituloEsperado
    ):
        pontos += 60

    elif tituloEsperado in titulo:
        pontos += 30

    if artista == artistaEsperado:
        pontos += 120

    elif artista.startswith(
        artistaEsperado
    ):
        pontos += 60

    elif artistaEsperado in artista:
        pontos += 30

    if tipoAlbum == "album":
        pontos += 40

    elif tipoAlbum == "single":
        pontos += 15

    elif tipoAlbum == "compilation":
        pontos -= 60

    termosVersao = [
        "radio edit",
        "radio version",
        "remix",
        "remastered",
        "remaster",
        "live",
        "acoustic",
        "instrumental",
        "karaoke",
        "sped up",
        "slowed",
        "nightcore",
        "edit"
    ]

    if contemTermo(
        titulo,
        termosVersao
    ):
        pontos -= 100

    termosAlbumRuim = [
        "greatest hits",
        "best of",
        "songs to",
        "chill",
        "party hits",
        "various artists",
        "karaoke",
        "tribute",
        "remixes",
        "remix",
        "collection",
        "compilation"
    ]

    if contemTermo(
        album,
        termosAlbumRuim
    ):
        pontos -= 70

    ano = musica.get(
        "ano"
    )

    if ano and str(ano).isdigit():
        pontos += 5

    faixa = musica.get(
        "faixa"
    )

    if faixa is not None:
        pontos += 5

    return pontos


def ordenarResultados(
    resultados,
    titulo,
    artista
):
    return sorted(
        resultados,
        key=lambda musica: calcularPontuacao(
            musica,
            titulo,
            artista
        ),
        reverse=True
    )


def escolherResultadoOficial(
    resultados,
    titulo,
    artista
):
    if not resultados:
        return None

    resultadosOrdenados = ordenarResultados(
        resultados,
        titulo,
        artista
    )

    melhorResultado = resultadosOrdenados[0]

    melhorResultado = dict(
        melhorResultado
    )

    melhorResultado["pontuacao"] = (
        calcularPontuacao(
            melhorResultado,
            titulo,
            artista
        )
    )

    return melhorResultado


def pesquisarMusica(
    titulo,
    artista,
    quantidade=10
):
    token = obterToken()

    if not token:
        return []

    consulta = criarPesquisa(
        titulo,
        artista
    )

    if not consulta:
        return []

    try:
        quantidade = int(
            quantidade
        )

    except (TypeError, ValueError):
        quantidade = 10

    quantidade = max(
        1,
        min(
            quantidade,
            10
        )
    )

    try:
        resposta = requests.get(
            URLPESQUISA,
            headers={
                "Authorization":
                "Bearer " + token
            },
            params={
                "q": consulta,
                "type": "track",
                "limit": quantidade,
                "market": "BR"
            },
            timeout=15
        )

        resposta.raise_for_status()

        dados = resposta.json()

        faixas = dados.get(
            "tracks",
            {}
        ).get(
            "items",
            []
        )

        resultados = []

        for item in faixas:
            resultados.append(
                tratarResultado(
                    item
                )
            )

        return resultados

    except requests.exceptions.Timeout:
        print()
        print(
            "A PESQUISA NO SPOTIFY "
            "EXPIROU."
        )
        print()

    except requests.exceptions.ConnectionError:
        print()
        print(
            "SEM CONEXAO COM O SPOTIFY."
        )
        print()

    except requests.exceptions.HTTPError:
        print()
        print(
            "ERRO NA PESQUISA "
            "DO SPOTIFY."
        )
        print(
            "CODIGO:",
            resposta.status_code
        )

        try:
            print(
                "DETALHES:",
                resposta.json()
            )

        except ValueError:
            pass

        print()

    except requests.exceptions.RequestException as erro:
        print()
        print(
            "ERRO AO PESQUISAR "
            "NO SPOTIFY."
        )
        print(
            "DETALHES:",
            erro
        )
        print()

    return []


def pesquisarResultadoOficial(
    titulo,
    artista
):
    resultados = pesquisarMusica(
        titulo,
        artista,
        10
    )

    return escolherResultadoOficial(
        resultados,
        titulo,
        artista
    )


def formatarFaixa(faixa):
    if faixa is None:
        return "NAO INFORMADA"

    try:
        return f"{int(faixa):02}"

    except (TypeError, ValueError):
        return str(faixa)


def mostrarMusica(musica):
    if not musica:
        print(
            "NENHUMA MUSICA ENCONTRADA."
        )
        return

    print("-" * 60)
    print(
        "TITULO    :",
        musica.get(
            "titulo",
            ""
        )
    )
    print(
        "ARTISTA   :",
        musica.get(
            "artista",
            ""
        )
    )
    print(
        "ALBUM     :",
        musica.get(
            "album",
            ""
        )
    )
    print(
        "TIPO      :",
        musica.get(
            "tipoAlbum",
            ""
        )
    )
    print(
        "ANO       :",
        musica.get(
            "ano"
        ) or "NAO INFORMADO"
    )
    print(
        "FAIXA     :",
        formatarFaixa(
            musica.get(
                "faixa"
            )
        )
    )

    popularidade = musica.get(
        "popularidade"
    )

    if popularidade is None:
        print(
            "POPULAR   :",
            "INDISPONIVEL"
        )

    else:
        print(
            "POPULAR   :",
            popularidade
        )

    if "pontuacao" in musica:
        print(
            "PONTUACAO :",
            musica["pontuacao"]
        )

    print("-" * 60)


def mostrarResultados(
    resultados,
    titulo="",
    artista=""
):
    if not resultados:
        print(
            "NENHUMA MUSICA ENCONTRADA."
        )
        return

    if titulo or artista:
        resultados = ordenarResultados(
            resultados,
            titulo,
            artista
        )

    for numero, musica in enumerate(
        resultados,
        start=1
    ):
        print("-" * 60)
        print(
            "RESULTADO :",
            numero
        )
        print(
            "TITULO    :",
            musica.get(
                "titulo",
                ""
            )
        )
        print(
            "ARTISTA   :",
            musica.get(
                "artista",
                ""
            )
        )
        print(
            "ALBUM     :",
            musica.get(
                "album",
                ""
            )
        )
        print(
            "TIPO      :",
            musica.get(
                "tipoAlbum",
                ""
            )
        )
        print(
            "ANO       :",
            musica.get(
                "ano"
            ) or "NAO INFORMADO"
        )
        print(
            "FAIXA     :",
            formatarFaixa(
                musica.get(
                    "faixa"
                )
            )
        )

        popularidade = musica.get(
            "popularidade"
        )

        if popularidade is None:
            print(
                "POPULAR   :",
                "INDISPONIVEL"
            )

        else:
            print(
                "POPULAR   :",
                popularidade
            )

        if titulo or artista:
            pontos = calcularPontuacao(
                musica,
                titulo,
                artista
            )

            print(
                "PONTUACAO :",
                pontos
            )

    print("-" * 60)