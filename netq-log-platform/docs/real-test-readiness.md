# Real Test Readiness

## Purpose

This document maps the legacy `NetQTools` configuration into the new backend and defines the minimum checklist required to run useful real-environment tests without mocks.

## 1. What the legacy project already provides

The legacy folder already contains real integration values in:

- `NetQTools/conf/app.json`
- `NetQTools/conf/app_DEV.json`
- `NetQTools/conf/app_PRD.json`

Those files contain:

- LDAP server host, port, bind DN and bind password
- Audit Logs upstream URLs for prod and QA
- SAPA URL
- SIGRA SOAP URL, action, app code and timeout
- Basic-auth values for the prod mongo endpoint

The legacy runtime usage is confirmed in:

- `NetQTools/src/java/NetqTools/Login.java`
- `NetQTools/src/java/NetqTools/URLRequest.java`
- `NetQTools/src/java/NetqTools/URLRequestSigra.java`

## 2. New backend bridge to the legacy config

The new backend can now load the legacy JSON config through:

- `NETQ_LEGACY_CONFIG_FILE`

Example:

```bash
NETQ_AUTH_PROVIDER=ldap
NETQ_LEGACY_CONFIG_FILE=../NetQTools/conf/app_DEV.json
```

Behavior:

- explicit `NETQ_*` environment variables still win
- any unset integration field can be hydrated from the legacy JSON
- the bridge is intended for local validation and migration support, not for long-term secret management

## 3. Authentication rule used for real tests

Legacy login uses both:

- local allowed-user file `usrPerm`
- LDAP bind

For real-environment tests in the new backend we support this minimum rule:

- if `allowed_users` is configured, it is enforced
- if `allowed_users` is empty, access depends only on successful LDAP authentication

This makes real smoke testing possible even when the legacy `usrPerm` file is not present in the new runtime.

## 4. Minimum checklist before running real tests

- [ ] Confirm network access from the backend runtime to LDAP, Audit Logs, SAPA and SIGRA hosts
- [ ] Set `NETQ_AUTH_PROVIDER=ldap`
- [ ] Set `NETQ_LEGACY_CONFIG_FILE` to one of the legacy `app*.json` files or provide equivalent `NETQ_*` variables directly
- [ ] Decide whether to enforce `allowed_users`
- [ ] If testing LDAP-only access, set `NETQ_ALLOWED_USERS=` to an empty value
- [ ] Start the backend with the real-environment configuration
- [ ] Start the frontend with `NETQ_API_BASE_URL` pointing to the backend
- [ ] Execute real login
- [ ] Validate session bootstrap, keep-alive and logout against the live backend
- [ ] Only after auth passes, move on to real integration tests for Audit Logs and SIGRA

## 5. Current limitation

The configuration bridge is ready, but the new platform still does not implement the functional API contracts for:

- Audit Logs
- SIGRA UI/API flow end to end

So the first useful real tests should start with:

1. authentication
2. session bootstrap
3. keep-alive
4. logout
