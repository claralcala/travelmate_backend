# Get official base image
FROM postgres:16.2-alpine

# Run create.sql on init
ADD create.sql /docker-entrypoint-initdb.d
