from enum import Enum


class Direction(Enum):
    LEFT = -1
    RIGHT = 1


class Tape:
    __tape: list[str]
    __head: int

    EMPTY = " "

    def __init__(self):
        self.__tape = [Tape.EMPTY]
        self.__head = 0

    def get(self):
        return self.__tape[self.__head]

    def set(self, value):
        self.__tape[self.__head] = value

    def __next(self):
        self.__head += 1
        if self.__head == len(self.__tape):
            self.__tape.append(Tape.EMPTY)

    def __prev(self):
        self.__head -= 1
        if self.__head < 0:
            self.__tape.insert(0, Tape.EMPTY)
            self.__head = 0


    def set_initial(self, values: list[str]):
        self.__tape = values

    def move(self, direction: Direction):
        if direction == Direction.RIGHT:
            self.__next()
        elif direction == Direction.LEFT:
            self.__prev()
        else:
            raise ValueError("Invalid direction")
        

    def print(self):    
        str_tape = str(self.__tape) + '\n'
        spacing = len(str(self.__tape[0:self.__head + 1])) - 3
        str_tape += " " * spacing + "^"

        print(str_tape)


class State:
    name: str
    __transitions: dict[str, "Transition"]

    def __init__(self, name):
        self.name = name
        self.__transitions = {}

    def add_transition(self, to: "State", read: str, write: str, move: Direction):
        self.__transitions[read] = Transition(self, to, read, write, move)

    def get_transition(self, read) -> "Transition":
        return self.__transitions.get(read)

    def print_transitions(self):
        print(f"Transitions of {self.name}:")
        for read_symbol, transition in self.__transitions.items():
            print(f"  On '{read_symbol}': Write '{transition.write}', Move {transition.move}, Go to '{transition.to_state.name}'")


class Transition:
    from_state: State
    to_state: State

    read: str
    write: str
    move: Direction

    def __init__(self, from_state: State, to_state: State, read, write, move):
        self.from_state = from_state
        self.to_state = to_state

        self.read = read
        self.write = write
        self.move = move


class TuringMachine:
    def __init__(self, initial_state: State):
        self.__tape = Tape()
        self.__states = {initial_state.name: initial_state}
        self.__current_state = initial_state

    def add_state(self, state: State):
        self.__states[state.name] = state

    def load_input(self, values: list[str]):
        self.__tape.set_initial(values)

    def next_step(self):
        current_symbol = self.__tape.get()
        transition = self.__current_state.get_transition(current_symbol)
        self.__tape.set(transition.write)
        self.__tape.move(transition.move)
        self.__current_state = transition.to_state

    def print_tape(self):
        self.__tape.print()




def example_2():
    state_a = State("A")
    state_b = State("B")

    state_a.add_transition(state_a, " ", "a", Direction.RIGHT)
    state_a.add_transition(state_b, "b", "b", Direction.LEFT)

    state_a.print_transitions()

    state_b.add_transition(state_a, " ", "a", Direction.RIGHT)
    state_b.add_transition(state_b, "a", "a", Direction.LEFT)

    tm = TuringMachine(state_a)

    tm.load_input([" ", " ", " ", " ", "b"])


    print("Starting tape:")
    tm.print_tape()
    for _ in range(10):
        tm.next_step()
        tm.print_tape()


if __name__ == "__main__":
    example_2()
