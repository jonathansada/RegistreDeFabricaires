FROM python:3.14.0-slim

WORKDIR /regfab

RUN mkdir -p ./data
COPY ./src ./src
COPY ./static ./static
COPY ./templates ./templates
COPY ./__init__.py ./__init__.py 
COPY ./filldb.py ./filldb.py
COPY ./requirements.txt ./requirements.txt
COPY ./template.env ./.env

RUN pip install --upgrade pip
RUN pip install -r requirements.txt
RUN pip install gunicorn

#RUN python ./filldb.py
VOLUME ["/regfab/data"]
EXPOSE 8000

CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:8000", "__init__:flask"]