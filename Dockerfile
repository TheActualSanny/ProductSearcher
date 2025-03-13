FROM python:3.12

WORKDIR /
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . /src

WORKDIR /src

EXPOSE 8000
CMD python manage.py migrate && python manage.py runserver 0.0.0.0:8000 --noreload  