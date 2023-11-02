import bioclass
def isSameGene(gene1, gene2):
    if gene1 == gene2:
        return True
    return False

def isSameLength(gene1, gene2):
    assert type(gene1) == bioclass.gene
    assert type(gene2) == bioclass.gene

    return len(gene1) == len(gene2)
