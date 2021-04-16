SHELL := $(shell which bash)
.SHELLFLAGS := -xeEuo pipefail -c
.ONESHELL:

export BUILDKIT_PROGRESS=plain
export DOCKER_BUILDKIT=1

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
	./.dapper -m bind $@
	@[[ -d out-replace ]] && cp -a out-replace/. ./

.DEFAULT_GOAL := ci

.PHONY: $(TARGETS) $(IN_PLACE_TARGETS)

burn:
	[[ -e /dev/mmcblk0 ]] || exit 1
	sudo dd if=out/sdcard.img of=/dev/mmcblk0 bs=4K status=progress
