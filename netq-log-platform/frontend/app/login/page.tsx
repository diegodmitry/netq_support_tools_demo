import { redirect } from "next/navigation";

import { LoginForm } from "./form";
import { FormMessage } from "@/shared/components/ui";
import { getAuthConfig } from "@/shared/lib/auth-client.server";
import { AUTH_BYPASS_ENABLED } from "@/shared/lib/dev-auth";

export default async function LoginPage({
  searchParams,
}: {
  searchParams?: Promise<{ reason?: string }>;
}) {
  if (AUTH_BYPASS_ENABLED) {
    redirect("/app");
  }

  const [config, params] = await Promise.all([getAuthConfig(), searchParams]);
  const expired = params?.reason === "session-expired";

  return (
    <main id="main-content" className="shell">
      <section
        className="login-card"
        aria-labelledby="login-title"
        aria-describedby="login-description"
      >
        <div className="login-copy">
          <div className="eyebrow">NetQ Support Tools</div>
          <h1 id="login-title">Sign in</h1>
          <p id="login-description">Authorized access only.</p>
        </div>
        {expired ? (
          <FormMessage tone="info">
            Sessao expirada ou inexistente.
          </FormMessage>
        ) : null}
        <LoginForm domains={config.domains} />
      </section>
    </main>
  );
}
