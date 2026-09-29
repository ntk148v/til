# Jev

## 1. System One

System One models make fast, structured decisions for software. Jev is TypeSafe’s flagship model and the first System One model.

Like an LLM, a System One model understands natural-language input. It returns typed decisions and probabilities rather than generated text. System One models do not write replies, produce code, or generate explanations of their reasoning. You define the possible answers through [primitives](https://docs.typesafe.ai/primitives):

| Primitive                                            | Question                              | Example answer space                          | Example output      |
| ---------------------------------------------------- | ------------------------------------- | --------------------------------------------- | ------------------- |
| [Choice](https://docs.typesafe.ai/primitives/choice) | Which team should handle this ticket? | `billing`, `technical`, or `account`          | `choice: "billing"` |
| [Score](https://docs.typesafe.ai/primitives/score)   | How frustrated is this customer?      | 0 = calm, 1 = frustrated, 2 = very frustrated | `score: 1.4`        |
| [Noul](https://docs.typesafe.ai/primitives/noul)     | Does this message request a refund?   | True or false                                 | `noul: 0.95`        |

**How System One models work**

Most AI products are built around a conversation between a model and a person. TypeSafe starts from a different bet: large-scale automation will be dominated by AI-to-AI and AI-to-software interactions, so the machine interface matters more than the chat interface.

Pretrained language models have been adapted in two major ways. TypeSafe adds a third. RLHF and RLVR are shown here for context; TypeSafe’s training path is RLCD.

- **RLHF - Reinforcement learning from human feedback** turned pretrained models into chatbots. It trains models to produce responses people prefer.
- **RLVR - Reinforcement learning with verifiable rewards** created reasoning models that are strong at tasks such as mathematics, but slower and more expensive.
- **RLCD - Reinforcement learning for calibrated decisions** trains TypeSafe to return decisions and calibrated probabilities instead of generated text.

![](https://mintcdn.com/ts-docs/aFVnpmCIX68NpsV1/images/ai-primer/training-paths-dark.webp?w=1650&fit=max&auto=format&n=aFVnpmCIX68NpsV1&q=85&s=aa7b5afa27451a07b0601ba6c4a0f4c9)

## 2. Jev

Jev is TypeSafe’s flagship model and the first [System One model](https://docs.typesafe.ai/concepts/system-one). System One models are built to make fast, structured decisions that software can use directly. Jev evaluates typed _questions_ against a _state_ and returns structured results directly. No text generation, no parsing. You get typed values and probability distributions that your code can branch on, sort by, and route with. Choice and Score also return [confidence](https://docs.typesafe.ai/confidence), which your code can use to decide whether and how to act on an answer.

## 3. Use cases

- <https://thecode-jev-use-cases.netlify.app>
- <https://github.com/walidboulanouar/awesome-jev-use-cases>

![](https://substackcdn.com/image/fetch/$s_!HL1C!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F9845db07-115f-4cd6-aaaa-76b90bc9ec7d_1280x1546.jpeg)
