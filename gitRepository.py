import logging
import os
import threading

from qtCore import *
from git.repo import Repo
from git.repo.fun import is_git_dir


class GitRepository(object):
    """
    git repository manager
    """

    def __init__(self, local_path, repo_url, branch='main'):
        self.local_path = local_path
        self.repo_url = repo_url
        self.repo = None

        self.local_commit = None
        self.remote_commit = None

        self.initial()

        self.check_timer = QTimer(None)
        self.check_timer.timeout.connect(self.check)
        self.check_timer.start(300000) # 10 min
        self.pull_thread = threading.Thread(target=self.pull)

    def initial(self):
        """
        init git repository(local)
        :return:
        """
        if not os.path.exists(self.local_path):
            os.makedirs(self.local_path)

        git_local_path = os.path.join(self.local_path, '.git')
        if is_git_dir(git_local_path):
            self.repo = Repo(self.local_path)

    def check(self):
        """
        update remote status
        check local commit & remote commit
        :return:
        """
        if self.repo:
            try:
                # os.system('git remote update origin --p')
                # self.repo.remote().update()
                self.repo.remote().fetch()
                logging.debug(f"git repository FETCH_HEAD: {self.repo.git.rev_parse('FETCH_HEAD')}")
                logging.debug(f"git repository HEAD: {self.repo.git.rev_parse('HEAD')}")
                logging.debug(f"git repository is_dirty: {self.repo.is_dirty()}")
            except :
                logging.error('git remote update failed.')

            local_branch = self.repo.active_branch
            remote_branch = self.repo.remotes.origin.refs[local_branch.name]
            commits_ahead = list(self.repo.iter_commits(f'{remote_branch.name}'))
            self.remote_commit = str(commits_ahead[0])[0:7]
            self.local_commit = str(self.commits()[0]['commit'])
            logging.debug(f'local: {self.local_commit}, remote: {self.remote_commit}')

        # commits_ahead = list(self.repo.iter_commits(f'{remote_branch.name}..{local_branch.name}'))
        # commits_behind = list(self.repo.iter_commits(f'{local_branch.name}..{remote_branch.name}'))
        # print(f"本地分支领先远程分支 {len(commits_ahead)} 个提交")
        # print(f"本地分支落后远程分支 {len(commits_behind)} 个提交")

    def pull(self):
        """
        Pull the latest code from remote
        :return:
        """
        self.repo.git.pull()
        self.check()
        if self.remote_commit and self.local_commit == self.remote_commit:
            os.system('sudo systemctl restart MixwareScreen')

    def update(self):
        self.pull_thread = threading.Thread(target=self.pull)
        self.pull_thread.start()

    def commits(self):
        """
        get all commit log
        :return:
        """
        commit_log = self.repo.git.log('--pretty={"commit":"%h","author":"%an","summary":"%s","date":"%cd"}',
                                       max_count=10,
                                       date='format:%Y-%m-%d %H:%M')
        log_list = commit_log.split("\n")
        return [eval(item) for item in log_list]

# if __name__ == '__main__':
#     local_path = str(Path(__file__).resolve().parent)
#     remote_path = "https://github.com/Mixwarebot/MixwareScreen.git"
#     repo = GitRepository(local_path, remote_path)