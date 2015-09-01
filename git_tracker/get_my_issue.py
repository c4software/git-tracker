import os
import settings
from tools import sorted_ls, exec_command, load_issue

def main():
    # Get user configuration for issue creation
    try:
        settings.author_name = exec_command("git config user.name").pop()
    except:
        print ("Username unavailable. You are now : {0}".format(settings.author_name))

    try:
        settings.author_email = exec_command("git config user.email").pop()
    except:
        print ("Email unavailable. You are now : {0}".format(settings.author_email))

    count_issue = 0
    for f in sorted_ls("{0}/i*".format(settings.issue_folder)):
        try:
            issue = load_issue(settings.issue_folder,  os.path.basename(f))
            if issue["author"] == "{0} <{1}>".format(settings.author_name, settings.author_email):
                count_issue = count_issue+1
        except:
            pass

    print ("You have\033[1m {0} issue(s)\033[0m assigned to you.".format(count_issue))

if __name__ == '__main__':
    main()
