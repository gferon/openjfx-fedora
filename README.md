# How to test this specfile without Mock (to debug steps for example)

## Install dependencies
dnf builddep SPECS/openjfx.spec

## Download sources
spectool -g -R SPECS/openjfx.spec
