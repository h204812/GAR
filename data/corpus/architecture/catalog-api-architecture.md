---
doc_id: catalog-api-architecture
doc_type: architecture
service: catalog-api
team: inventory
last_updated: 2024-06-20
source: synthetic
title: catalog-api Architecture
---

# catalog-api Architecture

## Overview

`catalog-api` is a tier-2 service owned by **inventory**.

## Dependencies

inventory-db

## Design notes

- Exposes HTTPS APIs behind edge-gateway when customer-facing.
- Emits metrics to metrics-collector.
- Authn/z via auth-service for user-scoped calls.
