---
doc_id: edge-gateway-architecture
doc_type: architecture
service: edge-gateway
team: platform
last_updated: 2024-06-20
source: synthetic
title: edge-gateway Architecture
---

# edge-gateway Architecture

## Overview

`edge-gateway` is a tier-0 service owned by **platform**.

## Dependencies

checkout-api, auth-service, catalog-api

## Design notes

- Exposes HTTPS APIs behind edge-gateway when customer-facing.
- Emits metrics to metrics-collector.
- Authn/z via auth-service for user-scoped calls.
