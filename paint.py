import turtle
import math
import inspect


MAX_ANGLE = 360
COMMAND_LIST = ('exit', 'print_commands', 'set_pensize', 'set_pencolor','set_fillcolor', 'draw_line', 'draw_regular_polygon',
                'turn', 'get_current_state', 'draw_polygon','draw_circle')
COMMAND_ARGS_LIST = dict(set_pensize='new_size',
                         set_pencolor='new_color',
                         set_fillcolor='new_color',
                         draw_line='start_x start_y angle length (start_x = x, start_y = y to continue from current location)',
                         draw_regular_polygon='start_x start_y sides_num side_len (start_x = x, start_y = y to continue from current location)',
                         turn='side(l/r) angle',
                         draw_polygon='start_x start_y (start_x = x, start_y = y to continue from current location)',
                         draw_line_by_dots='next_x next_y',
                         draw_circle='start_x start_y radius (start_x = x, start_y = y to continue from current location)')


class Paint:
    pointer = turtle.Turtle()
    wn = turtle.Screen()

    def do(self, func, args):
        func(*args)

    def goto(self, x, y):
        self.pointer.penup()
        self.pointer.goto(x, y)
        self.pointer.pendown()

    def turn(self, side, angle):
        if side == 'l':
            self.pointer.lt(float(angle))
        elif side == 'r':
            self.pointer.rt(float(angle))

    def convert(self, arr):
        for i in range(len(arr)):
            arr[i] = float(arr[i]) if arr[i] != 'x'and arr[i] != 'y' else getattr(self.pointer, '{}cor'.format(arr[i]))()
        return arr

    def get_current_state(self):
        print(" Current pos: %s,%s\n Current pen color: %s\n Current fill color: %s"
              % (self.pointer.xcor(), self.pointer.ycor(), self.pointer.pencolor(), self.pointer.fillcolor()))

    def set_pensize(self, size):
        self.pointer.pensize(size)

    def set_pencolor(self, *args):
        if len(args) == 1:
            self.pointer.pencolor(args[0])
        elif len(args) == 3:
            self.pointer.pencolor(float(args[0]), float(args[1]), float(args[2]))

    def set_fillcolor(self, *args):
        if len(args) == 1:
            self.pointer.fillcolor(args[0])
        elif len(args) == 3:
            self.pointer.fillcolor(float(args[0]), float(args[1]), float(args[2]))

    def draw_line(self, x, y, angle, length):
        x, y, angle, length = self.convert([x, y, angle, length])
        self.goto(x, y)
        self.pointer.seth(angle)
        self.pointer.fd(length)

    def draw_line_by_dots(self, x1, y1, x2, y2):
        x1, x2, y1, y2 = self.convert([x1, x2, y1, y2])
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

    def draw_regular_polygon(self, x, y, n, side_length):
        x, y, side_length = self.convert([x, y, side_length])
        self.goto(x, y)
        n = int(n)
        self.pointer.begin_fill()
        for i in range(n):
            self.pointer.fd(float(side_length))
            self.pointer.rt(MAX_ANGLE/n)
        self.pointer.end_fill()

    def draw_polygon(self, x, y):
        x, y = self.convert([x, y])
        self.goto(x, y)
        self.pointer.begin_fill()
        while True:
            args = input("[%s] or 'end' to finish: " % (COMMAND_ARGS_LIST['draw_line_by_dots']))
            if args == 'end':
                self.draw_line_by_dots('x', 'y', x, y)
                self.pointer.end_fill()
                break
            else:
                self.draw_line_by_dots('x', 'y', *args.split(" "))

    def draw_circle(self, x, y, radius):
        x, y, radius = self.convert([x, y, radius])
        self.goto(x, y)
        self.pointer.begin_fill()
        self.pointer.circle(radius)
        self.pointer.end_fill()


def print_commands():
    print("Command list: ")
    for command in sorted(COMMAND_LIST):
        print(command)


def init():
    paint = Paint()
    print_commands()
    while True:
        command = input("Input command: ")
        if command in COMMAND_LIST:
            if command == 'exit':
                break
            elif command == 'print_commands' or command == 'get_current_state':
                getattr(paint, command)()
            else:
                #print(inspect.getargspec(getattr(paint, command)).args[1:])
                args = input("[%s]: " % (COMMAND_ARGS_LIST[command]))
               # paint.do(getattr(paint, command), map(float, args.split(" ")))
                paint.do(getattr(paint, command), args.split(" "))
        else:
            print("Unknown command. Type in 'print_commands' to see commands list")


if __name__ == "__main__":
    init()