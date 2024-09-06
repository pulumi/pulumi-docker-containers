import * as process from "node:process";
import * as semver from "semver";

const version = semver.parse(process.version, {
  loose: true
});

if (version?.major != 18) {
  throw new Error(`Expected node version 18.x.x, got ${process.version}`);
}
