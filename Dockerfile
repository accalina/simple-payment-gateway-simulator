# Preparing Stage
FROM python:3.8-slim as base
LABEL author="Accalina"

# Builder Stage
FROM base as builder
WORKDIR /pg_sim
ENV PATH=/install/bin:$PATH
RUN mkdir /install

COPY ./backend .
RUN pip install --prefix=/install -U setuptools pip
RUN pip install --prefix=/install -r requirements.txt

# Runtime Stage
FROM base as runtime
WORKDIR /pg_sim
ENV PYTHONUNBUFFERED 1

COPY --from=builder /pg_sim .
COPY --from=builder /install /usr/local
