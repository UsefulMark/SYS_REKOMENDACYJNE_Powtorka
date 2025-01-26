#Najpopularniejszym pakietem stoowanym w systemach rekomendacyjnych jest pakiet 'surprise'
#Więcej o nim można zanelźć na stronie https://surprise.readthedocs.io/en/stable/index.html

#Pakiet dostarca osobną klasę do przechowywania danych. KLasa nazywa się Dataset
from surprise import Dataset
from surprise import Reader
import pandas as pd

#Pakiet umożliwia automatyczne pobranie jedynie 3 znanych zbiorów danych.
#Po pierwszym wywołaniu komendy program zapyta nas czy chcemy pobrać dane. 
#Jesli potwierdzimy, program pobierze dane i zachowa je w zmiennej.
#Proszę spróbować pobrać jeden z poniższych zbiorów.

#MovieLens 100k
data = Dataset.load_builtin('ml-100k')
#MovieLens 1m
data = Dataset.load_builtin('ml-1m')
#Jester
data = Dataset.load_builtin('jester')

#Teraz aby odczytać konkretne ratingi możemy odwołać się do pola raw_ratings
ratings = data.raw_ratings
#wynikiem jest lista krotek
type(ratings)
type(ratings[0])

#Na ogół będziemy jednak chcieli pracować na własnych danych. W tym celu pakiet umożliwia nam kilka możliwosci,
#jednak wszystkie one wymagają obietu klasy Reader.
#Obiekt ten pozwala sprecyzować różne informacje o danych. Najważniejsze argumenty konstruktora to:
#   - line_format - pozwala okreslić w której kolumnie są informacje o użytkowniku, o produkcie, a w której rating. Domyslna wartosć to 'user item rating' 
#   - sep         - wprzypadku wczytywania danych zpliku okresla sposób rozdzielania kolumn  
#   - rating_scale - Okrela skalę w której są ratingi
#   - skip_lines  - wprzypadku wczytywania danych zpliku okresla ile wierszy ma zostać pominiętych

#Przykład dla DataFrameu
#W tym celu wykorzystamy metodę load_from_df
R = {'id_user': [1, 2, 3, 1, 8, 5, 2],
                'id_item': [2, 3, 2, 12,3, 3, 2],
                'rating':  [3, 5, 2, 1, 5, 5, 3]}
df = pd.DataFrame(R)
reader = Reader(rating_scale=(1, 10))
data = Dataset.load_from_df(df, reader)
data.raw_ratings

#Przykład dla danych z plku
#W tym celu wykorzystamy metodę load_from_file
sciezka = "dane.txt"
reader = Reader(line_format='user item rating', sep=';', rating_scale=(1, 10))
data = Dataset.load_from_file(sciezka, reader)
data.raw_ratings

#Przykład dla danych wczeniej przygotowanych w kilku plikach, najczęsciej stoswany do cross-validacji
#Tu jako pierwszy argument musi być podana lista zawierająca krotki o adresach w kolejnosci dane uczące, dane testowe.
#Obiekt reader w tym przypadku jest taki sam jak poprzednio.
data = Dataset.load_from_folds([('dane_train_1.txt', 'dane_test_1.txt'), ('dane_train_2.txt', 'dane_test_2.txt')], reader)

#Wróćmy do DataFameu
R = {'id_user': [1, 2, 3, 1, 8, 5, 2],
                'id_item': [2, 3, 2, 12,3, 3, 2],
                'rating':  [3, 5, 2, 1, 5, 5, 3]}
df = pd.DataFrame(R)
reader = Reader(rating_scale=(1, 10))
data = Dataset.load_from_df(df, reader)


#Mając dane możemy być zainteresowani wbudowanymi algorytmami ich przewidywań.
#Zgrupowane są w module prediction_algorithms 
import surprise.prediction_algorithms as sp

#AlgoBase
#Jest to klasa po której dziedziczą wszystkie inne algorytmy.
#Dostarcza ona metody:
#compute_baselines - obliczająca prametry używane w innych algorytmach
#compute_similarities - obliczjąca macierz podobieństwa wykorzystywaną przez niektóre algorytmy. Miarę podobieństwa okrela się jako pramtery.
#default_prediction - zwraca wartosć gdy metoda nie pozwala podać swojej prognozy (np. za mało sąsiadów). Zwraca wówczas srednią z ratingów.
#get_neighbors() - zwraca najbliższych sąsziadów. Kogo sąsiedzi mają być  wskazani oraz ilu ich ma być podaje się jako argumenty.
#predict - zwraca progozowany rating. Wymagane parametry to id_użytkownika i id_przedmiotu. Opcjonalnie można podać faktyczny rating (r_ui), czy rating ma zostać liczbą zmiennoprzecinkową, czy przybliżony do skali (clip=True/False)
#test - używana dostesowania działania na zbiorze testowym

#NormalPredictor
#Nadaje ratingi w sposób losowy zakładajac normalnosć rozkładu. Parametry rozkładu obliczane są z danych.
#Tworzymy model
model = sp.random_pred.NormalPredictor()
#Przygotowujemy zbiór danych metodą build_full_trainset()
trainset = data.build_full_trainset()
#Uczymy model
model.fit(trainset )
#Aby uzyskać prognozy dla używkownika u i przdmiotu j wywołujemy metodę predict(u, j)
#Argumenty tej metody muszą być tego samego typu co wczytane dane
#Jeżeli dane tak jak tu wczytywałem z dataframeu gdzie były int-ami, to tu muszą być int-ami.
#Gdym dane wczytywał z pliku musiałby być stringami, np predict('1','2'). Pakiet rozróżnia to jako raw id (te wczytane) i inner ids (niezależnie jak wczytane to są rzutowane na inty)
model.predict(1,2)
#W rezultacie dostajemy obiekt klasy Prediction
#Jeżeli chcemy uzyskać samą prognozę, to odwołujemy się do pola est
model.predict(1,2).est
#Próba kilkukrotnego wywołania tego samego polecenia da różne wyniki. To dlatego, że model ten nadaje prognozy losowo.

#BaselineOnly
#Wystawia tzw baseline ratings, czyli oceną będącą sumą sredniej ze wszystkich ocen, biasów użytkownika i biasu przedmiotu.
#Biasy ustalane są poprzez minimalizaję funkcji starty  
model = sp.baseline_only.BaselineOnly()
model.fit(trainset )
model.predict(1,2)
model.predict(1,2).est
#Tym razem wielkrotne wywołanie da ten sam wynik.

#SlopeOne
#Przewidywana ocena dla przedmiotu j i użytkownika u to srednia z srednich różnich ocen przedmiotów, 
#które zostały ocenione przez użytkownika posiadającego przynajmniej jedną wspólną ocenę z u.
model = sp.slope_one.SlopeOne()
model.fit(trainset )
model.predict('1','2')
model.predict('1','2').est

#KNNBasic
model = sp.knns.KNNBasic()
model.fit(trainset )
model.predict(1,3)
#Wywołanie tej procedury spowoduje wyswietlenie informacji, że niemożne uzyskać ratingu.
#Możemy jednak nadal odwołać się do prognozy, która została zwrócona przez metodę default_prediction 
model.predict(1,3).est
#Paramtery dotyczące miary podobieństwa mają być podawane w postaci słownika
#np.: sim_options = {'name': 'cosine', 'user_based': False}
#Parametry jakie tu okrelamy to:
#name: to nazwa miasry podobieństwa. Dostępne to cosine, pearson, pearson_baseline (to samo co pearson, tylko zamiast srednich używa wyestymowanych wartosci baseline), msd (mean square differences)
#user_based: True to podejscie user-base, False to podejscie item-based
#min_support: ile ocen musi być wspólnych, żeby podobieństwo nie zostało uznane za 0

#Ten algorytm korzysta z macierzy podobieństwa
model.compute_similarities()


#KNNWithMeans
#Wyciąga srednie z poszczególnych wierzy/kolumn, a następnie oblicza podobieństwa odchyleń.
model = sp.knns.KNNWithMeans()
model.fit(trainset )
model.predict(1,3)
model.predict(1,3).est

#KNNWithZScore
#To samo co wyżej, tylko jeszcze rozrzut odchyleń jest zminiejszany, poprzez wydzilenie ich przez odchylenie standardowe wiersza/kolumny
model = sp.knns.KNNWithMeans()
model.fit(trainset )
model.predict(1,3)
model.predict(1,3).est


#KNNBaseline
#To samo co KNNWithMeans tylko srednie są zastąpione wartosciami baseline 
model = sp.knns.KNNBaseline()
model.fit(trainset )
model.predict(1,3)
model.predict(1,3).est

#Matrix factorization
#SVD wersja algorytmu przeznaczona do systemów rekomendacyjnych
#Przewidywany rating to suma sredniej z wszystkich ocen + biaseline urzytkownia + baseline przedmiotu + iloczyn odpowiednich wierszy macierz
#Parametry jakie przyjmuje to:
    #n_factors  - liczba czynników ukrytych
    #n_epochs   - liczba epok przez które będzie optymalizowana funkcja celu
    #biased     -wartosć boolowa. Jesli True to rating wyznaczany jest tak jak opisano powyżej, jeli False to tak jak robilismy na poprzednich zajęciach.
    #i cała masa parametrów związana z regularyzacją poszczególnych elementów
model = sp.matrix_factorization.SVD()
model.fit(trainset )
#Po wykonaniu metody fit mozna odczytać pola:
    #pu - macierz urzytkowników
    #qi - macierz przedmiotów
    #bu - biasy urzytkoników
    #bi - biasy przedmiotów
print(model.pu)
print(model.qi)
print(model.bu)
print(model.bi)
model.predict(1,3)
model.predict(1,3).est

#SVD++
#Wersja SVD uwzględniająca, że nie tylko wartoci ocen upodoniają urzytkowników, ale również to czy oceniali te same przedmioty.
#Parametry jak przy SVD.
model = sp.matrix_factorization.SVDpp()
model.fit(trainset )
#Dodakowo pojawaia się pole yj (implicity item factors)
print(model.yj)
model.predict(1,3)
model.predict(1,3).est

#NMP
#Inny algorytm dekompozycji. Różniż optymalizowany SGD.
#Parametry te same co w SVD.
model = sp.matrix_factorization.NMF()
model.fit(trainset )
model.predict(1,3)
model.predict(1,3).est

#Metody oparte na grupowaniu
#CoClustering
#Algorytm oparty na grupowaniu. Grupowanie odbywa się porzez algorytm k-srednich.
#Parametry:
    #n_cltr_u - liczba klastrów dla użytkoników
    #n_cltr_i
    #n_epochs
model = sp.co_clustering.CoClustering()
model.fit(trainset )
model.predict(1,3)
model.predict(1,3).est

#Ocena modelu
from surprise.model_selection import split as sps
#Podobnie jak w pakiecie sklearn można użyć metod:
    #KFold
    #RepeatedKFold
    #PredefinedKFold
    #ShuffleSplit
    #LeaveOneOut
    #train_test_split

#Dodatkowo można badać model automatycznie dziękifunkcji cross_validate

from surprise.model_selection.validation import cross_validate
#Funkcja ta ma następujące parametry:
    #algo - oceniany model
    #data - obiekt klasy Dataset
    #measures - jaka miara ma być obliczana. Możliwosci to mse, rmse, mae i fcp.
    #cv - w jaki sposób ma być dzielony zbiór. Może to być jedna z metod wspomnianych powyżej, lub liczba całkowita. Jesli jest to liczba to stosowany jest KFold z tą liczbą podziałów.
    #return_train_measures - czy mierzyć dokładnosć na zbiorze uczącym (True/False)

cross_validate(model, data, measures=['MSE', 'MAE'], cv=2)

#W efekcie dostajemy pola test_mse, test_mae, fit_time, test_time

# Zadanie 
# Proszę spróbować zastosować narzędzia z tego pakietu do wygenerowania rekomendacji dla 5 urzytkownika z wybranego przez siebie zbioru danych (jednego z 3 wbudowanych zbiorów). 

