FROM python:3
RUN touch /var/log/access.log
WORKDIR /usr/src
ADD . /usr/src
RUN pip install .
ENTRYPOINT ["log-analyzer"]