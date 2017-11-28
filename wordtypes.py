class WordTypes:
    NOUN = "N"
    VERB = "V"
    ADJECTIVE = "A"
    PRONOUN = "P"
    ADVERB = "R"
    ADPOSITION = "S"
    CONJUCTION = "C"
    NUMERAL = "M"
    PARTICLE = "Q"
    INTERJECTION = "I"
    ABBRECIATION = "Y"
    RESIDUAL = "X"
    PUNCTUATION = "Z"
        
    # word_marks_path specifies relative path of file where marked words are    
    def __init__(self, word_marks_path=None):
        self._word_marks_path = word_marks_path
        self._word_pos_idx = 0
        self._word_original_idx = 1
        self._word_type_idx = 2
        self._word_nominative_idx = 3

    # sentences from which words will be compared in word_mark_path file.
    # wanted word types that will be extracted (nouns, verbs etc) and will contain array of this class's contants
    def get_marked_words_dict(self, sentences_list, word_types):
        with open(self._word_marks_path, "r") as f:
            print(f.readline())
        