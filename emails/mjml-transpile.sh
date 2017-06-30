#!/usr/bin/env bash
find . -type f -name '*.html' -delete
for d in */ ; do
    ls $d *.mjml
    cd $d
    mjml *.mjml
    cd ..
done