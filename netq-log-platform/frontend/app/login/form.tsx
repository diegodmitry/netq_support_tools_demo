"use client";

import { useActionState } from "react";

import {
  Button,
  FormField,
  FormMessage,
  SelectInput,
  TextInput,
} from "@/shared/components/ui";
import { loginAction, type LoginActionState } from "./actions";

const initialState: LoginActionState = {};

type Domain = {
  value: string;
  label: string;
  default: boolean;
};

export function LoginForm({ domains }: { domains: Domain[] }) {
  const [state, formAction, pending] = useActionState(
    loginAction,
    initialState,
  );

  return (
    <form action={formAction} className="stack" noValidate aria-busy={pending}>
      {state.error ? <FormMessage>{state.error}</FormMessage> : null}

      <FormField
        label="Domain"
        htmlFor="domain"
      >
        <SelectInput
          id="domain"
          name="domain"
          defaultValue={domains.find((item) => item.default)?.value}
          autoComplete="organization"
        >
          {domains.map((domain) => (
            <option key={domain.value} value={domain.value}>
              {domain.label}
            </option>
          ))}
        </SelectInput>
      </FormField>

      <FormField label="Username" htmlFor="username">
        <TextInput
          id="username"
          name="username"
          type="text"
          placeholder="username"
          autoComplete="username"
          autoFocus
          required
        />
      </FormField>

      <FormField label="Password" htmlFor="password">
        <TextInput
          id="password"
          name="password"
          type="password"
          autoComplete="current-password"
          required
        />
      </FormField>

      <div className="button-row login-button-row">
        <Button type="submit" busy={pending} busyLabel="Signing in...">
          Login
        </Button>
      </div>
    </form>
  );
}
