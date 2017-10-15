# adding_stats_to_mmcif

Adds data to an mmCIF file from aimless XML file.

Requires https://github.com/glenveegee/PDBeCIF

typical usage

### INPUT: Aimless XML file, Any STAR/CIF/mmCIF file, OUTPUT: updated cifFile
```python
    ar = aimless_xml_parser.aimlessReport(xml_file=xml_file)
    xml_data = ar.return_data()
    if xml_data:
        pc = pdbe_cif_handling.mmcifHandling(fileName=input_cif)
        pc.parse_mmcif()
        pc.addToCif(data_dictionary=xml_data)
        pc.writeCif(fileName=output_cif)
```
where
xml_file is an aimless XML file
input_cif is an existing mmCIF file
output_cif is the output modified mmCIF file which data from the aimless XML file.