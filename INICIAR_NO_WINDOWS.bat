@echo off
setlocal
cd /d "%~dp0"
echo ======================================================
echo PORTFOLIO DE ENGENHARIA - DJANGO
 echo ======================================================
if not exist "db.sqlite3" (
  echo.
  echo [AVISO] Banco db.sqlite3 nao esta na pasta.
  echo Copie o arquivo db.sqlite3 entregue em separado para ca.
  echo Se nao houver banco, sera criado um novo banco vazio.
)
if not exist ".venv\Scripts\python.exe" (
  echo.
  echo Criando ambiente virtual Python...
  py -3 -m venv .venv
  if errorlevel 1 (
    echo ERRO: instale Python 3 e habilite o comando py.
    pause
    exit /b 1
  )
)
call ".venv\Scripts\activate.bat"
echo Instalando dependencias...
python -m pip install -r requirements.txt
if errorlevel 1 (
  echo ERRO: nao foi possivel instalar Django. Verifique sua internet.
  pause
  exit /b 1
)
echo Conferindo banco e migracoes...
python manage.py migrate --noinput
if errorlevel 1 (
  echo ERRO ao migrar o banco. Consulte o arquivo README.md.
  pause
  exit /b 1
)
echo Rodando verificacoes...
python manage.py check
if errorlevel 1 (
  echo ERRO: verificacao Django falhou.
  pause
  exit /b 1
)
echo.
echo Site em http://127.0.0.1:8000/
echo Para encerrar: Ctrl+C nesta janela.
start "" "http://127.0.0.1:8000/"
python manage.py runserver
pause
