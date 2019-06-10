#!/bin/sh
su -m app -c "celery -A tasks worker --loglevel INFO"  