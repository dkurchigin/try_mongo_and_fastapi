FROM python:latest

# PREPARE LINUX PROGRAMMS
RUN apt-get update
RUN apt-get install -y mc
RUN apt-get install -y htop
RUN apt-get install -y curl

# COPY FILES
COPY employees.json employees.json
COPY load_data.py load_data.py
COPY run_load_data.sh run_load_data.sh
COPY requirements.txt requirements.txt

# PREPARE PYTHON
RUN curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
RUN python3 get-pip.py
RUN apt-get install -y python3-venv


# LOAD REQ
RUN pip install -r requirements.txt

CMD . /run_load_data.sh