# Alertmanager Silence

## A silence is a snooze

- A silence similar to that of the snooze feature of your alarm clock that wakes you up every morning to get out of bed for work. When you silence an alert, you're not scheduling the Alertmanager to not alert you of a particular event for certain periods of the day, or indefinitely ignoring the firing of a particular alert. It's simply a tool for the engineers responding to the alert to not have it ringing in their ear while they try to deal with the issue causing it in the first place.
- When use?
  - Alerts fired by the Alertmanager only ever stop once their causes have been dealt with. Using silences allows us to simply mute alerts for a given amount of time while we investigate the problem causing them.
  - Another scenario where you may find silencing your alerts useful is in the case of maintenance work. In order to prevent the unnessary firing alerts for machines you know are going to be down for maintenance, one could silence these alerts for the time period they'll be worked on to avoid pointless alerts being sent out to your team.

## Control silences via the Alertmanager

- Go to web interface (usually `<host_ip>:9093`) and click the New Silence button.

![schedule-silence](./imgs/schedule_silence.png)

- Silences specify a start time, end time, or a duration. The alerts to be silenced are identified by matching alerts using labels, much like alert routing. You can use straight matches - for example, matching every alert that has a label with a specify value - or you can use a regular expression match. You also need to specify an author for the silence and a comment explaining why alerts are being silenced.

![new-silence](./imgs/new_silence.png)

> NOTE: Using regex

![new-silence-regex](./imgs/new_silence_regex.png)

- Note that, you can fill start time in the future, the Silence will be in PENDING state. Otherwise, it should be in ACTIVE state.

- We click Create to create the new Silence (and we can use Preview Alerts to identify if any current alerts will be silenced). Once created we can edit a silence or expire it to remove the silence.

![edit-expire-silence](./imgs/edit_expire_silence.png)

- Here is the silence with its affected alerts

![affected-alerts](./imgs/affected_alerts.png)
