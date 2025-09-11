import tkinter as tk
from tkinter import messagebox
import requests

from cadastro_pessoas import tela_cadastro_pessoa
from principal import tela_principal

BASE_URL = "http://127.0.0.1:5000" 

def realizar_login(janela, entry_usuario, entry_senha):
    usuario = entry_usuario.get()
    senha = entry_senha.get()

    if not usuario or not senha:
        messagebox.showwarning("Aviso", "Usuário e senha são obrigatórios!")
        return

    try:
        response = requests.get(f"{BASE_URL}/api/login/{usuario}")
        if response.status_code == 200:
            login_data = response.json()
            if login_data['senha'] == senha:
                usuario_id = login_data['id']
                usuario_nome = login_data['usuario'] 
                messagebox.showinfo("Login", "Login realizado com sucesso!")
                janela.destroy()
                tela_principal(usuario_id,usuario_nome)
            else:
                messagebox.showerror("Erro", "Usuário ou senha incorretos!")
    except Exception as e:
        messagebox.showerror("Erro", f"Ocorreu um erro: {str(e)}")


def cadastrar_usuario(janela, entry_usuario, entry_senha):
    usuario = entry_usuario.get()
    senha = entry_senha.get()

    if not usuario or not senha:
        messagebox.showwarning("Aviso", "Usuário e senha são obrigatórios!")
        return

    try:
        response = requests.post(f"{BASE_URL}/api/login", data={"usuario": usuario, "senha": senha})
        if response.status_code == 201:
            messagebox.showinfo("Cadastro", "Usuário cadastrado com sucesso!")
            janela.destroy()
            tela_cadastro_pessoa(usuario)

        else:
            messagebox.showerror("Erro", f"Erro ao cadastrar usuário: {response.status_code}")
    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao cadastrar usuário: {str(e)}")

janela = tk.Tk()
janela.title("Tela de Login")
janela.geometry("300x180+700+400")
janela.resizable(False, False)

frame = tk.Frame(janela, padx=20, pady=20)
frame.pack()

label_usuario = tk.Label(frame, text="Usuario:")
label_usuario.grid(row=0, column=0, sticky="e", pady=5)

entry_usuario = tk.Entry(frame, width=25)
entry_usuario.grid(row=0, column=1, pady=5)

label_senha = tk.Label(frame, text="Senha:")
label_senha.grid(row=1, column=0, sticky="e", pady=5)

entry_senha = tk.Entry(frame, width=25, show="*")
entry_senha.grid(row=1, column=1, pady=5)

tk.Button(frame, text="Entrar", width=10, command=lambda: realizar_login(janela, entry_usuario, entry_senha)).grid(
    row=2, column=0, pady=10, padx=5
)

tk.Button(frame, text="Cadastrar", width=10,
    command=lambda: cadastrar_usuario(janela, entry_usuario, entry_senha)).grid(row=2, column=1, pady=10, padx=5)

janela.mainloop()
