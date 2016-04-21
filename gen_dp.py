#!/usr/bin/python
import sys
import os
import math
import json
from argparse import ArgumentParser

parser = ArgumentParser(description="Generate dependecy graph")
parser.add_argument('--size', '-S',
                    type=int,
                    help="Size of each object: 1 (1K), 10 (10K), 100(100K)," +
                    "1000(1M), -1(100B)",
                    required=True)
parser.add_argument('--num', '-N',
                    type=int,
                    help="Number of objects",
                    required=True)
parser.add_argument('--out', '-O',
                    type=str,
                    help="Output directory, format: dg/[name].com_/",
                    required=True)
parser.add_argument('--time', '-T',
                    type=int,
                    help="Computation time for each object",
                    default=200)
parser.add_argument('--deptime', '-DT',
                    type=int,
                    help="Dependency time for each dependency relation",
                    default=100)
args = parser.parse_args()

def gen():
  # Init
  host = "10.0.0.2"
  time = args.time
  dep_time = args.deptime
  if args.size >= 1000:
    path = "/pages/rawobj.com/obj_1M.js"
    name = '1M' + str(args.num)
    desc = "obj_size = 1M, " + "obj_num = " + str(args.num)
  elif args.size > 0:
    path = "/pages/rawobj.com/obj_" + str(args.size) + "K.js"
    name = str(args.size) + 'K' + str(args.num)
    desc = "obj_size = " + str(args.size) + "K, " + "obj_num = " + str(args.num)
  else:
    path = "/pages/rawobj.com/obj_100B.js"
    name = '100B' + str(args.num)
    desc = "obj_size = 100B, " + "obj_num = " + str(args.num)
  dg = {
      'name' : name,
      'description' : desc,
      'objs' : [],
      'deps' : []
  }

  # Generate objects
  for i in range(1, args.num + 1):
    if i == 1:
      wcs = 1
      type_ = "evalhtml"
      dg['start_activity'] = "r" + str(i) + "_d"
    else:
      wcs = -1
      type_ = "evaljs"
      dg['load_activity'] = "r2_c"

    obj = {
        'id' : "r" + str(i),
        'host' : host,
        'path' : path,
        'when_comp_start' : wcs,
        'download' : {
          'id' : "r" + str(i) + "_d",
          'type' : "download"
        },
        'comps' : [
          {
            'id' : "r" + str(i) + "_c",
            'type' : type_,
            'time' : time
          }
        ]
    }

    dg['objs'].append(obj)

    if i != 1:
      dep = {
          'id' : "dep" + str(i-1),
          'a1' : "r" + str(i-1) + "_c",
          'a2' : "r" + str(i) + "_d",
          'time' : dep_time
      }
      dg['deps'].append(dep)

  # Make the graphs partially dependent.
  for i in range(1, args.num/2):
    dg['deps'][i]['a1'] = "r1_c"
  for i in range(args.num/2, args.num/2 + args.num/3):
    dg['deps'][i]['a1'] = "r2_c"

  # Dump pretty JSON
  json_str = json.dumps(dg, indent=4, sort_keys=True)

  # Output the result dependency graph
  if not os.path.exists(args.out):
    os.makedirs(args.out)
  f1=open(args.out + name + ".json", 'w')
  f1.write(json_str)

if __name__ == "__main__":
  gen()
