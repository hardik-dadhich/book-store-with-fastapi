# -*- mode:makefile; coding:utf-8 -*-
# define the name of the virtual environment directory

SHELL := /bin/sh
VENV_NAME?=venv
PYTHON?=python3
PIP_ARGS?=

# default target, when make executed without arguments
activate::
        @echo "Entering in Virtual Env" \
        source $(ENV_NAME)/bin/activate

.PHONY: all clean-all check-all doc install develop lint mypy hadolint build publish-version publish deactivate