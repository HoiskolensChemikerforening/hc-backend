#!/usr/bin/env bash

# Set PATH to include the Node.js binary directory managed by nvm
# Uncomment and update the path to your node installation if npm cannot be found
# export PATH="/home/paulj/.nvm/versions/node/v21.6.1/bin:$PATH"

find . -type f -name '*.html' -delete

for d in */ ; do
    cd "$d"
    for mjml_file in *.mjml; do
        html_file="${mjml_file%.mjml}.html"
        mjml "$mjml_file" --output "$html_file"
    done

    cd ..
done


