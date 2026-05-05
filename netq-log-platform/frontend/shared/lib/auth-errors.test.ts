import { describe, expect, it } from "vitest";

import { DEFAULT_AUTH_ERROR_MESSAGE, getAuthErrorMessage } from "./auth-errors";

describe("getAuthErrorMessage", () => {
  it("returns the api message when it is present", () => {
    expect(
      getAuthErrorMessage({
        error: {
          message: "Sessao expirada ou inexistente.",
        },
      }),
    ).toBe("Sessao expirada ou inexistente.");
  });

  it("falls back to the default message when the api message is missing", () => {
    expect(getAuthErrorMessage(null)).toBe(DEFAULT_AUTH_ERROR_MESSAGE);
  });

  it("falls back to the default message when the api message is blank", () => {
    expect(
      getAuthErrorMessage({
        error: {
          message: "   ",
        },
      }),
    ).toBe(DEFAULT_AUTH_ERROR_MESSAGE);
  });
});
