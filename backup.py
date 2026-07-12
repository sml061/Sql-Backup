import subprocess
import os
import datetime
import gzip
import shutil
import shutil
from pathlib import Path
from dotenv import load_dotenv

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()
data_hoje = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M")

# Configuraçao

possiveis = [
    shutil.which("mysqldump"),
    "/opt/lampp/bin/mysqldump",
    "/usr/bin/mysqldump",
    "/usr/local/bin/mysqldump",
]

MYSQLDUMP = next((p for p in possiveis if p and os.path.exists(p)), None)

if MYSQLDUMP is None:
    raise FileNotFoundError(
        "mysqldump não encontrado. Instale MySQL/MariaDB ou configure o caminho."
    )


HOST = os.getenv("DB_HOST")
USER = os.getenv("DB_USER")
PASSWORD = os.getenv("DB_PASSWORD")
DATABASE = os.getenv("DB_NAME")
DIR = os.getcwd()

BACKUP_DIR = Path(f"{DIR}/backups")
BACKUP_DIR.mkdir(exist_ok=True)

OLD_BACKUP = BACKUP_DIR / f"backup_{data_hoje}.sql"
TEMP_BACKUP = BACKUP_DIR / "backup_temp.sql"

def criar_backup():

    if PASSWORD == '':
        comando = [MYSQLDUMP, "-h", HOST, "-u", USER, DATABASE]
    else:
        comando = [MYSQLDUMP, "-h", HOST, "-u", USER, f"-p{PASSWORD}", DATABASE]

    with open(TEMP_BACKUP, "w", encoding="utf8") as arquivo:

        resultado = subprocess.run(
            comando,
            stdout=arquivo,
            stderr=subprocess.PIPE,
            text=True
        )

    if resultado.returncode != 0:
        print("Erro no backup:")
        print(resultado.stderr)
        return False

    if not TEMP_BACKUP.exists():
        return False

    if TEMP_BACKUP.stat().st_size < 100:
        return False

    return True


def substituir_backup():

    if OLD_BACKUP.exists():
        OLD_BACKUP.unlink()

    TEMP_BACKUP.rename(OLD_BACKUP)

def compactar_backup():
    with open(OLD_BACKUP, "rb") as arquivo:
        with open(f"{OLD_BACKUP}.gz", "wb") as arquivo_compactado:
            subprocess.run(["gzip"], stdin=arquivo, stdout=arquivo_compactado)

def criar_log(mensagem):
    log_file = "backup.log"
    with open(log_file, "a") as log:
        log.write(f"{datetime.datetime.now()}: {mensagem}\n")


if criar_backup():
    print("Backup realizado com sucesso.")
    try:
        substituir_backup()
        compactar_backup()
        criar_log(f"Backup criado e compactado: {OLD_BACKUP}.gz")
        os.remove(OLD_BACKUP)
    except Exception as e:
        print(f"Erro ao compactar o backup: {e}")
        criar_log(f"Erro ao compactar o backup: {e}")
else:
    if TEMP_BACKUP.exists():
        TEMP_BACKUP.unlink()

    print("Backup falhou. Backup antigo mantido.")
    criar_log("Backup falhou. Backup antigo mantido.")