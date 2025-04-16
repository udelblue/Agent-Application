

## Setting up a Virtual Environment on Windows

1. Open a terminal or command prompt.
2. Ensure Python is installed and added to your PATH by running `python --version` or `py --version`.
3. Navigate to your project folder using `cd <path_to_project>`.
4. Create a virtual environment by running `python -m venv .venv` or `py -m venv .venv`.
5. Activate the virtual environment by running `.venv\Scripts\activate`.
6. Install necessary dependencies within the virtual environment using `pip install -r requirements.txt`.

## Install
pip install -r requirements.txt

rename .env-example to .env and replace sk-*********************************** with your OpenAI key

## Run
uvicorn main:app --reload

Note the swagger endpoint is located at http://127.0.0.1:8000/docs

## Docker

docker build -t backend-agent . 

docker run -d -p 8000:8000 backend-agent
