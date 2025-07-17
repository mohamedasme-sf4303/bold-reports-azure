import dlt
import json
from dlt.common import pendulum
import pandas as pd
import requests
from requests.auth import HTTPBasicAuth
import base64
import os
import posixpath
from typing import Iterator

import dlt
from dlt.sources import TDataItem, TDataItems

try:
    from .filesystem import FileItemDict, filesystem, readers, read_csv, read_jsonl, read_parquet  # type: ignore
except ImportError:
    from filesystem import (
        FileItemDict,
        filesystem,
        readers,
        read_csv,
        read_jsonl,
        read_parquet,
    )
    
api_endpoint = '{8}'
{1}


# Set headers with Basic Authentication
{2}
{3}
if response.status_code == 200:
    api_data = json.loads(response.text)
else:
    print("Error: "+ str(response.status_code))
    api_data = None

# Create DataFrame if data is available
if api_data:

    def api_data_generator() -> Iterator[dict]:
       yield from api_data
    
    resource = dlt.resource(api_data_generator(), name="{4}")
    pipeline = dlt.pipeline("{0}_pipeline", destination="filesystem", dataset_name="{0}")
    pipeline.run(resource, loader_file_format="jsonl")
    dir_path = '{5}'
    try:
        if os.path.isdir(dir_path):
            
    
            file_paths = [os.path.join(dir_path, filename) for filename in os.listdir(directory_path)]

            for file_path in file_paths:
                filePath = (file_path)
                def jsonl_reader() -> Iterator[dict]:
                    with open(filePath, "r", encoding="utf-8") as f:
                        for line in f:
                            yield json.loads(line)
                web_data = dlt.resource(jsonl_reader(), name="{6}")
                pipelinef = dlt.pipeline(pipeline_name="{0}_pipeline",destination='{9}',staging={10} ,dataset_name="{0}",)
                load_info = pipelinef.run(web_data)
                print(pipelinef.last_trace.last_normalize_info)
        else:
            directory_path = '{7}'
    
            file_paths = [os.path.join(directory_path, filename) for filename in os.listdir(directory_path)]
    
            for file_path in file_paths:
                filePath = (file_path)
                def jsonl_reader() -> Iterator[dict]:
                    with open(filePath, "r", encoding="utf-8") as f:
                        for line in f:
                            yield json.loads(line)
                web_data = dlt.resource(jsonl_reader(), name="{6}")
                pipelinef = dlt.pipeline(pipeline_name="{0}_pipeline",destination='{9}',staging={10} ,dataset_name="{0}",)
                load_info = pipelinef.run(web_data)
                print(pipelinef.last_trace.last_normalize_info)
    except Exception as e:
        print(f'An unexpected error occurred: {{e}}')