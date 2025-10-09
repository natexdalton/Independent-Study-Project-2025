from datasets import load_dataset

ds = load_dataset("akhan02/cultural-dimension-cover-letters")
df = ds["train"].to_pandas()[["Cover_Letter"]].dropna()

# Simple “prompt + answer” structure for supervised fine-tuning
df["input_text"]  = "Job description: [PLACEHOLDER]\nCover letter:"
df["target_text"] = df["Cover_Letter"]

print(df.head())

