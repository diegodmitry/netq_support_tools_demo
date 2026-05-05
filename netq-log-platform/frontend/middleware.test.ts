import { describe, expect, it } from "vitest";
import { NextRequest } from "next/server";

import { proxy } from "./proxy";

function buildRequest(path: string, sessionCookie?: string) {
  const request = new NextRequest(`https://netq.example${path}`);

  if (sessionCookie) {
    request.cookies.set("netq_session", sessionCookie);
  }

  return request;
}

describe("proxy", () => {
  it("redirects unauthenticated protected requests to login", () => {
    const response = proxy(buildRequest("/app"));

    expect(response.status).toBe(307);
    expect(response.headers.get("location")).toBe(
      "https://netq.example/login?reason=session-expired",
    );
  });

  it("redirects authenticated login requests to the protected shell", () => {
    const response = proxy(buildRequest("/login", "session-123"));

    expect(response.status).toBe(307);
    expect(response.headers.get("location")).toBe("https://netq.example/app");
  });

  it("keeps the expired-session login route accessible even with a stale cookie", () => {
    const response = proxy(
      buildRequest("/login?reason=session-expired", "session-123"),
    );

    expect(response.status).toBe(200);
  });

  it("redirects the root path based on cookie presence", () => {
    const anonymousResponse = proxy(buildRequest("/"));
    const authenticatedResponse = proxy(buildRequest("/", "session-123"));

    expect(anonymousResponse.headers.get("location")).toBe(
      "https://netq.example/login",
    );
    expect(authenticatedResponse.headers.get("location")).toBe(
      "https://netq.example/app",
    );
  });
});
