#!/bin/bash

echo "Waiting for the DB to start"
sleep 10;

echo "cd to alembic dir."
echo "cd /app/app"
cd /app/app && pwd

echo "Trying to upgrade migrations to head"
alembic upgrade head
