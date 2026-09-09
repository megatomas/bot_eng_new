"""
Генерация словаря с помощью AI (Groq/Gemini).

Использование:
    python -m scripts.generate_dictionary --level A1 --count 100 --output data/words_a1.json
"""

import asyncio
import json
import argparse
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.ai.providers import get_llm_provider


async def generate_words_batch(
    level: str,
    count: int,
    category: str | None = None,
) -> list[dict]:
    """Generate a batch of words using AI."""
    
    category_hint = f"Category: {category}. " if category else ""
    
    prompt = f"""
Generate {count} English words/phrases for level {level}.
{category_hint}

Requirements:
- Focus on most useful CONVERSATIONAL words
- Include phrasal verbs, idioms, contractions where appropriate
- For each word provide:

Return JSON array with this structure:
[
  {{
    "word": "run",
    "translation": "бежать; работать; управлять",
    "part_of_speech": "verb",
    "frequency_rank": 150,
    "level": "{level}",
    "pronunciation": "/rʌn/",
    "examples": [
      {{"en": "I run every morning.", "ru": "Я бегаю каждое утро."}},
      {{"en": "She runs a business.", "ru": "Она управляет бизнесом."}}
    ],
    "common_phrases": ["run out of", "run late"],
    "collocations": ["run a business", "run fast"],
    "synonyms": ["sprint", "jog"],
    "forms": ["run", "ran", "running"],
    "tags": ["daily", "movement"],
    "category": "movement",
    "importance": 9.4
  }}
]

IMPORTANT:
- Return ONLY valid JSON, no other text
- Include Russian translations
- Make examples natural and conversational
- frequency_rank: 1-10000 (1 = most frequent)
- importance: 1-10 (10 = most important)
"""
    
    llm = get_llm_provider()
    response = await llm.chat(
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7,
        max_tokens=4000,
    )
    
    # Extract JSON from response
    try:
        # Try to find JSON in response
        if "{" in response or "[" in response:
            # Find JSON array
            start = response.find("[")
            end = response.rfind("]") + 1
            if start != -1 and end > start:
                json_str = response[start:end]
                words = json.loads(json_str)
                return words
    except json.JSONDecodeError as e:
        print(f"Error parsing JSON: {e}")
        print(f"Response: {response[:500]}")
    
    return []


async def generate_dictionary(
    level: str,
    total_count: int,
    output_file: str,
    batch_size: int = 20,
):
    """Generate full dictionary in batches."""
    
    print(f"🎯 Generating {total_count} words for level {level}")
    print(f"📦 Batch size: {batch_size}")
    print(f"💾 Output: {output_file}\n")
    
    all_words = []
    batches = (total_count + batch_size - 1) // batch_size
    
    for i in range(batches):
        current_count = min(batch_size, total_count - len(all_words))
        
        print(f"📝 Batch {i + 1}/{batches}: generating {current_count} words...")
        
        try:
            words = await generate_words_batch(level, current_count)
            all_words.extend(words)
            print(f"✅ Got {len(words)} words (total: {len(all_words)})")
            
            # Small delay to avoid rate limiting
            await asyncio.sleep(2)
            
        except Exception as e:
            print(f"❌ Error in batch {i + 1}: {e}")
            continue
    
    # Save to file
    output_path = Path(output_file)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump({"words": all_words}, f, ensure_ascii=False, indent=2)
    
    print(f"\n✅ Done! Generated {len(all_words)} words")
    print(f"💾 Saved to: {output_path}")
    
    # Stats
    categories = {}
    for word in all_words:
        cat = word.get("category", "unknown")
        categories[cat] = categories.get(cat, 0) + 1
    
    print(f"\n📊 Categories:")
    for cat, count in sorted(categories.items(), key=lambda x: -x[1]):
        print(f"  • {cat}: {count}")


async def main():
    parser = argparse.ArgumentParser(description="Generate dictionary with AI")
    parser.add_argument("--level", default="A1", help="CEFR level (A0, A1, A2, B1, B2, C1)")
    parser.add_argument("--count", type=int, default=100, help="Number of words to generate")
    parser.add_argument("--output", default="data/generated_words.json", help="Output file path")
    parser.add_argument("--batch-size", type=int, default=20, help="Words per batch")
    
    args = parser.parse_args()
    
    await generate_dictionary(
        level=args.level,
        total_count=args.count,
        output_file=args.output,
        batch_size=args.batch_size,
    )


if __name__ == "__main__":
    asyncio.run(main())
