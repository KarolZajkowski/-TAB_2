"""
Sprawdzenie poprawności działania API:
Należy utworzyć testy automatyczne fragmentu API.
Testy należy utworzyć dla żądania:

1. POST /v1/payment (dodanie nowej płatności) z losowymi danymi (np. losowe userId -
format: UUID)
2. POST /v1/payment z niepoprawnym formatem wybranego pola lub pól (można
skorzystać np. z parametryzacji testów)
3. weryfikacja poprawności dodania pozycji z punktu 1 poprzez jej pobranie żądaniem:
GET /v1/payment/{id}.
4. Test usunięcia stworzonego zasobu DELETE /v1/payment/{id}
Definicja API znajduję się w osobnym pliku.
Plik można wyświetlić w formie przyjaznej użytkownikowi używając strony
https://editor.swagger.io (zawartość pliku należy wkleić w lewym panelu).
"""

import pdb
import json
import requests
import schemathesis
from pathlib import Path
from urllib.parse import urljoin


TESTING_API = '.'
schema = schemathesis.from_path(
    Path(__file__).parent / "definicjaAPI.txt"
)


class ServerError(Exception):
    """ 500 occurred """
    def __init__(self, text, area):
        super().__init__(text)
        self.area = area

    def __str__(self):
        return "server issue occurred: {} {}".format(super().__str__(), self.area)


class Payment(object):
    version = '1.0'

    def __init__(self, backend=None):
        self.backend = backend
        self._payments = []

    def payment_post(self, endpoint, headers, data):
        if not endpoint:
            return None  # no post method endpoint
        url = urljoin(TESTING_API, endpoint)
        resp = requests.post(url, headers, data)

        if resp.status_code == 200:
            if self.backend:
                self.backend.write(json.dumps(resp.json()))
                # self.payment(resp.json())
        # if resp.status_code == 400:
        #     try:
        #         resp_code_user_id = resp.json()['userId']
        #         UUID(resp_code_user_id, version=4)
        #     except ValueError:
        #         return "No valid data"
        #
        # elif resp.status_code == 500:
        #     raise ServerError("No data")

        return resp

    def payment_get(self, endpoint):
        if not endpoint:
            return None  # no post method endpoint
        url = urljoin(TESTING_API, endpoint)
        resp = requests.post(url)  # no body in this step

        return resp

    def payment_delete(self, endpoint):
        if not endpoint:
            return None  # no post method endpoint
        url = urljoin(TESTING_API, endpoint)
        resp = requests.delete(url)

        return resp

    @property
    def payments(self):
        if self.backend and not self._payments:
            beckend_text = self.backend.read()
            if beckend_text:
                self._payments = json.loads(beckend_text)
            return self._payments

    def payment(self, response):
        self.payments.append(response)
        if self.backend:
            self.backend.write(json.dumps(self.payments))