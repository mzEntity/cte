from typing import List, TypeAlias

from utils.cursor import CursorPosition, Cursor, cprint

char: TypeAlias = str

class CommandLine:
    def __init__(self, height, width, position: CursorPosition):
        self._height = height
        self._width = width
        
        self._base = position
        
        self._edit_y = 0
        self._command: List[char] = []
        
    def edit_cursor_left(self):
        if self._edit_y > 0:
            self._edit_y -= 1
            
    def edit_cursor_right(self):
        if self._edit_y < len(self._command):
            self._edit_y += 1
        
    def insert_command_char(self, c: char):
        x = self._edit_y
        self._command.insert(x, c)
        self.show()
        self.edit_cursor_right()
        
    def delete_command_char(self):
        if self._edit_y > 0:
            del self._command[self._edit_y-1]
        self.show()
        self.edit_cursor_left()
        
    def clear_command(self):
        self._command.clear()
        self._edit_y = 0
        self.show()
        
    def extract_command(self):
        # print(f"Execute command {''.join(self._command)}")
        command_str = ''.join(self._command)
        self.clear_command()
        return command_str
        
    def show_cursor(self):
        Cursor().goto(self._base)
        Cursor().move_offset(0, self._edit_y)
        Cursor().show()
        
    def show(self):
        Cursor().goto(self._base)
        display_str = ''.join(self._command)
        if len(display_str) < self._width:
            display_str += " " * (self._width - len(display_str))
        cprint(display_str)