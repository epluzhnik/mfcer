import re
import pycrfsuite
import rutokenizer
import rupostagger
import rulemma

ru_mask = r'[^а-яА-ЯёЁ0-9]'

def clean_text_question(text):
    temp = re.sub(ru_mask, ' ', str(text))
    return " ".join(temp.split())

def ru_lemmatize(text):
    lemmatizer = rulemma.Lemmatizer()
    lemmatizer.load()

    tokenizer = rutokenizer.Tokenizer()
    tokenizer.load()

    tagger = rupostagger.RuPosTagger()
    tagger.load()

    sent = text
    tokens = tokenizer.tokenize(sent)
    tags = tagger.tag(tokens)
    lemmas = lemmatizer.lemmatize(tags)

    lem = []
    for word, tags, lemma, *_ in lemmas:
        lem.append('{}'.format(lemma))

    return " ".join(lem).strip()


def lemmatize(text: str) -> str:
    lover = text.lower()

    clean = clean_text_question(lover)

    lemma = ru_lemmatize(clean)

    return lemma
