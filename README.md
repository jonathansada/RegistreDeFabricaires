# Description
This is an application for collecting information about the users who visits [EspluLab](https://www.esplugues.cat/es/esplulab/) and get information about the usage of the the machines and material. 

# App details
This was meant to be executed on local network inside EspluLab and is *not ready to be exposed on the internet*.
This was done as an opportunity to practice with SQLAlchemy and Flask as the same time I provided an easy way to collect the information needed through any machine in the local network.

# Set-up App
This is expected to be using Conda (throough micro-forge)

## 1. Prepare the environment
Install the conda environment
``` bash
conda env create --name RegFab --file base_env.yml
```

Install pip requirements
```bash
pip install -r requirements.txt
```
## 2. Configure the App
Duplicate the file `template.env` as `.env` 
```bash
cp template.env .env
```

And set the [environment](#environment-vars) vars for the application

## 3. Poplulate the database (*optional*)
``` bash
conda activate RegFab
python filldb.py
```

# Environment Vars
- **DB_CON_STRING**: A valid SQLAlchemy [Database URL](https://docs.sqlalchemy.org/en/21/core/engines.html#database-urls) (tested on SQLite)
- **DB_DEBUG**: Use 1 or 0 to define if you want to debug the database.
- **FLASK_SECRET**: Flask [cryptographic](https://flask.palletsprojects.com/en/stable/api/#flask.Flask.secret_key) key required for keeping cookies safe.

# Run App (Debug Mode)
This is expected to be executed in the project main directory
``` bash
conda activate RegFab
flask --app . run --debug
```
