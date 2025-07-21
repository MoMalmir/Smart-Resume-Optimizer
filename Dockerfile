
FROM pandoc/extra:latest

RUN apk add --no-cache python3 py3-pip ttf-freefont

WORKDIR /app
COPY . /app


RUN mkdir -p /app/.streamlit && chmod -R 777 /app/.streamlit


RUN pip3 install --no-cache-dir --break-system-packages -r requirements.txt


ENV HOME=/app

EXPOSE 7860

ENTRYPOINT [ "streamlit" ]
CMD ["run", "app.py", "--server.port=7860", "--server.address=0.0.0.0", "--server.enableCORS=false", "--server.enableXsrfProtection=false"]
