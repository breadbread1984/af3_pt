#!/usr/bin/python3

from alphafold3_pytorch.inputs import PDBInput, INPUT_TO_ATOM_TRANSFORM
from alphafold3_pytorch.common.biomolecule import from_mmcif_string

# this script is for testing samples which can raise exception 

preprocessor = INPUT_TO_ATOM_TRANSFORM.get(PDBInput)
mmcif_path = '/mnt/c/Users/bread/Downloads/pdb_tests/reference/9hvc.cif'
with open(mmcif_path, 'r') as f:
  mmcif_str = f.read()
biomol = from_mmcif_string(mmcif_str, '9hvc')
i = PDBInput(
  mmcif_filepath = '/mnt/c/Users/bread/Downloads/pdb_tests/reference/9hvc.cif',
  biomol = biomol,
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
res_idx, token_idx, asym_id, entity_id, sym_id = result.additional_molecule_feats.unbind(dim = -1)

