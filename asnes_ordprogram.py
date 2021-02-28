# asne_program.py

# Her får jeg inn teksten som skal søkes på:
tekstEllerFil = input("Vil du lime inn tekst, eller laste opp en fil? Tast f for fil, l for lime inn. ")
if tekstEllerFil == "f":
    filBane = input("Hva er det fulle navnet på filen? ")
    tekstFil = open(filBane)
    tekst = tekstFil.read()
    tekstFil.close()
elif tekstEllerFil == "l":
    tekst = input("Lim inn tekst her: ")
else:
    print("Ugyldig input. Avslutter programmet")
    quit()
# Gjør alt til lower-case
tekst = tekst.lower()
# Fjerner linjeskift
tekst = tekst.replace('\xad', '')
tekst = tekst.replace("\n", " ")
# Fjerner ekstra mellomrom:
findDoubleSpaces = tekst.find("  ")
while findDoubleSpaces != -1:
    tekst = tekst.replace("  ", " ")
    findDoubleSpaces = tekst.find("  ")

#Input første søkeord
wordLookUp1 = input("Skriv søkeord her: ")

# Finner et ord å sammenligne med:
wordLookUp2 = input("Tast inn søkestrengen du vil finne i sammenheng med: ")
# Setter parametere for hvor det skal søkes

searchContextBackwardParameter = input("Hvor mange tegn bakover vil du søke? (Press enter for standard, som er 100) ")
if searchContextBackwardParameter == "":
    searchContextBackwardParameter = 100
searchContextBackwardParameter = int(searchContextBackwardParameter)
searchContextForwardParameter = input("Hvor mange tegn forover vil du søke? (Press enter for standard, som er 100) ")
if searchContextForwardParameter == "":
    searchContextForwardParameter = 100
searchContextForwardParameter = int(searchContextForwardParameter)


# Nå skal jeg finne ut om wordLookUp2 finnes i nærheten av wordLookUp1
teller = 0
positionWordEnd = 0
result1 = 0
listeTekst = []
while not (result1 == -1):                                   #-1 betyr ingen funnet
    result1 = tekst.find(wordLookUp1, positionWordEnd)
    # Finner posisjon det skal søkes i;
    searchPositionBackward = result1 - searchContextBackwardParameter
    searchPositionForward = result1 + (len(wordLookUp1)) + searchContextForwardParameter
    # Søker gjennom feltet:
    result2 = tekst.find(wordLookUp2, searchPositionBackward, searchPositionForward)
    if result2 != -1:
        listeTekst.append(tekst[searchPositionBackward:searchPositionForward])
    # Forbereder neste instans
        teller += 1
    positionWordEnd = (result1 + (len(wordLookUp1)))

#  for i in listeTekst:
#     print("\n")
#     print(i)

# svar-rangering = input("Vil du rangere dem etter hvor nærme de er? n = nei, eller tast for å gå videre")
# if svar-rangering != "n":

antallTreff = len(listeTekst)
#print("Antall treff: ", antallTreff)

# Lager ny liste med avstsand mellom de to søkeordene innenfor hvert treff i listeTekst:
antallSorteringer = antallTreff
teller = 0
listeAvstand = []

while antallSorteringer > 0: # Sorterer så mange ganger som det er funnet instanser
    streng = listeTekst[teller]
    posisjon1 = streng.find(wordLookUp1)
    posisjon2 = streng.find(wordLookUp2)
    avstand = posisjon1 - posisjon2
    if avstand < 0:
        avstand = avstand * -1
    listeAvstand.append(avstand)
    teller += 1
    antallSorteringer -=1

# Setter de to listene sammen (streng : verdi)
usortertOrdbok = dict(zip(listeTekst, listeAvstand))

# Sorterer
import operator
# sortertOrdbok = sorted(usortertOrdbok.items(), key=operator.itemgetter(1))
sortertOrdbokListe = sorted(usortertOrdbok.items(), key=lambda kv: kv[1])

# Konverterer tilbake fra liste til ordbok:
import collections
sortertOrdbok = collections.OrderedDict(sortertOrdbokListe)

# Nå skal jeg finne på hvilken side i teksten det er:
listeSidetall = []
for i in sortertOrdbok:
    # Søker på posisjonen til begynnelsen av strengen i dokumentet:
    posisjonStreng = tekst.find(i)
    # Søker på nærmeste instans av "beginning page "
    posisjonBeginningNextPage = tekst.find("beginning of page ", posisjonStreng)
    # Slicer strengen fra beginning page og et par tegn bortover, så jeg ikke trenger å søke igjennom hele teksten.
    slicedStreng = tekst[posisjonBeginningNextPage:(posisjonBeginningNextPage + 25 )]
    # Finner integer:
    import re
    sidetallSøk = re.search(r'\d+', slicedStreng).group()
    sidetall = int(sidetallSøk)
    sidetall -= 1
    listeSidetall.append(sidetall)

# Git output:
highlightSvar = input("Vil du highlighte svarene? Trykk y, eller tast enter for ikke å gjøre det ")
teller = 0
listeOutput = ""
for i in sortertOrdbok:
    outputInt = i
    output = str(outputInt)
    # Fjernet "beginning page" fra strengen, hvis den finnes:
    beginningOfPage = output.find("beginning of page")
    if beginningOfPage:
        output = output.replace("beginning of page ", "")
        # Fjerner sidetall
        sideTallTilFjerningInt = listeSidetall[teller]
        sideTallTilFjerning = str(sideTallTilFjerningInt)
        sideTallTilFjerningFunnet = output.find(sideTallTilFjerning)
        if sideTallTilFjerningFunnet:
            output = output.replace(sideTallTilFjerning, "")
    if highlightSvar == "y":
        wordLookUp1Highlight = "**" + wordLookUp1 + "**"
        wordLookUp2Highlight = "**" + wordLookUp2 + "**"
        output = output.replace(wordLookUp1, wordLookUp1Highlight)
        output = output.replace(wordLookUp2, wordLookUp2Highlight)
    sidetall = listeSidetall[teller]
    sidetall = str(sidetall)
    outputFerdig = "På side " + sidetall + ": " + "\n" + output + "\n\n"
    listeOutput = listeOutput + outputFerdig
    teller += 1

printSvar = input("Hvis du vil ha listen her, trykk h + enter. For å skriver til en fil, trykk f. Den vil bli lagret som output.txt ")
if printSvar == "h":
    print(listeOutput)
if printSvar == "f":
    outputFil = open("output.txt", "w")
    outputFil.write(listeOutput)
    outputFil.close()
else:
    print("Du må trykke h eller f, sorry")
