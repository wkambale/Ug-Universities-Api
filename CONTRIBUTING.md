# <a name="contribution-head">Contribution Overview</a>

Thank you for your help in improving this project.

All contributors are welcome. This project is community-built and welcomes collaboration. Contributors are expected to adhere to our [Code of Conduct (In Progress)](#).

All set to contribute? Grab an open issue with the [help wanted](https://github.com/stuartelimu/vaccination-centres/issues?q=is%3Aissue+is%3Aopen+label%3A%22help+wanted%22) or [good first issue](https://github.com/stuartelimu/vaccination-centres/issues?q=is%3Aissue+is%3Aopen+label%3A%22good+first+issue%22) label and jump in.

Create a [new issue](https://github.com/stuartelimu/vaccination-centres/issues/new) if needed. All [pull requests](https://github.com/stuartelimu/vaccination-centres/pulls) should ideally reference an open [issue](https://github.com/stuartelimu/vaccination-centres/issues?q=is%3Aopen+is%3Aissue). Include keywords in your pull request descriptions, as well as commit messages, to [automatically close related issues in GitHub](https://help.github.com/en/github/managing-your-work-on-github/closing-issues-using-keywords).

**Sections**

- <a href="#contribution">General Contribution Flow</a>
  - <a href="#commit-signing">Signing-off on Commits (Developer Certificate of Origin)</a>
  - <a href="#dev-setup">Development Setup</a>
    - <a href="#fork">Fork and Clone Repository</a>
    - <a href="#install">Setup and Installation</a>
    - <a href="#future-contribution">Making Contributions</a>
    - <a href="#submitting">Submitting your changes (Pull Request)</a>

# <a name="contribution">General Contribution Flow</a>

## <a name="commit-signing">Signing-off on Commits (Developer Certificate of Origin)</a>

To contribute to this project, you must agree to the Developer Certificate of
Origin (DCO) for each commit you make. The DCO is a simple statement that you,
as a contributor, have the legal right to make the contribution.

See the [DCO](https://developercertificate.org) file for the full text of what you must agree to
and how it works [here](https://github.com/probot/dco#how-it-works).
To signify that you agree to the DCO for contributions, you simply add a line to each of your
git commit messages:

```
Signed-off-by: John Doe <john.doe@example.com>
```

In most cases, you can add this signoff to your commit automatically with the
`-s` or `--signoff` flag to `git commit`. You must use your real name and a reachable email
address (sorry, no pseudonyms or anonymous contributions). An example of signing off on a commit (sign-off will be automatically included):

```
$ commit -s -m “my commit message”
```

To ensure all your commits are signed, you may (optional) choose to add this alias to your global `.gitconfig`:

_~/.gitconfig_

```
[alias]
  amend = commit -s --amend
  cm = commit -s -m
  commit = commit -s
```

Or you may configure your IDE of your choice to automatically sign-off commits for you.

## <a name="dev-setup">Development Setup</a>

### <a name="fork">Fork and clone the repository</a>

Fork this repository by clicking on the fork button on the top of this page. This will create a copy of this repository in your account.

Now clone the forked repository to your machine. Go to your GitHub account, open the forked repository, click on the code button and then click the copy to clipboard icon.

```
git clone https://github.com/WesleyKambale/ug-universities-api.git
```

Navigate to the project directory

```
cd ug-universities-api
```

### Keeping Your Fork Up to Date

While this isn't a necessary step, if you plan on doing anything more than a tiny quick fix, you'll want to make sure you keep your fork up to date by tracking the original "upstream" repo that you forked earlier.

To do this, you'll need to add a remote:

```
git remote add upstream https://github.com/WesleyKambale/ug-universities-api.git
```

### Verify the new remote named 'upstream'

```
git remote -v
```

You will get something like:

```
origin	https://github.com/your-user-name/ug-universities-api.git (fetch)
origin	https://github.com/your-user-name/ug-universities-api.git (push)
upstream	https://github.com/stuartelimu/ug-universities-api.git (fetch)
upstream	https://github.com/stuartelimu/ug-universities-api.git (push)
```

Whenever you want to update your fork with the latest upstream changes, you'll need to first fetch the upstream repo's branches and latest commits to bring them into your repository:

```
git fetch upstream
```

If there are no unique commits on the local master/main branch, git will simply perform a fast-forward.

However, if you have been making changes on master (in the vast majority of cases you probably shouldn't be - see the next section, you may have to deal with conflicts. When doing so, be careful to respect the changes made upstream.

Now, your local master branch is up-to-date with everything modified upstream.

### <a name="install">Setup and installation</a>

Ensure GDAL Library is installed:

For Windows users, please refer [here](https://pypi.org/project/GDAL/#windows).

For Ubuntu:

```
sudo apt-get install gdal-bin
```

For MacOS (via HomeBrew):

```
brew install gdal
```

Next in the project directory, create a virtual environment using the following command:

```
python3 -m venv env
```

Once you’ve created a virtual environment, you may activate it:

On Windows, run:

```
env\Scripts\activate.bat
```

On Linux or MacOS, run:

```
source env/bin/activate
```

You can install the project requirements from the `requirements.txt` file using the following command

```
python -m pip install -r requirements.txt
```

Create a `.env` file, copy all the contents from `.env.sample` file and paste them in the `.env` file you just created.

Make migrations to sync and create a database:

```
python manage.py migrate
```

Run the web app using this command:

```
python manage.py runserver
```

On your browser, navigate to:

```
http://127.0.0.1:8000/
```

To deactivate a virtual environment insider (env), type:

```
deactivate
```

### <a name="future-contribution">Making contributions</a>

Create a new branch where your change(s) will reside, run:

```
git checkout -b new-branch
```

Example: The `new-branch` here could be something like:

```
git checkout -b issue/your-username/#001
```

, where 001 is the issue number.

Make the necessary changes, commit and then push to remote server.

For example:

If you fixed a typo in `README.md` file, run: `git status` to see the files that have been changed

Add these changes to your branch

```
git add README.md
```

Now commit these changes to your branch with a meaningful message, run:

```
git commit -m "fix typo in README.md file"
```

Push these changes to github

```
git push origin new-branch
```

### <a name="submitting"> Submitting your changes (Pull Request) </a>

Before submitting your pull request, you might want to do a few things to clean up your branch and make it as simple as possible for the original repo's maintainer to test, accept, and merge your work.

In the time that you've been working on your changes, if any commits have been made to the upstream master branch, you will need to rebase your development branch so that merging it will be a simple fast-forward that won't require any conflict resolution work.

### Fetch upstream master and merge with your repo's master branch

```
git fetch upstream
git checkout master
git merge upstream/master
```

### If there were any new commits, rebase your development branch

```
git checkout issue/jdoe/567
git rebase master
```

Now, it may be desirable to squash some of your smaller commits down into a small number of larger more cohesive commits. You can do this with an interactive rebase:

### Rebase all commits on your development branch

```
git checkout
git rebase -i master
```

This will open up a text editor where you can specify which commits to squash.

Once you've committed and pushed all of your changes to GitHub, go to the page for your fork on GitHub, select your development branch, and click the pull request button.

If you need to make any adjustments to your pull request, just push the updates to GitHub. Your pull request will automatically track the changes in your development branch and update it.

Submit your changes for review, If you go to your repository on GitHub, you'll see a [Compare & pull request](https://docs.github.com/en/github/collaborating-with-pull-requests/proposing-changes-to-your-work-with-pull-requests/about-comparing-branches-in-pull-requests) button. Click on that button.

Add a brief description and submit the pull request.

Soon we'll be merging all your changes into the master branch of this project. You will get push notification on github and a notification email once the changes have been merged.
