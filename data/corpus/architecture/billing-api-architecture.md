---
doc_id: billing-api-architecture
doc_type: architecture
service: billing-api
team: finance
last_updated: 2024-06-20
source: synthetic
title: billing-api Architecture
---

# billing-api Architecture

## Overview

`billing-api` is a tier-1 service owned by **finance**.

## Dependencies

payments-ledger

## Design notes

- Exposes HTTPS APIs behind edge-gateway when customer-facing.
- Emits metrics to metrics-collector.
- Authn/z via auth-service for user-scoped calls.
