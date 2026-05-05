export const AUTH_BYPASS_ENABLED = process.env.NETQ_SKIP_AUTH === "true";

export function buildDevSession() {
  return {
    authenticated: true,
    user: {
      username: "xid11185",
      displayName: "xid11185",
      domain: "ptportugal",
    },
    session: {
      authenticated: true,
      expiresInSeconds: 28800,
      idleTimeoutSeconds: 28800,
      keepAliveIntervalSeconds: 300,
      lastActivityAt: new Date().toISOString(),
    },
  };
}
