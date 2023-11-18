import logging
import os
import threading

import requests

from qtCore import *
from git.repo import Repo
from git.repo.fun import is_git_dir


class GitRepository(QObject):
    """
    git repository manager
    """

    state_changed = pyqtSignal(str)
    def __init__(self, local_path):
        super(GitRepository, self).__init__()
        self.local_path = local_path

        self.screen_repo_url = "https://github.com/Mixwarebot/MixwareScreen.git"
        self.screen_repo = None
        self.screen_local_commit = None
        self.screen_remote_commit = None

        self.latest_firmware_url = 'https://api.github.com/repos/Mixwarebot/Mixware-Hyper-X-Firmware/releases/latest'
        self.latest_firmware_version = None
        self.firmware_path = 'firmware.bin'
        self.firmware_url = f'https://github.com/Mixwarebot/Mixware-Hyper-X-Firmware/releases/download/{self.latest_firmware_version}/firmware.bin'

        self._state = None
        self.initial()

        # self.check_timer = QTimer(None)
        # self.check_timer.timeout.connect(self.start_check)
        #self.check_timer.start(300000) # 10 min

        self.screen_check_thread = None
        self.screen_pull_thread = None
        self.firmware_check_thread = None
        self.firmware_download_thread = None

    def initial(self):
        """
        init git repository(local)
        :return:
        """
        if not os.path.exists(self.local_path):
            os.makedirs(self.local_path)

        git_local_path = os.path.join(self.local_path, '.git')
        if is_git_dir(git_local_path):
            self.screen_repo = Repo(self.local_path)
            self.change_state(self.tr("Upgrade is ready."))

            # self.check_thread = threading.Thread(target=self.check)
            # self.check_thread.start()
            
    def change_state(self, state: str):
        self._state = state
        logging.info(self._state)
        self.state_changed.emit(self._state)

    def screen_check(self):
        """
        update remote status
        check local commit & remote commit
        :return:
        """
        if self.screen_repo:
            if self.tr("Updating Mixware Screen.") not in self._state:
                self.change_state(self.tr("Checking Mixware Screen."))
            try:
                # os.system('git remote update origin --p')
                # self.repo.remote().update()
                self.screen_repo.remote().fetch()
                logging.debug(f"git repository FETCH_HEAD: {self.screen_repo.git.rev_parse('FETCH_HEAD')}")
                logging.debug(f"git repository HEAD: {self.screen_repo.git.rev_parse('HEAD')}")
                logging.debug(f"git repository is_dirty: {self.screen_repo.is_dirty()}")

                local_branch = self.screen_repo.active_branch
                remote_branch = self.screen_repo.remotes.origin.refs[local_branch.name]
                commits_ahead = list(self.screen_repo.iter_commits(f'{remote_branch.name}'))
                self.screen_remote_commit = str(commits_ahead[0])[0:7]
                self.screen_local_commit = str(self.commits()[0]['commit'])
                logging.debug(f'local: {self.screen_local_commit}, remote: {self.screen_remote_commit}')
                if self.tr("Updating Mixware Screen.") not in self._state:
                    self.change_state(self.tr("Mixware Screen check successful."))
            except :
                self.screen_local_commit = None
                self.screen_remote_commit = None
                if self.tr("Updating Mixware Screen.") not in self._state:
                    self.change_state(self.tr("Mixware Screen check failed."))

        # commits_ahead = list(self.repo.iter_commits(f'{remote_branch.name}..{local_branch.name}'))
        # commits_behind = list(self.repo.iter_commits(f'{local_branch.name}..{remote_branch.name}'))
        # print(f"本地分支领先远程分支 {len(commits_ahead)} 个提交")
        # print(f"本地分支落后远程分支 {len(commits_behind)} 个提交")

    def start_screen_check(self):
        self.screen_check_thread = threading.Thread(target=self.screen_check)
        self.screen_check_thread.start()

    def screen_exist_update(self):
        '''
        remote commit != local commit -> exist update -> True
        :return:
        '''
        return self.screen_remote_commit and self.screen_remote_commit != self.screen_local_commit

    def screen_pull(self):
        """
        Pull the latest code from remote
        :return:
        """
        try:
            self.change_state(self.tr("Updating Mixware Screen."))
            self.screen_repo.git.pull()
            self.screen_check()
            if self.screen_remote_commit and self.screen_local_commit == self.screen_remote_commit:
                self.change_state(self.tr("Mixware Screen update successful."))
                # os.system('sudo systemctl restart MixwareScreen')
            else:
                self.change_state(self.tr("Mixware Screen update failed."))
        except :
            self.change_state(self.tr("Mixware Screen update failed."))


    def start_screen_pull(self):
        self.screen_pull_thread = threading.Thread(target=self.screen_pull)
        self.screen_pull_thread.start()

    def commits(self):
        """
        get all commit log
        :return:
        """
        commit_log = self.screen_repo.git.log('--pretty={"commit":"%h"}', max_count=10)
        log_list = commit_log.split('\n')
        return [eval(item) for item in log_list]

    def firmware_check(self):
        self.change_state(self.tr("Checking firmware."))
        try:
            firmware_latest_version_request = requests.get(self.latest_firmware_url)
            self.latest_firmware_version = firmware_latest_version_request.json()['tag_name']
            self.change_state(self.tr("Latest firmware version is Marlin {}.".format(self.latest_firmware_version)))
        except :
            self.change_state(self.tr("firmware check error."))
        self.firmware_check_thread = None

    def start_firmware_check(self):
        self.firmware_check_thread = threading.Thread(target=self.firmware_check, daemon=True)
        self.firmware_check_thread.start()

    def get_firmware_latest_version(self):
        return self.latest_firmware_version

    def set_firmware_path(self, path):
        self.firmware_path = path + '/firmware.bin'

    def firmware_download(self):
        self.change_state(self.tr("Start download firmware."))
        try:
            firmware_request = requests.get(self.firmware_url)
            with open(self.firmware_path, 'wb') as file:
                file.write(firmware_request.content)
                self.change_state(self.tr("Firmware download successful."))
        except :
            self.change_state(self.tr("Firmware download error."))

    def start_firmware_download(self):
        self.firmware_download_thread = threading.Thread(target=self.firmware_download)
        self.firmware_download_thread.start()
