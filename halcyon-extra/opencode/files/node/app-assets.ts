import { spawnSync } from "node:child_process"
import { readFile } from "node:fs/promises"
import path from "node:path"
import { promisify } from "node:util"
import { brotliCompress, constants } from "node:zlib"
import { AppArchive } from "../src/app-archive"
import { collectFiles } from "./files"

export async function buildAppArchive(channel: string, options?: { skipBuild?: boolean }) {
  if (options?.skipBuild) return AppArchive.encode([])
  const root = path.resolve(import.meta.dirname, "../../app")
  if (!process.env.OPENCODE_SKIP_APP_BUILD) {
    const vite = path.resolve(import.meta.dirname, "../../../node_modules/vite/bin/vite.js")
    const result = spawnSync(process.execPath, [vite, "build"], {
      cwd: root,
      stdio: "inherit",
      env: { ...process.env, OPENCODE_CHANNEL: channel, VITE_OPENCODE_SERVER_MODE: "origin" },
    })
    if (result.error) throw result.error
    if (result.status !== 0) throw new Error(`vite build exited with status ${result.status}`)
  }
  return AppArchive.encode(
    await Promise.all(
      (await collectFiles(path.join(root, "dist")))
        .map((key) => key.replaceAll(path.sep, "/"))
        .filter((key) => !key.endsWith(".map"))
        .toSorted()
        .map(async (key) => {
          const body = await readFile(path.join(root, "dist", key))
          // Independent entries let the server materialize only assets the browser requests.
          return [key, await compress(body, channel)] as const
        }),
    ),
  )
}

function compress(body: Buffer, channel: string) {
  return promisify(brotliCompress)(body, {
    params: {
      [constants.BROTLI_PARAM_QUALITY]: channel === "beta" ? 6 : 11,
      [constants.BROTLI_PARAM_SIZE_HINT]: body.length,
    },
  })
}
