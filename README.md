# LabVIEW_Scripts
Scripts to Change Bitstream Files in lvbitx

# Summary
Xilinx Vivado generates a bitstream file and using the memory info file it maps an executable of form .elf in to the bitstream.

This bitstream is then read by National Instruments createBitstream.exe, which strips off the bitstream header turning the bitstream in to a binary file.  This binary file is then uu64 encoded and placed inside an lvbitx file.

What we are doing is taking the original bitstream file, the original memory info file and using the Xilinx updatemem command to update the elf that is stored in the bistream, then we convert it in to a format suitable for the lvbitx file and update the file accordingly.

This helps you avoid spending over an hour re-running the implementation and Generate Bitstream stages of Xilinx Vivado allowing for much faster development times.

With LabVIEW 2018, Xilinx Vivado 2017.2 is being used which contains a bug where changes to the elf file are not detected by the Generate Bitstream phase.  The only workaround that I have found after spending countless hours researching this topic on Xilinx and NI's website is to re-run implementation and the generate bitstream steps, which on my desktop takes at least one hour.

# Requirements:
You will need the following files from your Vivado Build:
* original bit file (file extension .bit)
* original memory information file (file extension .mmi)
* a sample LabVIEW bitstream (file extension .lvbitx)



Notes:
* The .mmi file should automatically be generated through your Vivado build and should be located in the runs directory
* In may case, from the ProjectExportForVivado directory I have:
** ProjectExportForVivado
*** .\fpga_nic\fpga_nic.lvbitx
*** .\fpga_nic\VivadoProject\fpga_nic.runs\impl_1\PXIe6592R_Top_Gen2x8.bit
*** .\fpga_nic\VivadoProject\fpga_nic.runs\impl_1\PXIe6592R_Top_Gen2x8.mmi


