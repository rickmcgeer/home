# ghostwheel/orchestrator.py

from llm.selector import select_llm_variant
from vault.context_loader import get_context_for_prompt
from aikollm import AikoLLMRegistry

class AikoOrchestrator:
    def __init__(self, vault, selector, llm_registry):
        self.vault = vault
        self.selector = selector
        self.llm_registry = llm_registry

    def handle_prompt(self, user_prompt: str) -> str:
        # Step 1: Analyze & classify task (TBD — external or inline)
        # Step 2: Retrieve context
        context = get_context_for_prompt(user_prompt, self.vault)

        # Step 3: Select LLM
        variant = self.selector.select_variant(user_prompt)
        llm = self.llm_registry.get(variant)

        # Step 4: Invoke
        full_prompt = context + "\n\n" + user_prompt
        result = llm.call(full_prompt)

        # Step 5: Postprocess
        self.vault.gestalt_engine.observe_interaction(user_prompt, result)
        return result
