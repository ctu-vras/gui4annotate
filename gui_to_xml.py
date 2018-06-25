#!/usr/bin/env python

import os
import lxml.etree as ET
import ast
from xml.dom import minidom
import warnings
import argparse
import cv2
from collections import defaultdict
import math
import hashlib

fw_orig = warnings.formatwarning
warnings.formatwarning = lambda msg, categ, fname, lineno, line=None: fw_orig(msg, categ, fname, lineno, '')

def parse_args():
	parser = argparse.ArgumentParser()
	parser.add_argument('indir')
	parser.add_argument('max_size', type=int)
	parser.add_argument('min_overlap', type=int)
	parser.add_argument('outdir')
	parser.add_argument('outxml')
	
	args =  parser.parse_args()
	return args
	
def hashfile(afile, hasher, blocksize=65536):
	buf = afile.read(blocksize)
	while len(buf) > 0:
		hasher.update(buf)
		buf = afile.read(blocksize)
	return hasher.hexdigest()

def convert_data(txtfiles, args):
	xml = ET.Element('folder')
	for txt in txtfiles:
		im_name = os.path.splitext(txt)[0] + '.JPG'
		im = cv2.imread(im_name)
		height, width = im.shape[:2]
		rows, cols = map(lambda x: int(math.ceil(float(x - args.min_overlap)/(args.max_size - args.min_overlap))), (height, width))
		lines = defaultdict(list)
		hh = open(im_name, 'rb')		
		h = hashfile(hh, hashlib.md5())
		hh.close()
		with open(txt, mode='r') as f:
			for line in f:
				line = line.strip().split(',')
				if line[4] == 'onject':
					line[4] = 'object'
				line[:4] = map(float, line[:4])
				data1 = map(lambda x: int((x - args.min_overlap)/(args.max_size - args.min_overlap)), line[:4])
				data2 = map(lambda x: int(x)/(args.max_size - args.min_overlap), line[:4])
				d1, d2 = False, False
				if data1[0] is data1[2] and data1[1] is data1[3]:
					d1 = True
				if data2[0] is data2[2] and data2[1] is data2[3]:
					d2 = True
				if d1 and not d2:
					lines[(data1[0], data1[1])].append(line)
				elif not d1 and d2:
					lines[(data2[0], data2[1])].append(line)
				elif not d1 and not d2:
					if data1[0] is not data1[2] and data1[1] is data1[3]:
						lines[(data1[0] + 0.5, data1[1])].append(line)
					elif data1[0] is data1[2] and data1[1] is not data1[3]:
						lines[(data1[0], data1[1] + 0.5)].append(line)
					else:
						lines[(data1[0] + 0.5, data1[1] + 0.5)].append(line)
				else:
					lines[(data1[0], data1[1]) if len(lines[(data1[0], data1[1])]) > len(lines[(data2[0], data2[1])]) else (data2[0], data2[1])].append(line)					
			for key in lines.keys():
				size = (args.max_size - args.min_overlap)
				endx = key[0] * size + args.max_size if key[0] < cols - 1 else width
				endy = key[1] * size + args.max_size if key[1] < cols - 1 else height
				imn = im[key[1] * size:endy, key[0] * size:endx]
				imn_name = os.path.join(args.outdir, os.path.splitext(os.path.split(txt)[1])[0] + '-' + h + '-' + str(key[0]) + '-' + str(key[1]) + '.JPG')
				
				cv2.imwrite(imn_name, imn)
				elem = ET.Element('file')
				elem.set('path', imn_name)
				for obj in lines[key]:
					ee = ET.Element('object')
					ee.set('class', obj[4])
					ee.set('bbox', '(%.2f, %.2f, %.2f, %.2f)' % tuple(map(lambda x, y: x-y, obj[:4], (key[0] * (args.max_size - args.min_overlap), key[1] * (args.max_size - args.min_overlap)) * 2)))
					ee.set('prob', 'gt')
					elem.append(ee)
				xml.append(elem)
	return xml
				

if __name__ == '__main__':
	args = parse_args()
	if not os.path.isdir(args.outdir):
		os.makedirs(args.outdir)
	else:
		warnings.warn('Folder ' + args.outdir + ' already exists')
	if os.path.isfile(args.outxml):
		warnings.warn('File ' + args.outxml + ' will be overridden')
	txtfiles = [os.path.join(cur_dir,f) for cur_dir, dirs, files in os.walk(os.path.abspath(args.indir)) for f in files if os.path.splitext(f)[1] == '.txt']
	xml = convert_data(txtfiles, args)
	xml.set('path', args.outdir)
	xml.set('files', str(len(xml)))
	root = ET.Element('Ground_truth')
	root.set('dataset', 'broucci')
	root.append(xml)
	xml = root
	rough = ET.tostring(xml)
	with open(args.outxml, mode='w') as f:
		minidom.parseString(rough).writexml(f, addindent='\t', newl='\n')
