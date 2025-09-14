FROM python:3.13.5

ADD app.py .

# Install dependencies
RUN pip install Flask requests Flask-Session Flask-Cors Flask-SQLAlchemy python-dotenv psycopg2-binary bcrypt

EXPOSE 5000

CMD [ "python", "./app.py" ]