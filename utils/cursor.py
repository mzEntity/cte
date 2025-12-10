from others.singleton import singleton


class CursorPosition:
    def __init__(self, pos_x, pos_y):
        self.pos_x = pos_x
        self.pos_y = pos_y

        
def _cursor_up(n: int) -> str:
    return f"\033[{n}A"

def _cursor_down(n: int) -> str:
    return f"\033[{n}B"

def _cursor_right(n: int) -> str:
    return f"\033[{n}C"

def _cursor_left(n: int) -> str:
    return f"\033[{n}D"

def _move_cursor_up(n: int):
    print(_cursor_up(n), end="")
    
def _move_cursor_down(n: int):
    print(_cursor_down(n), end="")
    
def _move_cursor_right(n: int):
    print(_cursor_right(n), end="")

def _move_cursor_left(n: int):
    print(_cursor_left(n), end="")

@singleton
class Cursor:
    def __init__(self):
        self._cursor_x = 0
        self._cursor_y = 0

    def position(self):
        return CursorPosition(self._cursor_x, self._cursor_y)
    
    def offset(self, cp: CursorPosition):
        return cp.pos_x - self._cursor_x, cp.pos_y - self._cursor_y
    
    def set(self, cp: CursorPosition):
        self._cursor_x = cp.pos_x
        self._cursor_y = cp.pos_y
        
    def goto(self, cp: CursorPosition):
        offset_x, offset_y = self.offset(cp)
        
        if offset_x > 0:
            _move_cursor_down(offset_x)       
        elif offset_x < 0:
            _move_cursor_up(-offset_x)
            
        if offset_y > 0:
            _move_cursor_right(offset_y)
        elif offset_y < 0:
            _move_cursor_left(-offset_y)
        
        self.set(cp)
        
        
def cprint(message: str):
    lines = message.split("\n")
    line_count = len(lines)
    enter_count = line_count - 1
    if line_count == 0:
        return
    if len(lines[line_count-1]) == 0:
        lines.pop(line_count-1)

    cur_enter_count = 0
    for line in lines:
        _cprint_within_line(line)
        if cur_enter_count < enter_count:
            _cnewline(1)
            cur_enter_count += 1



def _cprint_within_line(message: str):
    length = len(message)
    Cursor()._cursor_y += length
    print(message, end="")
    
    
    
def _cnewline(n: int):
    Cursor()._cursor_x += n
    Cursor()._cursor_y = 0
    print("\n" * n, end="")
    
    
    
def cindent(cp: CursorPosition):
    cur = Cursor().position()
    offset_y = cp.pos_y - cur.pos_y
    if offset_y > 0:
        _move_cursor_right(offset_y)
    elif offset_y < 0:
        _move_cursor_left(-offset_y)
    Cursor()._cursor_y += offset_y
    
def cnewline_indent(cp: CursorPosition):
    cur = Cursor().position()
    offset_y = cp.pos_y - cur.pos_y
    _move_cursor_down(1)
    if offset_y > 0:
        _move_cursor_right(offset_y)
    elif offset_y < 0:
        _move_cursor_left(-offset_y)
    Cursor()._cursor_x += 1
    Cursor()._cursor_y += offset_y