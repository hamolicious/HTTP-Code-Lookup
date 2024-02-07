import json
import os
from fire import Fire
import colorama
import re


class Config:
    no_color: bool = False


def _colour_print(color: str, *args, **kwargs) -> None:
    reset = colorama.Style.RESET_ALL
    if Config.no_color:
        reset = ""
        color = ""

    print(color, " ".join(args) + reset, **kwargs)


def _fussy_compare(actual: str, compare: str) -> bool:
    for char_a, char_b in zip(list(str(actual)), list(str(compare))):
        if (char_a != "x" and char_b != "x") and char_a != char_b:
            return False

    return True


def _load_data() -> dict:
    cwd = __file__.removesuffix(os.path.basename(__file__))
    with open(os.path.join(cwd, "codes.json"), "rb") as f:
        return json.load(f)


def _get_subset(code: str, data: dict) -> dict:
    if code.startswith("x"):
        subset = []
        for key in data:
            subset += data.get(key)

        return subset

    elif _fussy_compare(code, "1xx"):
        return data.get("info")

    elif _fussy_compare(code, "2xx"):
        return data.get("success")

    elif _fussy_compare(code, "3xx"):
        return data.get("redirect")

    elif _fussy_compare(code, "4xx"):
        return data.get("client-errors")

    elif _fussy_compare(code, "5xx"):
        return data.get("server-errors")


def _get_color(code: str) -> dict:
    if Config.no_color:
        return ""

    if _fussy_compare(code, "1xx"):
        return colorama.Fore.LIGHTBLUE_EX

    elif _fussy_compare(code, "2xx"):
        return colorama.Fore.LIGHTGREEN_EX

    elif _fussy_compare(code, "3xx"):
        return colorama.Fore.LIGHTMAGENTA_EX

    elif _fussy_compare(code, "4xx"):
        return colorama.Fore.LIGHTRED_EX

    elif _fussy_compare(code, "5xx"):
        return colorama.Fore.LIGHTYELLOW_EX


def _check_if_code(term: str) -> bool:
    return any(
        [
            re.match(r"[\d+|x+]{3,}", term) is not None,
            term.strip() == "x",
        ]
    )


def _search_by_code(code: str) -> None:
    plagiarised_wikipedia_data = _load_data()
    subset: list[dict] = _get_subset(code, plagiarised_wikipedia_data)
    search_results: list[dict] = []

    for entry in subset:
        if _fussy_compare(code, entry.get("code")):
            search_results.append(entry)

    return search_results


def _search_by_text(text: str) -> None:
    data = _load_data()
    subset: list[dict] = _get_subset("xxx", data)
    search_results: list[dict] = []

    for entry in subset:
        if (
            text.lower() in entry.get("message", "").lower()
            or text.lower() in entry.get("desc", "").lower()
        ):
            search_results.append(entry)

    return search_results


def _display_data(search_term: str, results: list[dict]) -> None:
    _colour_print("🔍", f'Results for "{search_term}"')
    _colour_print(colorama.Fore.CYAN, "-" * 50)

    for entry in results:
        color = _get_color(entry.get("code"))
        _colour_print(
            color + colorama.Style.BRIGHT,
            f'{entry.get("code")} - {entry.get("message")}',
        )
        _colour_print(color, entry.get("desc"))
        print()


def _search(search_term: str) -> None:
    search_term = str(search_term)
    is_code = _check_if_code(search_term)
    if is_code:
        data = _search_by_code(search_term)
    else:
        data = _search_by_text(search_term)

    return data


def main(
    search_term: str,
    output_as_json: bool = False,
    no_pretty: bool = False,
    indent_size: int = 2,
    no_colour: bool = False,
) -> str | None:
    """Look up and search HTTP codes

    Args:
        search_term (str): 3-digit status code (use `x` as a wildcard) or text to be searched.
        output_as_json (bool, optional): Output search results as JSON. Defaults to False.
        no_pretty (bool, optional): Don't pretty print JSON, does nothing without `--output-as-json`. Defaults to False.
        indent_size (int, optional): Indent size, does nothing without `--no-pretty`. Defaults to 2.
        no_colour (bool, optional): Don't use colour, , does nothing if `--output-as-json` is set. Defaults to False.

    Returns:
        str | None: Prints or returns search results
    """
    if no_colour:
        Config.no_color = True

    filtered_plagiarised_wikipedia_data = _search(search_term)

    if output_as_json:
        return json.dumps(
            filtered_plagiarised_wikipedia_data,
            indent=None if no_pretty else indent_size,
        )
    _display_data(search_term, filtered_plagiarised_wikipedia_data)

    return


if __name__ == "__main__":
    app = Fire(main)
