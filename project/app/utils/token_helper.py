from typing import Any, Dict, Union

from jwt import (
    DecodeError,
    ExpiredSignatureError,
    InvalidSignatureError,
    decode,
    encode,
)

from app import app_config


def encode_token(token_info: Dict[str, Any]) -> str:
    """
    Encode a token passed by parameter
    :param token_info: token information to encode
    :return: generated token
    :rtype: str
    """
    return encode(token_info, app_config.token_secret_key, algorithm="HS256")


def decode_token(token: str) -> Union[Dict, None]:
    """
    Decode a token passed by parameter
    :param token: token to decode
    :return: payload of the token
    :rtype: Union[Dict, None]
    """
    try:
        return decode(token, app_config.token_secret_key, algorithms="HS256")
    except (InvalidSignatureError, DecodeError, ExpiredSignatureError):
        # Exceptions raises by jwt
        return None
