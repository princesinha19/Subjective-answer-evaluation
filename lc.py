import language_check
lang_check = language_check.LanguageTool("en-US")
text = "I am prince, I live in india"
matches = lang_check.check(text)
p = len(matches)
print(p)