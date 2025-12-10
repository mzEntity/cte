# windows platform
import msvcrt    

def _getch():
    got_list = []
    got_list.append(msvcrt.getch())
    msvcrt.ungetch(b'0')
    c = msvcrt.getch()
    while c != b'0':
        got_list.append(c)
        c = msvcrt.getch()
    return got_list

def getch():
    byte_list = _getch()
    bytes_input = b''.join(byte_list)
    control_dict = {
        b'\xe0H': "UP",
        b'\xe0P': "DOWN",
        b'\xe0K': "LEFT",
        b'\xe0M': "RIGHT",
        b'\x1b': "ESC"
    }
    
    if bytes_input in control_dict:
        return control_dict[bytes_input]
    
    for encoding in ['utf-8']:
        try:
            s = bytes_input.decode(encoding)
            return s
        except UnicodeDecodeError:
            continue
    return "UNKNOWN"


if __name__ == "__main__":
    print('Press 10 keys: ')
    for i in range(10):
        result = getch()
        print(result)