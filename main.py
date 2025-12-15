from typing import List
import shutil, os, sys

from utils.cursor import Cursor, CursorPosition, cprint, enter_venv, leave_venv
from utils.interactive import getch

from layout.editor import Editor
from layout.command import CommandLine

class MyVim:
    def __init__(self, height: int, width: int, content: List[str]):
        self._mode = 'normal'
        self._active = True
        self.editor = Editor(height-1, width, Cursor().position(), content)
        self.command_line = CommandLine(1, width, Cursor().position().offset(height-1, 0))
        
        self._init_operate_dict()
        
        
    def _init_operate_dict(self):
        self._operate_dict = {
            'normal': {
                'i': self._change_mode_to_insert,
                'a': self._change_mode_to_insert,
                'o': self._change_mode_to_insert,
                ':': self._change_mode_to_command,
            },
            'insert': {
                'ESC': self._change_mode_to_normal,
                'UP': lambda: (self.editor.display_cursor_up(), self.editor.show_cursor()),
                'DOWN': lambda: (self.editor.display_cursor_down(), self.editor.show_cursor()),
                'LEFT': lambda: (self.editor.display_cursor_left(), self.editor.show_cursor()),
                'RIGHT': lambda: (self.editor.display_cursor_right(), self.editor.show_cursor()),
                'BACKSPACE': lambda: (self.editor.delete_char(), self.editor.show_cursor()),
                'ENTER': lambda: (self.editor.insert_line(), self.editor.show_cursor())
            },
            'command': {
                'ESC': self._change_mode_to_normal,
                'UP': lambda: (self.command_line.history_pointer_up(), self.command_line.show_cursor()),
                'DOWN': lambda: (self.command_line.history_pointer_down(), self.command_line.show_cursor()),
                'LEFT': lambda: (self.command_line.edit_cursor_left(), self.command_line.show_cursor()),
                'RIGHT': lambda: (self.command_line.edit_cursor_right(), self.command_line.show_cursor()),
                'BACKSPACE': lambda: (self.command_line.delete_command_char(), self.command_line.show_cursor()),
                'ENTER': lambda: (self.execute_command(self.command_line.extract_command()), self.command_line.show_cursor())
            }
        }
        insertable_list = [c for c in "!@#$%^&*()`~-_=+[{]}\\|;:'\",<.>/?"]
        insertable_list.extend([chr(i) for i in range(ord('a'), ord('z')+1)])
        insertable_list.extend([chr(i) for i in range(ord('A'), ord('Z')+1)])
        insertable_list.extend([chr(i) for i in range(ord('0'), ord('9')+1)])
        for c in insertable_list:
            self._operate_dict['insert'][c] = lambda x=c: (self.editor.insert_char(x), self.editor.show_cursor())
            self._operate_dict['command'][c] = lambda x=c: (self.command_line.insert_command_char(x), self.command_line.show_cursor())
            
    def execute_command(self, command_str):
        if command_str == "!q":
            self._exit()

    def _change_mode_to_normal(self):
        self.command_line.clear_command()
        self._mode = 'normal'
        
    def _change_mode_to_insert(self):
        self.editor.show_cursor()
        self._mode = 'insert'
        
    def _change_mode_to_command(self):
        self.command_line.show_cursor()
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