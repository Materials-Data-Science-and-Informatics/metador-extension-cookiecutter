#!/usr/bin/env bash
# Finalization of project template

# create gitlab issue templates by stripping metadata from GH issue templates
for file in .github/ISSUE_TEMPLATE/*; do
    cat $file | awk -v x=0 '
    {
        if ( x > 1 )
            { print }
        if ( $1 ~ /^---/)
            { x++; }
    }' > .gitlab/issue_templates/$(basename $file)
done

# ----
# remove unneeded demo code (will only keep metador extension example code)
rm src/{{ cookiecutter.__project_package }}/cli.py
rm tests/test_cli.py
rm src/{{ cookiecutter.__project_package }}/api.py
rm tests/test_api.py
# ----


# finalize repo setup
git init
poetry install --with docs
poetry run poe init-dev  # init git repo + register pre-commit
poetry run pip install pipx  # install pipx into venv without adding it as dep
poetry run pipx run reuse download --all  # get license files for REUSE compliance

# ----
# if we use somesy, CITATION.cff + codemeta.json is created automatically
rm CITATION.cff  # using somesy -> will be created from pyproject.toml
if [ -f "CITATION.cff" ]; then
    # not using somesy -> create a minimal codemeta.json based on the CITATION.cff
    # (avoiding the buggy codemetapy pyproject.toml parsing)
    pipx run cffconvert -i CITATION.cff -f codemeta -o codemeta.json
fi
# ----
# use somesy to create CITATION.cff + codemeta.json
poetry run poe lint somesy --files pyproject.toml

# create first commit
git add .
poetry run git commit \
    -m "generated project using metador-extension-cookiecutter" \
    -m "https://github.com/Materials-Data-Science-and-Informatics/metador-extension-cookiecutter"

# make sure that the default branch is called 'main'
git branch -M main

# exit 0  # <- uncomment for debugging (keep output dir even in case of errors)
