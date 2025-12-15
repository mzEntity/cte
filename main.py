from typing import List
import shutil, os, sys

from utils.cursor import Cursor, CursorPosition, cprint, enter_venv, leave_venv
from utils.interactive import getch

from layout.editor import Editor

class MyVim:
    def __init__(self, height: int, width: int, content: List[str]):
        self._mode = 'normal'
        self._active = True
        self.editor = Editor(height, width, Cursor().position(), content)
        
        self._init_operate_dict()
        
        
    def _init_operate_dict(self):
        self._operate_dict = {
            'normal': {
                'i': self._change_mode_to_insert,
                'a': self._change_mode_to_insert,
                'o': self._change_mode_to_insert,
                ':': self._change_mode_to_command
            },
            'insert': {
                'ESC': self._change_mode_to_normal,
                'UP': lambda: (self.editor.display_cursor_up(), self.editor.show_cursor()),
                'LEFT': lambda: (self.editor.display_cursor_left(), self.editor.show_cursor()),
                'DOWN': lambda: (self.editor.display_cursor_down(), self.editor.show_cursor()),
                'RIGHT': lambda: (self.editor.display_cursor_right(), self.editor.show_cursor()),
                'BACKSPACE': lambda: (self.editor.delete_char(), self.editor.show_cursor()),
                'ENTER': lambda: (self.editor.insert_line(), self.editor.show_cursor())
            },
            'command': {
                'ESC': self._change_mode_to_normal,
                'q': self._exit
            }
        }
        insertable_list = []
        insertable_list.extend([chr(i) for i in range(ord('a'), ord('z')+1)])
        insertable_list.extend([chr(i) for i in range(ord('A'), ord('Z')+1)])
        insertable_list.extend([chr(i) for i in range(ord('0'), ord('9')+1)])
        for c in insertable_list:
            self._operate_dict['insert'][c] = lambda: (self.editor.insert_char(c), self.editor.show_cursor())

    def _change_mode_to_normal(self):
        self._mode = 'normal'
        
    def _change_mode_to_insert(self):
        self.editor.show_cursor()
        self._mode = 'insert'
        
    def _change_mode_to_command(self):
        self._mode = 'command'
        
    def _exit(self):
        self._active = False

    def work(self):
        self.editor.show()
        while self._active:
            operation_available = self._operate_dict[self._mode]
            ch, source = getch()
            if ch in operation_available:
                operation_available[ch]()



if __name__ == "__main__":
    enter_venv()
    
    size = shutil.get_terminal_size()
    columns = size.columns
    lines = size.lines
    
    file_path = "test/test_file2.txt"
    with open(file_path, "r") as f:
        content = [line.rstrip() for line in f.readlines()]
    vim = MyVim(lines, columns, content)
    vim.work()
    
    leave_venv()