#!/usr/bin/env python3
def main():
#	from sys import argv
#	argv.pop(0)	

#	for surname in argv:
#		surname.replace(" ", "")
#		print(surname)
#		PyCrawler(surname)

	surnames = SearchSurnames()
	for surname in surnames:
		surname=surname.replace(" ", "")
		surname=surname.replace("\n", "")
		print(surname)
		PyCrawler(surname)	

	print("Finished!")

def PyCrawler(apellido):

    import sqlite3

    bd = sqlite3.connect('paginasblancas.db') #bd = sqlite3.connect(:memory:)

    cursor = bd.cursor()

    cursor.execute("""CREATE TABLE IF NOT EXISTS paginasblancas
                      (Nombre text, Apellido1 text, Apellido2 text, Telefono text PRIMARY KEY, Calle text, CP text, CiudadRegion text) 
                   """)

    pa = apellido1(apellido)
    getInfo(pa, cursor, bd)

    pa = apellido2(apellido)
    getInfo(pa, cursor, bd)

    ## Cambiar el apellido y también hacerlo con la A ##
    apellidoMujer = "".join(apellido + "a")

    pa = apellido1(apellidoMujer)
    getInfo(pa, cursor, bd)

    pa = apellido2(apellidoMujer)
    getInfo(pa, cursor, bd)

    cursor.close()


def apellido1(apellido):

    import requests
    pa = requests.get('http://blancas.paginasamarillas.es/jsp/resultados.jsp?ap1=%s&sec=30&pgpv=1&tbus=0&nomprov=Murcia&idioma=spa' % apellido)
    return pa


def apellido2(apellido):

    import requests
    pa = requests.get('http://blancas.paginasamarillas.es/jsp/resultados.jsp?ap2=%s&sec=30&pgpv=1&tbus=0&nomprov=Murcia&idioma=spa' % apellido)
    return pa


def getInfo(pa,cursor,bd):

    from bs4 import BeautifulSoup

    soup = BeautifulSoup(pa.content, 'html.parser')

    # ## Si se quisiera seguir mirando en las siguientes páginas... ##
    # searchNumber = int(soup.find_all('strong')[11].contents[0])
    #
    # for x in range(math.ceil(searchNumber/10)):
    # ##

    ### BUSCAR NOMBRES ###
    h3 = soup.find_all('h3')

    names = []
    for item in h3:
        names.append(item.contents[-1].strip().replace(u'\xa0\xa0', u' '))
        #print(list(item.children)[1].get_text())

    ### BUSCAR TELÉFONOS ###
    telef = soup.find_all('span', class_='telef')

    telefonos=[]
    for item in telef:
        telefonos.append(item.contents[2][-11:].replace(u' ', u'')) if item.contents[2][-11].isdigit() else "" ## Comprobar si no es un "Otros teléfonos"

    ### BUSCAR DIRECCIÓN COMPLETA ###
    calle = []
    cp = []
    lugar = []
    for item in h3:
        p = item.find_next_sibling('p')
        calle.append(str(p.contents).split("\\t")[1].replace(u"\\r\\n", "").replace(u" ", u"").replace(u"'", u" "))
        cp.append(str(p.contents).split("\t")[5].split("-")[0].replace(u"\xa0", u""))
        lugar.append(",".join(str(p.contents).split("\t")[5].split("-")[1:]).replace(u"\xa0", u"").replace(u"\r\n",u"").replace(u" ", u""))

    for i in range(len(h3)):
        sql="INSERT OR IGNORE INTO paginasblancas VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s')" % ("".join(names[i].split()[:-2]), names[i].split()[-2], names[i].split()[-1], telefonos[i], calle[i], cp[i], lugar[i])
        cursor.execute(sql)

    bd.commit()


def SearchSurnames():
	
	from bs4 import BeautifulSoup
	import requests
	page = requests.get('http://worlduniverse.wikia.com/wiki/Bulgarian_surnames')
	soup = BeautifulSoup(page.content, 'html.parser')

	surnames=[]
	for item in soup.find_all('div', attrs={'id':'mw-content-text'}):
		for li in item.find_all('li'):
			surnames.append(li.text)

#	surnames = []
#	for item in li:
#		surnames.append(item.contents)
		#print()

	return surnames


if __name__ == "__main__":
    main()
