import {
  cloneElement,
  isValidElement,
  type ComponentPropsWithoutRef,
  type ReactNode,
  useId,
} from "react";

import { classNames } from "@/shared/lib/classnames";

type FormFieldProps = {
  label: string;
  htmlFor: string;
  hint?: ReactNode;
  error?: ReactNode;
  children: ReactNode;
  className?: string;
};

export function FormField({
  label,
  htmlFor,
  hint,
  error,
  children,
  className,
}: FormFieldProps) {
  const fieldId = useId();
  const hintId = hint ? `${fieldId}-hint` : undefined;
  const errorId = error ? `${fieldId}-error` : undefined;
  const describedBy = [hintId, errorId].filter(Boolean).join(" ") || undefined;
  const control = isValidElement(children)
    ? cloneElement(children as React.ReactElement<Record<string, unknown>>, {
        "aria-describedby": describedBy,
        "aria-invalid": Boolean(error) || undefined,
      })
    : children;

  return (
    <div className={classNames("field", className)}>
      <label htmlFor={htmlFor}>{label}</label>
      {control}
      {hint ? (
        <div id={hintId} className="field-hint">
          {hint}
        </div>
      ) : null}
      {error ? (
        <div id={errorId} className="field-error">
          {error}
        </div>
      ) : null}
    </div>
  );
}

export function TextInput({
  className,
  ...props
}: ComponentPropsWithoutRef<"input">) {
  return (
    <input className={classNames("input-control", className)} {...props} />
  );
}

export function SelectInput({
  className,
  children,
  ...props
}: ComponentPropsWithoutRef<"select">) {
  return (
    <select className={classNames("input-control", className)} {...props}>
      {children}
    </select>
  );
}

export function FormMessage({
  children,
  tone = "error",
}: {
  children: ReactNode;
  tone?: "error" | "info";
}) {
  return (
    <div
      className={tone === "error" ? "error" : "info-banner"}
      role={tone === "error" ? "alert" : "status"}
      aria-live={tone === "error" ? "assertive" : "polite"}
    >
      {children}
    </div>
  );
}

export function ButtonRow({
  children,
  className,
}: {
  children: ReactNode;
  className?: string;
}) {
  return <div className={classNames("button-row", className)}>{children}</div>;
}
