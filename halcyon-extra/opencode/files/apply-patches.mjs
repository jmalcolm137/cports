import { existsSync, readFileSync } from "node:fs"
import { spawnSync } from "node:child_process"
import path from "node:path"

const root = path.resolve(process.argv[2] ?? process.cwd())
const map = JSON.parse(readFileSync(path.join(root, "patched-dependencies.json"), "utf8"))

let applied = 0
let skipped = 0
for (const [key, patchRel] of Object.entries(map)) {
  const at = key.lastIndexOf("@")
  const name = key.slice(0, at)
  const version = key.slice(at + 1)
  const dir = path.join(root, "node_modules", name)
  if (!existsSync(path.join(dir, "package.json"))) {
    console.log(`skip (not installed): ${key}`)
    skipped++
    continue
  }
  const actual = JSON.parse(readFileSync(path.join(dir, "package.json"), "utf8")).version
  if (actual !== version) {
    console.log(`skip (version ${actual} != ${version}): ${name}`)
    skipped++
    continue
  }
  const r = spawnSync("patch", ["-p1", "-d", dir, "-i", path.join(root, patchRel)], { stdio: "inherit" })
  if (r.status !== 0) {
    console.log(`failed to apply (ignored): ${patchRel}`)
    skipped++
    continue
  }
  applied++
}
console.log(`applied ${applied} patches, skipped ${skipped}`)
