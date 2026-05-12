import * as pulumi from "@pulumi/pulumi";

if (typeof Bun === "undefined") {
  throw new Error("Expected to be running under the Bun runtime");
}
