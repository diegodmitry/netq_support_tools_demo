"use client";

import { useId, useState, type FormEvent } from "react";
import { usePathname, useRouter } from "next/navigation";

import {
  Button,
  FormField,
  SelectInput,
  TextInput,
} from "@/shared/components/ui";

type QueryType = "NETQ" | "TIBCO" | "NETWIN" | "SIGRA" | "NA" | "SAPA";

const UUID_EXAMPLE = "f29f1ced-56c2-4a4e-b9cb-e38a623b7676";
const NPU_EXAMPLE = "0099F1638V1_0x202604141314075570000001831896486000";
const OPK_EXAMPLE = "3067769867";

const queryFieldConfig: Record<
  QueryType,
  {
    label: string;
    placeholder: string;
  }
> = {
  NETQ: {
    label: "Request ID",
    placeholder: UUID_EXAMPLE,
  },
  TIBCO: {
    label: "TIBCO ID",
    placeholder: NPU_EXAMPLE,
  },
  NETWIN: {
    label: "NETWIN ID",
    placeholder: NPU_EXAMPLE,
  },
  SIGRA: {
    label: "SIGRA ID",
    placeholder: NPU_EXAMPLE,
  },
  NA: {
    label: "NA ID",
    placeholder: OPK_EXAMPLE,
  },
  SAPA: {
    label: "SAPA ID",
    placeholder: "1700426781",
  },
};

export function QueryForm({
  environment,
  queryType,
}: {
  environment: "prod" | "qa";
  queryType: QueryType;
  queryValue: string;
}) {
  const router = useRouter();
  const pathname = usePathname();
  const [selectedEnvironment, setSelectedEnvironment] = useState<"prod" | "qa">(environment);
  const [selectedQueryType, setSelectedQueryType] = useState<QueryType>(queryType);
  const [inputValue, setInputValue] = useState("");
  const config = queryFieldConfig[selectedQueryType];
  const queryValueId = useId();

  function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();

    const trimmedValue = inputValue.trim();
    if (!trimmedValue) {
      return;
    }

    const searchParams = new URLSearchParams({
      environment: selectedEnvironment,
      queryType: selectedQueryType,
      queryValue: trimmedValue,
    });

    router.push(`${pathname}?${searchParams.toString()}`);
    setInputValue("");
  }

  return (
    <form className="stack query-form" onSubmit={handleSubmit}>
      <div className="query-grid">
        <FormField
          label="Environment"
          htmlFor="environment"
          className="query-field"
        >
          <SelectInput
            id="environment"
            name="environment"
            value={selectedEnvironment}
            onChange={(event) =>
              setSelectedEnvironment(event.currentTarget.value as "prod" | "qa")
            }
          >
            <option value="prod">Production</option>
            <option value="qa">QA</option>
          </SelectInput>
        </FormField>

        <FormField
          label="Service Type"
          htmlFor="queryType"
          className="query-field"
        >
          <SelectInput
            id="queryType"
            name="queryType"
            value={selectedQueryType}
            onChange={(event) => {
              setSelectedQueryType(event.currentTarget.value as QueryType);
            }}
          >
            <option value="NETQ">NETQ</option>
            <option value="TIBCO">TIBCO(NPU)</option>
            <option value="NETWIN">NETWIN(NPU)</option>
            <option value="SIGRA">SIGRA(NPU)</option>
            <option value="NA">NA(OPK)</option>
            <option value="SAPA">SAPA</option>
          </SelectInput>
        </FormField>

        <FormField
          label={config.label}
          htmlFor={queryValueId}
          className="query-field"
        >
          <TextInput
            id={queryValueId}
            name="queryValue"
            value={inputValue}
            onChange={(event) => setInputValue(event.currentTarget.value)}
            placeholder={config.placeholder}
            required
          />
        </FormField>

        <div className="query-action-field">
          <div className="query-action-spacer" aria-hidden="true">
            Action
          </div>
          <Button type="submit" className="query-submit-button">
            Submit
          </Button>
        </div>
      </div>
    </form>
  );
}
