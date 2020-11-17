FROM mediapipe:latest
ENV PYTHONUNBUFFERED 1

RUN mkdir -p /webapps/mediapipe

WORKDIR /webapps/mediapipe

COPY requirements.txt serve.py /webapps/mediapipe/
RUN pip3 install -r requirements.txt

RUN addgroup webapps
RUN useradd -g webapps mediapipe
RUN chown -R mediapipe:webapps /webapps/mediapipe
USER mediapipe