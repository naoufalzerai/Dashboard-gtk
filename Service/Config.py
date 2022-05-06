class Config:
    def __init__(self):
        self.installed_plugin = None
        self.load_installed_plugins()

    def get_installed_plugin(self):
        return self.installed_plugin

    def load_installed_plugins(self):
        self.installed_plugin = ["smb", "ssh", "budget"]

    def load_plugins_from_repo(self):
        return None

    def install_plugin(self):
        return None

    def remove_plugin(self):
        return None

    def load_config(self):
        return None

    def save_config(self):
        return None

    def load_plugin_config(self):
        return None

    def save_plugin_config(self):
        return None
