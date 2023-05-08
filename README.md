# PhageOrder v0.0.1
This python script (phage_order.py) will run a docker container to reorder and annotate phage genomes.

## Open source citation:
```
Iszatt J.(2023).PhageOrder(v0.0.1)[Source code].Github:https://github.com/JoshuaIszatt/phage_order
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
| Software | Version | Description | doi / link |
| -------- | -------- | -------- | -------- |
| prokka | 1.14.6 | Annotation software designed by Torsten Seemann | https://doi.org/10.1093/bioinformatics/btu153 |
| PHROGS database | - | Database of proteins organised into orthologous groups | https://academic.oup.com/nargab/article/3/3/lqab067/6342220 |
| Biopython | 1.79 | A set of tools written in python for biological computation | https://biopython.org/ |

## Docker tags
https://hub.docker.com/r/iszatt

## License
[GNU AGPLv3](https://github.com/JoshuaIszatt/phage_order/blob/master/LICENSE.md)
