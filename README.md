# gone-fishing-mcp

## Dev Setup

### Things you'll need
**API Keys**
* `openai` - [Link](https://platform.openai.com/docs/quickstart?api-mode=responses)
* `tomorrow.io` - [Link](https://docs.tomorrow.io/reference/api-authentication)

### Steps
1. Clone Repo
```bash
git clone https://github.com/phelanjo/gone-fishing-mcp.git
cd src
```

2. Install Virtual Environment
```bash
python -m venv venv/
source /venv/bin/activate
```

3. Install Dependencies
```bash
pip install -r requirements.txt

python -m spacy download en_core_web_sm
```

4. Start Server
```bash
uvicorn src.main:app --reload
```

Now you can access the Swagger docs locally at `http://localhost:8000/docs` and play around with the endpoint.