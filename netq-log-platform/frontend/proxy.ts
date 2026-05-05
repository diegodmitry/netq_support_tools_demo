import { NextResponse } from "next/server";
import type { NextRequest } from "next/server";

const PROTECTED_PREFIX = "/app";
const SESSION_COOKIE = "netq_session";
const AUTH_BYPASS_ENABLED = process.env.NETQ_SKIP_AUTH === "true";

export function proxy(request: NextRequest) {
  if (AUTH_BYPASS_ENABLED) {
    const { pathname } = request.nextUrl;

    if (pathname === "/") {
      return NextResponse.redirect(new URL("/app", request.url));
    }

    if (pathname === "/login") {
      return NextResponse.redirect(new URL("/app", request.url));
    }

    return NextResponse.next();
  }

  const sessionCookie = request.cookies.get(SESSION_COOKIE)?.value;
  const { pathname, searchParams } = request.nextUrl;

  if (pathname.startsWith(PROTECTED_PREFIX) && !sessionCookie) {
    const loginUrl = new URL("/login", request.url);
    loginUrl.searchParams.set("reason", "session-expired");
    return NextResponse.redirect(loginUrl);
  }

  if (
    pathname === "/login" &&
    sessionCookie &&
    searchParams.get("reason") !== "session-expired"
  ) {
    return NextResponse.redirect(new URL("/app", request.url));
  }

  if (pathname === "/") {
    return NextResponse.redirect(
      new URL(sessionCookie ? "/app" : "/login", request.url),
    );
  }

  return NextResponse.next();
}

export const config = {
  matcher: ["/", "/login", "/app/:path*"],
};
