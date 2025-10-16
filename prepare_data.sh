#!/bin/bash

set -u
set -o pipefail

rsync -rlpt -v -z --delete -P --port=33444 \
rsync.rcsb.org::ftp_data/assemblies/mmCIF/divided/ ./data/pdb_data/unfiltered_assembly_mmcifs/
rsync -rlpt -v -z --delete -P --port=33444 \
rsync.rcsb.org::ftp_data/structures/divided/mmCIF/ ./data/pdb_data/unfiltered_asym_mmcifs/
find ./data/pdb_data/unfiltered_assembly_mmcifs/ -type f -name "*.gz" -exec gzip -d {} \;
find ./data/pdb_data/unfiltered_asym_mmcifs/ -type f -name "*.gz" -exec gzip -d {} \;
wget -P ./data/ccd_data/ https://files.wwpdb.org/pub/pdb/data/monomers/components.cif.gz
wget -P ./data/ccd_data/ https://files.wwpdb.org/pub/pdb/data/component-models/complete/chem_comp_model.cif.gz
find data/ccd_data/ -type f -name "*.gz" -exec gzip -d {} \;
PYTHONPATH=. python scripts/filter_pdb_train_mmcifs.py --mmcif_assembly_dir ./data/pdb_data/unfiltered_assembly_mmcifs/ --mmcif_asym_dir ./data/pdb_data/unfiltered_asym_mmcifs/ --ccd_dir ./data/ccd_data/ --output_dir ./data/pdb_data/train_mmcifs/
PYTHONPATH=. python scripts/filter_pdb_val_mmcifs.py --mmcif_assembly_dir ./data/pdb_data/unfiltered_assembly_mmcifs/ --mmcif_asym_dir ./data/pdb_data/unfiltered_asym_mmcifs/ --output_dir ./data/pdb_data/val_mmcifs/
PYTHONPATH=. python scripts/filter_pdb_test_mmcifs.py --mmcif_assembly_dir ./data/pdb_data/unfiltered_assembly_mmcifs/ --mmcif_asym_dir ./data/pdb_data/unfiltered_asym_mmcifs/ --output_dir ./data/pdb_data/test_mmcifs/
PYTHONPATH=. python scripts/cluster_pdb_train_mmcifs.py --mmcif_dir ./data/pdb_data/train_mmcifs/ --output_dir ./data/pdb_data/data_caches/train_clusterings/ --clustering_filtered_pdb_dataset
PYTHONPATH=. python scripts/cluster_pdb_val_mmcifs.py --mmcif_dir ./data/pdb_data/val_mmcifs/ --reference_clustering_dir ./data/pdb_data/data_caches/train_clusterings/ --output_dir ./data/pdb_data/data_caches/val_clusterings/ --clustering_filtered_pdb_dataset
PYTHONPATH=. python scripts/cluster_pdb_test_mmcifs.py --mmcif_dir ./data/pdb_data/test_mmcifs/ --reference_1_clustering_dir ./data/pdb_data/data_caches/train_clusterings/ --reference_2_clustering_dir ./data/pdb_data/data_caches/val_clusterings/ --output_dir ./data/pdb_data/data_caches/test_clusterings/ --clustering_filtered_pdb_dataset

