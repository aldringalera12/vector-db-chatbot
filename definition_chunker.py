#!/usr/bin/env python3
"""
Definition Chunker Script

This script chunks text per definition and stores it in a vector database.
Usage: python definition_chunker.py
"""

import argparse
import re
import sys
from typing import List, Dict, Tuple
import chromadb
from chromadb.config import Settings
import uuid
from sentence_transformers import SentenceTransformer
import os


class DefinitionChunker:
    def __init__(self, db_path: str = "./vector_db", collection_name: str = "definitions"):
        """Initialize the definition chunker with vector database."""
        self.db_path = db_path
        self.collection_name = collection_name
        
        # Initialize ChromaDB
        self.client = chromadb.PersistentClient(path=db_path)
        
        # Get or create collection
        try:
            self.collection = self.client.get_collection(name=collection_name)
            print(f"Using existing collection: {collection_name}")
        except:
            self.collection = self.client.create_collection(name=collection_name)
            print(f"Created new collection: {collection_name}")
    
    def chunk_by_end_markers(self, text: str) -> List[Dict[str, str]]:
        """
        Chunk text by 'end' markers. Each chunk is separated by a line containing only 'end'.
        Extracts the term from the first line and treats the rest as definition.
        """
        chunks = []

        # Split by 'end' markers (case insensitive, allowing whitespace)
        sections = re.split(r'\n\s*end\s*\n', text.strip(), flags=re.IGNORECASE)

        for section in sections:
            section = section.strip()
            if not section:
                continue

            # Remove any trailing 'end' text that might have been left
            section = re.sub(r'\s*end\s*$', '', section, flags=re.IGNORECASE).strip()
            if not section:
                continue

            # Split into lines
            lines = section.split('\n')
            if not lines:
                continue

            # First line should contain the term
            first_line = lines[0].strip()
            if not first_line:
                continue

            # Extract term from first line - look for patterns like "TERM -" or just "TERM"
            term_match = re.match(r'^([^-]+?)(?:\s*-\s*(.*))?$', first_line)
            if term_match:
                term = term_match.group(1).strip()
                first_line_def = term_match.group(2) if term_match.group(2) else ""

                # Collect definition from first line (if any) and remaining lines
                definition_parts = []
                if first_line_def:
                    definition_parts.append(first_line_def.strip())

                # Add remaining lines as definition, but skip any line that's just "end"
                for line in lines[1:]:
                    line = line.strip()
                    if line and line.lower() != 'end':
                        definition_parts.append(line)

                definition = ' '.join(definition_parts)

                if term and definition:
                    chunks.append({
                        'term': term,
                        'definition': definition,
                        'full_text': section
                    })

        return chunks

    def chunk_by_definitions(self, text: str) -> List[Dict[str, str]]:
        """
        Chunk text by definitions. Looks for patterns like:
        - Term: Definition
        - **Term**: Definition
        - Term - Definition
        - 1. Term: Definition
        - Text separated by 'end' markers
        """
        chunks = []

        # First try the new 'end' marker format
        if 'end' in text.lower():
            end_chunks = self.chunk_by_end_markers(text)
            if end_chunks:
                return end_chunks

        # Clean up the text - remove extra whitespace and normalize line breaks
        text = re.sub(r'\n\s*\n', '\n\n', text.strip())

        # Split by double newlines to get potential definition blocks
        blocks = text.split('\n\n')

        for block in blocks:
            block = block.strip()
            if not block:
                continue

            # Look for dash-separated definitions (TERM - Definition)
            # Handle cases where definition might be on the same line or next line
            if ' - ' in block:
                # Split on the first dash that has spaces around it
                parts = block.split(' - ', 1)
                if len(parts) == 2:
                    term = parts[0].strip()
                    definition = parts[1].strip()

                    # Clean up multi-line definitions
                    definition = ' '.join(definition.split())

                    if term and definition:
                        chunks.append({
                            'term': term,
                            'definition': definition,
                            'full_text': f"{term} - {definition}"
                        })
                        continue

            # Look for definitions where term ends with dash and definition is on next lines
            # Pattern: "TERM -\nDefinition content..."
            dash_end_match = re.match(r'^([^-\n]+)\s*-\s*\n(.+)', block, re.DOTALL)
            if dash_end_match:
                term = dash_end_match.group(1).strip()
                definition = dash_end_match.group(2).strip()

                # Clean up multi-line definitions
                definition = ' '.join(definition.split())

                if term and definition:
                    chunks.append({
                        'term': term,
                        'definition': definition,
                        'full_text': f"{term} - {definition}"
                    })
                    continue

            # Look for colon-separated definitions (TERM: Definition)
            if ':' in block:
                # Split on the first colon
                parts = block.split(':', 1)
                if len(parts) == 2:
                    term = parts[0].strip()
                    definition = parts[1].strip()

                    # Clean up multi-line definitions
                    definition = ' '.join(definition.split())

                    if term and definition:
                        chunks.append({
                            'term': term,
                            'definition': definition,
                            'full_text': f"{term}: {definition}"
                        })
                        continue

            # Look for bold markdown definitions (**TERM**: Definition)
            bold_match = re.match(r'^\*\*([^*]+)\*\*:\s*(.+)', block, re.DOTALL)
            if bold_match:
                term = bold_match.group(1).strip()
                definition = bold_match.group(2).strip()

                # Clean up multi-line definitions
                definition = ' '.join(definition.split())

                if term and definition:
                    chunks.append({
                        'term': term,
                        'definition': definition,
                        'full_text': f"**{term}**: {definition}"
                    })
                    continue

            # Look for numbered definitions (1. TERM: Definition)
            numbered_match = re.match(r'^(\d+\.\s*)([^:]+):\s*(.+)', block, re.DOTALL)
            if numbered_match:
                term = numbered_match.group(2).strip()
                definition = numbered_match.group(3).strip()

                # Clean up multi-line definitions
                definition = ' '.join(definition.split())

                if term and definition:
                    chunks.append({
                        'term': term,
                        'definition': definition,
                        'full_text': f"{term}: {definition}"
                    })
                    continue

        return chunks

    def chunk_by_sections(self, text: str) -> List[Dict[str, str]]:
        """
        Chunk text by sections, preserving hierarchical structure.
        Looks for main headings and groups related content under them.
        """
        chunks = []
        lines = text.strip().split('\n')
        current_section = None
        current_items = []
        current_item = ""

        for line in lines:
            original_line = line
            line = line.strip()

            # Skip empty lines but use them to separate items
            if not line:
                if current_item:
                    current_items.append(current_item.strip())
                    current_item = ""
                continue

            # Check if this is a main heading
            is_heading = False

            # Skip numbered items (like 2.5.1, 2.7.9, etc.) - these are NOT headings
            if re.match(r'^\d+\.\d+(\.\d+)?', line):
                is_heading = False

            # Skip single words that might be part of content (like "BID")
            elif len(line.split()) == 1 and not line.endswith(':'):
                is_heading = False

            # Pattern 1: All caps line with colon at end (main section headers)
            elif line.isupper() and line.endswith(':'):
                is_heading = True

            # Pattern 2: Title case line that ends with colon and doesn't start with common item words
            elif (line.endswith(':') and
                  line[0].isupper() and
                  not line.startswith(('Color', 'Gears', 'Atom', 'Books', 'Fish', 'Tree', 'Tractor', 'Column', 'Shield', 'Circle', 'President', '7 Rays', 'University', 'Section', 'Applicants')) and
                  not re.match(r'^\d+\.\d+', line)):
                is_heading = True

            # Pattern 3: Long title-like lines (more than 8 words, all caps with colon)
            elif (len(line.split()) > 8 and
                  line.isupper() and
                  line.endswith(':') and
                  not any(line.startswith(word) for word in ['Color', 'Gears', 'Atom', 'Books', 'Fish', 'Tree', 'Tractor', 'Column', 'Shield', 'Circle', 'President', '7 Rays', 'University', 'Section', 'Applicants']) and
                  not re.match(r'^\d+\.\d+', line)):
                is_heading = True

            if is_heading:
                # Save any current item
                if current_item:
                    current_items.append(current_item.strip())
                    current_item = ""

                # Save previous section if exists
                if current_section and current_items:
                    full_content = f"{current_section}\n" + "\n".join(current_items)
                    # Create a more specific section identifier to avoid confusion
                    section_id = current_section.rstrip(':').lower().replace(' ', '_')
                    chunks.append({
                        'term': current_section.rstrip(':'),  # Remove trailing colon for clean term
                        'definition': "\n".join(current_items),
                        'full_text': full_content,
                        'type': 'section',
                        'section_id': section_id  # Add unique section identifier
                    })

                # Start new section
                current_section = line
                current_items = []

            elif current_section:
                # Check if this starts a new item (has dash or starts with key terms)
                if (line.startswith(('University Vision', 'University Mission', 'Quality Policy', 'Color', 'Gears', 'Atom', 'Books', 'Fish', 'Tree', 'Tractor', 'Column', 'Shield', 'Circle', 'President', '7 Rays')) or
                    line.startswith(tuple(str(i) + '.' for i in range(1, 20)))):

                    # Save previous item if exists
                    if current_item:
                        current_items.append(current_item.strip())

                    # Start new item
                    current_item = line
                else:
                    # Continue current item (multi-line content)
                    if current_item:
                        current_item += " " + line
                    else:
                        current_item = line

            elif not current_section and ':' in line:
                # Standalone definition
                parts = line.split(':', 1)
                if len(parts) == 2:
                    term = parts[0].strip()
                    definition = parts[1].strip()
                    if definition:  # Only if there's actual content after colon
                        chunks.append({
                            'term': term,
                            'definition': definition,
                            'full_text': line,
                            'type': 'definition'
                        })

        # Don't forget the last item and section
        if current_item:
            current_items.append(current_item.strip())

        if current_section and current_items:
            full_content = f"{current_section}\n" + "\n".join(current_items)
            chunks.append({
                'term': current_section.rstrip(':'),  # Remove trailing colon for clean term
                'definition': "\n".join(current_items),
                'full_text': full_content,
                'type': 'section'
            })

        return chunks
    
    def store_chunks(self, chunks: List[Dict[str, str]], source: str = "manual_input") -> int:
        """Store chunks in the vector database."""
        if not chunks:
            print("No chunks to store.")
            return 0

        documents = []
        metadatas = []
        ids = []

        for i, chunk in enumerate(chunks):
            doc_id = str(uuid.uuid4())

            documents.append(chunk['full_text'])
            metadatas.append({
                'term': chunk['term'],
                'definition': chunk['definition'],
                'source': source,
                'chunk_index': i,
                'type': chunk.get('type', 'definition'),
                'section_id': chunk.get('section_id', '')  # Include section_id in metadata
            })
            ids.append(doc_id)

        # Add to collection
        self.collection.add(
            documents=documents,
            metadatas=metadatas,
            ids=ids
        )

        print(f"Stored {len(chunks)} chunks in vector database.")
        return len(chunks)
    
    def search_definitions(self, query: str, n_results: int = 5) -> List[Dict]:
        """Search for definitions in the vector database."""
        results = self.collection.query(
            query_texts=[query],
            n_results=n_results
        )
        
        search_results = []
        if results['documents'] and results['documents'][0]:
            for i, doc in enumerate(results['documents'][0]):
                metadata = results['metadatas'][0][i] if results['metadatas'] else {}
                distance = results['distances'][0][i] if results['distances'] else None
                
                search_results.append({
                    'document': doc,
                    'term': metadata.get('term', ''),
                    'definition': metadata.get('definition', ''),
                    'source': metadata.get('source', ''),
                    'distance': distance
                })
        
        return search_results
    
    def list_all_definitions(self) -> List[Dict]:
        """List all stored definitions."""
        try:
            results = self.collection.get()
            definitions = []

            if results['documents']:
                for i, doc in enumerate(results['documents']):
                    metadata = results['metadatas'][i] if results['metadatas'] else {}
                    doc_id = results['ids'][i] if results['ids'] else ''
                    definitions.append({
                        'id': doc_id,
                        'term': metadata.get('term', ''),
                        'definition': metadata.get('definition', ''),
                        'source': metadata.get('source', ''),
                        'type': metadata.get('type', 'definition'),
                        'full_text': doc
                    })

            return definitions
        except Exception as e:
            print(f"Error listing definitions: {e}")
            return []

    def delete_by_term(self, term: str) -> int:
        """Delete definitions by term name."""
        try:
            # Get all documents
            results = self.collection.get()
            ids_to_delete = []

            if results['metadatas']:
                for i, metadata in enumerate(results['metadatas']):
                    if metadata.get('term', '').lower() == term.lower():
                        ids_to_delete.append(results['ids'][i])

            if ids_to_delete:
                self.collection.delete(ids=ids_to_delete)
                print(f"Deleted {len(ids_to_delete)} definitions for term: {term}")
                return len(ids_to_delete)
            else:
                print(f"No definitions found for term: {term}")
                return 0

        except Exception as e:
            print(f"Error deleting by term: {e}")
            return 0

    def delete_by_id(self, doc_id: str) -> bool:
        """Delete a specific definition by its ID."""
        try:
            self.collection.delete(ids=[doc_id])
            print(f"Deleted definition with ID: {doc_id}")
            return True
        except Exception as e:
            print(f"Error deleting by ID: {e}")
            return False

    def delete_by_source(self, source: str) -> int:
        """Delete all definitions from a specific source."""
        try:
            # Get all documents
            results = self.collection.get()
            ids_to_delete = []

            if results['metadatas']:
                for i, metadata in enumerate(results['metadatas']):
                    if metadata.get('source', '') == source:
                        ids_to_delete.append(results['ids'][i])

            if ids_to_delete:
                self.collection.delete(ids=ids_to_delete)
                print(f"Deleted {len(ids_to_delete)} definitions from source: {source}")
                return len(ids_to_delete)
            else:
                print(f"No definitions found from source: {source}")
                return 0

        except Exception as e:
            print(f"Error deleting by source: {e}")
            return 0

    def delete_by_section_id(self, section_id: str) -> int:
        """Delete definitions by section_id."""
        try:
            # Get all documents
            results = self.collection.get()
            ids_to_delete = []

            if results['metadatas']:
                for i, metadata in enumerate(results['metadatas']):
                    if metadata.get('section_id', '') == section_id:
                        ids_to_delete.append(results['ids'][i])

            if ids_to_delete:
                self.collection.delete(ids=ids_to_delete)
                print(f"Deleted {len(ids_to_delete)} definitions for section_id: {section_id}")
                return len(ids_to_delete)
            else:
                print(f"No definitions found for section_id: {section_id}")
                return 0

        except Exception as e:
            print(f"Error deleting by section_id: {e}")
            return 0

    def clear_all(self) -> bool:
        """Delete all definitions from the collection."""
        try:
            # Get all IDs
            results = self.collection.get()
            if results['ids']:
                self.collection.delete(ids=results['ids'])
                print(f"Deleted all {len(results['ids'])} definitions from the database.")
                return True
            else:
                print("Database is already empty.")
                return True
        except Exception as e:
            print(f"Error clearing database: {e}")
            return False


def main():
    parser = argparse.ArgumentParser(description="Chunk text by definitions and store in vector database")
    parser.add_argument("--db-path", default="./vector_db", help="Path to vector database")
    parser.add_argument("--collection", default="definitions", help="Collection name")
    parser.add_argument("--search", help="Search for definitions")
    parser.add_argument("--list", action="store_true", help="List all stored definitions")
    parser.add_argument("--file", help="Input file to process")
    parser.add_argument("--delete-term", help="Delete definitions by term name")
    parser.add_argument("--delete-id", help="Delete definition by specific ID")
    parser.add_argument("--delete-source", help="Delete all definitions from a specific source")
    parser.add_argument("--delete-section-id", help="Delete definitions by section_id")
    parser.add_argument("--clear-all", action="store_true", help="Delete ALL definitions (use with caution)")
    parser.add_argument("--sections", action="store_true", help="Chunk by sections instead of individual definitions")

    args = parser.parse_args()
    
    # Initialize chunker
    chunker = DefinitionChunker(db_path=args.db_path, collection_name=args.collection)

    # Handle delete operations
    if args.clear_all:
        confirm = input("Are you sure you want to delete ALL definitions? Type 'yes' to confirm: ")
        if confirm.lower() == 'yes':
            chunker.clear_all()
        else:
            print("Operation cancelled.")
        return

    if args.delete_term:
        chunker.delete_by_term(args.delete_term)
        return

    if args.delete_id:
        chunker.delete_by_id(args.delete_id)
        return

    if args.delete_source:
        chunker.delete_by_source(args.delete_source)
        return

    if args.delete_section_id:
        chunker.delete_by_section_id(args.delete_section_id)
        return

    # Handle different modes
    if args.search:
        print(f"Searching for: {args.search}")
        results = chunker.search_definitions(args.search)
        if results:
            for i, result in enumerate(results, 1):
                print(f"\n{i}. {result['term']}")
                print(f"   Definition: {result['definition']}")
                print(f"   Source: {result['source']}")
                if result['distance']:
                    print(f"   Similarity: {1 - result['distance']:.3f}")
        else:
            print("No results found.")
        return
    
    if args.list:
        definitions = chunker.list_all_definitions()
        if definitions:
            print(f"Found {len(definitions)} items:")
            for i, defn in enumerate(definitions, 1):
                chunk_type = defn.get('type', 'definition')
                print(f"\n{i}. {defn['term']} [{chunk_type.upper()}]")
                if chunk_type == 'section':
                    print(f"   Content: {defn['definition'][:200]}...")
                else:
                    print(f"   Definition: {defn['definition']}")
                print(f"   Source: {defn['source']}")
                print(f"   ID: {defn['id']}")
        else:
            print("No definitions found in database.")
        return
    
    # Input mode
    if args.file:
        try:
            with open(args.file, 'r', encoding='utf-8') as f:
                text = f.read()
            source = f"file:{args.file}"
        except Exception as e:
            print(f"Error reading file: {e}")
            return
    else:
        print("Enter your text with definitions (press Ctrl+D or Ctrl+Z when done):")
        print("Supported formats:")
        print("- Term: Definition")
        print("- **Term**: Definition")
        print("- Term - Definition")
        print("- 1. Term: Definition")
        print()
        
        try:
            text = sys.stdin.read()
            source = "manual_input"
        except KeyboardInterrupt:
            print("\nOperation cancelled.")
            return
    
    if not text.strip():
        print("No text provided.")
        return
    
    # Process text
    print("Processing text...")
    if args.sections:
        print("Using section-based chunking...")
        chunks = chunker.chunk_by_sections(text)
    else:
        print("Using definition-based chunking...")
        chunks = chunker.chunk_by_definitions(text)

    if chunks:
        if args.sections:
            print(f"Found {len(chunks)} sections:")
            for i, chunk in enumerate(chunks, 1):
                chunk_type = chunk.get('type', 'definition')
                if chunk_type == 'section':
                    print(f"{i}. Section: {chunk['term']}")
                    print(f"   Contains: {len(chunk['definition'].split(chr(10)))} items")
                else:
                    print(f"{i}. Definition: {chunk['term']}: {chunk['definition'][:100]}...")
        else:
            print(f"Found {len(chunks)} definitions:")
            for i, chunk in enumerate(chunks, 1):
                print(f"{i}. {chunk['term']}: {chunk['definition'][:100]}...")

        # Store in database
        stored_count = chunker.store_chunks(chunks, source)
        print(f"\nSuccessfully stored {stored_count} chunks in vector database.")
    else:
        print("No definitions or sections found in the provided text.")
        print("Make sure your text follows one of the supported formats.")


if __name__ == "__main__":
    main()
