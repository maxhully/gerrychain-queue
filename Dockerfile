FROM python:3.6.5
RUN pip install pipenv

WORKDIR /app

COPY Pipfile Pipfile.lock /app/
RUN pipenv install --system

COPY . /app

EXPOSE 5000

ENV FLASK_APP=gerrychain_queue
ENV FLASK_ENV=production

CMD pipenv run gunicorn -b :5000 --access-logfile - --error-logfile - "gerrychain_queue:create_app()"