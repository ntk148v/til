# AI agents

Source:

- <https://www.ibm.com/think/topics/ai-agents>
- <https://sendbird.com/blog/how-to-build-an-ai-agent>
- <https://blogs.nvidia.com/blog/what-is-agentic-ai/>
- <https://github.com/microsoft/ai-agents-for-beginners>
- <https://www.baseten.co/blog/compound-ai-systems-explained/>

## 1. What is AI agent?

- An AI agent refers to a system or program that is capable of autonomously performing tasks on behalf of a user or another system by designing its workflow and utilizing available tools.
- It can interact with its environment, gather data, and use that data to achieve predefined goals.

```python
def loop(llm):
    msg = user_input()
    while True:
        output, tool_calls = llm(msg)
        print("Agent: ", output)
        if tool_calls:
            msg = [ handle_tool_call(tc) for tc in tool_calls ]
        else:
            msg = user_input()
```

## 2. How do AI agents work?

- LLMs (of course) -> this enables the AI agent to receive instructions from non-technical teams, interpret its environment, and generate meaningful responses to users.
- Take 4-step approach:
  - **Perception**: AI agents gather data from various sources like customer interactions, databases, web searches, and social media.
  - **Reasoning**: AI agents analyze the collected data using advanced machine learning models.
  - **Action**: AI agents integrate with external tools and data to execute tasks based on the plans it has generated. Boundaries can be set to ensure tasks are completed correctly.
  - **Learning**: AI agents learn from each interaction, updating their knowledge base (or memoryy) to improve their accuracy and effectiveness.

![](https://blogs.nvidia.com/wp-content/uploads/2024/10/agentic-ai-workflow-1.png)

## 3. AI agents in action

- AI agents use reason to solve problems.
- Tool calling: From monolithic to compound AI
  - Monolithic AI uses single models or workflows tightly coupled with their infrastructure, while compound AI leverages multiple modularized processing components.
  - Compound AI systems combine multiple interacting components to form a holistic workflow:
    - Multiple AI/ML models (e.g., speech-to-text and text-to-image)
    - Distinct processing steps (like chunking an audio file before transcribing it)
    - Varying architectures (such as combining rule-based systems with ML models)
    - Dedicated hardware (CPUs and GPUs) and infrastructure for orchestration and inference.

  ![](https://sendbird.imgix.net/cms/What-is-an-AI-agent__1.png)

- AI agents learn and improve continuously.
  - AI agents learn from each interaction, refining their reasoning to continuously improve their accuracy and performance. They do this by storing interaction data in their knowledge base (memory), as well as receiving feedback from other agents or human managers.

  ![](https://sendbird.imgix.net/cms/What-is-an-AI-agent__2.png)

## 4. Reasoning paradigms

There is not one standard architecture for building AI agents.

- ReAct (Reasoning and Action)
  - Instruct agents to "think" and plan after each action taken and with each tool response to decide which tool to use next. These Think-Act-Observe loops are used to solve problems step by step and iteratively improve upon responses.
- ReWOO (Reasoning WithOut Observation)
  - Eliminate the dependence on tool outputs for action planning. Instead, agents plan upfront.
  - The ReWOO workflow is made up of three modules.
    - In the planning module, the agent anticipates its next steps given a user's prompt.
    - The next stage entails collecting the outputs produced by calling these tools.
    - Lastly, the agent pairs the initial plan with the tool outputs to formulate a response.

## 5. Types of AI agents

### 5.1. Simple reflex agents

- Does not hold any memory, nor does it interact with other agents if it is missing information.
- These agents function on a set of so-called reflexes or rules.
- If the agent encounters a situation that it is not prepared for, it cannot respond appropriately.

![](https://www.ibm.com/content/dam/connectedassets-adobe-cms/worldwide-content/creative-assets/s-migr/ul/g/17/5b/ai-agents-image1.component.xl.ts=1741183012419.png/content/adobe-cms/us/en/think/topics/ai-agents/jcr:content/root/table_of_contents/body-article-8/image)

### 5.2. Model-based reflex agents

- Use both their current perception and memory to maintain an internal model of the world. As the agent continues to receive new information, the model is updated. The agent's actions depend on its model, reflexes, previous precept and current state.
- Can store information in memory and can operate in environments that are partially observable and changing.
- Still limited by their set of rules.

![](https://www.ibm.com/content/dam/connectedassets-adobe-cms/worldwide-content/creative-assets/s-migr/ul/g/3a/2d/ai-agents-image2.component.m.ts=1741183012575.png/content/adobe-cms/us/en/think/topics/ai-agents/jcr:content/root/table_of_contents/body-article-8/image_1822054753)

### 5.3. Goal-based agents

- Have an internal model of the world and also a goal or set of goals.
- These agents search for action sequences that reach their goal and plan these actions before acting on them.

![](https://www.ibm.com/content/dam/connectedassets-adobe-cms/worldwide-content/creative-assets/s-migr/ul/g/e7/d8/ai-agents-image3.component.xl.ts=1741183012785.png/content/adobe-cms/us/en/think/topics/ai-agents/jcr:content/root/table_of_contents/body-article-8/image_848100326)

### 5.4. Utility-based agents

- Select the sequence of actions that reach the goal and also maximize utility or reward. Utility is calculated using a utility function.
- The criteria can include factors such as progression toward the goal, time requirements, or computational complexity. The agent then selects the actions that maximize the expected utility. Hence, these agents are useful in cases where multiple scenarios achieve a desired goal and an optimal one must be selected.

### 5.5. Learning agents

- Hold the same capabilities as the other agent types but are unique in their ability to learn.
- New experiences are added to their initial knowledge base, which occurs autonomously. This learning enhances the agent’s ability to operate in unfamiliar environments. Learning agents may be utility or goal-based in their reasoning and are comprised of four main elements:
  - Learning: This improves the agent's knowledge by learning from the environment through its precepts and sensors.
  - Critic: This provides feedback to the agent on whether the quality of its responses meets the performance standard.
  - Performance: This element is responsible for selecting actions upon learning.
  - Problem generator: This creates various proposals for actions to be taken.
