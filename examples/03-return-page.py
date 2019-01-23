#
# Example: How to show a return page to the customer.
#
# In this example we retrieve the order stored in the database.
# Here, it's unnecessary to use the Mollie API Client.
#
from __future__ import print_function

from __future__ import absolute_import
import flask

from app import database_read


def main():
    if "my_webshop_id" not in flask.request.args:
        flask.abort(404, "Unknown my_webshop_id")
    data = database_read(flask.request.args["my_webshop_id"])

    body = "<p>Your payment status is '{status}'".format(status=data["status"])
    body += "<p>"
    body += '<a href="/">Back to examples</a><br>'
    body += "</p>"

    return body


if __name__ == "__main__":
    print(main())
