#!/usr/bin/env python3
"""Verify or explicitly regenerate hai-jp-report's pinned, offline vendor bundle.

No arguments (or --check) verifies the bundle. Regeneration requires:
    python3 dev/sync_hai_jp_vendor.py --sync --commit <PINNED_COMMIT>

Uses only the Python standard library and local Git objects; never fetches.
Changing the upstream pin requires a reviewed change to PINNED_COMMIT below.
"""

import argparse
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import stat
import subprocess
import sys
import tempfile


PINNED_COMMIT = "03bc944a0c4a9f0b2a66eab065b30de5c529bf08"
UPSTREAM_URL = "https://github.com/coji/natural-japanese"
SOURCE_ROOT = "skills/natural-japanese"
VENDOR_ROOT = "skills/hai-jp-report/vendor/natural-japanese"
MANIFEST_NAME = "UPSTREAM.json"


class ValidationError(Exception):
    """A source, bundle, or path does not meet the vendoring contract."""


def digest(data):
    return hashlib.sha256(data).hexdigest()


def safe_path(root, relative):
    """Reject traversal and symlinks before reading or writing a repo path."""
    parts = PurePosixPath(relative)
    if (not relative or parts.is_absolute() or ".." in parts.parts
            or "\\" in relative or parts.as_posix() != relative):
        raise ValidationError(f"Unsafe relative path: {relative!r}")
    path = root
    for part in parts.parts:
        path = path / part
        if path.is_symlink():
            raise ValidationError(f"Symlink is not allowed: {path}")
    return path


def scan_tree(root):
    """Return every file/directory, including hidden entries, without links."""
    if root.is_symlink() or not root.is_dir():
        raise ValidationError(f"Expected a real directory: {root}")
    files, directories = set(), set()

    def visit(directory):
        with os.scandir(directory) as entries:
            for entry in sorted(entries, key=lambda item: item.name):
                relative = Path(entry.path).relative_to(root).as_posix()
                safe_path(root, relative)
                mode = entry.stat(follow_symlinks=False).st_mode
                if stat.S_ISDIR(mode):
                    directories.add(relative)
                    visit(Path(entry.path))
                elif stat.S_ISREG(mode):
                    files.add(relative)
                else:
                    raise ValidationError(f"Not a regular file or directory: {entry.path}")

    visit(root)
    return files, directories


def git(root, *arguments):
    # Prevent a partial clone from lazily fetching a missing object.
    env = os.environ.copy()
    env.update(GIT_NO_LAZY_FETCH="1", GIT_TERMINAL_PROMPT="0")
    result = subprocess.run(
        ["git", "-c", "protocol.allow=never", "-C", str(root), *arguments],
        stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=env, timeout=30,
    )
    if result.returncode:
        detail = result.stderr.decode("utf-8", errors="replace").strip()
        raise ValidationError(f"Local Git command failed: {detail}")
    return result.stdout


def require_same_set(label, actual, expected):
    missing = sorted(expected - actual)
    extra = sorted(actual - expected)
    if missing or extra:
        details = []
        if missing:
            details.append("missing: " + ", ".join(missing))
        if extra:
            details.append("unexpected: " + ", ".join(extra))
        raise ValidationError(f"{label} differs ({'; '.join(details)})")


def load_pinned_files(root):
    """Read pinned Git blobs and require the working upstream to match them."""
    top = Path(git(root, "rev-parse", "--show-toplevel").decode().strip()).resolve()
    if top != root:
        raise ValidationError("--repo-root must identify the repository root")
    if git(root, "cat-file", "-t", PINNED_COMMIT).strip() != b"commit":
        raise ValidationError("The pinned object is not a commit")
    tree = git(root, "ls-tree", "-r", "-z", "--full-tree", PINNED_COMMIT,
               "--", SOURCE_ROOT, "LICENSE")
    files = {}
    source_paths = set()
    for record in tree.split(b"\0"):
        if not record:
            continue
        metadata, path_bytes = record.split(b"\t", 1)
        mode, kind, object_id = metadata.decode("ascii").split()
        source = path_bytes.decode("utf-8")
        source_path = safe_path(root, source)
        if kind != "blob" or mode not in {"100644", "100755"}:
            raise ValidationError(f"Unsupported upstream entry: {source}")
        if source == "LICENSE":
            destination = "LICENSE"
        elif source.startswith(SOURCE_ROOT + "/"):
            source_paths.add(source[len(SOURCE_ROOT) + 1:])
            destination = source[len(SOURCE_ROOT) + 1:]
            if destination == "SKILL.md":
                destination = "GUIDE.md"
        else:
            raise ValidationError(f"Unexpected upstream path: {source}")
        safe_path(root, VENDOR_ROOT + "/" + destination)
        if (destination in files or destination == MANIFEST_NAME
                or PurePosixPath(destination).name == "SKILL.md"):
            raise ValidationError(f"Unsafe or colliding bundle entry: {destination}")
        data = git(root, "cat-file", "blob", object_id)
        if not source_path.is_file() or source_path.read_bytes() != data:
            raise ValidationError(f"Working upstream differs from pin: {source}")
        files[destination] = {"data": data, "upstream_path": source, "mode": mode}

    if "GUIDE.md" not in files or "LICENSE" not in files:
        raise ValidationError("Pinned source must contain SKILL.md and root LICENSE")
    actual_source, _ = scan_tree(safe_path(root, SOURCE_ROOT))
    require_same_set("Working upstream file set", actual_source, source_paths)
    return files


def expected_bundle(files):
    manifest = {
        "schema_version": 1,
        "upstream": {
            "repository": UPSTREAM_URL,
            "commit": PINNED_COMMIT,
            "skill_path": SOURCE_ROOT,
        },
        "bundle_path": VENDOR_ROOT,
        "transformation": "SKILL.md renamed to GUIDE.md; all copied file bytes unchanged.",
        "files": {
            name: {"upstream_path": item["upstream_path"],
                   "sha256": digest(item["data"]), "mode": item["mode"]}
            for name, item in sorted(files.items())
        },
    }
    bundle = {name: (item["data"], int(item["mode"], 8) & 0o777)
              for name, item in files.items()}
    manifest_bytes = (json.dumps(manifest, ensure_ascii=False, indent=2) + "\n").encode("utf-8")
    bundle[MANIFEST_NAME] = (manifest_bytes, 0o644)
    return bundle


def expected_directories(bundle):
    return {parent.as_posix() for name in bundle
            for parent in PurePosixPath(name).parents if parent != PurePosixPath(".")}


def check_bundle(root, bundle):
    files, directories = scan_tree(root)
    require_same_set("Bundle file set", files, set(bundle))
    require_same_set("Bundle directory set", directories, expected_directories(bundle))
    for name, (data, mode) in sorted(bundle.items()):
        path = safe_path(root, name)
        if digest(path.read_bytes()) != digest(data):
            raise ValidationError(f"Bundle checksum mismatch: {name}")
        if stat.S_IMODE(path.stat().st_mode) != mode:
            raise ValidationError(f"Bundle permission mode mismatch: {name}")


def atomic_write(path, data, mode):
    # Replace files rather than changing existing hard-link targets in place.
    temporary = None
    try:
        with tempfile.NamedTemporaryFile(dir=path.parent, prefix=".vendor-", delete=False) as stream:
            temporary = Path(stream.name)
            stream.write(data)
            stream.flush()
            os.fchmod(stream.fileno(), mode)
        os.replace(temporary, path)
    finally:
        if temporary is not None and temporary.exists():
            temporary.unlink()


def sync_bundle(root, bundle):
    root.mkdir(parents=True, exist_ok=True)
    files, directories = scan_tree(root)  # Validate all entries before any removal.
    for name in sorted(files - set(bundle)):
        safe_path(root, name).unlink()
    extra_directories = directories - expected_directories(bundle)
    for name in sorted(extra_directories, key=lambda item: (item.count("/"), item), reverse=True):
        safe_path(root, name).rmdir()
    for name in sorted(expected_directories(bundle), key=lambda item: (item.count("/"), item)):
        safe_path(root, name).mkdir(exist_ok=True)
    # Publish the deterministic manifest last.
    for name in sorted(bundle, key=lambda item: (item == MANIFEST_NAME, item)):
        data, mode = bundle[name]
        path = safe_path(root, name)
        if (not path.exists() or path.read_bytes() != data
                or stat.S_IMODE(path.stat().st_mode) != mode):
            atomic_write(path, data, mode)
    check_bundle(root, bundle)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    action = parser.add_mutually_exclusive_group()
    action.add_argument("--check", action="store_true", help="verify only (the default)")
    action.add_argument("--sync", action="store_true", help="explicitly regenerate the vendor bundle")
    parser.add_argument("--commit", help="acknowledge the pinned upstream commit; required with --sync")
    parser.add_argument("--repo-root", type=Path, default=Path(__file__).resolve().parents[1],
                        help="repository root (default: the parent of this script's dev directory)")
    args = parser.parse_args(argv)
    if args.sync and args.commit != PINNED_COMMIT:
        parser.error(f"--sync requires --commit {PINNED_COMMIT}")
    if args.commit is not None and args.commit != PINNED_COMMIT:
        parser.error("--commit differs from this helper's reviewed pin")
    try:
        repo = args.repo_root.resolve(strict=True)
        bundle = expected_bundle(load_pinned_files(repo))
        vendor = safe_path(repo, VENDOR_ROOT)
        if args.sync:
            sync_bundle(vendor, bundle)
        else:
            check_bundle(vendor, bundle)
        verb = "Synced and verified" if args.sync else "Verified"
        print(f"{verb} {len(bundle) - 1} upstream files + {MANIFEST_NAME} at {PINNED_COMMIT} (offline).")
        return 0
    except (ValidationError, OSError, subprocess.TimeoutExpired) as error:
        print(f"ERROR: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
