# Optimize Your code

Source:

- <https://github.com/dgryski/go-perfbook/blob/master/performance.md>
- <https://wiki.c2.com/?PrematureOptimization>

This note is about coding optimization, something like caching, designing performant distributed systems is beyond the scope of this work. Optimizing distributed systems encompasses an entirely different set of research and design trade-offs.

You may find the content is quite familiar, cause I don't write it all by myself. Most parts of this note are gotten from other sources, please refer _Source_ at the beginning.

## 1. When and Where to Optimize

First of all, let's ask yourself a question: Should you even be doing this at all?

Every optimization has a cost. Generally, this cost is expressed in terms of code complexity or cognitive load -- optimized code is rarely simpler than the unoptimized version. But there's another side - economics of optimization. [Time is money](<https://en.wikipedia.org/wiki/Time_is_money_(aphorism)>), same goes for programming. With the same amount of time, you could fix bugs, add feature, instead of optimization. Optimizing things is fun, but it's not always the right task to do.

_Choose the most important thing to work on_. You find that your code doesn't use CPU effectively, you spend a ton of time for CPU optimization then. But at the end, the application's user-experience (UX) is still suck, your optimization isn't worth it. Doing simple thing like add a progress bar, do computation in the background after rendering page is more valuable.

_In another thing, just because something is easy to optimize doesn't it's worth optimizing_. Ignoring low-hanging fruit is a valid development strategy.

_Optimizing your code is about optimizing your time_. In DonaldKnuth's paper ["Strutctured Progamming with Go To Statements"](https://wiki.c2.com/?StructuredProgrammingWithGoToStatements), he wrote:

```
Programmers waste enormous amounts of time thinking about, or worrying about, the speed of noncritical parts of their programs, and these attempts at efficiency actually have a strong negative impact when debugging and maintenance are considered. We should forget about small efficiencies, say about 97% of the time: premature optimization is the root of all evil. Yet we should not pass up our opportunities in that critical 3%.
```

Let's go back to our question:

```
Q: Should you optimize?
A: Yes, but only if the problem is important, the program is genuinely too slow, and there is some expectation that it can be made faster while maintaining correctness, robustness, and clarity.(The Practice of Programming, Kernighan and Pike)
```

Hmmm, so...

```shell
if $your_answer is in ["yes, it's worth it", "f*ck that, i want to do this sh*t"] find
then
    move_on
fi
```

## 2. How to Optimize

// WIP: Haiz, I'm lazy... come back later
