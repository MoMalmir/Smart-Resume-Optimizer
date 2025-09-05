
FROM debian:bullseye-slim

# Avoid prompts during package installation
ENV DEBIAN_FRONTEND=noninteractive

# Install system dependencies
RUN apt-get update && apt-get install -y \
    pandoc \
    python3 python3-pip \
    fonts-freefont-ttf \
    texlive-full \
    latexmk \
    make \
    fontconfig \
    bash \
 && apt-get clean && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY . /app

# Set permissions for Streamlit
RUN mkdir -p /app/.streamlit && chmod -R 777 /app/.streamlit

# Install Python dependencies
RUN pip3 install --no-cache-dir -r requirements.txt

ENV HOME=/app

EXPOSE 7860

ENTRYPOINT ["streamlit"]
CMD ["run", "app.py", "--server.port=7860", "--server.address=0.0.0.0", "--server.enableCORS=false", "--server.enableXsrfProtection=false"]
