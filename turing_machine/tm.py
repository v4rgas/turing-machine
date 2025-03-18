from enum import Enum


class Direction(Enum):
    LEFT = -1
    RIGHT = 1


class Tape:
    tape: list[str]
    head: int

    EMPTY = " "

    def __init__(self):
        self.tape = [Tape.EMPTY]
        self.head = 0

    def get(self):
        return self.tape[self.head]

    def set(self, value):
        self.tape[self.head] = value

    def __next(self):
        self.head += 1
        if self.head == len(self.tape):
            self.tape.append(Tape.EMPTY)

    def __prev(self):
        self.head -= 1
        if self.head < 0:
            self.tape.insert(0, Tape.EMPTY)
            self.head = 0

    def move(self, direction: Direction):
        if direction == Direction.RIGHT:
            self.__next()
        elif direction == Direction.LEFT:
            self.__prev()
        else:
            raise ValueError("Invalid direction")


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
        self.tape = Tape()
        self.states = {initial_state.name: initial_state}
        self.current_state = initial_state

    def add_state(self, state: State):
        self.states[state.name] = state

    def next_step(self):
        current_symbol = self.tape.get()
        transition = self.current_state.get_transition(current_symbol)
        self.tape.set(transition.write)
        self.tape.move(transition.move)
        self.current_state = transition.to_state

    def print_tape(self):
        print(self.tape.tape)


if __name__ == "__main__":
    state_a = State("A")
    state_a.add_transition(state_a, " ", "a", Direction.RIGHT)

    tm = TuringMachine(state_a)

    tm.print_tape()
    for _ in range(10):
        tm.next_step()
        tm.print_tape()

    print(tm.current_state.name)
