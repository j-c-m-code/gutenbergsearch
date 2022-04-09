# <codecell>
import csv
import unicodedata

test_char = "\u00e9"  # LATIN SMALL LETTER E WITH ACUTE

print(test_char)  # prints correctly

with open("test.csv", "w", newline="", encoding="UTF-8") as file:
    writer = csv.writer(file)
    writer.writerow(test_char)

# when I open test.csv in Atom, I see the correct character
# but when I open test.csv in Excel on Windows 10, I see these two characters:

unicodedata.name("Ã")  # LATIN CAPITAL LETTER A WITH TILDE
unicodedata.name("©")  # COYRIGHT SIGN
