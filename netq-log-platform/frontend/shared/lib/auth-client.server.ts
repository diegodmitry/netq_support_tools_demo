import "server-only";

import { cookies } from "next/headers";

import { getAuthErrorMessage } from "./auth-errors";
import { AUTH_BYPASS_ENABLED, buildDevSession } from "./dev-auth";
import { buildNetqMockQueryResponse } from "./netq-log-mock";

type LoginPayload = {
  domain: string;
  username: string;
  password: string;
};

type AuthConfig = {
  domains: Array<{
    value: string;
    label: string;
    default: boolean;
  }>;
};

type SessionResponse = {
  authenticated: boolean;
  user: {
    username: string;
    displayName: string;
    domain: string;
  };
  session: {
    authenticated: boolean;
    expiresInSeconds: number;
    idleTimeoutSeconds: number;
    keepAliveIntervalSeconds: number;
    lastActivityAt?: string;
  };
};

type LoginSuccessResponse = SessionResponse & {
  redirectTo: string;
};

type ErrorResponse = {
  error?: {
    message?: string;
  };
};

type LoginResult =
  | {
      ok: true;
      data: LoginSuccessResponse;
      sessionCookie: string;
    }
  | {
      ok: false;
      error: string;
    };

type AuditLogsQueryPayload = {
  environment: "prod" | "qa";
  queryType: "NETQ" | "TIBCO" | "NETWIN" | "SIGRA" | "NA" | "SAPA";
  queryValue: string;
  source: "request-id" | "sapa-id";
};

type AuditPayloadView = {
  contentType: string;
  formatted: string;
  raw: string;
};

type AuditLogsQueryMeta = {
  generatedAt: string;
  requestId?: string;
  totalRecords?: number;
};

type AuditLogsQueryResponse =
  | {
      query: AuditLogsQueryPayload;
      mode: "netq";
      result: {
        rootOrderId: string;
        records: Array<{
          orderId: string;
          orderType: string;
          auditPayload: AuditPayloadView;
          mongoPayload: AuditPayloadView;
          relatedOrderIds: string[];
        }>;
      };
      meta: AuditLogsQueryMeta;
    }
  | {
      query: AuditLogsQueryPayload;
      mode: "external";
      result: {
        externalSystem: string;
        externalId: string;
        payload: AuditPayloadView;
      };
      meta: AuditLogsQueryMeta;
    }
  | {
      query: AuditLogsQueryPayload;
      mode: "sapa";
      result: {
        sapaId: string;
        payload: AuditPayloadView;
      };
      meta: AuditLogsQueryMeta;
    };

type AuditLogsQueryResult =
  | {
      ok: true;
      data: AuditLogsQueryResponse;
    }
  | {
      ok: false;
      error: string;
    };

const API_BASE_URL =
  process.env.NETQ_API_BASE_URL ?? "http://localhost:8000/api/v1";
// Temporary NETQ frontend fixture. Remove after the real UI flow is validated end-to-end.
const USE_NETQ_MOCKS = process.env.NETQ_USE_MOCKS === "true";

async function apiFetch(path: string, init?: RequestInit): Promise<Response> {
  const cookieStore = await cookies();
  const sessionToken = cookieStore.get("netq_session")?.value;
  const headers = new Headers(init?.headers ?? {});

  if (!headers.has("Content-Type")) {
    headers.set("Content-Type", "application/json");
  }

  if (sessionToken) {
    headers.set("Cookie", `netq_session=${sessionToken}`);
  }

  return fetch(`${API_BASE_URL}${path}`, {
    ...init,
    headers,
    cache: "no-store",
  });
}

export async function getAuthConfig(): Promise<AuthConfig> {
  const response = await apiFetch("/auth/config", { method: "GET" });
  if (!response.ok) {
    return {
      domains: [
        { value: "ptportugal", label: "PTPORTUGAL", default: true },
        { value: "ptc", label: "PTC", default: false },
      ],
    };
  }
  return response.json();
}

export async function login(payload: LoginPayload): Promise<LoginResult> {
  if (AUTH_BYPASS_ENABLED) {
    return {
      ok: true,
      data: {
        ...buildDevSession(),
        redirectTo: "/app",
      },
      sessionCookie: "dev-auth-bypass",
    };
  }

  const response = await apiFetch("/auth/login", {
    method: "POST",
    body: JSON.stringify(payload),
  });

  if (!response.ok) {
    const errorBody = (await response
      .json()
      .catch(() => null)) as ErrorResponse | null;
    return {
      ok: false,
      error: getAuthErrorMessage(errorBody),
    };
  }

  const setCookieHeader = response.headers.get("set-cookie") ?? "";
  const sessionCookie =
    setCookieHeader.split(";")[0]?.split("=")[1] ?? "session-created";
  return {
    ok: true,
    data: (await response.json()) as LoginSuccessResponse,
    sessionCookie,
  };
}

export async function getSession(): Promise<SessionResponse> {
  if (AUTH_BYPASS_ENABLED) {
    return buildDevSession();
  }

  const response = await apiFetch("/auth/session", { method: "GET" });
  if (!response.ok) {
    throw new Error("Unauthenticated session");
  }
  return response.json();
}

export async function logout(): Promise<void> {
  if (AUTH_BYPASS_ENABLED) {
    return;
  }

  await apiFetch("/auth/session", { method: "DELETE" });
}

export async function queryAuditLogs(
  payload: AuditLogsQueryPayload,
): Promise<AuditLogsQueryResult> {
  if (USE_NETQ_MOCKS && payload.queryType === "NETQ") {
    return {
      ok: true,
      data: buildNetqMockQueryResponse(payload),
    };
  }

  const response = await apiFetch("/audit-logs/query", {
    method: "POST",
    body: JSON.stringify(payload),
  });

  if (!response.ok) {
    const errorBody = (await response
      .json()
      .catch(() => null)) as ErrorResponse | null;
    return {
      ok: false,
      error: getAuthErrorMessage(errorBody),
    };
  }

  return {
    ok: true,
    data: (await response.json()) as AuditLogsQueryResponse,
  };
}
