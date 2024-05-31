# Software Technology Project 2024

## Software Installation

There are two ways to install and run the app:

- Cloning the repository and running the Docker container.
- Cloning the repository and running the app manually.

### Cloning the Repository

Make sure you have [Git](https://git-scm.com/downloads) installed on your machine.

```bash
git clone https://github.com/maikkundev/soft-tech-project-2024.git
```

### Docker

Docker is the easiest way to run the app. Make sure you have [Docker](https://docs.docker.com/get-docker/) installed on your machine.

```bash
docker compose up
```

*Please make sure that port `8501` is not being used by some other process.*

### Manual Installation & Running

#### Virtual Environment

Create a Python virtual enviroment (venv) and activate said enviroment:

```bash
python -m venv ./.venv
```

```bash
# Linux/Unix:
$ source <PROJECT_PATH>/.venv/bin/activate
```

```bash
# Windows: 
PS <PROJECT_PATH>\.venv\Scripts\Activate.ps1
```

#### Installing the Required Libraries

Install the necessary Python libraries that are included in the `requirements.txt` file using your preferred package manager:

```bash
pip3 install -r requirements.txt
```

#### Running the App

Run app via the `streamlit` command:

```bash
streamlit run ./web/Info.py
```
