# Description
This is an application for collecting information about the users who visits [EspluLab](https://www.esplugues.cat/es/esplulab/) and get information about the usage of the the machines and material. 

# App details
This was meant to be executed on local network inside EspluLab and is *not ready to be exposed on the internet*.
This was done as an opportunity to practice with SQLAlchemy and Flask as the same time I provided an easy way to collect the information needed through any machine in the local network.

# Set-up App
This is expected to be using Conda (throough micro-forge)

Install the conda environment
``` bash
conda env create --name EspluLab --file base_env.yml
```

Install pip requirements
```bash
pip install -r requirements.txt
```

# Run App (Debug Mode)
This is expected to be executed in the project main directory
``` bash
conda activate EspluLab
flask --app . run --debug
```
