import { readFileSync } from "node:fs"
import path from "node:path"

const rootPkgPath = path.resolve(import.meta.dirname, "../../../package.json")
const rootPkg = JSON.parse(readFileSync(rootPkgPath, "utf8"))

const CHANNEL = process.env["OPENCODE_CHANNEL"] || "latest"
const VERSION = process.env["OPENCODE_VERSION"] || rootPkg.version
const IS_PREVIEW = CHANNEL !== "latest"
const team: string[] = []

export const Script = {
  get channel() {
    return CHANNEL
  },
  get version() {
    return VERSION
  },
  get preview() {
    return IS_PREVIEW
  },
  get team() {
    return team
  },
}
