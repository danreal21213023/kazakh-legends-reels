// Episode data for the "English, explained" template (Chat → Notebook).
// Times are seconds. The template's scene timing is fixed; only texts change per episode.
window.EP = {
  "id": "B2-a-vs-an",
  "dur": 36.6,
  "chat": {
    "title": "Tom",
    "msgs": [
      {"from": "me",    "t": 0.30, "text": "I waited a hour for you! 😤"},
      {"typing": [0.95, 1.75]},
      {"from": "other", "t": 1.80, "text": "An hour?! So sorry! 🙈"}
    ]
  },
  "wrong":  {"text": "I waited a hour.", "strike": "a", "strikeAt": 9, "point": "hour", "ghost": "h", "ghostAt": 11, "ghostT": 6.9},
  "why": [
    {"t": 6.0,  "text": "the h is silent: (h)our",  "style": "red"},
    {"t": 7.8,  "text": "vowel SOUND → an",          "style": "red"},
    {"t": 10.2, "text": "әріп емес — дыбыс!",        "style": "kz"}
  ],
  "right": {"text": "I waited an hour."},
  "clock": {"t": 15.6, "x": -240, "y": 800, "r": 62},
  "examples": [
    {"t": 19.8, "text": "She studies at a university.", "sub": "u = “you” sound → a"},
    {"t": 22.2, "text": "He has an MBA.",               "sub": "M = “em” sound → an"}
  ],
  "note": {"t": 24.0, "text": "not: an university"},
  "quiz": {"q": "Quiz time! 🤔 Which is right?", "a": "A) a European city", "b": "B) an European city"},
  "end":  {"title": "English, explained", "kz": "Ағылшын тілі — қарапайым", "cta": "Save it"}
};
