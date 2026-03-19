#!/bin/sh
git tag "$1"
git push origin dev:stable
git push origin "$1"