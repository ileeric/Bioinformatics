class gene:
    def __init__(self, code, fullname, ncbiId, sequence, animal=None):
        self.code = code
        self.fullname = fullname
        self.ncbiId = ncbiId
        self.sequence = sequence
        self.basepair = len(sequence)
        self.animal = animal

    def beautifulString(self):
        if self.animal != None:
            return f"Code: {self.code}\nName: {self.fullname}\nNCBI Code: {self.ncbiId}\nSequence: {self.sequence}\nBasepair: {self.basepair}\nAnimal: {self.animal}"
        else:
            return f"Code: {self.code}\nName: {self.fullname}\nNCBI Code: {self.ncbiId}\nSequence: {self.sequence} ({self.basepair}bp)"

    def __len__(self):
        return self.basepair

    def __eq__(self, gene2):
        assert type(gene2) == gene

        return self.sequence == gene2.sequence

    def __hash__(self):
        return self.fullname
