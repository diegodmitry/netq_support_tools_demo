import type { ReactNode } from "react";

import { classNames } from "@/shared/lib/classnames";

type StateTone = "neutral" | "danger";

type StateCardProps = {
  title: string;
  description: ReactNode;
  meta?: ReactNode;
  tone?: StateTone;
  action?: ReactNode;
  className?: string;
};

function StateCard({
  title,
  description,
  meta,
  tone = "neutral",
  action,
  className,
}: StateCardProps) {
  return (
    <section
      className={classNames("state-card", `state-card-${tone}`, className)}
      role={tone === "danger" ? "alert" : "status"}
      aria-live={tone === "danger" ? "assertive" : "polite"}
    >
      <div className="state-copy">
        <div className="state-kicker">
          {tone === "danger" ? "Error state" : "System state"}
        </div>
        <strong>{title}</strong>
        <p>{description}</p>
        {meta ? <div className="state-meta">{meta}</div> : null}
      </div>
      {action ? <div className="state-action">{action}</div> : null}
    </section>
  );
}

type PublicStateProps = {
  title?: string;
  description?: ReactNode;
  meta?: ReactNode;
  action?: ReactNode;
  className?: string;
};

export function LoadingState({
  title = "Loading operational data",
  description = "Preparing the requested surface and preserving a readable shell while data arrives.",
  meta,
  action,
  className,
}: PublicStateProps) {
  return (
    <StateCard
      title={title}
      description={description}
      meta={meta}
      action={action}
      className={className}
    />
  );
}

export function ErrorState({
  title = "We could not complete this request",
  description = "The requested operation returned an unexpected failure.",
  meta,
  action,
  className,
}: PublicStateProps) {
  return (
    <StateCard
      title={title}
      description={description}
      meta={meta}
      action={action}
      tone="danger"
      className={className}
    />
  );
}

export function EmptyState({
  title = "No records yet",
  description = "The current filter or workflow did not return any items.",
  meta,
  action,
  className,
}: PublicStateProps) {
  return (
    <StateCard
      title={title}
      description={description}
      meta={meta}
      action={action}
      className={className}
    />
  );
}
