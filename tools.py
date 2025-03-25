import requests
from bs4 import BeautifulSoup
import openai
import os
from dotenv import load_dotenv

load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")
openai.api_model = os.getenv("OPENAI_MODEL_NAME")


def web_search(query):
    """
    Searches the web for relevant information.
    """
    try:
        url = f"https://www.google.com/search?q={query}"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raise HTTPError for bad responses (4xx or 5xx)

        soup = BeautifulSoup(response.text, "html.parser")
        results = [result.get_text() for result in soup.find_all("div", class_="tF2Cxc")]  # Adjust class based on Google's structure
        return "\n".join(results[:5])  # Return top 5 results

    except requests.exceptions.RequestException as e:
        return f"Error during web search: {e}"
    except Exception as e:
        return f"An unexpected error occurred: {e}"

def generate_outline(topic, research_content):
    """
    Generates a blog outline based on the topic and research content.
    """
    prompt = f"""
    Given the topic: "{topic}" and the research content: "{research_content}", create a detailed blog outline.
    Include headings, subheadings, and key points. Aim for a structure that will help create a 2000-word blog post.
    """
    try:
        response = openai.chat.completions.create(
            model=openai.api_model,
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error generating outline: {e}"

def generate_content(topic, outline, research_content):
    """
    Generates blog content based on the outline and research.
    """
    prompt = f"""
    Write a 2000-word blog post about "{topic}" using the following outline: "{outline}".
    Use the research content: "{research_content}" to support your writing. 
    Ensure the content is informative and engaging.
    """
    try:
        response = openai.chat.completions.create(
            model=openai.api_model,
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error generating content: {e}"

def optimize_seo(content, keywords):
    """
    Optimizes the blog content for SEO.
    """
    prompt = f"""
    Optimize the following blog content for SEO using these keywords: "{keywords}".
    Content: "{content}"
    Focus on natural keyword integration, heading optimization, and formatting.
    """
    try:
        response = openai.chat.completions.create(
            model=openai.api_model,
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error optimizing SEO: {e}"

def review_content(content):
    """
    Reviews the blog content for grammar, clarity, and quality.
    """
    prompt = f"""
    Proofread and review the following blog content. 
    Suggest improvements for grammar, clarity, and overall quality.
    Content: "{content}"
    """
    try:
        response = openai.chat.completions.create(
            model=openai.api_model,
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error reviewing content: {e}"

# Tool Definitions
web_search_tool = lambda query: web_search(query)
outline_tool = lambda topic, research_content: generate_outline(topic, research_content)
content_generation_tool = lambda topic, outline, research_content: generate_content(topic, outline, research_content)
seo_optimization_tool = lambda content, keywords: optimize_seo(content, keywords)
review_tool = lambda content: review_content(content)
