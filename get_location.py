class WordLocator(object):
	''' Word locating object'''
	def __init__(self, words, freq_list):
		self.__words = words
		self.__freq_list = freq_list
		self.__word_locations = []
		self.__avg_locations = []
		self.__total_words = len(words)
		
	
	def get_avg_locations(self):
		for word,freq in self.__word_locations:
			length = len(freq)
			if length > 1:
				total = 0
				for i in range(length-1):
					total += abs(freq[i] - freq[i+1])
				self.__avg_locations.append((word, total/(length-1)))
		return self.__avg_locations


	def get_word_locations(self):
		for v,k in self.__freq_list:
			locations = []
			for i in range(len(self.__words)):
				if (self.__words[i] == v):
					locations.append(i / self.__total_words)
			self.__word_locations.append((v, locations))
		return self.__word_locations
