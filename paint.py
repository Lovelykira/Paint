import turtle
import inspect


MAX_ANGLE = 360
COMMAND_LIST = ('exit', 'print_commands', 'set_pensize', 'set_pencolor','set_fillcolor', 'draw_line', 'draw_regular_polygon',
                'turn', 'get_current_state')
COMMAND_ARGS_LIST = dict(set_pensize='new_size',
                         set_pencolor='new_color',
                         set_fillcolor='new_color',
                         draw_line='start_x start_y angle length (start_x = x, start_y = y to continue from current location)',
                         draw_regular_polygon='start_x start_y sides_num side_len (start_x = x, start_y = y to continue from current location)',
                         turn='side(l/r) angle')


class Paint:
    pointer = turtle.Turtle()
    wn = turtle.Screen()

    def do(self, func, args):
        func(*args)

    def goto(self,x, y):
        if x != 'x' and y != 'y':
            self.pointer.penup()
            self.pointer.goto(float(x), float(y))
            self.pointer.pendown()

    def turn(self, side, angle):
        if side == 'l':
            self.pointer.lt(float(angle))
        elif side == 'r':
            self.pointer.rt(float(angle))

    def get_current_state(self):
        print(" Current pos: %s,%s\n Current pen color: %s\n Current fill color: %s"
              %(self.pointer.xcor(), self.pointer.ycor(), self.pointer.pencolor(), self.pointer.fillcolor()))
    def set_pensize(self, size):
        self.pointer.pensize(size)

    def set_pencolor(self, *args):
        if len(args) == 1:
            self.pointer.pencolor(args[0])
        elif len(args) == 3:
            self.pointer.pencolor(float(args[0]), float(args[1]), float(args[2]))


#    def set_pencolor(self, r, g, b):
 #       self.pointer.pencolor(float(r), float(g), float(b))

    def set_fillcolor(self, *args):
        if len(args) == 1:
            self.pointer.fillcolor(args[0])
        elif len(args) == 3:
            self.pointer.fillcolor(float(args[0]), float(args[1]), float(args[2]))

 #   def set_fillcolor(self, r, g, b):
#        self.pointer.fillcolor(float(r), float(g), float(b))

    def draw_line(self, x, y, angle, length):
        self.goto(x, y)
        self.pointer.seth(float(angle))
        self.pointer.fd(float(length))

    def draw_regular_polygon(self, x, y, n, side_length):
        self.goto(x, y)
        #self.pointer.seth(MAX_ANGLE)
        self.pointer.begin_fill()
        for i in range(int(n)):
            self.pointer.fd(float(side_length))
            self.pointer.rt(MAX_ANGLE/int(n))
        self.pointer.end_fill()

    def draw_polygon(self):
        return
        #TO DO




def print_commands():
    print("Command list: ")
    for command in sorted(COMMAND_LIST):
        print(command)


#def print_


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