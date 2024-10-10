# Bandwidth

Source: <https://cacm.acm.org/practice/you-dont-know-jack-about-bandwidth/>

## Bandwidth is how much, Latency is how slow

If you think of the Internet as a series of pipes, then bandwidth conveys how much data you can send down the pipe. It is the diameter.

![](https://cacm.acm.org/wp-content/uploads/2024/10/Collier-Brown_Fig1.png?resize=1024,299)

If you buy a narrow, little pipe, you absolutely will have bad performance: You will not be able to get all your data through it in any reasonable amount of time. You will have starved yourself. If you buy a pipe big enough to contain your data, you are fine. The data will all flow straight down the pipe instead of having to sit around waiting for the previous bytes to squeeze their way through.

However, buying a pipe with a larger diameter than you need will not help. Your data will still flow into it without delay, but it will not go any faster. It will not exceed the speed of light. There isn’t a “warp speed” available for the Internet.

## Why is it slow?

Latency is how quickly (or slowly) data shows up. The least latency you can have equals the length of the pipe divided by the speed of light. Consider an outgoing Zoom call, comprising a bunch of short snippets of picture and sound, nicely compressed, with a period of time between each.

![](https://cacm.acm.org/wp-content/uploads/2024/10/Collier-Brown_Fig2.png?resize=768,128)

Each little slice of audio and video shoots through the pipe by itself, leaving room for other slices. For a Zoom call to fail, you need a lot of other traffic at the same time, enough to fill up the pipe. If you are working from home, this could mean someone in your family is streaming a movie or uploading photos from a cell phone.

That causes contention, where the photos (the big, long slice at the top) elbow their way into the pipe ahead of the smaller Zoom slices.

![](https://cacm.acm.org/wp-content/uploads/2024/10/Collier-Brown_Fig3.png?resize=1024,202)

If you have bad router software, the smaller Zoom slices will have to sit around in a queue (buffering) until the photos finish. Because the Zoom slices are delayed, other people on the Zoom call may see you freeze or stutter. Sometimes you will sound like you are shouting from the bottom of a well. On really bad days, you will just drop out.
