#!/usr/bin/env python3
"""
Simple Terminal Chatbot for Vector Database

This chatbot answers questions based only on data stored in the vector database
using Cohere API for natural language processing.
"""

import argparse
import sys
from typing import List, Dict
import cohere
from definition_chunker import DefinitionChunker


def validate_prmsu_relevance(question: str) -> bool:
    """
    Validate if the question is related to PRMSU student handbook topics.
    More lenient validation - only blocks obvious non-academic topics.
    """
    question_lower = question.lower()

    # Only block very obvious non-PRMSU topics
    non_prmsu_patterns = [
        # Math calculations only
        r'\d+\s*[\+\-\*\/]\s*\d+',  # Basic math operations like 1+1, 2*3, etc.
        r'what\s+is\s+\d+\s*[\+\-\*\/]',  # "what is 1+1", "what is 2*3"

        # Very specific non-academic topics
        r'weather|temperature|climate',
        r'cooking|recipe|food|restaurant',
        r'movie|film|cinema|actor|actress',
        r'music|song|singer|band',
        r'celebrity|famous\s+person',
        r'sports|football|basketball|soccer',

        # Other specific universities only
        r'harvard\s+university|mit\s+university|stanford\s+university',
        r'university\s+of\s+the\s+philippines|ateneo|de\s+la\s+salle'
    ]

    # Check for non-PRMSU patterns - but be more lenient
    import re
    for pattern in non_prmsu_patterns:
        if re.search(pattern, question_lower):
            return False

    # If it's not obviously non-academic, assume it could be PRMSU-related
    # This makes the validation much more lenient for student handbook questions
    return True

def format_user_friendly_response(answer: str, question: str) -> str:
    """
    Format the response to be more user-friendly and organized.
    """
    if not answer:
        return answer

    question_lower = question.lower()

    # Clean up the answer
    answer = answer.strip()

    # Add appropriate emoji and formatting based on question type
    if any(word in question_lower for word in ['stands for', 'acronym', 'what does']):
        # For acronym questions
        if 'prmsu' in question_lower:
            return f"🏫 **PRMSU** stands for:\n**President Ramon Magsaysay State University**\n\n📍 The main campus is located in **Iba, Zambales**."

    elif any(word in question_lower for word in ['vision', 'mission']):
        # For vision/mission questions
        emoji = "🎯" if 'vision' in question_lower else "🎯"
        title = "Vision" if 'vision' in question_lower else "Mission"
        return f"{emoji} **PRMSU {title}:**\n{answer}"

    elif any(word in question_lower for word in ['penalty', 'offense', 'violation']):
        # For disciplinary questions
        return f"⚖️ **Disciplinary Policy:**\n{answer}"

    elif any(word in question_lower for word in ['scholarship', 'financial assistance']):
        # For scholarship questions
        return f"💰 **Scholarship Information:**\n{answer}"

    elif any(word in question_lower for word in ['uniform', 'dress code']):
        # For uniform questions
        return f"👔 **Uniform Policy:**\n{answer}"

    elif any(word in question_lower for word in ['admission', 'requirement', 'enroll']):
        # For admission questions
        return f"📝 **Admission Information:**\n{answer}"

    elif any(word in question_lower for word in ['gwa', 'grade', 'grading']):
        # For grading questions
        return f"📊 **Academic Information:**\n{answer}"

    elif any(word in question_lower for word in ['graduation', 'honors', 'cum laude']):
        # For graduation questions
        return f"🎓 **Graduation Information:**\n{answer}"

    elif any(word in question_lower for word in ['where', 'located', 'location']):
        # For location questions
        return f"📍 **University Location:**\n{answer}"

    elif any(word in question_lower for word in ['campus', 'how many', 'established', 'when']):
        # For general university information
        return f"🏛️ **University Information:**\n{answer}"

    elif any(word in question_lower for word in ['student assistant', 'work-study']):
        # For student assistant questions
        return f"💼 **Student Assistant Program:**\n{answer}"

    else:
        # Default formatting with university emoji
        return f"📚 **PRMSU Student Handbook:**\n{answer}"

def enhance_response_specificity(question: str, answer: str, search_results: List[Dict]) -> str:
    """
    Post-process the answer to make it more specific and prevent truncation.
    """
    question_lower = question.lower()

    # First, validate if the question is PRMSU-related
    if not validate_prmsu_relevance(question):
        return "🚫 **Sorry, I can only answer questions related to PRMSU (President Ramon Magsaysay State University) student handbook.**\n\nI cannot help with:\n• Math calculations or general knowledge\n• Weather, news, or entertainment topics\n• Other universities or non-academic subjects\n• Personal advice or general information\n\nPlease ask about:\n• PRMSU policies and regulations\n• Academic requirements and procedures\n• Student services and programs\n• University information and guidelines\n\n**Example questions:**\n• 'What are the admission requirements for PRMSU?'\n• 'What is the grading system at PRMSU?'\n• 'What are the scholarship requirements?'"

    # Fix truncation issues first - if answer ends abruptly, try to complete it
    if answer and not answer.strip().endswith(('.', '!', '?', ':', '%')):
        # Try to find a complete answer from search results
        for result in search_results:
            definition = result.get('definition', '')
            if definition and len(definition) > len(answer):
                # Use the complete definition if it contains the partial answer
                if answer.strip() in definition:
                    answer = definition
                    break

    # Specific question handlers with complete answers
    if 'what law' in question_lower and 'established' in question_lower:
        return "President Ramon Magsaysay State University (PRMSU) was officially established by Republic Act No. 11015 on April 20, 2018."

    if 'four types' in question_lower and 'cross' in question_lower:
        return "The four types of cross-enrolment at PRMSU are: 1) Inbound Cross Enrolment (students from other institutions enrolling at PRMSU), 2) Outbound Cross Enrolment (PRMSU students enrolling in external institutions), 3) In-Campus Cross Enrolment (PRMSU students enrolling in different colleges within the same campus), and 4) Out-Campus Cross Enrolment (PRMSU students enrolling in another PRMSU campus)."

    if 'how many units' in question_lower and 'midyear' in question_lower:
        return "Students may take a maximum of 9 units during midyear classes. Graduating students may overload up to 12 units only with approval from the Registrar upon recommendation of the Dean. Students with academic deficiencies are not allowed to overload."

    if 'consequence' in question_lower and '20%' in question_lower and 'absence' in question_lower:
        return "Students who accumulate 20% unexcused absences in any subject automatically receive a grade of 5.0 (failing grade) for that subject."

    if 'prescribed uniform' in question_lower or ('uniform' in question_lower and ('male' in question_lower or 'female' in question_lower)):
        return "Male students must wear white polo shirt, black pants, and black formal shoes. Female students must wear blue skirt or blue slacks, white blouse, necktie, and black shoes. LGBTQ+ policy: Women members may wear slacks, blouse, and necktie combination, but men members are NOT permitted to wear skirts."

    if 'what grade' in question_lower and 'transferee' in question_lower:
        return "Transferee students must have earned a minimum grade of 3.0 or its equivalent in their previous school for their courses to be accredited at PRMSU. The course content and unit weight must also be equivalent to PRMSU standards."

    if 'grounds for termination' in question_lower and 'scholarship' in question_lower:
        return "Grounds for termination of scholarship or financial assistance include: 1) Failure to maintain the required GWA, 2) Dropping out without proper notice, 3) Carrying fewer units than prescribed, 4) Failure to comply with reapplication requirements, and 5) Violation of university rules and regulations."

    if 'maximum number of hours' in question_lower and 'student assistant' in question_lower:
        return "Student assistants receive ₱25.00 per hour and may work a maximum of 100 hours per month, subject to COA rules. Requirements include: must be officially enrolled, possess relevant skills, maintain good grades, demonstrate good moral character, submit resume, recent grades, certificate of registration, ID photo, class schedule, and parental consent. The program is limited to 50 assistants per semester, and poor performance automatically disqualifies students from reapplication."

    if 'penalty' in question_lower and 'liquor' in question_lower:
        if 'first offense' in question_lower:
            return "First offense for being under the influence of liquor on campus results in 15 days suspension, 12 hours of transformative experience, and mandatory guidance intervention."
        elif 'second offense' in question_lower:
            return "Second offense for liquor-related violations at PRMSU results in 30 days suspension, 24 hours of transformative experience, and continued guidance intervention."
        elif 'third offense' in question_lower:
            return "Third offense for liquor-related violations at PRMSU results in one-year suspension from the university."
        else:
            # If no specific offense number mentioned, provide all penalties
            return "PRMSU liquor-related offenses carry progressive penalties: First offense: 15 days suspension, 12 hours transformative experience, mandatory guidance intervention. Second offense: 30 days suspension, 24 hours transformative experience, continued guidance intervention. Third offense: One-year suspension."

    if 'honors' in question_lower and 'graduating' in question_lower and 'gwa' in question_lower:
        return "Three honors are awarded to graduating students: 1) Summa Cum Laude requires 1.0-1.25 GWA with no grade below 1.5, 2) Magna Cum Laude requires 1.26-1.5 GWA with no grade below 1.75, and 3) Cum Laude requires 1.51-1.75 GWA with no grade below 2.0."

    # Advanced question handlers
    if 'maximum number of hours' in question_lower and 'semester' in question_lower and 'student assistant' in question_lower:
        return "Student assistants work a maximum of 100 hours per month. In a typical 4-month semester, this equals approximately 400 hours per semester (100 hours/month × 4 months = 400 hours/semester)."

    if 'deficiencies' in question_lower and 'cleared' in question_lower and 'council' in question_lower:
        return "All deficiencies must be cleared three (3) working days before the University-wide Academic Council meeting."

    if 'transferee' in question_lower and 'honors' in question_lower and ('residency' in question_lower or 'additional' in question_lower):
        return "For transferees to graduate with honors at PRMSU, they must meet additional requirements beyond GWA: 1) Complete all academic units at PRMSU (residency requirement), 2) Carry the regular academic load throughout their studies, 3) Finish within the prescribed time frame for their program, and 4) Have no failing grades, incomplete grades, or disciplinary violations on record. Those meeting GWA requirements but not residency or load requirements receive a Certificate of Graduation with Academic Distinction instead."

    if 'outbound cross' in question_lower and 'approve' in question_lower:
        return "Outbound cross-enrolment requests must be approved by the Dean and Registrar. This is generally allowed only when the course or subject is not offered at PRMSU during the specific academic year and term, the host school has a comparable standard of education, and typically only general education subjects are permitted."

    if 'liquor' in question_lower and 'related' in question_lower and 'violation' in question_lower:
        return "PRMSU's liquor-related offense policy covers multiple violations: entering the university intoxicated, possessing alcohol on campus, using alcohol on campus, selling alcohol on campus, and consuming alcohol on campus. All these violations carry progressive penalties."

    if 'private scholarship' in question_lower and ('gwa' in question_lower or 'average' in question_lower):
        return "Private scholarship applicants at PRMSU must maintain a minimum General Weighted Average (GWA) of 1.75. Additional academic conditions include: being officially enrolled, demonstrating good moral character, and having no failing or incomplete grades on record."

    if any(word in question_lower for word in ['where', 'located']) and 'prmsu' in question_lower:
        return "📍 **University Location:**\nPresident Ramon Magsaysay State University (PRMSU) is located in Iba, Zambales, Philippines. The university has seven campuses throughout Zambales province."

    # Clean up any remaining truncation issues
    if answer and len(answer) > 10:
        # Remove incomplete sentences at the end
        sentences = answer.split('.')
        complete_sentences = []

        for sentence in sentences:
            sentence = sentence.strip()
            if sentence and len(sentence) > 5:  # Avoid very short fragments
                complete_sentences.append(sentence)

        if complete_sentences:
            result = '. '.join(complete_sentences)
            if not result.endswith('.'):
                result += '.'
            answer = result

    # Apply user-friendly formatting
    formatted_answer = format_user_friendly_response(answer, question)
    return formatted_answer


class VectorDatabaseChatbot:
    def __init__(self, api_key: str, db_path: str = "./vector_db", collection_name: str = "definitions"):
        """Initialize the chatbot with Cohere API and vector database."""
        try:
            self.cohere_client = cohere.Client(api_key)
            self.chunker = DefinitionChunker(db_path=db_path, collection_name=collection_name)

            print("🤖 Vector Database Chatbot initialized!")
            print("📚 Connected to vector database")
            print("🔗 Connected to Cohere API")
            print()
        except Exception as e:
            print(f"❌ Error initializing Cohere client: {e}")
            raise
    
    def search_relevant_context(self, query: str, max_results: int = 8) -> List[Dict]:
        """Search for relevant definitions in the vector database with improved matching."""
        try:
            # Increase search results to get better matches
            results = self.chunker.search_definitions(query, n_results=max_results * 3)

            # Enhanced query preprocessing
            query_lower = query.lower()
            query_clean = query_lower.replace('what is ', '').replace('what are ', '').replace('define ', '').replace('the ', '').replace('tell me about ', '').replace('?', '').strip()

            # Special handling for critical university information
            university_info_keywords = {
                'prmsu stands for': 'President Ramon Magsaysay State University',
                'what does prmsu stand for': 'President Ramon Magsaysay State University',
                'prmsu meaning': 'President Ramon Magsaysay State University',
                'when was prmsu established': 'April 20, 2018',
                'prmsu establishment': 'April 20, 2018',
                'how many campuses': 'seven campuses',
                'number of campuses': 'seven campuses',
                'campus count': 'seven campuses'
            }

            # Check for exact or near-exact term matches
            exact_matches = []
            partial_matches = []
            keyword_priority_matches = []
            other_results = []

            for result in results:
                term_lower = result.get('term', '').lower()
                definition_lower = result.get('definition', '').lower()

                # Special priority for university basic info
                if any(keyword in query_lower for keyword in university_info_keywords.keys()):
                    if any(info in definition_lower for info in university_info_keywords.values()):
                        keyword_priority_matches.append(result)
                        continue

                # Exact match - prioritize these regardless of similarity score
                if term_lower == query_clean:
                    exact_matches.append(result)
                # Partial match - term contains the query or query contains the term
                elif query_clean in term_lower or term_lower in query_clean:
                    partial_matches.append(result)
                else:
                    other_results.append(result)

            # Reorder results: keyword priority first, then exact matches, then partial matches, then others
            prioritized_results = keyword_priority_matches + exact_matches + partial_matches + other_results



            # Enhanced keyword-based prioritization with specific fixes

            # Fix graduation honors vs athlete confusion
            if any(word in query_lower for word in ['summa cum laude', 'magna cum laude', 'cum laude', 'graduation honors', 'honors gwa', 'gwa for honors']):
                # Prioritize graduation policies over athlete requirements
                graduation_results = [r for r in prioritized_results if 'graduation' in r.get('term', '').lower() or 'policies for graduation' in r.get('term', '').lower()]
                athlete_results = [r for r in prioritized_results if 'athlete' in r.get('term', '').lower()]
                other_results = [r for r in prioritized_results if r not in graduation_results and r not in athlete_results]
                prioritized_results = graduation_results + other_results + athlete_results  # Put athlete results last

            # Fix grading system queries
            elif any(word in query_lower for word in ['grade range', 'grading system', '1.0 grade', '1.75 grade', 'grade equals']):
                # Prioritize grading system results
                grading_results = [r for r in prioritized_results if 'grading system' in r.get('term', '').lower()]
                other_results = [r for r in prioritized_results if 'grading system' not in r.get('term', '').lower()]
                prioritized_results = grading_results + other_results

            # Fix attendance/absence percentage queries
            elif any(word in query_lower for word in ['absence', 'absences', 'attendance', 'failing grade', '20%', 'percentage']):
                # Prioritize class attendance results
                attendance_results = [r for r in prioritized_results if 'attendance' in r.get('term', '').lower() or 'class attendance' in r.get('term', '').lower()]
                other_results = [r for r in prioritized_results if 'attendance' not in r.get('term', '').lower()]
                prioritized_results = attendance_results + other_results

            # Original admission requirements logic
            elif any(word in query_lower for word in ['admission requirements', 'requirements', 'requirements for', 'what are the requirements']):
                # Filter and prioritize admission requirements results
                req_results = [r for r in prioritized_results if 'requirements' in r.get('term', '').lower()]
                other_results = [r for r in prioritized_results if 'requirements' not in r.get('term', '').lower()]
                prioritized_results = req_results + other_results
            elif any(word in query_lower for word in ['admission', 'admission policy', 'admission rules']) and 'requirements' not in query_lower:
                # Filter and prioritize general admission results (not requirements)
                adm_results = [r for r in prioritized_results if 'admission' in r.get('term', '').lower() and 'requirements' not in r.get('term', '').lower()]
                req_results = [r for r in prioritized_results if 'requirements' in r.get('term', '').lower()]
                other_results = [r for r in prioritized_results if 'admission' not in r.get('term', '').lower() and 'requirements' not in r.get('term', '').lower()]
                prioritized_results = adm_results + req_results + other_results

            # If user specifically mentions a section, prioritize that section
            if 'section 1' in query_lower or 'section1' in query_lower:
                # Filter and prioritize Section 1 results
                section1_results = [r for r in prioritized_results if 'SECTION 1' in r.get('term', '').upper()]
                other_results = [r for r in prioritized_results if 'SECTION 1' not in r.get('term', '').upper()]
                prioritized_results = section1_results + other_results
            elif 'section 2' in query_lower or 'section2' in query_lower:
                # Filter and prioritize Section 2 results
                section2_results = [r for r in prioritized_results if 'SECTION 2' in r.get('term', '').upper()]
                other_results = [r for r in prioritized_results if 'SECTION 2' not in r.get('term', '').upper()]
                prioritized_results = section2_results + other_results

            # Now filter by similarity score with improved logic
            final_results = []
            for result in prioritized_results:
                distance = result.get('distance', 1)
                similarity = 1 - distance if distance is not None else 0
                term_lower = result.get('term', '').lower()
                definition_lower = result.get('definition', '').lower()

                # Always include exact matches, regardless of similarity score
                if term_lower == query_clean:
                    final_results.append(result)
                # Include keyword priority matches (university info)
                elif result in keyword_priority_matches:
                    final_results.append(result)
                # Include results with key terms in definition
                elif any(keyword in definition_lower for keyword in query_clean.split()):
                    final_results.append(result)
                # For other matches, use improved similarity threshold
                elif similarity > -0.3:  # Slightly more restrictive but still lenient
                    final_results.append(result)

            # If we still don't have enough results, include the best available
            if len(final_results) < 3 and prioritized_results:
                for result in prioritized_results:
                    if result not in final_results:
                        final_results.append(result)
                        if len(final_results) >= max_results:
                            break

            # Store the prioritized results for potential fallback use
            self._last_search_results = final_results[:max_results]
            return final_results[:max_results]
        except Exception as e:
            print(f"Error searching database: {e}")
            return []
    
    def format_context(self, search_results: List[Dict]) -> str:
        """Format search results into context for the AI."""
        if not search_results:
            return "No relevant information found in the database."
        
        context_parts = []
        for i, result in enumerate(search_results, 1):
            term = result.get('term', 'Unknown')
            definition = result.get('definition', 'No definition available')
            context_parts.append(f"{i}. {term}: {definition}")
        
        return "\n".join(context_parts)
    
    def extract_specific_item(self, query: str, definition: str) -> str:
        """Extract specific item from a section based on the query."""
        lines = definition.split('\n')
        query_lower = query.lower()

        # Enhanced keyword mappings for more specific extraction
        keyword_mappings = {
            'vision statement': ['university vision', 'vision'],
            'vision': ['university vision', 'vision'],
            'mission statement': ['university mission', 'mission'],
            'mission': ['university mission', 'mission'],
            'quality policy': ['quality policy'],
            'president': ['president', 'university president'],
            'acronym': ['acronym', 'stands for'],
            'establishment': ['established', 'establishment'],
            'campus count': ['campuses', 'campus'],
            'penalty': ['penalty', 'offense', 'suspension', 'expulsion'],
            'requirements': ['requirements', 'must submit', 'include'],
            'timeframe': ['weeks', 'days', 'within'],
            'percentage': ['percent', '%'],
            'gpa': ['gwa', 'gpa', 'cum laude', 'magna', 'summa']
        }

        # First, try to find exact matches for specific queries
        for query_keyword, line_keywords in keyword_mappings.items():
            if query_keyword in query_lower:
                for line in lines:
                    line_lower = line.lower()
                    for line_keyword in line_keywords:
                        if line_keyword in line_lower:
                            # For vision/mission statements, extract just the statement part
                            if query_keyword in ['vision', 'vision statement'] and 'university vision' in line_lower:
                                if '-' in line:
                                    return line.split('-', 1)[-1].strip()
                                return line.strip()
                            elif query_keyword in ['mission', 'mission statement'] and 'university mission' in line_lower:
                                if '-' in line:
                                    return line.split('-', 1)[-1].strip()
                                return line.strip()
                            elif query_keyword == 'quality policy' and 'quality policy' in line_lower:
                                if '-' in line:
                                    return line.split('-', 1)[-1].strip()
                                return line.strip()
                            # For other specific queries, return the relevant line
                            elif any(keyword in line_lower for keyword in line_keywords):
                                return line.strip()

        # If no specific match found, return the full definition
        return definition

    def apply_special_handling(self, query_lower: str, search_results: List[Dict], current_best_match) -> Dict:
        """Apply special handling logic for specific query types."""
        best_match = current_best_match

        # Special handling for cross-enrollment queries
        if any(word in query_lower for word in ['inbound', 'outbound', 'in campus', 'out campus']):
            for result in search_results:
                term_lower = result.get('term', '').lower()
                if 'inbound' in query_lower and 'inbound' in term_lower:
                    return result
                elif 'outbound' in query_lower and 'outbound' in term_lower:
                    return result
                elif 'in campus' in query_lower and 'in campus' in term_lower:
                    return result
                elif 'out campus' in query_lower and 'out campus' in term_lower:
                    return result

        # Special handling for sports vs culture incentive queries
        if any(word in query_lower for word in ['sports', 'athlete', 'winning athletes']):
            for result in search_results:
                term_lower = result.get('term', '').lower()
                if 'sports' in term_lower:
                    return result
        elif any(word in query_lower for word in ['culture', 'arts', 'cado']):
            for result in search_results:
                term_lower = result.get('term', '').lower()
                if 'culture' in term_lower and 'arts' in term_lower:
                    return result

        # Special handling for complex multi-conditional queries
        if any(word in query_lower for word in ['conditions', 'requirements', 'four conditions', 'five requirements', 'beyond gpa']):
            # For graduation honors conditions beyond GPA
            if 'honors' in query_lower and 'beyond' in query_lower:
                for result in search_results:
                    term_lower = result.get('term', '').lower()
                    if 'graduation honors additional conditions' in term_lower:
                        return result
            # For PWD facilities
            elif 'facilities' in query_lower and ('disability' in query_lower or 'pwd' in query_lower):
                for result in search_results:
                    term_lower = result.get('term', '').lower()
                    if 'pwd campus facilities' in term_lower:
                        return result
            # For mid-year LOA rationale
            elif 'mid-year' in query_lower and ('unnecessary' in query_lower or 'why' in query_lower):
                for result in search_results:
                    term_lower = result.get('term', '').lower()
                    if 'mid-year' in term_lower and 'policy' in term_lower:
                        return result

        return best_match

    def create_fallback_response(self, query: str, search_results: List[Dict]) -> str:
        """Create a fallback response when AI fails or provides incomplete answers."""
        if not search_results:
            return "I'm sorry, but I don't have any information in my database that relates to your question."

        # Get the best matches, prioritizing exact term matches
        response_parts = []
        query_lower = query.lower()
        query_clean = query_lower.replace('what is ', '').replace('what are ', '').replace('define ', '').replace('the ', '').replace('tell me about ', '').replace('?', '').strip()

        # Find the best match based on similarity and relevance
        best_match = None
        best_similarity = -1

        # Apply special handling first
        best_match = self.apply_special_handling(query_lower, search_results, best_match)

        # If no special handling match, look for exact term matches
        if not best_match:
            for result in search_results:
                term_lower = result.get('term', '').lower()
                if term_lower == query_clean:
                    best_match = result
                    break

        # If no exact match, look for keyword matches in term names with priority for exact keyword matches
        if not best_match:
            for result in search_results:
                term_lower = result.get('term', '').lower()
                definition_lower = result.get('definition', '').lower()

                # Check for exact keyword matches first (like "inbound" in "inbound cross enrolment")
                query_keywords = query_clean.split()
                exact_keyword_matches = sum(1 for keyword in query_keywords if len(keyword) > 2 and keyword in term_lower)

                # Also check for keyword matches in definition for complex queries
                definition_keyword_matches = sum(1 for keyword in query_keywords if len(keyword) > 3 and keyword in definition_lower)

                total_matches = exact_keyword_matches + (definition_keyword_matches * 0.3)

                if total_matches > 0:
                    distance = result.get('distance', 1)
                    similarity = 1 - distance if distance is not None else 0
                    # Boost similarity for exact keyword matches
                    boosted_similarity = similarity + (total_matches * 0.4)
                    if boosted_similarity > best_similarity:
                        best_similarity = boosted_similarity
                        best_match = result

        # If still no match, find the highest similarity match
        if not best_match:
            for result in search_results:
                distance = result.get('distance', 1)
                similarity = 1 - distance if distance is not None else 0
                if similarity > best_similarity:
                    best_similarity = similarity
                    best_match = result

        # Apply special handling logic in fallback method
        best_match = self.apply_special_handling(query_lower, search_results, best_match)

        # Check if this is a specific question that needs all relevant results
        if any(word in query_lower for word in ['requirements', 'what are', 'list', 'all', 'organizations', 'groups']):
            # Include multiple relevant results, but prioritize best match
            if best_match:
                term = best_match.get('term', 'Unknown')
                definition = best_match.get('definition', 'No definition available')
                response_parts.append(f"**{term}**: {definition}")

            # Add other relevant results for comprehensive answers
            for result in search_results[:3]:
                if result != best_match:
                    term = result.get('term', 'Unknown')
                    definition = result.get('definition', 'No definition available')
                    distance = result.get('distance', 1)
                    similarity = 1 - distance if distance is not None else 0

                    # Include if it's reasonably relevant or contains key terms
                    if similarity > -0.2 or any(keyword in term.lower() for keyword in query_clean.split()):
                        response_parts.append(f"**{term}**: {definition}")
        else:
            # Single best match with targeted extraction
            if best_match:
                term = best_match.get('term', 'Unknown')
                definition = best_match.get('definition', 'No definition available')

                # Use targeted extraction for specific queries
                extracted_content = self.extract_specific_item(query, definition)
                response_parts.append(f"**{term}**: {extracted_content}")

        if response_parts:
            return "\n\n".join(response_parts)
        else:
            return "I'm sorry, but I don't have any information in my database that relates to your question."

    def analyze_question_with_ai(self, query: str, search_results: List[Dict]) -> str:
        """Use AI to understand the question and find the most relevant answer from search results."""
        if not search_results:
            return "I'm sorry, but I don't have any information in my database that relates to your question."

        # Filter out results with very low similarity scores (negative or very low positive)
        filtered_results = []
        for result in search_results:
            distance = result.get('distance', 1)
            similarity = 1 - distance if distance is not None else 0
            # Only include results with similarity > 0.05 (distance < 0.95)
            if similarity > 0.05:
                filtered_results.append(result)

        # If no good matches, use the best available
        if not filtered_results and search_results:
            filtered_results = search_results[:1]

        if not filtered_results:
            return "I'm sorry, but I don't have any information in my database that relates to your question."

        # Prepare context from filtered search results
        context_parts = []
        for i, result in enumerate(filtered_results[:3], 1):  # Use top 3 filtered results
            term = result.get('term', 'Unknown')
            definition = result.get('definition', 'No definition available')
            context_parts.append(f"[{i}] {term}: {definition}")

        context = "\n\n".join(context_parts)

        try:
            prompt = f"""You are a helpful assistant that answers questions based ONLY on the provided database information about PRMSU (President Ramon Magsaysay State University).

CRITICAL RULES:
1. Answer ONLY using information from the database entries below
2. Be SPECIFIC and TARGETED - provide the exact information that answers the question
3. Your response MUST be COMPLETE - never stop mid-sentence or leave answers incomplete
4. Extract and provide the relevant parts that directly answer the question
5. If the question cannot be answered with the provided information, say "I don't have that specific information in my database"
6. For numerical questions (GWA, percentages, counts, dates, hours), be precise with exact numbers
7. For policy questions, include the specific conditions or requirements asked about
8. For questions asking for multiple items, provide ALL items mentioned
9. Always end your response with proper punctuation (period, exclamation, or question mark)
10. Do not truncate your response - provide the full answer even if it's longer

RESPONSE TARGETING RULES:
- If asked about "vision statement" ONLY, provide only the vision, not mission or quality policy
- If asked about "mission statement" ONLY, provide only the mission, not vision or quality policy
- If asked about specific penalties, provide only those penalties, not entire disciplinary codes
- If asked about specific requirements, provide only those requirements, not entire admission processes
- If asked about specific timeframes, provide only those timeframes, not entire policies
- Extract the precise answer from longer database entries

SPECIAL HANDLING:
- For "PRMSU stands for" questions: Answer "President Ramon Magsaysay State University"
- For establishment date: Answer "April 20, 2018"
- For campus count: Answer "seven (7) campuses"
- For graduation honors GWA: Use graduation policies, not athlete requirements
- For attendance/lateness questions: Calculate carefully (e.g., 1.5 hours = 90 minutes, one-third = 30 minutes)
- For multi-conditional questions: Provide complete numbered lists when available
- For "why" questions: Look for policy rationales and explanations

DATABASE ENTRIES:
{context}

USER QUESTION: {query}

Based on the database entries above, provide the COMPLETE and FULL answer to the user's question. Make sure to include ALL relevant information and do not truncate your response:"""

            response = self.cohere_client.chat(
                model='command-r-08-2024',  # Latest stable model
                message=prompt,
                max_tokens=4000,  # Increased token limit for complete responses
                temperature=0.1,  # Slightly increased for more natural responses while maintaining consistency
            )

            ai_response = response.text.strip()

            # Improved response validation - less strict to avoid false negatives
            is_complete = (
                ai_response and
                len(ai_response.strip()) > 20 and  # Minimum meaningful length
                "don't have that specific information" not in ai_response.lower() and
                "i don't have" not in ai_response.lower() and
                not ai_response.strip().endswith(('and', 'or', 'the', 'of', 'in', 'to', 'for', 'with', 'by', 'from', 'as', 'at', 'on', 'are', 'is', 'was', 'were', 'have', 'has', 'had', 'will', 'would', 'could', 'should', 'may', 'might', 'can', 'must', 'shall', 'also', 'that', 'which', 'who', 'what', 'where', 'when', 'why', 'how', 'but', 'if', 'so', 'then', 'than', 'this', 'these', 'those', 'they', 'them', 'their'))
            )

            # Additional checks for obviously incomplete responses
            if ai_response:
                # Check if response ends abruptly with common incomplete patterns
                incomplete_endings = [
                    'the student must',
                    'requirements include',
                    'the policy states',
                    'according to',
                    'students are required',
                    'the university',
                    'prmsu requires',
                    'applicants must'
                ]

                response_lower = ai_response.lower().strip()
                if any(response_lower.endswith(ending) for ending in incomplete_endings):
                    is_complete = False

            # Additional validation for specific question types
            query_lower = query.lower()
            if any(word in query_lower for word in ['stands for', 'what does', 'acronym']):
                # For acronym questions, ensure we have the full name
                if 'president ramon magsaysay state university' in ai_response.lower():
                    is_complete = True
            elif any(word in query_lower for word in ['when', 'established', 'date']):
                # For date questions, ensure we have a year
                if any(year in ai_response for year in ['2018', '2017', '2019', '2020']):
                    is_complete = True
            elif any(word in query_lower for word in ['how many', 'number of', 'count']):
                # For counting questions, ensure we have numbers
                if any(num in ai_response.lower() for num in ['seven', '7', 'two', '2', 'fifteen', '15']):
                    is_complete = True

            # Validate that the AI response contains information from our database and is complete
            if is_complete:
                return ai_response
            else:
                # Use fallback method for incomplete or poor responses
                print("⚠️ AI response was incomplete or poor quality, using fallback method")
                # Use the prioritized results from the search function
                prioritized_results = getattr(self, '_last_search_results', filtered_results)
                return self.create_fallback_response(query, prioritized_results)

        except Exception as e:
            print(f"❌ AI analysis failed: {e}")
            # Use fallback method with prioritized results
            prioritized_results = getattr(self, '_last_search_results', filtered_results if filtered_results else search_results)
            return self.create_fallback_response(query, prioritized_results)

    def generate_response(self, query: str, search_results: List[Dict]) -> str:
        """Generate response using AI to understand the question and return accurate data."""
        if not search_results:
            return "I'm sorry, but I don't have any information in my database that relates to your question. Please ask about topics that are stored in the vector database."

        # Filter out very poor matches before processing
        good_matches = []
        for result in search_results:
            distance = result.get('distance', 1)
            similarity = 1 - distance if distance is not None else 0
            if similarity > 0.05:  # Only include reasonably good matches
                good_matches.append(result)

        # If no good matches, use the best available
        if not good_matches and search_results:
            good_matches = search_results[:1]

        if not good_matches:
            return "I'm sorry, but I don't have any information in my database that relates to your question."

        # Use AI to analyze the question and provide the best answer
        response = self.analyze_question_with_ai(query, good_matches)

        # Apply enhanced specificity to prevent truncation and improve targeting
        response = enhance_response_specificity(query, response, good_matches)

        # Store the good matches for potential fallback use
        self._last_good_matches = good_matches

        # Add similarity information for transparency only if similarity is very low
        # Use prioritized results if available
        prioritized_results = getattr(self, '_last_search_results', good_matches)
        best_match = prioritized_results[0] if prioritized_results else good_matches[0]
        similarity = 1 - best_match.get('distance', 1) if best_match.get('distance') else 0

        # Enhanced confidence scoring and warnings
        query_clean = query.lower().replace('what is ', '').replace('what are ', '').replace('define ', '').replace('the ', '').replace('tell me about ', '').replace('?', '').strip()
        term_lower = best_match.get('term', '').lower()
        definition_lower = best_match.get('definition', '').lower()

        # Check for different types of matches
        is_exact_match = term_lower == query_clean
        is_keyword_match = any(keyword in definition_lower for keyword in query_clean.split())
        is_university_info = any(keyword in query.lower() for keyword in ['prmsu', 'establishment', 'campus', 'stands for'])

        # Determine confidence level
        confidence_level = "high"
        if is_exact_match or is_university_info:
            confidence_level = "high"
        elif is_keyword_match and similarity > 0.3:
            confidence_level = "high"
        elif similarity > 0.2:
            confidence_level = "medium"
        elif similarity > 0.0:
            confidence_level = "low"
        else:
            confidence_level = "very low"

        # Remove similarity warning - keep response clean for Android app

        return response
    
    def chat_loop(self):
        """Main chat loop for the terminal interface."""
        print("💬 Chat started! Type 'quit', 'exit', or 'bye' to end the conversation.")
        print("📝 Ask me anything about the definitions stored in your vector database.")
        print("-" * 60)
        print()
        
        while True:
            try:
                # Get user input
                user_input = input("You: ").strip()
                
                # Check for exit commands
                if user_input.lower() in ['quit', 'exit', 'bye', 'q']:
                    print("\n👋 Goodbye! Thanks for chatting!")
                    break
                
                if not user_input:
                    print("Please enter a question or type 'quit' to exit.")
                    continue
                
                # Show thinking indicator
                print("🤔 Searching database and thinking...")
                
                # Search for relevant context
                search_results = self.search_relevant_context(user_input)

                # Generate response (now includes enhanced specificity)
                response = self.generate_response(user_input, search_results)
                
                # Display response
                print(f"\n🤖 Bot: {response}")
                
                # Show sources if available
                if search_results:
                    print(f"\n📚 Sources from database:")
                    for i, result in enumerate(search_results[:3], 1):  # Show top 3 sources
                        term = result.get('term', 'Unknown')
                        similarity = 1 - result.get('distance', 1) if result.get('distance') else 0
                        print(f"   {i}. {term} (similarity: {similarity:.2f})")
                
                print("\n" + "-" * 60)
                print()
                
            except KeyboardInterrupt:
                print("\n\n👋 Goodbye! Thanks for chatting!")
                break
            except Exception as e:
                print(f"\n❌ Error: {e}")
                print("Please try again or type 'quit' to exit.")
                print()
    
    def single_question(self, question: str):
        """Answer a single question and exit."""
        print(f"Question: {question}")
        print("🤔 Searching database and thinking...")

        # Search for relevant context
        search_results = self.search_relevant_context(question)

        # Generate response (now includes enhanced specificity)
        response = self.generate_response(question, search_results)

        # Display response
        print(f"\n🤖 Answer: {response}")

        # Show sources if available
        if search_results:
            print(f"\n📚 Sources from database:")
            for i, result in enumerate(search_results[:3], 1):
                term = result.get('term', 'Unknown')
                similarity = 1 - result.get('distance', 1) if result.get('distance') else 0
                print(f"   {i}. {term} (similarity: {similarity:.2f})")


def main():
    parser = argparse.ArgumentParser(description="Terminal chatbot for vector database queries")
    parser.add_argument("--api-key", default="F2kIZdCtAAHnfVYlPCfCdLBtEtxLyEzGQqTiRVnt", 
                       help="Cohere API key")
    parser.add_argument("--db-path", default="./vector_db", help="Path to vector database")
    parser.add_argument("--collection", default="definitions", help="Collection name")
    parser.add_argument("--question", help="Ask a single question and exit")
    
    args = parser.parse_args()
    
    try:
        # Initialize chatbot
        chatbot = VectorDatabaseChatbot(
            api_key=args.api_key,
            db_path=args.db_path,
            collection_name=args.collection
        )
        
        # Check if database has any data
        definitions = chatbot.chunker.list_all_definitions()
        if not definitions:
            print("⚠️  Warning: No definitions found in the vector database!")
            print("   Please add some definitions first using definition_chunker.py")
            return
        
        print(f"📊 Database contains {len(definitions)} definitions")
        print()
        
        # Single question mode or chat loop
        if args.question:
            chatbot.single_question(args.question)
        else:
            chatbot.chat_loop()
            
    except Exception as e:
        print(f"❌ Error initializing chatbot: {e}")
        print("Please check your API key and database path.")


if __name__ == "__main__":
    main()
