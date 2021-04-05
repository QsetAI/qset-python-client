import requests
import pandas as pd
import os
import math

from tenacity import retry, stop_after_attempt, wait_exponential
from loguru import logger

from .utils import *


class ClientV0:
    def __init__(
        self,
        api_key=None,
        api_url="http://api.qset.ai:8000/v0",
        verbose=False,
        show_progress_bar=True,
    ):
        self.api_key = api_key or os.environ.get(
            "QSET_API_KEY"
        )  # todo: warn if not found
        self.api_url = api_url

        self.verbose = verbose
        self.show_progress_bar = show_progress_bar
        self.progress_bar = None

        self.coder = MsgPackCoder()

    def _log(self, msg, level="DEBUG", **kwargs):
        if self.verbose:
            logger.log(level, msg, **kwargs)

    def _url(self, path):
        return f"{self.api_url}{path}"

    def _call(self, api_path, params=None, decoder=cast_dict_or_list):
        if not self.api_key:
            raise Exception("API key not set")

        req = self._raw_call(api_path, params)

        try:
            return decoder(req.content)
        except:
            logger.exception("Failed to decode message", message=req.content)
            raise

    @retry(
        stop=stop_after_attempt(10), wait=wait_exponential(multiplier=5.0, exp_base=1.5)
    )
    def _raw_call(self, api_path, params=None):
        self._log("API Call", api_path=api_path, params=params)
        req = requests.get(
            self._url(api_path), headers={"x-api-key": self.api_key}, params=params
        )
        return req

    def get_available_datasets(self, format="dataframe"):
        res = self._call("/available_datasets")

        if format == "dataframe":
            return pd.DataFrame(res)
        elif format == "list":
            return res
        else:
            raise Exception("Unknown format")

    def get_dataset_overview(self, dataset):
        return self._call("/dataset_overview", params={"dataset": dataset})

    def get_asset_dataset_range(self, dataset, tickers=None):
        return self._call(
            "/asset_dataset_range", params={"dataset": dataset, "tickers": tickers}
        )

    def get_asset_dataset(self, dataset, start, end, tickers=None, columns=None):
        params = {
            "dataset": dataset,
            "tickers": tickers,
            "start": start,
            "end": end,
            "columns": columns,
        }
        params["format"] = "msgpack"  # for speed and easier type conversion
        return self._call("/asset_dataset", params=params, decoder=self.coder.decode)

    def _iter_data(self, dataset, query=None):
        dataset_overview = self.get_dataset_overview(dataset)

        if dataset_overview["type"] != "asset":
            raise Exception("Client supports only asset datasets at the moment")

        query = query or {}
        query = cast_dict_or_list(query)

        start = cast_datetime(query["start"])
        end = cast_datetime(query["end"])
        tickers = query.get("tickers")
        columns = query.get("columns")

        if not columns:
            columns = dataset_overview["columns"]  # [(column_name, column_type), ...]
            columns = [c[0] for c in columns]

        yield {"type": "columns", "data": columns}

        asset_range = self.get_asset_dataset_range(dataset, tickers)

        start = max(cast_datetime(asset_range["minStartRange"]), start)
        end = min(cast_datetime(asset_range["maxStartRange"]), end)

        if dataset_overview["max_request_range"] == "31d":
            total = len(list(iter_range_by_months(start, end)))
            range_iterator = iter_range_by_months(start, end)
        else:
            total = len(
                list(
                    iter_range(
                        start,
                        end,
                        cast_timedelta(dataset_overview["max_request_range"]),
                    )
                )
            )
            range_iterator = iter_range(
                start, end, cast_timedelta(dataset_overview["max_request_range"])
            )

        if self.show_progress_bar:
            range_iterator = tqdm(range_iterator, total=total, desc=dataset)

        for cur_start, cur_end in range_iterator:
            self._log(f"Iterating over {cur_start} {cur_end}")
            chunk = self.get_asset_dataset(
                dataset, cur_start, cur_end, tickers=tickers, columns=columns
            )
            total = chunk["total"]

            if total > 0:
                # new chunk
                yield {"type": "values", "data": chunk["values"]}

    def iter_dataset(self, dataset, handler, query=None):
        self._log(f"Iterating through field data: {dataset}")

        for data in self._iter_data(dataset, query=query):
            handler(**data)

    def get_dataset(self, dataset, query=None):
        self._log(f"Getting field data: {dataset}")

        columns = []
        values = []

        def _load_data_handler(type, data):
            if type == "columns":
                columns.extend(data)
            elif type == "values":
                values.extend(data)

        # make requests to load granular_storage
        self.iter_dataset(dataset, _load_data_handler, query=query)

        return pd.DataFrame(values, columns=columns)

    def download_dataset(self, dataset, fn, query=None):
        self._log(f"Downloading field {dataset} data to file {fn}")
        if os.path.exists(fn):
            raise Exception(f"File {fn} already exists")

        writer = PandasCSVWriter(fn)

        def _save_handler(type, data):
            if type == "columns":
                writer.write_header(data)
            elif type == "values":
                writer.write_values(data)

        # make requests to save granular_storage
        self.iter_dataset(dataset, _save_handler, query=query)
        writer.flush()


Client = ClientV0
