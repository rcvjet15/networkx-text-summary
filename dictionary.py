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
    
    @property
    def node_list(self):
        return self._node_list
        
    @property
    def edge_list(self):
        return self._edge_list
        
    # dictionary_path specifies relative path of file where marked words are 
    def __init__(self, dictionary_path=None):
        self._dictionary_path = dictionary_path
        # mark column indexes in dictionary_path 
        self._word_pos_idx = 0 # word position index column
        self._word_original_idx = 1 # original word column index
        self._word_type_idx = 2 # word type column index
        self._word_nominative_idx = 3 # word as nominative column index
        self._node_list = []
        self._edge_list = []
    
    # sentences from which words will be compared in dictionary file.
    # wanted word types contains array of wanted types that will be extracted (nouns, verbs etc)
    def set_words_as_node_and_egde_list(self, sentences_list, word_types):
        words_link_dictionary = []
        
        # it will be 2d array where each element will contain array of words for sentence
        filtered_sentences = []
        
        dictionary_lines = None
        with open(self._dictionary_path, "r", encoding="utf-8", errors = "ignore") as f:
            # read all dictionary
            dictionary_lines = f.readlines()
        
        # loop through sentences in text
        for sentence in sentences_list:
            # list that will store words that are found in dictionary and are valid type
            valid_words = []
            # loop thourhg each word in sentence text
            for word in sentence.split():
                # search for word in dictionary by looping through each line                    
                for dict_line in dictionary_lines:
                    
                    # split dictionary line into columns
                    columns = dict_line.split()
                    
                    # if column contains anything                                 
                    if len(columns) > 0:
                        # check if dictionary word has valid type and sentence contains word from dictionary
                        if self.__is_valid_type(columns, word_types) and word == columns[self._word_original_idx]:
                            # if word is valid, get it as nominative from dictionary
                            valid_words.append(columns[self._word_nominative_idx])   
                            break            
            # add to 2d array of valid words         
            filtered_sentences.append(valid_words)
        
        # looop through each filtered sentence
        for filtered_sentence in filtered_sentences:
            # if sentence contains only one valid word, add it to node list
            if (len(filtered_sentence) == 1):
                self._node_list.append(filtered_sentence[0])
            # sentence contains more than one one valid word, add it to edge list
            else:
                # gets edge list as dictionary where preceding word is key and every word after is value
                for linked_words in self.__get_edge_list_for_sentence(filtered_sentence):
                    self._edge_list.append(linked_words)
                    
        return words_link_dictionary
                          
       
    def __is_valid_type(self, dictionary_column, wanted_word_types):
        # check if cell has content and check that first letter in cell marks wanted word type
        return (dictionary_column[self._word_type_idx][0] in wanted_word_types)
        
    def __sentence_contains(self, sentence, dictionary_column):
        return (dictionary_column[self._word_original_idx] in sentence.split())
        
    def __get_edge_list_for_sentence(self, words):
        edge_dict = []
        
        for i in range(0, len(words) - 2):
            for j in range(i + 1, len(words) - 1):
                edge_dict.append((words[i], words[j]))
                
        return edge_dict
            