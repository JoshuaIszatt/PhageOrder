def main():

    import os
    import sys
    import subprocess
    import argparse
    import random

    # Did you know prompt
    prompts = [
        "My (J.Iszatt) favourite bacteriophage is a Silviavirus named Koomba-kaat_1",
        "Phages were discovered independently by Frederick Twort and Félix d'Hérelle in 1915 and 1917, respectively",
        "A group of flamingos is called a flamboyance",
        "Bacteriophages are the most abundant organisms on Earth, with an estimated 10^31 phages in the biosphere",
        "Bacteriophages have played a key role in the evolution of bacteria, helping to drive the development of new bacterial traits and adaptations.",
        "A single strand of spaghetti is called a spaghetto",
        "I (J.Iszatt) made lab.py to make it easier for people to reorder their genomes AND obtain annotations using the PHROGs database",
        "Annotation is performed using prokka, software developed by Torsten Seemann: https://github.com/tseemann ",
        "The Prokaryotic Virus Remote Homologous Groups database (PHROGS) contains 38,880 protein orthologous groups (868,340 proteins).\nPlease cite: https://doi.org/10.1093/nargab/lqab067 for this"
    ]
    random_prompt = random.choice(prompts)

    # Creating function to check directory path
    def valid_dir(dir_path):
        if not os.path.isdir(dir_path):
            raise argparse.ArgumentTypeError(
                f"{dir_path} is not a valid directory path")
        if not os.access(dir_path, os.R_OK):
            raise argparse.ArgumentTypeError(
                f"{dir_path} is not a readable directory")
        return dir_path

    # Parsing arguments
    image = 'iszatt/phageorder:0.0.2'
    parser = argparse.ArgumentParser(description=f"Reorder and annotate phage genomes. Joshua J Iszatt: https://github.com/JoshuaIszatt")

    # Input/output options
    parser.add_argument('-i', '--input', type=valid_dir, 
                        required=True, help='Input fasta files')
    parser.add_argument('-o', '--output', type=valid_dir, 
                        required=True, help='Direct output to this location')
    parser.add_argument('--manual', action="store_true", 
                        help='Enter container interactively')
    args = parser.parse_args()

    # Obtaining absolute paths
    input_path = os.path.abspath(args.input)
    output_path = os.path.abspath(args.output)

    # Printing command variables
    print(
        f"Program run: {image}",
        f"Input file: {input_path}",
        f"Output file: {output_path}",
        ">>>",
        f"Did you know:",
        f"{random_prompt}",
        ">>>",
        sep='\n'
        )

    # Running docker
    if args.manual:
        
        os.system(f"docker exec -it \
            $(docker run -d \
            -v {input_path}:/lab/input \
            -v {output_path}:/lab/output \
            {image} sleep 1d) bash")

    else:

        command = ["docker run -d -v %s:/lab/input -v %s:/lab/output %s /lab/bin/annotate.sh" %
                (input_path, output_path, image)]
        result = subprocess.Popen(command, shell=True)
        print(command)    


if __name__ == "__main__":
    exit(main())