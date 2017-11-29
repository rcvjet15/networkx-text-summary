class Dictionary:
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
        
    # dictionary_path specifies relative path of file where marked words are 
    def __init__(self, dictionary_path=None):
        self._dictionary_path = dictionary_path
        # mark column indexes in dictionary_path 
        self._word_pos_idx = 0 # word position index column
        self._word_original_idx = 1 # original word column index
        self._word_type_idx = 2 # word type column index
        self._word_nominative_idx = 3 # word as nominative column index

    # sentences from which words will be compared in dictionary file.
    # wanted word types that will be extracted (nouns, verbs etc) and will contain array of this class's contants
    def get_marked_words_list(self, sentences_list, word_types):
        words_link_dictionary = []
        # current sentence index
        sentence_idx = 0
        # current sentence from text
        current_sentence = sentences_list[sentence_idx]
        # last word position in sentence that is read in dictionary
        last_word_pos = -1
        valid_words = []  
        with open(self._dictionary_path, "r") as f:
            # loop thourgh lines in dictionary
            for line in f:
                # split line into columns
                columns = line.split()
                # if column contains anything                                 
                if len(columns) > 0:
                    # current words position that is read from dictionary
                    current_word_pos = int(columns[self._word_pos_idx])
                    
                    # if current word is after last word that is read
                    if current_word_pos > last_word_pos:
                        # last word read is current word
                        last_word_pos = current_word_pos
                        
                        # check if dictionary word has valid type and sentence contains word from dictionary
                        if self.__is_valid_type(columns, word_types) and self.__sentence_contains(current_sentence, columns):
                            # if word is valid, get it as nominative
                            valid_words.append(columns[self._word_nominative_idx])
                    # if next word is from next sentence in dictionary is reached 
                    else:   
                        # link words between each other where preceeding word is key and word next to it is value
                        # and return dictionary
                        words_link_dictionary.append(self.__get_linked_words(valid_words))
                        
                        last_word_pos = -1
                        # go to next sentence in text
                        sentence_idx += 1
                        
                        if sentence_idx > len(sentences_list) - 1:
                            break
                        
                        # get current sentence in text
                        current_sentence = sentences_list[sentence_idx]
                        # since line is read, check if it word in dictionary is valid type and is in sentence
                        if self.__is_valid_type(columns, word_types) and self.__sentence_contains(current_sentence, columns):
                            valid_words = [columns[self._word_nominative_idx]]
                        else:
                            valid_words = []
                            
        return words_link_dictionary
                
                        
                
       
    def __is_valid_type(self, dictionary_column, wanted_word_types):
        # check if cell has content and check that first letter in cell marks wanted word type
        return (dictionary_column[self._word_type_idx][0] in wanted_word_types)
        
    def __sentence_contains(self, sentence, dictionary_column):
        return (dictionary_column[self._word_original_idx] in sentence.split())
        
    def __get_linked_words(self, words):
        words_dict = []
        
        for i in range(0, len(words) - 2):
            for j in range(i + 1, len(words) - 1):
                words_dict.append((words[i], words[j]))
        return words_dict
            