import threading
import time
import random
import curses
import sys


class Fork:

    def __init__(self):
        self.owner = False
        self.lock = threading.Lock()
        self.condition = threading.Condition()
        self.state = 'Clean'

    def pick_up(self, philosopher):
        if self.owner == philosopher:
            with self.lock:
                self.state = 'Clean'
                return

        if self.state == 'Dirty':
            with self.lock:
                self.state = 'Clean'
                self.owner = philosopher
            return

        if self.state == 'Clean':
            with self.condition:
                self.condition.wait()

                with self.lock:
                    self.owner = philosopher
                    self.state = 'Clean'

    def put_down(self):
        with self.lock:
            self.state = 'Dirty'

        with self.condition:
            self.condition.notify_all()


class Philosopher(threading.Thread):

    def __init__(self, id: int, left_fork: Fork, right_fork: Fork, stdscr):
        threading.Thread.__init__(self)
        self.id = id
        self.leftFork = left_fork
        self.rightFork = right_fork
        self.finished_eating_counter = 0
        self.stdscr = stdscr

    def run(self):
        while True:
            self.eat()
            self.finished_eating_counter += 1
            self.think()

    def __repr__(self):
        return f'Philosopher {self.id}'

    def eat(self):
        self.stdscr.addstr(self.id * 3, 0, f'{self} is trying to eat')
        self.stdscr.refresh()
        self.leftFork.pick_up(self)
        self.rightFork.pick_up(self)
        self.stdscr.addstr(self.id * 3, 0, f'{self} is eating       ')
        self.stdscr.refresh()
        time.sleep(random.uniform(2.5, 3.5))

    def think(self):
        self.stdscr.addstr(self.id * 3, 0, f'{self} is thinking     ')
        self.stdscr.refresh()
        self.leftFork.put_down()
        self.rightFork.put_down()
        self.stdscr.addstr((self.id * 3) + 1, 0, f'{self} ate {self.finished_eating_counter} times')
        self.stdscr.refresh()
        time.sleep(random.uniform(2.5, 3.5))


if __name__ == '__main__':
    stdscr = curses.initscr()

    number_of_philosophers = int(sys.argv[1])
    forks = [Fork() for i in range(number_of_philosophers)]
    philosophers = []

    for i in range(number_of_philosophers):
        left_fork = forks[i]
        right_fork = forks[(i + 1) % number_of_philosophers]
        philosopher = Philosopher(i, left_fork, right_fork, stdscr)

        if not left_fork.owner:
            left_fork.owner = philosopher
        if not right_fork.owner:
            right_fork.owner = philosopher

        philosophers.append(philosopher)

    for i in philosophers:
        i.start()
