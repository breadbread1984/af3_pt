#!/usr/bin/python3

from alphafold3_pytorch.inputs import PDBInput, INPUT_TO_ATOM_TRANSFORM

# this script is for testing samples which can raise exception 

preprocessor = INPUT_TO_ATOM_TRANSFORM.get(PDBInput)
i = PDBInput(
  mmcif_filepath = 'data/pdb_data/train_mmcifs/hr/3hr2-assembly1.cif',
  chains = (None, None),
  cropping_config = {
    "contiguous_weight": 0.2,
    "spatial_weight": 0.4,
    "spatial_interface_weight": 0.4,
    "n_res": 384
  },
  training = True,
  inference = True,
)

result = preprocessor(i)
