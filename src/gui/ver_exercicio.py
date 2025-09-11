import tkinter as tk
from tkinter import ttk, messagebox
import requests
import webbrowser  # Para abrir links no navegador

BASE_URL = "http://127.0.0.1:5000" 


def abrir_tela_exercicio():
    tela_exercicio = tk.Tk()
    tela_exercicio.title("Visualizar/Editar Exercício")
    tela_exercicio.geometry("700x500")
    tela_exercicio.overrideredirect(False)  

   
    selected_id = None
    grupos_musculares = {}  

    
    def carregar_grupos_musculares():
        try:
            response = requests.get(f"{BASE_URL}/api/grupo")
            if response.status_code == 200:
                data = response.json()
                for grupo in data:
                    grupos_musculares[grupo['id']] = grupo['nome']
                    combobox_grupo['values'] = list(grupos_musculares.values())
            else:
                messagebox.showerror("Erro", "Erro ao listar grupos musculares!")
        except Exception as e:
            messagebox.showerror("Erro", f"Ocorreu um erro ao carregar grupos musculares: {str(e)}")

    # Função para listar exercícios
    def listar_exercicios():
        for row in tree.get_children():
            tree.delete(row)
        try:
            response = requests.get(f"{BASE_URL}/api/exercicio")
            if response.status_code == 200:
                exercicios = response.json()
                for ex in exercicios:
                    grupo_nome = grupos_musculares.get(ex['idGrupoMuscular'], "Desconhecido")
                    tree.insert("", "end", values=(ex['id'], ex['nome'], ex['video'], grupo_nome))
            else:
                messagebox.showerror("Erro", "Erro ao listar exercícios!")
        except Exception as e:
            messagebox.showerror("Erro", f"Ocorreu um erro: {str(e)}")

    def salvar_exercicio():
        nome = entry_nome.get()
        video = entry_video.get()
        grupo_nome = combobox_grupo.get()

        if not nome or not video or not grupo_nome:
            messagebox.showwarning("Aviso", "Todos os campos são obrigatórios!")
            return

        grupo_muscular_id = [k for k, v in grupos_musculares.items() if v == grupo_nome]
        if not grupo_muscular_id:
            messagebox.showerror("Erro", "Grupo muscular inválido!")
            return

        data = {"nome": nome, "video": video, "idGrupoMuscular": grupo_muscular_id[0]}

        try:
            response = requests.post(f"{BASE_URL}/api/exercicio", data=data)
            if response.status_code == 201:
                messagebox.showinfo("Sucesso", "Exercício cadastrado com sucesso!")
                listar_exercicios()
                entry_nome.delete(0, tk.END)
                entry_video.delete(0, tk.END)
                combobox_grupo.set("")
            else:
                messagebox.showerror("Erro", "Erro ao salvar exercício!")
        except Exception as e:
            messagebox.showerror("Erro", f"Ocorreu um erro: {str(e)}")

    def selecionar_exercicio(event):
        nonlocal selected_id
        selected_item = tree.focus()
        if selected_item:
            values = tree.item(selected_item, "values")
            selected_id = values[0]
            entry_nome.delete(0, tk.END)
            entry_nome.insert(0, values[1])
            entry_video.delete(0, tk.END)
            entry_video.insert(0, values[2])
            combobox_grupo.set(values[3])

    def atualizar_exercicio():
        nonlocal selected_id
        if not selected_id:
            messagebox.showerror("Erro", "Nenhum exercício selecionado!")
            return

        nome = entry_nome.get()
        video = entry_video.get()
        grupo_nome = combobox_grupo.get()

        if not nome or not video or not grupo_nome:
            messagebox.showwarning("Aviso", "Todos os campos são obrigatórios!")
            return

        grupo_muscular_id = [k for k, v in grupos_musculares.items() if v == grupo_nome]
        if not grupo_muscular_id:
            messagebox.showerror("Erro", "Grupo muscular inválido!")
            return

        data = {"nome": nome, "video": video, "idGrupoMuscular": grupo_muscular_id[0]}

        try:
            response = requests.put(f"{BASE_URL}/api/exercicio/{selected_id}", data=data)
            if response.status_code == 200:
                messagebox.showinfo("Sucesso", "Exercício atualizado com sucesso!")
                listar_exercicios()
                selected_id = None
            else:
                messagebox.showerror("Erro", "Erro ao atualizar exercício!")
        except Exception as e:
            messagebox.showerror("Erro", f"Ocorreu um erro: {str(e)}")

    def deletar_exercicio():
        nonlocal selected_id
        if not selected_id:
            messagebox.showerror("Erro", "Nenhum exercício selecionado!")
            return

        try:
            response = requests.delete(f"{BASE_URL}/api/exercicio/{selected_id}")
            if response.status_code == 204:
                messagebox.showinfo("Sucesso", "Exercício excluído com sucesso!")
                listar_exercicios()
                selected_id = None
            else:
                messagebox.showerror("Erro", "Erro ao excluir exercício!")
        except Exception as e:
            messagebox.showerror("Erro", f"Ocorreu um erro: {str(e)}")

    def abrir_video(event):
        selected_item = tree.focus()
        if selected_item:
            values = tree.item(selected_item, "values")
            video_url = values[2] 
            if video_url:
                webbrowser.open(video_url) 

    frame_exercicio = tk.Frame(tela_exercicio, padx=10, pady=10)
    frame_exercicio.pack()

    tk.Label(frame_exercicio, text="Nome:").grid(row=0, column=0, sticky="e", pady=5)
    entry_nome = tk.Entry(frame_exercicio, width=30)
    entry_nome.grid(row=0, column=1, pady=5)

    tk.Label(frame_exercicio, text="Vídeo (Link):").grid(row=1, column=0, sticky="e", pady=5)
    entry_video = tk.Entry(frame_exercicio, width=30)
    entry_video.grid(row=1, column=1, pady=5)

    tk.Label(frame_exercicio, text="Grupo Muscular:").grid(row=2, column=0, sticky="e", pady=5)
    combobox_grupo = ttk.Combobox(frame_exercicio, width=28, state="readonly")
    combobox_grupo.grid(row=2, column=1, pady=5)

    tree = ttk.Treeview(frame_exercicio, columns=("ID", "Nome", "Vídeo", "Grupo Muscular"), show="headings", height=8)
    tree.heading("ID", text="ID")
    tree.heading("Nome", text="Nome")
    tree.heading("Vídeo", text="Vídeo")
    tree.heading("Grupo Muscular", text="Grupo Muscular")
    tree.column("ID", anchor="center", width=50)
    tree.column("Nome", anchor="center", width=150)
    tree.column("Vídeo", anchor="center", width=200)
    tree.column("Grupo Muscular", anchor="center", width=100)
    tree.grid(row=3, column=0, columnspan=3, pady=10, sticky="nsew")

    tree.bind("<ButtonRelease-1>", selecionar_exercicio)
    tree.bind("<Double-1>", abrir_video) 

    tk.Button(frame_exercicio, text="Salvar", command=salvar_exercicio).grid(row=4, column=0, pady=10)
    tk.Button(frame_exercicio, text="Atualizar", command=atualizar_exercicio).grid(row=4, column=1, pady=10)
    tk.Button(frame_exercicio, text="Excluir", command=deletar_exercicio).grid(row=4, column=2, pady=10)

    carregar_grupos_musculares()
    listar_exercicios()

    tela_exercicio.mainloop()
