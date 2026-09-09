"""
Script to import words from JSON/CSV into the database.

Usage:
    python -m scripts.import_words data/words_sample.json
"""

import json
import csv
import asyncio
import sys
from pathlib import Path
from typing import List, Dict

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from sqlalchemy import select
from app.database.base import async_session, init_db
from app.database.models.word import Word


async def import_from_json(filepath: str) -> Dict:
    """Import words from JSON file."""
    with open(filepath, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    if isinstance(data, dict) and 'words' in data:
        words_data = data['words']
    elif isinstance(data, list):
        words_data = data
    else:
        raise ValueError("Invalid JSON format. Expected list or {'words': [...]}")
    
    return await _import_words(words_data)


async def import_from_csv(filepath: str) -> Dict:
    """Import words from CSV file."""
    words_data = []
    
    with open(filepath, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            # Parse JSON fields
            for field in ['examples', 'common_phrases', 'collocations', 'synonyms', 'antonyms', 'forms', 'tags']:
                if field in row and row[field]:
                    try:
                        row[field] = json.loads(row[field])
                    except json.JSONDecodeError:
                        row[field] = []
                else:
                    row[field] = []
            
            words_data.append(row)
    
    return await _import_words(words_data)


async def _import_words(words_data: List[Dict]) -> Dict:
    """Import words into database."""
    stats = {
        'total': len(words_data),
        'imported': 0,
        'skipped': 0,
        'errors': 0,
    }
    
    async with async_session() as session:
        for word_data in words_data:
            try:
                # Check for duplicates
                existing = await session.execute(
                    select(Word).where(Word.word == word_data['word'].lower())
                )
                if existing.scalar_one_or_none():
                    stats['skipped'] += 1
                    continue
                
                # Create word
                word = Word(
                    word=word_data['word'].lower(),
                    translation=word_data['translation'],
                    part_of_speech=word_data.get('part_of_speech'),
                    frequency_rank=word_data.get('frequency_rank', 5000),
                    level=word_data.get('level', 'A1'),
                    importance=word_data.get('importance', 5.0),
                    pronunciation=word_data.get('pronunciation'),
                    examples=word_data.get('examples', []),
                    common_phrases=word_data.get('common_phrases', []),
                    collocations=word_data.get('collocations', []),
                    synonyms=word_data.get('synonyms', []),
                    antonyms=word_data.get('antonyms', []),
                    forms=word_data.get('forms', []),
                    tags=word_data.get('tags', []),
                    category=word_data.get('category'),
                    is_phrasal_verb=word_data.get('is_phrasal_verb', 0),
                    is_idiom=word_data.get('is_idiom', 0),
                    is_slang=word_data.get('is_slang', 0),
                    is_contraction=word_data.get('is_contraction', 0),
                )
                
                session.add(word)
                stats['imported'] += 1
                
                # Commit every 100 words
                if stats['imported'] % 100 == 0:
                    await session.commit()
                    print(f"  Imported {stats['imported']} words...")
            
            except Exception as e:
                print(f"  Error importing '{word_data.get('word', '?')}': {e}")
                stats['errors'] += 1
        
        # Final commit
        await session.commit()
    
    return stats


async def main():
    """Main entry point."""
    if len(sys.argv) < 2:
        print("Usage: python -m scripts.import_words <filepath>")
        print("Supported formats: .json, .csv")
        sys.exit(1)
    
    filepath = sys.argv[1]
    
    if not Path(filepath).exists():
        print(f"File not found: {filepath}")
        sys.exit(1)
    
    print(f"📚 Importing words from: {filepath}")
    print("Initializing database...")
    await init_db()
    
    print("Importing...")
    if filepath.endswith('.json'):
        stats = await import_from_json(filepath)
    elif filepath.endswith('.csv'):
        stats = await import_from_csv(filepath)
    else:
        print("Unsupported format. Use .json or .csv")
        sys.exit(1)
    
    print("\n✅ Import complete!")
    print(f"  Total: {stats['total']}")
    print(f"  Imported: {stats['imported']}")
    print(f"  Skipped (duplicates): {stats['skipped']}")
    print(f"  Errors: {stats['errors']}")


if __name__ == "__main__":
    asyncio.run(main())
