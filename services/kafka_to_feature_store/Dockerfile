FROM python:3.11-slim

# install gcc and python3-dev to compile Python packages
RUN apt-get update && apt-get install -y \
    gcc \
    python3-dev

# Stream output to console
ENV PYTHONUNBUFFERED=1

# add /app/src to PYTHONPATH
ENV PYTHONPATH "${PYTHONPATH}:/app/src"

# Install poetry
RUN pip install poetry==1.8.3

# Set the working directory in the container
WORKDIR /app

# Copy the pyproject.toml and poetry.lock file to the working directory
COPY pyproject.toml poetry.lock /app/

# Install dependencies
RUN poetry install

# Copy the source code to the working directory
COPY src/*.py /app/src/

CMD ["poetry", "run", "python", "src/main.py"]