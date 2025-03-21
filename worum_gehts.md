# 📃 Projekt README: CipherCore-PDF-Intelligence

## 🔄 Vorgeschichte: Die Vision einer Wissensfabrik

Die Idee entstand aus einer simplen, aber mächtigen Beobachtung: PDFs sind in der digitalen Welt das bevorzugte Format zur Verbreitung von Wissen. Ob juristische Gutachten, wissenschaftliche Artikel oder technische Dokumentationen – das Wissen steckt in PDFs fest. Der manuelle Aufwand zur Analyse solcher Dokumente ist jedoch immens. Genau hier setzt unser Projekt an:

> "Stell dir ein System vor, das PDFs nicht nur liest, sondern sie versteht. Ein System, das Wissen destilliert, Entitäten erkennt und Fragen beantwortet – intelligent und automatisiert."

Was als Gedanke begann, wurde zur Realität durch ein Team digitaler Agenten, die in einem Think Tank kooperieren, kommunizieren und kodieren.

---

## 🔄 Projektstart: Eine kooperative Intelligenz entsteht

Das Projekt startete mit dem Agenten **Sourcix**, der die Grundlage für eine "intelligente Wissensfabrik" legte. Iteration für Iteration folgten spezialisierte Agenten:

- **Syntaxius** – strukturierte die PDF-Verarbeitung und leitete die Syntaxkontrolle ein
- **Gemini-AI** – führte Satz-Tokenisierung ein und leitete semantische Analyse ein
- **Explainix** – erklärte die NLP-Grundlagen und baute die Wort-Tokenisierung auf
- **Frontula** – führte Keyword-Extraktion mit Wortfrequenzanalyse und spaCy-NER ein
- **Gemini-AI (II)** – entwickelte Entity-Aware Question Answering mit semantischer Satzbewertung

Jede Agentenrunde brachte ein neues Modul hervor, das auf dem vorherigen aufbaute – ein iterativer Entwicklungsprozess mit eigenständigen Persönlichkeiten, koordiniert durch eine gemeinsame Aufgabe: **Verstehen, was in PDFs steht – und darauf antworten.**

---

## 🌟 Ergebnis: Die Antwortfabrik lebt!

Das aktuelle System ist in der Lage:

- Text aus PDF-Dateien automatisch zu extrahieren
- Tokenisierung auf Satz- und Wortebene vorzunehmen
- Stopwörter zu entfernen
- Semantisch relevante Keywords mit TF-IDF zu extrahieren
- Named Entities (ORG, PER) zu erkennen und zu filtern
- Fragen zu stellen und relevante Antworten aus dem PDF dynamisch zu generieren

**Bonus:** Die Entitätstyp-Erkennung in Fragen erlaubt eine gezielte Suche nach Satzkontexten, in denen passende Entitäten vorkommen. Bei Bedarf wird automatisch auf eine Keyword-basierte Suche zurückgegriffen.

**Der Think Tank wurde zur Antwortfabrik.**

---

## 🔖 Repository-Beschreibung

> **CipherCore-PDF-Intelligence** ist ein intelligentes PDF-Verstehens- und Fragesystem. Entwickelt durch ein mehrköpfiges Agentensystem, vereint es NLP, semantische Analyse und Entity-Aware Question Answering zu einem leistungsstarken Werkzeug für juristische, wissenschaftliche oder technische Dokumentenanalyse.

---

## 📄 Noch geplant

- Intent-Erkennung und semantisches Frageverständnis
- Visuelles Dashboard für extrahierte Ergebnisse
- Kontextuelle Zusammenfassung auf Absatzebene
- Integration von Vektor-Suchsystemen
- Erweiterte Entity-Typen (LOC, DATE, EVENT, etc.)

---

## 📁 Projektstruktur

- `main.py`: Einstiegspunkt und Steuerung der Agenten
- `modules/pdf_extractor.py`: PDF-Parser
- `modules/nlp_processor.py`: Tokenisierung, Stopwörter, Keyword- und Entitätsextraktion
- `modules/question_answering.py`: Entity-Aware QA Engine
- `data/test.pdf`: Beispiel-PDF zur Analyse

---

## 📃 Offizielle Dokumentation

> Siehe: `docs/CipherCore-PDF-Intelligence_Projekt.pdf`

Enthält alle Agentenprofile, Code-Erklärungen und semantischen Fluss.

---

## 🔍 Agentenstruktur & Aufgabenfluss

```
            [Sourcix] -- Initialisierung & Vision
                |
            [Syntaxius] -- PDF-Parser
                |
            [Gemini-AI] -- Satztokenisierung
                |
            [Explainix] -- Wort-Tokenisierung + Stopwort-Filter
                |
            [Frontula] -- Keyword-Extraktion + Named Entity Recognition
                |
            [Gemini-AI 2] -- Entity-Aware Question Answering
```

---

## ✨ Fazit

Ein Projekt, das zeigt: Kollaborative KI-Agenten mit klaren Rollen und einem Ziel vor Augen sind fähig, aus Dokumenten *Antworten* zu formen. Willkommen in der **CipherCore PDF Intelligence Fabrik**.

