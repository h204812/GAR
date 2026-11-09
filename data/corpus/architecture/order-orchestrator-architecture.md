---
doc_id: order-orchestrator-architecture
doc_type: architecture
service: order-orchestrator
team: checkout
last_updated: 2024-06-20
source: synthetic
title: order-orchestrator Architecture
---

# order-orchestrator Architecture

## Overview

`order-orchestrator` is a tier-1 service owned by **checkout**.

## Dependencies

checkout-api, inventory-api

## Design notes

- Exposes HTTPS APIs behind edge-gateway when customer-facing.
- Emits metrics to metrics-collector.
- Authn/z via auth-service for user-scoped calls.
