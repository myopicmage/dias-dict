import json
import logging
from pprint import pprint
import requests

logger = logging.getLogger(__name__)

from discord_dict.api_response import word_from_dict


def get_definition(word: str) -> str:
    r = requests.get(f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}")

    try:
        word_response = word_from_dict(json.loads(r.text))

        definitions = []
        for idx, d in enumerate(word_response[0].meanings[0].definitions):
            definitions.append(f"{idx + 1}: {d.definition}")

        return "\n".join(definitions)
    except Exception as err:
        logger.exception(err)

        pprint(r.json())

        return "Whoops, something went wrong."
