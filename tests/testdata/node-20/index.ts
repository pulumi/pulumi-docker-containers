import * as process from "node:process";
import * as semver from "semver";

const version = semver.parse(process.version, {
  loose: true
});

if (version?.major != 20) {
  throw new Error(`Expected node version 20.x.x, got ${process.version}`);
}
