#!/usr/bin/env python3
"""
Script to create git tags corresponding to Docker tags.

This allows Dependabot to update images that use our images as bases.
https://docs.github.com/en/code-security/dependabot/ecosystems-supported-by-dependabot/supported-ecosystems-and-repositories#docker
"""

import argparse
import subprocess
import sys
from typing import List, Set


def run_command(cmd: List[str]) -> subprocess.CompletedProcess[str]:
    print(f"Running: `{' '.join(cmd)}`")
    try:
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        if result.stdout:
            print(f"  stdout: {result.stdout.strip()}")
        if result.stderr:
            print(f"  stderr: {result.stderr.strip()}")
        return result
    except subprocess.CalledProcessError as e:
        print(f"Command failed with exit code {e.returncode}")
        print(f"  stdout: {e.stdout}")
        print(f"  stderr: {e.stderr}")
        raise


def configure_git(username: str = "pulumi-bot", email: str = "bot@pulumi.com"):
    run_command(["git", "config", "user.name", username])
    run_command(["git", "config", "user.email", email])


def tag_exists_locally(tag: str) -> bool:
    result = run_command(["git", "tag", "-l", tag])
    return tag in result.stdout.strip().split("\n") if result.stdout.strip() else False


def delete_tag(tag: str):
    """Delete a tag locally & remotely. Assumes we have a current checkout with the tags present."""
    if tag_exists_locally(tag):
        run_command(["git", "tag", "-d", tag])
        run_command(["git", "push", "origin", f":refs/tags/{tag}"])


def create_and_push_tag(tag: str):
    delete_tag(tag)
    run_command(["git", "tag", tag])
    run_command(["git", "push", "origin", tag])


def generate_git_tags(pulumi_version: str, tag_latest: bool) -> Set[str]:
    tags = set[str]()

    tags.add(pulumi_version)
    tags.add(f"{pulumi_version}-amd64")
    tags.add(f"{pulumi_version}-arm64")
    tags.add(f"{pulumi_version}-nonroot")
    tags.add(f"{pulumi_version}-nonroot-amd64")
    tags.add(f"{pulumi_version}-nonroot-arm64")
    tags.add(f"{pulumi_version}-debian")
    tags.add(f"{pulumi_version}-debian-amd64")
    tags.add(f"{pulumi_version}-debian-arm64")
    tags.add(f"{pulumi_version}-ubi")
    if tag_latest:
        tags.add("latest")
        tags.add("latest-nonroot")

    return tags


def main():
    parser = argparse.ArgumentParser(description="Create git tags for Docker releases")
    parser.add_argument(
        "--pulumi-version", required=True, help="Pulumi version (e.g., 3.186.0)"
    )
    parser.add_argument(
        "--tag-latest", action="store_true", help="Also create latest tags"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what tags would be created without creating them",
    )
    args = parser.parse_args()

    all_tags = generate_git_tags(args.pulumi_version, args.tag_latest)
    print("Tags:")
    for tag in sorted(all_tags):
        print(f"  {tag}")

    if args.dry_run:
        print("\nDry run mode - no tags were created")
        return

    configure_git()

    failed_tags: list[str] = []

    for tag in sorted(all_tags):
        try:
            print(f"\nCreating tag: {tag}")
            create_and_push_tag(tag)
        except subprocess.CalledProcessError as e:
            print(f"Failed to create tag {tag}: {e}")
            failed_tags.append(tag)
            continue

    if failed_tags:
        print(f"\nFailed to create {len(failed_tags)} tags:")
        for tag in failed_tags:
            print(f"  {tag}")
        sys.exit(1)
    else:
        print(f"\nSuccessfully created and pushed {len(all_tags)} tags!")


if __name__ == "__main__":
    main()
