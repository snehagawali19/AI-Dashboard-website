"""
OpenAI GPT-4o-mini integration.
All AI features live here: summarize, caption, tag, embed.
"""
import logging
from openai import AsyncOpenAI
from app.models.models import NewsItem
from app.config import settings

logger = logging.getLogger(__name__)
client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)

SUMMARY_PROMPT = """Summarize this AI/tech news article in 2-3 sentences.
Be factual, clear, and omit marketing fluff.
Article title: {title}
Content: {content}
Return ONLY the summary text."""

LINKEDIN_PROMPT = """Write a LinkedIn post caption for this AI news article.
- 2-3 paragraphs, engaging and professional
- End with 3-5 relevant hashtags like #AI #MachineLearning
- No emojis in the first sentence
Article: {title}
Summary: {summary}"""

EMAIL_PROMPT = """Write a brief email teaser for this AI news article (3-4 sentences).
Suitable for a daily AI digest newsletter. Clear subject-line style opening.
Article: {title}
Summary: {summary}"""

TAG_PROMPT = """Extract 3-6 topic tags for this AI news article.
Return ONLY a JSON array of lowercase strings. Example: ["llm","openai","benchmark"]
Article: {title}
Content: {content[:500]}"""


async def summarize(title: str, content: str) -> str:
    """Generate a 2-3 sentence summary."""
    if not settings.AI_ENABLED or not content:
        return ""
    try:
        resp = await client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content":
                        SUMMARY_PROMPT.format(title=title, content=content[:3000])}],
            max_tokens=200, temperature=0.3,
        )
        return resp.choices[0].message.content.strip()
    except Exception as e:
        logger.error("Summarize error: %s", e)
        return ""


async def generate_captions(title: str, summary: str) -> tuple[str, str]:
    """Generate LinkedIn and email captions in parallel."""
    if not settings.AI_ENABLED:
        return "", ""
    import asyncio
    async def _linkedin():
        try:
            r = await client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content":
                           LINKEDIN_PROMPT.format(title=title, summary=summary)}],
                max_tokens=300, temperature=0.7,
            )
            return r.choices[0].message.content.strip()
        except Exception as e:
            logger.error("LinkedIn caption error: %s", e); return ""

    async def _email():
        try:
            r = await client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content":
                           EMAIL_PROMPT.format(title=title, summary=summary)}],
                max_tokens=150, temperature=0.4,
            )
            return r.choices[0].message.content.strip()
        except Exception as e:
            logger.error("Email caption error: %s", e); return ""

    return await asyncio.gather(_linkedin(), _email())


async def extract_tags(title: str, content: str) -> list[str]:
    """Extract topic tags as a list of strings."""
    if not settings.AI_ENABLED:
        return []
    import json
    try:
        resp = await client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content":
                       TAG_PROMPT.format(title=title, content=content)}],
            max_tokens=80, temperature=0.1,
        )
        raw = resp.choices[0].message.content.strip()
        return json.loads(raw)
    except Exception as e:
        logger.error("Tag extraction error: %s", e)
        return []


async def get_embedding(text: str) -> list[float]:
    """Get text-embedding-3-small vector for semantic dedup."""
    if not settings.AI_ENABLED:
        return []
    try:
        resp = await client.embeddings.create(
            model="text-embedding-3-small",
            input=text[:512],
        )
        return resp.data[0].embedding
    except Exception as e:
        logger.error("Embedding error: %s", e)
        return []


async def process_news_item(item) -> dict:
    """Run full AI pipeline for one news item. Returns update dict."""
    content = item.content or ""
    title = item.title or ""

    summary = await summarize(title, content)
    linkedin, email = await generate_captions(title, summary or title)
    tags = await extract_tags(title, content)
    embedding = await get_embedding(f"{title}. {summary}")

    return {
        "summary": summary,
        "linkedin_caption": linkedin,
        "email_caption": email,
        "tags": tags,
        "embedding": embedding,
        "ai_processed": True,
    }