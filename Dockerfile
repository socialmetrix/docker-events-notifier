FROM python:3-alpine

WORKDIR /usr/src/app

COPY . /usr/src/app

RUN pip install --no-cache-dir -r requirements.txt && \
  rm /usr/src/app/requirements.txt

CMD [ "python", "./app.py" ]