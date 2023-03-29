# About

I made heavy use of Pandas, since I enjoyed learning how to process and plot the data.

![types](types.png?raw=true "types")

# Running

    pip install -r requirements.txt
    API_KEY=xxxx python policies.py

## To see the graph(s)

    API_KEY=xxxx jupyter lab policies.ipynb

# Notes

## To cache locally

    curl -H "X-API-KEY: xxxx" "https://api.populus.ai/v1/mds/policies"| jq . > policies.json

## API parameters

I could not get params to work. Tried id, start_date, end_date. Also geography by uuid.

```bash
➜  curl -H "X-API-KEY: xxxx" -H "Accept: application/json" "https://api.populus.ai/v1/mds/policies" | wc
      0    6931  602886

➜  curl -H "X-API-KEY: xxxx" -H "Accept: application/json" "https://api.populus.ai/v1/mds/policies?end_date=1679957344000" | wc
      0    6931  602886

➜  curl -H "X-API-KEY: xxxx" -H "Accept: application/json" "https://api.populus.ai/v1/mds/policies/?end_date=1679957344000&end_date=1679957344000" | wc
      0    6931  602886

➜  curl -H "X-API-KEY: xxxx" -H "Accept: application/json" "https://api.populus.ai/v1/mds/policies/cb0e6c9d-34fc-40b9-9145-f03fc47c4cfa"
{"error":"Not Found"}

➜  curl -H "X-API-KEY: xxxx" -H "Accept: application/json" "https://api.populus.ai/v1/mds/policies/cb0e6c9d34fc40b99145f03fc47c4cfa" 
{"error":"Not Found"}

curl -H "X-API-KEY: xxxx" -H "Accept: application/json" "https://api.populus.ai/v1/mds/geographies/d74a13fd-e98c-4d65-9dfe-6e98c35478b4"|jq
{
  "error": "Not Found"
}

```
