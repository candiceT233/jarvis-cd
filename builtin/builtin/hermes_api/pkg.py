"""
This module provides classes and methods to inject the HermesMpiio interceptor.
HermesMpiio intercepts the MPI I/O calls used by a native MPI program and
routes it to Hermes.
"""
from jarvis_cd.basic.pkg import Interceptor
from jarvis_util import *


class HermesApi(Interceptor):
    """
    This class provides methods to inject the HermesMpiio interceptor.
    """
    def _init(self):
        """
        Initialize paths
        """
        pass

    def _configure_menu(self):
        """
        Create a CLI menu for the configurator method.
        For thorough documentation of these parameters, view:
        https://github.com/scs-lab/jarvis-util/wiki/3.-Argument-Parsing

        :return: List(dict)
        """
        return [
            {
                'name': 'mpi',
                'msg': 'Intercept MPI-IO',
                'type': bool,
                'default': False
            },
            {
                'name': 'posix',
                'msg': 'Intercept POSIX',
                'type': bool,
                'default': False
            },
            {
                'name': 'stdio',
                'msg': 'Intercept STDIO',
                'type': bool,
                'default': False
            },
            {
                'name': 'vfd',
                'msg': 'Intercept HDF5 I/O',
                'type': bool,
                'default': False
            },
        ]

    def _configure(self, **kwargs):
        """
        Converts the Jarvis configuration to application-specific configuration.
        E.g., OrangeFS produces an orangefs.xml file.

        :param kwargs: Configuration parameters for this pkg.
        :return: None
        """
        has_one = False
        if self.config['mpi']:
            self.config['HERMES_MPIIO'] = self.find_library('hermes_mpiio')
            if self.config['HERMES_MPIIO'] is None:
                raise Exception('Could not find hermes_mpi')
            print(f'Found libhermes_mpiio.so at {self.config["HERMES_MPIIO"]}')
            has_one = True
        if self.config['posix']:
            self.config['HERMES_POSIX'] = self.find_library('hermes_posix')
            if self.config['HERMES_POSIX'] is None:
                raise Exception('Could not find hermes_posix')
            print(f'Found libhermes_posix.so at {self.config["HERMES_POSIX"]}')
            has_one = True
        if self.config['stdio']:
            self.config['HERMES_STDIO'] = self.find_library('hermes_stdio')
            if self.config['HERMES_STDIO'] is None:
                raise Exception('Could not find hermes_posix')
            print(f'Found libhermes_stdio.so at {self.config["HERMES_STDIO"]}')
            has_one = True
        if self.config['vfd']:
            self.config['HERMES_VFD'] = self.find_library('hdf5_hermes_vfd')
            if self.config['HERMES_VFD'] is None:
                raise Exception('Could not find hdf5_hermes_vfd')
            print(f'Found libhdf5_hermes_vfd.so at {self.config["HERMES_VFD"]}')
            has_one = True
        if not has_one:
            raise Exception('Hermes API not selected')

    def modify_env(self):
        """
        Modify the jarvis environment.

        :return: None
        """
        if self.config['mpi']:
            self.append_env('LD_PRELOAD', self.config['HERMES_MPIIO'])
        if self.config['posix']:
            self.append_env('LD_PRELOAD', self.config['HERMES_POSIX'])
        if self.config['stdio']:
            self.append_env('LD_PRELOAD', self.config['HERMES_STDIO'])
        if self.config['vfd']:
            plugin_path_parent = (
                str(pathlib.Path(self.config['HERMES_VFD']).parent))
            self.setenv('HDF5_PLUGIN_PATH', plugin_path_parent)
            self.setenv('HDF5_DRIVER', 'hdf5_hermes_vfd')
