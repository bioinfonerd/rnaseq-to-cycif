# CIR: CyCif Antibody Integration With RNA-Seq
Purpose: Identify CyCif Validated Antibodies that match differentially expressed RNA-Seq results
Version: 0.0.1

To run:  python CyCif-RNA-Seq_0.0.1.py

Current Input Organization:
 1) Ensembl Gene/Transcript Mapping
 2) Zoltan's list of CyCif Antibodies
 3) RNA-Seq Differentially Expressed Results (directory: rna_seq_results)
 
 Output: 
    - Table summarizing antibodies found and what analysis found
    - For each individual RNA-Seq analysis, outputs file with cycif antibody found with all information associated

Possible Improvements:
- Additional Information To Find missing Gene IDs for CyCif Proteins 
- Merge all RNA-Seq results into 1 CyCif Panel (user limit on number of rounds)
- Smart CyCif Panel: 
- Add whether antibodies are better in earlier or later rounds
- Fluoresce Conflicts
- Graphical Output For Results
- Smart Way to Determine which RNA correlates with Protein
- Transcript specificity for CyCif Antibodies

## Programming Rationale
 ### PART 1: QC
    -  QC checks ie search all CyCif Antibodes with Ensembl names to check if possible 
    -  Method is independent of how Zoltan organizes Antibody Table
    -  Matches Gene Name to provide a match for each CyCif Antibody Catalog Number
    -  Prints out statistics on how many matches, where found, and what % of CyCif Antibodies were Found
    
 ### Part 2: RNA-Seq DEG & CyCif Selection
    - For each file of RNA-Seq Analysis output, save all genes with CyCif results in separate table in folder 'rna_cycif_results'
    - Prints statistics on search
    
    Example:
    
        RNA-Seq Results for analysis: RCB0_D1vsD8
        Differentially Expressed Genes Results: 85
        Differentially Expressed Transcript Results: 98
        Number of matching CyCif Antibodies: 11(0.13%)
        
     - Prints summary across all RNA-Seq Analysis
     
        Merging CyCif Antibodies From RNA-Seq Results
        Total RNA-Seq Analysis Merging: 21
        All DEG RNA-Seq Results with CyCif Antibodies: 274
        Combined CyCif RNA-Seq Results: 133
        
 ### PART 3: Merge CyCif Panel
    - Take all results from Part 2 and merge
    - Saves file that show gene id, gene short name, cycif antibody, RNA-Seq Supporting Analysis, Number of RNA-Seq analysis supporting observation
 

