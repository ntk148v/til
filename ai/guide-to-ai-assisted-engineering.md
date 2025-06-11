# Guide to AI Assisted Engineering

Source: <https://getdx.com/uploads/guide-to-ai-assisted-engineering.pdf>

## 1. Part 1 - AI Prompting Techniques

### 1.1. Meta-prompting

- The technique of embedding instructions within a prompt to help a model understand how to approach and respond to the task.
- An example:

```prompt
Don't

Fix this Spring Boot error: [error details]
```

```prompt
Do

Debug the following Spring Boot error: [paste error details]

- Identify and explain the root cause.
- Provide a fixed version of the problematic code.
- Suggest best practices to prevent similar issues in the future.
 
Output should follow this format:

1) Error Message & Stack Trace (Summarized).
2) Root Cause Analysis (Explain why the error happened).
3) Fixed Code (With comments).
4) Preventive Measures (Best practices to avoid this issue).
```

### 1.2. Prompt-chaining or recursive prompting

- One of the most powerful best practices that can be utilized is to create a full workflow rather
  than a single prompt, where the output of one prompt becomes the input to another. You can
  chain multiple tasks together that build on the previous output, and even switch model types
  in between.
- An example:

```prompt
Do

I am a mobile developer, and you are a senior React Native architect. Let's have a
brainstorming session where you ask me one question at a time about the
following requirements, and come up with a specification. I have a mobile
application that currently uses two separate code bases and build processes for
iOS and Android. I want to migrate this app to React Native so that I can unify the
codebase and build process
```

- As an example, the first question the LLM asks might be:

```text
1. What are the main features and functionalities of your existing mobile app across both
iOS and Android?

(Think screens, workflows, integrations, and anything that might differ between
platforms.)
```

- After a series of questions, one at a time as specified, the LLM will let you know that it has reached its final question.
- Once you answer the final question, the LLM will build a blueprint specification. You can then use this specification with a reasoning model to create a step-by-step process, including prompt examples, which can be followed to create the app. Meta-prompting can ensure that the output follows a repeatable process.

### 1.3. One-shot or few-shot vs. zero-shot prompting

Similar to meta-prompting, providing examples of the kind of output you are looking for can
result in much more accurate and comprehensive results from the assistant. This can help the
model learn from existing examples and provide better structure in its output. A zero-shot
prompt simply asks the assistant to produce some output without scoped precedent, whereas
a one-shot (providing a single output example) or a few-shot (providing multiple examples)
can save multiple cycles of refining and improving answers.

```prompt
Don't

Write a Spring Boot REST API with a /hello endpoint
```

```prompt
Do

Here is an example of a structured REST API design:


@RestController

@RequestMapping("/users")

public class UserController {

    private final UserService userService;

    public UserController(UserService userService) {

        this.userService = userService;

    }

    @GetMapping("/{id}")

    public ResponseEntity<UserDTO> getUser(@PathVariable
Long id) {

        return
ResponseEntity.ok(userService.getUser(id));

    }

}

Now generate a HelloController that:
- Uses a HelloService layer@
- Returns a DTO instead of plain strings@
- Follows RESTful response conventions (ResponseEntity,
proper status codes).
```

### 1.4. System prompt updates for better accuracy

One of the most effective ways to use this system prompt is by creating a feedback loop between users of the assistant and the model owners who configure the assistant platform organizationally. When the model creates inaccurate or suboptimal output, in many cases that output can be corrected going forward by changing the system prompt.

### 1.5. Multi-model or adversarial engineering

Basic workflow:

- Define the task.
- Prompt both AI models.
- Adversarial cross-testing.
- Evaluate feedback.
- Declare a winner.

### 1.6. Multi-context: use images and voice prompting

There are more ways to engage with copilots than just typing in prompts. Participants
reported that voice-to-text prompting can speed up code assistant usage by 30% or more.
Using images such as flow charts and roadmap visualizations can reduce the amount of
prompting and typing considerably.

### 1.7. Understand determinism and non-determinism

Determinism can be controlled using temperature, a system parameter that adjusts the randomness of token selection.

A lower temperature (i.e., “0.1” as opposed to “0.9”) makes the model more deterministic by favoring high-probability tokens, leading to consistent and repeatable outputs. Conversely, a higher temperature (i.e., “0.9” or above) increases randomness, fostering creativity but reducing predictability.

## 2. Part 2 - Recommend use cases

### 2.1. Stack trace analysis

```prompt
Analyze this Java stack trace and suggest the root cause and potential fixes: [Insert stack trace and additional error detail if appropriate]
```

### 2.2. Refactoring existing code

```prompt
Refactor this Java function to improve readability and efficiency: [Insert longer explanation, context, and code]
```

### 2.3. Mid-loop code generation

```prompt
Complete this Java function: [Example Function and additional context, metaprompts, etc]
```

### 2.4. Test case generation

```prompt
Generate JUnit test cases for the following Java class: [Insert class]
```

### 2.5. Learning new techniques

```prompt
I have five years of experience writing Java and Spring. Show me how to create a Java 24 virtual thread in Spring
```

### 2.6. Complex query writing (SQL, Regex, CLI commands)

Sometimes developers will need to generate complex patterns or queries such as regular
expression patterns or SQL queries. Rather than context switch to a different coding or pattern
framework, AI coding assistants can generate code-native expressions for you.

### 2.7. Code documentation

Once you’ve finished writing some code, a code assistant can help you comment that code for
better understandability and readability. It can also generate actual documentation in markup
formats like AsciiDoc and LaTeX.

### 2.8. Brainstorming and planning

Using a generative AI tool to plan out your work can be very effective, especially when using a
recursive workflow as described in the workflows and prompting techniques section above.

### 2.9. Initial feature scaffolding

Using a generative AI tool to plan out your work can be very effective, especially when using a
recursive workflow as described in the workflows and prompting techniques section above

```prompt
Create the code outline for a Java application that will listen on a Kafka topic and
create a multicast pattern to a Postgres endpoint, a RESTFul POST endpoint, and
an SMTP endpoint.
```

### 2.10. Code explanation

Rather than pore over unfamiliar code or try to chase down the initial authors of the code, a
code assistant can provide valuable insights into the functionality of existing code. This can be
especially helpful when trying to interpret code in frameworks you may be less familiar with.
