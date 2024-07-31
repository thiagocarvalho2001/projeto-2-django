# Verifique se as variáveis de ambiente estão definidas
if (!$env:POSTGRES_HOST -or !$env:POSTGRES_PORT) {
  Write-Host "Erro: Variáveis de ambiente POSTGRES_HOST e/ou POSTGRES_PORT não definidas"
  exit 1
}

# Verifique se o comando nc está disponível
if (!(Get-Command -Name nc -ErrorAction SilentlyContinue)) {
  Write-Host "Erro: Comando nc não encontrado"
  exit 1
}

while (!(Test-Connection -ComputerName $env:POSTGRES_HOST -Port $env:POSTGRES_PORT -Quiet)) {
  Write-Host "🟡 Waiting for Postgres Database Startup ($env:POSTGRES_HOST $env:POSTGRES_PORT) ..."
  Start-Sleep -Milliseconds 100
}

Write-Host "✅ Postgres Database Started Successfully ($env:POSTGRES_HOST:$env:POSTGRES_PORT)"

# Verifique se o comando python está disponível
if (!(Get-Command -Name python -ErrorAction SilentlyContinue)) {
  Write-Host "Erro: Comando python não encontrado"
  exit 1
}


# Run collectstatic, makemigrations, migrate, and runserver
python manage.py collectstatic --noinput
python manage.py makemigrations --noinput
python manage.py migrate --noinput
python manage.py runserver 0.0.0.0:8000

python manage.py collectstatic --noinput
python manage.py makemigrations --noinput
python manage.py migrate --noinput
python manage.py runserver 0.0.0.0:8000