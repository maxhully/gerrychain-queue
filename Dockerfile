FROM python:3.6.6
RUN pip install pipenv

WORKDIR /app

COPY Pipfile Pipfile.lock /app/
RUN pipenv install --system --deploy

COPY ./runner /app

EXPOSE 5000

CMD pipenv run python main.py