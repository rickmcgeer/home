# Open vs Commercial Models: Fine-Tuning and Persona Embodiment

## ❌ Commercial Models (Closed APIs)

| Provider     | Model             | Fine-Tuning Support | Notes                                                                               |
| ------------ | ----------------- | ------------------- | ----------------------------------------------------------------------------------- |
| OpenAI       | GPT-4             | ❌ No                | GPT-4 is inference-only. GPT-3.5-turbo supports fine-tuning, but with restrictions. |
| Anthropic    | Claude 3          | ❌ No                | No fine-tuning API available. Contextual memory only.                               |
| Google       | Gemini 1.5        | ❌ No                | Closed model; fine-tuning unavailable.                                              |
| Cohere, AI21 | Command, Jurassic | ❌ No                | Focused on inference and embeddings.                                                |

## ✅ Open Models (Self-Hosted or HuggingFace)

| Model               | Fine-Tuning Support | Notes                                                      |
| ------------------- | ------------------- | ---------------------------------------------------------- |
| LLaMA 2 / LLaMA 3   | ✅ Yes               | Best results on 7B–13B variants. 8B from LLaMA 3 is ideal. |
| Mistral / Mixtral   | ✅ Yes               | LoRA and QLoRA compatible, great quality.                  |
| Yi 6B / 34B         | ✅ Yes               | High-performing open alternative.                          |
| Zephyr / OpenHermes | ✅ Yes               | Community favorites, easy to tune.                         |
| Qwen / Deepseek     | ✅ Yes               | Good multilingual and instruction-following support.       |

## Summary

For **true persona development and memory embodiment** like Aiko, we must:

* Use **open models**
* Fine-tune via **PEFT/LoRA/QLoRA**
* Run on **infrastructure we control**

Commercial APIs are great for general-purpose inference but unsuitable for **long-term memory, fine-grained identity tuning, or emotional persistence**.
