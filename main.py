import json
import requests
import os
from datetime import datetime, timedelta

# load environment variables
PAT = os.environ["PAT"]
JSON_URL = os.environ["JSON_URL"]

# constants defined
OUT_FILE_PATH = "output/cas_recent_assets.json"
LOG_FILE_PATH = "output/cas_recent_assets_log.txt"
ASSET_FILE_NAME = "esploro_assets.json"

# TODO: change this to dynamically calculated
CUTOFF_YEAR = 2023


def main():

    log_it(f"======== Starting at {str(datetime.now())}")

    all_assets = fetch_json_data(JSON_URL, PAT)

    log_it(f"{len(all_assets)} assets retrieved from {ASSET_FILE_NAME}.")
    # build list of CAS assets
    cas_assets = []

    for asset in all_assets:
        if "asset.affiliation" in asset:
            if "College of Arts and Sciences" in asset["asset.affiliation"]:
                cas_assets.append(asset)

    log_it(f"Found {len(cas_assets)} CAS assets.")

    cas_output = []
    for asset in cas_assets:
        a = asset_format(asset)
        if a["date"] >= CUTOFF_YEAR:
            cas_output.append(asset_format(asset))

    log_it(
        str(len(cas_output))
        + " CAS assets after "
        + str(CUTOFF_YEAR)
        + ". Saving to "
        + OUT_FILE_PATH
    )

    save_json(cas_output, OUT_FILE_PATH)

    log_it(f"======== Finished at {str(datetime.now())}")


#### FUNCTIONS


def log_it(msg, log_file_path=LOG_FILE_PATH):
    print(msg)
    with open(log_file_path, "a") as f:
        f.write(msg + "\n")


def asset_format(a):
    # RETURN FORMATED ASSET
    print(a["originalRepository"]["assetId"])
    f = {"mmsid": a["originalRepository"]["assetId"], "title": a["title"]}
    if "identifier.uri" in a:
        f["uri"] = a["identifier.uri"]
    dates = []  # add publication-like dates and find the most recent
    if "date.published" in a:
        dates.append(trim_date(a["date.published"]))
    if "date.performance" in a:
        dates.append(trim_date(a["date.performance"]))
    if "date.presented" in a:
        dates.append(trim_date(a["date.presented"]))

    f["date"] = most_recent(dates)

    # creators

    the_creators = []
    for c in a["creators"]:
        if "creatorname" in c:
            the_creators.append(c["creatorname"])
        elif "organization" in c:
            the_creators.append(c["organization"])
    f["creators"] = the_creators
    f["affiliation"] = a["asset.affiliation"]
    return f


def trim_date(data):
    x = data[0] if isinstance(data, list) else data
    return int(x[:4])


def most_recent(list):
    return max(list) if len(list) > 0 else 0


def save_json(data, output_path):
    """save output as json file

    Args:
        data (dict): JSON representation
        output_path (str): path to save JSON
    """
    print(f"Saving to {str(output_path)}...")
    with open(output_path, "w") as f:
        json.dump(data, f)


def fetch_json_data(url, token):
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json()


if __name__ == "__main__":
    main()
