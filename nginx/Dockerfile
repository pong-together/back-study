FROM nginx:bookworm
RUN apt-get update && \
	apt-get install -y openssl
COPY ./conf.d /etc/nginx/conf.d
COPY ./scripts/entrypoint.sh .
RUN chmod +x entrypoint.sh 
EXPOSE 443
ENTRYPOINT ["./entrypoint.sh"]