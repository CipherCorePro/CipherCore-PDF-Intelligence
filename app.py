import PyPDF2  # Drittanbieter-Bibliotheken
import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from collections import Counter
from sklearn.feature_extraction.text import TfidfVectorizer
import spacy

# ----------------------------------------------------------------------
# NLP-Modell und Stopwörter laden
# ----------------------------------------------------------------------
try:
    nlp = spacy.load("de_core_news_sm")
except OSError:
    print("Fehler: Das spaCy-Modell 'de_core_news_sm' wurde nicht gefunden.")
    print("Stelle sicher, dass du es mit 'python -m spacy download de_core_news_sm' heruntergeladen hast.")
    exit()  # Beende das Programm, wenn das Modell nicht geladen werden kann

stop_words = set(stopwords.words('german'))  # Stopwörter einmalig laden

# ----------------------------------------------------------------------
# Hilfsfunktionen
# ----------------------------------------------------------------------

def detect_entity_type(question: str) -> str:
    """
    Erkennt den Entitätstyp in einer Frage anhand von Schlüsselwörtern.

    Args:
        question: Die Frage als String.

    Returns:
        Den Entitätstyp als String ("ORG", "PER" oder None).
    """
    org_keywords = ["organisation", "unternehmen", "firma", "institut", "behörde", "verein", "gmbh", "kg", "ag"]
    person_keywords = ["person", "name", "wer", "autor", "sprecher", "mitglied", "chef", "leiter", "direktor", "vorsitzender", "ceo"]

    question_lower = question.lower()
    if any(keyword in question_lower for keyword in org_keywords):
        return "ORG"
    elif any(keyword in question_lower for keyword in person_keywords):
        return "PER"
    return None

# ----------------------------------------------------------------------
# Hauptfunktionen
# ----------------------------------------------------------------------

def process_pdf(pdf_path: str) -> tuple[list, list, list, list]:
    """
    Verarbeitet eine PDF-Datei: Extrahiert Text, führt NLP durch, extrahiert Keywords und Entitäten.

    Args:
        pdf_path: Der Pfad zur PDF-Datei.

    Returns:
        Ein Tupel mit:
        - Liste von (Keyword, TF-IDF-Wert)-Tupeln.
        - Liste von (Entität, Typ, Häufigkeit)-Tupeln.
        - Liste von Sätzen.
        - Liste von gefilterten (Entität, Typ)-Tupeln.
    """

    print(f"Agent Frontula: PDF-Informationen von '{pdf_path}' empfangen, Verarbeitung gestartet...")
    try:
        with open(pdf_path, 'rb') as pdf_file:
            pdf_reader = PyPDF2.PdfReader(pdf_file)
            text = ""
            for page_num in range(len(pdf_reader.pages)):
                page = pdf_reader.pages[page_num]
                text += page.extract_text()
            print("Agent Frontula: Textinhalt aus PDF extrahiert.")

            # Satz-Tokenisierung
            sentences = sent_tokenize(text, language='german')
            print(f"Agent Frontula: Text in {len(sentences)} Sätze zerlegt.")

            # Wort-Tokenisierung, Stopwort-Entfernung und Vorbereitung für TF-IDF
            processed_sentences = []
            for sentence in sentences:
                words = word_tokenize(sentence, language='german')
                words_without_stopwords = [word.lower() for word in words if word.lower() not in stop_words and word.isalnum()]
                processed_sentences.append(" ".join(words_without_stopwords))
            print("Agent Frontula: Wort-Tokenisierung und Stopwort-Entfernung durchgeführt.")

            # TF-IDF Keyword-Extraktion
            vectorizer = TfidfVectorizer()
            tfidf_matrix = vectorizer.fit_transform(processed_sentences)
            word_index_map = vectorizer.vocabulary_
            idf_values = vectorizer.idf_
            index_word_map = {v: k for k, v in word_index_map.items()}
            word_idf_pairs = [(index_word_map[i], idf_values[i]) for i in range(len(idf_values))]
            sorted_word_idf_pairs = sorted(word_idf_pairs, key=lambda x: x[1], reverse=True)
            num_keywords = 10
            keywords = sorted_word_idf_pairs[:num_keywords]
            print(f"Agent Frontula: TF-IDF Keyword-Extraktion durchgeführt. Top {num_keywords} Keywords extrahiert.")

            # Named Entity Recognition (NER)
            doc = nlp(text)
            entities = [(ent.text, ent.label_) for ent in doc.ents]
            print(f"Agent Frontula: Named Entity Recognition durchgeführt. {len(entities)} Entitäten gefunden.")

            # NER-Ergebnisse filtern
            desired_entity_types = ["ORG", "PER"]
            filtered_entities = [ent for ent in entities if ent[1] in desired_entity_types]
            print(f"Agent Frontula: NER-Ergebnisse nach Typ gefiltert. {len(filtered_entities)} Entitäten nach Filterung verblieben.")

            # Entitätenhäufigkeit zählen und sortieren
            entity_counter = Counter(filtered_entities)
            sorted_entities_by_frequency = entity_counter.most_common()
            print(f"Agent Frontula: Entitätenhäufigkeit gezählt und nach Häufigkeit sortiert.")

            return keywords, sorted_entities_by_frequency, sentences, filtered_entities

    except FileNotFoundError:
        print(f"Agent Frontula: Fehler! PDF-Datei '{pdf_path}' nicht gefunden.")
        return [], [], [], []  # Rückgabe leerer Listen im Fehlerfall
    except Exception as e:
        print(f"Agent Frontula: Fehler bei der PDF-Verarbeitung oder NLP: {e}")
        return [], [], [], []  # Rückgabe leerer Listen im Fehlerfall



def answer_question(question: str, keywords: list, sorted_entities: list, sentences: list, filtered_entities: list) -> str:
    """
    Beantwortet eine Frage basierend auf dem extrahierten PDF-Inhalt.

    Args:
        question: Die Frage als String.
        keywords: Liste von (Keyword, TF-IDF-Wert)-Tupeln.
        sorted_entities: Liste von (Entität, Typ, Häufigkeit)-Tupeln.
        sentences: Liste von Sätzen.
        filtered_entities: Liste von gefilterten (Entität, Typ)-Tupeln

    Returns:
        Die Antwort als String.
    """

    print(f"Agent Frontula: Beantworte Frage: '{question}' (Verbesserte Entity-Aware QA)...")

    question_words = [word.lower() for word in word_tokenize(question, language='german') if word.lower() not in stop_words and word.isalnum()]
    entity_prioritized_answer_sentences = []
    keyword_based_answer_sentences = []
    entity_type = detect_entity_type(question)  # Nutze die Hilfsfunktion

    if entity_type:
        print(f"Agent Frontula: Frage zielt auf Entitätstyp: {entity_type}")
        for sentence in sentences:
            sentence_doc = nlp(sentence)
            for ent in sentence_doc.ents:
                if ent.label_ == entity_type:
                    entity_prioritized_answer_sentences.append(sentence)
                    break  # Satz nur einmal hinzufügen

        if entity_prioritized_answer_sentences:
            answer = "\n".join(entity_prioritized_answer_sentences)
            print("Agent Frontula: Antwort basierend auf Entity-Priorisierung gefunden.")
            return answer

    # Fallback zur Keyword-basierten Suche
    print("Agent Frontula: Fallback zu Keyword-basierter Suche...")
    for sentence in sentences:
        sentence_words_lower = [word.lower() for word in word_tokenize(sentence, language='german')]
        for question_word in question_words:
            if question_word in sentence_words_lower:
                keyword_based_answer_sentences.append(sentence)
                break

    if keyword_based_answer_sentences:
        answer = "\n".join(keyword_based_answer_sentences)
        print("Agent Frontula: Antwort basierend auf Keyword-Suche gefunden.")
    else:
        answer = "Agent Frontula: Keine passende Antwort im Dokument gefunden (weder Entity-basiert noch Keyword-basiert)."

    return answer



def wait_for_next_task():
    """Simuliert das Warten auf die nächste Aufgabe."""
    print("Agent Frontula: Warte auf die nächste Aufgabe und Anweisungen...")
    # TODO: Hier Logik zur Aufgabenannahme einfügen (z.B. Eingabeaufforderung)



# ----------------------------------------------------------------------
# Hauptprogramm
# ----------------------------------------------------------------------

if __name__ == "__main__":
    # pdf_path = "pfad/zur/pdf_aus_vorheriger_iteration.pdf"  # TODO: Ersetzen
    pdf_path = input("Bitte gib den Pfad zur PDF-Datei ein: ") # Deutlich besser

    pdf_keywords, sorted_pdf_entities, pdf_sentences, filtered_pdf_entities = process_pdf(pdf_path)

    if pdf_keywords or sorted_pdf_entities or pdf_sentences or filtered_pdf_entities: # Korrekte Prüfung
        # Ausgabe der Keywords (TF-IDF)
        print("\nExtrahierte Keywords (TF-IDF-basiert):")
        for word, tfidf_value in pdf_keywords:
            print(f"- Keyword: {word}, TF-IDF-Wert (vereinfacht IDF): {tfidf_value:.4f}")

        # Ausgabe der Entitäten (NER)
        print("\nGefilterte Entitäten (NER-basiert, nur ORG und PER, sortiert nach Häufigkeit):")
        for (entity, label), frequency in sorted_pdf_entities[:min(10, len(sorted_pdf_entities))]:
            print(f"- Entität: {entity}, Typ: {label}, Häufigkeit: {frequency}")

        # Beispielhafte Fragen
        questions = [
            "Welche Organisationen werden in dem Dokument erwähnt?",
            "Wer sind die Autoren in diesem Dokument?",
            "Was sind die wichtigsten Ergebnisse?",
        ]
        for question in questions:
            answer = answer_question(question, pdf_keywords, sorted_pdf_entities, pdf_sentences, filtered_pdf_entities)
            print(f"\nFrage: {question}")
            print(f"Antwort:\n{answer}")


        wait_for_next_task()
    else:
        print("Agent Frontula: Keine Daten zum verarbeiten")

    print("Agent Frontula: Code-Block abgeschlossen. Übergabe an nächsten Agenten.")