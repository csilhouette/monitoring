stop:
	-docker-compose down --remove-orphans

set-up-env-test: stop
	docker-compose up -d prometheus-server s3proxy

run: set-up-env-test
	python main.py