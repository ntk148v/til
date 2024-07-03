# Diagnose RemoteFX graphics performance issues

Source:

- <https://learn.microsoft.com/en-us/azure/virtual-desktop/remotefx-graphics-performance-counters>
- <https://learn.microsoft.com/en-us/windows-server/remote/remote-desktop-services/rds-rdsh-performance-counters>

Graphics-related performance issues generally into four categories:

- Low frame rate
- Random stalls
- High input latency
- Poor frame quality

## Addressing the issue

```mermaid
flowchard TD
    A[Face RemoteFX graphics performance issues] --> B{Is it Low Frame rate/Random stalls/High input latency issues?}
    B -- Yes --> C[Check Output Frames/Second counter]
    B -- No --> D[It may be Poor frame quality]
    C --> E{Output Frames/Second < Input Frames/Second?}
    E -- Yes --> F[Check Frames Skipped/Second counters (Insufficient Server/Client/Network Resources)]
    F --> J[Here we go! This is the root cause]
    E -- No --> G[Check Average Encoding Time]
    G --> H{Average Encoding Time < 33ms}
    H --> Yes --> I[May be an issue with the app or OS you are using]
    H --> No --> J[Here we go! This is the root cause]
    D --> K[Check Frame Quality counter]
    K --> J[Here we go! This is the root cause]
```

- First check Output Frames/Second counter. It measures the number of frames made available to the client.
  - Output Frames/Second < Input Frames/Second -> frames are being skipped -> check Frames Skipped/Second counters.
- There are 3 types of Frames Skipped/Second counters:
  - Frames Skipped/Second (Insufficient Server Resources)
  - Frames Skipped/Second (Insufficient Network Resources)
  - Frames Skipped/Second (Insufficient Client Resources)
- A high value for any of the Frames Skipped/Second counters implies that the problem is related to the resource the counter tracks. For example, if the client doesn't decode and present frames at the same rate the server provides the frames, the Frames Skipped/Second (Insufficient Client Resources) counter will be high.
- If the Output Frames/Second counter matches the Input Frames/Second counter, yet you still notice unusual lag or stalling, Average Encoding Time may be the culprit. Encoding is a synchronous process that occurs on the server in the single-session (vGPU) scenario and on the VM in the multi-session scenario. Average Encoding Time should be under 33 ms. If Average Encoding Time is under 33 ms but you still have performance issues, there may be an issue with the app or operating system you are using. For more information about diagnosing app-related issues, see [User Input Delay performance counters](https://learn.microsoft.com/en-us/windows-server/remote/remote-desktop-services/rds-rdsh-performance-counters/).
- Use the Frame Quality counter to diagnose frame quality issues. This counter expresses the quality of the output frame as a percentage of the quality of the source frame. The quality loss may be due to RemoteFX, or it may be inherent to the graphics source. If RemoteFX caused the quality loss, the issue may be a lack of network or server resources to send higher-fidelity content.

## Mitigation

If server resources are causing the bottleneck, try one of the following approaches to improve performance:

- Reduce the number of sessions per host.
- Increase the memory and compute resources on the server.
- Drop the resolution of the connection.

If network resources are causing the bottleneck, try one of the following approaches to improve network availability per session:

- Reduce the number of sessions per host.
- Use a higher-bandwidth network.
- Drop the resolution of the connection.

If client resources are causing the bottleneck, try one of the following approaches to improve performance:

- Install the most recent Remote Desktop client.
- Increase memory and compute resources on the client machine.
