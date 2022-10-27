# adding_stats_to_mmcif

Adds sequence and scaling data to an mmCIF file in preparation for submission to the wwPDB deposition system.

typical usage

### INPUT: Aimless XML file, Any STAR/CIF/mmCIF file, OUTPUT: updated cifFile
```python
from adding_stats_to_mmcif import run_process

aimless_xml_file = 'input.xml'
fasta_sequence_file = 'sequence.fasta'
input_mmcif = 'input.cif'
output_mmcif = 'output.cif'
worked = run_process(input_mmcif=input_mmcif, output_mmcif=output_mmcif,
                             fasta_file=fasta_sequence_file,
                             xml_file=aimless_xml_file)
```
where
aimless_xml_file is the output XML file from Aimless
input_cif is an existing mmCIF file from Refmac
fasta_sequence_file is a fasta file containing the sequence of the polymers in Fasta format
output_cif is the output modified mmCIF file which data from the aimless XML file.

[![Build Status](https://travis-ci.org/berrisfordjohn/adding_stats_to_mmcif.svg?branch=master)](https://travis-ci.org/berrisfordjohn/adding_stats_to_mmcif)
[![Build Status](https://dev.azure.com/berrisfordjohn/berrisford_john/_apis/build/status/berrisfordjohn.adding_stats_to_mmcif?branchName=master)](https://dev.azure.com/berrisfordjohn/berrisford_john/_build/latest?definitionId=2&branchName=master)
![Build status](https://github.com/berrisfordjohn/adding_stats_to_mmcif/actions/workflows/tests.yml/badge.svg)



## Testing
To run tests
    
    python -m unittest
