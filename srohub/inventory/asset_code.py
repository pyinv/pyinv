from re import compile

from django.core.exceptions import ValidationError
from django.conf import settings

import damm32

d32 = damm32.Damm32()

ASSET_CODE_REGEX = compile("^([A-Za-z0-9]{3})-([A-Za-z0-9]{3})-([A-Za-z0-9]{3})$")


def validate_asset_code(value: str):
    """Validate an asset code."""
    match = ASSET_CODE_REGEX.match(value)

    if match:
        groups = match.groups()
        if groups[0] != settings.INVENTORY_ORG:
            raise ValidationError(f"Invalid inventory org, expected {settings.INVENTORY_ORG}")

        e = "".join(groups)
        if not d32.verify("".join(groups).upper()):
            raise ValidationError(f"Invalid asset code check digit. {d32.calculate(e[:8])}")
    else:
        raise ValidationError("Invalid asset code format.")
