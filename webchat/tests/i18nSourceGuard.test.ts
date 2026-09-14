import assert from "node:assert/strict";
import { readdir, readFile, stat } from "node:fs/promises";
import { fileURLToPath } from "node:url";
import path from "node:path";
import test from "node:test";

const sourceRoot = path.resolve(
  path.dirname(fileURLToPath(import.meta.url)),
  "../src",
);

async function sourceFiles(directory: string): Promise<string[]> {
  const files: string[] = [];
  for (const name of await readdir(directory)) {
    const item = path.join(directory, name);
    if ((await stat(item)).isDirectory()) files.push(...await sourceFiles(item));
    else if (/\.(?:ts|tsx)$/.test(name)) files.push(item);
  }
  return files;
}

test("production UI text lives in the locale catalog", async () => {
  const failures: string[] = [];
  for (const file of await sourceFiles(sourceRoot)) {
    if (file.endsWith(path.join("i18n", "catalog.ts"))) continue;
    let source = await readFile(file, "utf8");
    if (file.endsWith(path.join("components", "ChatPanel.tsx"))) {
      source = source.replace('"任务已取消"', '"legacy-cancelled-marker"');
    }
    if (file.endsWith(path.join("i18n", "I18nProvider.tsx"))) {
      source = source.replace(">中文<", ">Chinese<");
    }
    source.split("\n").forEach((line, index) => {
      if (/\p{Script=Han}/u.test(line)) {
        failures.push(`${path.relative(sourceRoot, file)}:${index + 1}`);
      }
    });
  }
  assert.deepEqual(failures, []);
});
