.PHONY: install validate run-baseline docker-build docker-run

install:
	pip install -r requirements.txt

validate:
	openenv validate

run-baseline:
	python inference.py

docker-build:
	docker build -t smarthome-env .

docker-run:
	docker run -p 7860:7860 smarthome-env
