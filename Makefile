.SILENT:
.DEFAULT_GOAL := help

ifneq (,$(wildcard ./.env))
    include .env
endif

##### SELF-DOCUMENTATION #######
.PHONY: help
help:
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

##### UTILITIES #######

.PHONY: init
init:  ## [Does initial configurations]
	- mkdir -p ./dags ./logs ./plugins ./config
	- echo "AIRFLOW_UID=$$(id -u)" > .env
	- docker compose up airflow-init

.PHONY: deep-clean
deep-clean: ## [Destroys containers, images, networks and volumes]
	docker system prune -a -f --volumes

.PHONY: up
up:  ## [Spins the project up]
	docker compose up

.PHONY: lint
lint:  ## [Lints the project]
	black .