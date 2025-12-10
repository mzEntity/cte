from utils.interactive import getch

class MyVim:
    def __init__(self):
        self._mode = 'normal'
        self._active = False
        
        self._operate_dict = {
            'normal': {
                'i': self._change_mode_to_insert,
                'a': self._change_mode_to_insert,
                'o': self._change_mode_to_insert,
                ':': self._change_mode_to_command
            },
            'insert': {
                'ESC': self._change_mode_to_normal
            },
            'command': {
                'ESC': self._change_mode_to_normal
            }
        }
        
    def _normal_mode_func(self, key):
        pass
    
    def _insert_mode_func(self, key):
        pass
    
    def _command_mode_func(self, key):
        pass

    def _change_mode_to_normal(self):
        self._mode = 'normal'
        
    def _change_mode_to_insert(self):
        self._mode = 'insert'
        
    def _change_mode_to_command(self):
        self._mode = 'command'
        
    def _exit(self):
        self._active = True



if __name__ == "__main__":
    pass