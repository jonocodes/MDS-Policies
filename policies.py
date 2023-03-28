#!/usr/bin/python

import datetime
import os
import requests
import pandas as pd

# load the data into memory

try:
    # if we have the data cached locally, be polite and dont hammer the API
    df = pd.read_json("policies.json1")
except:
    print("fetching data from API")
    if not "API_KEY" in os.environ:
        exit("API_KEY environment variable required")

    data = requests.get(
        "https://api.populus.ai/v1/mds/policies",
        headers={"X-API-KEY": os.environ["API_KEY"], "Accept": "application/json"},
    ).json()
    df = pd.DataFrame.from_dict(data)


policies = pd.json_normalize(df["data"]["policies"])

print(f"total policies in catalog = {len(policies)}")

# reformat the date fields from epoc to datetime

policies["start_date"] = pd.to_datetime(policies["start_date"], unit="ms")
policies["end_date"] = pd.to_datetime(policies["end_date"], unit="ms")

# define the timespan to look for

ending = datetime.datetime.utcnow().replace(
    day=1, hour=0, minute=0, second=0, microsecond=0
) - datetime.timedelta(microseconds=1)

starting = ending.replace(day=1, hour=0, minute=0, second=0, microsecond=0)

active_policies = policies[
    (policies["start_date"].isnull() | (policies["start_date"] < ending))
    & (policies["end_date"].isnull() | (policies["end_date"] > starting))
]

print(
    f"active policies last month ({starting:%Y/%m/%d} - {ending:%Y/%m/%d}) = {len(active_policies)}"
)

# flatten all the rules into a single unique table
rule_list = []
for entries in active_policies["rules"]:
    rule_list.extend(entries)

rules = pd.DataFrame(rule_list).drop_duplicates(subset=["rule_id"])

print(f"unique rules in active policies = {len(rules)}\n")

# aggregrate/count the rules by type
type_counts = (
    rules.groupby("rule_type")["rule_type"]
    .agg(total="count")
    .sort_values(by="total", ascending=0)
)

print(type_counts)
