from transformers import pipeline
import logging

class TextSummarizer:
    def __init__(self):
        self.model_name = "sshleifer/distilbart-cnn-12-6"
        self.summarizer = pipeline(
            "summarization",
            model=self.model_name,
            device=-1  
        )
        
    async def summarize(self, text: str, max_length: int = 130, min_length: int = 30) -> str:
        if not text.strip():
            raise ValueError("Input text cannot be empty")

        input_length = len(text.split())

        if min_length > max_length:
            raise ValueError("min_length cannot be greater than max_length")

        if input_length <= 10:
            raise ValueError("Input text is too short to summarize effectively")

        adjusted_max_length = min(max_length, input_length - 10)
        adjusted_max_length = max(adjusted_max_length, 1)

        adjusted_min_length = min(min_length, adjusted_max_length // 2)
        adjusted_min_length = max(adjusted_min_length, 1)  

        try:
            summary = self.summarizer(
                text,
                max_length=adjusted_max_length,
                min_length=adjusted_min_length,
                truncation=True,
                do_sample=False
            )
            summary_text = summary[0]['summary_text']

            summary_words = summary_text.split()
            if len(summary_words) > max_length:
                summary_text = " ".join(summary_words[:max_length])

            return summary_text
        except Exception as e:
            logging.error(f"Summarization error: {str(e)}")
            raise Exception(f"Failed to summarize text: {str(e)}")
