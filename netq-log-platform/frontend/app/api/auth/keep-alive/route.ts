import { cookies } from "next/headers";
import { NextResponse } from "next/server";

import { AUTH_BYPASS_ENABLED } from "@/shared/lib/dev-auth";

const API_BASE_URL =
  process.env.NETQ_API_BASE_URL ?? "http://localhost:8000/api/v1";
const SESSION_COOKIE = "netq_session";

export async function POST() {
  if (AUTH_BYPASS_ENABLED) {
    return NextResponse.json({
      ok: true,
      session: {
        authenticated: true,
        bypassed: true,
      },
    });
  }

  const cookieStore = await cookies();
  const sessionToken = cookieStore.get(SESSION_COOKIE)?.value;

  if (!sessionToken) {
    return NextResponse.json(
      {
        ok: false,
        error: {
          code: "SESSION_EXPIRED",
          message: "Sessao expirada ou inexistente.",
        },
      },
      { status: 401 },
    );
  }

  const response = await fetch(`${API_BASE_URL}/auth/keep-alive`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      Cookie: `${SESSION_COOKIE}=${sessionToken}`,
    },
    body: JSON.stringify({}),
    cache: "no-store",
  });

  const body = await response.text();
  const refreshedCookieHeader = response.headers.get("set-cookie") ?? "";
  const refreshedSessionToken =
    refreshedCookieHeader.split(";")[0]?.split("=")[1] ?? sessionToken;

  if (response.ok) {
    const nextResponse = new NextResponse(body, {
      status: response.status,
      headers: {
        "Content-Type":
          response.headers.get("content-type") ?? "application/json",
      },
    });
    nextResponse.cookies.set(SESSION_COOKIE, refreshedSessionToken, {
      httpOnly: true,
      secure: process.env.NODE_ENV === "production",
      sameSite: "lax",
      path: "/",
      maxAge: 28800,
    });
    return nextResponse;
  }

  const nextResponse = new NextResponse(body, {
    status: response.status,
    headers: {
      "Content-Type":
        response.headers.get("content-type") ?? "application/json",
    },
  });
  nextResponse.cookies.delete(SESSION_COOKIE);
  return nextResponse;
}
