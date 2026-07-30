import os
import sqlite3


PASTA_DADOS = "dados"
CAMINHO_BANCO = os.path.join(
    PASTA_DADOS,
    "musicas.db"
)


def conectarBanco():
    if not os.path.isdir(PASTA_DADOS):
        os.makedirs(PASTA_DADOS)

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
            caminho TEXT NOT NULL UNIQUE,
            duracao INTEGER NOT NULL DEFAULT 0
        )
        """
    )

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
        conexao.close()

        print()
        print("ESSA MUSICA JA ESTA CADASTRADA.")
        print()

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
        ORDER BY titulo
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