FROM python:2.7-alpine
RUN mkdir /mypaas
ADD * /mypaas/
WORKDIR /mypaas
RUN pip install ansible; \
    pip install ovh

CMD sh genpass.sh
RUN echo "Container Ready"
CMD ansible-playbook -i "localhost," -c local main.yml --syntax-check
