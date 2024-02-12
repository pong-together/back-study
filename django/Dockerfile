FROM python:3.12
WORKDIR /code
COPY ./srcs/requirements.txt /code
RUN pip install -r requirements.txt
EXPOSE 8000
ENTRYPOINT ["sh", "/code/entrypoint.sh"]