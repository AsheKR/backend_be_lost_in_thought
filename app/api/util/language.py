from typing import Annotated, Tuple

import re

from core.language import SupportLanguage
from fastapi import Header


class AcceptLanguageHeader:
    ACCEPT_LANGUAGE_RE = re.compile(
        r"""
            # "en", "en-au", "x-y-z", "es-419", "*"
            ([A-Za-z]{1,8}(?:-[A-Za-z0-9]{1,8})*|\*)
            # Optional "q=1.00", "q=0.8"
            (?:\s*;\s*q=(0(?:\.[0-9]{,3})?|1(?:\.0{,3})?))?
            # Multiple accepts per header.
            (?:\s*,\s*|$)
        """,
        re.VERBOSE,
    )
    LANGUAGE_CODE_RE = re.compile(r"^[a-z]{1,8}(?:-[a-z0-9]{1,8})*(?:@[a-z0-9]{1,20})?$", re.IGNORECASE)

    def __call__(self, accept_language: Annotated[str | None, Header()] = None) -> SupportLanguage:
        if not accept_language:
            return SupportLanguage.fallback

        return self._get_language_code_from_accept_language_string(
            accept_language_string=accept_language,
            default=SupportLanguage.fallback,
        )

    def _get_language_code_from_accept_language_string(
        self, accept_language_string: str, default: SupportLanguage
    ) -> SupportLanguage:
        language_code_re = re.compile(r"^[a-z]{1,8}(?:-[a-z0-9]{1,8})*(?:@[a-z0-9]{1,20})?$", re.IGNORECASE)
        for language_string, priority in self._parse_accept_language_string(accept_language_string):
            if language_string == "*":
                return default

            if not language_code_re.search(language_string):
                continue

            return self._get_supported_language_variant(language_string, default=default)

        return default

    @staticmethod
    def _get_supported_language_variant(language_string: str, default: SupportLanguage) -> SupportLanguage:
        try:
            return SupportLanguage[language_string]
        except KeyError:
            pass

        if language_string:
            generic_language_string = language_string.split("-")[0]
            try:
                return SupportLanguage[generic_language_string]
            except KeyError:
                pass

        return default

    @classmethod
    def _parse_accept_language_string(cls, accept_language_string: str) -> list[Tuple[str, float]]:
        result = []
        pieces = cls.ACCEPT_LANGUAGE_RE.split(accept_language_string.lower())
        if pieces[-1]:
            return []
        for i in range(0, len(pieces) - 1, 3):
            first, lang, priority = pieces[i : i + 3]
            if first:
                return []
            if priority:
                priority = float(priority)
            else:
                priority = 1.0
            result.append((lang, priority))
        result.sort(key=lambda k: k[1], reverse=True)
        return result
