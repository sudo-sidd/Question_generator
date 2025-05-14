import random
import re

def generate_questions_simple(text):
    text = text.replace("\n", " ").strip()
    sentences = re.split(r'(?<=[.!?])\s+', text)
    sentences = [s.strip() for s in sentences if s.strip()]
    
    questions = []
    
    for sentence in sentences:
        if " is " in sentence:
            parts = sentence.split(" is ", 1)
            if len(parts) == 2:
                subject = parts[0].strip()
                predicate = parts[1].strip().rstrip('.?!')
                questions.append(f"What is {predicate}?")
                questions.append(f"Describe {subject}.")
        
        words = sentence.split()
        if len(words) > 5:  
           
            idx = random.randint(1, len(words) - 2)
            blank_word = words[idx]
            if len(blank_word) > 3 and blank_word.lower() not in ['and', 'the', 'that', 'this', 'with']:
                words[idx] = "_______"
                blank_question = " ".join(words)
                questions.append(f"Fill in the blank: {blank_question}")
                
        terms = re.findall(r'\b[A-Z][a-z]+\b', sentence)
        for term in terms:
            questions.append(f"Define the term '{term}'.")
        
        questions.append(f"Explain: {sentence}")
    
    if len(questions) > 10:
        questions = random.sample(questions, 10)
    
    return [f"{i+1}. {q}" for i, q in enumerate(questions)]

def main():
    text = input("Enter the text to generate questions from: ")
    questions = generate_questions_simple(text)
    print("\nGenerated Questions:")
    for question in questions:
        print(question)

if __name__ == "__main__":
    main()
