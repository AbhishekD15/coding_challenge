FROM python:3.12-slim

RUN apt-get update && rm -rf /var/lib/apt/lists*
RUN pip install pipenv

WORKDIR /app
COPY . /app
ARG PIPENV_INSTALL_ARGS="--system --deploy"
RUN pipenv install ${PIPENV_INSTALL_ARGS}

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONIOENCODING=UTF-8
ENV LANG=C.UTF-8
ENV LC_ALL=C.UTF-8

EXPOSE 8000
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
