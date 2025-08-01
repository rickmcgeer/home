import os
import json
from datasets import load_dataset
from transformers import AutoTokenizer, AutoModelForCausalLM, TrainingArguments
from peft import get_peft_model, LoraConfig, TaskType, prepare_model_for_kbit_training
from transformers import Trainer
import torch
import argparse

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--model_id", type=str, default="mistralai/Mistral-7B-Instruct")
    parser.add_argument("--dataset_path", type=str, default="llm/data/aiko_corpus.jsonl")
    parser.add_argument("--output_dir", type=str, default="llm/adapters/aiko-core")
    parser.add_argument("--use_qlora", action="store_true")
    args = parser.parse_args()

    tokenizer = AutoTokenizer.from_pretrained(args.model_id)
    tokenizer.pad_token = tokenizer.eos_token

    dataset = load_dataset("json", data_files=args.dataset_path, split="train")

    def tokenize(example):
        prompt = example["prompt"]
        response = example["response"]
        text = f"{prompt}\n{response}"
        return tokenizer(text, truncation=True, padding="max_length", max_length=512)

    tokenized = dataset.map(tokenize)

    quantization_config = None
    if args.use_qlora:
        from transformers import BitsAndBytesConfig
        quantization_config = BitsAndBytesConfig(load_in_4bit=True, bnb_4bit_use_double_quant=True,
                                                 bnb_4bit_quant_type="nf4", bnb_4bit_compute_dtype=torch.float16)

    model = AutoModelForCausalLM.from_pretrained(args.model_id,
                                                  device_map="auto",
                                                  quantization_config=quantization_config)

    if args.use_qlora:
        model = prepare_model_for_kbit_training(model)

    peft_config = LoraConfig(
        task_type=TaskType.CAUSAL_LM,
        inference_mode=False,
        r=16,
        lora_alpha=32,
        lora_dropout=0.1,
        bias="none"
    )

    model = get_peft_model(model, peft_config)

    training_args = TrainingArguments(
        output_dir=args.output_dir,
        per_device_train_batch_size=4,
        gradient_accumulation_steps=2,
        num_train_epochs=3,
        save_strategy="epoch",
        logging_dir=os.path.join(args.output_dir, "logs"),
        logging_steps=10,
        bf16=True,
        fp16=not args.use_qlora,
        report_to="none"
    )

    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=tokenized
    )

    trainer.train()
    model.save_pretrained(args.output_dir)
    tokenizer.save_pretrained(args.output_dir)

if __name__ == "__main__":
    main()