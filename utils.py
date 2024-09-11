import re

def validate_input(email, password, additional_info):
    if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
        return "Invalid email format."
    if len(password) < 6:
        return "Password must be at least 6 characters long."
    if 'full_name' in additional_info and not additional_info['full_name']:
        return "Full name is required."
    return None

def calculate_total_score(mcq_scores, descriptive_scores, weights):
    # Sample debug output
    print("MCQ Scores:", mcq_scores)
    print("Descriptive Scores:", descriptive_scores)
    
    total_mcq_score = sum(mcq_scores.values())  # Adjust according to scoring method
    total_descriptive_score = sum(descriptive_scores.values())  # Adjust according to scoring method
    
    print("Total MCQ Score:", total_mcq_score)
    print("Total Descriptive Score:", total_descriptive_score)
    
    # Apply weights if needed
    weighted_mcq_score = total_mcq_score * weights.get('mcq_weight', 1)
    weighted_descriptive_score = total_descriptive_score * weights.get('descriptive_weight', 1)
    
    total_score = weighted_mcq_score + weighted_descriptive_score
    
    print("Weighted MCQ Score:", weighted_mcq_score)
    print("Weighted Descriptive Score:", weighted_descriptive_score)
    print("Calculated Total Score:", total_score)
    
    return total_score

# Example usage
weights = {'mcq_weight': 1, 'descriptive_weight': 1}
mcq_scores = {2: 1, 1: 1, 6: 1}
descriptive_scores = {7: 209.4703262346285, 8: 122.47946837170112}

calculate_total_score(mcq_scores, descriptive_scores, weights)
