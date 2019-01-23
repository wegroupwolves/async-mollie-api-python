# coding=utf-8
#
# Example: How to prepare a new payment with the Mollie API.
#
from __future__ import print_function

from __future__ import absolute_import
import os
import time

import flask

from app import database_write
from mollie.api.client import Client
from mollie.api.error import Error


def main():
    try:
        #
        # Initialize the Mollie API library with your API key.
        #
        # See: https://www.mollie.com/dashboard/settings/profiles
        #
        api_key = os.environ.get("MOLLIE_API_KEY", "test_test")
        mollie_client = Client()
        mollie_client.set_api_key(api_key)

        #
        # Generate a unique webshop order id for this example. It is important to include this unique attribute
        # in the redirectUrl (below) so a proper return page can be shown to the customer.
        #
        my_webshop_id = int(time.time())

        #
        # Payment parameters:
        # amount        Currency and value. This example creates a € 120,- payment.
        # description   Description of the payment.
        # webhookUrl    Webhook location, used to report when the payment changes state.
        # redirectUrl   Redirect location. The customer will be redirected there after the payment.
        # metadata      Custom metadata that is stored with the payment.
        #
        payment = mollie_client.payments.create(
            {
                "amount": {"currency": "EUR", "value": "120.00"},
                "description": "My first API payment",
                "webhookUrl": "{root}02-webhook_verification".format(
                    root=flask.request.url_root
                ),
                "redirectUrl": "{root}03-return-page?my_webshop_id={id}".format(
                    root=flask.request.url_root, id=my_webshop_id
                ),
                "metadata": {"my_webshop_id": str(my_webshop_id)},
            }
        )

        #
        # In this example we store the order with its payment status in a database.
        #
        data = {"status": payment.status}
        database_write(my_webshop_id, data)

        #
        # Send the customer off to complete the payment.
        #
        return flask.redirect(payment.checkout_url)

    except Error as err:
        return "API call failed: {error}".format(error=err)


if __name__ == "__main__":
    print(main())
