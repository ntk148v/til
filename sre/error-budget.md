# Error budget

Source: <https://www.atlassian.com/incident-management/kpis/error-budget>

Every development, operations, and IT team knows that sometimes incidents happen. This reality means SLAs should never promise 100% uptime.

It also means that if your company is very good at avoiding or resolving incidents, you might not consistently knock your uptime goals out of the park. Perhaps you promise 99% uptime and actually come closer to 99.5%. Perhaps you promise 99.5% uptime and actually reach 99.99% on a typical month.

When that happens, industry experts recommend that instead of setting user expectations too high by constantly overshooting your promises, you consider that extra .99% an error budget—time that your team can use to take risks.

## What is an error budget?

An **error budget** is the maximum amount of time that a technical system can fail without contratual consequences.

For example, if your SLA specifies that systems will function 99.99% of the time before the business hsa to composensate customers for the outage, that measns your error budget (or the time your systems can go down without consequences) is 52 minutes and 35 seconds per years.

## How to use an error budget

- Error budgets based on uptime:
  - Most teams monitor uptime on a monthly basis. If availability is above the number promised by the SLA/SLO, the team can release new features and take risks. If it’s below the target, releases halt until the target numbers are back on track.
- Error budgets based on successful requests:
