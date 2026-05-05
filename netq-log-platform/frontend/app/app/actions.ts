"use server";

import { cookies } from "next/headers";
import { redirect } from "next/navigation";

import { logout } from "@/shared/lib/auth-client.server";

export async function logoutAction() {
  await logout();
  const cookieStore = await cookies();
  cookieStore.delete("netq_session");
  redirect("/login");
}
