# Drug Repositioning via Clustering and Classification of Molecular Physicochemical Descriptors

This project presents a machine learning approach for drug repositioning based on molecular physicochemical descriptors retrieved from the ChEMBL database, combining unsupervised clustering and supervised classification.

## Project Summary

1. **Data Source**: Physicochemical descriptors and therapeutic indications of pharmaceutical compounds were extracted from ChEMBL (https://www.ebi.ac.uk/chembl/).
2. **Clustering Analysis**: Four clustering algorithms (K-Means, GMM, MeanShift, and DBSCAN) were applied to analyze how compounds group within the physicochemical feature space.
3. **Indication Profiling**: For each resulting cluster, the most predominant therapeutic indications were identified.
4. **Classification & Repositioning**:
   - A Random Forest classifier was trained on the identified predominant therapeutic indications.
   - The trained model was applied to the compounds within each cluster that did NOT originally carry that predominant indication.
   - Compounds predicted positive by the model were identified as potential candidates for drug repositioning.
