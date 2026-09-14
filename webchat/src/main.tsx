import { createRoot } from "react-dom/client";
import App from "./App";
import { I18nProvider } from "./i18n/I18nProvider";
import "../styles.css";

const root = document.getElementById("root");
if (!root) throw new Error("Missing WebChat root element");

createRoot(root).render(
  <I18nProvider>
    <App />
  </I18nProvider>,
);
