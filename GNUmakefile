SHELL := $(shell which bash)
.SHELLFLAGS := -xeEuo pipefail -c
.ONESHELL:

TARGETS := $(shell ls scripts)
IN_PLACE_TARGETS := $(shell echo scripts/.* | sed 's#scripts/\.*##g')

.dapper:
	@echo Downloading dapper
	@curl -sL https://releases.rancher.com/dapper/latest/dapper-$$(uname -s)-$$(uname -m) > .dapper.tmp
	@@chmod +x .dapper.tmp
	@./.dapper.tmp -v
	@mv .dapper.tmp .dapper

$(TARGETS): .dapper
	@[[ -d out-replace ]] && rm -rf out-replace
	./.dapper $@
	@[[ -d out-replace ]] && cp -a out-replace/. ./

.DEFAULT_GOAL := ci

.PHONY: $(TARGETS) $(IN_PLACE_TARGETS)

