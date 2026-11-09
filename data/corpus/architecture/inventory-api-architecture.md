---
doc_id: inventory-api-architecture
doc_type: architecture
service: inventory-api
team: inventory
last_updated: 2024-06-20
source: synthetic
title: inventory-api Architecture
---

# inventory-api Architecture

## Overview

`inventory-api` is a tier-1 service owned by **inventory**.

## Dependencies

inventory-db

## Design notes

- Exposes HTTPS APIs behind edge-gateway when customer-facing.
- Emits metrics to metrics-collector.
- Authn/z via auth-service for user-scoped calls.
