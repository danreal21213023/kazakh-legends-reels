// Episode data for the "English, explained" template (Chat → Notebook).
// Times are seconds. The template's scene timing is fixed; only texts change per episode.
window.EP = {
  "id": "B1-i-agree",
  "dur": 36.6,
  "chat": {
    "title": "Tom",
    "msgs": [
      {"from": "me",    "t": 0.30, "text": "I am agree with you!"},
      {"typing": [0.95, 1.75]},
      {"from": "other", "t": 1.80, "text": "…you are what? 😅"}
    ]
  },
  "wrong":  {"text": "I am agree with you.", "strike": "am", "point": "agree"},
  "why": [
    {"t": 6.0,  "text": "agree is a VERB",           "style": "red"},
    {"t": 7.8,  "text": "→ don't add am / is / are", "style": "red"},
    {"t": 10.2, "text": "agree = келісу (етістік)",  "style": "kz"}
  ],
  "right": {"text": "I agree with you."},
  "examples": [
    {"t": 19.8, "text": "Do you agree?"},
    {"t": 22.2, "text": "She doesn't agree with me."}
  ],
  "note": {"t": 24.0, "text": "not: She isn't agree"},
  "quiz": {"q": "Quiz time! 🤔 Which is right?", "a": "A) I am agree with Tom.", "b": "B) I agree with Tom."},
  "end":  {"title": "English, explained", "kz": "Ағылшын тілі — қарапайым", "cta": "Save it"}
};
