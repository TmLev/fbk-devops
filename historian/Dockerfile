# Python image
FROM python:3.9.1-buster

# Install runtime libraries for Postgres connection
RUN apt-get install -y libpq-dev

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PYTHONPATH "/historian/src:${PYTHONPATH}"

# Set working directory
WORKDIR /historian

# Copy Pipfile[.lock]
COPY historian/Pipfile* ./

# Install pipenv and packages
RUN pip install pipenv && \
    pipenv install --system --deploy --dev

# Copy tools
COPY tools /tools

# Copy everything else
COPY historian .

# Run service
CMD ["python", "src/main.py"]
