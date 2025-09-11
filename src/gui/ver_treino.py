import tkinter as tk
from tkinter import ttk, messagebox
import requests
import webbrowser
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter

BASE_URL = "http://127.0.0.1:5000"  


def abrir_tela_treino(usuario_id):
    tela_treino = tk.Tk()
    tela_treino.title("Treinos do Usuário")
    tela_treino.geometry("1000x600")
    tela_treino.overrideredirect(False)

    exercicios = {} 
    treinos = []  
    dados_pessoa = {}

    def preencher_dados_pessoa():
        nonlocal dados_pessoa
        try:
            response = requests.get(f"{BASE_URL}/api/pessoa/login/{usuario_id}")
            if response.status_code == 200:
                dados_pessoa = response.json()
            else:
                messagebox.showerror("Erro", f"Erro ao buscar dados da pessoa: {usuario_id}")
        except Exception as e:
            messagebox.showerror("Erro", f"Ocorreu um erro: {str(e)}")

    def carregar_exercicios():
        try:
            response = requests.get(f"{BASE_URL}/api/exercicio")
            if response.status_code == 200:
                data = response.json()
                for exercicio in data:
                    exercicios[exercicio['id']] = exercicio['nome']
                    combobox_exercicio['values'] = list(exercicios.values())
            else:
                messagebox.showerror("Erro", "Erro ao listar exercícios!")
        except Exception as e:
            messagebox.showerror("Erro", f"Ocorreu um erro ao carregar exercícios: {e}")

    def listar_treinos():
        nonlocal treinos
        for row in tree.get_children():
            tree.delete(row)
        try:
            response = requests.get(f"{BASE_URL}/api/treino/pessoa/{usuario_id}")
            if response.status_code == 200:
                treinos = response.json()
                for treino in treinos:
                    exercicio_nome = treino['exercicio']['nome'] if treino.get('exercicio') else "Desconhecido"
                    exercicio_video = treino['exercicio']['video'] if treino.get('exercicio') else "Sem vídeo"
                    tree.insert("", "end", values=(
                        treino['id'],
                        treino['nome'],
                        treino['serie'],
                        treino['repeticao'],
                        exercicio_nome,
                        exercicio_video
                    ))
            else:
                messagebox.showerror("Erro", "Erro ao listar treinos!")
        except Exception as e:
            messagebox.showerror("Erro", f"Ocorreu um erro: {e}")

    def salvar_treino():
        nome = entry_nome.get()
        repeticao = entry_repeticao.get()
        serie = entry_serie.get()
        exercicio_nome = combobox_exercicio.get()

        if not nome or not repeticao or not serie or not exercicio_nome:
            messagebox.showwarning("Aviso", "Todos os campos são obrigatórios!")
            return

        exercicio_id = [k for k, v in exercicios.items() if v == exercicio_nome]
        if not exercicio_id:
            messagebox.showerror("Erro", "Exercício inválido!")
            return

        data = {
            "nome": nome,
            "repeticao": int(repeticao),
            "serie": int(serie),
            "idPessoa": usuario_id,
            "idExercicio": exercicio_id[0]
        }

        try:
            response = requests.post(f"{BASE_URL}/api/treino", data=data)
            if response.status_code == 201:
                messagebox.showinfo("Sucesso", "Treino cadastrado com sucesso!")
                listar_treinos()
                entry_nome.delete(0, tk.END)
                entry_repeticao.delete(0, tk.END)
                entry_serie.delete(0, tk.END)
                combobox_exercicio.set("")
            else:
                messagebox.showerror("Erro", "Erro ao salvar treino!")
        except Exception as e:
            messagebox.showerror("Erro", f"Ocorreu um erro: {(e)}")

    def atualizar_treino():
        nonlocal selected_id
        if not selected_id:
            messagebox.showerror("Erro", "Nenhum treino selecionado!")
            return

        nome = entry_nome.get()
        repeticao = entry_repeticao.get()
        serie = entry_serie.get()
        exercicio_nome = combobox_exercicio.get()

        if not nome or not repeticao or not serie or not exercicio_nome:
            messagebox.showwarning("Aviso", "Todos os campos são obrigatórios!")
            return

        exercicio_id = [k for k, v in exercicios.items() if v == exercicio_nome]
        if not exercicio_id:
            messagebox.showerror("Erro", "Exercício inválido!")
            return

        data = {
            "nome": nome,
            "repeticao": int(repeticao),
            "serie": int(serie),
            "idPessoa": usuario_id,
            "idExercicio": exercicio_id[0]
        }

        try:
            response = requests.put(f"{BASE_URL}/api/treino/{selected_id}", data=data)
            if response.status_code == 200:
                messagebox.showinfo("Sucesso", "Treino atualizado com sucesso!")
                listar_treinos()
                selected_id = None
            else:
                messagebox.showerror("Erro", "Erro ao atualizar treino!")
        except Exception as e:
            messagebox.showerror("Erro", f"Ocorreu um erro: {(e)}")

    def deletar_treino():
        nonlocal selected_id
        if not selected_id:
            messagebox.showerror("Erro", "Nenhum treino selecionado!")
            return

        try:
            response = requests.delete(f"{BASE_URL}/api/treino/{selected_id}")
            if response.status_code == 204:
                messagebox.showinfo("Sucesso", "Treino excluído com sucesso!")
                listar_treinos()
                selected_id = None
            else:
                messagebox.showerror("Erro", "Erro ao excluir treino!")
        except Exception as e:
            messagebox.showerror("Erro", f"Ocorreu um erro: {(e)}")
    
    def gerar_pdf():
        if not treinos:
            messagebox.showwarning("Aviso", "Não há treinos para gerar o PDF.")
            return

        arquivo_pdf = "treinos_usuario.pdf"

        try:
            c = canvas.Canvas(arquivo_pdf, pagesize=letter)
            largura, altura = letter

            c.setFont("Helvetica-Bold", 16)
            c.drawString(50, altura - 50, "Relatório de Treinos")
            c.setFont("Helvetica", 12)
            c.drawString(50, altura - 80, f"Matricula: {usuario_id}")
            
            linha_y = altura - 120  
            c.setFont("Helvetica-Bold", 14)
            c.drawString(50, linha_y, "Dados da Pessoa:")
            c.setFont("Helvetica", 12)
            linha_y -= 20
            c.drawString(50, linha_y, f"Nome: {dados_pessoa.get('nome')}")
            linha_y -= 20
            c.drawString(50, linha_y, f"Peso: {dados_pessoa.get('peso')}")
            linha_y -= 20
            c.drawString(50, linha_y, f"Altura: {dados_pessoa.get('altura')}")
            linha_y -= 20
            c.drawString(50, linha_y, f"Idade: {dados_pessoa.get('idade')}")

            linha_y -= 30
            c.setFont("Helvetica-Bold", 14)
            c.drawString(50, linha_y, f"IMC: {dados_pessoa.get('imc', 'Não informado')}")
            
            imc = dados_pessoa.get('imc', None)
            if imc:
                imc = float(imc)
                if imc < 18.5:
                    grau = "Abaixo do peso"
                elif 18.5 <= imc < 24.9:
                    grau = "Peso normal"
                elif 25.0 <= imc < 29.9:
                    grau = "Sobrepeso"
                elif 30.0 <= imc < 34.9:
                    grau = "Obesidade Grau 1"
                elif 35.0 <= imc < 39.9:
                    grau = "Obesidade Grau 2"
                else:
                    grau = "Obesidade Grau 3"
            else:
                grau = "IMC não informado"

            linha_y -= 20
            c.setFont("Helvetica", 12)
            c.drawString(50, linha_y, f"Grau de Obesidade: {grau}")

            linha_y -= 30
            c.line(50, linha_y, largura - 50, linha_y) 
            linha_y -= 20

            c.setFont("Helvetica-Bold", 12)
            c.drawString(50, linha_y, "Nome")
            c.drawString(200, linha_y, "Exercício")
            c.drawString(400, linha_y, "Repetições")
            c.drawString(500, linha_y, "Séries")
            linha_y -= 20

           
            c.setFont("Helvetica", 12)
            for treino in treinos:
                if linha_y < 50: 
                    c.showPage()  
                    linha_y = altura - 50 
                    c.setFont("Helvetica-Bold", 12)
                    c.drawString(50, linha_y, "Nome")
                    c.drawString(200, linha_y, "Exercício")
                    c.drawString(400, linha_y, "Repetições")
                    c.drawString(500, linha_y, "Séries")
                    linha_y -= 20
                    c.setFont("Helvetica", 12)

                c.drawString(50, linha_y, treino['nome'] if treino.get('nome') else "Desconhecido")
                c.drawString(200, linha_y, treino['exercicio']['nome'] if treino.get('exercicio') else "Desconhecido")
                c.drawString(400, linha_y, str(treino['repeticao']))
                c.drawString(500, linha_y, str(treino['serie']))
                linha_y -= 20

            c.save()
            messagebox.showinfo("Sucesso", f"PDF gerado com sucesso: {arquivo_pdf}")
        except Exception as e:
            messagebox.showerror("Erro", f"Ocorreu um erro ao gerar o PDF: {str(e)}")

    frame_treino = tk.Frame(tela_treino, padx=10, pady=10)
    frame_treino.pack()

    tk.Label(frame_treino, text="Nome:").grid(row=0, column=0, sticky="e", pady=5)
    entry_nome = tk.Entry(frame_treino, width=30)
    entry_nome.grid(row=0, column=1, pady=5)

    tk.Label(frame_treino, text="Série:").grid(row=1, column=0, sticky="e", pady=5)
    entry_serie = tk.Entry(frame_treino, width=30)
    entry_serie.grid(row=1, column=1, pady=5)

    tk.Label(frame_treino, text="Repetição:").grid(row=2, column=0, sticky="e", pady=5)
    entry_repeticao = tk.Entry(frame_treino, width=30)
    entry_repeticao.grid(row=2, column=1, pady=5)

    tk.Label(frame_treino, text="Exercício:").grid(row=3, column=0, sticky="e", pady=5)
    combobox_exercicio = ttk.Combobox(frame_treino, width=28, state="readonly")
    combobox_exercicio.grid(row=3, column=1, pady=5)

    tree = ttk.Treeview(
        frame_treino,
        columns=("ID", "Nome", "Série", "Repetição", "Exercício", "Vídeo"),
        show="headings",
        height=8
    )
    tree.heading("ID", text="ID")
    tree.heading("Nome", text="Nome")
    tree.heading("Série", text="Série")
    tree.heading("Repetição", text="Repetição")
    tree.heading("Exercício", text="Exercício")
    tree.heading("Vídeo", text="Vídeo")
    tree.grid(row=4, column=0, columnspan=3, pady=10, sticky="nsew")

    selected_id = None

    def selecionar_item(event):
        nonlocal selected_id
        for item in tree.selection():
            selected_id = tree.item(item, "values")[0]

    tree.bind("<<TreeviewSelect>>", selecionar_item)

    frame_botoes = tk.Frame(frame_treino)
    frame_botoes.grid(row=5, column=0, columnspan=3, pady=10)

    tk.Button(frame_botoes, text="Adicionar", command=salvar_treino, width=15).pack(side=tk.LEFT, padx=10)
    tk.Button(frame_botoes, text="Atualizar", command=atualizar_treino, width=15).pack(side=tk.LEFT, padx=10)
    tk.Button(frame_botoes, text="Deletar", command=deletar_treino, width=15).pack(side=tk.LEFT, padx=10)
    tk.Button(frame_botoes, text="Gerar PDF", command=gerar_pdf, width=15).pack(side=tk.LEFT, padx=10)

    carregar_exercicios()
    listar_treinos()
    preencher_dados_pessoa()

    tela_treino.mainloop()
