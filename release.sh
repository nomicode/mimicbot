#!/bin/sh -e

if git status -s > /dev/null; then
    echo "unsaved changes"
    exit 1
fi

git fetch origin > /dev/null

version=`python setup.py --version`

if git tag | grep $version > /dev/null; then
    echo "tag exists"
    exit 1
fi

# build and upload
rm -f dist/*
python setup.py sdist bdist_wheel --universal
twine upload dist/*

# tag release
git tag -a "$version" -m "tagging $version"
git push --tags
