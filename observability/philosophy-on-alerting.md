# My Philosophy on Alerting

Source:

- <https://docs.google.com/document/d/199PqyG3UsyXlwieHaqbGiWVa8eMWi8zzAn0YfcApr8Q/edit?usp=sharing>
- <https://www.oreilly.com/radar/monitoring-distributed-systems/>

## Monitor for your users

- Symptom-based monitoring > cause-based monitoring.
- Users, in general, care about a small number of things:
  - Basic availability and correctness
  - Latency
  - Completeness/freshness/durability
  - Features
- Cause-based alerts are bad, but sometimes necessary. ere's (often) no symptoms to "almost" running out of quota
or memory or disk I/O, etc., so you want rules to know you're walking towards a cliff. Use these
sparingly; don't write cause-based paging rules for symptoms you can catch otherwise.

## Tickets, Reports and Email

- Bug or ticket-tracking systems can be usefuil.
- A daily (or more frequent) report can work too.
- Every alert should be tracked through a workflow system.

The underlying point is to create a system that still has accountability for responsiveness, but doesn't have the high cost of waking someone up, interrupting their dinner, or preventing snuggling with a significant other.

## Playbooks

Playbooks (or runbooks) are an important part of an alerting system; it's best to have an entry for each alert or family of alerts that catch a symptom, which can further explain what the alert means and how it might be addressed.

## Tracking & Accountability
