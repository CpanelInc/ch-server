#!/bin/bash

if [ ! -e "ch-server.spec" ]; then
  cd ..;
fi

if [ ! -e "ch-server.spec" ]; then
  echo "This script needs to be run in the directory that ch-server resides in (or one below it)";
  exit 1;
fi

#Note: ! takes precedence over -o, so this is more like !(-e xxx -o -e xxx)
if [ ! -e "~/rpmbuild/SPECS" -a -e "~/rpmbuild/SOURCES" ]; then
  echo "It doesn't look like you have build directories in ~/rpmbuild. Please fix that first and then try this tool again";
  exit 1;
fi

cp ch-server.spec ~/rpmbuild/SPECS
cp ch-server.tar.gz rpm-patches/* ~/rpmbuild/SOURCES
