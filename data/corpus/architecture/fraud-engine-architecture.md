---
doc_id: fraud-engine-architecture
doc_type: architecture
service: fraud-engine
team: payments
last_updated: 2024-06-20
source: synthetic
title: fraud-engine Architecture
---

# fraud-engine Architecture

## Overview

`fraud-engine` is a tier-1 service owned by **payments**.

## Dependencies

payments-ledger

## Design notes

- Exposes HTTPS APIs behind edge-gateway when customer-facing.
- Emits metrics to metrics-collector.
- Authn/z via auth-service for user-scoped calls.
