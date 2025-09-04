# FROM pandoc/extra:latest

# # Use apt-get instead of apk — pandoc/extra is Debian-based
# RUN apt-get update && apt-get install -y \
#     python3 python3-pip \
#     ttf-freefont \
#     texlive-full \
#     xetex \
#     latexmk \
#     make \
#     fontconfig \
#     bash \
#     texlive-fonts-extra  

# WORKDIR /app
# COPY . /app

# RUN mkdir -p /app/.streamlit && chmod -R 777 /app/.streamlit

# # Install Python requirements
# RUN pip3 install --no-cache-dir --break-system-packages -r requirements.txt

# ENV HOME=/app

# EXPOSE 7860

# ENTRYPOINT ["streamlit"]
# CMD ["run", "app.py", "--server.port=7860", "--server.address=0.0.0.0", "--server.enableCORS=false", "--server.enableXsrfProtection=false"]



FROM pandoc/extra:latest


RUN apk update && apk add --no-cache \
    python3 py3-pip \
    ttf-freefont \
    texlive-full \
    texmf-dist-xetex \
    latexmk \
    make \
    fontconfig \
    bash \
    texlive-fontsextra

WORKDIR /app
COPY . /app

RUN mkdir -p /app/.streamlit && chmod -R 777 /app/.streamlit

# Install Python requirements
RUN pip3 install --no-cache-dir -r requirements.txt

ENV HOME=/app

EXPOSE 7860

ENTRYPOINT ["streamlit"]
CMD ["run", "app.py", "--server.port=7860", "--server.address=0.0.0.0", "--server.enableCORS=false", "--server.enableXsrfProtection=false"]
