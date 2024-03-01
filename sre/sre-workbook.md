# SRE Workbook

Source: <https://sre.google/workbook>

## Chapter 2: Implementing SLOs

- Service level objectives (SLOs) specify a target level for the reliability of your service.
- An SLO sets a target level of reliability for the service’s customers.
- What to Measure: using SLIs.
  - An SLI is an _indicator_ of the level of service that you are providing.
  - Treat the SLI as the ratio of two numbers: the number of good events dividied by the total number of events. For example:
    - Number of the successful HTTP requests / total HTTP requests (success rate).
    - Number of gRPC calls that completed successfully in < 100 ms / total gRPC requests
  - We have found this ratio scale intuitive, and this style lends itself easily to the concept of an error budget: the SLO is a target percentage and the error budget is _100% - SLO_.
  - When attempting to formulate SLIs for the first time, you might find it useful to further divide SLIs into:
    - _SLI specification_: the assessment of service outcome that you think matters to uses, independent of how it is measured.
    - _SLI implementation_: the SLI specification and a way to measure it.
- If you are having trouble figuring out what sort of SLIs to start with, it helps to start simple:
  - Choose one application for which you want to define SLOs. If your product comprises many applications, you can add those later.
  - Decide clearly who the “users” are in this situation. These are the people whose happiness you are optimizing.
  - Consider the common ways your users interact with your system—common tasks and critical activities.
  - Draw a high-level architecture diagram of your system; show the key components, the request flow, the data flow, and the critical dependencies. Group these components into categories listed in the following section (there may be some overlap and ambiguity; use your intuition and don’t let perfect be the enemy of the good).
- The easiest way to get started with settings SLIs is to abstract your system into a few common types of components:
  - _Request-driven_: the user creates some type of event and expects a response. For example, this could be an HTTP service where the user interacts with a browser or an API for mobile application.
  - _Pipeline_: a system that takes records as input, mutates them, and places the output somewhere else. This might be a simple process that runs on a single instance in real time, or a multistage batch process that takes many hours.
  - _Storage_: a system that accepts data (e.g., bytes, records, files, videos) and makes it available to be retrieved at a later date.

| Type of service | Type of SLI  | Description                                                                                                                                                                                                                                                                            |
| --------------- | ------------ | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Request-driven  | Availability | The proportion of requests that resulted in a successful response.                                                                                                                                                                                                                     |
| Request-driven  | Latency      | The proportion of requests that were faster than some threshold                                                                                                                                                                                                                        |
| Request-driven  | Quality      | If the service degrades gracefully when overloaded or when backends are unavailable, you need to measure the proportion of responses that were served in an undegraded state. For example, if the User Data store is unavailable, the game is still playable but uses generic imagery. |
| Pipeline        | Freshness    | The proportion of the data that was updated more recently than some time threshold. Ideally this metric counts how many times a user accessed the data, so that it most accurately reflects the user experience.                                                                       |
| Pipeline        | Correctness  | The proportion of records coming into the pipeline that resulted in the correct value coming out.                                                                                                                                                                                      |
| Pipeline        | Coverage     | For batch processing, the proportion of jobs that processed above some target amount of data. For streaming processing, the proportion of incoming records that were successfully processed within some time window.                                                                   |
| Storage         | Durability   |

The proportion of records written that can be successfully read. Take particular care with durability SLIs: the data that the user wants may be only a small portion of the data that is stored. For example, if you have 1 billion records for the previous 10 years, but the user wants only the records from today (which are unavailable), then they will be unhappy even though almost all of their data is readable.|

- SLOs can be defined over various time intervals, and can use either a rolling window or a calendar-aligned window (e.g., a month). 
  - Rolling windows are more closely aligned with user experience.
  - Calendar windows are more closely aligned with business planning and project work. For example, you might evaluate your SLOs every quarter to determine where to focus the next quarter's project headcount.
  - Shorter time windows allow you to make decisions more quickly.
  - Longer time periods are better for more strategic decisions.
- Getting Stakeholder Agreement.
- Once you have an SLO, you can use the SLO to derive an error budget. In order to use this error budget, you need a policy outlining what to do when your service runs out of budget.
  - Need the agreement of all stakeholders - the product manager, the development team, and the SREs.
  - If all three parties do not agree to enforce the error budget policy, you need to iterate on the SLIs and SLOs until all stakeholders are happy.
- Documenting the SLO and Error Budget Policy.
- Dashboard and reports.
