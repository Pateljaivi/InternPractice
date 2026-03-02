1. Setup & Configuration

- git config --global user.name "Name"
Sets your name globally for all repositories.

- git config --global user.email "email@example.com"
Sets your email globally for all commit history.

- git init
Turns the current folder into a new Git repository.

- git clone <url>
Copies a remote repository to your local machine.


2. Daily Workflow

- git status
Shows modified, staged, and untracked files.

- git add .
Stages all changes in the current directory.

- git commit -m "msg"
Saves staged changes with a descriptive label.

- git commit --amend
Updates the last commit with new changes or a new message.

3. Branching & Switching

- git branch
Lists all local branches.

- git switch <name>
Switches the working directory to the specified branch.

- git switch -c <name>
Creates a new branch and switches to it immediately.

- git merge <name>
Combines the specified branch into your current branch.

4. Logs & Differences

- git log --oneline
Shows commit history in a single-line format.

- git diff
Shows changes that are not yet staged.

- git diff --staged 
Shows changes that are staged but not yet committed.

5. Remote & GitHub

- git remote add origin <url>
Links your local repo to a remote server (GitHub).

- git push -u origin <branch>
Uploads local commits and sets the default remote branch.

- git pull
Fetches and merges the latest remote changes.

6. Git Flow (Workflow Extensions)

- git flow init
Initializes a new repo with the Git Flow branching structure.

- git flow feature start <name>
Creates a new feature branch based on develop.

- git flow feature finish <name>
Merges the feature back into develop and deletes the branch.

- git flow release start <version>
Starts a release branch for final bugfixes and metadata.

- git flow release finish <version>
Merges the release into main and develop and tags it.

- git flow hotfix start <version>
Creates a branch from main to fix critical production bugs.

- git flow hotfix finish <version>
Merges the fix into both main and develop immediately.

7. Undoing & Stashing

- git restore <file>
Reverts a file to the last commit (discards changes).

- git reset --soft HEAD~1
Undo the last commit but keeps your code in the folder.

- git reset --hard HEAD~1
Undo the last commit and deletes all associated changes.

- git stash
Temporarily hides uncommitted changes to clean your folder.

- git stash pop
Brings back the most recently hidden (stashed) changes.