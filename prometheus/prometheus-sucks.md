# Prometheus sucks?

*Huh, really?*

![](https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRk26SiCrYdFmDMs2o4YD4MuwEnP8rHSR1hAyymXTKVUg2UJuUqaQ)

Ok ok, calm down, the title is completely a clickbait. Prometheus is still a very great monitoring and alerting solution, no doubt but beside the wonderful features, there are some existing disadvantages.

This post is my personal opinion, so if you are disagree, [leave some comments](https://ntk148v.github.io/blog/posts/lets-comment/).

- [Prometheus sucks?](#Prometheus-sucks)
  - [1. Doesn't support TLS or authentication](#1-Doesnt-support-TLS-or-authentication)
  - [2. Plain Configuration](#2-Plain-Configuration)
  - [3. Doesn't have RBAC (Role-based access control)](#3-Doesnt-have-RBAC-Role-based-access-control)
  - [4. High-availability](#4-High-availability)
  - [5. The lack of documentation](#5-The-lack-of-documentation)
  - [Conclusion](#Conclusion)

## 1. Doesn't support TLS or authentication

Ok, look at [FAQ](https://prometheus.io/docs/introduction/faq/#why-dont-the-prometheus-server-components-support-tls-or-authentication-can-i-add-those):

```
While TLS and authentication are frequently requested features, we have intentionally not implemented them in any of Prometheus's server-side components.
```

IMO, there should be a built-in feature rather than using 3rd-party components like a reverse proxy. Nicely, the Prometheus team has changed their stance (*Thanks!!!* :bow:) on this during its development summit on August 11, 2018, and support for TLS and authentication in serving endpoints is now on [the project's roadmap](https://prometheus.io/docs/introduction/faq/#why-dont-the-prometheus-server-components-support-tls-or-authentication-can-i-add-those). TLS and authentication aren't available now, so let's list it as a drawback, right.

## 2. Plain Configuration

In general, there is `user experience`.

Not everyone is familiar with plain configuration file(s). When I introduce Prometheus to my colleagues, how great it is, what it can do, blah..., everytime they ask me like:

```
(People) - "Hey, how can I add a new target, change rule?"
(Me) - "Open configuration files, like this" *click* ... "find this line and change it" *typing, typing*
(People) - "Huh, what..." *disappointed*
```

Then they deny all wonderful features I mentioned before. :sweat: :sweat:

Even me, sometimes I wish that Prometheus provides an user interface to update its configuration. [LINE's Promgen]() for example:

![](https://raw.githubusercontent.com/line/promgen/master/docs/images/screenshot.png)

## 3. Doesn't have RBAC (Role-based access control)

Prometheus doesn't have user, project, group, role and permission concepts. In production, the number of targets keeps increasing rapidly, I couldn't handle them all. I want to share Prometheus configuration with someone else, so they can update it for me. But at the same time, I don't want they change other set of targets. "Please don't touch anything rather than your targets!" and no guarantee that my configuration won't be changed suddenly. You know, *Humans are all curious creatures*.

In my expectation, Prometheus could has an user/project management with RBAC.

## 4. High-availability

Prometheus itself provides no real HA/clustering support. As such the best-practice is to run multiple (e.g N) hosts with the same config (and it should be **Active-Passive model** instead of **Active-Active**). Data between Prometheus servers aren't sync with each other. They aren't persistent data.

If we have 3 Prometheus servers, metrics have to be scraped 3 times. It increases network traffics and target resource usages (a little bit).

Another thing should be considered as a drawback. Prometheus resource are restricted on a single physical servers that has its own limit. We can scale up only, to scale out we have to split a set of targets to other Prometheus servers manually.

## 5. The lack of documentation

IMO, Prometheus doesn't give enough necessary information for user. Many important tips I have to learn from [Robust Perception blog](https://www.robustperception.io/) instead of official documentation. But this is just a minor drawback, Prometheus is an open-source project so we can contribute to it :muscle:.

## Conclusion

Everything isn't perfect. Prometheus isn't an exception, it still has some drawbacks (IMO). Note again that there is my opinon, it could be wrong. Someone can tell that Prometheus is good enough, Prometheus should focus on performance rather than wasting time on side features... If you have other opinions, please leave comments bellow :point_down:.
