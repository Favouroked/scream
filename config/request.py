import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

retry_strategy = Retry(total=5,
                       backoff_factor=0.1,
                       status_forcelist=[500, 502, 503, 504])


def get_retry_request():
    adapter = HTTPAdapter(max_retries=retry_strategy)
    http = requests.Session()
    http.mount('https://', adapter)
    http.mount('http://', adapter)
    return http
