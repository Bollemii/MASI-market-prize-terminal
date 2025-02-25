FROM python:3.12.0-alpine3.18

WORKDIR /app

COPY requirements.txt /app/requirements.txt

RUN pip install --upgrade pip

RUN pip install -r requirements.txt

COPY . /app/

CMD [ "python", "__main__.py" ]
