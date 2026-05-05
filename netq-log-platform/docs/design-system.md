# Design System

## Purpose

This document defines the initial design system direction for `netq-log-platform`.

The goal is to keep the frontend minimal, high-contrast and operationally efficient while giving the new platform a clear visual identity.

## Visual direction

- Inspired by Vercel in clarity and restraint, not as a literal copy
- Minimal layout with strong typography and clean surfaces
- High contrast for long operational sessions
- Low-noise components that prioritize scan speed over decoration

## Foundations

### Typography

- Serif display headlines for emphasis and hierarchy
- Strong sans-serif body text for day-to-day readability
- Monospace labels and metadata for operational cues

### Color

- Warm neutral background
- Dark carbon hero and shell accents
- Green accent reserved for primary action and healthy state
- Red reserved only for error or risk feedback

### Components

- Rounded but sharp-feeling surfaces
- Inputs with clear focus ring and strong border contrast
- Pills, cards and panels for dense operational information
- Primary and secondary actions with clear visual separation

## Interaction principles

- Every state should be readable in a quick glance
- Focus, error and session states must be visually explicit
- Layout should remain usable on desktop and mobile
- XML and other dense payload views should inherit the same high-contrast rules

## Current implementation anchors

- Tokens and component primitives live in `frontend/app/globals.css`
- Login shell expresses the auth entry pattern
- App shell expresses card hierarchy, status pills and operational density
