
DEBUG = False

def debug_print(*args):
    if DEBUG:
        print(*args)


class Directory():
    def __init__(self, name):
        self.name = name
        self.parent= None
        self.directories = {}
        self.files = []

    def add_directory(self, directory_name):
        if directory_name in self.directories:
            return
        #print("Adding Dir: {} + {}".format(self.name, directory_name))
        new_directory = Directory(directory_name)
        new_directory.parent = self
        self.directories[directory_name] = new_directory 
        
    def add_file(self, file_name, file_size):
        for file_info in self.files:
            if file_name == file_info[0]:
                return
        #print("Adding File: {} + {}".format(self.name, file_name))
        self.files.append([file_name, file_size])

    def size(self):
        result = 0

        for file_info in self.files:
            result += file_info[1]

        for directory in self.directories.values():
            result += directory.size()

        return result

    def path(self):
        result = ""

        cur_dir = self
        stack = []
        while cur_dir.parent:
            stack.append(cur_dir.parent)
            cur_dir = cur_dir.parent

        while stack:
            d = stack.pop(-1)
            result += d.name + '/'
        result += self.name

        return result

    def __repr__(self):
        return self.repr_recurse()

    def repr_recurse(self, indent = 0):
        result = "  " * indent
        
        result += self.name + '\n'
        for directory in self.directories.values():
            result += directory.repr_recurse(indent + 1)

        for file_info in self.files:
            line  = "  " * (indent + 1)
            line += "{}\t{}".format(file_info[0], file_info[1])
            result += line + '\n'

        return result
        
def main():
    root_dir = parse_input()
    #print(root_dir)

    answer_01 = part_01(root_dir)
    answer_02 = part_02(root_dir)

    print("Answer 01: {}".format(answer_01))
    print("Answer 02: {}".format(answer_02))


def parse_input():
    data = None
    with open("puzzle_07_input.txt", 'r') as f:
        data = f.readlines()
    f.close()

    root_dir = Directory('/')
    cur_dir = root_dir

    for line in data:
        if not line:
            continue

        line = line.strip()
        #print(line)

        if line[0] == '$':
           info = line.split(' ')
           cmd = info[1]

           if cmd == 'ls':
               continue

           if cmd == 'cd':
               arg = info[2]
               if arg == '..':
                   #print("{} <-- {}".format(cur_dir.name, cur_dir.parent.name))
                   cur_dir = cur_dir.parent
               else:
                   if arg == '/':
                       cur_dir = root_dir
                   else:
                       #print("{} --> {}".format(cur_dir.name, arg))
                       cur_dir = cur_dir.directories[arg]
        else:
            info = line.split(' ')
            if info[0] == 'dir':
                dir_name = info[1]
                cur_dir.add_directory(dir_name)
            else:
                file_size = int(info[0])
                file_name = info[1]
                # print("{}: {}".format(file_name, file_size))
                cur_dir.add_file(file_name, file_size)

    return root_dir


def part_01(root_dir):
    result = 0

    dp = {}
    stack = [root_dir]

    while stack:
        cur_dir = stack.pop()
        dir_path = cur_dir.path()

        if dir_path not in dp:
            dp[dir_path] = cur_dir.size()

        for sub_dir in cur_dir.directories.values():
            stack.append(sub_dir)

    debug_print("************* PART 1 **************")
    for k, v in dp.items():
        if v <= 100000:
            result += v
            debug_print(k)
            debug_print(v)
    return result


def part_02(root_dir):
    result = 0

    total_size = 70000000
    used_size = root_dir.size()

    unused_size = total_size - used_size
    needed_size = 30000000

    target_size = needed_size - unused_size
    if target_size <= 0:
        debug_print("All good!")
        return 0

    dp = {}
    stack = [root_dir]

    while stack:
        cur_dir = stack.pop()
        dir_path = cur_dir.path()

        if dir_path not in dp:
            dp[dir_path] = cur_dir.size()

        for sub_dir in cur_dir.directories.values():
            stack.append(sub_dir)

    debug_print("************* PART 2 **************")
    result = used_size
    for k, v in dp.items():
        if v < target_size:
            continue
        result = min(result, v)


    debug_print("Available After Delete: {}".format(total_size - (used_size - result)))
    return result



if __name__ == "__main__":
    main()
