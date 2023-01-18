# How to invest in technical infrastructure

Source: <https://lethain.com/how-to-invest-technical-infrastructure/>

## What is technical infrastructure?

Technical infrastructure is the software and systems we use to create, evolve and operate our businesses. The more precise definition that this talk will use is "Tool used by many teams for critical workfloads."

## Why does infrastructure matter?

This sort of infrastructure is a rare opportunity to do truly leveraged work.

The consequences of doing infrastructure poorly are equally profound.

Scaled company is an excellent infrastructure team doing remarkable things.

## Foundations

![](https://lethain.com/static/blog/2019/ti-forced-disc.png)

The 1st distinction that's important to make is between _forced_ and _discretionary_ work. _Forced_ work is stuff that simply must happen, and might be driven by a critical launch, a company-defining user, a security vulnerability,... _Discretionary_ work is much more open ended, and is the sort of work where you're able to pick from the entire universe of possibilities: new products, rewrites,...

![](https://lethain.com/static/blog/2019/ti-short-long.png)

The 2nd distinction is between _short-term_ and _long-term_ work. _Short-term_ might be needing to patch all your servers this wek for a new security vulnerability. _Long-term_ might be building the automation and tooling to reduce the p99 age of your compute instances, which will make it quicker and safer to deploy patches in the future.

Combine these ideas:

![](https://lethain.com/static/blog/2019/ti-full-grid.png)

1. _Forced, short-term_: emergencies of all shapes and sizes.
2. _Forced, long-term_: preparation for the mandatory future work that requires major investment. Acknowledging this sort of work can be subversive in some cultures, but it's real, and creating visibility into its existence is a core aspect of properly investing in infrastructure.
3. _Discretionary, short-term_: these tend to be small, user-feedback-driven tweaks avoid usability, targeted reliability remediations.
4. _Discretionary, long-term_: often generational improvements to existing systems, like moving from batch to streaming computation paradigm, moving from a monolith to an SoA, and so on.

## The evolution of Stripe's approach to infrastructure

### Firefighting

![](https://lethain.com/static/blog/2019/ti-grid-fire.png)

An important aspect of infrastructure engineeing: the percentage of work that simply must be done.

Keypoints:

- Prioritize as much work into the future as possible, shedding "forced" work.
- Sometimes you can get creative, finding more leveraged approach. The goal here is to find work that addresses "forced" work that also reduces future "forced" work.
- Do less.
- If you can't reduce forced work and you're falling behind, you have to hire your way out.

### Investment

![](https://lethain.com/static/blog/2019/ti-grid-research.png)

Most infrastructure teams really struggle when they make the shift from the very clear focus created by emergencies to the oppressively board opportunity that comes from escaing the tyranny of forced, short-term work.

Keypoints:

- You're going to have be very intentional about determining what to work on and how to approach it.
- The fundamentals of product management: discover problems, prioritize across them, validate your planned approach.

### Principles

![](https://lethain.com/static/blog/2019/ti-grid-good.png)

Keypoints:

- Identify broad categories that capture the different properties you want to maintain in your infrastructure.
- Security, reliability, usability, efficiency and latency.
- For each of these properties, you need to identify a baseline of what acceptable performance is.

## Conclusion

There's no single approach to investing into infrastructure that's going to work for you all of the time. Identifying an effective approach depends on recognizing your current constraints, and then accounting for them properly.

Good pattern to reuse:

- If your team is doing forced, short-term work, then dig out by investing into your operational excellence.
- If your team is just starting to experience the thrills of discretionary, long-term work, then invest into your product management skills.
- If you have discretionary budget, but still find yourself running from one problem, then identify the principles to balance your approach, and set baselines for each principle.
