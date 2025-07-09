# "Gone Fishing" MCP Server

## Setup

### Things you'll need
**API Keys**
* `tomorrow.io` - [Link](https://docs.tomorrow.io/reference/api-authentication)
    * Tomorrow.io offeres a free rate-limited plan.

### Steps
**TODO**

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
