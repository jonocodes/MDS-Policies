#!/usr/bin/python

import datetime
import os
import requests
import pandas as pd
from collections import defaultdict


def fetch_policies(region_id: str = None):
    """Fetch the policies from the API with the specifed region"""

    # if no region is specified, fetch for all regions
    if not region_id:
        region_id = ""

    data = requests.get(
        f"https://api.populus.ai/v1/mds/policies?region_id={region_id}",
        headers={"X-API-KEY": os.environ["API_KEY"], "Accept": "application/json"},
    ).json()

    df = pd.DataFrame.from_dict(data)

    policies = pd.json_normalize(df["data"]["policies"])

    # reformat the date fields from epoc to datetime

    policies["start_date"] = pd.to_datetime(
        policies["start_date"], unit="ms"
    )
    policies["end_date"] = pd.to_datetime(policies["end_date"], unit="ms")

    return policies

def get_active_policies(policies: pd.DataFrame, starting: datetime, ending: datetime):
    """Get the policies that are active between 'starting' and 'ending'."""

    active_policies = policies[
        (
            policies["start_date"].isnull()
            | (policies["start_date"] < ending)
        )
        & (
            policies["end_date"].isnull()
            | (policies["end_date"] > starting)
        )
    ]

    return active_policies


def get_rules(policies: pd.DataFrame):
    """Fetch the unique rules in the policies."""

    rule_list = []
    for entries in policies["rules"]:
        rule_list.extend(entries)

    return pd.DataFrame(rule_list).drop_duplicates(subset=["rule_id"])


def get_vehicle_types(rules: pd.DataFrame):

    vtype_counts = defaultdict(int)

    for entries in rules["vehicle_types"]:
        if isinstance(entries, list):
            for t in entries:
                vtype_counts[t] += 1

    return pd.DataFrame(vtype_counts.items(), columns=["type", "count"]) 


def get_rule_types(rules: pd.DataFrame):
    """Fetch the rule counts aggregated by type."""

    return (
        rules.groupby("rule_type")["rule_type"]
        .agg(total="count")
        .sort_values(by="total", ascending=0)
    )


def print_stats(region_id: str=None):
    """Fetch and print policy stats for a region."""

    # define the timespan to look for (the last month)
    ending = datetime.datetime.utcnow().replace(
        day=1, hour=0, minute=0, second=0, microsecond=0
    ) - datetime.timedelta(microseconds=1)

    starting = ending.replace(day=1, hour=0, minute=0, second=0, microsecond=0)

    print(f"fetching data from API for region {region_id if region_id else 'ALL'}")

    policies = fetch_policies(region_id)

    print(f"total policies in region = {len(policies)}")

    active_policies = get_active_policies(policies, starting, ending)

    print(
        f"active policies last month ({starting:%Y/%m/%d} - {ending:%Y/%m/%d}) = {len(active_policies)}"
    )

    rules = get_rules(active_policies)

    print(f"unique rules in active policies = {len(rules)}\n")

    print("specified vehicle representation in rules = ")

    vtypes = get_vehicle_types(rules)

    print(vtypes.to_string(header=False, index=False))

    types = get_rule_types(rules)

    print("\nrule types = ")

    print(types['total'].to_string(header=False))

    # plot a bar graph if run in jupiter notebook
    types.sort_values(by="total", ascending=1).plot.barh(ylabel="rule")


# MAIN

if not "API_KEY" in os.environ:
    exit("API_KEY environment variable required")


print_stats()

print()

print_stats("oakland")

print()
