import subprocess
import os
from pathlib import Path
from dotenv import load_dotenv

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

# Configuraçao
MYSQLDUMP = r"/opt/lampp/bin/mysqldump"

HOST = os.getenv("DB_HOST")
USER = os.getenv("DB_USER")
PASSWORD = os.getenv("DB_PASSWORD")
DATABASE = os.getenv("DB_NAME")

BACKUP_DIR = Path("/opt/MySql/backups")
BACKUP_DIR.mkdir(exist_ok=True)

OLD_BACKUP = BACKUP_DIR / "backup_atual.sql"
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


if criar_backup():
    substituir_backup()
    print("Backup realizado com sucesso.")
else:
    if TEMP_BACKUP.exists():
        TEMP_BACKUP.unlink()

    print("Backup falhou. Backup antigo mantido.")