# FROM python:3.11-slim

# RUN apt-get update && apt-get install -y \
#     pandoc \
#     texlive-latex-base \
#     texlive-xetex \
#     texlive-fonts-recommended \
#     texlive-latex-extra \
#     fonts-freefont-ttf \
#     && apt-get clean

# WORKDIR /app
# COPY . /app

# RUN pip install --no-cache-dir -r requirements.txt

# EXPOSE 8501
# CMD ["streamlit", "run", "Run_App.py", "--server.port=8501", "--server.enableCORS=false"]


FROM pandoc/extra:latest

RUN apk add --no-cache python3 py3-pip ttf-freefont

WORKDIR /app
COPY . /app

RUN pip3 install --no-cache-dir -r requirements.txt


EXPOSE 8501
ENTRYPOINT [ "streamlit" ]
CMD ["run", "app.py", "--server.port=8501", "--server.address=0.0.0.0", "--server.enableCORS=false", "--server.enableXsrfProtection=false"]
