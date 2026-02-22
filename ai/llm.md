# Large Language Models

## 1. Introduction

Source:

- <https://www.cloudskillsboost.google/course_templates/539/video/518194>
- <https://developers.google.com/machine-learning/resources/intro-llms>

### 1.1. What is language model?

- A language model is a machine learning model that aims to predict and generate plausible language. Autocomplete is a language model, for example.
- These models work by estimating the probability of a **token** or sequence of tokens occurring within a longer sequence of tokens.
  - Token: the atomic unit that themodel is training on and making predictions on. A token is typically one of the following:
    - A word - for example, the phrase "dogs like cats" consists of three word tokens: "dogs", "like", and "cats".
    - A character - for example, the phrase "bike fish" consists of nine character tokens.
    - Subwords - in which a single world can be a single token or multiple tokens. A subword consists of a root word, a prefix, or a suffix. For example, a language model that uses subwords as tokens might view the word "dogs" as two tokens (the root world "dog" and the plural suffix "s"). That same language model might view the single word "taller" as two subwords (the root word "tall" and the suffix "er").

```text
When I hear rain on my roof, I _______ in my kitchen.

# Assume that a token is a word, then a language model determines the probabilities of different words of sequences of words to replace that underscore.

cook soup 9.4%
warm up a kettle 5.2%
cower 3.6%
nap 2.5%
relax 2.2%
...
```

- Estimating the probability of what comes next in a sequence is useful for all kinds of things: generating text, translating languages, and answering questions, to name a few.

### 1.2. What is a large language model?

- Large Language Models refer to _large_, _general-purpose_ language models that can be _pre-trained_ and then _fine-tuned_ for specific purposes.
  - Large: So _how large is large_? "Large" can refer either to the number of parameters in the model, or sometimes the number of words in the dataset. It has been used to describe BERT (110M parameters) as well as PaLM 2 (up to 340B parameters). **Parameters**: the weights and biases that a model learns during training.
    - Large training dataset.
    - Large number of parameters.
  - General purpose:
    - Commonality of human languages.
    - Resource restriction.
  - Pre-trained and fine-tuned:

- **Transformers**:
  - Transformers are the state-of-the-art architecture for a wide variety of language model applications, such as translators.
  - It is designed around the idea of **attention**.
    - A mechanism used in a neural network that indicates the importance of a particular word or part of a word.
    - Attention compresses the amount of information a model needs to predict the next token/word.
  - Full Transformers consist of an encoder and a decoder.
    - An encoder converts input text into an intermediate representation.
    - A decoder converts that intermediate representation into useful text.
- Transformers rely heavily on a concept called **self-attention**. The self part of self-attention refers to the "egocentric" focus of each token in a corpus. Effectively, on behalf of each token of input, self-attention asks, "How much does every other token of input matter to **me**?"

## 2. Understanding LLMs

Source:

- <https://towardsdatascience.com/understanding-llms-from-scratch-using-middle-school-math-e602d27ec876>

## 3. Prompt engineering

- Prompt engineering is the art of asking the right question to get the best output from an LLM. It enables direct interaction with the LLM using only plain language prompts.
- Prompting Best Practices
  - Clearly communicate what content or information is most important.
  - Structure the prompt: Start by defining its role, give context/input data, then provide the instruction.
  - Use specific, varied examples to help the model narrow its focus and generate more accurate results.
  - Use constraints to limit the scope of the model's output. This can help avoid meandering away from the instructions into factual inaccuracies.
  - Break down complex tasks into a sequence of simpler prompts.
  - Instruct the model to evaluate or check its own responses before producing them. ("Make sure to limit your response to 3 sentences", "Rate your work on a scale of 1-10 for conciseness", "Do you think this is correct?").
- <...>
