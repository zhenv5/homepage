#!/usr/bin/env bash
set -euo pipefail

export PATH="/opt/homebrew/bin:/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin"
export HOME="/Users/jiankai"

REPO_DIR="/Users/jiankai/Library/CloudStorage/Dropbox/Codes/homepage"
cd "$REPO_DIR"

# Log every run to logs/activity.log (git-ignored) while still printing to the terminal
mkdir -p logs
exec > >(tee -a logs/activity.log) 2>&1

LOG_TAG="[$(date '+%Y-%m-%d %H:%M:%S')]"
echo "$LOG_TAG [activity-sync] Checking for activity updates..."

# 1. Skip if git is in middle of rebase/merge
if [ -d .git/rebase-merge ] || [ -d .git/rebase-apply ] || [ -f .git/MERGE_HEAD ]; then
  echo "$LOG_TAG [activity-sync] Git rebase or merge in progress. Skipping."
  exit 0
fi

# 2. Safety guard: Skip if generate_index.py has uncommitted edits
if ! git diff --quiet HEAD -- .oil-ui/generate_index.py; then
  echo "$LOG_TAG [activity-sync] generate_index.py has uncommitted changes. Skipping automated sync."
  exit 0
fi

# 3. Pull latest remote master if fast-forwardable
git fetch origin master --quiet || true
if git status -uno | grep -q 'Your branch is behind'; then
  git merge origin/master --ff-only --quiet || {
    echo "$LOG_TAG [activity-sync] Cannot fast-forward origin/master. Skipping."
    exit 0
  }
fi

# 4. Run the generator to refresh commit count & heatmap SVG
/opt/homebrew/bin/python3 .oil-ui/generate_index.py > /dev/null

# 5. Check if heatmap or index changed
if git diff --quiet assets/github-heatmap.svg index.html; then
  echo "$LOG_TAG [activity-sync] No activity or heatmap changes."
  exit 0
fi

# 6. Stage only the heatmap and index.html
git add assets/github-heatmap.svg index.html
git commit -m "chore(activity): update daily contribution heatmap"
git push origin master --quiet

echo "$LOG_TAG [activity-sync] Heatmap updated and pushed to origin/master successfully."
