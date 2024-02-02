#!/usr/bin/env python
# coding: utf-8

# In[1]:


from bs4 import BeautifulSoup
import requests
import pandas as pd
from tkinter import *
import tkinter as tk
from tkinter import filedialog as fd
from tkinter import messagebox

def webscraping():
    data = textbox1.get()
    keyword = textbox2.get()
     
    print("This search will be carried out in the Nature database.")
    print('\n')
    
    url_base =  'https://www.nature.com/search?q=' #default url that will be generated on all searches
    
    material_name = data.replace(' ', '%20') #Swap space for site default character
    
    print('What do you want to search for in the articles? '+data) #base search input
    print("Enter a keyword that you want to know is contained in the articles: "+keyword) #keyword that will judge the articles
    print('Website accessed: ', url_base + material_name) #Link created and accessed
    print('\n')
    print('Below is the list of articles. Data obtained: Title, Authors, DOI, Description, Publication Date, Abstract, Citation, Subjects.')

    url_final = url_base + material_name #Final url
    
    response = requests.get(url_final) #Searching the site

    soup1 = BeautifulSoup(response.text,  'html.parser') #Website content conversion

    quant = soup1.find('span', attrs={'class':"u-display-flex"}).get_text().strip()
    quant_pages= quant[11:13]
    quant_arts= quant[17:].replace(" ", "").replace("results", "")
    
    print('\n')
    print('Number of results for this search: '+ quant)
    print('\n')
    print("______________________________________________________________________________________________________")
    print('\n')

    news_data = []
    
    for i in range(1, int (quant_pages)):
        url_page = url_final + "&page=" + str (i)
        response = requests.get(url_page)

        # Create the BeautifulSoup object
        soup3 = BeautifulSoup(response.content, 'html.parser')
        
        for news_item in soup3.find_all('article', class_='u-full-height c-card c-card--flush'):
            # Extracts the title, author, description, DOI of each article
            info = news_item.find('a', attrs={'class':'c-card__link u-link-inherit'}) #Search for informations
            title = news_item.find('a', attrs={'class':'c-card__link u-link-inherit'}).get_text().strip() #Search by title
            author = news_item.find('ul', attrs={'class':"c-author-list c-author-list--compact c-author-list--truncated"}) #search for authors
            DOI = info['href'] #search for DOI
            description = news_item.find('div', attrs={'class':'c-card__summary u-mb-16 u-hide-sm-max'}) #Search for description
        
            if(title):
                title_article = title
                print('Article Title:', title_article) #Article Title Print
            else:
                title_article = 'Not Found'
                print("Article Title: Not Found.")
            
            print('\n')    
                
            if(author):
                   
                authors_article = author.get_text().strip()
                
                def separate_comma(authors_article):
                    resultado = []
                    palavra_atual = ""

                    for i, char in enumerate(authors_article):
                        if char.isupper():
                            if i > 0 and i < len(authors_article) - 1 and authors_article[i - 1].islower() and authors_article[i + 1].islower():
                                if palavra_atual:
                                    resultado.append(palavra_atual)
                                palavra_atual = char
                            else:
                                palavra_atual += char
                        else:
                            palavra_atual += char

                    if palavra_atual:
                        resultado.append(palavra_atual)

                    return "".join(resultado)                
                
                # Imprimir os elementos separados por vírgula
                elementos_separados = separate_comma(authors_article)              
               
            
                authors_article_separate =  elementos_separados
                print("Authors:")
                    
                print(authors_article_separate) #Print subjects, if there is  
                
            else:
                author = news_item.find('ul', attrs={'class':"c-author-list c-author-list--compact"})#Author search
                if(author):
                    authors_article = author.get_text().strip()
                    
                    def separate_comma(authors_article):
                        resultado = []
                        palavra_atual = ""

                        for i, char in enumerate(authors_article):
                            if char.isupper():
                                if i > 0 and i < len(authors_article) - 1 and authors_article[i - 1].islower() and authors_article[i + 1].islower():
                                    if palavra_atual:
                                        resultado.append(palavra_atual)
                                    palavra_atual = char
                                else:
                                    palavra_atual += char
                            else:
                                palavra_atual += char

                        if palavra_atual:
                            resultado.append(palavra_atual)

                        return "".join(resultado)
                    

                    # Imprimir os elementos separados por vírgula
                    elementos_separados = separate_comma(authors_article)              
               
            
                    authors_article_separate =  elementos_separados
                    print("Authors:")
                    
                    print(authors_article_separate) #Print subjects, if there is
                    
                   
                else:
                    print('Author(s) of the article: Not Found.')
        
            print('\n')        
            
            if(DOI):
                DOI_article = DOI[10:]
                print('DOI of the article: ', DOI_article) #Search for Article Title
            else:
                DOI_article = 'Not Found'
                print("DOI of the article: : Not Found.")
                      
            print('\n')
            
            if(description):
                print("Article Description:" + description.get_text().strip()) #Search for Article Description, if there is.
        
            else:
                print("Article Description: Not Found.")
            
            print('\n')
    
            #Web Scraping on the specific article
    
            url_article = "https://www.nature.com/articles/" + DOI_article.replace(" ", "") #Starts web scraping on the specific article
            
            print("Article Link: " + url_article) #Provide the article link
            print('\n')
            
            response2= requests.get(url_article) #Site search
            soup2 = BeautifulSoup(response2.text, 'html.parser') #Website conversion
            abstract= soup2.find('div', class_="c-article-section__content", id="Abs1-content") #Search for abstract
            citation = soup2.find('p', attrs={'class':"c-bibliographic-information__citation"})
            subjects = soup2.find('ul', attrs={'class':"c-article-subject-list"})#Search for subjects, if there is.
    
            
            if soup2.find('a', attrs={'data-track-action':"publication date"}): #Search for publication date, if there is.
                datepubli= soup2.find('a', attrs={'data-track-action':"publication date"}).get_text().strip()
                date_article = datepubli[11:]
                print("Publication date: " + date_article)
            elif soup2.find('spam', attrs={'class':"time"}):
                datepubli= soup2.find('spam', attrs={'class':"time"}).get_text().strip()
                date_article = datepubli
                print("Publication date: " + date_article)    
            elif soup2.find('ul', attrs={'class':'c-article-identifiers'}):
                datepubli= soup2.find('ul', attrs={'class':'c-article-identifiers'}).get_text().strip().replace("\n","")
                if(datepubli):
                    i = 0
                    while i != len(datepubli):
                        test = datepubli[(i):(i+1)]
                        if (test == '0'):
                            date_article = datepubli[i:]
                            break
                        elif (test == '1'):
                            date_article = datepubli[i:]
                            break
                        elif (test == '2'):
                            date_article = datepubli[i:]
                            break
                        elif (test == '3'):
                            date_article = datepubli[i:]
                            break
                        else:
                            date_article = 'Not Found'
                            i += 1
                    
                    print("Publication date: " + date_article)
                else:
                    date_article = 'Not Found'
                    print("Publication date: " + date_article)
            else: 
                date_article = 'Not Found'
                print("Publication date: " + date_article)
             
            print('\n')    
        
            if(abstract):
                print("Abstract: " + abstract.get_text().strip()) #Print abstract, if there is
            else:
                print("Abstract: Not Found") #Abstract not found
                
            print('\n')
            
            if(citation):
                citation_article = citation.get_text().replace("                    "," ").replace("\n","")
                print("Citation: " + citation_article) #Print citation, if there is
            else:
                citation_article = 'Not Found'
                print("Citation: Not Found") #citation not found
                
            print('\n')
            
            if(subjects): 
                subjects_article = subjects.get_text().strip()
                
                def separate_comma(subjects_article):
                    resultado = []
                    palavra_atual = ""

                    for char in subjects_article:
                        if char.isupper():
                            if palavra_atual:
                                resultado.append(palavra_atual)
                            palavra_atual = char
                        else:
                            palavra_atual += char

                    if palavra_atual:
                        resultado.append(palavra_atual)

                    return ", ".join(resultado)

                # Imprimir os elementos separados por vírgula
                elementos_separados = separate_comma(subjects_article)
                
                
                subjects_article_separate =  elementos_separados
                print("Subjects:")
                
                print(subjects_article_separate) #Print subjects, if there is
                
            else:
                subjects_article_separate = "Not Found"
                print("Subjects: "+ subjects_article_separate) #citation not found
                
            print('\n')
            
            if keyword in soup2.get_text().strip(): #Evaluation if the article has the user's keyword
                print("PROMISING ARTICLE, results were found for "+ keyword+".")
                analysis = "Promising"
            else:
                print("ARTICLE IS NOT PROMISING, no results were found for "+ keyword+".")
                analysis = "Not Promising"
        
            print('\n')
            print("____________________________________________________________________________________________________________________________")
            print('\n')
            
            news_data.append({'Title': title_article,'Subjects': subjects_article_separate, 'DOI': DOI_article, 'Publication Date': date_article,'Link': url_article, 'Citation': citation_article, 'Evaluation': analysis})
       
    # Creating a DataFrame with the collected information
    df = pd.DataFrame(news_data)

    # Displaying the DataFrame
    print(df)
    
    # Saving the DataFrame to an Excel File
    file_name = data+"-"+keyword+".xlsx"
    df.to_excel(file_name, index=False)
    
    #final instructions
    explanation = """
    Your results have been saved as excel (.xlsx)
    in the same folder where the program was run.
    Usually: My computer -> Local Disk -> User
    
    Thank you for using Web Scraping Analysis!""" 
    w1 = tk.Label(window, text=explanation)
    w1.grid(column=2, row=10)

#Graphic Interface    
window = Tk()
window.title("Web Scraping Analysis")
window.geometry("300x300") # dimentions
espace1 = Label(window, text= "")
espace1.grid(column = 1, row = 0)
label1 = Label(text = "What do you want to search for in the Nature articles?") # creates label with this text
label1.grid(column = 2, row = 1)
textbox1 = Entry(text = "") # creates textbox1 where data is entered 
textbox1.grid(column = 2, row = 2)
textbox1["bg"] = "white" # white background 
textbox1["fg"] = "black" # black font
espace2 = Label(window, text= "")
espace2.grid(column = 2, row = 3)
label2 = Label(text = "Enter a keyword: ") # creates label with this text
label2.grid(column = 2, row = 4)
textbox2 = Entry(window) # creates textbox1 where data is entered 
textbox2.grid(column = 2, row = 5)
textbox2["bg"] = "white" # white background 
textbox2["fg"] = "black" # black font

espace3 = Label(window, text= "")
espace3.grid(column = 2, row = 7)
t_guide1 = Label(window, text= "Then, click on the search button:")
t_guide1.grid(column = 2, row = 8)
button = Button(window, text= " Web Scraping ", command = webscraping)
button.grid(column = 2, row = 9)

espace4 = Label(window, text= "")
espace4.grid(column = 2, row = 10)
espace5 = Label(window, text= "")
espace5.grid(column = 2, row = 11)
espace6 = Label(window, text= "")
espace6.grid(column = 2, row = 12)
creator= Label(window, text= "Creator: Willian Alber- Materials Engineer (UFRN)")
creator.grid(column = 2, row = 13)
window.mainloop()


# In[ ]:




