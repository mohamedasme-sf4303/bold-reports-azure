import requests
import msal
import pandas as pd
from io import StringIO, BytesIO
import dlt
import os
import json
import yaml

CLIENT_ID = "{0}"
AUTHORITY = "https://login.microsoftonline.com/{1}"
SCOPES = ["Files.Read.All", "User.Read"]
ONEDRIVE_FILE_PATH = "{2}"

CACHE_PATH = "token_cache.json"
cache = msal.SerializableTokenCache()
if os.path.exists(CACHE_PATH):
    cache.deserialize(open(CACHE_PATH, "r").read())

app = msal.PublicClientApplication(client_id=CLIENT_ID, authority=AUTHORITY, token_cache=cache)

accounts = app.get_accounts()
result = None
if accounts:
    result = app.acquire_token_silent(scopes=SCOPES, account=accounts[0])

if not result:
    result = app.acquire_token_interactive(scopes=SCOPES)

if cache.has_state_changed:
    with open(CACHE_PATH, "w") as f:
        f.write(cache.serialize())

if result and "access_token" in result:
    access_token = result["access_token"]
    auth_header = ("Bearer " + access_token).strip()
    headers = dict(Authorization=auth_header)

    item_url = "https://graph.microsoft.com/v1.0/me/drive/root:/{2}"
    item_resp = requests.get(item_url, headers=headers)

    if item_resp.status_code != 200:
        print("File not found")
        print(item_resp.text)
        exit()

    file_id = item_resp.json()["id"]

    download_url = "https://graph.microsoft.com/v1.0/me/drive/items/" + file_id + "/content"
    file_response = requests.get(download_url, headers=headers)

    file_ext = os.path.splitext(ONEDRIVE_FILE_PATH)[1].lower()
    df = None

    if file_ext == ".csv":
        content = file_response.content.decode("utf-8")
        df = pd.read_csv(StringIO(content))
    elif file_ext == ".json":
        content = file_response.content.decode("utf-8")
        json_data = json.loads(content)
        if isinstance(json_data, list):
            df = pd.DataFrame(json_data)
        elif isinstance(json_data, dict):
            try:
                df = pd.json_normalize(json_data)
            except Exception:
                df = pd.DataFrame.from_dict(json_data, orient='index')
    elif file_ext in [".xls", ".xlsx"]:
        df = pd.read_excel(BytesIO(file_response.content))
    elif file_ext in [".yml", ".yaml"]:
        content = file_response.content.decode("utf-8")
        yaml_data = yaml.safe_load(content)
        if isinstance(yaml_data, list):
            df = pd.DataFrame(yaml_data)
        elif isinstance(yaml_data, dict):
            df = pd.json_normalize(yaml_data)
    else:
        print(f"Unsupported file type")
        exit()

    pipeline = dlt.pipeline(
        pipeline_name="{4}_pipeline",
        destination="{5}",
        dataset_name="{4}"
    )

    load_info = pipeline.run(df.to_dict(orient="records"), table_name="{3}")
    print("Data loaded to destination:")
    print(load_info)

else:
    print("Authentication failed:")
    print(result.get("error_description"))
