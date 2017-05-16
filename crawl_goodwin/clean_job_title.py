import pandas as pd
from fuzzywuzzy import fuzz
import enchant
# from HTMLParser import HTMLParser
import re
dict_en = enchant.Dict("en_US")


def remove_special_character(word):
	result = ''.join(e for e in word if e.isalnum() or e == ' ')
	result = re.sub('.[!@#$%^&*()]', '', result)
	return result

def remove_after_character(word, special_character):
	below_charactor = word.find(special_character)
	if below_charactor != -1:
		return word[:below_charactor]
	return word

def add_suggest_word_to_dict(original_word, suggest_word):
	""" Add a new word to dictionary. Dictionary will be save at file 'word_not_in_en.csv'
	Input: 
		Original_word: the word need to replace. Ex: Dev., Sr. 
		Suggeest_word: The word use to replace the wrong word: Ex: Developer, Senoir
	"""

	words_not_in_en = pd.read_csv("words_not_in_en.csv")
	words_not_in_en = words_not_in_en.drop('Unnamed: 0', 1)


	word = str.lower(original_word)
	new_words = words_not_in_en[words_not_in_en.word == word].head(1)


	frequency = 0 
	if len(new_words) != 0:
		frequency = words_not_in_en.get_value(new_words.index[0], 'frequency') + 1 
		words_not_in_en.set_value(new_words.index[0], 'frequency', frequency)
		words_not_in_en.set_value(new_words.index[0], 'score', 200)
		words_not_in_en.set_value(new_words.index[0], 'suggest_word', suggest_word)
	else :
		words_not_in_en.loc[len(words_not_in_en)] = [original_word, 0, suggest_word, 200]

	words_not_in_en.to_csv("words_not_in_en.csv")




def standard_job_title(original_job_title, suggest_words_dict):
	# h = HTMLParser()
	job_title_lower_case = str.lower(original_job_title)
	# job_title_remove_unicode = h.unescape(job_title_lower_case)
	job_title_remove_unicode = job_title_lower_case


	suggest_title = job_title_remove_unicode
	original_title = remove_special_character(job_title_remove_unicode)
	
	# Remove all word between "(" and ")"
	open_bracket = suggest_title.find("(")
	close_bracket = suggest_title.find(")") 
	if open_bracket != -1 and close_bracket != -1:
		suggest_title = suggest_title[:open_bracket] + suggest_title[(close_bracket + 1):]
	
	# Remove all word after "/", or "-"
	suggest_title = remove_after_character(suggest_title, "/")
	suggest_title = remove_after_character(suggest_title, "-")

	

	for word in original_title.split():
		wrong_words = suggest_words_dict[suggest_words_dict.word == word].head(1)
		if (len(wrong_words) == 1):

			suggest_word = wrong_words.get_value(wrong_words.index[0], 'suggest_word')
			wrong_word = wrong_words.get_value(wrong_words.index[0], 'word')
			score = wrong_words.get_value(wrong_words.index[0], 'score')


			if score >= 95:
				suggest_title = suggest_title.replace(wrong_word, suggest_word)
   

	score = fuzz.ratio(original_title,suggest_title)
	suggest_title = remove_special_character(suggest_title)
	return (suggest_title, score)  

	
   
