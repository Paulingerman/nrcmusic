import sqlite3
import os


def conectarBanco():
    os.makedirs("dados", exist_ok=True)

    conexao = sqlite3.connect("dados/musicas.db")

    return conexao


def criarBanco():
    conexao = conectarBanco()
    cursor = conexao.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS musicas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            titulo TEXT NOT NULL,
            artista TEXT NOT NULL,
            album TEXT,
            caminho TEXT NOT NULL,
            duracao INTEGER DEFAULT 0
        )
    """)

    conexao.commit()
    conexao.close()


def cadastrarMusica(titulo, artista, album, caminho, duracao):
    conexao = conectarBanco()
    cursor = conexao.cursor()

    cursor.execute("""
        INSERT INTO musicas (
            titulo,
            artista,
            album,
            caminho,
            duracao
        )
        VALUES (?, ?, ?, ?, ?)
    """, (
        titulo,
        artista,
        album,
        caminho,
        duracao
    ))

    conexao.commit()
    conexao.close()


def listarMusicas():
    conexao = conectarBanco()
    cursor = conexao.cursor()

    cursor.execute("""
        SELECT id, titulo, artista, album, caminho, duracao
        FROM musicas
        ORDER BY titulo
    """)

    musicas = cursor.fetchall()

    conexao.close()

    return musicas