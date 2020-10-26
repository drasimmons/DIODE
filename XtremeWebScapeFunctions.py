# this function scrapes all table data from webpage

def get_data(html):
    data = []
    with urlopen(html) as fp:
        soup = BeautifulSoup(fp, 'html.parser')
        rows = soup.find_all('tr') #Find all table row tags
        for row in rows: #For each row in that tag
            cols = row.find_all('td') #Find all the columns
            cols = [ele.text.strip() for ele in cols]  #Trim the junk off the cols
            data.append([ele if ele else '' for ele in cols])   #Append while ignoring empty vals
    return data


# this function organizes the data from the get_data function
def parse_data(data):
    titles = []
    tables = {}
    for row in data:
        if len(row) == 1:
            current_title = row[0]
            tables[current_title] = []
            titles.append(current_title)
        elif len(row) != 0:
            tables[current_title].append(row)
    return(titles, tables)


# this function places all subtables on a results page into one large table
def get_pandas(titles_in, tables_in):
    for j in range(len(tables_in)):
        for i in range(len(tables_in[titles_in[j]])):
            desc = titles_in[j].split(" / ")
            for string in desc:
                tables_in[titles_in[j]][i].append(string)
        if j==0:
            t = pd.DataFrame(tables_in[titles_in[j]],
                              columns=['Placement','Team','Score','TitleEligibile','Year','Event','Date','Division'])
        else:
            t = t.append(pd.DataFrame(tables_in[titles_in[j]],
                       columns=['Placement','Team','Score','TitleEligibile',
                                'Year','Event','Date','Division']))
    return t


# this function pulls all Xtreme Distance data from Skyhoundz website

def XtremeDist_WebScrape():
    # let's grab html from page listing links to individual year results
    html_outer = urlopen("https://skyhoundz.com/previous-competition-results/")

    # turn it to soup
    soup_outer = BeautifulSoup(html_outer,'html.parser')

    # gather each link containing xtreme distance results
    result_links = []
    for a in soup_outer.find_all('a'):
        if re.search('xtreme-distance-results',a['href']):
            result_links.append(a['href'])

    # the following loop cycles through each url containing results (1 page per year of results)
    # and creates pandas dataframe of all results combined
    for k in range(len(result_links)):

        html_inner = urlopen(result_links[k])
        soup_inner = BeautifulSoup(html_inner,'html.parser')

        data = get_data(result_links[k])
        titles, tables = parse_data(data)

        if k == 0:
            p = get_pandas(titles, tables)
        else:
            p = p.append(get_pandas(titles, tables))

    return p
