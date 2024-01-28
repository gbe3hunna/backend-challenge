FROM python:3.10-bullseye

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY /src /code/src
COPY ./docker/api/entrypoint.sh /code/entrypoint.sh

ENTRYPOINT ["bash", "entrypoint.sh"]