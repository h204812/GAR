---
doc_id: notification-svc-architecture
doc_type: architecture
service: notification-svc
team: notifications
last_updated: 2024-06-20
source: synthetic
title: notification-svc Architecture
---

# notification-svc Architecture

## Overview

`notification-svc` is a tier-1 service owned by **notifications**.

## Dependencies

redis-notif

## Design notes

- Exposes HTTPS APIs behind edge-gateway when customer-facing.
- Emits metrics to metrics-collector.
- Authn/z via auth-service for user-scoped calls.
