import subprocess
import datetime
import os

def run_cmd(command, cwd):
    try:
        result = subprocess.run(command, cwd=cwd, check=True, capture_output=True, text=True)
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"[ERROR] Command failed: {' '.join(command)}\nDetails: {e.stderr}")
        return None

def quantum_sync(repo_path, branch="main"):
    print(f"\n[QUANTUM SYNC] Initiating sequence for: {repo_path}")
    
    if not os.path.exists(os.path.join(repo_path, ".git")):
        print(f"[ERROR] {repo_path} is not a valid Git repository.")
        return

    status = run_cmd(["git", "status", "--porcelain"], cwd=repo_path)
    if not status:
        print("[STATUS] Absolute equilibrium. No changes to commit.")
        return

    print("[ACTION] Staging modifications...")
    run_cmd(["git", "add", "."], cwd=repo_path)

    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    commit_msg = f"Quantum Auto-Sync: {timestamp}"
    print(f"[ACTION] Committing: '{commit_msg}'")
    run_cmd(["git", "commit", "-m", commit_msg], cwd=repo_path)

    print("[ACTION] Synchronizing with remote state...")
    run_cmd(["git", "pull", "--rebase", "origin", branch], cwd=repo_path)

    print("[ACTION] Transmitting to origin...")
    push_result = run_cmd(["git", "push", "origin", branch], cwd=repo_path)
    
    if push_result is not None:
        print(f"[SUCCESS] Repository {repo_path} is now absolute.")

if __name__ == "__main__":
    # Ensure these paths perfectly match your local architecture
    repositories = [r"F:\UENCC", r"F:\LuffyStudio"]
    for repo in repositories:
        quantum_sync(repo)