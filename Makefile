.PHONY: pipreqs
pipreqs:
	pipreqs /Users/winston/Development/keyword-registry-server --force

.PHONY: install
install:
	pip install -r requirements.txt

.PHONY: local-compose
local-compose:
	docker compose up

.PHONY: dev
dev:
	fastapi dev main.py