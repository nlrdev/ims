FROM python:3.10-slim
RUN mkdir /usr/src/app
WORKDIR /usr/src/app
ADD ./ims /usr/src/app
RUN pip install --upgrade pip 
RUN pip install pipenv
RUN pipenv install --skip-lock --system