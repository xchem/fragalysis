#!/usr/bin/env python
#
# A test utility to allow concurrent downloads of targets
# and developed to stress-test the download mechanism.
# Developed for issue #1952.

import argparse
import datetime
from multiprocessing import Process
import os
import shutil
import time

from frequests.download import download_target


_DOWNLOAD_DIR: str = f"/tmp/download-target-stress-test"

if __name__ == "__main__":

    parser = argparse.ArgumentParser(
        prog="download_target_stress_test",
        description="A stress-test for the download_target function,"
            " You define the concurrency, and each download is written to a separate"
            f" sub-directory in '{_DOWNLOAD_DIR}'"
            " with the value of the concurrency number (i.e. 1..N)",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument("--tas",
                        type=str,
                        help="A Target Access String",
                        required=True)
    parser.add_argument("--concurrency", "-c",
                        type=int,
                        help="Number of concurrent processes",
                        default=1)
    parser.add_argument("--stack", "-s",
                        type=str,
                        help="An optional stack identity",
                        default="staging")
    parser.add_argument("--target", "-t",
                        type=str,
                        help="An optional Target name",
                        default="A71EV2A")
    parser.add_argument("--token",
                        type=str,
                        help="An optional API access token")

    args = parser.parse_args()

    # Run each download (to a separate local destination)
    # as a concurrent set of (parallel) processes.

    start_time_s: float = time.time()
    processes: list[Process] = []

    for c in range(args.concurrency):

        iteration: int = c + 1

        # We need to wipe (and recreate) each target download directory
        destination: str = f"{_DOWNLOAD_DIR}/{iteration:02d}"
        if os.path.isdir(destination):
            shutil.rmtree(destination)
        os.makedirs(destination)

        # Create a Process, start it,
        # and add it to a list of running processes
        process = Process(
            target=download_target,
            args=(args.target, args.tas, iteration, args.stack),
            kwargs={"destination": destination},
        )
        process.start()
        processes.append(process)

    # Wait for each process
    for p in processes:
        p.join()

    now = datetime.datetime.now()
    elapsed_s: float = time.time() - start_time_s
    print(f"{now} Elapsed(S)={elapsed_s}")
