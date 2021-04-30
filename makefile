stop:
	-docker-compose down --remove-orphans

set-up-env-test: stop
    docker-compose up -d prometheus-server s3proxy

    # Minio setup
    mc config host add minio http://localhost:9000 minio password --api S3v4
    mc cp -r tests/mocks/business_events/ minio/stuart-data/business_events
