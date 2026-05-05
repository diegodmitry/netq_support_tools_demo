"use client";

import { useEffect } from "react";
import { useRouter } from "next/navigation";

const KEEP_ALIVE_INTERVAL_MS = 300000;

export function KeepAlive() {
  const router = useRouter();

  useEffect(() => {
    let cancelled = false;

    async function ping() {
      const response = await fetch("/api/auth/keep-alive", {
        method: "POST",
        cache: "no-store",
      });

      if (!response.ok && response.status === 401 && !cancelled) {
        router.replace("/login?reason=session-expired");
      }
    }

    void ping();
    const timer = window.setInterval(() => {
      void ping();
    }, KEEP_ALIVE_INTERVAL_MS);

    return () => {
      cancelled = true;
      window.clearInterval(timer);
    };
  }, [router]);

  return null;
}
