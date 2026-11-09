---
doc_id: payments-ledger-architecture
doc_type: architecture
service: payments-ledger
team: payments
last_updated: 2024-06-20
source: synthetic
title: payments-ledger Architecture
---

# payments-ledger Architecture

## Overview

`payments-ledger` is a tier-0 service owned by **payments**.

## Dependencies

auth-service, payments-db

## Design notes

- Exposes HTTPS APIs behind edge-gateway when customer-facing.
- Emits metrics to metrics-collector.
- Authn/z via auth-service for user-scoped calls.
