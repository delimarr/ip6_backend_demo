FROM python:3.9.18

WORKDIR /workdir

RUN apt-get update && apt-get upgrade -y

RUN pip install --upgrade pip \
    && pip install 'poetry==1.6.1'

# git stuff required for linux
RUN git config --global --add safe.directory /workdir

# activate poetry and pre-commit hook
CMD poetry install \
    && poetry shell \
    && pre-commit install
