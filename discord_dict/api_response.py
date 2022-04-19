# To use this code, make sure you
#
#     import json
#
# and then, to convert JSON from a string, do
#
#     result = welcome_from_dict(json.loads(json_string))
from typing import Any, List, Optional, TypeVar, Callable, Type, cast


T = TypeVar("T")


def from_str(x: Any) -> str:
    assert isinstance(x, str)
    return x


def from_list(f: Callable[[Any], T], x: Any) -> List[T]:
    assert isinstance(x, list)
    return [f(y) for y in x]


def to_class(c: Type[T], x: Any) -> dict:
    assert isinstance(x, c)
    return cast(Any, x).to_dict()


class License:
    name: str
    url: str

    def __init__(self, name: str, url: str) -> None:
        self.name = name
        self.url = url

    @staticmethod
    def from_dict(obj: Any) -> Optional["License"]:
        if not isinstance(obj, dict):
            return None

        name = from_str(obj.get("name"))
        url = from_str(obj.get("url"))
        return License(name, url)

    def to_dict(self) -> dict:
        result: dict = {}
        result["name"] = from_str(self.name)
        result["url"] = from_str(self.url)
        return result


class Definition:
    antonyms: List[Any]
    definition: str
    synonyms: List[Any]

    def __init__(
        self, antonyms: List[Any], definition: str, synonyms: List[Any]
    ) -> None:
        self.antonyms = antonyms
        self.definition = definition
        self.synonyms = synonyms

    @staticmethod
    def from_dict(obj: Any) -> "Definition":
        assert isinstance(obj, dict)
        antonyms = from_list(lambda x: x, obj.get("antonyms"))
        definition = from_str(obj.get("definition"))
        synonyms = from_list(lambda x: x, obj.get("synonyms"))
        return Definition(antonyms, definition, synonyms)

    def to_dict(self) -> dict:
        result: dict = {}
        result["antonyms"] = from_list(lambda x: x, self.antonyms)
        result["definition"] = from_str(self.definition)
        result["synonyms"] = from_list(lambda x: x, self.synonyms)
        return result


class Meaning:
    antonyms: List[str]
    definitions: List[Definition]
    part_of_speech: str
    synonyms: List[str]

    def __init__(
        self,
        antonyms: List[str],
        definitions: List[Definition],
        part_of_speech: str,
        synonyms: List[str],
    ) -> None:
        self.antonyms = antonyms
        self.definitions = definitions
        self.part_of_speech = part_of_speech
        self.synonyms = synonyms

    @staticmethod
    def from_dict(obj: Any) -> "Meaning":
        assert isinstance(obj, dict)
        antonyms = from_list(from_str, obj.get("antonyms"))
        definitions = from_list(Definition.from_dict, obj.get("definitions"))
        part_of_speech = from_str(obj.get("partOfSpeech"))
        synonyms = from_list(from_str, obj.get("synonyms"))
        return Meaning(antonyms, definitions, part_of_speech, synonyms)

    def to_dict(self) -> dict:
        result: dict = {}
        result["antonyms"] = from_list(from_str, self.antonyms)
        result["definitions"] = from_list(
            lambda x: to_class(Definition, x), self.definitions
        )
        result["partOfSpeech"] = from_str(self.part_of_speech)
        result["synonyms"] = from_list(from_str, self.synonyms)
        return result


class Phonetic:
    audio: str
    license: Optional[License]
    source_url: str
    text: str

    def __init__(
        self, audio: str, license: Optional[License], source_url: str, text: str
    ) -> None:
        self.audio = audio
        self.license = license
        self.source_url = source_url
        self.text = text

    @staticmethod
    def from_dict(obj: Any) -> "Phonetic":
        assert isinstance(obj, dict)

        audio = from_str(obj.get("audio"))
        license = License.from_dict(obj.get("license"))

        source_url = ""
        if "sourceUrl" in obj:
            source_url = from_str(obj.get("sourceUrl"))

        text = ""
        if "text" in obj:
            text = from_str(obj.get("text"))

        return Phonetic(audio, license, source_url, text)

    def to_dict(self) -> dict:
        result: dict = {}
        result["audio"] = from_str(self.audio)
        result["license"] = to_class(License, self.license)
        result["sourceUrl"] = from_str(self.source_url)
        result["text"] = from_str(self.text)
        return result


class Word:
    license: Optional[License]
    meanings: List[Meaning]
    phonetic: str = ""
    phonetics: Optional[List[Phonetic]] = []
    source_urls: List[str]
    word: str

    def __init__(
        self,
        license: Optional[License],
        meanings: List[Meaning],
        phonetic: str = "",
        phonetics: Optional[List[Phonetic]] = None,
        source_urls: List[str] = [],
        word: str = "",
    ) -> None:
        self.license = license
        self.meanings = meanings
        self.phonetic = phonetic
        self.phonetics = phonetics
        self.source_urls = source_urls
        self.word = word

    @staticmethod
    def from_dict(obj: Any) -> "Word":
        assert isinstance(obj, dict)
        license = License.from_dict(obj.get("license"))
        meanings = from_list(Meaning.from_dict, obj.get("meanings"))

        phonetic = ""
        if "phonetic" in obj:
            phonetic = from_str(obj.get("phonetic"))

        phonetics = None
        if "phonetics" in obj:
            phonetics = from_list(Phonetic.from_dict, obj.get("phonetics"))

        source_urls = from_list(from_str, obj.get("sourceUrls"))
        word = from_str(obj.get("word"))

        return Word(license, meanings, phonetic, phonetics, source_urls, word)

    def to_dict(self) -> dict:
        result: dict = {}
        result["license"] = to_class(License, self.license)
        result["meanings"] = from_list(lambda x: to_class(Meaning, x), self.meanings)
        result["phonetic"] = from_str(self.phonetic)
        result["phonetics"] = from_list(lambda x: to_class(Phonetic, x), self.phonetics)
        result["sourceUrls"] = from_list(from_str, self.source_urls)
        result["word"] = from_str(self.word)
        return result


def word_from_dict(s: Any) -> List[Word]:
    return from_list(Word.from_dict, s)
