import { cookies } from "next/headers";
import { NextRequest, NextResponse } from "next/server";

const API_BASE_URL =
  process.env.NETQ_API_BASE_URL ?? "http://localhost:8000/api/v1";
const SESSION_COOKIE = "netq_session";

export async function POST(request: NextRequest) {
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

  const body = await request.text();
  const response = await fetch(`${API_BASE_URL}/audit-logs/related-detail`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      Cookie: `${SESSION_COOKIE}=${sessionToken}`,
    },
    body,
    cache: "no-store",
  });

  const responseBody = await response.text();
  const nextResponse = new NextResponse(responseBody, {
    status: response.status,
    headers: {
      "Content-Type":
        response.headers.get("content-type") ?? "application/json",
    },
  });

  if (response.status === 401) {
    nextResponse.cookies.delete(SESSION_COOKIE);
  }

  return nextResponse;
}
