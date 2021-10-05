# Get the latest version of Pulumi CLI to use in testing the containers
VERSION := $(shell curl --fail --silent -L "https://www.pulumi.com/latest-version")

.PHONY: test_containers
test_containers:
	./scripts/test-containers.sh ${VERSION}
