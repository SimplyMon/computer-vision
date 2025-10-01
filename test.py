import os
import subprocess
import random
from datetime import datetime, timedelta, timezone

AUTHOR_NAME = "mon"  #
AUTHOR_EMAIL = "mon.dev005@gmail.com"
REPO_DIR = "computer-vision"
DRY_RUN = False
PUSH = True
REMOTE_URL = "https://github.com/SimplyMon/computer-vision.git"

MESSAGES = [
    "Update code",
    "Minor fix",
    "Refactor function",
    "Tweak performance",
    "Docs update",
    "Add tests",
    "Cleanup",
    "Improve logging",
    "Experiment",
    "Adjust formatting",
]


def run_git(args, env=None, cwd=None):
    cmd = ["git"] + args
    subprocess.run(cmd, env=env, cwd=cwd, check=True)


def iso_for_git(dt):
    return dt.strftime("%Y-%m-%d %H:%M:%S +0000")


def ensure_dir(path):
    if os.path.exists(path) and os.listdir(path):
        raise SystemExit(f"Error: {path} already exists and is not empty")
    os.makedirs(path, exist_ok=True)


def main():
    ensure_dir(REPO_DIR)
    print(f"Creating repo in {REPO_DIR}  (DRY_RUN={DRY_RUN}, PUSH={PUSH})")

    run_git(["init"], cwd=REPO_DIR)
    run_git(["config", "user.name", AUTHOR_NAME], cwd=REPO_DIR)
    run_git(["config", "user.email", AUTHOR_EMAIL], cwd=REPO_DIR)

    with open(os.path.join(REPO_DIR, "README.md"), "w") as f:
        f.write("# Computer Vision Course\n")
    run_git(["add", "README.md"], cwd=REPO_DIR)
    run_git(["commit", "-m", "Initial commit"], cwd=REPO_DIR)

    start = datetime(2024, 10, 1, tzinfo=timezone.utc)
    end = datetime(2024, 12, 31, tzinfo=timezone.utc)
    cur = start
    total = 0

    while cur <= end:
        weekday = cur.weekday()

        if weekday < 5:
            commits_today = random.randint(3, 7)
            if random.random() < 0.1:
                commits_today = 0
        else:
            commits_today = random.randint(0, 2)

        for _ in range(commits_today):
            hour = min(max(int(random.normalvariate(13, 2)), 9), 20)
            minute = random.randint(0, 59)
            second = random.randint(0, 59)
            dt = datetime(
                cur.year, cur.month, cur.day, hour, minute, second, tzinfo=timezone.utc
            )

            git_ts = iso_for_git(dt)
            msg = random.choice(MESSAGES)

            env = os.environ.copy()
            env.update(
                {
                    "GIT_AUTHOR_NAME": AUTHOR_NAME,
                    "GIT_AUTHOR_EMAIL": AUTHOR_EMAIL,
                    "GIT_COMMITTER_NAME": AUTHOR_NAME,
                    "GIT_COMMITTER_EMAIL": AUTHOR_EMAIL,
                    "GIT_AUTHOR_DATE": git_ts,
                    "GIT_COMMITTER_DATE": git_ts,
                }
            )

            run_git(["commit", "--allow-empty", "-m", msg], env=env, cwd=REPO_DIR)
            total += 1

        cur += timedelta(days=1)

    print(f"Done. Created {total} commits between Oct–Dec 2024.")

    if not DRY_RUN:
        run_git(["branch", "-M", "main"], cwd=REPO_DIR)
        if REMOTE_URL:
            run_git(["remote", "add", "origin", REMOTE_URL], cwd=REPO_DIR)
        if PUSH:
            print("Pushing to GitHub...")
            run_git(["push", "-u", "origin", "main"], cwd=REPO_DIR)
            print("Push complete.")


if __name__ == "__main__":
    main()
