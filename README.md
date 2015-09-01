# Git-Tracker

Git-Tracker is a simple issue tracker based on git for a git repository. The main
purpose of this tool is to manage issue on a full decentralized git repository like git bare hosted on dropbox or Bittorrent Sync.

Warning : This tool is designed to works with **Python2** on Linux and OSX **ONLY**

## Functionalities

- Issue management (Creation, assignation, comments, status).
- Gravatar icon.
- Web visualisation of git log.
- Stats visualisation
- Author(s) visualisation

## Installation

```
pip install -U https://github.com/c4software/git-tracker/archive/master.zip
```

## Usage

The usage is simple, just cd to your favorite git repository and

```
➜ cd myAwesomeSharedGit/
➜ git-tracker
Git-Tracker is now listening on http://localhost:5000/
```

## Usage command line

### Number of issue

You can invoke git-tracker-get-my-issue from your command line to check how many issue you have assigned to you.

```
➜ cd myAwesomeSharedGit/
➜ git-tracker-get-my-issue
You have 1 issue(s) assigned to you.
```
