FROM python:2.7-alpine

COPY Mini-Blog /Mini-Blog 
WORKDIR /Mini-Blog


CMD ["/bin/sh"]