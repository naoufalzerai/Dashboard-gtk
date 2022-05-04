class Config:
    def __init__(self):
        self.load_menu()

    def get_menu(self):
        return self.menu

    def load_menu(self):
        self.menu = ["smb", "ssh"]