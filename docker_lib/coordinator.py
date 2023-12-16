#!/usr/bin/env python

# Coordinator script by J.J.Iszatt

import os
import sys
import datetime
import subprocess
import pandas as pd
from Bio import SeqIO
import csv

# Reading input directory
input = '/lab/input'
output = '/lab/output'
index = '/lab/database/PHROG_index.csv'
logs = '/lab/output/docker_log.tsv'

# Reading index file
df2 = pd.read_csv(index)

# Creating Annotation class
class Annotation(object):
    def __init__(self, genome, id, feature, start, end, strand, pseudo, product):
        self.genome = genome;
        self.id = id;
        self.feature = feature;
        self.start = start;
        self.end = end;
        self.strand = strand;
        self.pseudo = pseudo;
        self.product = product;

# Creating log file
if not os.path.exists(logs):
    with open(logs, 'w') as file:
        file.write("Container\tDate and time\tFunction\tLog")

# Logging function
def logfile(function, text):
    newline = '\n'
    container = "PhageOrder v0.0.3"
    date_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    report = f"{newline}[{container}]\t[{date_time}]\t[{function}]\t[{text}]"
    with open(logs, 'a') as file:
        file.write(report)
        
# Check path function  
def check_filepath(filepath, create=False):
    if os.path.exists(filepath):
        print(f"Found:{filepath}")
    else:
        if create:
            try:
                os.makedirs(filepath)
            except:
                sys.exit(1)
        else:
            sys.exit(1)

# Annotation
def annotate(genome, output, phage_name):
    # construct the prokka command
    cmd = [
        'prokka',
        genome,
        '--hmms', '/opt/conda/envs/lab/db/hmm/all_phrogs.hmm',
        '--outdir', output,
        '--addgenes',
        '--kingdom', 'Viruses',
        '--gcode', '11',
        '--locustag', phage_name,
        '--prefix', f"{phage_name}",
        '--compliant'
    ]
    # run the prokka command using subprocess
    subprocess.run(cmd)
    
def scan_records(file):   
    scan = ['CDS', 'tRNA', 'rRNA']
    annotations = []
    with open(gbk, 'r') as file:
        records = SeqIO.parse(file, 'genbank')
        for A in records:
            for feature in A.features:
                f_type = feature.type
                
                # If the feature is a CDS, tRNA or rRNA (consider options for these)
                if f_type in scan:
                    
                    # Protein name
                    if 'locus_tag' in feature.qualifiers:
                        locus_tag = feature.qualifiers['locus_tag'][0]
                    else:
                        locus_tag = 'NA'

                    # Strand
                    if feature.strand == 1:
                        strand = '+'
                    else:
                        strand = '-'
                    
                    # pseudo
                    if 'pseudo' in feature.qualifiers or 'pseudogene' in feature.qualifiers:
                        pseudo = 'Y'
                    else:
                        pseudo = 'N'
                    
                    # products
                    if "product" in feature.qualifiers:
                        product = feature.qualifiers["product"][0]
                    else:
                        product = "unknown"
                    
                    # Creating dataframe
                    genome = A.name
                    start = str(feature.location.nofuzzy_start + 1)
                    end = str(feature.location.nofuzzy_end)
                    annotation = Annotation(
                        genome,
                        locus_tag,
                        feature.type,
                        start,
                        end,
                        strand,
                        pseudo,
                        product
                    )
                    annotations.append(annotation)
    return annotations

def isolate_subunits(annotations):
    if len(annotations) == 0:
        return None
    small = []
    large = []
    for A in annotations:
        
        if A.product == 'terminase small subunit':
            small.append(A)
            
        if A.product == 'terminase large subunit':
            large.append(A)
            
    return small, large

def subunit_decision(small, large):        
    if len(small) == 1:
        logfile("Subunit decision", f"{name}: Small subunit reorder")
        return small
    else:
        if len(large) == 1:
            logfile("Subunit decision", f"{name}: Large subunit reorder")
            return large
        else:
            if len(small) > 1 and len(large) > 1:
                logfile("Subunit decision", f"{name}: Too many subunits")
                return None
            else:
                if len(small) == 0 and len(large) == 0:
                    logfile("Subunit decision", f"{name}: No subunits found")
                    return None
                else:
                    return None

def reverse(input, output):
    logfile("Reversing sequence", f"{name}")
    for record in SeqIO.parse(open(input), 'fasta'):
        reverse_seq = str(record.seq.reverse_complement())
    with open(output, "w") as out:
        out.write('>' + record.id + '\n' + reverse_seq)

def reorder_genome(start, file, output):
    starter = int(start)-1
    print(starter, 'should be 1 less than', start)
    for contig_record in SeqIO.parse(open(file), 'fasta'):
        contig = str(contig_record.seq)
    str1 = contig[starter:]
    str2 = contig[:starter]
    str_final = '>'+contig_record.id + '\n' + str1 + str2
    with open(output, "w") as out:
        out.write(str_final)
        
def create_csv(filename, data):
    with open(filename, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(data)

def append_csv(filename, data):
    with open(filename, 'a', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(data)

# Checking filepaths
logfile("Validation", "Checking input files")
check_filepath(input)
check_filepath(output)
check_filepath(index)
logfile("Validation","Passed filepath checks")

# Finding genomes
files = []
for fasta in os.listdir(input):
    if fasta.endswith('.fasta'):
        files.append(f"{input}/{fasta}")
        logfile("File scan", f"Adding file: {fasta}")
    else:
        logfile("File scan", f"Skipping file: {fasta}")

# Running first prokka pass
if len(files) == 0:
    sys.exit("No genomes with .fasta extension found")

for file in files:
    
    # Assigning base file names
    name = os.path.basename(file)[:-6]
    outdir = f"{output}/{name}"
    
    # Checking if it already exists
    if os.path.exists(outdir):
        logfile("Check", f"{name} outdir already exists, skipping")
        continue
    else:
        os.makedirs(outdir)
    
    # Beginning annotation:
    logfile("Process", f"Running annotation: {name}")
    prokka_dir = f"{outdir}/{name}_raw"
    prokka_dir2 = f"{outdir}/{name}_reversed"
    prokka_dir3 = f"{outdir}/{name}_reordered"
    
    # First annotation
    annotate(file, prokka_dir, name)
    logfile("Annotation", f"{name}")
    
    # Obtaining features from genbank file
    gbk = f"{prokka_dir}/{name}.gbk"
    annotations = scan_records(gbk)
    logfile("Genbank file scan", f"{name}")
    
    # Isolating subunits
    small, large = isolate_subunits(annotations)
    logfile("Subunit isolation", f"{name}")
    
    # Making decision
    genome = file
    subunit = subunit_decision(small, large)
    
    # Checking subunit 
    if subunit == None:
        logfile("Error catch", f"Moving to next genome")
        continue
    
    # Reordering
    subunit_strand = subunit[0].strand
    if subunit_strand == '-':
        
        reversed_genome = f"{outdir}/reversed.fasta"
        reverse(file, reversed_genome)
        
        annotate(reversed_genome, prokka_dir2, name)
        logfile("Annotation", f"{name} (reversed)")
        
        gbk = f"{prokka_dir2}/{name}.gbk"
        annotations = scan_records(gbk)
        logfile("Genbank file scan for reverse", f"{name} (reversed)")
        
        small, large = isolate_subunits(annotations)
        logfile("Subunit isolation", f"{name} (reversed)")
        
        genome = reversed_genome
        subunit = subunit_decision(small, large)
    
    # Obtaining start of the subunit
    if not len(subunit) == 1:
        logfile("ERROR", f"{name}")
        continue
        
    print(f"Reordering based on {subunit[0].id}")
    start = subunit[0].start
    
    # Reordering
    logfile("Reordering", f"{name}")
    reordered_genome = f"{outdir}/{name}_reordered.fasta"
    reorder_genome(subunit[0].start, genome, reordered_genome)
    
    # Final annotation:
    annotate(reordered_genome, prokka_dir3, name)
    logfile("Finished reordering", f"{name}")
    
    # Isolating proteins
    gbk = gbk = f"{prokka_dir3}/{name}.gbk"
    annotations = scan_records(gbk)
    
    # Reading data from TSV file
    tsv_file = f"{prokka_dir3}/{name}.tsv"
    df = pd.read_csv(tsv_file, sep = '\t')
    df = df.drop(df[df['ftype'] == 'gene'].index)
    df = df.reset_index(drop=True)
    
    # Creating CSV
    csv_file = f"{outdir}/{name}_proteins.csv"
    headers = [[
        'locus_tag',
        'length_bp',
        'EC_number',
        'product',
        'start',
        'end',
        'category',
        'strand'
        ]]
    create_csv(csv_file, headers)
    
    # Looping through features for reordered genome
    for A in annotations:
        
        # Adding from tsv
        for index, row in df.iterrows():
            if A.id == row['locus_tag']:
                phrog = row['EC_number']
                length = row['length_bp']
                break
    
        # Adding category from index
        for index, row in df2.iterrows():
            if phrog == row['#phrog']:
                category = row['Category']
                break
            else:
                category = None
        
        # Appending data
        data = [
                A.id,
                length,
                phrog,
                A.product,
                A.start,
                A.end,
                category,
                A.strand
            ]
        
        append_csv(csv_file, data)
    logfile("Protein file (reordered) creation", f"{name} complete")
        
    ########### Going back to create proteins file from raw

    # Obtaining features from genbank file
    gbk = f"{prokka_dir}/{name}.gbk"
    annotations = scan_records(gbk)
        
    # Reading data from TSV file
    tsv_file = f"{prokka_dir}/{name}.tsv"
    df = pd.read_csv(tsv_file, sep = '\t')
    df = df.drop(df[df['ftype'] == 'gene'].index)
    df = df.reset_index(drop=True)
    
    # Creating CSV
    csv_file = f"{outdir}/raw_{name}_proteins.csv"
    headers = [[
        'locus_tag',
        'length_bp',
        'EC_number',
        'product',
        'start',
        'end',
        'category',
        'strand'
        ]]
    create_csv(csv_file, headers)
        
    # Looping through features for reordered genome
    for A in annotations:
        
        # Adding from tsv
        for index, row in df.iterrows():
            if A.id == row['locus_tag']:
                phrog = row['EC_number']
                length = row['length_bp']
                break
    
        # Adding category from index
        for index, row in df2.iterrows():
            if phrog == row['#phrog']:
                category = row['Category']
                break
            else:
                category = None
        
        # Appending data
        data = [
                A.id,
                length,
                phrog,
                A.product,
                A.start,
                A.end,
                category,
                A.strand
            ]
        
        append_csv(csv_file, data)
    logfile("Protein file (raw) creation", f"{name} complete")
    
# Creating summary file with genome length, number of CDS, tRNAs, hypothetical proteins, and coding capacity

    
    
    
logfile("FINISH", f"END SCRIPT")     
