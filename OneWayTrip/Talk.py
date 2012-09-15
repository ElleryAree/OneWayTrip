from OneWayTrip.Utils import load_xml
__author__ = 'elleryaree'

class TalkParser(object):
    def parse(self):

        tree = load_xml("dialogs.xml")
        root = tree.getroot()

        chars = {}
        for char_xml in root.iter('char'):
            phrases = {}
            name = char_xml.get("name")
            char = Character(name, char_xml.get("display_name"), phrases)
            chars[name] = char

            for phrase_xml in char_xml.iter('phrase'):
                answers = []
                id = phrase_xml.get("id")
                text = []
                for text_xml in phrase_xml.findall("text"):
                    text.append(text_xml.text)

                phrase = Phrase(id, text, answers)
                item = phrase_xml.get("item")
                if item:
                    phrase.item = int(item)
                cost = phrase_xml.get("cost")
                if cost:
                    phrase.cost = int(cost)
                phrases[int(id)] = phrase

                for answer_xml in phrase_xml.iter('answer'):
                    answer = Answer(int(answer_xml.get("next_id")), answer_xml.find("text").text)
                    required = answer_xml.get("required")
                    if required:
                        answer.required = int(required)
                    answers.append(answer)

        return chars

class Character:
    def __init__(self, name, display_name, phrases):
        self.name = name
        self.display_name = display_name
        self.phrases = phrases

class Phrase:
    def __init__(self, id, text, answers):
        self.id = id
        self.text = text
        self.answers = answers

        self.item = None
        self.cost = None

class Answer:
    def __init__(self, next_id, text):
        self.next_id = next_id
        self.text = text

        self.required = None