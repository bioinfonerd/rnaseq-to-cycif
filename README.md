# CyCif Antibody Selection Based on RNA-Seq

Purpose: Identify CyCif Validated Antibodies that match differentially expressed RNA-Seq results

Version: 0.0.1 (Current)

To run: python CyCif-RNA-Seq_0.0.1.py

The tool priority ranks validated CyCif antibodies based on differential gene expression from RNA-Seq.  In brief, the method 1) resolves gene and protein name discrepancies through an integrated (>30) database as quality control, 2) merges a list of validated CyCif Antibodies and RNA-Seq differential gene expression, and 3) priority ranks by the frequency a particular gene appears across all RNA-Seq analysis.  This priority list is further refined by 1) including known RNA and protein correlated expressions and 2) utilizing a literature-based network analysis for targets-of-interest that lack an antibody but high RNA-Seq evidence support. 

# Current Input Organization: 
  1) Ensembl Gene/Transcript Mapping ('gt_mapping.feather') 
  2) List of Validated CyCif Antibodies ('Validated_CyCif_Antibodies_2019.01.24-NJ.csv') 
  3) RNA-Seq Differentially Expressed Results 
      - A directory with one or more RNA-Seq Differentially Expressed Results (see rna_seq_results/) 

# Output: 
  1) Table summarizing for each RNA-Seq analysis which antibodies found and what analysis found 
      - For each individual RNA-Seq analysis, outputs file with cycif antibody found with all information associated
      - Saved in directory: rna_cycif_results 
  2) Summary File (CyCif_RNA_Seq_summary.tsv): 

# Possible Improvements

- Add method to find missing Gene IDs for CyCif Proteins
- Add user defined parameters on what differentially expressed selection criteria 
  - p-value, adjusted p-value cutoffs 
  - fold change 
  - consideration expression theshhold (Gene/Transcript may be significant but below CyCif detection limit) 
- Smart CyCif Panel:
  - Add whether antibodies are better in earlier or later rounds 
  - Fluoresce Conflicts 
  - Merge all RNA-Seq results into X CyCif Panel (user limit on number of rounds per panel) 
- Graphical Output For Results 
- Smart Way to Determine which RNA correlates with Protein 
- Transcript specificity for CyCif Antibodies 
- add python environment to improve user use Programming Rationale
- INDRA integration for edge effects(Peter Suggestion)
- Speak with proteomics about proteomics/RNA integration (Sarah suggestion)
- Level of antibody valiation for CyCif (Anninna)

# Future Improvements

This priority list is further refined by 1) including known RNA and protein correlated expressions and 2) utilizing a literature-based network analysis for targets-of-interest that lack an antibody but high RNA-Seq evidence support.

## PART 1: Quality Control

- QC checks ie search all CyCif Antibodes with Ensembl names to check if possible
- Method is independent of how Antibody Table is organized and updated
- Matches Gene Name to provide a match for each CyCif Antibody Catalog Number
- Prints out statistics on how many matches, where found, and what % of CyCif Antibodies were Found

    Example:

      Analyzing QC Data
      Found in column GeneID 474
      Found in column Uniprot 0
      Found in column Synonyms 2
      Found in column Target 41
      Found in column PTM 0
      Found in column Fluor 2
      Found in column Species 0
      Found in column Clone 2
      Found in column Isotype 0
      Found in column Reactivity 0
      Found in column Vendor 0
      Found in column Cat No 0
      Found in column Channel 0
      Found in column Expected 0
      Found in column Hs_confidence 0
      Found in column Hs_signoff 0
      Found in column Mm_confidence 0
      Found in column Mm_signoff 0
      Found in column JRL_bio 0
      Found in column SM_notes 0
      Found in column SS_list 0
      Found in column dil 0
      Found in column expt_TON 0
      Found in column sample_TON 0
      Found in column cyc_TON 0
      Found in column ch_TON 0
      Found in column dil_TON 0
      Found in column eval_TON 0
      Found in column TMA_expt 0
      Found in column TMA_sample 2
      Found in column TMA_cyc 0
      Found in column TMA_ch 0
      Found in column Unnamed: 32 1
      Found in column eval_TMA 0
      Found in column other 0
      Found in column sample 0
      Found in column ch 0
      Found in column cycle 0
      Found in column note 0
      Total CyCif Antibodies found: 524(0.85%) out of 615

## Part 2: RNA-Seq Differentially Expressed Genes & Transcripts with CyCif Selection

  - For each file of RNA-Seq Analysis output, save all genes with CyCif results in separate table in folder 'rna_cycif_results'
  - Prints statistics on search


    - Individual RNA-Seq Analysis Example:

          RNA-Seq Results for analysis: RCB0_D1vsD8 
          Differentially Expressed Genes Results: 85 
          Differentially Expressed Transcript Results: 98 
          Number of matching CyCif Antibodies: 11(0.13%)

## PART 3: Merge Individual RNA-Seq Seq & CyCif Results

  - Take all results from Part 2 and merge
  - Saves file that show gene id, gene short name, cycif antibody, RNA-Seq Supporting Analysis, Number of RNA-Seq analysis
  - Prints summary across all RNA-Seq Analysis

          Merging CyCif Antibodies From RNA-Seq Results 
          Total RNA-Seq Analysis Merging: 21 
          All DEG RNA-Seq Results with CyCif Antibodies: 274 
          Combined CyCif RNA-Seq Results: 133



