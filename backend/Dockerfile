FROM python:3

ENV PYTHONUNBUFFERED 1
RUN mkdir /code
WORKDIR /code
ADD requirements.txt /tmp/
RUN pip install -i http://nexus.daocloud.io/repository/daocloud-pypi/simple  --trusted-host nexus.daocloud.io -r /tmp/requirements.txt