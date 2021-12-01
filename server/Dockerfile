FROM python:latest

# PREPARE LINUX PROGRAMMS
RUN apt-get update
RUN apt-get install -y mc
RUN apt-get install -y htop
RUN apt-get install -y curl

# COPY FILES
COPY run_server.sh run_server.sh
COPY requirements.txt requirements.txt
COPY . /

# PREPARE PYTHON
RUN curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
RUN python3 get-pip.py
RUN apt-get install -y python3-venv

# OPEN PORT FOR UVICORN
EXPOSE 8000

# LOAD REQ
RUN pip install -r requirements.txt

CMD . /run_server.sh