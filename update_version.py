import re
import subprocess
from datetime import datetime

def get_latest_version():
    """Read the current version from version.txt."""
    try:
        with open('version.txt', 'r') as f:
            return f.read().strip()
    except FileNotFoundError:
        print("Error: version.txt not found.")
        return None

def bump_version(version, part='patch'):
    """Increment version based on the specified part (major, minor, patch)."""
    major, minor, patch = map(int, version.split('.'))
    if part == 'major':
        major += 1
        minor, patch = 0, 0
    elif part == 'minor':
        minor += 1
        patch = 0
    else:  # patch
        patch += 1
    return f"{major}.{minor}.{patch}"

def update_version_file(new_version):
    """Write the new version to version.txt."""
    with open('version.txt', 'w') as f:
        f.write(new_version)
    print(f"Updated version.txt to {new_version}")

def update_changelog(new_version):
    """Append a new version entry to the changelog."""
    entry = f"\n## {new_version} - {datetime.now().strftime('%Y-%m-%d')}\n"
    entry += "- Auto-generated changelog entry.\n"
    with open('CHANGELOG.md', 'a') as f:
        f.write(entry)
    print(f"Updated CHANGELOG.md with version {new_version}")

def commit_changes(new_version):
    """Commit the changes to Git."""
    try:
        subprocess.run(['git', 'add', 'CHANGELOG.md', 'version.txt'], check=True)
        subprocess.run(['git', 'commit', '-m', f'chore: bump version to {new_version}'], check=True)
        subprocess.run(['git', 'tag', f'v{new_version}'], check=True)
        subprocess.run(['git', 'push', '--follow-tags'], check=True)
        print(f"Committed and pushed changes with tag v{new_version}")
    except subprocess.CalledProcessError as e:
        print(f"Error committing changes: {e}")

def main():
    # Step 1: Get the current version
    current_version = get_latest_version()
    if not current_version:
        return

    # Step 2: Bump the version
    part = input("Enter version part to bump (major, minor, patch): ").strip().lower()
    new_version = bump_version(current_version, part)

    # Step 3: Update version.txt
    update_version_file(new_version)

    # Step 4: Update CHANGELOG.md
    update_changelog(new_version)

    # Step 5: Commit changes
    commit_changes(new_version)

if __name__ == "__main__":
    main()
