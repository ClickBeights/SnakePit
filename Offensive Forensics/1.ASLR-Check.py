# Search all processes and check for ASLR protection.
# Almost all Win11 default processes are protected.
from typing import Callable, List

from volatility.framework import constants, exceptions, interfaces, renderers
from volatility.framework.configuration import requirements
from volatility.framework.renderers import format_hints
from volatility.framework.symbols import intermed
from volatility.framework.symbols.windows import extensions
from volatility.plugins.windows import pslist

import io
import logging
import os
import pefile  # Used to analyze Portable Executable (PE) files.

vollog = logging.getLogger(__name__)

IMAGE_DLL_CHARACTERISTICS_DYNAMIC_BASE = 0x0040
IMAGE_FILE_RELOCS_STRIPPED = 0x0001

# Helper function to do the analysis by taking a PE as argument.
def check_aslr(pe):
    # Parse the PE.
    pe.parse_data_directories([pefile.DIRECTORY_ENTRY['IMAGE_DIRECTORY_ENTRY_LOAD_CONFIG']])
    dynamic = False
    stripped = False

    # Check whether if it has been compiled with the DYNAMIC base settings
    if pe.OPTIONAL_HEADER.DllCharacteristics & IMAGE_DLL_CHARACTERISTICS_DYNAMIC_BASE:
        dynamic = True
    # Checks if the file relocation data has been stripped out.
    if pe.FILE_HEADER.Characteristics & IMAGE_FILE_RELOCS_STRIPPED:
        stripped = True
    # If both checks failed then the PE is not ASLR protected.
    if not dynamic or (dynamic and stripped):
        aslr = False
    else:
        aslr = True
    return aslr


# Inherit the pluginInterface object (required for volatility plugins).
class AslrCheck(interfaces.plugins.PluginInterface):

    @classmethod
    # Define the required parameters.
    def get_requirements(cls):

        return [
            # Define the memory layer for the plugin.
            requirements.TranslationLayerRequirement(
                name='primary', description='Memory layer for the kernel',
                architectures=["Intel32", "Intel64"]),

            # Define the symbols table.
            requirements.SymbolTableRequirement(
                name="nt_symbols", description="Windows kernel symbols"),

            # Call the pslist plugin as a requirement to collect all processes from memory and re-create the PE file.
            requirements.PluginRequirement(
                name='pslist', plugin=pslist.PsList, version=(1, 0, 0)),

            # Takes a list of process IDs to limit the checking only for those processes.
            requirements.ListRequirement(name='pid',
                                         element_type=int,
                                         description="Process ID to include (all other processes are excluded)",
                                         optional=True),

        ]

    # A filter function that returns False for every process ID in the list.
    @classmethod
    def create_pid_filter(cls, pid_list: List[int] = None) -> Callable[[interfaces.objects.ObjectInterface], bool]:
        filter_func = lambda _: False
        pid_list = pid_list or []
        filter_list = [x for x in pid_list if x is not None]
        if filter_list:
            filter_func = lambda x: x.UniqueProcessId not in filter_list
        return filter_func

    def _generator(self, procs):
        # A data structure to use as we loop over each process in memory.
        pe_table_name = intermed.IntermediateSymbolTable.create(
            self.context,
            self.config_path,
            "windows",
            "pe",
            class_types=extensions.pe.class_types)

        procnames = list()
        for proc in procs:
            procname = proc.ImageFileName.cast("string", max_length=proc.ImageFileName.vol.count, errors='replace')
            if procname in procnames:
                continue
            procnames.append(procname)

            proc_id = "Unknown"
            try:
                proc_id = proc.UniqueProcessId
                proc_layer_name = proc.add_process_layer()
            except exceptions.InvalidAddressException as e:
                vollog.error(f"Process {proc_id}: invalid address {e} in layer {e.layer_name}")
                continue

            # Get Process Environment Block (PEB) memory region associated with each process and put it in an object.
            peb = self.context.object(
                self.config['nt_symbols'] + constants.BANG + "_PEB",
                layer_name=proc_layer_name,
                offset=proc.Peb)

            try:
                dos_header = self.context.object(
                    pe_table_name + constants.BANG + "_IMAGE_DOS_HEADER",
                    offset=peb.ImageBaseAddress,
                    layer_name=proc_layer_name)
            except Exception as e:
                continue

            pe_data = io.BytesIO()
            for offset, data in dos_header.reconstruct():
                pe_data.seek(offset)
                pe_data.write(data)
            # Write the region into a file like object to access this welth of information.
            pe_data_raw = pe_data.getvalue()
            pe_data.close()

            try:
                # Create a PE object using the pefile library.
                pe = pefile.PE(data=pe_data_raw)
            except Exception as e:
                continue

            # pass the object to the ASLR checker
            aslr = check_aslr(pe)

            # Yield the tuple of information containing the process ID and other information...
            yield (0, (proc_id,
                       procname,
                       format_hints.Hex(pe.OPTIONAL_HEADER.ImageBase),
                       aslr,
                       ))

    # No need for arguments as all settings are populated in the config object.
    def run(self):
        # Use pslist to get a list of processes.
        procs = pslist.PsList.list_processes(self.context,
                                             self.config["primary"],
                                             self.config["nt_symbols"],
                                             filter_func=self.create_pid_filter(self.config.get('pid', None)))
        # Return the data from the generator using TreeGrid renderer.
        return renderers.TreeGrid([
            ("PID", int),
            ("Filename", str),
            ("Base", format_hints.Hex),
            ("ASLR", bool)],
            self._generator(procs))
