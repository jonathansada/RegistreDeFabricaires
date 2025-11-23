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
- **ADMIN_USER**: Username for the administration space.
- **ADMIN_PASSWORD**: Password for the administration space.

It's recommended to generate a unike secret key for **FLASK_SECRET** with:
``` bash
python -c 'import secrets; print(secrets.token_hex())'
```


# Run Application
## Development / Local Mode 
This is expected to be executed in the project main directory
``` bash
conda activate RegFab
flask --app . run --debug
```

## Deployment mode
### Podman / Docker
Create container image:
``` bash
$ podman build -t regfab .
```

Run app
``` bash
podman run -p 8000:8000 -v ./data:/regfab/data regfab
```

### Compose (recomended)
Init the container:
``` bash
$ podman-compose up -d
```

Stop the container:
``` bash
$ podman-compose down
```

Force upgrade the container (if needed):
``` bash
$ podman-compose up -d --build
```

Fill database (if needed):
```bash
$ podman exec registredefabricaires_regfab_1 "python /regfab/filldb.py"
```
(to get the container_name use `docker ps`)