FROM python:3.6.5

RUN apt-get install libtiff5-dev libjpeg62-turbo-dev zlib1g-dev libfreetype6-dev liblcms2-dev libwebp-dev gcc libmagickwand-dev imagemagick
# RUN apk --update add --no-cache g++
# RUN apk add --no-cache python3-dev libstdc++ && \
#     apk add --no-cache g++ && \
#     ln -s /usr/include/locale.h /usr/include/xlocale.h && \
#     pip3 install numpy && \
#     pip3 install pandas
# set working directory
WORKDIR /app/

# add requirements (to leverage Docker cache)
ADD ./requirements.txt /app/requirements.txt
# install requirements
RUN pip install --no-cache-dir --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt
# ENTRYPOINT celery -A tasks worker --loglevel=info
# create unprivileged user
# RUN adduser --disabled-password --gecos '' app 
