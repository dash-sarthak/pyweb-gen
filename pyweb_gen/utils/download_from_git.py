import subprocess


def download_from_git(
    user_name: str, repo_name: str, branch: str = None, download_path: str = None
):
    download_path = download_path if download_path is not None else "."
    git_url = f"https://github.com/{user_name}/{repo_name}.git"

    clone_command: list = ["git", "clone", git_url, download_path]
    if branch is not None:
        clone_command.insert(2, "-b")
        clone_command.insert(3, branch)

    subprocess.run(
        clone_command, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT
    )
