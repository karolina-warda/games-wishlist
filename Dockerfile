FROM selenium/standalone-chrome:latest

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt --no-cache-dir

COPY main.py main.py

ENTRYPOINT ["python3", "-u", "main.py"]
