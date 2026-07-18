.DEFAULT_GOAL := help

.PHONY: \
	help \
	bootstrap \
	format \
	lint \
	test \
	clean \
	precommit

help:
	@echo "Available targets:"
	@echo "  bootstrap   Install development dependencies"
	@echo "  format      Format source code"
	@echo "  lint        Run static analysis"
	@echo "  test        Run tests"
	@echo "  clean       Remove generated files"
	@echo "  precommit   Run formatting, linting, and tests"

bootstrap:
	@./scripts/bootstrap.sh

format:
	@./scripts/format.sh

lint:
	@./scripts/lint.sh

test:
	@./scripts/test.sh

clean:
	@./scripts/clean.sh

precommit:
	@./scripts/precommit.sh
