import { useEffect, useMemo, useState, type FormEvent } from "react";
import { browserFrameUrl, workspaceDownloadUrl } from "../api";
import { formatBytes } from "../format";
import { useI18n } from "../i18n/I18nProvider";
import type {
  BrowserSnapshot,
  ContextPanelName,
  WorkspaceItem,
} from "../types";
import { Icon } from "./Icon";

interface ContextPaneProps {
  activePanel: ContextPanelName;
  workspacePath: string;
  workspaceItems: WorkspaceItem[];
  workspaceFilePath: string | null;
  workspaceContent: string;
  workspaceDirty: boolean;
  browserSnapshot: BrowserSnapshot | null;
  browserFrameSeed: number;
  onOpenConversations: () => void;
  onSelectPanel: (panel: ContextPanelName) => void;
  onWorkspacePath: () => void;
  onWorkspaceItem: (item: WorkspaceItem) => void;
  onWorkspaceRefresh: () => void;
  onWorkspaceContent: (content: string) => void;
  onWorkspaceSave: () => void;
  onBrowserAction: (payload: Record<string, unknown>) => void;
  onBrowserRefresh: () => void;
}

export function ContextPane({
  activePanel,
  workspacePath,
  workspaceItems,
  workspaceFilePath,
  workspaceContent,
  workspaceDirty,
  browserSnapshot,
  browserFrameSeed,
  onOpenConversations,
  onSelectPanel,
  onWorkspacePath,
  onWorkspaceItem,
  onWorkspaceRefresh,
  onWorkspaceContent,
  onWorkspaceSave,
  onBrowserAction,
  onBrowserRefresh,
}: ContextPaneProps) {
  const { messages } = useI18n();
  const [browserUrl, setBrowserUrl] = useState("");
  const browserAvailable = browserSnapshot?.available === true;
  const frameUrl = useMemo(() => browserFrameUrl(browserFrameSeed), [browserFrameSeed]);

  useEffect(() => {
    if (browserSnapshot?.currentUrl) setBrowserUrl(browserSnapshot.currentUrl);
  }, [browserSnapshot?.currentUrl]);

  function navigate(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    const url = browserUrl.trim();
    if (url) onBrowserAction({ action: "navigate", url, tool_title: "Web Chat Navigate" });
  }

  return (
    <aside className="context-pane">
      <div className="mobile-context-header">
        <button className="appbar-icon" type="button" aria-label={messages.openConversationList} onClick={onOpenConversations}>
          <Icon name="menu" size={20} />
        </button>
        <strong>{activePanel === "workspace" ? messages.workspace : messages.browser}</strong>
        <span />
      </div>
      <div className="context-tabs" role="tablist">
        {(["workspace", "browser"] as ContextPanelName[]).map((panel) => (
          <button
            className={`context-tab${activePanel === panel ? " active" : ""}`}
            type="button"
            role="tab"
            aria-selected={activePanel === panel}
            onClick={() => onSelectPanel(panel)}
            key={panel}
          >{panel === "workspace" ? messages.workspace : messages.browser}</button>
        ))}
      </div>

      <section id="workspace-panel" className={`context-panel${activePanel === "workspace" ? " active" : ""}`}>
        <header className="context-header">
          <div>
            <strong>{messages.workspace}</strong>
            <button className="path-button" type="button" title={workspacePath} onClick={onWorkspacePath}>
              {workspacePath || messages.workspace}
            </button>
          </div>
          <div className="header-actions">
            {workspaceFilePath && (
              <a className="quiet-link" href={workspaceDownloadUrl(workspaceFilePath)} title={messages.download}>
                <Icon name="download" size={15} /><span>{messages.download}</span>
              </a>
            )}
            <button className="quiet-button" type="button" onClick={onWorkspaceRefresh}>
              <Icon name="refresh" size={14} /><span>{messages.refresh}</span>
            </button>
            <button
              className="primary-small-button"
              type="button"
              disabled={!workspaceDirty || !workspaceFilePath}
              onClick={onWorkspaceSave}
            ><Icon name="save" size={14} /><span>{messages.save}</span></button>
          </div>
        </header>
        <div className="workspace-layout">
          <div className="workspace-list">
            {!workspaceItems.length && <div className="list-empty">{messages.emptyDirectory}</div>}
            {workspaceItems.map((item) => (
              <button
                className={`workspace-item${item.path === workspaceFilePath ? " active" : ""}`}
                type="button"
                onClick={() => onWorkspaceItem(item)}
                key={item.path}
              >
                <Icon name={item.isDirectory ? "folder" : "file"} size={15} />
                <span>{item.name}</span>
                <small>{item.isDirectory ? "" : formatBytes(item.size)}</small>
              </button>
            ))}
          </div>
          <div className="workspace-editor-wrap">
            <p>{workspaceFilePath || messages.selectFile}</p>
            <textarea
              id="workspace-editor"
              spellCheck={false}
              disabled={!workspaceFilePath}
              value={workspaceContent}
              onChange={(event) => onWorkspaceContent(event.target.value)}
            />
          </div>
        </div>
      </section>

      <section id="browser-panel" className={`context-panel${activePanel === "browser" ? " active" : ""}`}>
        <header className="context-header browser-controls">
          <form className="browser-address-form" onSubmit={navigate}>
            <input
              type="url"
              placeholder={messages.enterBrowserUrl}
              value={browserUrl}
              onChange={(event) => setBrowserUrl(event.target.value)}
            />
            <button className="primary-small-button" type="submit">{messages.open}</button>
          </form>
          <div className="browser-buttons">
            <button
              className="quiet-button"
              type="button"
              onClick={() => onBrowserAction({ action: "scroll", direction: "up", amount: 420, tool_title: "Web Chat Scroll Up" })}
            >{messages.scrollUp}</button>
            <button
              className="quiet-button"
              type="button"
              onClick={() => onBrowserAction({ action: "scroll", direction: "down", amount: 420, tool_title: "Web Chat Scroll Down" })}
            >{messages.scrollDown}</button>
            <button className="quiet-button" type="button" onClick={onBrowserRefresh}>{messages.refreshFrame}</button>
          </div>
        </header>
        <div className="browser-summary">
          <strong>{browserSnapshot?.title || messages.noBrowserSession}</strong>
          <span>{browserSnapshot?.currentUrl || ""}</span>
        </div>
        <div className="browser-frame-wrap">
          {browserAvailable
            ? <img src={frameUrl} alt={messages.browserLiveFrame} />
            : <p>{messages.noBrowserSessionToMirror}</p>}
        </div>
      </section>
    </aside>
  );
}
