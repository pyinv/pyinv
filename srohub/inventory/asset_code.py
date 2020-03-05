from random import choice
from re import compile

from django.core.exceptions import ValidationError
from django.conf import settings

import damm32

d32 = damm32.Damm32()

ASSET_CODE_REGEX = compile("^([A-Za-z0-9]{3})-([A-Za-z0-9]{3})-([A-Za-z0-9]{3})$")


def validate_asset_code(value: str) -> None:
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


def generate_asset_code() -> str:

    code = settings.INVENTORY_ORG

    for _ in range(5):
        code += choice(damm32.Damm32.ALPHABET)

    code += d32.calculate(code)

    return f"{code[:3]}-{code[3:6]}-{code[6:9]}"
