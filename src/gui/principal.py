import tkinter as tk
from ver_treino import abrir_tela_treino
from ver_exercicio import abrir_tela_exercicio
from ver_grupo import abrir_tela_grupo
from ver_pessoa import abrir_tela_pessoa
import requests
from tkinter import messagebox

BASE_URL = "http://127.0.0.1:5000"  

pessoa_id = None

def obter_pessoa_id(usuario_id):
    global pessoa_id
    try:
        response = requests.get(f"{BASE_URL}/api/pessoa/login/{usuario_id}")
        if response.status_code == 200:
            pessoa = response.json()
            pessoa_id = pessoa.get("id") 
        else:
            messagebox.showerror("Erro", f"Erro ao buscar dados da pessoa: {usuario_id}")
            pessoa_id = None
    except Exception as e:
        messagebox.showerror("Erro", f"Ocorreu um erro: {str(e)}")
        pessoa_id = None

def ver_pessoa(usuario_id):
        abrir_tela_pessoa(usuario_id)

def ver_treino():
        abrir_tela_treino(pessoa_id)

def ver_exercicio():
    abrir_tela_exercicio()

def ver_grupo_muscular():
    abrir_tela_grupo()

def tela_principal(usuario_id, usuario_nome):
   
    global pessoa_id
    
    obter_pessoa_id(usuario_id)

    if not pessoa_id:
        
        return

    tela_principal = tk.Tk()
    tela_principal.title("Página Principal")
    tela_principal.geometry("500x400+700+400")

    tk.Label(tela_principal, text=f"Bem-vindo! {usuario_nome}", font=("Arial", 12)).pack(pady=20)

    frame_botoes = tk.Frame(tela_principal)
    frame_botoes.pack(pady=20)

    btn_pessoa = tk.Button(frame_botoes, text="Ver Pessoa", command=lambda:ver_pessoa(usuario_id), width=20)
    btn_pessoa.grid(row=0, column=0, padx=10, pady=10)

    btn_treino = tk.Button(frame_botoes, text="Ver Treino", command=ver_treino, width=20)
    btn_treino.grid(row=0, column=1, padx=10, pady=10)

    btn_exercicio = tk.Button(frame_botoes, text="Ver Exercício", command=ver_exercicio, width=20)
    btn_exercicio.grid(row=1, column=0, padx=10, pady=10)

    btn_grupo_muscular = tk.Button(frame_botoes, text="Ver Grupo Muscular", command=ver_grupo_muscular, width=20)
    btn_grupo_muscular.grid(row=1, column=1, padx=10, pady=10)

    tk.Button(tela_principal, text="Sair", command=tela_principal.destroy, width=20, bg="red", fg="white").pack(pady=20)

    tela_principal.mainloop()
