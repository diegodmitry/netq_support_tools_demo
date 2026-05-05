import {
  Button,
  CodeViewer,
  EmptyState,
  ErrorState,
} from "@/shared/components/ui";
import { getSession, queryAuditLogs } from "@/shared/lib/auth-client.server";
import { cookies } from "next/headers";
import { redirect } from "next/navigation";

import { logoutAction } from "./actions";
import { KeepAlive } from "./keep-alive";
import { NetqResults } from "./netq-results";
import { QueryForm } from "./query-form";

export default async function AppHomePage({
  searchParams,
}: {
  searchParams?: Promise<{
    environment?: string;
    queryType?: string;
    queryValue?: string;
    source?: string;
  }>;
}) {
  let session: Awaited<ReturnType<typeof getSession>>;
  const params = await searchParams;

  try {
    session = await getSession();
  } catch {
    const cookieStore = await cookies();
    cookieStore.delete("netq_session");
    redirect("/login?reason=session-expired");
  }

  const environment = params?.environment === "qa" ? "qa" : "prod";
  const isSapaQuery =
    params?.source === "sapa-id" || params?.queryType === "SAPA";
  const queryType =
    isSapaQuery
      ? "SAPA"
      : params?.queryType === "TIBCO" ||
          params?.queryType === "NETWIN" ||
          params?.queryType === "SIGRA" ||
          params?.queryType === "NA"
        ? params.queryType
        : "NETQ";
  const queryValue = params?.queryValue?.trim() ?? "";
  const source = queryType === "SAPA" ? "sapa-id" : "request-id";

  let queryResult: Awaited<ReturnType<typeof queryAuditLogs>> | null = null;

  if (queryValue.length > 0) {
    try {
      queryResult = await queryAuditLogs({
        environment,
        queryType,
        queryValue,
        source,
      });
    } catch {
      queryResult = {
        ok: false,
        error:
          "The frontend could not reach the audit lookup service. Check the backend connection and try again.",
      };
    }
  }

  const queryData = queryResult?.ok ? queryResult.data : null;
  const netqResult = queryData?.mode === "netq" ? queryData.result : null;
  const externalResult =
    queryData?.mode === "external" ? queryData.result : null;
  const sapaResult = queryData?.mode === "sapa" ? queryData.result : null;
  const pageClassName = "query-page page-frame";

  return (
    <main id="main-content" className="shell">
      <KeepAlive />
      <section className={pageClassName} aria-labelledby="audit-logs-title">
        <header className="query-shell-header">
          <div className="query-shell-copy">
            <div className="eyebrow">NETQ TOOLS</div>
          </div>
          <form action={logoutAction}>
            <Button type="submit" variant="secondary">
              {session.user.username} Logout
            </Button>
          </form>
        </header>

        <section
          className="surface-section query-surface"
          aria-labelledby="app-shell-title"
        >
          {/* <div className="surface-section-header query-surface-header">
            <h2 id="audit-logs-title">
              Query by environment, service type and value.
            </h2>
            <p>Search the logs using the options below.</p>
          </div> */}

          <QueryForm
            environment={environment}
            queryType={queryType}
            queryValue={queryValue}
          />

          {queryResult === null ? (
            <EmptyState
              title="No query executed yet"
              description="Enter the Environment, Service Type, and Value to run the query."
              className="query-empty-state"
            />
          ) : queryResult.ok ? (
            queryData?.mode === "netq" && netqResult ? (
              <NetqResults environment={environment} records={netqResult.records} />
            ) : externalResult && queryData ? (
              <CodeViewer
                title={`${externalResult.externalSystem} payload`}
                code={externalResult.payload.formatted}
                language="xml"
                meta={`ID: ${externalResult.externalId}`}
              />
            ) : sapaResult && queryData ? (
              <CodeViewer
                title="SAPA payload"
                code={sapaResult.payload.formatted}
                language="xml"
                meta={`SAPA ID: ${sapaResult.sapaId}`}
              />
            ) : (
              <ErrorState
                description="The response shape did not match the selected query mode."
                meta="Check the backend contract and frontend discriminated unions."
              />
            )
          ) : (
            <ErrorState
              description={queryResult.error}
              meta="The backend returned a handled error for this lookup."
            />
          )}
        </section>
      </section>
    </main>
  );
}
