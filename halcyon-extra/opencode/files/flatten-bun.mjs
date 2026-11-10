import { readFileSync, writeFileSync, globSync, statSync } from "node:fs"
import path from "node:path"

const root = process.argv[2] ?? process.cwd()
const rootPkgPath = path.join(root, "package.json")
const rootPkg = JSON.parse(readFileSync(rootPkgPath, "utf8"))
const catalog = rootPkg.workspaces?.catalog ?? {}
const patterns = rootPkg.workspaces?.packages ?? []
const patched = rootPkg.patchedDependencies ?? {}

// which libc the embedded native assets must match; the build host may differ
// (e.g. a glibc host building a musl SEA), so allow overriding it
const targetLibc =
  process.env.OPENCODE_TARGET_LIBC ?? (process.report?.getReport()?.header?.glibcVersionRuntime ? "glibc" : "musl")
const targetLinuxLibc = targetLibc === "musl" ? "musl" : "gnu"

const depFields = ["dependencies", "devDependencies", "peerDependencies", "optionalDependencies"]
// drop native packages for platforms we never build for
function keepPlatformDependency(name) {
  if (name.startsWith("@ff-labs/fff-bin-")) return name === `@ff-labs/fff-bin-linux-x64-${targetLinuxLibc}`
  if (name.startsWith("@yuuang/ffi-rs-")) return name === `@yuuang/ffi-rs-linux-x64-${targetLinuxLibc}`
  if (name.startsWith("@lydell/node-pty-")) return name === "@lydell/node-pty-linux-x64"
  if (name.startsWith("@parcel/watcher-")) return name === `@parcel/watcher-linux-x64-${targetLibc}`
  if (name.startsWith("@opencode/pty-")) return name === `@opencode/pty-linux-x64-${targetLinuxLibc}`
  return true
}

function flattenDeps(pkg) {
  for (const field of depFields) {
    const deps = pkg[field]
    if (!deps) continue
    for (const [name, value] of Object.entries(deps)) {
      if (!keepPlatformDependency(name)) {
        delete deps[name]
        continue
      }
      if (value === "catalog:") {
        if (!catalog[name]) throw new Error(`missing catalog entry for ${name} in ${field}`)
        deps[name] = catalog[name]
      } else if (value.startsWith("catalog:")) {
        const key = value.slice("catalog:".length)
        if (!catalog[key]) throw new Error(`missing catalog entry ${key} for ${name}`)
        deps[name] = catalog[key]
      } else if (value.startsWith("workspace:")) {
        deps[name] = "*"
      }
    }
  }
  if (pkg.overrides) {
    for (const [name, value] of Object.entries(pkg.overrides)) {
      if (value === "catalog:") {
        if (!catalog[name]) throw new Error(`missing catalog entry for override ${name}`)
        pkg.overrides[name] = catalog[name]
      } else if (value.startsWith("catalog:")) {
        const key = value.slice("catalog:".length)
        if (!catalog[key]) throw new Error(`missing catalog entry ${key} for override ${name}`)
        pkg.overrides[name] = catalog[key]
      }
    }
  }
}

flattenDeps(rootPkg)
// the build driver runs under Node; tsx resolves the TypeScript build scripts
// the musl native assets are not listed by the Bun workspace but are needed for the target
rootPkg.devDependencies = {
  ...(rootPkg.devDependencies ?? {}),
  redis: "5.12.1",
  tsx: "4.20.6",
  ...(targetLibc === "musl"
    ? {
        "@ff-labs/fff-bin-linux-x64-musl": "0.10.5",
        "@opentui/core-linux-x64-musl": catalog["@opentui/core"] ?? "0.8.0",
        "@opencode/pty-linux-x64-musl": "0.4.0",
        "@parcel/watcher-linux-x64-musl": "2.5.1",
        "@yuuang/ffi-rs-linux-x64-musl": "1.3.2",
      }
    : {}),
}
rootPkg.workspaces = patterns
delete rootPkg.packageManager
delete rootPkg.patchedDependencies
delete rootPkg.trustedDependencies
writeFileSync(rootPkgPath, JSON.stringify(rootPkg, null, 2) + "\n")
writeFileSync(path.join(root, "patched-dependencies.json"), JSON.stringify(patched, null, 2) + "\n")

const dirs = new Set(["."])
for (const pattern of patterns) {
  for (const p of globSync(pattern, { cwd: root })) {
    if (statSync(path.join(root, p)).isDirectory()) dirs.add(p)
  }
}
let count = 0
for (const dir of dirs) {
  const file = path.join(root, dir, "package.json")
  if (!statSync(file, { throwIfNoEntry: false })) continue
  const pkg = JSON.parse(readFileSync(file, "utf8"))
  flattenDeps(pkg)
  delete pkg.packageManager
  writeFileSync(file, JSON.stringify(pkg, null, 2) + "\n")
  count++
}
console.log(`flattened ${count} package.json files`)
