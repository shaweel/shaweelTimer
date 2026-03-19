#!/bin/sh
cd shaweelTimerGitHub
git tag "$1"
git push origin dev:stable --force
git push origin "$1"
cd ..
cd shaweelTimerAur
makepkg --printsrcinfo > ./.SRCINFO
git add .
git commit -m "$1"
git push origin main
cd ..
cd shaweelTimerAurDev
makepkg --printsrcinfo > ./.SRCINFO
git add .
git commit -m "$1"
git push origin main