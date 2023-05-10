# PhageOrder v0.0.2
The python script (phage_order.py) will run a docker container to reorder and annotate phage genomes.

This is useful to compare multiple genomes, which are often uploaded 'as is' once the assembly has been complete. However, assembly is random (more information on this elsewhere...) and reordering genomes is not such a trivial task. Especially when many genomes are compared to one another using visual metrics. 

Unordered genomes are very likely to lead people to beleive that genomes are less related than they actually are.

**As an example:** 

The image below depicts three publicly available Pseudomonas genomes:
![Unordered genomes](example_images/pseud_unordered.png)

This next image are the same three genomes, but reordered so they begin with the terminase subunits on the forward coding strand.
![Ordered genomes](example_images/pseud_ordered.png)

Image details:
* Pseudomonas phage Kara-mokiny_1: GenBank: OP314870.1
* Pseudomonas phage Chunk GenBank: MT119376.1
* Pseudomonas phage Pa-A GenBank: MN871454.1

**These images are not produced as part of this software**

To increase the number of ordered phages in public repositories, and make comparisons easier, PhageOrder will reorder the genome based on the small terminase subunit if it can be found. If not it will use the large terminase subunit.

If there is neither, or more than 1 of both, then the genome will be left alone.
This container will not change your RAW files. 

## Open source citation:
```
Iszatt J.(2023).PhageOrder(v0.0.2)[Source code].Github:https://github.com/JoshuaIszatt/PhageOrder
```

## Usage:

**PRE-REQUISITES:**
* Docker installation
* Python

Easy method (After cloning this repository or copying the phage_order.py script)
```sh
python phage_order.py --input <INPUT DIR> --output <OUTPUT DIR>
```

Direct method (Does not require cloning this repo or copying the phage_order.py script)
```sh
docker run -v <PATH TO INPUT DIRECTORY>:/lab/input -v <PATH TO OUTPUT DIRECTORY>:/lab/output iszatt/phageorder:0.0.2 /lab/bin/annotate.sh
```

## Output
* Reordered genome based on the small or large terminase subunit (hierarchy: small>large)
* Annotations using prokka and the PHROGS database (see third party software below)
* Proteins file produced using the PHROGs index directly from: https://phrogs.lmge.uca.fr/
* Log file

## Third-party software
| Software | Version | Description | Please cite |
| -------- | -------- | -------- | -------- |
| prokka | 1.14.6 | Annotation software designed by Torsten Seemann | https://doi.org/10.1093/bioinformatics/btu153 |
| PHROGS database | - | Database of proteins organised into orthologous groups | https://academic.oup.com/nargab/article/3/3/lqab067/6342220 |
| Biopython | 1.79 | A set of tools written in python for biological computation | https://biopython.org/ |

## Docker tags
https://hub.docker.com/r/iszatt

## License
[GNU AGPLv3](https://github.com/JoshuaIszatt/phage_order/blob/master/LICENSE.md)
