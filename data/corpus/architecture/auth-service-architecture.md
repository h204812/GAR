---
doc_id: auth-service-architecture
doc_type: architecture
service: auth-service
team: identity
last_updated: 2024-06-20
source: synthetic
title: auth-service Architecture
---

# auth-service Architecture

## Overview

`auth-service` is a tier-0 service owned by **identity**.

## Dependencies

identity-db, redis-sessions

## Design notes

- Exposes HTTPS APIs behind edge-gateway when customer-facing.
- Emits metrics to metrics-collector.
- Authn/z via auth-service for user-scoped calls.
