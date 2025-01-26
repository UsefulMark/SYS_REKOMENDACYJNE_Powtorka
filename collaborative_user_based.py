import pandas as pd
import numpy as np

#Wczytujemy dane
dane = pd.read_csv('u.data', header=None, sep='	')

#Liczba użytkowników
no_users = len(pd.unique(dane[0]))
#Liczba filmów
no_movies = len(pd.unique(dane[1]))

#Sprawdzamy jakie są największe i najmniejsze wartości id użytkonika i filmu 
dane[0].max()
dane[0].min()
dane[1].max()
dane[1].min()

#Ja wolę pracować na ndarray
dane = dane.values

#Tworzymy tablicę ratingów. Wartość 0 oznacza brak ratingu
R = np.empty((no_users, no_movies))

#Uzupełniamy tablicę ratingów wartościami z wczytanego pliku
for u, m, r, t in dane:
    R[u-1, m-1] = r
    
#Wczytujemy informacje o filmach ograniczając się do id i tytułu
movie_info = pd.read_csv('u.item', usecols=(0,1), header=None, sep='|', 
                         encoding=('latin-1'))

#Tworzymy słownik tłumacząc nr id filmu na jego tytuł
id2name = {}
#Tworzymy słownik tłumacząc index filmu w tablicy R na jego tytuł
row_no2name = {}

#Zmieniamy wartości na ndarray
movie_info = movie_info.values

#uzupełniamy słowniki
for idt, t in movie_info:
    id2name[idt] = t
    row_no2name[idt-1] = t

#Funkcja zwracająca informację o podobieństwie użytkowników z tablicy R
# do podanego użytwkownika
def similarity(user):
    #Lista do przetrzymywania podobieństw użytkowników
    lista = []
    #Pętla po indeksach użytkownikaów 
    for i in range(len(R)): 
        #Do listy dołączamy podobieństwo cosinusowe i index użytkownika
        #Sokoro używamy podobieństwa cosinusowowego to nie ma problemu z kodowaniem brakujących wartości zerami  
        lista.append([np.dot(user, R[i])/ (np.sqrt(np.dot(user, user))* 
                                 np.sqrt(np.dot(R[i], R[i]))), i])
        #Jeden z elementów odległości consinusowej mogłem policzyć przed pętlą.
        #Zasatanów się który.
    return lista

#Funkcja zwracająca podobieństwa i indexy dla k najbardziej podobnych użytkowników
def top_k(user, k=15):
    #Obliczamy podobieństwa dla wszystkich
    temp = similarity(user)
    #Sortujemy tablicę pamiętając, że jest sortowana rosnąco według pierwszej kolumny
    temp.sort()
    #Zwracamy k wartości z końca tablicy, bez ostatniego, który będzie zawsze równy 1.
    return temp[-k-1:-1]

# =============================================================================
# #Alternatywne formy liczenia podobieństw - mało istotne, ale było na zajęciach
# # from sklearn.metrics.pairwise import cosine_similarity
# # cosine_similarity(R, R)
# 
# 
# # def similarity(user):
# #     lista = []
# #     for i in range(len(R)): 
# #         lista.append(np.dot(user, R[i])/ (np.sqrt(np.dot(user, user))* 
# #                                   np.sqrt(np.dot(R[i], R[i]))))
# #     return lista
#     
# # def top_k(user, k=15):
# #     sim = np.array(similarity(user))
# #     temp = np.argsort(sim)
# #     return temp[-k:], sim[temp[-k:]]
# =============================================================================


#Funkcja wyświetlająca rekomendacje
# user - oceny użytkownika dla którego generujemy rekomendacje
# how_many - ile filmów ma być rekomendowanych
# Na podstawie ilu użytkowników ma być nadana rekomendacja
def recommendation(user, how_many = 10, k = 15):
    #Wyznaczamy informacje o k najbardziej podobnych użytkownikach
    most_similar = top_k(user, k)
    #Odczytujemy wartości podobieństw tych użytkowników
    sim = np.array(most_similar)[:,0]
    # i ich indeksy
    indices = np.array(np.array(most_similar)[:,1], dtype=int)
    #Z tablicy R wybieramy wiersze tylko dla wskazanych użytkowników
    sub_R = R[indices]

    #Zmieniamy pdobieństwa na wagi (to nie jest konieczne)
    weights = sim/sum(sim)

    #Tworzymy tablicę dla przewidywanych ratingów    
    pred_ratings = np.zeros(no_movies)

    #Dla każdego filmu z osobna
    for m in range(no_movies):
        #wybieramy ratingi wskazanych użytkoników dla rozważanego filmu
        ratings = sub_R[:,m]
        #Tworzymy tablicę określajacą kto ocenił ten film
        #Ma ona wartości True lub False
        who = sub_R[:,m]>0
        #Sprawdzamy, czy ktokolwiek ocenił ten film
        if sum(who) > 0:
            #Uzupełniamy przewidywany rating dla rozważanego filmu
            #Mnożymy ratingi przez wagi i dzielmy przez sumę wag użytkowników, którzy ocenili ten film
            #Zastosowany if chroni nas przed dzieleniem przez zero
            pred_ratings[m] = sum(ratings*weights)/sum(who*weights)

    #Wszystkie ratingi są uzupełnione. 
    #Nie chcemy proponować filmów już ocenionych przez tego użytkownika, więc zastępujemy ratingi tych filmów zerami     
    pred_ratings[user > 0] = 0

    #argsoet zwraca indeksy sortowania tablicy
    #Ostatnie indeksy wskazują na najwyższe wartości ratingów
    #Wybieramy tyle indeksów ile określiliśmy parametrem funkcji
    #Dodając +1 do indeksów zmieniamy je na id
    for i in np.argsort(pred_ratings)[-how_many:]+1:
        #Wyświetlamy tytuły na podstawie id
        print(id2name[i])

#Tworzę urzytkownika, któremu wyświetlimy rekomendacje
user=R[2]

#Wyświetlamy w konsoli rekomendacje
recommendation(user)

#Definujemy funkcję sprawdzającą na ile obliczone ratingi są zgodne z wskazanymi przez użytkonika
def evaluate(user, how_many, k):
    pass
    print("MSE wyniósł: {:.4f}".format( pass ))
    print("MAE wyniósł: {:.4f}".format( pass ))
    
#Definujemy funkcję sprawdzającą skuteczność metody, jeśli wartości obliczonych ratingów ratingów zaokrąglimy do liczb całkowitych
def evaluate_acc(user, how_many, k):
    pass

# Sprawdź jak algorytm działa na danych ze zbioru uczącego i testowego
# Wypróbuj z różnymi wartościami k









