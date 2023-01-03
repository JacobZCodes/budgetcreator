# Jacob Zamore, No Sources
# Needed files outside of this one: mapbox.py; December, 2022.pdf; and README.txt.
from mapbox import find_properties
import os
import time
from reportlab.lib.units import mm
from PyPDF2 import PdfReader
from reportlab.pdfgen.canvas import Canvas

# Practically, I think this program would be something that is run once a month,
# so I want the returned PDF title to be able to dynamically reflect this.
time_tuple = time.localtime(time.time())
year = time.strftime("%Y",time_tuple)
month = time.strftime("%B",time_tuple)

# CHANGE THIS TO WHEREVER YOU HAVE DOWNLOADED THE CARD STATEMENTS PDF.
os.chdir()

# Utilizes PyPDF2 module to read in the card statements pdf.
reader = PdfReader(f'{month}, {year}.pdf')

# Writes PDF to a .txt file
with open('statements.txt', 'w') as my_file:
        for page in range(len(reader.pages)):
            my_file.write(reader.pages[page].extractText())

# This dictionary contains the categories that each expenditure can fall into.
# Within the dictionary, each key has a list value whose first index is another dictionary with a
# 'spent' key. This key's value is originally set to zero but will be updated later on.
types_of_expenditures = {
        'GROCERIES': [{'spent': 0}, 'convenience',
        'groceries', 'grocery', 'market','supermarket',
        'department store','deli'],
    
        'CLOTHES': [{'spent': 0},'apparel'],
    
        'OUT TO EAT': [{'spent': 0},'coffee', 'cafe', 'tea'],
    
        'TRAVEL': [{'spent': 0},'lodging', 'airport'],

        'AUTO': [{'spent': 0},'car repair'],
}

with open('statements.txt') as my_file:
    for line in my_file.readlines():
        # For this program, the only lines I care about have to do with spending money.
        if '$' in line:
            try:
                # Tedious way to parse through each line to find where an
                # expenditure was made.
                line = line.strip().split('$')
                amount_spent = float(line[-1])
                line = line[0].split(':')
                line = line[1].split()
                location = ' '.join(line[1:])
            except:
                continue
            # This try-except block catches an edge case where TOTAL AMOUNT
            # is accidentally being processed (I don't care about the total
            # amount, but rather only each individual expenditure).
            counter = 0
            for descriptor in find_properties(location):
                if counter > 0:
                    break
                for category in types_of_expenditures:
                        if descriptor in types_of_expenditures[category]:
                            types_of_expenditures[category][0]['spent'] += amount_spent
                            # Counter needed here in order to not recount the amount spent at a location.
                            # Without this counter, this loop would keep iterating through each of the 
                            # descriptors in the set returned by the find_properties() function, and 
                            # the 'spent' value would be way too high. I only care about the descriptors
                            # within the returned set insofar as they match to the most likely type of expenditure;
                            # once a match is made, the rest of the descriptors within the properties set can be ignored.
                            counter += 1
                            break
# Rounds out expenditures.           
for key in types_of_expenditures:   
    types_of_expenditures[key][0]['spent'] = round(types_of_expenditures[key][0]['spent'], 2)

"""
START PDF CREATION 
DEFAULT PAGE SIZE IS A4: 210 x 297 mm; (595.2755905511812, 841.8897637795277)
"""
# This function can be improved to make it dynamically react to the number of
# types in types_of_expenditures, but I realized that would then require 
# a dynamically changing height for each type which is a little above my 
# paygrade.
def display(p):
    p.drawString(52.5 * mm, 260 * mm, f"GROCERIES:${types_of_expenditures['GROCERIES'][0]['spent']}")
    p.drawString(52.5 * mm, 235 * mm, f"CLOTHES:${types_of_expenditures['CLOTHES'][0]['spent']}")
    p.drawString(52.5 * mm, 210 * mm, f"OUT TO EAT:${types_of_expenditures['OUT TO EAT'][0]['spent']}")
    p.drawString(52.5 * mm, 185 * mm, f"TRAVEL:${types_of_expenditures['TRAVEL'][0]['spent']}")
    p.drawString(52.5 * mm, 160 * mm, f"AUTO:${types_of_expenditures['AUTO'][0]['spent']}")
    p.save()

my_pdf = Canvas(f'{month}_Expenditures.pdf')
my_pdf.setTitle('Expenditures')
my_pdf.setFont('Times-Italic', 15)
display(my_pdf)









