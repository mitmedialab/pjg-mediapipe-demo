FROM mediapipe:latest
ENV PYTHONUNBUFFERED 1

WORKDIR /mediapipe

COPY serve.py /mediapipe/
COPY requirements.txt /mediapipe/requirements_server.txt
RUN pip3 install -r requirements_server.txt

#RUN mkdir -p /webapps/mediapipe
#RUN addgroup webapps
#RUN useradd -g webapps mediapipe
#RUN chown -R --no-dereference mediapipe:webapps /webapps/mediapipe /mediapipe/
#USER mediapipe