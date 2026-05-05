"use server";

import { cookies } from "next/headers";
import { redirect } from "next/navigation";

import { login } from "@/shared/lib/auth-client.server";

export type LoginActionState = {
  error?: string;
};

export async function loginAction(
  _prevState: LoginActionState,
  formData: FormData,
): Promise<LoginActionState> {
  const payload = {
    domain: String(formData.get("domain") ?? ""),
    username: String(formData.get("username") ?? ""),
    password: String(formData.get("password") ?? ""),
  };

  const result = await login(payload);

  if (!result.ok) {
    return { error: result.error };
  }

  const cookieStore = await cookies();
  cookieStore.set("netq_session", result.sessionCookie, {
    httpOnly: true,
    secure: process.env.NODE_ENV === "production",
    sameSite: "lax",
    path: "/",
    maxAge: 28800,
  });

  redirect("/app");
}
