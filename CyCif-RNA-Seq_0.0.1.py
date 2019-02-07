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

# <editor-fold desc="Library Loading & Data Load">

# Libraries
print("Loading Libraries")
import pandas as pd
import numpy as np
from sklearn.decomposition import PCA
import os
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.model_selection import KFold
from sklearn.model_selection import StratifiedKFold
from sklearn.metrics import precision_recall_fscore_support
from sklearn.metrics import matthews_corrcoef
from sklearn import metrics
from sklearn.metrics import classification_report
from sklearn.decomposition import PCA
import glob
import feather
import urllib

#load in data
print('Loading Data')
location='/home/bionerd/Dana_Farber/IRC/CyCif/git/RNA_Seq-to-CyCif'
os.chdir(location)

rna_seq_cycif_output_loc='./rna_cycif_results/'

#user input [TODO: add user input]
antibodies=pd.read_table("Validated_CyCif_Antibodies_2019.01.24-NJ.csv", sep=',',header='infer') #Zoltan CyCif Antbiodies
#RNA_Seq_Results = glob.glob("/home/bionerd/Dana_Farber/IRC/Analysis/BAM_Starting_Point_Analysis/*p001_sig_statistics.tsv")#read in all RNA-Seq DEG files
RNA_Seq_Results = glob.glob("./rna_seq_results/*.tsv")#read in all RNA-Seq DEG files
gene_mapping = feather.read_dataframe('gt_mapping.feather') #gene & transcript mapping reference file (feather format)
#filter down to just ensembl gene name and gene id
gene_mapping = gene_mapping.loc[:,['ens_gene', 'ext_gene']] #filter to just columns
gene_mapping = gene_mapping.drop_duplicates()# drop duplicates
column_cut_off = 'pval'
cut_off = 0.0001
# </editor-fold>

# <editor-fold desc="PART 1: QC">
print('')
print('Analyzing QC Data')
#read in each column of antibody file and assign Ensembl Gene ID if present
# if match: remove matches from file, add ID
# prints result of matching by column in case Zoltan changes antibody formatting

df = pd.DataFrame() #initialize dataframe for antibody + Ensembl Gene ID

for i in antibodies.columns: #
    if i == antibodies.columns[0]: #start the process
        if len(antibodies[antibodies[i].isin(gene_mapping.ext_gene)]) > 0: #if match, add
            input = antibodies[antibodies[i].isin(gene_mapping.ext_gene)] #select for genes that match
            input=pd.merge(input,gene_mapping,left_on=i,right_on='ext_gene',how='left') # add Ensembl Gene ID
            df = df.append(input)  # add selection
            tmp = antibodies[~antibodies[i].isin(gene_mapping.ext_gene)]  # substract matches from total
        else: #in case there are not matches in first column
            tmp = antibodies
            input = 0
    else: #if not first column, move on
        if len(tmp[tmp[i].isin(gene_mapping.ext_gene)]) > 0: #if information selected, add, if not move on
            input = tmp[tmp[i].isin(gene_mapping.ext_gene)]
            input=pd.merge(input,gene_mapping,left_on=i,right_on='ext_gene',how='left') # add Ensembl Gene ID
            df = df.append(input)  # add selection
            tmp = tmp[~tmp[i].isin(gene_mapping.ext_gene)] # substract matches from total
        else:
            input = 0
    if isinstance(input, pd.DataFrame): #handle int vs dataframe output
        print('Found in column', i, len(input['Cat No'].unique())) #if antibody column name changes, will error
    else:
        print('Found in column', i, input)
print('Total CyCif Antibodies found:',
      ''.join([str(len(df['Cat No'].unique())),'(',
               str(round(len(df['Cat No'].unique())/len(antibodies['Cat No'].unique()),2)),'%)']),
      'out of',len(antibodies['Cat No'].unique()))

# WEB LOOKUP for gene ids
print('[TODO] Add method to find missing CyCif Gene IDs')
#import urllib.request
#url = 'https://biodbnet-abcc.ncifcrf.gov/webServices/rest.php/biodbnetRestApi.xml?method=db2db&format=row&input=genesymbol&inputValues=MYC,MTOR&outputs=geneid&taxonId=9606'
#u = urllib.request.urlopen(url)
#response = u.read()

##



# </editor-fold>

# <editor-fold desc="PART 2: RNA-Seq DEG & CyCif">
print('')
print('Selecting for RNA-Seq Data with CyCif Antibodies')

for i in RNA_Seq_Results:
    tmp = pd.read_table(i) #load in RNA-Seq results
    print('')
    print('RNA-Seq Results for analysis:', i.split('/')[-1].split('.')[0])
    Sig_RNA_Seq=tmp[tmp[column_cut_off] <= cut_off] # separate results by cut off
    print('Differentially Expressed Genes Results:', len(Sig_RNA_Seq.ens_gene.unique()))
    print('Differentially Expressed Transcript Results:', len(Sig_RNA_Seq))
    output=pd.merge(Sig_RNA_Seq,df,on='ens_gene') # calculate number of CyCif Antibodies match
    #filter to unique antibody Catalog
    print('Number of matching CyCif Antibodies:',
          ''.join([str(len(output.drop_duplicates(['Cat No']))),'(',str(round(len(output.drop_duplicates(['Cat No']))
                                                  /len(Sig_RNA_Seq.ens_gene.unique()),2)),'%)']))
    #write results
    output.to_csv(''.join([rna_seq_cycif_output_loc,i.split('/')[-1].split('.')[0],'.RNA_Seq_CyCif_Antibodies.tsv']), sep="\t", index=True)
# </editor-fold>

# <editor-fold desc="PART 3: Merge RNA-Seq Results Panel">

print('')
print('Merging CyCif Antibodies From RNA-Seq Results')

results = glob.glob(''.join([rna_seq_cycif_output_loc,'*.RNA_Seq_CyCif_Antibodies.tsv']))#read in all CyCif/RNA-Seq files
print('Total RNA-Seq Analysis Merging:',len(results))
output=pd.DataFrame(columns=['ens_gene','ext_gene_x','Cat No','Analysis'])

for i in results: #merge all CyCif Samples
    tmp = pd.read_table(i)  # initialize
    tmp = tmp.loc[:, ['ens_gene', 'ext_gene_x', 'Cat No']].drop_duplicates(['Cat No'])
    tmp['Analysis'] = i.split('/')[-1].split('.')[0]
    output = pd.concat([output, tmp], keys=['ens_gene', 'ext_gene_x'],ignore_index=True)
print('All DEG RNA-Seq Results with CyCif Antibodies:',len(output))
output = output.groupby(['ens_gene','ext_gene_x','Cat No'])['Analysis'].apply(','.join).reset_index()
print('Combined CyCif RNA-Seq Results:',len(output))
output['Supporting Evidence']=output['Analysis'].str.count(',')
output['Supporting Evidence']=output['Supporting Evidence']+1
output.columns=['Ensembl Gene ID', 'Gene Name', 'CyCif Catalog Number', 'RNA-Seq Analysis', '# of Supporting Evidence']
output.to_csv('CyCif_RNA_Seq_summary.tsv', sep="\t")

# </editor-fold>

# <editor-fold desc="PART 4: Graphical Summary & Output">
print('')
print('[TODO] Graphical Output For Results')
# </editor-fold>

# <editor-fold desc="PART 5: RNA & Protein Correlation Metric Implementation">
print('[TODO] Smart Way to Guess if RNA correlates with Protein')
# </editor-fold>

# <editor-fold desc="PART 6: Make CyCif Panel">
print('[TODO] Make CyCif Panel')
# </editor-fold>

# <editor-fold desc="PART 7: Add Transcript Level CyCif Antibody Integration">
print('[TODO] Add Transcript Level CyCif Antibody Integration')
# </editor-fold>
