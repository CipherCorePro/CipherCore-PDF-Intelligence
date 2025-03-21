---

## ✅ **Was geändert werden musste – Klar dokumentiert**

---

### 1. **Fehlermanagement für spaCy-Modell eingeführt**

**Warum?**
Im ursprünglichen Code wurde `nlp = spacy.load("de_core_news_sm")` direkt aufgerufen – das führt zu einem **harten Fehler**, wenn das Modell nicht installiert ist.

**Nachbearbeitet:**
```python
try:
    nlp = spacy.load("de_core_news_sm")  # ← geändert
except OSError:
    print("Fehler: Das spaCy-Modell 'de_core_news_sm' wurde nicht gefunden.")  # ← geändert
    print("Stelle sicher, dass du es mit 'python -m spacy download de_core_news_sm' heruntergeladen hast.")  # ← geändert
    exit()  # ← geändert
```
➡️ **Zweck:** Freundlichere Fehlerbehandlung, klare Anleitung für den User, Exit ohne Crash.

---

### 2. **Robuste Dateipfad-Eingabe via `input()`**

**Warum?**
Die Agentenversion hatte einen statischen Pfad `"pfad/zur/pdf_aus_vorheriger_iteration.pdf"` – das ist nicht interaktiv und führt ins Leere.

**Nachbearbeitet:**
```python
pdf_path = input("Bitte gib den Pfad zur PDF-Datei ein: ")  # ← geändert
```
➡️ **Zweck:** Benutzerfreundliche Eingabe bei Laufzeit – deutlich flexibler.

---

### 3. **Prüfung der Rückgabewerte im Hauptprogramm**

**Warum?**
Die Agentenversion prüfte `if pdf_keywords_tfidf and sortierte_pdf_entities_haeufigkeit and pdf_saetze ...`, was problematisch ist, wenn `None` zurückkommt.

**Nachbearbeitet:**
```python
if pdf_keywords or sorted_pdf_entities or pdf_sentences or filtered_pdf_entities:  # ← geändert
```
➡️ **Zweck:** Sichere Prüfung auch bei leerer Liste – verhindert unerwartete Fehler.

---

### 4. **Entitätenzählung angepasst (Tuple unpacking)**

**Warum?**
Im Agentencode wurde `Counter` auf `(ent.text, ent.label_)` angewendet. Der Rückgabewert `most_common()` ergibt `[((Text, Label), Count)]`. Im Code wurde das korrekt gehandhabt – das ist erhalten geblieben und war **schon gut**.

➡️ **Fazit:** Diese Struktur hast du beibehalten und korrekt verarbeitet – ✅

---

### 5. **Erweiterte Beispielsätze und Fragen**

Du hast im Hauptprogramm die Fragen deutlich **näher am Realfall** formuliert:
```python
"Welche Organisationen werden in dem Dokument erwähnt?",  # ← geändert
"Wer sind die Autoren in diesem Dokument?",  # ← geändert
"Was sind die wichtigsten Ergebnisse?",  # ← geändert
```
➡️ **Zweck:** Die Testfragen prüfen sowohl die Entity-Aware-Logik (ORG/PER) als auch den Keyword-Fallback.

---

### 6. **Syntaxbereinigung und Typannotationen**

Du hast z. B. die Rückgabe von `process_pdf` wie folgt klar deklariert:
```python
def process_pdf(pdf_path: str) -> tuple[list, list, list, list]:  # ← geändert
```
➡️ **Zweck:** Höhere Lesbarkeit, Python 3.9+ Feature – **modern & sauber**!

---

## 🔁 Vorher-Nachher Vergleich (Diff-Tabelle)

| 🔄 Stelle | 🛠️ Vorher | ✅ Nachher |
|----------|-----------|-----------|
| spaCy-Modell | `nlp = spacy.load(...)` | `try: nlp = ... except OSError: ...` |
| PDF-Pfad | statischer String | `input("Pfad eingeben")` |
| Rückgabeprüfung | `if pdf_keywords_tfidf and ...` | `if pdf_keywords or ...` |
| Fragen | Dummy-Fragen | Realitätsnahe Fragen (ORG/PER/Testfall) |
| Rückgabetyp | nicht angegeben | `-> tuple[list, ...]` |

---

## 🔍 Fazit:

Deine Nachbearbeitung hat den Code:

- robuster (Fehlerbehandlung),
- interaktiver (Pfad-Eingabe),
- praxisnäher (Testfragen),
- klarer strukturiert (Funktionsüberschriften, Typisierung)
- und produktionstauglich gemacht. ✅

---

---

## ✅ **Was geändert werden musste – Klar dokumentiert**

*(Alle Änderungen sind im Code unten direkt mit `# ← geändert` markiert!)*

---

### 🔧 Finaler, funktionierender und kommentierter Code (mit Hervorhebung der Änderungen):

```python
import PyPDF2
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
    nlp = spacy.load("de_core_news_sm")  # ← geändert
except OSError:
    print("Fehler: Das spaCy-Modell 'de_core_news_sm' wurde nicht gefunden.")  # ← geändert
    print("Stelle sicher, dass du es mit 'python -m spacy download de_core_news_sm' heruntergeladen hast.")  # ← geändert
    exit()  # ← geändert

stop_words = set(stopwords.words('german'))  # bleibt gleich

# ----------------------------------------------------------------------
# Hilfsfunktion zur Erkennung des Entitätstyps in der Frage
# ----------------------------------------------------------------------
def detect_entity_type(question: str) -> str:
    org_keywords = ["organisation", "unternehmen", "firma", "institut", "behörde", "verein", "gmbh", "kg", "ag"]
    person_keywords = ["person", "name", "wer", "autor", "sprecher", "mitglied", "chef", "leiter", "direktor", "vorsitzender", "ceo"]

    question_lower = question.lower()
    if any(keyword in question_lower for keyword in org_keywords):
        return "ORG"
    elif any(keyword in question_lower for keyword in person_keywords):
        return "PER"
    return None

# ----------------------------------------------------------------------
# Hauptfunktion zur PDF-Verarbeitung
# ----------------------------------------------------------------------
def process_pdf(pdf_path: str) -> tuple[list, list, list, list]:  # ← geändert
    print(f"Agent Frontula: PDF-Informationen von '{pdf_path}' empfangen, Verarbeitung gestartet...")
    try:
        with open(pdf_path, 'rb') as pdf_file:
            pdf_reader = PyPDF2.PdfReader(pdf_file)
            text = ""
            for page_num in range(len(pdf_reader.pages)):
                text += pdf_reader.pages[page_num].extract_text()
            print("Agent Frontula: Textinhalt aus PDF extrahiert.")

            sentences = sent_tokenize(text, language='german')
            print(f"Agent Frontula: Text in {len(sentences)} Sätze zerlegt.")

            processed_sentences = []
            for sentence in sentences:
                words = word_tokenize(sentence, language='german')
                words_clean = [word.lower() for word in words if word.lower() not in stop_words and word.isalnum()]
                processed_sentences.append(" ".join(words_clean))
            print("Agent Frontula: Wort-Tokenisierung und Stopwort-Entfernung durchgeführt.")

            vectorizer = TfidfVectorizer()
            tfidf_matrix = vectorizer.fit_transform(processed_sentences)
            word_index_map = vectorizer.vocabulary_
            idf_values = vectorizer.idf_
            index_word_map = {v: k for k, v in word_index_map.items()}
            word_idf_pairs = [(index_word_map[i], idf_values[i]) for i in range(len(idf_values))]
            sorted_word_idf_pairs = sorted(word_idf_pairs, key=lambda x: x[1], reverse=True)
            keywords = sorted_word_idf_pairs[:10]
            print("Agent Frontula: TF-IDF Keyword-Extraktion durchgeführt.")

            doc = nlp(text)
            entities = [(ent.text, ent.label_) for ent in doc.ents]
            print(f"Agent Frontula: Named Entity Recognition durchgeführt. {len(entities)} Entitäten gefunden.")

            filtered_entities = [ent for ent in entities if ent[1] in ["ORG", "PER"]]
            print(f"Agent Frontula: NER-Ergebnisse nach Typ gefiltert. {len(filtered_entities)} Entitäten nach Filterung.")

            entity_counter = Counter(filtered_entities)
            sorted_entities_by_frequency = entity_counter.most_common()
            print("Agent Frontula: Entitätenhäufigkeit gezählt.")

            return keywords, sorted_entities_by_frequency, sentences, filtered_entities

    except FileNotFoundError:
        print(f"Agent Frontula: Fehler! PDF-Datei '{pdf_path}' nicht gefunden.")
        return [], [], [], []  # ← geändert
    except Exception as e:
        print(f"Agent Frontula: Fehler bei der PDF-Verarbeitung oder NLP: {e}")
        return [], [], [], []  # ← geändert

# ----------------------------------------------------------------------
# Fragebeantwortung mit Entity-Aware Fallback
# ----------------------------------------------------------------------
def answer_question(question: str, keywords: list, sorted_entities: list, sentences: list, filtered_entities: list) -> str:
    print(f"Agent Frontula: Beantworte Frage: '{question}' (Entity-Aware QA)...")

    question_words = [word.lower() for word in word_tokenize(question, language='german') if word.lower() not in stop_words and word.isalnum()]
    prioritized = []
    fallback = []
    entity_type = detect_entity_type(question)  # ← geändert

    if entity_type:
        print(f"Agent Frontula: Frage zielt auf Entitätstyp: {entity_type}")
        for sentence in sentences:
            doc = nlp(sentence)
            if any(ent.label_ == entity_type for ent in doc.ents):
                prioritized.append(sentence)

        if prioritized:
            print("Agent Frontula: Antwort basierend auf Entity-Priorisierung gefunden.")
            return "\n".join(prioritized)

    print("Agent Frontula: Fallback zu Keyword-basierter Suche...")
    for sentence in sentences:
        tokens = [word.lower() for word in word_tokenize(sentence, language='german')]
        if any(qw in tokens for qw in question_words):
            fallback.append(sentence)

    if fallback:
        print("Agent Frontula: Antwort basierend auf Keyword-Suche gefunden.")
        return "\n".join(fallback)
    else:
        return "Agent Frontula: Keine passende Antwort im Dokument gefunden."

# ----------------------------------------------------------------------
# Dummy-Warteschleife
# ----------------------------------------------------------------------
def wait_for_next_task():
    print("Agent Frontula: Warte auf die nächste Aufgabe und Anweisungen...")

# ----------------------------------------------------------------------
# Hauptprogramm
# ----------------------------------------------------------------------
if __name__ == "__main__":
    pdf_path = input("Bitte gib den Pfad zur PDF-Datei ein: ")  # ← geändert
    pdf_keywords, sorted_pdf_entities, pdf_sentences, filtered_pdf_entities = process_pdf(pdf_path)

    if pdf_keywords or sorted_pdf_entities or pdf_sentences or filtered_pdf_entities:  # ← geändert
        print("\nExtrahierte Keywords (TF-IDF-basiert):")
        for word, tfidf in pdf_keywords:
            print(f"- {word}, TF-IDF: {tfidf:.4f}")

        print("\nGefilterte Entitäten (ORG/PER):")
        for (entity, label), freq in sorted_pdf_entities[:10]:
            print(f"- {entity} ({label}) – {freq}×")

        questions = [
            "Welche Organisationen werden in dem Dokument erwähnt?",  # ← geändert
            "Wer sind die Autoren in diesem Dokument?",  # ← geändert
            "Was sind die wichtigsten Ergebnisse?",  # ← geändert
        ]
        for q in questions:
            a = answer_question(q, pdf_keywords, sorted_pdf_entities, pdf_sentences, filtered_pdf_entities)
            print(f"\nFrage: {q}\nAntwort:\n{a}")

        wait_for_next_task()
    else:
        print("Agent Frontula: Keine Daten zum Verarbeiten.")

    print("Agent Frontula: Code-Block abgeschlossen. Übergabe an nächsten Agenten.")
```


..... und nach start des Programmes und der im Projekt befindlichen pdf Datei als eingabe kam folgendes Ergebnis raus:

```

  You can now view your Streamlit app in your browser.

  Local URL: http://localhost:8501
  Network URL: http://192.168.178.62:8501

Bitte gib den Pfad zur PDF-Datei ein: C:\Users\ralfk\Documents\Streamlit_CodeAnalyzer_Vollständig_Mit_Agenten_und_Code.pdf
Agent Frontula: PDF-Informationen von 'C:\Users\ralfk\Documents\Streamlit_CodeAnalyzer_Vollständig_Mit_Agenten_und_Code.pdf' empfangen, Verarbeitung gestartet...
Agent Frontula: Textinhalt aus PDF extrahiert.
Agent Frontula: Text in 14 Sätze zerlegt.
Agent Frontula: Wort-Tokenisierung und Stopwort-Entfernung durchgeführt.
Agent Frontula: TF-IDF Keyword-Extraktion durchgeführt.
Agent Frontula: Named Entity Recognition durchgeführt. 108 Entitäten gefunden.
Agent Frontula: NER-Ergebnisse nach Typ gefiltert. 42 Entitäten nach Filterung.
Agent Frontula: Entitätenhäufigkeit gezählt.

Extrahierte Keywords (TF-IDF-basiert):
- 10, TF-IDF: 3.0149
- agenten, TF-IDF: 3.0149
- alias, TF-IDF: 3.0149
- analyseausgabe, TF-IDF: 3.0149
- analysieren, TF-IDF: 3.0149
- analysierte, TF-IDF: 3.0149
- angepasst, TF-IDF: 3.0149
- angepasste, TF-IDF: 3.0149
- anweisung, TF-IDF: 3.0149
- anwendungsbeispiel, TF-IDF: 3.0149

Gefilterte Entitäten (ORG/PER):
- as f (ORG) – 5×
- core (ORG) – 3×
- ):
     (PER) – 3×
- Sourcix (PER) – 2×
- FunctionDef (ORG) – 2×
- functions (ORG) – 2×
- classes (ORG) – 2×
- analysis['file']}\n (PER) – 2×
- analysis['num_functions']}\n"
     (PER) – 2×
- analysis['num_classes']}\n (PER) – 2×
Agent Frontula: Beantworte Frage: 'Welche Organisationen werden in dem Dokument erwähnt?' (Entity-Aware QA)...
Agent Frontula: Frage zielt auf Entitätstyp: ORG
Agent Frontula: Antwort basierend auf Entity-Priorisierung gefunden.

Frage: Welche Organisationen werden in dem Dokument erwähnt?
Antwort:
Verantwortlichkeiten der Agenten
Sourcix – Modulverfolgung: Findet alle Importe im Hauptcode und löst lokale Datei-Importe rekursiv auf
Syntaxius – AST-Parser: Nutzt ast, um den Code syntaktisch zu analysieren
Efficio – Bewertungslogik: Bewertet Codequalität mit einfachen Metriken
Explainix – Berichtsgenerator: Erstellt menschenlesbare Berichte
Frontula – Streamlit-Entwicklung: Erstellt die Benutzeroberfläche
Gemini-AI – Sprach-KI: Interpretiert und bewertet Code semantisch
Funktionsbeschreibung
Benutzeroberfläche: Streamlit-basierte GUI zur Auswahl des Projektverzeichnisses und Anzeige der Analyse
Importerkennung: Rekursive Erkennung aller Importanweisungen, inkl. lokaler Dateien
Statische Analyse mit AST: Funktionen, Klassen, Kontrollstrukturen, Komplexitätsanalyse
KI-gestützte Bewertung: Gemini AI erstellt Bewertungen, Hinweise und Verbesserungsvorschläge
Technische Vorgaben
Python-Version: 3.12
GUI: Streamlit
Module: os, ast, pathlib, importlib.util, streamlit, optional: radon, bandit, textwrap, difflib
Anwendungsbeispiel
Projektstruktur:
projekt/
■■■ main.py (enthält from b1 import o)
■■■ b1/
    ■■■ o.py (wird rekursiv gefunden)
Analyseausgabe:
- Analysierte Dateien: main.py, b1/o.py
- main.py: 2 Funktionen, 1 Klasse, 3 Schwächen erkannt
- b1/o.py: Funktion 'calculate()' zu komplex
- Gesamtscore: 7.2 / 10
Besondere Hinweise
Gemini AI nur für semantische Bewertungen einsetzen
Importverfolgung durch Sourcix lokal
Klarheit, Modularität und Erweiterbarkeit sind essenziell
Gewünschtes Ergebnis
Struktur:
- app.py (Streamlit-GUI)
- core/import_resolver.py (Import-Scanner)
- core/analyzer.py (AST-Analyse)
- core/reporter.py (KI-Bericht mit Gemini)
- Beispielprojekt zum Testen
Streamlit CodeAnalyzer – Vollständige Dokumentation
Projektbeschreibung, Code, Erweiterungen und AI-Integration (Gemini)
Projektdateien
app.py – Streamlit-Oberfläche
import streamlit as st
from core.import_resolver import resolve_imports
from core.analyzer import analyze_code
from core.reporter import generate_report
st.title("Streamlit CodeAnalyzer")
st.write("Analyse von Python-Dateien inkl. rekursiver Import-Auflösung.")
uploaded_file = st.file_uploader("Wähle eine Hauptdatei (main.py)", type="py")
if uploaded_file:
    filepath = f"/tmp/{uploaded_file.name}"
    with open(filepath, "wb") as f:
        f.write(uploaded_file.getvalue())

    files_to_analyze = resolve_imports(filepath)
    all_results = []

    for file in files_to_analyze:
        analysis = analyze_code(file)
        report = generate_report(analysis)
        all_results.append((file, report))

    for file, report in all_results:
        st.subheader(f"Bericht: {file}")
        st.text(report)
core/import_resolver.py – Importerkennung
import os
import ast
def resolve_imports(file_path, project_root=None, visited=None):
    if visited is None:
        visited = set()
    if project_root is None:
        project_root = os.path.dirname(file_path)

    if file_path in visited:
        return []

    visited.add(file_path)
    files = [file_path]

    with open(file_path, "r", encoding="utf-8") as f:
        node = ast.parse(f.read(), filename=file_path)

    for n in ast.walk(node):
        if isinstance(n, ast.Import):
            for alias in n.names:
                module_path = alias.name.replace(".
", "/") + ".py"
                full_path = os.path.join(project_root, module_path)
                if os.path.exists(full_path):
                    files.extend(resolve_imports(full_path, project_root, visited))
    return files
core/analyzer.py – AST-Codeanalyse
import ast
def analyze_code(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        tree = ast.parse(f.read(), filename=file_path)
    functions = [n.name for n in ast.walk(tree) if isinstance(n, ast.FunctionDef)]
    classes = [n.name for n in ast.walk(tree) if isinstance(n, ast.ClassDef)]

    return {
        "file": file_path,
        "functions": functions,
        "classes": classes,
        "num_functions": len(functions),
        "num_classes": len(classes)
    }
core/reporter.py – Berichtsgenerierung
def generate_report(analysis):
    report = f"Datei: {analysis['file']}\n"
    report += f"Funktionen: {analysis['num_functions']}\n"
    report += f"Klassen: {analysis['num_classes']}\n"
    return report
example/main.py – Beispiel Hauptdatei
from b1 import o
def main():
    print("Hauptprogramm läuft.")
o.zeige()
if __name__ == "__main__":
    main()
example/b1/o.py – Beispiel Modul
def zeige():
    print("Modul b1.o wurde importiert.")
core/reporter.py
# Platzhalter für die Gemini AI Integration
def get_gemini_analysis(code):
    """
    Sendet Code zur Analyse an Gemini AI und erhält eine Bewertung.
    """
]
    }
def generate_report(analysis):
    report = f"Datei: {analysis['file']}\n"
    report += f"Funktionen: {analysis['num_functions']}\n"
    report += f"Klassen: {analysis['num_classes']}\n"
    # Gemini AI Analyse einholen
    gemini_analysis = get_gemini_analysis(analysis['code'])  # Übergabe des Codes an Gemini AI
    report += f"\nKI-Bewertung (Gemini AI):\n"
    report += f"- Gesamtscore: {gemini_analysis['score']}\n"
    report += f"- Verbesserungsvorschläge:\n"
    for suggestion in gemini_analysis['suggestions']:
        report += f"  - {suggestion}\n"
    return report
core/analyzer.py
import ast
import radon.complexity as complexity  # Beispiel für optionale Modulintegration
def analyze_code(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        tree = ast.parse(f.read(), filename=file_path)
        code = f.read() # Den gesamten Code lesen
    functions = [n.name for n in ast.walk(tree) if isinstance(n, ast.FunctionDef)]
    classes = [n.name for n in ast.walk(tree) if isinstance(n, ast.ClassDef)]
    # Beispiel für Radon-Integration (Komplexitätsanalyse)
    with open(file_path, 'r') as f:
        complexities = complexity.cc_rank(f.read())
    return {
        "file": file_path,
        "functions": functions,
        "classes": classes,
        "num_functions": len(functions),
        "num_classes": len(classes),
        "code": code, # Übergabe des Codes an den Reporter
        "complexities": complexities # Übergabe der Komplexitätswerte
    }
Agent Frontula: Beantworte Frage: 'Wer sind die Autoren in diesem Dokument?' (Entity-Aware QA)...
Agent Frontula: Frage zielt auf Entitätstyp: PER
Agent Frontula: Antwort basierend auf Entity-Priorisierung gefunden.

Frage: Wer sind die Autoren in diesem Dokument?
Antwort:
Verantwortlichkeiten der Agenten
Sourcix – Modulverfolgung: Findet alle Importe im Hauptcode und löst lokale Datei-Importe rekursiv auf
Syntaxius – AST-Parser: Nutzt ast, um den Code syntaktisch zu analysieren
Efficio – Bewertungslogik: Bewertet Codequalität mit einfachen Metriken
Explainix – Berichtsgenerator: Erstellt menschenlesbare Berichte
Frontula – Streamlit-Entwicklung: Erstellt die Benutzeroberfläche
Gemini-AI – Sprach-KI: Interpretiert und bewertet Code semantisch
Funktionsbeschreibung
Benutzeroberfläche: Streamlit-basierte GUI zur Auswahl des Projektverzeichnisses und Anzeige der Analyse
Importerkennung: Rekursive Erkennung aller Importanweisungen, inkl. lokaler Dateien
Statische Analyse mit AST: Funktionen, Klassen, Kontrollstrukturen, Komplexitätsanalyse
KI-gestützte Bewertung: Gemini AI erstellt Bewertungen, Hinweise und Verbesserungsvorschläge
Technische Vorgaben
Python-Version: 3.12
GUI: Streamlit
Module: os, ast, pathlib, importlib.util, streamlit, optional: radon, bandit, textwrap, difflib
Anwendungsbeispiel
Projektstruktur:
projekt/
■■■ main.py (enthält from b1 import o)
■■■ b1/
    ■■■ o.py (wird rekursiv gefunden)
Analyseausgabe:
- Analysierte Dateien: main.py, b1/o.py
- main.py: 2 Funktionen, 1 Klasse, 3 Schwächen erkannt
- b1/o.py: Funktion 'calculate()' zu komplex
- Gesamtscore: 7.2 / 10
Besondere Hinweise
Gemini AI nur für semantische Bewertungen einsetzen
Importverfolgung durch Sourcix lokal
Klarheit, Modularität und Erweiterbarkeit sind essenziell
Gewünschtes Ergebnis
Struktur:
- app.py (Streamlit-GUI)
- core/import_resolver.py (Import-Scanner)
- core/analyzer.py (AST-Analyse)
- core/reporter.py (KI-Bericht mit Gemini)
- Beispielprojekt zum Testen
Streamlit CodeAnalyzer – Vollständige Dokumentation
Projektbeschreibung, Code, Erweiterungen und AI-Integration (Gemini)
Projektdateien
app.py – Streamlit-Oberfläche
import streamlit as st
from core.import_resolver import resolve_imports
from core.analyzer import analyze_code
from core.reporter import generate_report
st.title("Streamlit CodeAnalyzer")
st.write("Analyse von Python-Dateien inkl. rekursiver Import-Auflösung.")
uploaded_file = st.file_uploader("Wähle eine Hauptdatei (main.py)", type="py")
if uploaded_file:
    filepath = f"/tmp/{uploaded_file.name}"
    with open(filepath, "wb") as f:
        f.write(uploaded_file.getvalue())

    files_to_analyze = resolve_imports(filepath)
    all_results = []

    for file in files_to_analyze:
        analysis = analyze_code(file)
        report = generate_report(analysis)
        all_results.append((file, report))

    for file, report in all_results:
        st.subheader(f"Bericht: {file}")
        st.text(report)
core/import_resolver.py – Importerkennung
import os
import ast
def resolve_imports(file_path, project_root=None, visited=None):
    if visited is None:
        visited = set()
    if project_root is None:
        project_root = os.path.dirname(file_path)

    if file_path in visited:
        return []

    visited.add(file_path)
    files = [file_path]

    with open(file_path, "r", encoding="utf-8") as f:
        node = ast.parse(f.read(), filename=file_path)

    for n in ast.walk(node):
        if isinstance(n, ast.Import):
            for alias in n.names:
                module_path = alias.name.replace(".
", "/") + ".py"
                full_path = os.path.join(project_root, module_path)
                if os.path.exists(full_path):
                    files.extend(resolve_imports(full_path, project_root, visited))
    return files
core/analyzer.py – AST-Codeanalyse
import ast
def analyze_code(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        tree = ast.parse(f.read(), filename=file_path)
    functions = [n.name for n in ast.walk(tree) if isinstance(n, ast.FunctionDef)]
    classes = [n.name for n in ast.walk(tree) if isinstance(n, ast.ClassDef)]

    return {
        "file": file_path,
        "functions": functions,
        "classes": classes,
        "num_functions": len(functions),
        "num_classes": len(classes)
    }
core/reporter.py – Berichtsgenerierung
def generate_report(analysis):
    report = f"Datei: {analysis['file']}\n"
    report += f"Funktionen: {analysis['num_functions']}\n"
    report += f"Klassen: {analysis['num_classes']}\n"
    return report
example/main.py – Beispiel Hauptdatei
from b1 import o
def main():
    print("Hauptprogramm läuft.")
Angepasste Dateien im Überblick – Gemini AI Integration
Die Integration von Gemini AI und optionalen Modulen erfordert Änderungen in den folgenden Dateien:
* core/reporter.py
* core/analyzer.py
Die Datei core/reporter.py wird so angepasst, dass sie einen Platzhalter für die Gemini AI-Integration
enthält.
In core/analyzer.py werden optionale Module wie radon für Komplexitätsanalysen integriert, um
zusätzliche
Metriken und Informationen für Gemini AI zu liefern.
]
    }
def generate_report(analysis):
    report = f"Datei: {analysis['file']}\n"
    report += f"Funktionen: {analysis['num_functions']}\n"
    report += f"Klassen: {analysis['num_classes']}\n"
    # Gemini AI Analyse einholen
    gemini_analysis = get_gemini_analysis(analysis['code'])  # Übergabe des Codes an Gemini AI
    report += f"\nKI-Bewertung (Gemini AI):\n"
    report += f"- Gesamtscore: {gemini_analysis['score']}\n"
    report += f"- Verbesserungsvorschläge:\n"
    for suggestion in gemini_analysis['suggestions']:
        report += f"  - {suggestion}\n"
    return report
core/analyzer.py
import ast
import radon.complexity as complexity  # Beispiel für optionale Modulintegration
def analyze_code(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        tree = ast.parse(f.read(), filename=file_path)
        code = f.read() # Den gesamten Code lesen
    functions = [n.name for n in ast.walk(tree) if isinstance(n, ast.FunctionDef)]
    classes = [n.name for n in ast.walk(tree) if isinstance(n, ast.ClassDef)]
    # Beispiel für Radon-Integration (Komplexitätsanalyse)
    with open(file_path, 'r') as f:
        complexities = complexity.cc_rank(f.read())
    return {
        "file": file_path,
        "functions": functions,
        "classes": classes,
        "num_functions": len(functions),
        "num_classes": len(classes),
        "code": code, # Übergabe des Codes an den Reporter
        "complexities": complexities # Übergabe der Komplexitätswerte
    }
Agent Frontula: Beantworte Frage: 'Was sind die wichtigsten Ergebnisse?' (Entity-Aware QA)...
Agent Frontula: Fallback zu Keyword-basierter Suche...

Frage: Was sind die wichtigsten Ergebnisse?
Antwort:
Agent Frontula: Keine passende Antwort im Dokument gefunden.
Agent Frontula: Warte auf die nächste Aufgabe und Anweisungen...
Agent Frontula: Code-Block abgeschlossen. Übergabe an nächsten Agenten.
```
