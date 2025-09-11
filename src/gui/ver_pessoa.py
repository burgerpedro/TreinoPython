import tkinter as tk
from tkinter import messagebox
import requests

BASE_URL = "http://127.0.0.1:5000"  

pessoa_id = None

def abrir_tela_pessoa(usuario_id):
    global pessoa_id  
    tela_pessoa = tk.Tk()
    tela_pessoa.title("Visualizar/Editar Pessoa")
    tela_pessoa.geometry("400x400")
    tela_pessoa.overrideredirect(False) 

    def preencher_dados_pessoa():
        global pessoa_id
        try:
            response = requests.get(f"{BASE_URL}/api/pessoa/login/{usuario_id}")
            if response.status_code == 200:
                pessoa = response.json()
                pessoa_id = pessoa.get("id") 
    
                entry_nome.insert(0, pessoa.get("nome", ""))
                entry_peso.insert(0, pessoa.get("peso", ""))
                entry_altura.insert(0, pessoa.get("altura", ""))
                entry_idade.insert(0, pessoa.get("idade", ""))
            else:
                messagebox.showerror("Erro", f"Erro ao buscar dados da pessoa: {usuario_id}")
        except Exception as e:
            messagebox.showerror("Erro", f"Ocorreu um erro: {str(e)}")

    def atualizar_pessoa():
        global pessoa_id

        if not pessoa_id:
            messagebox.showerror("Erro", "ID da pessoa não encontrado!")
            return

        nome = entry_nome.get()
        peso = entry_peso.get()
        altura = entry_altura.get()
        idade = entry_idade.get()

        if not nome or not peso or not altura or not idade:
            messagebox.showwarning("Aviso", "Todos os campos são obrigatórios!")
            return

        try:
            peso = float(peso)
            altura = float(altura)
            idade = int(idade)
            imc = round(peso / (altura ** 2), 2)
        except ValueError:
            messagebox.showerror("Erro", "Peso, altura e idade devem ser números!")
            return

        try:
            response = requests.put(f"{BASE_URL}/api/pessoa/{pessoa_id}", data={
                "nome": nome,
                "peso": peso,
                "altura": altura,
                "imc": imc,
                "idade": idade,
                "idLogin": usuario_id
            })

            if response.status_code == 200:
                messagebox.showinfo("Sucesso", "Dados atualizados com sucesso!")
                tela_pessoa.destroy()
            else:
                messagebox.showerror("Erro", f"Erro ao atualizar pessoa: {response.status_code}")
        except Exception as e:
            messagebox.showerror("Erro", f"Ocorreu um erro: {str(e)}")

    frame_pessoa = tk.Frame(tela_pessoa, padx=20, pady=20)
    frame_pessoa.pack()

    tk.Label(frame_pessoa, text="Nome:").grid(row=1, column=0, sticky="e", pady=5)
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

    tk.Button(frame_pessoa, text="Atualizar", command=atualizar_pessoa).grid(row=5, column=0, columnspan=2, pady=20)
    tk.Button(frame_pessoa, text="Fechar", command=tela_pessoa.destroy).grid(row=6, column=0, columnspan=2, pady=10)

    preencher_dados_pessoa()

    tela_pessoa.mainloop()
