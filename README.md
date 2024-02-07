# HTTP Code Lookup
Allows you to very quickly view and search [Wikipedia's HTTP Codes](https://en.wikipedia.org/wiki/List_of_HTTP_status_codes) page.

## What the hell is this?
Look up specific codes

![code lookup](https://i.ibb.co/vBWgJS1/image.png)

Filter using wildcards

![wildcard lookup](https://i.ibb.co/CWZ3ZW1/image.png)

Don't know the status code?

![text lookup](https://i.ibb.co/9TQgxtw/image.png)


## How to run
Install `requirements.txt` using `pip install -r requirements.txt`. Although not required, setting up a [`virtualenv`](https://www.freecodecamp.org/news/how-to-setup-virtual-environments-in-python/) is advised.

### Using Python
```bash
python main.py <search_term>
```

### Using alias/DOSKEY
Setting up an alias for the script will allow you to use a custom, short "name" for any action.

For Unix systems place the following into `.bashrc` or `.zshrc`
```bash
alias http-code="path/to/python /path/to/main.py $@"
```

For Windows place the following into your bat file that runs on terminal startup. If you do not know how to set this up, look into [this answer on Stack Overflow](https://superuser.com/questions/1749663/add-launch-commands-to-command-prompt-in-windows-terminal)
```bat
DOSKEY http-code="path/to/python /path/to/main.py" $*
```


### Arguments
The usage for the tool is as follows:
```bash
python main.py <search_term> --output-as-json --no-pretty --indent-size --no-colour
```
* `<search_term>`
  * **Mandatory**: Can be either a 3 digit code (use x to replace unknowns, eg: 2xx for all codes starting with 2) or a text search.
* `--output-as-json`
  * _Optional_: Output as JSON, by default will pretty-print JSON... use `--no-pretty` to disable
* `--no-pretty`
  * _Optional_: Disable pretty printing of JSON, does nothing without `--output-as-json` flag set
* `--indent-size`
  * _Optional_: Change the default (2) indent size
* `--no-colour`
  * _Optional_: Disable colour for non-JSON output


## How to test
```bash
python tests/test.py
```

## Known Issues
* Tests don't run on Windows systems :|
