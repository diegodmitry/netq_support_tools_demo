export const DEFAULT_AUTH_ERROR_MESSAGE = "Erro na autenticacao.";

type ErrorPayload = {
  error?: {
    message?: string;
  };
} | null;

export function getAuthErrorMessage(payload: ErrorPayload): string {
  const message = payload?.error?.message?.trim();
  return message ? message : DEFAULT_AUTH_ERROR_MESSAGE;
}
