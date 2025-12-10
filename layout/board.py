from typing import List

from utils.cursor import CursorPosition, Cursor, cprint, cnewline_indent


class Board:
    def __init__(self, height, width, position):
        self.height = height
        self.width = width
        
        self.contents = []
        for _ in range(self.height):
            self.contents.append(" " * self.width)
        self.start = CursorPosition(position[0], position[1])
        
        self.children = dict()
        
    def show(self):
        Cursor().goto(self.start)
        for content in self.contents:
            cprint(content)
            cnewline_indent(self.start)
    
        for _, child in self.children.items():
            child.show()
            
        
    def addChild(self, name, board):
        self.children[name] = board
        
        
class Line:
    def __init__(self, content, width):
        self.width = width
        self.content = [c for c in content]
        self.updated = False
        self.update_display(self.width)
        
    def height(self):
        if not self.updated:
            self.update_display(self.width)
        return len(self.display_content)
    
    def get_line_idx(self, display_x, display_y):
        return display_x * self.width + display_y
        
    def insert_char(self, idx, c):
        if len(self.content) < idx:
            self.content.extend([" "] * (idx - len(self.content)))
        self.content.insert(idx, c)
        self.updated = False
    
    def delete_char(self, idx):
        if len(self.content) <= idx:
            return
        self.content.pop(idx)
        self.updated = False
        
    def split_line(self, idx):
        if len(self.content) <= idx:
            return Line("", self.width)
        split_content = self.content[idx:]
        self.content = self.content[:idx]
        self.updated = False
        return Line(split_content, self.width)
    
    def combine_line(self, new_line):
        self.content.extend(new_line.content)
        self.updated = False
        
    def update_display(self, width):
        content_length = len(self.content)
        lines = content_length // width
        display_content = [self.content[i*width:(i+1)*width] for i in range(lines)]
        if content_length % width != 0:
            display_content.append(self.content[lines*width:])
        if len(display_content) == 0:
            display_content.append([" "])
        self.display_content = display_content
        self.updated = True
        
    def print_display(self):
        if not self.updated:
            self.update_display(self.width)
        for line in self.display_content:
            print(''.join(line))
        

class ContentDisplayManager:
    def __init__(self, height, width):
        self.height = height
        self.width = width
        
        self.raw_content: List[Line] = []
    
    def init_raw_content(self, raw_content):
        self.raw_content = [Line(line[:], self.width) for line in raw_content]
        
    def display_index_to_content_index(self, x, y):
        target_height = x + 1
        cur_height = 0
        for idx, line in enumerate(self.raw_content):
            if cur_height + line.height() >= target_height:
                remain = target_height - cur_height - 1
                return idx, line.get_line_idx(remain, y)
            else:
                cur_height += line.height()
        return len(self.raw_content) - 1 + (target_height - cur_height), y
    

    def insert_char(self, x, y, c):
        cx, cy = self.display_index_to_content_index(x, y)
        while len(self.raw_content) <= cx:
            self.raw_content.append(Line("", self.width))
        
        target_line = self.raw_content[cx]
        target_line.insert_char(cy, c)
        
        
    def delete_char(self, x, y):
        cx, cy = self.display_index_to_content_index(x, y)
        if len(self.raw_content) <= cx:
            return
        target_line = self.raw_content[cx]
        target_line.delete_char(cy)
        
    def display(self):
        for line in self.raw_content:
            line.print_display()

        
    def insert_line(self, x, y):
        cx, cy = self.display_index_to_content_index(x, y)
        while len(self.raw_content) < cx:
            self.raw_content.append(Line("", self.width))
        if cy == 0:
            self.raw_content.insert(x, Line("", self.width))
        else:
            new_line = self.raw_content[cx].split_line(cy)
            self.raw_content.insert(cx+1, new_line)

        
    def delete_line(self, x):
        cx, cy = self.display_index_to_content_index(x, 0)
        if cx == 0 or cy != 0 or len(self.raw_content) <= cx:
            return
        self.raw_content[cx-1].combine_line(self.raw_content[cx])
        self.raw_content.pop(cx)
        
if __name__ == "__main__":
    file_path = "test/test_file1.txt"
    with open(file_path, "r") as f:
        content = [line.strip() for line in f.readlines()]
    
    cdm = ContentDisplayManager(100, 100)
    cdm.init_raw_content(content)
    cdm.display()
    
    print("========================================")
    
    cdm.insert_char(0, 9, 'a')
    cdm.insert_char(1, 0, 'c')
    cdm.insert_char(1, 0, 'b')
    
    cdm.delete_char(0, 10)
    cdm.insert_line(1, 1)
    # cdm.insert_char(0, 9, 'a')
    cdm.delete_line(3)
    cdm.display()
    