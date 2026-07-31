import re
import subprocess
import time
from pathlib import Path

from mutagen import File

from banco import atualizarDuracao
from banco import cadastrarMusica
from banco import listarMusicas


PASTA_PROJETO = Path(__file__).resolve().parent.parent
PASTA_MUSICAS = PASTA_PROJETO / "musicas"

EXTENSOES_AUDIO = [
    ".mp3",
    ".wav",
    ".ogg",
    ".flac"
]


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


def mostrarCarregamento():
    print()
    print("ESCANEANDO PASTA MUSICAS...")
    print()

    tamanho = 30

    for posicao in range(tamanho + 1):
        preenchido = "█" * posicao
        vazio = "░" * (tamanho - posicao)
        porcentagem = int(
            (posicao / tamanho) * 100
        )

        print(
            f"\r[{preenchido}{vazio}] {porcentagem}%",
            end="",
            flush=True
        )

        time.sleep(0.02)

    print()
    print()


def buscarArquivos():
    PASTA_MUSICAS.mkdir(
        parents=True,
        exist_ok=True
    )

    arquivos = []

    for caminho in PASTA_MUSICAS.iterdir():
        if not caminho.is_file():
            continue

        if caminho.suffix.lower() in EXTENSOES_AUDIO:
            arquivos.append(caminho.name)

    arquivos.sort(key=str.lower)

    return arquivos


def mostrarArquivos(arquivos):
    print("ARQUIVOS ENCONTRADOS")
    print("-" * 60)

    for numero, arquivo in enumerate(
        arquivos,
        start=1
    ):
        print(f"{numero}. {arquivo}")

    print("-" * 60)
    print()


def escolherArquivo(arquivos):
    while True:
        escolha = input(
            "ESCOLHA O NUMERO DO ARQUIVO "
            "OU 0 PARA CANCELAR: "
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
        r"\[official music video\]",
        r"\[lyrics\]",
        r"kissvk\.com",
        r"www\."
        r"-corrigido$",
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
    nomeSemExtensao = Path(
        nomeArquivo
    ).stem

    if " - " in nomeSemExtensao:
        partes = nomeSemExtensao.split(
            " - ",
            1
        )

    elif "-" in nomeSemExtensao:
        partes = nomeSemExtensao.split(
            "-",
            1
        )

    else:
        return (
            "DESCONHECIDO",
            limparTitulo(nomeSemExtensao)
        )

    artista = partes[0].strip()
    titulo = limparTitulo(
        partes[1].strip()
    )

    if not artista:
        artista = "DESCONHECIDO"

    if not titulo:
        titulo = nomeSemExtensao

    return artista, titulo


def criarCaminhoRelativo(nomeArquivo):
    caminho = Path("musicas") / nomeArquivo

    return caminho.as_posix()


def criarCaminhoCompleto(caminho):
    caminhoRecebido = Path(caminho)

    if caminhoRecebido.is_absolute():
        return caminhoRecebido

    return PASTA_PROJETO / caminhoRecebido


def obterPrimeiroValor(tags, chave):
    if not tags:
        return ""

    valor = tags.get(chave)

    if not valor:
        return ""

    if isinstance(valor, list):
        valor = valor[0]

    return str(valor).strip()


def lerMetadados(caminho):
    caminhoCompleto = criarCaminhoCompleto(
        caminho
    )

    metadados = {
        "titulo": "",
        "artista": "",
        "album": "",
        "ano": "",
        "duracao": 0
    }

    if not caminhoCompleto.is_file():
        return metadados

    try:
        audio = File(
            str(caminhoCompleto),
            easy=True
        )

        if audio is None:
            return metadados

        metadados["titulo"] = obterPrimeiroValor(
            audio.tags,
            "title"
        )

        metadados["artista"] = obterPrimeiroValor(
            audio.tags,
            "artist"
        )

        metadados["album"] = obterPrimeiroValor(
            audio.tags,
            "album"
        )

        metadados["ano"] = obterPrimeiroValor(
            audio.tags,
            "date"
        )

        if (
            audio.info is not None
            and hasattr(audio.info, "length")
            and audio.info.length
        ):
            metadados["duracao"] = round(
                audio.info.length
            )

    except Exception as erro:
        print()
        print(
            "AVISO: NAO FOI POSSIVEL LER "
            "TODOS OS METADADOS."
        )
        print("DETALHES:", erro)
        print()

    return metadados


def buscarDuracaoComFfprobe(caminho):
    caminhoCompleto = criarCaminhoCompleto(
        caminho
    )

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
                str(caminhoCompleto)
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
        print()

        return 0

    except subprocess.CalledProcessError as erro:
        print()
        print("ERRO AO ANALISAR O ARQUIVO DE AUDIO.")

        mensagem = erro.stderr.strip()

        if mensagem:
            print(mensagem)

        print()

        return 0

    except ValueError:
        print()
        print("A DURACAO RETORNADA PELO FFPROBE")
        print("NAO E VALIDA.")
        print()

        return 0


def buscarDuracao(caminho):
    metadados = lerMetadados(caminho)

    duracao = metadados["duracao"]

    if duracao > 0:
        return duracao

    return buscarDuracaoComFfprobe(caminho)


def mostrarValor(valor):
    if valor:
        return valor

    return "NAO INFORMADO"


def solicitarCampo(nomeCampo, valorSugerido):
    if valorSugerido:
        valorDigitado = input(
            f"{nomeCampo} [{valorSugerido}]: "
        ).strip()

        if valorDigitado:
            return valorDigitado

        return valorSugerido

    return input(
        f"{nomeCampo}: "
    ).strip()


def adicionarMusica():
    mostrarCarregamento()

    arquivos = buscarArquivos()

    if not arquivos:
        print("NENHUM ARQUIVO DE AUDIO FOI ENCONTRADO.")
        print()
        print("COLOQUE AS MUSICAS DENTRO DA PASTA:")
        print(PASTA_MUSICAS)
        print()

        return

    mostrarArquivos(arquivos)

    arquivoEscolhido = escolherArquivo(
        arquivos
    )

    if arquivoEscolhido is None:
        print()
        print("CADASTRO CANCELADO.")
        print()

        return

    caminho = criarCaminhoRelativo(
        arquivoEscolhido
    )

    artistaArquivo, tituloArquivo = separarNome(
        arquivoEscolhido
    )

    print()
    print("LENDO METADADOS DO ARQUIVO...")

    metadados = lerMetadados(caminho)

    tituloSugerido = (
        metadados["titulo"]
        or tituloArquivo
    )

    artistaSugerido = (
        metadados["artista"]
        or artistaArquivo
    )

    albumSugerido = metadados["album"]
    anoSugerido = metadados["ano"]
    duracao = metadados["duracao"]

    print()
    print("INFORMACOES ENCONTRADAS")
    print("-" * 60)
    print(
        "TITULO  :",
        mostrarValor(tituloSugerido)
    )
    print(
        "ARTISTA :",
        mostrarValor(artistaSugerido)
    )
    print(
        "ALBUM   :",
        mostrarValor(albumSugerido)
    )
    print(
        "ANO     :",
        mostrarValor(anoSugerido)
    )

    if duracao > 0:
        print(
            "DURACAO :",
            formatarDuracao(duracao)
        )

    else:
        print("DURACAO : NAO IDENTIFICADA")

    print("-" * 60)
    print()
    print(
        "PRESSIONE ENTER PARA ACEITAR "
        "A INFORMACAO SUGERIDA."
    )
    print()

    titulo = solicitarCampo(
        "TITULO",
        tituloSugerido
    )

    artista = solicitarCampo(
        "ARTISTA",
        artistaSugerido
    )

    album = solicitarCampo(
        "ALBUM",
        albumSugerido
    )

    if not titulo:
        print()
        print("O TITULO NAO PODE FICAR VAZIO.")
        print("CADASTRO CANCELADO.")
        print()

        return

    if not artista:
        artista = "DESCONHECIDO"

    if duracao <= 0:
        print()
        print("ANALISANDO DURACAO DO ARQUIVO...")

        duracao = buscarDuracaoComFfprobe(
            caminho
        )

    if duracao <= 0:
        print()
        print("NAO FOI POSSIVEL IDENTIFICAR")
        print("A DURACAO DA MUSICA.")
        print("A MUSICA NAO FOI CADASTRADA.")
        print()

        return

    print()
    print("RESUMO DO CADASTRO")
    print("-" * 60)
    print("TITULO  :", titulo)
    print("ARTISTA :", artista)
    print(
        "ALBUM   :",
        mostrarValor(album)
    )
    print(
        "ANO     :",
        mostrarValor(anoSugerido)
    )
    print(
        "TEMPO   :",
        formatarDuracao(duracao)
    )
    print(
        "ARQUIVO :",
        caminho
    )
    print("-" * 60)
    print()

    confirmacao = input(
        "CONFIRMAR CADASTRO? [S/N]: "
    ).strip().lower()

    if confirmacao not in [
        "s",
        "sim"
    ]:
        print()
        print("CADASTRO CANCELADO.")
        print()

        return

    cadastrada = cadastrarMusica(
        titulo,
        artista,
        album,
        caminho,
        duracao
    )

    if not cadastrada:
        return

    print()
    print("MUSICA CADASTRADA COM SUCESSO.")
    print("TITULO  :", titulo)
    print("ARTISTA :", artista)
    print(
        "ALBUM   :",
        mostrarValor(album)
    )
    print(
        "TEMPO   :",
        formatarDuracao(duracao)
    )
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
        caminho = musica[4]
        duracao = musica[5]

        caminhoCompleto = criarCaminhoCompleto(
            caminho
        )

        print("ID      :", idMusica)
        print("TITULO  :", titulo)
        print("ARTISTA :", artista)
        print(
            "ALBUM   :",
            mostrarValor(album)
        )
        print(
            "TEMPO   :",
            formatarDuracao(duracao)
        )

        if not caminhoCompleto.is_file():
            print("ARQUIVO : NAO ENCONTRADO")

        print("-" * 60)

    print()


def atualizarBiblioteca():
    musicas = listarMusicas()

    print()
    print("=" * 60)
    print("                 ATUALIZANDO BIBLIOTECA")
    print("=" * 60)
    print()

    if not musicas:
        print("NENHUMA MUSICA CADASTRADA.")
        print()

        return

    atualizadas = 0
    naoEncontradas = 0
    erros = 0

    for musica in musicas:
        idMusica = musica[0]
        titulo = musica[1]
        caminho = musica[4]

        caminhoCompleto = criarCaminhoCompleto(
            caminho
        )

        print(f"ANALISANDO: {titulo}")

        if not caminhoCompleto.is_file():
            print(
                "RESULTADO : ARQUIVO NAO ENCONTRADO"
            )
            print()

            naoEncontradas += 1
            continue

        duracao = buscarDuracao(caminho)

        if duracao <= 0:
            print(
                "RESULTADO : ERRO AO LER DURACAO"
            )
            print()

            erros += 1
            continue

        atualizarDuracao(
            idMusica,
            duracao
        )

        print(
            "RESULTADO :",
            formatarDuracao(duracao)
        )
        print()

        atualizadas += 1

    print("-" * 60)
    print(
        "ATUALIZADAS      :",
        atualizadas
    )
    print(
        "NAO ENCONTRADAS :",
        naoEncontradas
    )
    print(
        "ERROS            :",
        erros
    )
    print()