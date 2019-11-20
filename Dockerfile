FROM python:3.7-stretch as builder

ENV PYTHONPATH /src:/venv/lib/python3.7/site-packages
ENV PATH $PATH:/venv/bin

# Copy files needed to install app requirements
COPY ./requirements.txt /src/requirements.txt

# Install app requirements in virtualenv
ENV PYTHONUSERBASE /venv
RUN mkdir /venv \
  && pip3 install --ignore-installed --user -U pyopenssl cryptography certifi idna ndg-httpsclient pyasn1 \
  && pip3 install --ignore-installed --user -r /src/requirements.txt

# Copy the source code into the container
COPY . /src

################################################################################################################

FROM python:3.7-stretch as app

ENV PYTHONPATH /:/venv/lib/python3.7/site-packages
ENV PATH $PATH:/venv/bin
ENV FLASK_APP karrot.wsgi
ENV FLASK_ENV production
# Copy the app src and dependencies
COPY --from=0 /src /app
COPY --from=0 /venv /venv
COPY docker/entrypoint.sh /entrypoint.sh

WORKDIR /app
EXPOSE 5000

ENTRYPOINT ["/entrypoint.sh"]
CMD ["karrot:create_app()", "--bind 127.0.0.1:5000", "-w 4"]
