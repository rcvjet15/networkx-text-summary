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
        # mark column indexes in word_marks_path 
        self._word_pos_idx = 0 # word position index column
        self._word_original_idx = 1 # original word column index
        self._word_type_idx = 2 # word type column index
        self._word_nominative_idx = 3 # word as nominative column index

    # sentences from which words will be compared in word_mark_path file.
    # wanted word types that will be extracted (nouns, verbs etc) and will contain array of this class's contants
    def get_marked_words_list(self, sentences_list, word_types):
        
        # will contain lines from self._word_marks_path that contain word that is wanted type in word_types
        filtered_word_marks = list()
        with open(self._word_marks_path, "r") as f:
            for line in f:                
                columns = line.split()                
                # check if cell has content. First letter in cell marks word type
                if len(columns) > 0 and columns[self._word_type_idx] and columns[self._word_type_idx][0] in word_types:
                    filtered_word_marks.append(line)
                    print(line)
        
                   
           
    # filters given line by splitting                
    # def __filter_line_by_types(self, word_types):
        
           
    # def get_words_linked(self, )