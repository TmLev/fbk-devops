import os
import time

import pytest
import requests


@pytest.fixture
def base_url() -> str:
    host = os.environ["HISTORIAN_HOST"]
    port = os.environ["HISTORIAN_PORT"]
    return f"http://{host}:{port}"


@pytest.fixture
def ensure_historian_running(base_url) -> None:
    while True:
        try:
            response = requests.get(base_url)
            assert response.status_code == 404
            break
        except requests.exceptions.ConnectionError:
            print(f'Waiting for "{base_url}" to run...')
            time.sleep(1)


@pytest.fixture
def entry() -> dict[str, str]:
    return {
        "data": "Some interesting entry",
    }


@pytest.mark.usefixtures("ensure_historian_running")
def test_post_entry_writes_to_database(base_url, entry) -> None:
    response = requests.post(f"{base_url}/entries/", json=entry)
    assert response.status_code == 200

    id_ = response.json()["id"]
    response = requests.get(f"{base_url}/__tests/entries/{id_}/")
    assert response.status_code == 200
    assert response.json() == entry
