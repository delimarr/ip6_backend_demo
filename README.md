# ip6_ebl_coords
This repository contains an interface to GoT, coordinates recording and analysis.

# setup poetry and pre-commit hook in local venv
- run `poetry install`
- run `poetry shell`
- select newly created env from poetry as python interpreter
- if you are on linux run `git config --global --add safe.directory /workdir`
- run `pre-commit install`

# start poetry shell in docker terminal
- run `poetry install`

# vsc does not show poetry env
https://stackoverflow.com/questions/59882884/vscode-doesnt-show-poetry-virtualenvs-in-select-interpreter-option

# start flask REST APi
- run `flask --app ebl_coords.main run --host=0.0.0.0`
