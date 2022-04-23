import os
import csv
import config
import random
import argparse

# Returns a number of reference and decoded text pairs along with scores from specified data.
parser = argparse.ArgumentParser()
parser.add_argument("-d",
                dest="data_name",
                required=False,
                default="data_T50",
                help="Dataset name which examples to be fetched.")
parser.add_argument("-n",
                dest="num_examples",
                required=False,
                default=3,
                help="Number of examples to be fetched.")
args = parser.parse_args()

data_path = "decode_" + args.data_name
log_name = os.path.join(config.log_root, data_path)

ref_dir = os.path.join(log_name, "rouge_ref")
dec_dir = os.path.join(log_name, "rouge_dec_dir")
scores_dir = os.path.join(log_name, "rouge_scores")
file_count = len(os.listdir(ref_dir))
random_ids = random.sample(range(0,file_count), int(args.num_examples))

for i, id in enumerate(random_ids):
    # Read the reference text
    file_name = str(id).zfill(6) + "_reference.txt"
    file_dir = os.path.join(ref_dir,file_name)
    with open(file_dir) as f:
        ref_text = f.read()
    
    # Read the decoded text
    file_name = str(id).zfill(6) + "_decoded.txt"
    file_dir = os.path.join(dec_dir,file_name)
    with open(file_dir) as f:
        dec_text = f.read()

    # Read the score
    score_list = []
    for file_name in ["rouge_1.csv", "rouge_2.csv", "rouge_l.csv"]:
        file_dir = os.path.join(scores_dir,file_name)
        with open(file_dir) as f:
            scores = csv.reader(f)
            for row in scores:
                if row[0] == str(id):
                    score_list.append(round(float(row[1]),4))
                    break


    print("\nFile: {} - F1 scores of-> Rouge1:{}, Rouge2: {}, RougeL: {}".format(str(id).zfill(6),
        score_list[0], score_list[1], score_list[2]
        ))
    print("--------------- REFERENCE ---------------")
    print(ref_text)
    print("--------------- DECODED ---------------")
    print(dec_text)
    print("---------------------------------------\n")