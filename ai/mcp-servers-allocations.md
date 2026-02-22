# too many model context protocol servers and LLM allocations on the dance floor

Source: <https://ghuntley.com/allocations/>

This blog post intends to be a definitive guide to context engineering fundamentals from the perspective of an engineer who builds commercial coding assistants and harnesses for a living.

## 1. Model Context Protocol

### 1.1. What is a tool?

A tool is an external piece of software that an agent can invoke to provide context to an LLM. Typically, they are packaged as binaries and distributed via NPM, or they can be written in any programming language; alternatively, they may be a remote MCP provided by a server.

```python
    @mcp.tool()
    async def list_files(directory_path: str, ctx: Context[ServerSession, None]) -> List[Dict[str, Any]]:
        ###
        ### tool prompt starts here
        """
        List all files and directories in a given directory path.

        This tool helps explore filesystem structure by returning a list of items
        with their names and types (file or directory). Useful for understanding
        project structure, finding specific files, or navigating unfamiliar codebases.

        Args:
            directory_path: The absolute or relative path to the directory to list

        Returns:
            List of dictionaries with 'name' and 'type' keys for each filesystem item
        """
        ###
        ### tool prompt ends here
        ...
```

For the remainder of this blog post, we'll focus on tool descriptions rather than the application logic itself, as each tool description is allocated into the context window to advertise capabilities that the LLM can invoke.

### 1.2. What is a token?

Language models process text using tokens, which are common sequences of characters found in a set of text. Below you will find a tokenisation of the tool description above.

![](https://ghuntley.com/content/images/size/w1000/2025/08/image-3.png)

### 1.3. What is a context window?

An LLM context window is the maximum amount of text (measured in tokens, which are roughly equivalent to words or parts of words) that a large language model can process at one time when generating or understanding text.

### 1.4. What is a harness?

A harness is anything that wraps the LLM to get outcomes. For software development, this may include tools such as Roo/Cline, Cursor, Amp, Opencode, Codex, Windsurf, or any of these coding tools available.

### 1.5. What is the real context window size?

The numbers advertised by LLM vendors for the context window are not the real context window. You should consider that to be a marketing number.

It's because there are two cold, hard facts:

- The LLM itself needs to allocate to the context window through its system prompt to function.
- The coding harness also needs to allocate resources in addition to those to function correctly.

LLMs work by needle in the haystack. The more you allocate, the worse your outcomes will be. Less is more, folks! You don't need the "full context window" (whatever that means); you really only want to use 100k of it.

## 2. How amny tools does an MCP server expose?

It's not just the amount of tokens allocated, but also a question of the number of tools - the more tools that are allocated into a context window, the greater the chances of driving inconsistent behaviour in the coding harness.

![](https://ghuntley.com/content/images/2025/08/image-7.png)

## 3. What is in the billboard or tool prompt description?

Different LLMs have different styles and recommendations on how a tool or a tool prompt should be designed.

![](https://ghuntley.com/content/images/size/w1000/2025/08/image-9.png)

## 4. What about security?

There is no name-spacing in the context window. If it's in the context window, it is up for consideration and execution. There is no significant difference between the coding harness prompt, the model system prompt, and the tooling prompts. It's all the same.
