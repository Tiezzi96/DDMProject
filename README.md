# DDMProject
Il progetto è stato realizzato per l'esame di Data and Document Mining, appartenente al corso di Laurea Magistrale in Ingegneria Informatica dell'Università degli Studi di Firenze. 

## Idea
L'idea alla base del programma è eseguire una classificazione di documenti sviluppando un algoritmo OCR. Ogni documento appartiene alla banca dati fornita dalla piattaforma [SpringerLink](https://link.springer.com/). Per classificare il documento si fornisce in input al programma il link di riferimento. 

## Installazione dei requisiti
L'algoritmo sviluppato richiede di poter scaricare e leggere sia il file PDF sia il file HTML associato, entrambi ottenuti da SpringerLink. Per il funzionamento del programma è necessario possedere un account SpringerLink o credenziali accademiche.
L'elaborato è un progetto sviluppato nel linguaggio di programmazione **python3.8**. Le librerie utilizzate sono le seguenti:
- [PyMuPDF](https://github.com/pymupdf/PyMuPDF)
- [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)
- [Scikit-Image](https://scikit-image.org/)
- [SymPy](https://www.sympy.org/en/index.html).