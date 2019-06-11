FROM python:3.6.5

RUN apt-get install libtiff5-dev libjpeg62-turbo-dev zlib1g-dev libfreetype6-dev liblcms2-dev libwebp-dev gcc libmagickwand-dev 
RUN apt-get update
RUN apt-get install -y software-properties-common
RUN apt-get update && apt-get install -y ffmpeg
RUN apt-get install -y imagemagick

WORKDIR /app/

# add requirements (to leverage Docker cache)
ADD ./requirements.txt /app/requirements.txt
# install requirements
RUN pip install --no-cache-dir --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt
RUN apt-get install -y libmagick++-dev
RUN sed -i 's/.*pattern.*@.*//' /etc/ImageMagick-6/policy.xml
