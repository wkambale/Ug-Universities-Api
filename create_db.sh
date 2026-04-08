#!/bin/bash
set -e

export PROJECT_ID="ug-universities-api"
export REGION="africa-south1"

gcloud sql instances create ug-universities-db \
  --database-version=POSTGRES_15 \
  --tier=db-f1-micro \
  --region=$REGION \
  --storage-type=SSD \
  --storage-size=10GB \
  --backup-start-time=02:00
