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
                        
            # if sentence contains only one valid word, add it to node list
            if len(valid_words) == 1:
                self._node_list.append(valid_words[0])
            # sentence contains more than one one valid word, add it to edge list
            else:    
                 # gets edge list as dictionary where preceding word is key and every word after is value
                for linked_words in self.__get_edge_list_for_sentence(valid_words):
                    # if key and value doesn't have same value then add it to edge list. SAmoe word cannot be linked to itself
                    if linked_words[0] != linked_words[1]:
                        self._edge_list.append(linked_words)
                    else:
                        # if key/value are same then add it as node
                        self._node_list.append(linked_words[0])

    # add weights do node list where every time same pair words appear, their weight is incremented by 1.0
    def set_edge_list_as_weighted_edges(self, weight_value = 1.0):
        # temporary list which will containt distinct edge list and 
        # each element will be tuple in format (edge.key, edge.value, weight)
        tmp_weight_list = []
        
        for edge in self.edge_list:
            # flag to test if edge list item is already added to tmp_list
            found = False
            # index of temp item
            tmp_idx = 0
            for tmp_item in tmp_weight_list:
                # if key/value from orig list match with temp list (item is already added to temp list)
                if edge == (tmp_item[0], tmp_item[1]):
                    # tuple objects are immutable so assignment to one element is not possible, 
                    # then whole tuple item must be replaced and weight is incremented by weight_value
                    tmp_weight_list[tmp_idx] = (tmp_item[0], tmp_item[1], tmp_item[2] + weight_value)
                    found = True
                    break
                # increment temp item index if not found
                tmp_idx +=1
            # if edge item is not added to temp list
            if not found:
                # add edge item to temp list with default weight value
                tmp_weight_list.append((edge[0], edge[1], weight_value))
                
        self._edge_list = tmp_weight_list
        print(self._edge_list)
    
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
            