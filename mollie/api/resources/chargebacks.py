from ..error import IdentifierError
from ..objects.chargeback import Chargeback
from .base import Base


class Chargebacks(Base):
    RESOURCE_ID_PREFIX = "chb_"

    def get_resource_object(self, result):
        return Chargeback(result)

    async def get(self, chargeback_id, **params):
        """Verify the chargeback ID and retrieve the chargeback from the API."""
        if not chargeback_id or not chargeback_id.startswith(self.RESOURCE_ID_PREFIX):
            raise IdentifierError(
                "Invalid chargeback ID: '{id}'. A chargeback ID should start with '{prefix}'.".format(
                    id=chargeback_id, prefix=self.RESOURCE_ID_PREFIX
                )
            )
        result = await super(Chargebacks, self).get(chargeback_id, **params)
        return result
