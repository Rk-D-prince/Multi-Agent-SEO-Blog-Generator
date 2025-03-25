from crewai import Crew, Task, Process
from agents import research_agent, planning_agent, generation_agent, seo_agent, review_agent
from tools import web_search_tool, outline_tool, content_generation_tool, seo_optimization_tool, review_tool

def generate_seo_blog(topic, keywords):
    """
    Generates a detailed, SEO-optimized blog post using a multi-agent system, sequentially.

    Args:
        topic (str): The HR-related topic for the blog post.
        keywords (str): Comma-separated keywords for SEO optimization.

    Returns:
        str: The generated blog post in markdown format.
    """

    # Research Task
    research_task = Task(
        description=f"""
        Research trending HR topics and gather in-depth, authoritative information from the web. 
        Focus on scholarly articles, industry reports, and reputable news sources. 
        Provide a detailed summary of your findings, including key statistics, expert opinions, and relevant examples. 
        Include a list of sources for each key piece of information.
        The topic is: '{topic}'.
        """,
        expected_output="A detailed report on the topic, with relevant sources.",
        tools=[web_search_tool],
        agent=research_agent
    )

    # Content Planning Task
    planning_task = Task(
        description=f"""
        Based on the research provided, create a comprehensive and structured outline for a 2000-word SEO-optimized blog post. 
        Include an introduction, multiple main sections with subheadings, and a conclusion. 
        Ensure the outline facilitates a clear and engaging narrative with a logical flow.
        Include potential H2 and H3 headers.
        The topic is: '{topic}'.
        """,
        expected_output="A structured blog outline with headings and subheadings.",
        tools=[outline_tool],
        agent=planning_agent
    )

    # Content Generation Task
    generation_task = Task(
        description=f"""
        Write a detailed and engaging 2000-word blog post based on the provided outline and research. 
        Use clear and concise language, incorporate relevant examples and statistics, and maintain a consistent tone. 
        Structure the content with headings and subheadings for readability.
        Include internal and external links where appropriate.
        The topic is: '{topic}'.
        """,
        expected_output="A complete 2000-word blog post.",
        tools=[content_generation_tool],
        agent=generation_agent
    )

    # SEO Optimization Task
    seo_task = Task(
        description=f"""
        Optimize the blog post for SEO using the following keywords: '{keywords}'. 
        Focus on natural keyword integration, heading optimization, meta descriptions, and internal/external linking. 
        Ensure the content is well-structured and easy to read, with proper use of headings and subheadings.
        Provide a meta description and suggested title.
        """,
        expected_output="An SEO-optimized blog post with meta description and title.",
        tools=[seo_optimization_tool],
        agent=seo_agent
    )

    # Review Task
    review_task = Task(
        description="""
        Proofread the blog post and suggest improvements for grammar, clarity, and overall quality. 
        Pay attention to sentence structure, flow, and consistency. 
        Provide specific feedback and actionable suggestions.
        Also check for plagiarism and factual accuracy.
        """,
        expected_output="A reviewed and improved blog post with feedback.",
        tools=[review_tool],
        agent=review_agent
    )

    # Create crew with sequential process
    crew = Crew(
        agents=[research_agent, planning_agent, generation_agent, seo_agent, review_agent],
        tasks=[research_task, planning_task, generation_task, seo_task, review_task],
        verbose=True,
        process=Process.sequential  # Set process to sequential
    )

    # Run crew
    result = crew.kickoff()
    return result

# Example Usage
topic = "The Impact of AI on Talent Acquisition"
keywords = "AI, talent acquisition, recruitment, HR, technology"
blog_post = generate_seo_blog(topic, keywords)

# Save the blog post to a file (e.g., Markdown)
with open("hr_talent_ai_blog_post.md", "w", encoding="utf-8") as f:
    f.write(blog_post)

print("SEO-optimized blog post generated and saved to hr_talent_ai_blog_post.md")
