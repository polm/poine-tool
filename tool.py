import streamlit as st

import spacy
import pronouncing
import json

en = spacy.load("en_core_web_sm")

st.title("強弱アクセント判定ツール")

text = st.text_input("入力", "This is a very interesting script.")

def get_syllable_count(text):
    phones = pronouncing.phones_for_word(text)
    # maybe it's not there
    if not phones:
        return -1
    # use the first
    phone = phones[0]
    return pronouncing.syllable_count(phone)

FILLER = 'DET PUNCT AUX ADP PRON'.split()

def get_word_stress(word):
    out = {'word': word.text}
    out['pos'] = word.pos_
    out['syl'] = get_syllable_count(word.text)

    if word.pos_ in FILLER:
        out['stress'] = 'none'
    elif out['syl'] in (-1, 1, 2):
        out['stress'] = 'stress'
    else:
        out['stress'] = 'long'

    return out


doc = en(text)

info = [get_word_stress(word) for word in doc]

st.table(info)

st.markdown("```\n" + json.dumps(info, indent=2) + "\n```")
