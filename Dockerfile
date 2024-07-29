# Use an official Python runtime as a parent image
FROM python:3.12-slim-bullseye

# Set environment variables
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

# Set the working directory
WORKDIR /app

# Install Python dependencies
COPY requirements.txt /app/
# 첫 번째 시도
RUN pip install --upgrade pip || \
    # 실패할 경우, python.exe -m pip로 재시도
    python.exe -m pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Copy the Django project
COPY . /app/

# Expose port 8000 to allow communication to/from uwsgi
EXPOSE 8000

# Run uWSGI
CMD ["uwsgi", "--ini", "/app/uwsgi.ini"]
