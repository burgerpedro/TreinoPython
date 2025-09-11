import tkinter as tk
from tkinter import messagebox
import requests

from principal import tela_principal


BASE_URL = "http://127.0.0.1:5000"  

def tela_cadastro_pessoa(usuario_nome):
    tela_cadastro_pessoa = tk.Tk()
    tela_cadastro_pessoa.title("Cadastro de Pessoa")
    tela_cadastro_pessoa.geometry("400x350")
    tela_cadastro_pessoa.overrideredirect(True)

    try:
        response = requests.get(f"{BASE_URL}/api/login/{usuario_nome}")
        if response.status_code == 200:
            usuario_id = response.json().get("id")  
            usuario_nome = response.json().get("usuario")
        else:
            messagebox.showerror("Erro", f"Erro ao buscar usuário: {usuario_nome}")
            return
    except Exception as e:
        messagebox.showerror("Erro", f"Ocorreu um erro: {str(e)}")
        return

    def salvar_pessoa():
        nome = entry_nome.get()
        peso = float(entry_peso.get())
        altura = float(entry_altura.get())
        idade = int(entry_idade.get())
        imc = round(peso / (altura ** 2), 2)
        usuario_nome = nome

        if not nome or not peso or not altura or not idade:
            messagebox.showwarning("Aviso", "Todos os campos são obrigatórios!")
            return
        
        try:
            response = requests.post(f"{BASE_URL}/api/pessoa", data={
                "nome": nome,
                "peso": peso,
                "altura": altura,
                "imc": imc,
                "idade": idade,
                "idLogin": usuario_id
            })

            if response.status_code == 201:
                messagebox.showinfo("Sucesso", "Pessoa cadastrada com sucesso!")
                tela_cadastro_pessoa.destroy()
                tela_principal(usuario_id,usuario_nome)

            else:
                messagebox.showerror("Erro", f"Erro ao cadastrar pessoa: {response.status_code}")
        except Exception as e:
            messagebox.showerror("Erro", f"Ocorreu um erro: {str(e)}")

    frame_pessoa = tk.Frame(tela_cadastro_pessoa, padx=20, pady=20)
    frame_pessoa.pack()

    tk.Label(frame_pessoa, text=f"Nome de Usuário: {usuario_nome}").grid(row=0, column=0, columnspan=2, pady=10)

    tk.Label(frame_pessoa, text="Nome (Pessoa):").grid(row=1, column=0, sticky="e", pady=5)
    entry_nome = tk.Entry(frame_pessoa, width=25)
    entry_nome.grid(row=1, column=1, pady=5)

    tk.Label(frame_pessoa, text="Peso (kg):").grid(row=2, column=0, sticky="e", pady=5)
    entry_peso = tk.Entry(frame_pessoa, width=25)
    entry_peso.grid(row=2, column=1, pady=5)

    tk.Label(frame_pessoa, text="Altura (m):").grid(row=3, column=0, sticky="e", pady=5)
    entry_altura = tk.Entry(frame_pessoa, width=25)
    entry_altura.grid(row=3, column=1, pady=5)

    tk.Label(frame_pessoa, text="Idade:").grid(row=4, column=0, sticky="e", pady=5)
    entry_idade = tk.Entry(frame_pessoa, width=25)
    entry_idade.grid(row=4, column=1, pady=5)

    
    tk.Label(frame_pessoa, text=f"ID do Usuário: {usuario_id}").grid(row=5, column=0, columnspan=2, pady=5)


    tk.Button(frame_pessoa, text="Salvar", command=salvar_pessoa).grid(row=6, column=0, columnspan=2, pady=20)

    tela_cadastro_pessoa.mainloop()
