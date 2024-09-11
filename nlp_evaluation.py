from sentence_transformers import SentenceTransformer, util
import spacy
import language_tool_python
import yake

# Initialize models and tools
nlp = spacy.load("en_core_web_sm")
language_tool = language_tool_python.LanguageTool('en-US')
keyword_extractor = yake.KeywordExtractor()
model = SentenceTransformer('all-MiniLM-L6-v2')

def evaluate_answer(user_answer, correct_answer):
    # Semantic Similarity
    user_embedding = model.encode(user_answer, convert_to_tensor=True)
    correct_embedding = model.encode(correct_answer, convert_to_tensor=True)
    semantic_similarity = util.pytorch_cos_sim(user_embedding, correct_embedding).item()

    # Concept Matching
    correct_keywords = set([kw[0] for kw in keyword_extractor.extract_keywords(correct_answer)])
    user_keywords = set([kw[0] for kw in keyword_extractor.extract_keywords(user_answer)])
    concept_match_score = len(user_keywords.intersection(correct_keywords)) / len(correct_keywords) if correct_keywords else 0

    # Completeness and Detail Level
    user_doc = nlp(user_answer)
    correct_doc = nlp(correct_answer)
    detail_score = len(user_doc) / len(correct_doc) if len(correct_doc) > 0 else 0

    # Grammar Check
    matches = language_tool.check(user_answer)
    grammar_score = max(0, 100 - 10 * len(matches))  # Adjust penalty per error as needed

    # Adjust scores to a scale of 0-10
    normalized_scores = {
        "Semantic Similarity": min(10, semantic_similarity * 10),
        "Concept Matching": min(10, concept_match_score * 10),
        "Detail Level": min(10, detail_score * 10),
        "Grammar Quality": min(10, grammar_score / 10)  # Normalize to 10
    }

    # Apply a minimum score threshold for very brief answers
    if len(user_answer.strip()) < 10:  # Assuming very brief answers should get a minimum score
        return {key: 1 for key in normalized_scores}

    print(normalized_scores)

    return normalized_scores
