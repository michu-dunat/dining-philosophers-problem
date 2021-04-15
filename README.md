# Dining philosophers problem
My solution for [dining philosophers problem](https://en.wikipedia.org/wiki/Dining_philosophers_problem) written in Python. 
Curses library is used for displaying philosophers and forks.

## Running the script

The program is launched from the console. One argument is required - the number of dining philosophers. 

```
python .\main.py 5
```

## Note

The program can run for a large number of threads, but when running it, you should take into account the size of the console window - on the screen
with a resolution of 1920x1080, I could observe a maximum of 16 philosophers and forks.
