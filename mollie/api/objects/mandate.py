from .base import Base


class Mandate(Base):
    @classmethod
    def get_resource_class(cls, client):
        from ..resources.customer_mandates import CustomerMandates

        return CustomerMandates(client)

    STATUS_PENDING = "pending"
    STATUS_VALID = "valid"
    STATUS_INVALID = "invalid"

    @property
    def id(self):
        return self._get_property("id")

    @property
    def resource(self):
        return self._get_property("resource")

    @property
    def status(self):
        return self._get_property("status")

    @property
    def method(self):
        return self._get_property("method")

    @property
    def details(self):
        return self._get_property("details")

    @property
    def mandate_reference(self):
        return self._get_property("mandateReference")

    @property
    def signature_date(self):
        return self._get_property("signatureDate")

    @property
    def created_at(self):
        return self._get_property("createdAt")

    def is_pending(self):
        """Check if the mandate is pending."""
        return self.status == self.STATUS_PENDING

    def is_valid(self):
        """Check if the mandate is valid."""
        return self.status == self.STATUS_VALID

    def is_invalid(self):
        """Check if the mandate is invalid."""
        return self.status == self.STATUS_INVALID

    async def get_customer(self):
        """Return the customer for this mandate."""
        from .customer import Customer  # work around circular imports

        url = self._get_link("customer")
        if url:
            resp = await self._resource.perform_api_call(self._resource.REST_READ, url)
            return Customer(resp)
