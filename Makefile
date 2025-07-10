# Makefile para o Sistema de Predição de Criptomoedas
# Nota: Este Makefile é otimizado para ambientes Unix (Linux/macOS).
# Para Windows, os comandos podem precisar ser executados manualmente no PowerShell ou CMD.

# --- Variáveis ---
PYTHON = venv/bin/python
STREAMLIT = venv/bin/streamlit

# --- Alvos Principais ---
all: install

.PHONY: all install freeze run clean help venv

# Comando de ajuda para listar os alvos disponíveis.
help:
	@echo "Comandos disponíveis:"
	@echo "  make help       - Mostra esta mensagem de ajuda."
	@echo "  make venv       - Cria o ambiente virtual 'venv'."
	@echo "  make install    - Instala as dependências do projeto a partir de requirements.txt."
	@echo "  make freeze     - Faz upload das dependências para dentro do arquivo requirements.txt"
	@echo "  make run        - Executa a aplicação Streamlit."
	@echo "  make clean      - Remove arquivos temporários do Python (.pyc, __pycache__)."

# Cria o ambiente virtual.
venv:
	@echo "-> Criando ambiente virtual Python na pasta 'venv'..."
	python3 -m venv venv

# Instala as dependências. Depende do alvo 'venv' para garantir que o ambiente exista.
install: venv
	@echo "-> Instalando dependências do projeto..."
	$(PYTHON) -m pip install --upgrade pip
	$(PYTHON) -m pip install -r requirements.txt
	@echo "-> Instalação concluída com sucesso."

# Faz upload das dependências para dentro do arquivo requirements.txt
freeze:
	@echo "-> Fazendo upload das dependências do projeto..."
	$(PYTHON) freeze > requirements.txt 
	@echo "-> Upload concluído com sucesso."

# Executa a aplicação Streamlit.
run:
	@echo "-> Iniciando a aplicação Streamlit..."
	@echo "Acesse o endereço fornecido no seu navegador."
	$(STREAMLIT) run app.py

# Limpa o projeto de arquivos temporários.
clean:
	@echo "-> Limpando arquivos temporários..."
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -exec rm -rf {} +
	@echo "-> Limpeza concluída."

