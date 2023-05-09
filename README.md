# PhageOrder v0.0.2
This python script (phage_order.py) will run a docker container to reorder and annotate phage genomes.

This is useful to compare multiple genomes, which are often uploaded 'as is' once the assembly has been complete. Not very useful if you are comparing bacteriophages.

To increase the number of ordered phages in public repositories, and make comparisons easier, PhageOrder will reorder the genome based on the small terminase subunit if it can be found. If not it will use the large terminase subunit.

If there is neither, or more than 1 of both, then the genome will be left alone.
This container will not change your RAW files. 


## Open source citation:
```
Iszatt J.(2023).PhageOrder(v0.0.2)[Source code].Github:https://github.com/JoshuaIszatt/PhageOrder
```

## Prerequisites
* Docker installation
* Python

## Usage
```sh
python phage_order.py --input <INPUT DIR> --output <OUTPUT DIR>
```

## Output
* Reordered genome based on the small or large terminase subunit (hierarchy: small>large)
* Annotations using prokka and the PHROGS database (see third party software below)
* Proteins file produced using the PHROGs index directly from: https://phrogs.lmge.uca.fr/
* Log file of exactly what was done to your genomes

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
