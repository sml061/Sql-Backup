Create the Python venv command 

    python -m venv venv

------------------------------

Then enter venv

    source venv/bin/activate

------------------------------

Install the Python dependencies.

    pip install dotenv

------------------------------

Create the .env file in the project's base directory; use the following template for the file.

    DB_HOST='Host. Default: localhost'
    DB_USER='Database user. Default: root'
    DB_PASSWORD='DataBase password'
    DB_NAME='DataBase name'

------------------------------

Schedules the backup task

// Linux

    0 */12 * * * /usr/bin/python3 /home/usuario/backup.py

// Windows
    Use o Agendador de Tarefas.

Configure:

Programa:
python.exe

Argumentos:

C:\backup\backup.py

Gatilho:

Repetir tarefa a cada 12 horas
