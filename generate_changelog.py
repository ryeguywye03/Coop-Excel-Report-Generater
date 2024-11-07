import subprocess
from datetime import datetime

def get_git_tags():
    """Retrieve all Git tags in the repository with their commit date."""
    try:
        result = subprocess.run(
            ['git', 'tag', '--list', '--format=%(refname:strip=2) %(creatordate:iso)'],
            stdout=subprocess.PIPE, text=True, check=True
        )
        tags = []
        for line in result.stdout.strip().split('\n'):
            parts = line.split(maxsplit=1)  # Split only once to separate tag and date
            if len(parts) == 2:  # Only include lines with both a tag and a date
                tags.append((parts[0], parts[1]))
        return tags  # Return list of (tag, date) tuples
    except subprocess.CalledProcessError:
        print("Error: Unable to fetch Git tags.")
        return []

def get_commits_for_tag_range(previous_tag, current_tag):
    """Retrieve commit messages between two tags."""
    try:
        result = subprocess.run(
            ['git', 'log', '--pretty=format:%s', f'{previous_tag}..{current_tag}'],
            stdout=subprocess.PIPE, text=True, check=True
        )
        commits = result.stdout.strip().split('\n')
        return commits
    except subprocess.CalledProcessError:
        print(f"Error: Unable to fetch commits for range {previous_tag}..{current_tag}.")
        return []

def get_commits_up_to_tag(tag):
    """Retrieve all commit messages up to a specific tag (for the first tag)."""
    try:
        result = subprocess.run(
            ['git', 'log', '--pretty=format:%s', tag],
            stdout=subprocess.PIPE, text=True, check=True
        )
        commits = result.stdout.strip().split('\n')
        return commits
    except subprocess.CalledProcessError:
        print(f"Error: Unable to fetch commits up to tag {tag}.")
        return []

def format_changelog_entry(version, date, commits):
    """Format a changelog entry for a given version, date, and commit messages."""
    entry = f"\n## {version} - {date}\n"
    for commit in commits:
        entry += f"- {commit}\n"
    return entry

def generate_changelog():
    """Generate the changelog by iterating over each Git tag."""
    changelog = "# Changelog\n\n"
    tags = get_git_tags()
    
    # Process each tag from oldest to newest
    for i, (tag, date) in enumerate(tags):
        if i == 0:
            # For the first tag, get all commits up to this tag
            commits = get_commits_up_to_tag(tag)
        else:
            # For subsequent tags, get the commits between this and the previous tag
            previous_tag = tags[i - 1][0]
            commits = get_commits_for_tag_range(previous_tag, tag)
        
        if commits:
            changelog += format_changelog_entry(tag, date, commits)
    return changelog

def write_changelog(changelog):
    """Write the generated changelog to CHANGELOG.md."""
    with open('CHANGELOG.md', 'w') as f:
        f.write(changelog)
    print("CHANGELOG.md updated successfully.")

def main():
    # Generate the changelog content
    changelog = generate_changelog()

    # Write the changelog content to CHANGELOG.md
    write_changelog(changelog)

if __name__ == "__main__":
    main()
