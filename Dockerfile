# Imagem base
FROM python:3.11.3-alpine3.18

# Informações do mantenedor
LABEL manteiner="tcarva94@gmail.com"

# Configurações do Python
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Cópia de arquivos
COPY ./site-legal ./site-legal
COPY ./scripts /scripts

# Definição do diretório de trabalho
WORKDIR /site-legal

# Exposição da porta
EXPOSE 8000

# Instalação de dependências
RUN python -m venv /venv && \
  /venv/bin/pip install --upgrade pip && \
  /venv/bin/pip install -r /site-legal/requirements.txt

# Instalação do PowerShell
RUN apk update && apk add --no-cache powershell
#...

# Criação de usuário e permissões
RUN adduser --disabled-password --no-create-home duser && \
  mkdir -p /data/web/static && \
  mkdir -p /data/web/media && \
  chown -R duser:duser /venv && \
  chown -R duser:duser /data/web/static && \
  chown -R duser:duser /data/web/media && \
  chmod -R 755 /data/web/static && \
  chmod -R 755 /data/web/media && \
  chmod -R +x /scripts

# Configuração do PATH
ENV PATH="/scripts:/venv/bin:$PATH"

# Configuração do PATH para o PowerShell
ENV PATH=$PATH:/usr/bin/pwsh

# Troca de usuário
USER duser

# Comando de execução
CMD ["pwsh", "-Command", "commands.ps1"]