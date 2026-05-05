import type { ButtonHTMLAttributes, ReactNode } from "react";

import { classNames } from "@/shared/lib/classnames";

type ButtonVariant = "primary" | "secondary";

type ButtonProps = ButtonHTMLAttributes<HTMLButtonElement> & {
  variant?: ButtonVariant;
  busy?: boolean;
  busyLabel?: ReactNode;
};

export function Button({
  className,
  children,
  variant = "primary",
  busy = false,
  busyLabel,
  disabled,
  ...props
}: ButtonProps) {
  return (
    <button
      className={classNames(
        variant === "primary" ? "button" : "button-secondary",
        className,
      )}
      aria-busy={busy || undefined}
      disabled={disabled ?? busy}
      {...props}
    >
      {busy ? (busyLabel ?? children) : children}
    </button>
  );
}
