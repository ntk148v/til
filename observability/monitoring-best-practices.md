# Monitoring Best Practices

> "You can't improve what you don't measure, but you can definitely overwhelm yourself by measuring everything."

## Table of Contents

- [Monitoring Best Practices](#monitoring-best-practices)
  - [Table of Contents](#table-of-contents)
  - [1. Common Mistakes](#1-common-mistakes)
    - [1.1. Monitoring Everything, Not What Matters](#11-monitoring-everything-not-what-matters)
    - [1.2. High Cardinality Metrics](#12-high-cardinality-metrics)
    - [1.3. Alerting on Everything (Alert Fatigue)](#13-alerting-on-everything-alert-fatigue)
    - [1.4. Not Testing Alerts](#14-not-testing-alerts)
    - [1.5. Over-engineering the Monitoring System](#15-over-engineering-the-monitoring-system)
    - [1.6. Forgetting about the Human Element](#16-forgetting-about-the-human-element)
    - [1.7. Forget To Monitor The Monitoring System](#17-forget-to-monitor-the-monitoring-system)
  - [2. Best practices](#2-best-practices)
    - [2.1. What to be monitored?](#21-what-to-be-monitored)

> [!Important]
>
> "The best monitoring is invisible until you need it, and invaluable when you do."

After years in the trenches of monitoring, I've learned that great observability is less about fancy dashboards and more about asking the right questions. Here are the most valuable lessons, mistakes, and creative best practices I've picked up—often the hard way.

## 1. Common Mistakes

### 1.1. Monitoring Everything, Not What Matters

_What should you monitor?_ The rookie answer: **everything**. The reality: you'll drown in data and never look at most of it.

![Too many metrics meme](https://giphy.com/embed/fxZ7cC3zYIVXi)

More metrics ≠ better monitoring. Focus on signals that actually reflect user experience or system health. Ask yourself:

- Can I explain why this metric matters in one sentence?
- Do I use this metric in a dashboard, alert, or decision? If not, delete it.

### 1.2. High Cardinality Metrics

High cardinality (think: a label for every user, container, or request) is the silent killer of monitoring systems. Prometheus TSDB will groan, queries will crawl, and you'll be troubleshooting your monitoring stack instead of your app.

**Creative fixes:**

- **Ditch high-cardinality labels** like `user_id` or `session_id` unless you truly need them.
- **Aggregate early:** If you always aggregate in queries, aggregate at the source and store only what you need.
- **Keep label combos minimal:** Too many labels = exponential time series growth.
- **Monitor your monitoring:** Track cardinality itself to catch issues before they snowball.

### 1.3. Alerting on Everything (Alert Fatigue)

[Alert fatigue](https://en.wikipedia.org/wiki/Alarm_fatigue) is real. Once, ~~my boss~~ someone requires to set up alerts for every minor metric. The result? Thousands of notifications, most ignored. When a real incident hit, it was lost in the noise.

**How to stay sane:**

- Only alert on _actionable_ issues that need a human.
- Only wake people for _critical_ incidents. If you can go back to sleep after an alert, it probably shouldn't have woken you up.

### 1.4. Not Testing Alerts

Alert rules are rarely perfect on the first try. That's normal! But if you never test or tune them, you'll miss real problems or get woken up for nothing.

**Pro tip:** Regularly simulate incidents and review alert performance. Tweak thresholds and logic as your system evolves.

### 1.5. Over-engineering the Monitoring System

I've been there: building a distributed, multi-cluster, self-healing monitoring monster... for a tiny app. Start simple. Build for your current scale, not your dream scale. You can always upgrade later.

### 1.6. Forgetting about the Human Element

A monitoring system is only as effective as the people behind it. If your team can't interpret the data or respond to alerts, even the best setup is useless.

**Creative solutions:**

- Invest in _clear, living documentation_ and _regular hands-on training_.
- Make sure everyone knows how to use the tools, read dashboards, and follow runbooks.
- Celebrate learning from incidents—blameless postmortems help everyone grow.

### 1.7. Forget To Monitor The Monitoring System

It's easy to assume your monitoring stack is always up and running—until the day you need it and discover it's been down for hours. Ironically, one of the most common blind spots is not monitoring the health of your own monitoring system.

**Why it matters:**

- If Prometheus, Grafana, or your alerting pipeline goes down, you lose visibility just when you need it most.
- Silent failures in your monitoring stack can lead to missed incidents, delayed responses, and a false sense of security.

**How to avoid this trap:**

- Set up external probes (blackbox monitoring) to check the availability of your monitoring endpoints and dashboards.
- Monitor the resource usage (CPU, memory, disk) and error logs of your monitoring components.
- Create meta-alerts: alert if no data is received from critical exporters, or if alert volume drops to zero unexpectedly.
- Regularly test your monitoring and alerting pipeline end-to-end—simulate failures and ensure alerts are delivered.

> "Trust, but verify—even your monitoring tools."

**If your monitoring system breaks, you won't know your application is broken either.**

## 2. Best practices

### 2.1. What to be monitored?

**Monitor your actual pain points, not theoretical ones**. You should focus on the most common failure issues.

If you don't have any failure, good for you (but usually it's impossible). You may want to check this

> WIPPPPPP
