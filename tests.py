import json
from unittest.mock import patch

import cerberus
import pytest
import requests


def test_random_random_image(base_url):
    with patch('requests.get') as mock_request:
        response = requests.get(base_url + "api/breeds/image/random")

        schema = {
            "message": {"type": "string", "required": True},
            "status": {"type": "string", "required": True}
        }

        mock_request.return_value.status_code = 200
        mock_request.return_value.json.return_value = {
            "message": "https://images.dog.ceo/breeds/pitbull/20190710_143021.jpg",
            "status": "success"
        }

        validate = cerberus.Validator()
        assert response.status_code == 200
        assert validate.validate(response.json(), schema)


def test_multiple_random_image(base_url):
    with patch('requests.get') as mock_request:
        response = requests.get(base_url + "api/breeds/image/random/3")

        schema = {
            "message": {"type": "list",
                        "items": [{"type": "string"}, {"type": "string"}, {"type": "string"}], "required": True},
            "status": {"type": "string", "required": True}
        }

        mock_request.return_value.status_code = 200
        mock_request.return_value.json.return_value = {
            "message": [
                "https://images.dog.ceo/breeds/chow/n02112137_1687.jpg",
                "https://images.dog.ceo/breeds/terrier-toy/n02087046_2957.jpg",
                "https://images.dog.ceo/breeds/mastiff-tibetan/n02108551_7523.jpg"
            ],
            "status": "success"
        }

        validate = cerberus.Validator()
        assert response.status_code == 200
        assert validate.validate(response.json(), schema)


def test_image_by_breed_status(base_url):
    with patch('requests.get') as mock_request:
        response = requests.get(base_url + "api/breed/hound/images")
        mock_request.return_value.status_code = 200
        assert response.status_code == 200


@pytest.mark.parametrize("breed", ["affenpinscher", "african", "akita"])
def test_image_by_breed(base_url, breed):
    with patch('requests.get') as mock_request:
        response = requests.get(base_url + f"api/breed/{breed}/images")

        schema = {
            "message": {"type": ["list", "string"], "required": True},
            "status": {"type": "string", "required": True}
        }

        mock_request.return_value.status_code = 200
        with open("random.json") as f:
            breeds = json.load(f)
            print(breeds["breeds"][0])
            if breed == "affenpinscher":
                mock_request.return_value.json.return_value = breeds["breeds"][0]

            if breed == "african":
                mock_request.return_value.json.return_value = breeds["breeds"][1]

            if breed == "akita":
                mock_request.return_value.json.return_value = breeds["breeds"][2]

        validate = cerberus.Validator()
        assert response.status_code == 200
        assert validate.validate(response.json(), schema)


@pytest.mark.parametrize("breed", ["affenpinscher", "african", "akita"])
def test_image_by_breed(base_url, breed):
    with patch('requests.get') as mock_request:
        response = requests.get(base_url + f"api/breed/{breed}/images/random")

        schema = {
            "message": {"type": ["list", "string"], "regex": r".*\.jpg", "required": True},
            "status": {"type": "string", "required": True}
        }

        mock_request.return_value.status_code = 200
        with open("images.json") as f:
            breeds = json.load(f)
            if breed == "affenpinscher":
                mock_request.return_value.json.return_value = breeds["image"][0]

            if breed == "african":
                mock_request.return_value.json.return_value = breeds["image"][1]

            if breed == "akita":
                mock_request.return_value.json.return_value = breeds["image"][2]

        validate = cerberus.Validator()
        assert response.status_code == 200
        assert validate.validate(response.json(), schema)
