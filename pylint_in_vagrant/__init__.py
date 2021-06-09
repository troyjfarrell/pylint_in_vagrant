"Run Pylint on files inside a Vagrant virtual machine"
import argparse
import os.path
import subprocess
import sys
import typing


def build_pylint_args(
    config: typing.Dict[str, typing.Any]
) -> typing.List[str]:
    "Build a Pylint command line as a list of arguments"
    pylint: str = config["pylint"]
    prefix: str = config["prefix"]
    rawfiles: typing.List[str] = config["files"]
    files = (
        [os.path.join(prefix, f) for f in rawfiles]
        if prefix is not None
        else rawfiles
    )
    return [pylint] + files


def call_pylint_in_vagrant(
    vagrant_cmd: str,
    vagrant_dir: str,
    args: typing.List[str],
    directory: typing.Optional[str],
) -> typing.Tuple[int, str, str]:
    "Use Vagrant to run Pylint via SSH"
    argv = [vagrant_cmd, "ssh", "--"]
    if directory is not None:
        argv.extend(["cd", directory, "&&"])
    argv.extend(args)
    with subprocess.Popen(
        argv, stdin=subprocess.PIPE, stdout=subprocess.PIPE, cwd=vagrant_dir
    ) as process:
        out, err = process.communicate()
        outs = out.decode("UTF-8") if out is not None else ""
        errs = err.decode("UTF-8") if err is not None else ""
        return (process.returncode, outs, errs)


def configure() -> typing.Dict[str, typing.Any]:
    "Convert command-line arguments to a configuration"
    parser = argparse.ArgumentParser(description="Run Pylint in Vagrant")
    parser.add_argument(
        "pylint",
        metavar="pylint",
        type=str,
        help="full path to Pylint inside the virtual machine",
    )
    parser.add_argument(
        "files",
        metavar="file",
        type=str,
        nargs="+",
        help="files to lint with Pylint inside the virtual machine",
    )
    parser.add_argument(
        "--directory",
        metavar="directory",
        type=str,
        help="the path to use as the working directory inside the virtual machine",
    )
    parser.add_argument(
        "--prefix",
        metavar="file_prefix",
        type=str,
        help="the path inside the virtual machine where the files are found",
    )
    parser.add_argument(
        "--vagrant-dir",
        metavar="vagrant_dir",
        default=".",
        type=str,
        help="the path to the directory containing the Vagrantfile",
    )
    parser.add_argument(
        "--vagrant-cmd",
        metavar="vagrant_cmd",
        default="vagrant",
        type=str,
        help="the command used to execute Vagrant",
    )
    args = parser.parse_args()
    return vars(args)


def main():
    "The main event"
    config = configure()
    args = build_pylint_args(config)
    status, out, err = call_pylint_in_vagrant(
        config["vagrant_cmd"], config["vagrant_dir"], args, config["directory"]
    )
    sys.stdout.write(out)
    if err:
        sys.stderr.write(err)
    sys.exit(status)
