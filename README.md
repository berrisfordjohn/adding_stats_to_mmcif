# adding_stats_to_mmcif

Adds data to an mmCIF file from aimless XML file.

Requires https://github.com/glenveegee/PDBeCIF

typical usage

### INPUT: Aimless XML file, Any STAR/CIF/mmCIF file, OUTPUT: updated cifFile
```python
import aimless_xml_parser
import cif_handling

xml_file = 'input.xml'
input_mmcif = 'input.cif'
output_mmcif = 'output.cif'

ar = aimless_xml_parser.aimlessReport(xml_file=xml_file)
xml_data = ar.return_data()
if xml_data:
    pc = cif_handling.mmcifHandling(fileName=input_mmcif)
    pc.parse_mmcif()
    pc.addToCif(data_dictionary=xml_data)
    pc.writeCif(fileName=output_mmcif)
```
where
xml_file is an aimless XML file
input_cif is an existing mmCIF file
output_cif is the output modified mmCIF file which data from the aimless XML file.