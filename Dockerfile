FROM python:3

ENV PYTHONBUFFERD 1

ENV PYTHONDONTWRTEBYTECODE 1

RUN mkdir /kilo

WORKDIR /kilo

COPY . /kilo

RUN python -m venv /appenv

ENV PATH="/appenv/bin/:$PATH"

COPY entrypoint.sh /kilo/entrypoint.sh

RUN python -m pip install --upgrade pip

RUN pip install -r requirements.txt