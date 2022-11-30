FROM python:3.10.5-alpine

ENV TZ=America/Sao_Paulo
RUN ln -snf /usr/share/zoneinfo/${TZ} /etc/location && echo &{TZ} > /etc/timezone

ARG UID=1000
ARG GID=1000
ARG ENV=development
ARG UNAME=dev
ENV PATH="/home/dev/.local/bin:${PATH}"

RUN addgroup -S devgroup && adduser -S dev -G devgroup -u ${UID} -h /home/dev

RUN mkdir /opt/python-webapp

RUN chown ${UID} /opt/python-werbapp

WORKDIR /opt/python-webapp

USER ${UID}

ENTRYPOINT [ "/bin/sh", "/opt/setup.sh" ]

CMD ["flask", "run", "--host=0.0.0.0", "--port=5000"]

