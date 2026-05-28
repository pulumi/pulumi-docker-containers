import { execSync } from "node:child_process";

// The image's global pnpm is the latest 10.x. Corepack's shim, when enabled,
// instead reads the `packageManager` field in package.json and runs that exact
// version. Observing the pinned 9.x below is proof that corepack is active for the
// current node version, not just that `pnpm` exists.
const expected = "9.15.0";

const actual = execSync("pnpm --version").toString().trim();

if (actual !== expected) {
  throw new Error(
    `Expected corepack-managed pnpm ${expected}, got ${actual}. ` +
      `Is corepack enabled for this node version?`,
  );
}
