#! /usr/bin/env python

import tensorflow as tf
import numpy as np
import os
import time
import datetime
import data_helpers
from text_cnn import TextCNN

# Parameters
# ==================================================

# Eval Parameters
tf.flags.DEFINE_integer("batch_size", 64, "Batch Size (default: 64)")
tf.flags.DEFINE_string("checkpoint_dir", "", "Checkpoint directory from training run")

# Misc Parameters
tf.flags.DEFINE_boolean("allow_soft_placement", True, "Allow device soft device placement")
tf.flags.DEFINE_boolean("log_device_placement", False, "Log placement of ops on devices")


FLAGS = tf.flags.FLAGS
FLAGS._parse_flags()
print("\nParameters:")
for attr, value in sorted(FLAGS.__flags.items()):
    print("{}={}".format(attr.upper(), value))
print("")

# Load data. Load your own data here
print("Loading data...")
x_test, y_test, vocabulary, vocabulary_inv = data_helpers.load_data()
y_test = np.argmax(y_test, axis=1)

print("Vocabulary size: {:d}".format(len(vocabulary)))
print("Test set size {:d}".format(len(y_test)))

print("\nEvaluating...\n")

# Evaluation
# ==================================================
checkpoint_file = tf.train.latest_checkpoint(FLAGS.checkpoint_dir)
graph = tf.Graph()
with graph.as_default():
    session_conf = tf.ConfigProto(
      allow_soft_placement=FLAGS.allow_soft_placement,
      log_device_placement=FLAGS.log_device_placement)
    sess = tf.Session(config=session_conf)
    with sess.as_default():
			# Load the saved meta graph and restore variables
			saver = tf.train.import_meta_graph("{}.meta".format(checkpoint_file))
			saver.restore(sess, checkpoint_file)

			# Get the placeholders from the graph by name
			input_x = graph.get_operation_by_name("input_x").outputs[0]
			# input_y = graph.get_operation_by_name("input_y").outputs[0]
			dropout_keep_prob = graph.get_operation_by_name("dropout_keep_prob").outputs[0]

			# Tensors we want to evaluate
			predictions = graph.get_operation_by_name("output/predictions").outputs[0]

			# Generate batches for one epoch
			# batches = data_helpers.batch_iter(x_test, FLAGS.batch_size, 1, shuffle=False)


			# ##################################################################################################
			"""
			s = raw_input("type the sentence:")
			s = data_helpers.clean_str(s)
			s = s.split(" ")
			s = s + ["<PAD/>"] * (56 - len(s))
			for i, w in enumerate(s):
				if w not in vocabulary:
					s[i] =  "<PAD/>"
			s = np.array([vocabulary[word] for word in s])
			s = [s]

			print "Prediction: ", sess.run(predictions, {input_x: s, dropout_keep_prob: 1.0})
			"""
			def predict2(s):
				s = data_helpers.clean_str(s)
				s = s.split(" ")
				s = s + ["<PAD/>"] * (56 - len(s))
				for i, w in enumerate(s):
					if w not in vocabulary:
						s[i] =  "<PAD/>"
				s = np.array([vocabulary[word] for word in s])
				s = [s]
				return sess.run(predictions, {input_x: s, dropout_keep_prob: 1.0})
			# ##################################################################################################

			# Collect the predictions here
			pos_file_name= "amazon_pos.txt"
			f = open("/home/jein/cnn-text-classification-tf/data/rt-polaritydata/" + pos_file_name, "r")
			total_test_num = 0
			correct_count = 0
			while True:
				line = f.readline()
				if not line: break
				if len(line.split()) > 55:
					continue
				if predict2(line)[0] == 1:
					correct_count += 1
				total_test_num += 1
			f.close()
			neg_file_name= "amazon_neg.txt"
			f = open("/home/jein/cnn-text-classification-tf/data/rt-polaritydata/" + neg_file_name, "r")
			while True:
				line = f.readline()
				if not line: break
				if len(line.split()) > 55:
					continue
				if predict2(line)[0] == 0:
					correct_count += 1
				total_test_num += 1
			f.close()
				
			# Print accuracy
			print("Input file name : " + pos_file_name + " , " + neg_file_name)
			print("Total number of test examples: {}".format(correct_count))
			print("Accuracy: {:g}".format(correct_count/float(total_test_num)))
