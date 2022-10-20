
def getSmilesColumn(df):
    """
    Guess the smiles column from a dataframe
    """
    candidateList = ['smiles', 'smiles', 'smiles', 'molecules', 'structures','mols','smi','canonical_smiles','canonicalsmiles']
    smilesColumn = [x for x in df.columns if x.lower() in candidateList]
    if len(smilesColumn) == 0: raise Exception('Could not find smiles column from dataframe, please specify it from the list: {}'.format(df.columns))
    assert len(smilesColumn) == 1, "Dataframe should contain ONLY one smiles column, but found: {}".format(smilesColumn)
    smilesColumn = smilesColumn[0]
    return smilesColumn
