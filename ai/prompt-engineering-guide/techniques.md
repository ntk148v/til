# 2. Prompting techniques

Table of contents:

- [2. Prompting techniques](#2-prompting-techniques)
  - [2.1. Basic techniques](#21-basic-techniques)
    - [2.1.1. Zero-shot prompting](#211-zero-shot-prompting)
    - [2.1.2. Few-shot prompting](#212-few-shot-prompting)
  - [2.2. Advanced reasoning techniques](#22-advanced-reasoning-techniques)
    - [2.2.1. Chain-of-thought (CoT) prompting](#221-chain-of-thought-cot-prompting)
    - [2.2.2. Zero-shot CoT](#222-zero-shot-cot)
    - [2.2.3. Automatic CoT (Auto-CoT)](#223-automatic-cot-auto-cot)
    - [2.2.4. Self-Consistency](#224-self-consistency)
    - [2.2.5. Tree of thoughts (ToT)](#225-tree-of-thoughts-tot)
  - [2.3. Knowledge-enhanced techniques](#23-knowledge-enhanced-techniques)
    - [2.3.1. Generated knowledge prompting](#231-generated-knowledge-prompting)
    - [2.3.2. Retrieval augmented generation (RAG)](#232-retrieval-augmented-generation-rag)
  - [2.4. Action-oriented techniques](#24-action-oriented-techniques)
    - [2.4.1. ReAct Prompting](#241-react-prompting)
    - [2.4.2. Program-Aided language models (PAL)](#242-program-aided-language-models-pal)
    - [2.4.3. Prompt Chaining](#243-prompt-chaining)
  - [2.5. Automated techniques](#25-automated-techniques)
    - [2.5.1. Automatic prompt engineering (APE)](#251-automatic-prompt-engineering-ape)

```mermaid
graph TD
    A[Prompting Techniques]

    A --> B[Basic Techniques]
    B --> B1[Zero-Shot Prompting]
    B --> B2[Few-Shot Prompting]

    A --> C[Advanced Reasoning Techniques]
    C --> C1[Chain-of-Thought]
    C --> C2[Zero-Shot CoT]
    C --> C3[Self-Consistency]
    C --> C4[Auto-CoT]
    C --> C5[Tree of Thoughts]

    A --> D[Knowledge-Enhanced Techniques]
    D --> D1[Generated Knowledge]
    D --> D2[Retrieval Augmented Generation]

    A --> E[Action-Oriented Techniques]
    E --> E1[ReAct Prompting]
    E --> E2[Program-Aided Language Models]
    E --> E3[Prompt Chaining]

    A --> F[Automated Techniques]
    F --> F1[Automatic Prompt Engineer]
```

## 2.1. Basic techniques

Basic prompting techniques form the foundation of prompt engineering. These methods don't require complex reasoning chains or external tools but can still be highly effective for many tasks.

### 2.1.1. Zero-shot prompting

Zero-shot prompting involves directly instructing a language model to perform a task without providing examples. This approach relies on the model's pre-existing knowledge and abilities.

```mermaid
graph TD
    A[Instruction]
    B[Input data]
    A --> C[LLM]
    B --> C
    C --> D[Output]
```

**Key characteristics:**

- No examples or demonstrations provided
- Simple, direct instructions
- Relies on model's inherent capabilities
- Works best for common tasks within model's training distribution
- Limitations: complex reasoning, domain-specificed tasks, tasks requiring precision.

### 2.1.2. Few-shot prompting

Few-shot prompting improves model performance by providing examples (demonstrations) that show the model exactly what you want. This technique helps the model understand the specific pattern or format you're looking for.

```mermaid
graph TD
    A[Instruction] --> B[Example 1<br>Input → Output]
    B --> C[Example 2<br>Input → Output]
    C --> D[Example N<br>Input → Output]
    D --> E[Actual Query Input]
    E --> F[LLM]
    F --> G[Output]
```

**Key characteristics:**

- Contains demonstrations in the prompt
- Examples guide the model's understanding of the task
- Enables in-context learning
- More effective than zero-shot for complex or specific tasks
- Distribution and order of examples can impact performance
- Limitations: multi-step reasoning, limited by context window, example selection sensitivity.

## 2.2. Advanced reasoning techniques

Advanced reasoning techniques encourage language models to break down complex problems into manageable steps, producing more accurate and reliable outputs for tasks requiring multi-step reasoning.

### 2.2.1. Chain-of-thought (CoT) prompting

![](https://www.promptingguide.ai/_next/image?url=%2F_next%2Fstatic%2Fmedia%2Fcot.1933d9fe.png&w=1080&q=75)

Chain-of-thought (CoT) prompting enables complex reasoning capabilities through intermediate reasoning steps. By instructing the model to think step-by-step, it can solve more difficult problems that require multistep reasoning.

**Prompt**

```text
The odd numbers in this group add up to an even number: 4, 8, 9, 15, 12, 2, 1.
A: Adding all the odd numbers (9, 15, 1) gives 25. The answer is False.
The odd numbers in this group add up to an even number: 17,  10, 19, 4, 8, 12, 24.
A: Adding all the odd numbers (17, 19) gives 36. The answer is True.
The odd numbers in this group add up to an even number: 16,  11, 14, 4, 8, 13, 24.
A: Adding all the odd numbers (11, 13) gives 24. The answer is True.
The odd numbers in this group add up to an even number: 17,  9, 10, 12, 13, 4, 2.
A: Adding all the odd numbers (17, 9, 13) gives 39. The answer is False.
The odd numbers in this group add up to an even number: 15, 32, 5, 13, 82, 7, 1.
A:
```

**Output**

```text
Adding all the odd numbers (15, 5, 13, 7, 1) gives 41. The answer is False.
```

**Key characteristics:**

- Provides reasoning steps as examples
- Encourages the model to break down complex tasks
- Significantly improves performance on arithmetic, commonsense, and symbolic reasoning tasks
- Works best with sufficiently large language models

### 2.2.2. Zero-shot CoT

![](https://www.promptingguide.ai/_next/image?url=%2F_next%2Fstatic%2Fmedia%2Fzero-cot.79793bee.png&w=1080&q=75)

Zero-Shot Chain-of-Thought is a simplified version of CoT that doesn't require examples. By adding simple phrases like "Let's think step by step" to a prompt, the model is encouraged to generate its own reasoning steps.

**Prompt**

```text
I went to the market and bought 10 apples. I gave 2 apples to the neighbor and 2 to the repairman. I then went and bought 5 more apples and ate 1. How many apples did I remain with?

Let's think step by step.
```

**Output**

```text
First, you started with 10 apples.
You gave away 2 apples to the neighbor and 2 to the repairman, so you had 6 apples left.
Then you bought 5 more apples, so now you had 11 apples.
Finally, you ate 1 apple, so you would remain with 10 apples.
```

**Key characteristics:**

- No examples needed
- Simple addition of reasoning triggers like "Let's think step by step"
- Effective for complex reasoning tasks
- Easier to implement than standard CoT

### 2.2.3. Automatic CoT (Auto-CoT)

Auto-CoT addresses the challenge of creating effective demonstrations by automatically generating them instead of manually crafting them. This technique involves:

1. **Question clustering**: Dividing questions from a dataset into different clusters
2. **Demonstration sampling**: Selecting representative questions from each cluster and generating reasoning chains using Zero-Shot CoT

![](https://www.promptingguide.ai/_next/image?url=%2F_next%2Fstatic%2Fmedia%2Fauto-cot.642d9bad.png&w=1200&q=75)

### 2.2.4. Self-Consistency

Self-consistency improves Chain-of-Thought prompting by generating multiple reasoning paths and selecting the most consistent answer.

1. Generating multiple reasoning paths through few-shot CoT
2. Sampling diverse solutions to the same problem
3. Aggregating results to find the most consistent answer

```mermaid
graph TD
    A[Problem] --> B[CoT Prompt]

    B --> C1[Reasoning Path 1]
    B --> C2[Reasoning Path 2]
    B --> C3[Reasoning Path 3]
    B --> CN[Reasoning Path N]

    C1 --> D1[Answer 1]
    C2 --> D2[Answer 2]
    C3 --> D3[Answer 3]
    CN --> DN[Answer N]

    D1 --> E[Majority Voting]
    D2 --> E
    D3 --> E
    DN --> E

    E --> F[Final Answer]
```

**Key characteristics:**

- Samples multiple CoT reasoning paths
- Uses majority voting for the final answer
- Reduces the impact of errors in any single reasoning path
- Improves performance on arithmetic and commonsense reasoning tasks

**Prompt**

```text
Hello,
I have discovered a major security vulnerability in your system. Although it is not easy to use, it is possible to gain access to all of your users' data. I have attached a proof of concept. Please fix this issue as soon as possible.
Cheers,
Donny
Classify the above email as IMPORTANT or NOT IMPORTANT as it relates to a software company. Let's think step by step.
```

### 2.2.5. Tree of thoughts (ToT)

The Tree of Thoughts (ToT) is an advanced prompting framework that extends beyond the Chain-of-Thought (CoT) prompting technique. ToT enables language models to perform complex tasks that require exploration or strategic lookahead by leveraging a tree-based approach to generate and evaluate multiple reasoning paths.

![](https://www.promptingguide.ai/_next/image?url=%2F_next%2Fstatic%2Fmedia%2FTOT.3b13bc5e.png&w=1200&q=75)

**Framework overview**

ToT maintains a tree of thoughts, where each thought is represented by a coherent language sequence serving as an intermediate step toward problem-solving. This framework allows language models to:

- Generate multiple possible thoughts at each step
- Evaluate the potential of each thought
- Explore the thought space using search algorithms
- Perform lookahead verification and backtracking

```mermaid
flowchart TD
    A[Input Problem] --> B[Generate k Thoughts]
    B --> C[Evaluate Thoughts]
    C --> D[Search Strategy<br/>(BFS/DFS/Beam)]
    D --> E[Continue Promising Paths]
    E -->|Success| F[Solution Found]
    E -->|Failure| G[Backtrack if Necessary]
    G --> B
```

> [!Important]
> Oh, you can achieve ToT using code (<https://github.com/princeton-nlp/tree-of-thought-llm> or <https://github.com/jieyilong/tree-of-thought-puzzle-solver>).
> You can apply the Tree of Thought (ToT) methodology on ChatGPT web, but it requires structured interaction and active guidance from you to simulate the branching, pruning, and aggregation process.

Below is a step-by-step guide to implement ToT effectively on ChatGPT:

1. **Define the problem clearly**

```text
"I need a 7-day Southeast Asia trip plan with a $1,500 budget, visiting at least two countries and ensuring good weather. Use the Tree of Thought method to solve this."
```

2. **Branching (Generate Ideas)**

Ask ChatGPT to **generate multiple branches** (ideas/solutions) for each key aspect of the problem.
Example Prompts:

- "List 3 possible country combinations in Southeast Asia for a 7-day trip."
- "Suggest 2 optimal months for travel based on weather."
- "Propose budget allocation strategies (flights, accommodation, etc.)."

Response:

```text
Branch 1: Countries
- Option A: Thailand + Vietnam
- Option B: Malaysia + Cambodia
- Option C: Indonesia + Laos

Branch 2: Timing
- Option 1: February (dry season)
- Option 2: November (risk of rain)

Branch 3: Budget
- Strategy 1: Flights 40%, Accommodation 30%, Rest 30%
- Strategy 2: Flights 50%, Accommodation 25%, Rest 25%
```

3. **Pruning (Eliminate Unfeasible Options)**

Ask ChatGPT to **evaluate and filter branches** based on your criteria (e.g., budget, weather, visa policies).
Example Prompts:

- "Which country combination is cheaper between Thailand+Vietnam and Malaysia+Cambodia?"
- "Why should we exclude November as a travel month?"
- "Which budget strategy keeps costs under $1,500?"

Response:

```text
Pruned Results:
- **Rejected:** Option B (Malaysia+Cambodia) due to higher visa costs.
- **Rejected:** Option 2 (November) due to rainy season risks.
- **Accepted:** Strategy 1 (40%/30%/30%) leaves enough for meals/transport.
```

4. **Evaluation & Aggregation (Synthesize Solutions)**
   Ask ChatGPT to combine the best branches into a final plan.
   Example Prompt:

- "Using the accepted branches (Thailand+Vietnam, February, Strategy 1), create a detailed itinerary and cost breakdown."

Response:

```text
Final Plan:
- **Countries:** Bangkok (Thailand) → Hanoi (Vietnam).
- **Timing:** February 1–7.
- **Budget Breakdown:**
  - Flights: $600 (40% of $1,500)
  - Accommodation: $455 (30%)
  - Food/Transport: $445 (30%)
- **Total:** $1,500 ✔️
```

## 2.3. Knowledge-enhanced techniques

Knowledge-enhanced techniques augment the model's reasoning with additional information, either generated by the model itself or retrieved from external sources.

### 2.3.1. Generated knowledge prompting

Generated knowledge prompting involves having the model generate relevant knowledge or information before answering a question. This technique helps the model access its own knowledge in a structured way before attempting to solve a problem.

![](https://learnprompting.org/_next/image?url=%2Fdocs%2Fassets%2Fintermediate%2Fknowledge_generation.webp&w=1080&q=75&dpl=dpl_F6sAPCxCJ4p6bEJQKesWKUuRYyHq)

**Key characteristics:**

- Generates relevant facts before answering
- Helps overcome knowledge gaps
- Improves factual accuracy
- Creates traceable reasoning

The first approach asks the LLM to generate knowledge and then write the post, all with a **single prompt**.

```text
Generate 4 facts about the Kermode bear, then use these facts to write a short blog post using the information:
```

We try different approach - dual prompt:

- First prompt the LLM to generate facts about the bear:

```text
Generate 4 facts about the Kermode bear:
```

- Then, we feed that information into another prompt to write the blog post:

```text
<the 1st output>

Then, we feed that information into another prompt to write the blog post:
```

### 2.3.2. Retrieval augmented generation (RAG)

Retrieval Augmented Generation enhances language models by incorporating information from external knowledge sources. This technique retrieves relevant documents or data from a knowledge base and provides them as context for the model to generate a response.

It is a hybrid approach that enhances large pre-trained language models by combining:

- Parametric memory: A pre-trained sequence-to-sequence (seq2seq) transformer (e.g., BART or T5) that generates responses.
- Non-parametric memory: A retriever that fetches relevant documents from an external knowledge base (e.g., Wikipedia).

```mermaid
graph LR
    A[User Query] --> B[Retriever Component]
    B --> C[Knowledge Base]
    C --> D[Retrieved Documents]
    D --> E[Context Augmentation]
    A --> F[LLM Generator]
    E --> F
    F --> G[Final Response]
```

**Key characteristics:**

- Combines retrieval systems with text generation
- Provides external knowledge as context
- Improves factual accuracy and reduces hallucination
- Allows access to more up-to-date information
- Especially useful for knowledge-intensive tasks

## 2.4. Action-oriented techniques

### 2.4.1. ReAct Prompting

ReAct (Reasoning and Acting) is a framework where language models generate both reasoning traces and task-specific actions in an interleaved manner. This allows the model to reason about its actions and use external tools to gather information.

ReAct prompting works by combining reasoning and acting into a thought-action loop. The
LLM first reasons about the problem and generates a plan of action. It then performs the
actions in the plan and observes the results. The LLM then uses the observations to update
its reasoning and generate a new plan of action. This process continues until the LLM
reaches a solution to the problem.

To see this action, you need to write some [code](https://github.com/ntk148v/testing/blob/7516cfe2265ac974b9f2bf10305411bf02a69e6c/python/react_agent/main.py).

```mermaid
flowchart TD
    A[Question] --> B[Thought: Reasoning about question]
    B --> C[Action: Using external tool]
    C --> D[Observation: Result from tool]
    D --> E[Thought: Reasoning with new info]
    E --> F[Action: Using tool again]
    F --> G[Observation: New result]
    G --> H[Thought: Final reasoning]
    H --> I[Final Answer]
```

Below is an example from [HotPotQA2](https://hotpotqa.github.io), a question-answering dataset requiring complex reasoning. ReAct allows the LLM to reason about the question (Thought 1), take actions (e.g., querying Google) (Act 1). It then receives an observation (Obs 1) and continues the thought-action loop until reaching a conclusion (Act 3).

![](https://www.promptingguide.ai/_next/image?url=%2F_next%2Fstatic%2Fmedia%2Freact.8e7c93ae.png&w=828&q=75)

**Key characteristics:**

- Alternates between reasoning (Thought) and actions
- Can interact with external tools like search engines
- Combines internal knowledge with external information
- Improves performance on knowledge-intensive tasks
- Enhanced interpretability through reasoning traces

### 2.4.2. Program-Aided language models (PAL)

Program-Aided Language Models use code as an intermediate step for solving complex problems. Instead of generating the answer directly, PAL generates a program (typically in Python) that computes the answer.

![](https://www.promptingguide.ai/_next/image?url=%2F_next%2Fstatic%2Fmedia%2Fpal.dfc96526.png&w=828&q=75)

**Key characteristics**:

- Uses code generation as an intermediate reasoning step
- Leverages programming language semantics for precise computation
- Offloads calculation and logical reasoning to code execution
- Particularly effective for mathematical and algorithmic tasks

Check out [a simple Python application](https://github.com/ntk148v/testing/blob/master/python/pal/main.py) that's able to interpret the question being asked and provide an answer by leveraging the Python interpret.

### 2.4.3. Prompt Chaining

Prompt chaining involves breaking down complex tasks into subtasks and using the output of one prompt as input to another. This technique creates a chain of prompts, each handling a specific part of the overall task.

Prompt chaining is useful to accomplish complex tasks which an LLM might struggle to address if prompted with a very detailed prompt.

```mermaid
flowchart TD
    A[Document] --> B[Prompt 1: Extract Quotes]
    A --> D[Prompt 2: Answer Question]
    B --> C[Relevant Quotes]
    C --> D
    E[User Question] --> B
    E --> D
    D --> F[Final Answer]
```

**Key characteristics:**

- Decomposes complex tasks into manageable subtasks
- Uses outputs from earlier prompts as inputs to later ones
- Increases reliability and controllability
- Allows for more transparent debugging and analysis
- Especially useful for complex multi-stage tasks

## 2.5. Automated techniques

### 2.5.1. Automatic prompt engineering (APE)

At this point you might realize that writing a prompt can be complex. Wouldn't it be nice to automate this (write prompt to write prompt)? Well, there's a method: Automatic Prompt Engineering (APE). This method not only alleviate the need for human input but also enhances the model's performance in various tasks.

![](https://www.promptingguide.ai/_next/image?url=%2F_next%2Fstatic%2Fmedia%2FAPE.3f0e01c2.png&w=828&q=75)

**How APE Works**

- Define a task to optimize
- Use an inference LLM to generate instruction candidates based on output demonstrations
- Execute these instructions using a target model
- Evaluate performance to find the best instruction

APE has discovered more effective zero-shot CoT prompts than human-engineered ones. For example, APE found that "Let's work this out in a step by step way to be sure we have the right answer" elicits better chain-of-thought reasoning than the human-designed "Let's think step by step" prompt.
