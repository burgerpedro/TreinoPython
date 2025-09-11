Projeto com Flask API RESTful
Este é um projeto desenvolvido com o framework Flask, que inclui uma API RESTful para interagir com um banco de dados e funcionalidades para gerar relatórios em PDF.

Principais Tecnologias
Backend: Flask, Flask-SQLAlchemy, Flask-RESTful

Banco de Dados: SQLite (embarcado)

Geração de PDF: ReportLab

Documentação da API: Flask-API-Spec

Testes (Opcional): Jupyter Notebook

🚀 Começando
Siga estas instruções para obter uma cópia do projeto em funcionamento na sua máquina local para desenvolvimento e testes.

Pré-requisitos
Certifique-se de que você tenha o Python 3.8+ e o gerenciador de pacotes pip instalados.

Instalação
Clone o repositório (opcional, caso esteja no Git):

git clone https://github.com/burgerpedro/TreinoPython.git
cd TreinoPython


Instale as dependências:
Você pode instalar todas as bibliotecas de uma vez usando o arquivo requirements.txt (método recomendado):

pip install -r requirements.txt

Ou, se preferir, instale-as manualmente:

pip install -U Flask Flask-SQLAlchemy flask-restful sqlalchemy flask-apispec reportlab notebook

⚙️ Como Executar a Aplicação
1. Iniciar a API Flask
Para rodar o servidor da API em modo de desenvolvimento (com recarregamento automático e depurador), execute o comando a partir da raiz do projeto:

flask --app src run --debug

A API estará disponível em http://127.0.0.1:5000.

2. Ponto de Entrada da Interface Gráfica
A interface do programa deve ser iniciada pelo módulo de login, localizado em:

src/gui/login

🗃️ Banco de Dados
Este projeto utiliza SQLite, um banco de dados leve e embarcado que não requer um servidor dedicado. O arquivo do banco de dados (por exemplo, database.db) será criado automaticamente no diretório do projeto na primeira vez que a aplicação for executada.
