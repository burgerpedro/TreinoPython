import tkinter as tk
from tkinter import messagebox, ttk
import requests

BASE_URL = "http://127.0.0.1:5000"  

selected_id = None

def abrir_tela_grupo():

    def listar_grupos():
        for row in tree.get_children():
            tree.delete(row)

        try:
            response = requests.get(f"{BASE_URL}/api/grupo")
            response.raise_for_status()
            grupos = response.json()

            for gp in grupos:
                tree.insert("", "end", values=(gp['id'], gp['nome']))
        except requests.RequestException as e:
            messagebox.showerror("Erro", f"Erro ao listar grupos: {e}")

    def salvar_grupo():
        nome = entry_nome.get()
        if not nome:
            messagebox.showerror("Erro", "O campo Nome não pode estar vazio!")
            return

        data = {"nome": nome}
        try:
            response = requests.post(f"{BASE_URL}/api/grupo", data=data)
            response.raise_for_status()
            grup = response.json()
            tree.insert("", "end", values=(grup['id'], grup['nome']))
            messagebox.showinfo("Sucesso", "Grupo cadastrado com sucesso!")
            entry_nome.delete(0, tk.END)
        except requests.RequestException as e:
            messagebox.showerror("Erro", f"Erro ao salvar grupo: {e}")

    def deletar_grupo():
        global selected_id
        if selected_id is None:
            messagebox.showerror("Erro", "Nenhum grupo selecionado!")
            return

        try:
            response = requests.delete(f"{BASE_URL}/api/grupo/{selected_id}")
            response.raise_for_status()
            listar_grupos() 
            messagebox.showinfo("Sucesso", "Grupo excluído com sucesso!")
            selected_id = None  
        except requests.RequestException as e:
            messagebox.showerror("Erro", f"Erro ao excluir grupo: {e}")

    def selecionar_grupo(event):
        global selected_id
       
        selected_item = tree.focus()
        if selected_item:
            values = tree.item(selected_item, "values")
            selected_id = values[0]  

 
    root = tk.Tk()
    root.title("Cadastro Grupo Muscular")

    
    tk.Label(root, text="Nome:").grid(row=1, column=0, padx=10, pady=5, sticky="e")
    entry_nome = tk.Entry(root)
    entry_nome.grid(row=1, column=1, padx=10, pady=5, sticky="w")

    tree = ttk.Treeview(root, columns=("ID", "Nome"), show="headings", height=8)
    tree.heading("ID", text="ID")
    tree.heading("Nome", text="Nome")
    tree.column("ID", anchor="center", width=200)
    tree.column("Nome", anchor="center", width=200)
    tree.grid(row=5, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")

    tree.bind("<ButtonRelease-1>", selecionar_grupo)

    save_button = tk.Button(root, text="Salvar Grupo", command=salvar_grupo)
    save_button.grid(row=4, column=0, columnspan=1, pady=10)

    delete_button = tk.Button(root, text="Excluir Grupo", command=deletar_grupo)
    delete_button.grid(row=4, column=1, columnspan=1, pady=10)

    root.grid_rowconfigure(5, weight=1)
    root.grid_columnconfigure(0, weight=1)
    root.grid_columnconfigure(1, weight=1)

    listar_grupos()

    root.mainloop()
