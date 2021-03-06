# Copyright 2018 The Bazel Authors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""LLVM pre-built distribution file names."""

import platform
import sys

def _darwin(llvm_version):
    return "clang+llvm-{llvm_version}-x86_64-apple-darwin.tar.xz".format(
        llvm_version=llvm_version)

def _windows(llvm_version):
    if platform.machine().endswith('64'):
        win_arch = "win64"
    else:
        win_arch = "win32"

    return "LLVM-{llvm_version}-{win_arch}.exe".format(
        llvm_version=llvm_version,
        win_arch=win_arch)

def _linux(llvm_version):
    arch = platform.machine()

    release_file_path = "/etc/os-release"
    with open(release_file_path) as release_file:
        lines = release_file.readlines()
        info = dict()
        for line in lines:
            line = line.decode('utf-8').strip()
            if not line:
                continue
            [key, val] = line.split('=', 1)
            info[key] = val
    if "ID" not in info:
        sys.exit("Could not find ID in /etc/os-release.")
    distname = info["ID"].strip('"')

    version = None
    if "VERSION_ID" in info:
        version = info["VERSION_ID"].strip('"')

    # NOTE: Many of these systems are untested because I do not have access to them.
    # If you find this mapping wrong, please send a Pull Request on Github.
    if arch in ["aarch64", "armv7a", "mips", "mipsel"]:
        os_name = "linux-gnu"
    elif distname == "freebsd":
        os_name = "unknown-freebsd-%s" % version
    elif distname == "suse":
        os_name = "linux-sles%s" % version
    elif distname == "ubuntu" and version == "14.04":
        os_name = "linux-gnu-ubuntu-14.04"
    elif distname == "ubuntu":
        os_name = "linux-gnu-ubuntu-16.04"
    elif distname == "arch":
        os_name = "linux-gnu-ubuntu-16.04"
    elif distname == "debian":
        os_name = "linux-gnu-ubuntu-16.04"
    elif distname == "fedora":
        os_name = "linux-gnu-Fedora%s" % version
    elif distname == "centos" and version == "7" and llvm_version == "6.0.0":
        os_name = "linux-gnu-Fedora27"
    elif distname == "centos" and version == "7" and llvm_version == "6.0.1":
        os_name = "linux-sles12.3"
    else:
        sys.exit("Unsupported linux distribution: %s-%s" % (distname, version))

    return "clang+llvm-{llvm_version}-{arch}-{os_name}.tar.xz".format(
        llvm_version=llvm_version,
        arch=arch,
        os_name=os_name)

def main():
    """Prints the pre-built distribution file name."""

    if len(sys.argv) != 2:
        sys.exit("Usage: python %s llvm_version" % sys.argv[0])

    llvm_version = sys.argv[1]

    system = platform.system()
    if system == "Darwin":
        print(_darwin(llvm_version))
        sys.exit()

    if system == "Windows":
        print(_windows(llvm_version))
        sys.exit()

    if system == "Linux":
        print(_linux(llvm_version))
        sys.exit()

    sys.exit("Unsupported system: %s" % system)

if __name__ == '__main__':
    main()
