import turtle
import math
import json
import inspect

MAX_ANGLE = 360
COMMAND_LIST = ['exit']
COMMAND_ARGS_LIST = dict()


def commands(func):
    if not COMMAND_LIST.__contains__(func.__name__):
        COMMAND_LIST.append(func.__name__)
    args = inspect.getargspec(func)[0]
    if args.__contains__('self'):
        args.remove('self')
    if inspect.getargspec(func)[1]:
        args.append(inspect.getargspec(func)[1])
    COMMAND_ARGS_LIST[func.__name__] = args
    return func


def convert_args(func):
    def convert(self, *args, **kwargs):
        arr = list(args)
        for i in range(len(arr)):
            arr[i] = float(arr[i]) if arr[i] != 'x'and arr[i] != 'y' else getattr(self.pointer, '{}cor'.format(arr[i]))()
        return func(self, *arr, **kwargs)
    convert.__name__ = func.__name__
    return convert


class Paint:
    pointer = turtle.Turtle()
    wn = turtle.Screen()
    file = []

    def do(self, func, args, from_file=False):
        if func.__name__ != 'save_to_file' and from_file is False:
            cmd = {func.__name__: args}
            self.file.append(cmd)
        func(*args)

    @commands
    def save_to_file(self, file_path):
        file = open(file_path, 'w')
        file.write(json.dumps(self.file))
        file.close()

    @commands
    def load_from_file(self, file_path):
        file = open(file_path, 'r')
        text = file.read()
        file.close()
        self.file = json.loads(text)

        for line in self.file:
            for key, val in line.items():
                self.do(getattr(self, key), val, True)

    @commands
    def goto(self, x, y):
        self.pointer.penup()
        self.pointer.goto(float(x), float(y))
        self.pointer.pendown()

    @commands
    def turn(self, side, angle):
        if side == 'l':
            self.pointer.lt(float(angle))
        elif side == 'r':
            self.pointer.rt(float(angle))

    @commands
    def get_current_state(self):
        print(" Current pos: %s,%s\n Current pen color: %s\n Current fill color: %s"
              % (self.pointer.xcor(), self.pointer.ycor(), self.pointer.pencolor(), self.pointer.fillcolor()))

    @commands
    def set_pensize(self, size):
        self.pointer.pensize(size)

    @commands
    def set_pencolor(self, *color):
        if len(color) == 1:
            self.pointer.pencolor(color[0])
        elif len(color) == 3:
            self.pointer.pencolor(float(color[0]), float(color[1]), float(color[2]))

    @commands
    def set_fillcolor(self, *color):
        if len(color) == 1:
            self.pointer.fillcolor(color[0])
        elif len(color) == 3:
            self.pointer.fillcolor(float(color[0]), float(color[1]), float(color[2]))

    @convert_args
    @commands
    def draw_line(self, x, y, angle, length):
        self.goto(x, y)
        self.pointer.seth(angle)
        self.pointer.fd(length)

    @convert_args
    @commands
    def draw_line_by_dots(self, x1, y1, x2, y2):
        self.goto(x1, y1)
        if x1 == x2:
            alpha_deg = 90
            if y2 < y1:
                alpha_deg -= 180
        else:
            alpha = math.atan((y1 - y2)/(x1-x2))
            alpha_deg = math.degrees(alpha)
            if x2 < x1:
                alpha_deg -= 180
        d = math.sqrt((x1-x2)**2 + (y1-y2)**2)
        self.draw_line('x', 'y', alpha_deg, d)

    @convert_args
    @commands
    def draw_regular_polygon(self, x, y, n, side_length):
        self.goto(x, y)
        n = int(n)
        self.pointer.begin_fill()
        for i in range(n):
            self.pointer.fd(float(side_length))
            self.pointer.rt(MAX_ANGLE/n)
        self.pointer.end_fill()

    @convert_args
    @commands
    def draw_polygon(self, *coords):
        self.pointer.begin_fill()
        self.goto(coords[0], coords[1])
        self.pointer.begin_fill()
        for i in range(2,len(coords),2):
            self.draw_line_by_dots('x', 'y', coords[i], coords[i+1])
        self.draw_line_by_dots('x', 'y', coords[0], coords[1])
        self.pointer.end_fill()

    @convert_args
    @commands
    def draw_circle(self, x, y, radius):
        self.goto(x, y)
        self.pointer.begin_fill()
        self.pointer.circle(radius)
        self.pointer.end_fill()

    @commands
    def print_commands(self):
        print("Command list: ")
        for command in sorted(COMMAND_LIST):
            print(command)


def init():
    paint = Paint()
    paint.print_commands()
    while True:
        command = input("Input command: ")
        if command in COMMAND_LIST:
            if command == 'exit':
                break
            elif command == 'print_commands' or command == 'get_current_state':
                getattr(paint, command)()
            else:
                args = input((COMMAND_ARGS_LIST[command]))
                paint.do(getattr(paint, command), args.split(" "), False)
        else:
            print("Unknown command. Type in 'print_commands' to see commands list")


if __name__ == "__main__":
    init()
