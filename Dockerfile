#FROM python:3.9.13-alpine3.16
FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1

# install project dependencies
ADD requirements.txt .
RUN pip install -r requirements.txt

# Add project files
ADD main.py .
ADD filters.py .

ENTRYPOINT ["python3", "./main.py"]