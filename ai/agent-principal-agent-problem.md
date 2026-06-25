# The agent principal-agent problem

Source: <https://crawshaw.io/blog/agent-principal-agent>

Code review back in the day, was very simple:

1. A human makes a change.
2. This change is packaged up, sent to another human for commentary.
3. Rounds of commentary and adjustments continue until the reviewer approves (LGTMs) it.
4. The change is committed.

Agents broke this. If you insert an agent into the existing process, your best possible outcome is:

1. A human instructs a machine to make a change.
2. The human reviews the code, iterates with comments until they approve it.
3. This change is packaged up, sent to another human for commentary.
4. Rounds of commentary and adjustments continue until the reviewer approves (LGTMs) it.
5. The change is committed.

-> double the amount of review. Additionally, the whole reason engineers use agents is it improves productivity. More total changes are generated. So we doubled review, and increased the total changes

What happens in reality are processes like this:

1. A human instructs a machine to make a change.
2. This change is lightly QA'd, packaged up, sent to another human for commentary.
3. Rounds of commentary come back from the reviewer and are sent wholesale to the machine for adjustments until the reviewer approves (LGTMs) it.
4. The change is committed.

This is an example of what economists call the [principal-agent problem](https://en.wikipedia.org/wiki/Principal%E2%80%93agent_problem): the reviewer is the principal, the contributor is the agent, and code review only worked because the reviewer could cheaply infer effort from reading the code. Agents collapse that signal. This is what is killing OSS, and it is commonly being referred to as "slop PRs". There is no incentive for the human driving the agent to actually read the code or spend time thinking about what the reviewer says.

**Potential solutions**

Small high-trust teams have an easy process they can adopt:

1. A human instructs a machine to make a change.
2. The human reviews the code, iterates with comments until they approve it.
3. They push the change to production and deploy.

This is not tenable in low-trust environments, i.e. large companies. You have to trust your co-workers to start a conversation about architectural changes before they do it.
