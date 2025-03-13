import pytest
from app.services.summarizer import TextSummarizer
import asyncio
import warnings
from transformers import AutoTokenizer  


class TestTextSummarizer:
    @pytest.fixture
    def summarizer(self):
        return TextSummarizer()


    @pytest.mark.asyncio
    async def test_summarize_basic(self, summarizer):
        text = (
            "Python is a high-level, general-purpose programming language. "
            "Its design philosophy emphasizes code readability with the use of significant indentation. "
            "Python is dynamically typed and garbage-collected. "
            "It supports multiple programming paradigms, including structured, object-oriented, and functional programming. "
            "Python's comprehensive standard library is often referred to as 'batteries included'."
        )
        max_length = 130
        min_length = 30
        summary = await summarizer.summarize(text, max_length=max_length, min_length=min_length)

        tokenizer = AutoTokenizer.from_pretrained("sshleifer/distilbart-cnn-12-6")
        tokens = tokenizer.tokenize(summary)

        assert isinstance(summary, str)
        assert len(tokens) >= min_length
        assert len(tokens) <= max_length

    @pytest.mark.asyncio
    async def test_summarize_with_custom_length(self, summarizer):
        text = """
        Python is a high-level, general-purpose programming language. Python's design philosophy
        emphasizes code readability with the use of significant indentation. Python is dynamically
        typed and garbage-collected. It supports multiple programming paradigms, including structured,
        object-oriented and functional programming. Python is often used as a scripting language, but it is also used to build large-scale web applications.  It has a large and active community that provides a wealth of libraries and frameworks. Python is used in a wide variety of domains, including data science, machine learning, web development, and scientific computing. Because of its flexibility and ease of use, Python is a popular choice for both beginners and experienced programmers.
        """
        max_length = 70
        min_length = 30
        summary = await summarizer.summarize(text, max_length=max_length, min_length=min_length)
        words = summary.split()

        assert isinstance(summary, str)
        assert len(words) <= max_length
        assert len(words) >= min_length

    @pytest.mark.asyncio
    async def test_summarize_empty_text(self, summarizer):
        with pytest.raises(Exception):
            await summarizer.summarize("")

    @pytest.mark.asyncio
    async def test_summarize_very_short_text(self, summarizer):
        text = "This is a very short text."
        with pytest.raises(Exception):
            await summarizer.summarize(text)

    @pytest.mark.asyncio
    async def test_summarize_long_text(self, summarizer):
        long_text = """
        Python is a high-level, general-purpose programming language. Python's design philosophy 
        emphasizes code readability with the use of significant indentation. Python is dynamically 
        typed and garbage-collected. It supports multiple programming paradigms, including structured, 
        object-oriented and functional programming. It is often described as a "batteries included" 
        language due to its comprehensive standard library. Python was created by Guido van Rossum 
        and was first released in 1991. Python consistently ranks as one of the most popular 
        programming languages.
        """ * 5  
        max_length = 200
        summary = await summarizer.summarize(long_text, max_length=max_length)
        words = summary.split()
        
        assert isinstance(summary, str)
        assert len(words) <= max_length
        assert len(summary) > 0

    @pytest.mark.asyncio
    async def test_invalid_length_parameters(self, summarizer):
        text = "Some valid text for summarization that should be long enough."
        
        with pytest.raises(ValueError, match="min_length cannot be greater than max_length"):
            await summarizer.summarize(text, max_length=50, min_length=100)