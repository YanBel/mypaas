FROM    python:2.7-alpine
RUN     mkdir /mypaas
ADD     * /mypaas/
WORKDIR /mypaas
RUN     echo "===> Installing sudo to emulate normal OS behavior..." && \
        apk --update add sudo && \
        echo "===> Adding Python runtime..." && \
        apk --update add python py-pip openssl ca-certificates pwgen && \
        apk --update add --virtual build-dependencies python-dev libffi-dev openssl-dev build-base && \
        pip install --upgrade pip cffi ovh && \
        echo "===> Installing Ansible..." && \
        pip install ansible==2.3.0.0 && \
        echo "===> Removing package list..." && \
        apk del build-dependencies && \
        rm -rf /var/cache/apk/*
        
RUN echo "Container Ready"
