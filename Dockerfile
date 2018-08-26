FROM python:3.6.6
RUN pip install pipenv
COPY Pipfile Pipfile.lock /app/
WORKDIR /app
RUN pipenv install --system --deploy
COPY . /app
EXPOSE 5000
CMD pipenv run python main.py