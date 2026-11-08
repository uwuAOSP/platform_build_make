# SPDX-FileCopyrightText: The uwuAOSP Project
# SPDX-License-Identifier: Apache-2.0

"""Copy only the files selected for a partition into target-files staging."""

import argparse
import os
import shutil
import stat


def copy_partition_files(source, destination, file_list):
    os.makedirs(destination, exist_ok=True)
    copied = set()
    with open(file_list, encoding="utf-8") as entries:
        for entry in entries:
            entry = entry.rstrip("\n")
            if not entry or entry in copied:
                continue
            if (entry == "." or entry != os.path.normpath(entry)
                    or os.path.isabs(entry) or entry == ".."
                    or entry.startswith("../")):
                raise ValueError(f"Invalid partition path: {entry!r}")
            src = os.path.join(source, entry)
            dst = os.path.join(destination, entry)
            mode = os.lstat(src).st_mode
            if stat.S_ISDIR(mode):
                # A listed directory does not authorize copying its children.
                os.makedirs(dst, exist_ok=True)
            else:
                os.makedirs(os.path.dirname(dst), exist_ok=True)
                # Target-files processing may modify its copies in place.
                shutil.copy2(src, dst, follow_symlinks=False)
            copied.add(entry)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source")
    parser.add_argument("destination")
    parser.add_argument("file_list")
    args = parser.parse_args()
    try:
        copy_partition_files(args.source, args.destination, args.file_list)
    except (OSError, ValueError) as error:
        parser.exit(1, f"{parser.prog}: {error}\n")


if __name__ == "__main__":
    main()
