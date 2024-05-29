FROM python:3.11-slim
ENV PYTHONUNBUFFERED 1

WORKDIR /app/

RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    software-properties-common \
    git \
    && rm -rf /var/lib/apt/lists/*

# Enable venv
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# copy dependencies
COPY ./requirements.txt /app/
RUN pip3 install -r requirements.txt

# Copy the web app
COPY /web/ /app/web/

HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

ENTRYPOINT [ "streamlit", "run", "./web/Hello.py", "--server.address=0.0.0.0" ]