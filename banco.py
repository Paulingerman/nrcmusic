import sqlite3
from pathlib import Path


PASTA_PROJETO = Path(__file__).resolve().parent
PASTA_DADOS = PASTA_PROJETO / "dados"
CAMINHO_BANCO = PASTA_DADOS / "musicas.db"


def conectarBanco():
    PASTA_DADOS.mkdir(parents=True, exist_ok=True)

    conexao = sqlite3.connect(CAMINHO_BANCO)

    return conexao


def criarBanco():
    conexao = conectarBanco()
    cursor = conexao.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS musicas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            titulo TEXT NOT NULL,
            artista TEXT NOT NULL,
            album TEXT,
            caminho TEXT NOT NULL,
            duracao INTEGER NOT NULL DEFAULT 0
        )
        """
    )

    try:
        cursor.execute(
            """
            CREATE UNIQUE INDEX IF NOT EXISTS
            indiceCaminhoMusica
            ON musicas(caminho)
            """
        )

    except sqlite3.IntegrityError:
        print()
        print("AVISO: EXISTEM CAMINHOS DUPLICADOS NO BANCO.")
        print("O INDICE DE CAMINHO NAO FOI CRIADO.")
        print()

    conexao.commit()
    conexao.close()


def cadastrarMusica(
    titulo,
    artista,
    album,
    caminho,
    duracao
):
    conexao = conectarBanco()
    cursor = conexao.cursor()

    try:
        cursor.execute(
            """
            INSERT INTO musicas (
                titulo,
                artista,
                album,
                caminho,
                duracao
            )
            VALUES (?, ?, ?, ?, ?)
            """,
            (
                titulo,
                artista,
                album,
                caminho,
                duracao
            )
        )

        conexao.commit()

    except sqlite3.IntegrityError:
        print()
        print("ESSA MUSICA JA ESTA CADASTRADA.")
        print()

        conexao.close()

        return False

    conexao.close()

    return True


def listarMusicas():
    conexao = conectarBanco()
    cursor = conexao.cursor()

    cursor.execute(
        """
        SELECT id, titulo, artista, album, caminho, duracao
        FROM musicas
        ORDER BY artista, titulo
        """
    )

    musicas = cursor.fetchall()

    conexao.close()

    return musicas


def buscarMusica(idMusica):
    conexao = conectarBanco()
    cursor = conexao.cursor()

    cursor.execute(
        """
        SELECT id, titulo, artista, album, caminho, duracao
        FROM musicas
        WHERE id = ?
        """,
        (idMusica,)
    )

    musica = cursor.fetchone()

    conexao.close()

    return musica


def atualizarDuracao(idMusica, duracao):
    conexao = conectarBanco()
    cursor = conexao.cursor()

    cursor.execute(
        """
        UPDATE musicas
        SET duracao = ?
        WHERE id = ?
        """,
        (
            duracao,
            idMusica
        )
    )

    conexao.commit()
    conexao.close()


def atualizarCaminho(idMusica, caminho):
    conexao = conectarBanco()
    cursor = conexao.cursor()

    try:
        cursor.execute(
            """
            UPDATE musicas
            SET caminho = ?
            WHERE id = ?
            """,
            (
                caminho,
                idMusica
            )
        )

        conexao.commit()

    except sqlite3.IntegrityError:
        conexao.close()

        return False

    conexao.close()

    return True


def removerMusica(idMusica):
    conexao = conectarBanco()
    cursor = conexao.cursor()

    cursor.execute(
        """
        DELETE FROM musicas
        WHERE id = ?
        """,
        (idMusica,)
    )

    removida = cursor.rowcount > 0

    conexao.commit()
    conexao.close()

    return removida