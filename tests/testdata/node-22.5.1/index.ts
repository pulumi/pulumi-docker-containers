import * as process from "node:process";

if (process.version != "v22.5.1") {
  throw new Error(`Expected node version 22.5.1 got ${process.version}`);
}
