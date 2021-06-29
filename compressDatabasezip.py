#!/usr/bin/env bash

## This script compresses the database directory to a zip file 


zip -qr database.zip database/ -x database/olddata/*

