# Usa uma imagem oficial do Python leve
FROM python:3.13-slim

# Evita que o Python grave arquivos .pyc no disco (economia de espaço)
ENV PYTHONDONTWRITEBYTECODE=1
# Garante que os logs apareçam no terminal sem delay
ENV PYTHONUNBUFFERED=1

# Define a pasta de trabalho dentro do container
WORKDIR /app

# Instala dependências do sistema necessárias para compilar algumas libs
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copia o arquivo de requisitos e instala
COPY requirements.txt /app/
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copia todo o código do projeto para dentro do container
COPY . /app/

# Roda o collectstatic para juntar os arquivos CSS/JS (Whitenoise vai servir)
RUN python manage.py collectstatic --noinput

# Expõe a porta 8000
EXPOSE 8000

# Comando para rodar o servidor em produção (Gunicorn)
CMD ["gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:8000"]