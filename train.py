#!/usr/bin/python3

from absl import flags, app
import torch
from alphafold3_pytorch import Alphafold3, Trainer, create_trainer_from_yaml
from alphafold3_pytorch.inputs import PDBDataset

FLAGS = flags.FLAGS

def add_options():
  flags.DEFINE_bool("weighted_sampling", default = False, help = 'whether weighted sampling')
  flags.DEFINE_string("ckpt", default = None, help = 'resume from existing checkpoint')

def main(unused_argv):
  # some pdb sample cannot be preprocessed. refer to https://github.com/lucidrains/alphafold3-pytorch/issues/296
  # to prevent the exception in preprocessing interrupt training loop, we commit https://github.com/breadbread1984/af3_pt/commit/0a383cf660ed33739289e730c76d6cf9695d765b
  config_path = './tests/configs/trainer_with_pdb_dataset.yaml' if FLAGS.weighted_sampling == False else \
                './tests/configs/trainer_with_pdb_dataset_and_weighted_sampling.yaml'
  trainer = create_trainer_from_yaml(config_path)
  if FLAGS.ckpt is not None: trainer.load(FLAGS.ckpt)
  trainer()
  print("Training finished.")

if __name__ == "__main__":
  add_options()
  app.run(main)
