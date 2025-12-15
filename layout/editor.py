from typing import List, Optional, TypeAlias

from utils.cursor import CursorPosition, Cursor, cprint, cnewline_indent

char: TypeAlias = str

class Editor:
    def __init__(self, height, width, position: CursorPosition, content: Optional[List[str]]=None):
        self._height = height
        self._width = width
        
        if content is None:
            content = [' ' * self._width for _ in range(self._height)]
            
        self._cm = ContentManager(content)
        self._dm = DisplayManager(self._width)
        self.update_display()
        
        self._base = position
        
        self._display_x_begin = 0
        self._display_x_end = self._display_x_begin + self._height
        
        self._display_cursor_x = 0
        self._display_cursor_y = 0
        
    
    def update_display(self):
        self._update_display_content()
        self._update_display_content_padded()
        
        
    def show_cursor(self):
        Cursor().goto(self._base)
        Cursor().move_offset(self._display_cursor_x - self._display_x_begin, self._display_cursor_y)
        Cursor().show()
        
        
    def _update_display_content(self):
        self._display_content_packed = self._dm.get_display_content_within_width(self._cm.get_content()) 
        self._display_content = [
            line 
            for split_result in self._display_content_packed
            for line in split_result
        ]
        
    def _update_display_content_padded(self):
        self._display_content_padded = []
        for line in self._display_content:
            new_line = line[:]
            if len(line) < self._width:
                new_line += ' ' * (self._width - len(line))
            self._display_content_padded.append(new_line)
        if self._height > len(self._display_content_padded):
            self._display_content_padded.extend([' ' * self._width] * (self._height - len(self._display_content_padded)))
            
        
    def show(self):
        Cursor().goto(self._base)
        display_list = self._display_content_padded[self._display_x_begin:self._display_x_end]
        
        for display_line in display_list:
            cprint(display_line)
            cnewline_indent(self._base)
            
            
    def display_cursor_left(self):
        if self._display_cursor_y > 0:
            self._display_cursor_y -= 1
        else:
            if self._display_cursor_x > 0:
                self._display_cursor_x -= 1
                self._display_cursor_y = len(self._display_content[self._display_cursor_x])
                if self._display_cursor_x < self._display_x_begin:
                    self._display_x_begin = self._display_cursor_x
                    self._display_x_end = self._display_x_begin + self._height
                    self.show()
            
            
    def display_cursor_right(self):
        if self._display_cursor_y < len(self._display_content[self._display_cursor_x]):
            self._display_cursor_y += 1
        else:
            if self._display_cursor_x < len(self._display_content) - 1:
                self._display_cursor_x += 1
                self._display_cursor_y = 0
                if self._display_cursor_x >= self._display_x_end:
                    self._display_x_end = self._display_cursor_x + 1
                    self._display_x_begin = self._display_x_end - self._height
                    self.show()
    
    
    def display_cursor_up(self):
        if self._display_cursor_x > 0:
            self._display_cursor_x -= 1
            self._display_cursor_y = min(self._display_cursor_y, len(self._display_content[self._display_cursor_x]))
            if self._display_cursor_x < self._display_x_begin:
                self._display_x_begin = self._display_cursor_x
                self._display_x_end = self._display_x_begin + self._height
                self.show()
            
            
    def display_cursor_down(self):
        if self._display_cursor_x < len(self._display_content) - 1:
            self._display_cursor_x += 1
            self._display_cursor_y = min(self._display_cursor_y, len(self._display_content[self._display_cursor_x]))
            if self._display_cursor_x >= self._display_x_end:
                self._display_x_end = self._display_cursor_x + 1
                self._display_x_begin = self._display_x_end - self._height
                self.show()
            
    # TODO: need refactor 以下顺序不能改变
    def insert_char(self, c: char):
        cx, cy = self._dm.display_index_to_content_index(self._display_cursor_x, self._display_cursor_y, self._display_content_packed)
        self._cm.insert_str(cx, cy, c)
        self.update_display()
        self.display_cursor_right()
        self.show()
        
        
    def delete_char(self):
        cx, cy = self._dm.display_index_to_content_index(self._display_cursor_x, self._display_cursor_y, self._display_content_packed)
        self.display_cursor_left()
        if cx != 0 and cy == 0:
            self._cm.combine_line(cx)
            self.update_display()
            self.show()
        else:
            self._cm.delete_str(cx, cy, 1)
            self.update_display()
            self.show()
            
        
    def insert_line(self):
        cx, cy = self._dm.display_index_to_content_index(self._display_cursor_x, self._display_cursor_y, self._display_content_packed)
        self._cm.insert_line(cx, cy)
        self.update_display()
        self.display_cursor_right()
        self.show()
        

class ContentManager:
    def __init__(self, content: Optional[List[str]] = None):
        if content is None:
            content = [""]
        self.init_content(content)
        
            
    def init_content(self, content: List[str]):
        self.content: List[List[char]] = [[c for c in line] for line in content]
        
        
    def insert_str(self, x: int, y: int, s: str):
        if len(self.content) <= x:
            raise ValueError(f"`x` out of bound: [0, {len(self.content)}). Got {x}")
        if len(self.content[x]) < y:
            raise ValueError(f"`y` out of bound: [0, {len(self.content[x])}]. Got {y}")
        
        self.content[x][y:y] = [c for c in s]
        
        
    def delete_str(self, x: int, y: int, count: int):
        if len(self.content) <= x:
            raise ValueError(f"`x` out of bound: [0, {len(self.content)}). Got {x}")
        if len(self.content[x]) < y:
            raise ValueError(f"`y` out of bound: [0, {len(self.content[x])}]. Got {y}")
        
        remove_count = min(y, count)
        del self.content[x][y-remove_count:y]
            
        
    def insert_line(self, x: int, y: int):
        if len(self.content) <= x:
            raise ValueError(f"`x` out of bound: [0, {len(self.content)}). Got {x}")
        if len(self.content[x]) < y:
            raise ValueError(f"`y` out of bound: [0, {len(self.content[x])}]. Got {y}")
        
        new_line = self.content[x][y:]
        self.content[x] = self.content[x][:y]
        self.content.insert(x+1, new_line)
        
        
    def combine_line(self, x: int):
        if x >= len(self.content) or x <= 0:
            raise ValueError(f"`x` out of bound: (0, {len(self.content)}). Got {x}")
        self.content[x-1].extend(self.content[x])
        del self.content[x]
        
    
    def get_content(self) -> List[str]:
        return [''.join(line) for line in self.content]
        


class DisplayManager:
    def __init__(self, width: int):
        self.width = width
        
        
    def display_index_to_content_index(self, x, y, display_content_packed: List[List[str]]):        
        target_height = x + 1
        sum_height = 0
        for i, display_line in enumerate(display_content_packed):
            cur_height = len(display_line)
            if sum_height + cur_height >= target_height:
                start_line = target_height - sum_height - 1
                content_x = i
                content_y = y
                for line_idx in range(start_line):
                    content_y += len(display_line[line_idx])
                return content_x, content_y
            sum_height += cur_height
            
        return -1, -1
    
    
    def get_display_content_within_width(self, content: List[str]) -> List[List[str]]:
        line_list_list: List[List[str]] = []
        for line in content:
            line_list_list.append(self.get_display_line_within_width(line))
        return line_list_list
    
    
    def get_display_line_within_width(self, line: str) -> List[str]:
        line_length = len(line)
        if line_length == 0:
            return [""]
        full_line_count = line_length // self.width
        
        line_list = [line[i*self.width:(i+1)*self.width] for i in range(full_line_count)]
        if line_length % self.width != 0:
            final_line = line[full_line_count*self.width:]
            line_list.append(final_line)
        return line_list
    

      
if __name__ == "__main__":
    file_path = "test/test_file1.txt"
    with open(file_path, "r") as f:
        content = [line.rstrip() for line in f.readlines()]
    # print(content)
    b = Editor(10, 100, Cursor().position(), content)
    
    b.show()
    print("===============")