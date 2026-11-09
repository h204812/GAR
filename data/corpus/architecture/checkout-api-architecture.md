---
doc_id: checkout-api-architecture
doc_type: architecture
service: checkout-api
team: checkout
last_updated: 2024-06-20
source: synthetic
title: checkout-api Architecture
---

# checkout-api Architecture

## Overview

`checkout-api` is a tier-0 service owned by **checkout**.

## Dependencies

payments-ledger, auth-service, inventory-api, notification-svc

## Design notes

- Exposes HTTPS APIs behind edge-gateway when customer-facing.
- Emits metrics to metrics-collector.
- Authn/z via auth-service for user-scoped calls.
