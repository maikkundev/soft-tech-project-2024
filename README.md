# Software Technology Project 2024

## How to run the Streamlit web app

### Clone repository using `git`

```bash
git clone https://github.com/maikkundev/soft-tech-project-2024.git
```

## Run the web app via

### Docker

```bash
docker compose up
```

*Please make sure that port `8501` is not taken by another process.*

### Using Streamlit

1. Create a Python virtual enviroment (venv) and activate said enviroment:

```bash
python -m venv ./.venv
```

```bash
# Unix platforms:
$ source <PROJECT_PATH>/.venv/bin/activate
```

```bash
# Windows: 
PS <PROJECT_PATH>\.venv\Scripts\Activate.ps1
```

2. Install the necessary Python libraries that are included in the `requirements.txt` file using your preferred package manager:

```bash
pip3 install -r requirements.txt
```

3. Run app via the `streamlit` command:

```bash
streamlit run ./web/Info.py
```
