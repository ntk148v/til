# Concurrency is not Parallelism

![](https://go101.org/article/res/concurrent-vs-parallel.png)

These two terms always make me confuse a lot and I know that I'm not the only one.
Let's make it clear.

Rob Pike (Unix, Golang, UTF-8 and Plan 9 Software Engineer) explains this well in this [video](https://www.youtube.com/watch?v=cN_DpYBzKso). You might want to take a look at this, a lot of articles point to it as refer and I'm not an exception.

## Concurrency

- Programming as the composition of independently executing processes.

- Handle multiple tasks and is used for the multi-tasking of eperating systems.

## Parallelism

- Programming as the simultaneous execution of (possibly related) computations.

- Handle an individual task by splitting it into multiple subtasks.

## Concurrency vs Parallelism

- Concurrency is about dealing with lots of things at once

- Parallelism is about doing lots of things at once

- Concurrency is about structure, parallelism is about execution.

## But

This is too abstract. Let's get concrete! You're assigned the task to build 2 parallel walls starting from a pile of bricks at one end. What are you going to finish the task?

- Option 1: To build 1 wall, go back to the pile, and build the second - this is typical `sequential` processing.

- Option 2: To alternately lay a brick for each wall - the two walls are being built within the same time - `concurrently`.

- Option 3: To ask another worker and build the walls at the same time - `parallel` processing.

![comparsion](http://www.dietergalea.com/images/parallel_sequential_concurrent.jpg)

[Source image](http://www.dietergalea.com/parallelism-concurrency/)
