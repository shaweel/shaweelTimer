#!/bin/sh
git tag "$1"
git push origin dev:stable --force
git push origin "$1"