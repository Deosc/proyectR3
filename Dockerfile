FROM python:alpine
MAINTAINER reus
RUN apk add nmap
RUN apk add fping
RUN apk add net-snmp-tools
RUN pip install flask
COPY . /src
WORKDIR /src
EXPOSE 5000
EXPOSE 161
EXPOSE 162
ENTRYPOINT ["python", "src/app.py"]
