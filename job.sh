#!/bin/bash

DIR_PATH=$(dirname "$0")

source "$DIR_PATH/.env"

START=$(date +"%T")
echo "Starting esselunga command at $START"

esselunga

END=$(date +"%T")
echo "Ending at $END"