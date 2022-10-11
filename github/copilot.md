# Github Copilot - AI Assistant

Source:

- <https://nira.com/github-copilot/>
- <https://www.fast.ai/posts/2021-07-19-copilot.html>
- <https://theankurtyagi.com/github-copilot-vs-tabnine-choose-the-best-ai-assistant-for-you/>
- <https://www.sitepoint.com/github-copilot-ai-pair-programming>

- [Github Copilot - AI Assistant](#github-copilot---ai-assistant)
  - [1. Introduction](#1-introduction)
  - [2. The good](#2-the-good)
  - [3. The bad](#3-the-bad)
    - [3.1. Code completition may be slow](#31-code-completition-may-be-slow)
    - [3.2. Good code bad code](#32-good-code-bad-code)
    - [3.3. Licensing](#33-licensing)
    - [3.5. Security and Privacy](#35-security-and-privacy)
    - [3.4. Does Copilot actually help me work faster?](#34-does-copilot-actually-help-me-work-faster)
  - [4. Compare with Tabnine](#4-compare-with-tabnine)

## 1. Introduction

- Copilot is described as "Your AI pair programmer".
- The result of collboration between Github and OpenAI, which is heavily backed by Microsoft. It's powered by a brand new AI system named Codex, which is based on the GPT3-model (Generative Pre-trained Transformer).
- According to Github: "OpenAI Codex was trained on publicly available source code and natural language, so it understands both programming and human language. The Github Copilot editor extension sends your comment and code to the Github Copilot service, which then uses OpenAI Codex to synthesize and suggest individual lines and whole functions." In addition, the service uses user choices to improve future suggestions.

![](https://nira.com/wp-content/uploads/2021/11/image4-1-620x308.png)

## 2. The good

- Copilot auto-generates code for you based on the contents of the current file, and your current cursor location.
- It really feels quite magical to use. For example, you type the name and docstring of a function which should "write text to file name", Copilot will write the rest of code.

![](https://media.makeameme.org/created/its-magic-5c9ab8.jpg)

- There are many many sites could show how magical Copilot is (or you can check [Copilot page](https://github.com/features/copilot)), so I don't dive into it.
- What Copilot can do:
  - Convert comments to code.
  - Autofill repetitive code.
  - Run tests (actually this is still convert comments to code).
  - Naviagting unfamiliar territory.

## 3. The bad

> Before we start, I have to notice that the above lines are simply my thought.

Copilot is an extremely fun-to-use tool. At first glance, it's really enjoyable to code with it.

### 3.1. Code completition may be slow

- Copilot predictions are exclusively Cloud-based, so it may turn slow sometimes.

### 3.2. Good code bad code

- The code Copilot writes is not always very good code.
- [Why Copilot writes bad code?](https://www.fast.ai/posts/2021-07-19-copilot.html#why-copilot-writes-bad-code) - The reason is because of how language models work. They show how, on average, most people write. They don't have any sense of what's correct or what's good. Most code on Github is (by software standard) pretty old, and (by definition) written by average programmers or worse (like me :face_exhaling:). Copilot spits out it’s best guess as to what those programmers might write if they were writing the same file that you are.
- One more thing is Copilot doesn't test any of code it's suggesting to you. Those suggestions may not actually compile or run.
- It might suggest code snippets using old libraries or modules.
- In other hand, Copilot may suggest code you may not understand.
- *Don't forget to review each large bunch of code Copilot offers up!*.

### 3.3. Licensing

- It's known that Copilot is trained on public Github repositories.
- As you may know, most open-source licenses (GNU, BSD, Apache, etc) allow you to use, modify and distribute software, with the only condition of using the same license. However, Copilot is meant to be a commercial product.

### 3.5. Security and Privacy

- You may notice that code must be sent off-premise to use Copilot.
  - Copilot relies on file content and additional data to work. It collects data both to provide the service and saves soe of the data to perform further analysis and enable improvements.
- Although [Github assures that your private code not be shared with other users](https://github.com/features/copilot/#faq-privacy), it still somehow uncomfortable.

### 3.4. Does Copilot actually help me work faster?

- Most time coding is not take up in *writing code*, but with *designing, debugging, and maintaining code*.
- Copilot gives you some lines of code, it's a `wow` at the first glance, but after that, you nearly always to have to verify and modify these.
- As a rule of thumb, less code means less to maintain and understand. Copilot's code is verbose, and it's so easy to generate lots of it that you're likely to end up with a lot of code!

## 4. Compare with Tabnine

- Tabnine is an AI coding assistant that helps you become a better coder.
- Tabnine never stores or share your code.
- Tabnine works with over 30 languages and can be installed in 15 IDEs.
- Tabnine predictions are both locally, hybrid, and cloud-based. Tabnine provides a private model trained on your code while Github Copilot doesn't.
- It's free plan available.
- Models trained only on permissive licenses.
- [Check more](https://www.tabnine.com/tabnine-vs-github-copilot-x).
