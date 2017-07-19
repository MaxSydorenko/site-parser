'''
#
'''
from urllib.request import urlopen
from urllib.error import HTTPError
from bs4 import BeautifulSoup
import sqlite3
import time
import datetime
'''
#
'''
def getPages():
    pageURL = "/kiev/list.php?r=101"
    try:
        html = urlopen("http://www.aviso.ua"+pageURL)
    except HTTPError as e:
      return None
    try:
        bsObj = BeautifulSoup(html,"html.parser")
        pages = bsObj.find("ul", {"class":"paginator"}).findAll("a")
    except AttributeError as e:
        return None

    # get max and min page number
    max_page_id = 1
    for tag in pages:
        link = tag.attrs["href"]
        page_number = int(link[link.find("&p=")+3:])
        #print(page_number)
        if max_page_id < page_number:
            max_page_id = page_number

    #print("max = ",max_page_id)

    #prepare link pages set
    i=1
    page_link = {}
    #comment here to test run
    max_page_id = 10
    while i <= max_page_id:
        page_link[i]=("/kiev/list.php?r=101&p="+str(i))
        i=i+1
    #print(page_link.keys())   
    
    return page_link
'''
#
'''
def getAdvertisment(in_pages):

    pages = in_pages
    advertisments = []
    for page in pages:
        pageURL = pages.get(page)
        try:
            html = urlopen("http://www.aviso.ua"+pageURL)
        except HTTPError as e:
          return None
        try:
            bsObj = BeautifulSoup(html,"html.parser")
            adv = bsObj.findAll("a",href = True)
        except AttributeError as e:
            return None

        for tag in adv:
            if tag['href'].find('?adid=') < 0: continue

            #print(tag['href']);
            advertisments.append((0,pageURL,tag['href']))
    #print(advertisments);
    return advertisments
'''
#
'''
def putPagesInDatabase(in_pages):
    pages = in_pages
    conn = sqlite3.connect('avisodb.sqlite')
    cur = conn.cursor()
    cur.execute("DELETE FROM AVISO_PAGE")
    
    sql_command = "INSERT INTO AVISO_PAGE VALUES "
    i=1
    curr_date = time.strftime("%x")
    for page in pages:
        sql_command = sql_command+"("+str(i)+",'"+str(pages.get(i))+"','"+str(curr_date)+"'),"
        i=i+1 
    sql_command = sql_command[0:len(sql_command)-1]
    #print (sql_command)
    cur.execute(sql_command)
    cur.close()
    conn.commit()
    return None
'''
#
'''
def putAdvertsInDatabase(in_adverts):
    adverts = in_adverts;
    #print(adv);
    conn = sqlite3.connect('avisodb.sqlite');
    cur = conn.cursor();
    cur.execute("DELETE FROM AVISO_ADVERTISMENT");
    sql_command = "INSERT INTO AVISO_ADVERTISMENT VALUES ";
    for adv in adverts:
        #print(adv);
        sql_command = sql_command + "(NULL,'"+adv[1]+"','"+adv[2]+"',NULL,NULL),";

    sql_command = sql_command[0:len(sql_command)-1]
    #print(sql_command);
    cur.execute(sql_command)
    cur.close();
    conn.commit();
    return None;
'''
#
'''
def getAdvertismentPage(in_pages,in_advertisments):
    pages = in_pages;
    advertisments = in_advertisments;

    advertisment_pages = [];
    adv_id = 1;

    conn = sqlite3.connect('avisodb.sqlite');
    cur = conn.cursor();
    
    print("########### GETTING ADVERTISMENTS FOR PAGES ###########");
    for page in pages:
        print("Page ID = ",page," page URL = ",pages.get(page));

        # get advertisment link from database on based on page name
        sql_command = "SELECT ADVERTISMENT_LINK FROM AVISO_ADVERTISMENT WHERE PAGE_LINK = '"+pages.get(page)+"'";
        cur.execute(sql_command);
        adv_links = cur.fetchall();        
        #print(page,adv_links);
        for adv_link in adv_links:
            #print(adv_link[0]);
            try:
                html = urlopen(adv_link[0]).read()
            except HTTPError as e:
                  return None
            html = str(html, "utf8")
            html = html.replace(chr(39),chr(34))
            sql_command = "UPDATE AVISO_ADVERTISMENT SET ID = "+str(adv_id)+", ADVERTISMENT_HTML = '''"+html+"''' WHERE ADVERTISMENT_LINK = '"+adv_link[0]+"'";
            cur.execute(sql_command);
            adv_id = adv_id + 1;
        
    print("########### GETTING ADVERTISMENTS FOR PAGES ###########");
    cur.close();
    conn.commit();
    return advertisment_pages;

'''
#
'''

start_time = datetime.datetime.now();
print("## START RUN at",start_time," ##");

pages = getPages()
putPagesInDatabase(pages)

adv = getAdvertisment(pages)
putAdvertsInDatabase(adv)

advp = getAdvertismentPage(pages,adv)

stop_time = datetime.datetime.now();
print("## STOP RUN at",stop_time," ##");
'''
#
'''

'''
#
'''

'''
#
'''

'''
#
'''

'''
#
'''

'''
#
'''






















