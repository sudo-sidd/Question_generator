import nltk
import random
import os
from nltk import word_tokenize, sent_tokenize, pos_tag, ne_chunk
from nltk.tree import Tree

# Set up NLTK data path
nltk_data_path = "/mnt/data/PROJECTS/Question_generator/nltk_data"
os.makedirs(nltk_data_path, exist_ok=True)
nltk.data.path.append(nltk_data_path)

# Download required NLTK resources
resources = ['punkt', 'averaged_perceptron_tagger', 'averaged_perceptron_tagger_eng', 'maxent_ne_chunker', 'maxent_ne_chunker_tab', 'words']
for resource in resources:
    try:
        nltk.download(resource, download_dir=nltk_data_path, quiet=True)
    except Exception as e:
        print(f"Failed to download {resource}: {e}")
        exit(1)

# Define common stopwords
stopwords = {'a', 'an', 'the', 'and', 'or', 'but', 'if', 'because', 'as', 'what',
             'while', 'of', 'at', 'by', 'for', 'with', 'about', 'against', 'between',
             'into', 'through', 'during', 'before', 'after', 'above', 'below', 'to',
             'from', 'up', 'down', 'in', 'out', 'on', 'off', 'over', 'under', 'again',
             'then', 'once', 'here', 'there', 'when', 'where', 'why', 'how', 'all',
             'any', 'both', 'each', 'few', 'more', 'most', 'other', 'some', 'such',
             'no', 'nor', 'not', 'only', 'own', 'same', 'so', 'than', 'too', 'very',
             'can', 'will', 'just', 'should', 'now'}

# Section headers to ignore
section_headers = {'key', 'features', 'causes', 'aftermath', 'survivors', 'significance', 'summary'}

def extract_entities(sentence):
    words = word_tokenize(sentence)
    try:
        pos_tags = pos_tag(words, lang='eng')
    except:
        pos_tags = [(word, 'NN') for word in words]
    
    try:
        tree = ne_chunk(pos_tags)
    except:
        entities = {'PERSON': [], 'ORGANIZATION': [], 'LOCATION': [], 'DATE': [], 'GPE': []}
        for i, (word, tag) in enumerate(pos_tags):
            if tag == 'NNP':
                entity = word
                j = i + 1
                while j < len(pos_tags) and pos_tags[j][1] == 'NNP':
                    entity += " " + pos_tags[j][0]
                    j += 1
                if "million" in sentence.lower() and "ago" in sentence.lower():
                    entities['DATE'].append(entity)
                elif any(loc_word in entity.lower() for loc_word in ['peninsula', 'crater', 'india', 'mexico']):
                    entities['GPE'].append(entity)
                else:
                    entities['PERSON'].append(entity)
        return entities
    
    entities = {'PERSON': [], 'ORGANIZATION': [], 'LOCATION': [], 'DATE': [], 'GPE': []}
    for subtree in tree:
        if isinstance(subtree, Tree):
            entity_type = subtree.label()
            entity_name = " ".join([word for word, tag in subtree.leaves()])
            if entity_type in entities:
                entities[entity_type].append(entity_name)
    
    return entities

def extract_key_terms(sentence):
    words = word_tokenize(sentence)
    try:
        pos_tags = pos_tag(words, lang='eng')
    except:
        pos_tags = [(word, 'NN') for word in words]
    
    key_terms = []
    for word, tag in pos_tags:
        if (tag.startswith('NN') and len(word) > 3 and word.lower() not in stopwords and 
            word.lower() not in section_headers):
            key_terms.append(word)
            
    return key_terms

def generate_fill_in_blank(sentence):
    questions = []
    words = word_tokenize(sentence)
    try:
        pos_tags = pos_tag(words, lang='eng')
    except:
        pos_tags = [(word, 'NN') for word in words]
    
    for i, (word, tag) in enumerate(pos_tags):
        if (tag.startswith('NN') and len(word) > 3 and word.lower() not in stopwords and 
            word.lower() not in section_headers):
            blanked_words = words.copy()
            blanked_words[i] = "_______"
            blanked_sentence = " ".join(blanked_words)
            questions.append(f"Fill in the blank: {blanked_sentence}")
            break
    
    return questions

def generate_definition_questions(sentence):
    questions = []
    key_terms = extract_key_terms(sentence)
    
    for term in key_terms:
        if term[0].isupper() and term.lower() not in stopwords and term.lower() not in section_headers:
            questions.append(f"What is meant by {term} in the context of the KT extinction?")
    
    return list(set(questions))

def generate_true_false(sentence):
    questions = []
    true_statement = sentence.rstrip('.?!') + "."
    questions.append(f"True or False: {true_statement}")
    
    words = word_tokenize(sentence)
    try:
        pos_tags = pos_tag(words, lang='eng')
    except:
        pos_tags = [(word, 'NN') for word in words]
    
    for i, (word, tag) in enumerate(pos_tags):
        if tag.startswith('VB') and word.lower() in ['eliminated', 'survived', 'caused', 'included']:
            false_words = words.copy()
            false_words[i] = "not " + false_words[i]
            false_statement = " ".join(false_words).rstrip('.?!') + "."
            questions.append(f"True or False: {false_statement}")
            break
    
    return questions

def generate_all_questions(text, max_questions=10):
    sentences = sent_tokenize(text)
    all_questions = []
    
    for sentence in sentences:
        if len(word_tokenize(sentence)) < 5:
            continue
            
        blanks = generate_fill_in_blank(sentence)
        definitions = generate_definition_questions(sentence)
        true_false = generate_true_false(sentence)
        
        all_questions.extend([("Definition", q) for q in definitions])
        all_questions.extend([("Fill-in-blank", q) for q in blanks])
        all_questions.extend([("True/False", q) for q in true_false])
    
    # Remove duplicates
    seen_questions = set()
    unique_questions = []
    for q_type, q in all_questions:
        if q not in seen_questions:
            seen_questions.add(q)
            unique_questions.append((q_type, q))
    
    random.shuffle(unique_questions)
    if len(unique_questions) > max_questions:
        unique_questions = unique_questions[:max_questions]
    
    questions_by_type = {}
    for q_type, q in unique_questions:
        if q_type not in questions_by_type:
            questions_by_type[q_type] = []
        questions_by_type[q_type].append(q)
    
    return questions_by_type

def main():
    print("Question Generator using NLTK")
    print("-----------------------------")
    print("Enter your text below. Type 'exit' on a new line when done.")
    
    lines = []
    while True:
        line = input()
        if line.lower() == 'exit':
            break
        lines.append(line)
    
    text = ' '.join(lines)
    
    if not text.strip():
        print("No text entered. Exiting.")
        return
    
    print("\nGenerating questions...\n")
    questions = generate_all_questions(text)
    
    for i, (q_type, q_list) in enumerate(questions.items()):
        print(f"\n{q_type} Questions:")
        print("-" * (len(q_type) + 10))
        for j, question in enumerate(q_list):
            print(f"{j+1}. {question}")
    
    total_questions = sum(len(q_list) for q_list in questions.values())
    print(f"\nGenerated {total_questions} questions across {len(questions)} question types.")

if __name__ == "__main__":
    main()