# CIR:CyCif Antibody Integration With RNA-Seq



#Purpose: Identify CyCif Antibodies that work from the differentially expressed RNA-Seq results
#Version: 0.0.1
#Input (currently hard coded):
# 1) Ensembl Gene/Transcript Mapping
# 2) Zoltan's list of CyCif Antibodies
# 3) List of RNA-Seq results (by using file format for list of DE genes/transcripts
#Program Overview:
# PART 1: QC
    # 1) QC checks ie search all CyCif Antibodes with Ensembl names to check if possible [TODO: currently filtering CyCif Antibody list by antibody column name, if change will break]
    # 2) Add Ensemble (ENSG...) unique id for each CyCif Antibody (multiple Ensembl ids for one gene name)
    # 3) NOT IMPLEMENTED, for gene names not found from CyCif, search for alternative names [TODO]
        # - use (https://biodbnet-abcc.ncifcrf.gov/db/db2db.php) to select
        # - alternatively download and make DB of possibles for local run without internet
# PART 2: RNA-Seq DEG & CyCif Selection
    # 1) For each file of DEG output, output all CyCif results
    # 2) NOT IMPLEMENTED: Produce each round of CyCif
    # 2) NOT IMPLEMENTED: consider any rules needed from Zoltan such as fluorensence or species that can
# PART 3: Merge CyCif Panel: Assumption is there will be a panel for each DEG list, but one comprehensive list representing all targets of interest
# 1) Take all results from PART 1 and top X
# PART 4: Graphical Summary & Output
# PART 5: Integrate a likelihood metric of RNA & Protein expression correlation ie if DEG will == protein?
#1) NOT IMPLEMENTED: Use DBs of this information and integrate

Does not matter how Zoltan organizes data
Searches for gene name matches:

Matches

CSF1R  = CSF1R    or   csf1r
CSF1 != CSF1R
CSF1 != csf

Spits out information in what column a match was found and how many

Summarizes the number found
