FROM python:2.7-alpine

COPY Mini-Blog /Mini-Blog 
WORKDIR /Mini-Blog
RUN pip install --upgrade pip
RUN python setting.py


CMD ["/bin/sh"]