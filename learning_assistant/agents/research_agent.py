"""Research Agent - Fetches and summarises information from Wikipedia."""

import wikipedia
import google.generativeai as genai
from typing import Dict

from learning_assistant.config import config


class ResearchAgent:
    """
    Research Agent that fetches information from Wikipedia and creates
    structured educational summaries using Gemini.
    """
    
    def __init__(self, api_key: str = None):
        """
        Initialise the Research Agent.
        
        Args:
            api_key: Google Gemini API key (optional, uses config if not provided)
        """
        api_key = api_key or config.GEMINI_API_KEY
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel(config.MODEL_NAME)
    
    def fetch_topic_info(self, topic: str) -> Dict[str, str]:
        """
        Fetch and summarise information about a topic.
        
        This method:
        1. Fetches information from Wikipedia
        2. Uses Gemini to create a structured educational summary
        
        Args:
            topic: The topic to research
            
        Returns:
            Dictionary containing:
                - raw_info: Raw Wikipedia summary
                - structured_summary: Gemini-generated educational summary
        """
        try:
            # Tool 1: Wikipedia search
            wiki_summary = wikipedia.summary(topic, sentences=config.WIKIPEDIA_SENTENCES)
            
            # Tool 2: LLM-based structured summarisation
            prompt = f"""Summarise this information about {topic} in a clear, educational format:

{wiki_summary}

Provide:
1. Brief overview (2-3 sentences)
2. Key concepts (3-5 bullet points)
3. Why it's important

Make it engaging and suitable for learners."""
            
            response = self.model.generate_content(prompt)
            
            return {
                "raw_info": wiki_summary,
                "structured_summary": response.text
            }
            
        except wikipedia.exceptions.DisambiguationError as e:
            # Handle disambiguation - suggest more specific topics
            suggestions = ", ".join(e.options[:5])
            return {
                "raw_info": f"Multiple topics found for '{topic}'",
                "structured_summary": f"Topic: {topic}\n\nPlease be more specific. Did you mean one of these?\n{suggestions}"
            }
            
        except wikipedia.exceptions.PageError:
            return {
                "raw_info": f"Could not find Wikipedia page for '{topic}'",
                "structured_summary": f"Topic: {topic}\n\nNo Wikipedia page found. Please check the spelling or try a different topic."
            }
            
        except Exception as e:
            return {
                "raw_info": f"Could not fetch Wikipedia info: {str(e)}",
                "structured_summary": f"Topic: {topic}\n\nAn error occurred while fetching information. Please try again or choose a different topic."
            }
