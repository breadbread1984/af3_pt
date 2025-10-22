#!/usr/bin/python3

from absl import flags, app
from os import walk
from os.path import splitext, join
import json
from tqdm import tqdm

FLAGS = flags.FLAGS

def add_options():
  flags.DEFINE_string('input_dir', default = 'data', help = 'path to input directory')
  flags.DEFINE_string('output', default = 'update_list.json', help = 'path to output json')

def main(unused_argv):
  pattern = """_pdbx_struct_assembly_gen.assembly_id
#
"""
  update_list = list()
  for root, dirs, files in tqdm(walk(FLAGS.input_dir)):
    for f in files:
      stem, ext = splitext(f)
      if ext != '.cif': continue
      with open(join(root, f), 'r') as ios:
        content = ios.read()
      pos = content.find(pattern)
      if pos = -1: continue
      if not content[pos + len(pattern):].startswith('loop_'):
        new_content = content[:pos + len(pattern)] + 'loop_\n' + content[pos + len(pattern):]
      update_list.append(join(root, f))
      with open(join(root, f), 'w') as ios:
        ios.write(new_content)
  with open(FLAGS.output, 'w') as f:
    f.write(json.dumps(update_list))

if __name__ == '__main__':
  add_options()
  app.run(main)

