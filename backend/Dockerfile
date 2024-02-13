FROM python:3.12
WORKDIR /config
COPY ./config /config
RUN pip install -r requirements.txt
EXPOSE 8000
ENTRYPOINT ["sh", "/config/entrypoint.sh"]