import requests
from bs4 import BeautifulSoup
import bioclass

def nameToId(name, type="gene", retmax=30):
    name = name.replace(" ", "+")
    api_url = f'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db={type}&term={name}&retmax={retmax}&sort=relevance'
    response = requests.get(api_url)

    # Check if the request was successful
    if response.status_code == 200:
        res = []
        soup = BeautifulSoup(response.text, 'xml')
        for id in soup.find_all('Id'):
            res.append(int(id.text))
        return (True, res)
    else:
        return (False, "Error: Failed to retrieve gene's name.")

def idToName(ncbi_id, type="gene"):
    api_url = f"https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi?db={type}&id={ncbi_id}"

    response = requests.get(api_url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'xml')
        name = soup.find('Item', {'Name': 'Title'}).text
        return (True, name)
    else:
        return (False, "Error: Failed to retrieve gene's name.")

def geneSequence(ncbi_id, type="gene"):
    api_url = f"https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db={type}&id={ncbi_id}&rettype=fasta&retmode=text"

    response = requests.get(api_url)

    if response.status_code == 200:
        res = response.text.split("\n")
        code = res[0].split()[0][1:]
        name = ""
        l = res[0].split()[1:]
        for word in l:
            name += word + " "
        res = res[1:]
        res = "".join(res)
        gene = bioclass.gene(code, name, ncbi_id, res)
        return (True, gene)
    else:
        return (False, "Error: Failed to retrieve gene sequence.")
