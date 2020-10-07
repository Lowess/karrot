FROM python:3.7-stretch as builder

ENV PYTHONPATH /src:/venv/lib/python3.7/site-packages
ENV PATH $PATH:/venv/bin

# Copy the source code into the container
COPY . /src

# Copy files needed to install app requirements
# COPY ./requirements.txt /src/requirements.txt
# COPY ./setup.py /src/setup.py
# COPY ./karrot/release.py /src/karrot/release.py

# Install app requirements in virtualenv
ENV PYTHONUSERBASE /venv
RUN mkdir /venv \
  && cd /src \
  && pip3 install --ignore-installed --user -r /src/requirements.txt

################################################################################################################

FROM python:3.7-stretch as app

ENV PYTHONPATH /:/venv/lib/python3.7/site-packages
ENV PATH $PATH:/venv/bin
ENV FLASK_APP karrot.wsgi
ENV FLASK_ENV production
ENV AWS_DEFAULT_REGION us-east-1

# Copy the app src and dependencies
COPY --from=0 /src /app
COPY --from=0 /venv /venv
COPY docker/entrypoint.sh /entrypoint.sh

WORKDIR /app
EXPOSE 5000

ENTRYPOINT ["/entrypoint.sh"]
CMD ["karrot:create_app()", "--config", "karrot/wsgi.py"]
