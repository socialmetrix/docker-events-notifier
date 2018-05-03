#!/bin/bash

IMAGE=socialmetrix/docker-events-notifier
VERSION=$(git describe --exact-match --tags HEAD 2>/dev/null)
if [[ $? -ne 0 ]]; then
  echo "Current commit doesn't have a release tag. Won't build."
  echo "Please check: https://git-scm.com/book/en/v2/Git-Basics-Tagging"
  exit 1
fi

echo "Building ${IMAGE}:${VERSION}"
docker build --build-arg BUILD_VERSION=${VERSION} -t ${IMAGE}:${VERSION} .

echo "Pushing ${IMAGE}:${VERSION}"
docker push ${IMAGE}:${VERSION}
