# Kubernetes Base Manifests

This folder contains the initial Kubernetes manifests for `netq-log-platform`.

## Current shape

- One `Deployment`
- One pod per replica
- Two containers in the same pod:
  - `backend` on port `8000`
  - `frontend` on port `3000`
- `Service` exposes only the frontend
- `Ingress` points to the frontend `Service`

## Apply

```bash
kubectl apply -k netq-log-platform/k8s/base
```

## Important follow-ups before non-local usage

- Replace placeholder values in `backend-secret.yaml`
- Review the final public host in `ingress.yaml`
- Replace `latest` tags with immutable version tags
- Switch `NETQ_LDAP_VALIDATE_CERTIFICATES` to `true` after mounting the corporate CA chain
