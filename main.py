from utils.cursor import Cursor, CursorPosition, cprint
from utils.interactive import getch

class MyVim:
    def __init__(self):
        self._mode = 'normal'
        self._active = True
        self._cursor = Cursor()
        self._cursor_pos = self._cursor.position()
        
        self._operate_dict = {
            'normal': {
                'i': self._change_mode_to_insert,
                'a': self._change_mode_to_insert,
                'o': self._change_mode_to_insert,
                ':': self._change_mode_to_command,
                'other': self._normal_mode_func
            },
            'insert': {
                'ESC': self._change_mode_to_normal,
                'other': self._insert_mode_func
            },
            'command': {
                'ESC': self._change_mode_to_normal,
                'q': self._exit,
                'other': self._command_mode_func
            }
        }
        
    def _normal_mode_func(self, key):
        pass
    
    def _insert_mode_func(self, key):
        if key == 'UP':
            self._cursor.up()
        elif key == 'LEFT':
            self._cursor.left()
        elif key == 'DOWN':
            self._cursor.down()
        elif key == 'RIGHT':
            self._cursor.right()
        else:
            cprint(key)
    
    def _command_mode_func(self, key):
        pass

    def _change_mode_to_normal(self):
        if self._mode == 'insert':
            self._cursor_pos = self._cursor.position()
        self._mode = 'normal'
        
    def _change_mode_to_insert(self):
        self._cursor.goto(self._cursor_pos)
        self._mode = 'insert'
        
    def _change_mode_to_command(self):
        self._mode = 'command'
        
    def _exit(self):
        self._active = False

    def work(self):
        count = 0
        while self._active and count < 10:
            operation_available = self._operate_dict[self._mode]
            ch, source = getch()
            if ch in operation_available:
                operation_available[ch]()
            else:
                operation_available['other'](ch)
            # print(ch, self._mode)
            count += 1
            

if __name__ == "__main__":
    vim = MyVim()
    vim.work()