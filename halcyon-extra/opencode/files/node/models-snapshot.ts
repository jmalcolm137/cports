import { readFile } from "node:fs/promises"
import type { BunPlugin } from "bun"

// A floor, not equality: guards against an error page or a truncated body
// that still parses as a small object.
const MINIMUM_PROVIDERS = 100
export const committedSnapshot = new URL("../src/models-dev/snapshot.txt", import.meta.url)

// Model fields opencode never reads. Dropping them keeps the bundled copy small; every
// other field, including ones models.dev adds later, is kept as published.
const UNUSED_MODEL_FIELDS = new Set([
  "description",
  "canonical_id",
  "knowledge",
  "last_updated",
  "deprecation_date",
  "open_weights",
  "metadata",
])

function trim(text: string) {
  const catalog = JSON.parse(text) as Record<string, { models: Record<string, Record<string, unknown>> }>
  return JSON.stringify(
    Object.fromEntries(
      Object.entries(catalog).map(([id, provider]) => [
        id,
        {
          ...provider,
          models: Object.fromEntries(
            Object.entries(provider.models).map(([modelID, model]) => [
              modelID,
              Object.fromEntries(Object.entries(model).filter(([key]) => !UNUSED_MODEL_FIELDS.has(key))),
            ]),
          ),
        },
      ]),
    ),
  )
}

async function validateModelsSnapshot(text: string) {
  const catalog = JSON.parse(text) as Record<string, unknown>
  const providers = Object.keys(catalog).length
  if (providers < MINIMUM_PROVIDERS)
    throw new Error(`models.dev catalog has ${providers} providers, expected at least ${MINIMUM_PROVIDERS}`)
  return { text, providers }
}

export async function bundledModelsSnapshot() {
  const file = process.env.OPENCODE_MODELS_SNAPSHOT
  if (!file) return readFile(committedSnapshot, "utf8")
  const snapshot = await validateModelsSnapshot(await readFile(file, "utf8"))
  console.log(`bundling models.dev catalog from ${file} (${snapshot.providers} providers)`)
  return snapshot.text
}

export function modelsSnapshotPlugin(text: string): BunPlugin {
  return {
    name: "opencode-models-snapshot",
    setup(build) {
      build.onLoad({ filter: /models-dev[/\\]snapshot\.txt$/ }, () => ({ contents: text, loader: "text" }))
    },
  }
}
