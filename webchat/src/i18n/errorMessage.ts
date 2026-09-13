import type { ApiErrorCode, AppLocale, MessageCatalog } from "./catalog";

const HAN_TEXT = /\p{Script=Han}/u;

export function localizedRequestErrorMessage(
  status: number,
  serverMessage: string,
  locale: AppLocale,
  messages: MessageCatalog,
): string {
  if (!serverMessage) return messages.requestFailedWithStatus(status);
  if (Object.prototype.hasOwnProperty.call(messages.apiErrors, serverMessage)) {
    return messages.apiErrors[serverMessage as ApiErrorCode];
  }
  if (locale !== "zh" && HAN_TEXT.test(serverMessage)) {
    return messages.requestFailedWithStatus(status);
  }
  return serverMessage;
}
