#!/usr/bin/env python3

import os
import argparse
from pathlib import Path

#Example run:
# ./generate_html.py -o /home/melody/testdir/QC_out/6_BTV-SISPA/html -v -q /home/melody/testdir/QC_out/6_BTV-SISPA/


def main():
  user_directory = os.getcwd()
  home_directory = os.path.expanduser('~')
  stylesheet = "/home/melody/style.css"
  #multiqc = home_directory + "/.local/bin/multiqc"
  #fastqc = "/usr/local/FastQC-0.11.9/fastqc"
  #uniprot_database = home_directory + "/db/viral_proteins/uniref90.fasta.gz"
  #diamond = "/usr/local/diamond-2.0.11/diamond"
  #seqtk = "/usr/local/seqtk-1.3/seqtk"
  #trinity = "/usr/local/trinityrnaseq-v2.13.1/Trinity"
  #refseq = home_directory + "/db/refseq/blastdb/refseq.virus.fasta"

  parser = argparse.ArgumentParser()
  parser.add_argument("-o", "--output_directory", help="Takes in path of directory that you want to create to store the output",
                      type=str)
  parser.add_argument("-v", "--version", help="Tells you the version of script",
                      action="store_true")
  parser.add_argument("-q", "--query", help="Takes in the directory that was generated by the pipeline that you wish to generate html pages for",
                      type=str)
  args = parser.parse_args()

  #Checking if input directory, q exists
  q_exists = os.path.exists(args.query)
  if not q_exists:
    print(args.query)
    print("-q does not exist, please see -h for more info.")
    return None
  
  if args.output_directory != None:
    if args.output_directory[0] != "/":
      args.output_directory = user_directory + "/" + args.output_directory
    print(f"Your html page will be generated in {args.output_directory}.")
  else:
    args.output_directory = args.query + "html_output"
    print(f"Your html page will be generated in {args.output_directory}.")
  
  if args.version:
    print("version 1.0")
    
  #Creates a dictionary to store all the blast and diamond data for html page
  d_html = {}
  
  for file in os.listdir(args.query):
    if file.endswith("Trinity.fasta"):
      trinity_fasta = os.path.join(args.query, file)
      tfasta_read = open(trinity_fasta, "r")
      tfasta = tfasta_read.read()
      d_html["tfasta"] = tfasta.split(">")
    elif file.endswith("qc1.html"):
      d_html["fastqc1"] = args.query + str(file)
      print(d_html["fastqc1"])
    elif file.endswith("qc2.html"):
      d_html["fastqc2"] = args.query + str(file)
      print(d_html["fastqc2"])
    elif file.startswith("coverage"):
      coverage = os.path.join(args.query, file)
      coverage_read = open(coverage, "r")
      coverage_table = coverage_read.readlines()
      d_html["coverage table"] = coverage_table
    elif file.endswith("blast.psl"):
      blast_hits = os.path.join(args.query, file)
      blast_hits_read = open(blast_hits, "r")
      genome = blast_hits_read.readlines()
      d_html["genome"] = tuple(genome)
      print(d_html["genome"])
    elif file.endswith("1.m8"):
      diamond_1 = os.path.join(args.query, file)
      diamond_read1 = open(diamond_1, "r")
      diamond_results1 = diamond_read1.read()
      d_html["diamond_1"] = diamond_results1
    elif file.endswith("1_diamond.txt"):
      dia_length1 = os.path.join(args.query, file)
      length_read1 = open(dia_length1, "r")
      diamond_length1 = length_read1.read()
      d_html["dia_length1"] = (diamond_length1.split(" "))[0]
    elif file.startswith("count1"):
      input_length1 = os.path.join(args.query, file)
      inputlength_read1 = open(input_length1, "r")
      input_diamond_length1 = inputlength_read1.read()
      d_html["input_length1"] = input_diamond_length1
    elif file.endswith("2.m8"):
      diamond_2 = os.path.join(args.query, file)
      diamond_read2 = open(diamond_2, "r")
      diamond_results2 = diamond_read2.read()
      d_html["diamond_2"] = diamond_results2
    elif file.endswith("2_diamond.txt"):
      dia_length2 = os.path.join(args.query, file)
      length_read2 = open(dia_length2, "r")
      diamond_length2 = length_read2.read()
      d_html["dia_length2"] = (diamond_length2.split(" "))[0]
    elif file.startswith("count2"):
      input_length2 = os.path.join(args.query, file)
      inputlength_read2 = open(input_length2, "r")
      input_diamond_length2 = inputlength_read2.read()
      d_html["input_length2"] = input_diamond_length2
    elif file.startswith("blast"):
      if file.endswith(".txt"):
        html_name = (file[6:-4])
        blast_file = os.path.join(args.query, file)
        blast_read = open(blast_file, "r")
        blast_results = blast_read.readlines()
        blast_read = open(blast_file, "r")
        blast_text = blast_read.read()
        d_html["name"] = html_name
        d_html["blast"] = blast_results
        print(d_html["blast"])
        hits_num = []
        hits_virus = []
        for hit in d_html["blast"]:
          blast_hit = (hit.lstrip()).split(" ", 1)
          hits_num.append(int(blast_hit[0]))
          hits_virus.append((blast_hit[1]).rstrip("\n"))
        d_html["blast_hits_num"] = hits_num
        d_html["blast_hits_virus"] = hits_virus
        
  name = d_html["name"]
  blast = d_html["blast"]
  hits_num = d_html["blast_hits_num"]
  hits_virus = d_html["blast_hits_virus"]
  d1 = d_html["diamond_1"]
  d1_length = d_html["dia_length1"]
  #d1_hits = d_html["d1_hits"]
  d1_input_length = d_html["input_length1"]
  d2 = d_html["diamond_2"]
  d2_length = d_html["dia_length2"]
  #d2_hits = d_html["d2_hits"]
  d2_input_length = d_html["input_length2"]
  genome = list(d_html["genome"])
  tfasta = d_html["tfasta"]

  fastqc1 = d_html["fastqc1"]
  fastqc2 = d_html["fastqc2"]
  
  tfasta_accession =[]
  tfasta_sequence_length = []
  for contig in tfasta:
    accession = (contig.split("\n"))[0]
    sequence = contig.replace(accession, "")
    sequence_length = len(sequence.replace("\n", ""))
    tfasta_accession.append(accession)
    tfasta_sequence_length.append(sequence_length)
  
  coverage_table = []
  for coverage_data in d_html["coverage table"]:
    strip_coverage = coverage_data.strip()
    ls_coverage = list(strip_coverage.split("\t"))
    coverage_table.append(ls_coverage)
  
  genome_ls = []
  for hit in genome:
    hit_strip = hit.rstrip()
    hit_ls = hit_strip.split("\t")
    genome_ls.append(hit_ls)
  
  print("genome_ls")
  print(genome_ls)
  
  summary_table = []
  for hit in genome_ls:
    for contig in coverage_table:
      if hit[0] == contig[0]:
        ls_query = [hit[1], contig[1], contig[2], contig[3], contig[5], contig[6]]
        summary_table.append(ls_query)
  
  final_summary = []
  for seq_assignment in hits_virus:
    reads_ls = []
    depth_ls = []
    coverage_ls = []
    length_ls = []
    for result in summary_table:
      if result[0] == seq_assignment:
        reads_ls.append(int(result[3]))
        seq_length = int(result[2]) - int(result[1])
        total_depth = float(result[5])*seq_length
        total_coverage = float(result[4])*seq_length
        coverage_ls.append(total_coverage)
        depth_ls.append(total_depth)
        length_ls.append(seq_length)
    reads_total = str(sum(reads_ls))
    depth_sum = sum(depth_ls)
    mean_depth = str(round(depth_sum/sum(length_ls), 1))
    mean_coverage = str(round(sum(coverage_ls)/sum(length_ls), 1))
    processed_result = [seq_assignment, reads_total, mean_coverage, mean_depth]
    final_summary.append(processed_result)
      
  # Create the html output directory in args.query
  if os.path.exists(args.output_directory):
    print(f"Warning: {args.output_directory} is an existing directory.")
  else:
    os.mkdir(args.output_directory)
    print(f"Directory {args.output_directory} created")
  
  #change directory
  os.chdir(f"{args.output_directory}")
  cwd = os.getcwd()

  WRITE_FLAG = "w"
  is_exist = os.path.isfile(f'./{name}.html')
  if (not is_exist):
    
    #Create html page in output directory
    f = open(f'./{name}.html', WRITE_FLAG)
    f.write('<!DOCTYPE html>\n')
    f.write('<html>\n')
    
    f.write('\t<head>\n')
    f.write('\t\t<script src="https://cdnjs.cloudflare.com/ajax/libs/Chart.js/2.6.0/Chart.min.js"></script>\n')
    f.write(f'\t\t<link rel="stylesheet" href="{stylesheet}">\n')
    f.write('\t</head>\n')
    
    f.write('\t<body>\n')
    f.write('\t<div id="logo"> </br>\n')
    f.write('\t<img src="https://cdn.shopify.com/s/files/1/0054/0141/1695/files/AVS_600x600.png?v=1564844702"> </div>\n\n')
    
    #FastQC
    f.write(f'\t<form method="get" action={fastqc1}><button id = "one" class = "main_buttons" type="submit"> FastQC for R1 </button></form><br>\n')
    f.write(f'\t<form method="get" action={fastqc2}><button id = "two" class = "main_buttons"  type="submit"> FastQC for R2 </button></form><br>\n')
    #f.write('\t<form method="get" action="zzzzz.html"><button id = "three" class = "main_buttons" type="submit"> z </button></form><br>\n')
    
    f.write('\t<h1> DIAMOND OUTPUT </h1></br>\n') 
    
    f.write(f'\t<h2> For {name} R1, there were {d1_length} hits out of {d1_input_length} reads </h2></br></br>\n')
    
    f.write(f'\t<h2> For {name} R2, there were {d2_length} hits out of {d2_input_length} reads </h2></br></br>\n')
    
    #f.write(f'\t{d1}</br></br>\n')
    #f.write(f'\t{d2}</br></br>\n')
    
    f.write('\t<h1> Trinity </h1></br>\n')
    f.write(f'\t<div class="container"></br>\n')
    f.write(f'\t\t<canvas id="trinitycontigs"></canvas></div></br></br>\n')
    
    f.write('\t<h1> BLAST OUTPUT </h1></br>\n')
    
    f.write('\t<TABLE class="styled-table" border="1"\n\tsummary="This table provides information on alignment depth and percent coverage. "></br>\n')
    f.write('\t<TR><TH>Assignment<TD>Reads Aligned to Region<TD>Coverage(%)<TD>Depth of Coverage</br>\n')
    for coverage_data in final_summary:
    #  f.write(f'\t<TR><TH>{coverage_data[0]}<TD>{coverage_data[1]}<TD>{coverage_data[2]}<TD>{coverage_data[3]}<TD>{coverage_data[4]}<TD>{coverage_data[5]}</br>\n')
      f.write(f'\t<TR><TH>{coverage_data[0]}<TD>{coverage_data[1]}<TD>{coverage_data[2]}<TD>{coverage_data[3]}</br>\n')
    f.write('\t</TABLE></br>\n')
    
    f.write(f'\t<div class="container"></br>\n')
    f.write(f'\t\t<canvas id="blasthits"></canvas></div></br></br>\n')
    
    f.write(f'\t<script src="{name}.js"></br>\n')
    f.write(f'\t</script></br></br>\n')
    f.write('\t\t</footer>\n')
    f.write('\t\t</footer>\n')
    
    f.write('\t</body>\n')
    
    
    f.write('</html>\n')
    
    f.close()
    
  else:
    print("Warning: existing html page already exists")
    return None

    #f = open(f'./{html_file}.html', WRITE_FLAG)
    #f.close()
    
  ###############  
  #generate javascript
  WRITE_FLAG = "w"
  is_exist = os.path.isfile(f'./{name}.js')
  if (not is_exist):
    
    #Create js file in output directory
    f = open(f'./{name}.js', WRITE_FLAG)
    
    #Doughnut chart for BLAST hits
    f.write('let myChart1 = document.getElementById("blasthits").getContext("2d");\n')
    f.write('\tChart.defaults.global.defaultFontFamily = "Courier";\n')
    f.write('\tChart.defaults.global.defaultFontSize = 18;\n')
    f.write('\tChart.defaults.global.defaultFontColor = "#777";\n\n')
    
    f.write('\tvar massPopChart = new Chart(blasthits, {\n')
    f.write('\t\ttype:"doughnut",\n')
    f.write('\t\tdata:{\n')
    f.write(f'\t\t\tlabels:{hits_virus},\n')
    f.write('\t\t\tdatasets:[{\n')
    f.write('\t\t\t\tlabel: "Hits",\n')
    f.write(f'\t\t\t\tdata:{hits_num},\n')
    f.write(f'\t\t\t\tbackgroundColor: "rgba(255, 99, 132, 0.6)",\n')
    f.write('\t\t\t\tborderWidth:1,\n')
    f.write('\t\t\t\tborderColor:"#777",\n')
    f.write('\t\t\t\thoverBorderWidth:3,\n')
    f.write('\t\t\t\thoverBorderColor:"#000"\n')
    f.write('\t\t\t}]\n')
    f.write('\t\t},\n')
    
    f.write('\t\toptions:{\n')
    f.write('\t\t\ttitle:{\n')
    f.write('\t\t\t\tdisplay:true,\n')
    f.write('\t\t\t\ttext:"Blast Hits",\n')
    f.write('\t\t\t\tfontSize:30\n')
    f.write('\t\t\t},\n')
    
    f.write('\t\t\tlegend:{\n')
    f.write('\t\t\t\tdisplay:false,\n')
    f.write('\t\t\t\tposition:"right",\n')
    f.write('\t\t\t\tlabels:{\n')
    f.write('\t\t\t\t\tfontColor:"#000"\n')
    f.write('\t\t\t\t}\n')
    f.write('\t\t\t},\n')
    
    f.write('\t\t\tlayout:{\n')
    f.write('\t\t\t\tpadding:{\n')
    f.write('\t\t\t\t\tleft:50,\n')
    f.write('\t\t\t\t\tright:0,\n')
    f.write('\t\t\t\t\tbottom:0,\n')
    f.write('\t\t\t\t\ttop:0\n')
    f.write('\t\t\t\t}\n')
    f.write('\t\t\t},\n')
    
    f.write('\t\t\ttooltips:{\n')
    f.write('\t\t\t\tenabled:true\n')
    f.write('\t\t\t}\n')
    f.write('\t\t}\n')
    f.write('\t});\n\n')
    
    #horizontal bar chart for BLAST hits
    f.write('let myChart2 = document.getElementById("trinitycontigs").getContext("2d");\n')
    f.write('\tChart.defaults.global.defaultFontFamily = "Courier";\n')
    f.write('\tChart.defaults.global.defaultFontSize = 18;\n')
    f.write('\tChart.defaults.global.defaultFontColor = "#777";\n\n')
    
    f.write('\tvar massPopChart2 = new Chart(trinitycontigs, {\n')
    f.write('\t\ttype:"horizontalBar",\n')
    f.write('\t\tdata:{\n')
    f.write(f'\t\t\tlabels:{tfasta_accession},\n')
    f.write('\t\t\tdatasets:[{\n')
    f.write('\t\t\t\tlabel: "Trinity Contig Length (bp)",\n')
    f.write(f'\t\t\t\tdata:{tfasta_sequence_length},\n')
    f.write(f'\t\t\t\tbackgroundColor: "rgba(54, 162, 235, 0.6)",\n')
    f.write('\t\t\t\tborderWidth:1,\n')
    f.write('\t\t\t\tborderColor:"#777",\n')
    f.write('\t\t\t\thoverBorderWidth:3,\n')
    f.write('\t\t\t\thoverBorderColor:"#000"\n')
    f.write('\t\t\t}]\n')
    f.write('\t\t},\n')
    
    f.write('\t\toptions:{\n')
    f.write('\t\t\ttitle:{\n')
    f.write('\t\t\t\tdisplay:true,\n')
    f.write('\t\t\t\ttext:"Trinity Contig Length",\n')
    f.write('\t\t\t\tfontSize:30\n')
    f.write('\t\t\t},\n')
    
    f.write('\t\t\tlegend:{\n')
    f.write('\t\t\t\tdisplay:false,\n')
    f.write('\t\t\t\tposition:"right",\n')
    f.write('\t\t\t\tlabels:{\n')
    f.write('\t\t\t\t\tfontColor:"#000"\n')
    f.write('\t\t\t\t}\n')
    f.write('\t\t\t},\n')
    
    f.write('\t\t\tlayout:{\n')
    f.write('\t\t\t\tpadding:{\n')
    f.write('\t\t\t\t\tleft:50,\n')
    f.write('\t\t\t\t\tright:0,\n')
    f.write('\t\t\t\t\tbottom:0,\n')
    f.write('\t\t\t\t\ttop:0\n')
    f.write('\t\t\t\t}\n')
    f.write('\t\t\t},\n')
    
    f.write('\t\t\ttooltips:{\n')
    f.write('\t\t\t\tenabled:true\n')
    f.write('\t\t\t}\n')
    f.write('\t\t}\n')
    f.write('\t});\n\n')
    
    f.close()
    
  else:
    print("Warning: existing javascript page already exists")
    return None

######
            
main()
