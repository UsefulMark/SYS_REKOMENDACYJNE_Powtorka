### Łączenie się ze stornami internetowymi.
## W tym celu można skorzystać z pakietu 'urllib'.
## Pakiet ten można zainstalować w condzie poleceniem.
# conda install -c anaconda urllib3
##Podastowe moduły tego pakietu to:
##urllib.request - otwieranie i odczytywanie stron internetowych,
##urllib.error - obsługa wyjątków powstałych w użyciu urllib.request,
##urllib.parse - parsowanie URLów,
##urllib.robotparser do obsługi robots.txt. 
##Nas będzie interesował głównie moduł urllib.request .
##Najważniejsza funkcja w tym pakiecie to urllib.request. 
from urllib.request import urlopen
##Umożliwia ona wykonanie połączenia. Jako parametr musi być podany poprawny 
##adres url w formie stringa, albo klasy Request możliwej do załadowania z tej biblioteki.
##Klasa Request poza adresem umożliwia przesłanie innych informacji, np. nagłówków
##Załóżmy, że chcemy się połaczyć z ze stroną https://kisi.pcz.pl/~pduda/
url ="https://kisi.pcz.pl/~pduda/"
page = urlopen(url) 
##Otrzymana odpowiedź nie jest html-em strony, a obiektem klasy http.client.HTTPResponse
type(page)
##Surowy tekst możemy wydobyć poprzez metodę read
page.read()
##Uwaga jednorazowe wywołanie tej metody zwraca html-a tej strony, a następnie zwalania zasoby.
page.read()
##Aby ponownie odczytać wartoć możemy powtórzyć otwarcie połączenia
page = urlopen(url) 
page.read()
##W pewnych przypadkach możemy chcieć odczytywać stronę w kawałkach. 
##Możemy ograniczyć liczbę wywietlanych bitów (znaków) podając wartoć jako parametr metody read
page = urlopen(url) 
page.read(1) #<
page.read(8) #!DOCTYPE
page.read(1) #
page.read(4) #HTML
page.read(1) #>
##Możemy z obiektu klasy http.client.HTTPResponse odczytać, też inne informacje 
page.getheaders() #lista krotek nagłówek, wartosć
page.url          #adres strony z którą się łączono
page.status       #status połączenia
##Wracając do naszego html-a, aby wywietlić go z użyciem wybranego kodowania użyjemy
##metody decode 
page = urlopen(url) 
html = page.read().decode("utf-8")
##W efekcie została zwrócona zmienna
type(html)
##Możemy ją wywitlić w konsoli
print(html)
##albo zapisać lokalnie w pliku
plik = open("nasz.html", "w")
plik.write(html)
plik.close()
##Po otwarciu pliku w przeglądarce powinna się wywielić zawartosć (bez skryptów i lokalnych odwołań)
##Czasem warto zapsiując plik upewnić się, że kodowanie się zgadza
plik = open("nasz_utf8.html", "w", encoding="utf-8")
plik.write(html)
plik.close()
##Przygotowany ciąg znaków możemy już w wybrany przez nas sposób przetwarzać. 
##Pierwszym ze sposob jest wyszukiwanie odpowiednich fraz w tekcie 
##Jeżeli chcemy wyciąć sekcję head, znajdujemy jej początkową pozycję
start = html.find("<head>")
print(start)
##Następnie końcową 
end = html.find("</head>")
print(end)
##i możemy już wyciąć szukaną sekcję
head = html[start+6:end]
print(head)
##Do zmiennej start dodajemy 6, gdyż jest to długosć tagu '<head>'
##Niepotrzebe znaki, np. białe znaki, możemy usunąć stosując metodę replace
##Należy pamiętać, że zwraca ona nowy obiekt, a nie zmienia tego na, którym jest wykonanywana.
head = head.replace('\t','')
head = head.replace('\r','')
head = head.replace('\n','')
print(head)

##Wygodniejszą alternatywą do wyszukiwania w tekscie interesujących nas elementów
## są wyrażenia regularne
##Pakiet do ich obsługi powinien być domylnie zainstalowany, ale w razie czego używamy polecenia
#conda install -c conda-forge regex
##Pakiet importujemy 
import re
##Więcej o wyrażeniach regularnych można znalesć na https://docs.python.org/3/library/re.html
##Jeżeli chcemy wyszukać wszystkie elemty img możemy posłużyć się następującym wzorcem <img (.*?)/>
img = re.findall(r'<img (.*?)/>', html, 0)
## <img -to znaki, które muszą być zawarte na poczatku wyszukanego wyrażenia
## (.*?) - () oznacza, że interesuje nas to co znajdzie się wewnątrz tego nawiasu
## (.*?) - . oznacza dowolny znak poza znakiem nowej linii
## (.*?) - * oznacza dwolną dopuszczalną liczba powtórzeń znaku poprzedzającego ten znak
## (.*?) - ? oznacza, że znak poprzedzającey ten znak zapytania może pojawić się zero razy lub raz.
##W efekcie otrzymalimy listę instancji spełniających nasz wzorzec
##Teraz w łatwy sposób możemy wypisać wszystkie adresy obrazów
for i in img:
    print(re.findall(r'src=\"(.*?)\"', i, 0))

## Jeżeli chcemy równoczesnie sprawdzić kilka warunków to możemy odwołać się do nich poprzez kilka warunków umieszczonych w ()
## W efekcie otrzymujemy listę, której elementami są krotki. 
## Wartosć w każdej z krotek to kolejne wyszukania z grup.
img = re.findall(r'<img src="(.*?)\" style=\"(.*?)\".*?/>', html, 0)

##Alternatywnie do findall możemy zastosować finditer. W efekcie wyniki nie będą 
## przechowywane w całoci w pamięci, a krotkami, każde osobne wystąpnienie. 
for r in re.finditer(r'<img (.*?)/>', html, 0):
    print(r.group())    

##Najwygodniejszą z opcji może okazać się korzystanie z biblioteki przeznaczonej do parsowania stron www.
##Jedną z najpopularniejszych bibliotek jest BeautifulSoup.
##Jeżeli nie została wczesnij zainstalowana, to będzie to można zrobić poleceniem
#conda install -c anaconda beautifulsoup4
#Więcej na https://www.crummy.com/software/BeautifulSoup/bs4/doc
from bs4 import BeautifulSoup
##Tworzymy obiekt, gdzie jako pierwszy parametr podajemy stringa, który chcemy przeszukiwać,
## a jako drugi typ parsera (dla nas nie istotny w tej chwili; inne możliwosci to: 'xml', 'lxml', 'html5lib') 
soup = BeautifulSoup(html, "html.parser")
##Aby wywietlić całą zawartosć obiektu można skorzystać z metody get_text
print(soup.get_text())
##Jeżeli chcemy odwołać się kluczowych tagów możemy to zrobić w następujący sposób
soup.title
##Jest to obiekt typu bs4.element.Tag
type(soup.title)
##Jeżeli chcemy odczytac jego zawartosć to wpisujemy
soup.title.string
##Możemy chcieć się też poruszać po drzewie DOM.
soup.title.parent
##Zwraca cały tag w którym title było zawarte.
##Jeżeli chcemy się odwołać do dzieci dostaniemy iterator wskazujący na nie
soup.head.children
for s in soup.head.children:
    print(s)
##Próba odwołania się od wybranego tagu, np. img, spwoduje odwołanie się pierwszego wystąpienia.
soup.img
##Aby odczytać atrybut wewnątrz tagu można odwołać się jak do słownika
soup.img['src']
##Jeżeli chcemy wybrać wszystkie tagi img można skorzystać z metody find_all
ff = soup.find_all("img")
##Elementy listy nie są stringami a obiektami klasy  bs4.element.Tag
image = ff[0]
type(image)
##Aby sprawdzić jakiego rodzaju jest dany tag możemy się odwołać do pola name
image.name
##Do wartosci atrybutu odwołujemy się analogicznie jak poprzednio. 
image["src"]
##Jeżeli chcemy ograniczyć się do obiektów dane klasy, mozemy to zrobić w metodzie find_all
divy = soup.find_all("div", class_="hexIn", recursive=True)
divy[0] 
divy[1]
divy[2]
##Przetwarzając strony możemy często natknąć się na sytuację, gdzie serwer wymaga przerwy pomiędzy kolejnymi zapytaniami.
##Można wtedy użyć
import time
time.sleep(3)



