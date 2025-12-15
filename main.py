from typing import List
import shutil, os, sys

from utils.cursor import Cursor, CursorPosition, cprint, enter_venv, leave_venv
from utils.interactive import getch

from layout.board import Editor

class MyVim:
    def __init__(self, height: int, width: int, content: List[str]):
        self._mode = 'normal'
        self._active = True
        self.editor = Editor(height, width, Cursor().position(), content)
        
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
            self.editor.display_cursor_up()
            self.editor.show_cursor()
        elif key == 'LEFT':
            self.editor.display_cursor_left()
            self.editor.show_cursor()
        elif key == 'DOWN':
            self.editor.display_cursor_down()
            self.editor.show_cursor()
        elif key == 'RIGHT':
            self.editor.display_cursor_right()
            self.editor.show_cursor()
        else:
            cprint(key)
    
    def _command_mode_func(self, key):
        pass

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
            if ch == 'q':
                break
            if ch in operation_available:
                operation_available[ch]()
            else:
                operation_available['other'](ch)
            # print(ch, self._mode)



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