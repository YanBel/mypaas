FROM python:2.7-alpine
RUN mkdir /mypaas
ADD * /mypaas
WORKDIR /mypaas
RUN pip install ansible; \
    pip install ovh

CMD sh genpass.sh
echo "Container Ready"
