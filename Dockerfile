FROM python:3.11-slim

WORKDIR /app

COPY pyproject.toml main.py analisi.py caricatore_dati.py ./

RUN pip install --no-cache-dir .

ENTRYPOINT ["python", "main.py"]
