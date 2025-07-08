# "Gone Fishing" MCP Server

## Dev Setup

### Things you'll need
**API Keys**
* `openai` - [Link](https://platform.openai.com/docs/quickstart?api-mode=responses)
    * Unfortunately, OpenAI's API isn't free. You'll also need to purchase a few credits 😭
* `tomorrow.io` - [Link](https://docs.tomorrow.io/reference/api-authentication)
    * Tomorrow.io offeres a free rate-limited plan.

### Steps
1. Clone Repo
```bash
git clone https://github.com/phelanjo/gone-fishing-mcp.git
cd src
cp .env__COPY_ME .env
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

## Example Queries
NLP should be able to pick out `body_of_water` and `state` from a prompt. 
```
What are the current fishing conditions and types of fish on Parker Canyon Lake in Arizona?
What are the current fishing conditions and types of fish on Lake Pleasant in Arizona?
What are the current fishing conditionsa and types of fish in Arizona along the Colorado River?
```

Certain queries perform better than others, so YMMV!

## Future Considerations
* Storing data more efficiently (or at all)
* Handle prompts for multiple bodies of water, city, city/state etc.
* Look for ways to improve NLP accuracy in finding bodies of water (Maybe just build a database instead?)
* Get accurate water data. 
    * USGS (water service) has an API, but there isn't much useful data in there based on the queries I was performing. 
    * If there isn't a better way, perhaps we could do estimations?
* Unit Tests!
