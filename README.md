# HTTP Code Lookup

Allows you to very quickly view and search an offline version of the [Wikipedia's HTTP Codes](https://en.wikipedia.org/wiki/List_of_HTTP_status_codes) page.

## What the hell is this?

Look up specific codes

![code lookup](https://i.ibb.co/vBWgJS1/image.png)

Filter using wildcards

![wildcard lookup](https://i.ibb.co/CWZ3ZW1/image.png)

Don't know the status code?

![text lookup](https://i.ibb.co/9TQgxtw/image.png)

## How to Install

```bash
pipx install hhttpcode
```

### Arguments

The usage for the tool is as follows:

```bash
http-code <search_term> --output-as-json --no-pretty --indent-size --no-colour
```

- `<search_term>`
  - **Mandatory**: Can be either a 3 digit code (use x to replace unknowns, eg: 2xx for all codes starting with 2) or a text search.
- `--output-as-json`
  - _Optional_: Output as JSON, by default will pretty-print JSON... use `--no-pretty` to disable
- `--no-pretty`
  - _Optional_: Disable pretty printing of JSON, does nothing without `--output-as-json` flag set
- `--indent-size`
  - _Optional_: Change the default (2) indent size
- `--no-colour`
  - _Optional_: Disable colour for non-JSON output

## How to test

```bash
python tests/test.py
```

## Known Issues

- Tests don't run on Windows systems :|
