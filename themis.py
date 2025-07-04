import os
import json
import time
from datetime import datetime

class Themis:
    def __init__(self):
        self.input_dir = "themis_input"
        self.output_dir = "themis_output"
        self.processed_dir = os.path.join(self.input_dir, "processed")
        os.makedirs(self.output_dir, exist_ok=True)
        os.makedirs(self.processed_dir, exist_ok=True)
        self.max_batch = 25

    def frame_prompt(self, chunk_data):
        chunk = chunk_data.get("chunk", "")
        metadata = chunk_data.get("metadata", {})

        categories = ", ".join(metadata.get("categories", []))
        priority = metadata.get("priority", "medium")
        content_type = metadata.get("content", "blog")

        prompt = (
            f"Write a article that is conversational and engaging, focusing on the following keywords:\n\n"
            f"{chunk}\n\n"
            f"The content should be between 900 and 2000 words, targeting the categories: {categories}.\n"
            f"Prioritize the content with '{priority}' importance.\n"
            f"Make it informative, easy to read, and compelling for the target audience."
        )

        return {
            "framed_prompt": prompt,
            "metadata": metadata,
            "keywords": chunk
        }

    def process_chunks(self):
        files = sorted([
            f for f in os.listdir(self.input_dir)
            if f.endswith(".json") and f != "index.json"
        ])

        batch = files[:self.max_batch]
        processed_count = 0

        for filename in batch:
            filepath = os.path.join(self.input_dir, filename)
            try:
                with open(filepath, "r", encoding="utf-8") as f:
                    data = json.load(f)

                if not isinstance(data, dict):
                    print(f"Skipping non-dict JSON file: {filename}")
                    continue

                framed = self.frame_prompt(data)

                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
                out_filename = f"framed_prompt_{timestamp}.json"
                out_path = os.path.join(self.output_dir, out_filename)

                with open(out_path, "w", encoding="utf-8") as f:
                    json.dump(framed, f, indent=2)

                # Move processed file to archive folder
                os.rename(filepath, os.path.join(self.processed_dir, filename))
                processed_count += 1

            except Exception as e:
                print(f"[Themis] Error processing {filename}: {e}")

        print(f"Themis: Processed {processed_count} chunks, saved framed prompts to '{self.output_dir}'.")

if __name__ == "__main__":
    themis = Themis()
    themis.process_chunks()

