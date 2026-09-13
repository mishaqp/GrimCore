import { useState, type FormEvent } from "react";
import { LanguageSwitcher, useI18n } from "../i18n/I18nProvider";

interface LoginViewProps {
  initialToken: string;
  busy: boolean;
  error: string;
  onLogin: (token: string) => Promise<void>;
}

export function LoginView({ initialToken, busy, error, onLogin }: LoginViewProps) {
  const { messages } = useI18n();
  const [token, setToken] = useState(initialToken);

  function submit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    const value = token.trim();
    if (value) void onLogin(value);
  }

  return (
    <main className="login-view">
      <section className="login-panel" aria-label={messages.login}>
        <LanguageSwitcher className="login-language-select" />
        <form className="login-form" onSubmit={submit}>
          <label htmlFor="token-input">{messages.serverToken}</label>
          <input
            id="token-input"
            name="token"
            type="password"
            autoComplete="current-password"
            value={token}
            disabled={busy}
            onChange={(event) => setToken(event.target.value)}
            required
          />
          <button className="primary-button" type="submit" disabled={busy}>
            {busy ? messages.connecting : messages.connect}
          </button>
        </form>
        <p className="form-error" role="alert">{error}</p>
      </section>
    </main>
  );
}
