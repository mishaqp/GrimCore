import assert from "node:assert/strict";
import test from "node:test";
import {
  createConversationDraft,
  isPersistedConversation,
} from "../src/conversationDraft.ts";

test("choosing a new conversation mode creates only a localized local draft", () => {
  const draft = createConversationDraft("codex", 1234, "claude-code-acp", "Новый чат");

  assert.equal(draft.id, 0);
  assert.equal(draft.mode, "codex");
  assert.equal(draft.agentId, "claude-code-acp");
  assert.equal(draft.updatedAt, 1234);
  assert.equal(draft.title, "Новый чат");
  assert.equal(isPersistedConversation(draft), false);
});

test("only a positive server id is considered persisted", () => {
  assert.equal(isPersistedConversation({ id: 17, mode: "normal" }), true);
  assert.equal(isPersistedConversation(null), false);
});

test("the standalone draft helper defaults to the fork locale", () => {
  assert.equal(createConversationDraft("normal", 1234).title, "Новый чат");
});
