#!/usr/bin/env python
from __future__ import division, absolute_import, print_function, unicode_literals
from qutip import *
from scipy import *
import numpy as np
from error_handling import *


class HilbertSpace(object):

    def __init__(self, ion_number, ion_motional_hilbert_space_dim, ion_electronic_hilbert_space_dim = 2, state_type='pure'):
        """ It takes a tuple of labels and their corresponding Hilbert space dimensions.

        """
        #self.__subsystems_dic                       =  subsystems_dic
        self.__set_hilbert_space_dimensions_array   =  self.__hilbert_space_dimensions()
        self.__identity_operators_array             =  self.__identity_operators_array()


   

    def construct_hilbert_space(self):
        pass


    def get_hilbert_space_array(self):
        return self.__subsystems_list

    def __set_identity_operators_array(self):


        for subsystem_dimensions in self.get_hilbert_space_array():
            tensor( qeye(subsystem_dimensions) )

    def get_identity_operators_array(self):

        return self.__identity_operators_array








class Ion:
        '''
        Create an Ion object with ion_number (>=0), 
        motional_state (>=0) and electronic_state (either 0 or 1).

        '''
        def __init__( self, ion_number, ion_motional_hilbert_space_dim, ion_electronic_hilbert_space_dim = 2, state_type='pure'):

                self.ion_number                        =  ion_number
                #HilbertSpace.__init__(self)
                self.ion_motional_hilbert_space_dim    =  ion_motional_hilbert_space_dim
                self.ion_electronic_hilbert_space_dim  =  ion_electronic_hilbert_space_dim
                self.state_type                        =  state_type
                self.ion_motional_state                =  None
                #self.ion_electronic_state              =  None
                #self.set_hilbert_space()

        def initialize_ion_state(func):

        	def wrapper(self, hilbert_space_dim, state):

            		if self.state_type == 'pure':
                    		if hilbert_space_dim <= state:
                        		raise Dimensionerror( "Ion number {}\n".format(self.ion_number) )
                    		else:
                        		func(self, hilbert_space_dim, state)

                	elif self.state_type == 'density_operator':

                            if type(state) != qutip.qobj.Qobj: 
                                raise Statetypeerror( self.ion_number, self.state_type )
                            else:

                                if hilbert_space_dim <= state.shape[0] - 1:
                                    raise Dimensionerror( "Ion number {}\n".format(self.ion_number) )
                                else:
                                    func(self, hilbert_space_dim, state)

        	return wrapper

 
        @initialize_ion_state
        def initialize_ion_motional_state(self, motional_hilbert_space_dim, ion_motional_state):
                self.motional_state_is_initialized = True
                self.ion_motional_state     = basis( motional_hilbert_space_dim, ion_motional_state )


        @initialize_ion_state
        def initialize_ion_motional_density_operator( self, ion_motional_hilbert_space_dim, density_operator ):
                self.motional_state_is_initialized = True
                self.ion_motional_state  =  density_operator


        @property
        def get_motional_state( self ):
        	try:
                	return self.ion_motional_state
        	except AttributeErroer as e:
                	print(e, "\nNo motional state is assinged to ion number {}".format(self.ion_number) )


        @initialize_ion_state
        def initialize_ion_electronic_state(self, electronic_hilbert_space_dim, ion_electronic_state_num):

                self.electronic_state_is_initialized = True
                self.ion_electronic_state   = basis( electronic_hilbert_space_dim, ion_electronic_state_num )
                    
        @initialize_ion_state
        def initialize_ion_electronic_density_operator(self, electronic_hilbert_space_dim, density_operator):
                self.electronic_state_is_initialized = True
                self.ion_electronic_state   = density_operator

        def set_ion_electronic_state_number(self, state):

        	if state == 0 or state == 1:
        		self.ion_electronic_state_number  =  state
        	else:
                	raise Exception("Ion electronic state could be only o (ground state) or 1 (excited state).")


        def get_position(self):
                try:
                	return self.position
                except AttributeError as e:
                	print(e, "\nNo position is assigned to ion number {}".format(self.ion_number) )


        def set_position(self, position):
                self.position   =  position

        @property
        def get_motional_state(self):

                try:
                	return self.ion_motional_state
                except AttributeError as e:
                	print(e, "\nNo motional state assigned to ion number {}.".format(self.ion_number) )

        @property
        def get_electronic_state(self):
                try:
               		return self.ion_electronic_state
                except AttributeError as e:
                	return self.ion_electronic_state_number
                    	
                #else:
                #    print( e, "\nNo electronic state assigned to ion number {}.".format(self.ion_number) )

class Chain:

        def __init__(self, N, ion_motional_hilbert_space_dim, ion_electronic_hilbert_space_dim = 2, state_type = 'pure'):

                self.num_of_ions                       =  N 
                self.ion_motional_hilbert_space_dim    =  ion_motional_hilbert_space_dim
                self.ion_electronic_hilbert_space_dim  =  ion_electronic_hilbert_space_dim
                self.Ions                              =  [Ion(i, self.ion_motional_hilbert_space_dim, self.ion_electronic_hilbert_space_dim, state_type) for i in range(N)]
                self.state                             =  None
                self.state_type                        =  state_type

        
        def initialize_chain_electronic_states( self, **kwargs): 
                ''' Initialize the initial electronic state of ions that are in coherent interaction with lasers
                and pulses.

                '''
                self.chain_electronic_states_initialized = False

                all_lasers = list(kwargs['lasers']) + list(kwargs['pulses'])
                ions_interacting_with_laser  =  [laser.ion_num for laser in all_lasers]

                for ion_num in ions_interacting_with_laser:
                        self.chain_electronic_states_initialized = True
                        try:
                            if self.state_type == 'pure':
                                self.Ions[ion_num].initialize_ion_electronic_state( self.ion_electronic_hilbert_space_dim, self.Ions[ion_num].ion_electronic_state_number )
                            elif self.state_type == 'density_operator':
                                density_operator = basis( self.ion_electronic_hilbert_space_dim, self.Ions[ion_num].ion_electronic_state_number ) * basis( self.ion_electronic_hilbert_space_dim, self.Ions[ion_num].ion_electronic_state_number ).dag()
                                self.Ions[ion_num].initialize_ion_electronic_density_operator( self.ion_electronic_hilbert_space_dim, density_operator )
                                #else:
                                 #       print("Ion numbering starts at 0 and ends at number of ions - 1.")
                        except ValueError as e:
                                print("Error: Ions name formatting must be as 'ion10' ", e)


        def set_pure_electronic_state_numbers( self, args ):
                ''' Set the initial electronic state of ions given in input,
                Example for input format:  args = (0, 0, 0, 1, 0)
                for a chain of 5 ions. 

                '''

                if len(args) != self.num_of_ions:
                        print("Number of arguments must be equal to the number of ions in the chain. \nLength of state = {}, whereas, number of ions = {}.".format(len(args), self.num_of_ions ) )
                        
                else:
                        for i in range(len(args)):
                        	self.Ions[i].set_ion_electronic_state_number( args[i] )


        @property
        def get_electronic_state( self ):
            states  =  [ ion.get_electronic_state for ion in self.Ions if type(ion.get_electronic_state) != int ]
            if states != []:
                return tensor(states)
            else:
                print("No electronic state is assigned.")


        def set_pure_motional_state( self, args): 
                ''' Initialize the initial motional state of ions given in input,
                Example for input format:  args = (0, 0, 0, 1, 0)
                for a chain of 5 ions. 

                '''
                if len(args) != self.num_of_ions:
                        print("Number of arguments must be equal to the number of ions in the chain. \nLength of state = {}, whereas, number of ions = {}.".format(len(args), self.num_of_ions ) )
                        
                else:
                        for i in range(len(args)):
                        	self.Ions[i].initialize_ion_motional_state( self.ion_motional_hilbert_space_dim, args[i] )

        def set_thermal_motional_state( self, args): 
                ''' Initialize the initial motional state of ions given in input,
                Example for input format:  args = (1.5, 1.0, ..., 2.4)
                for a chain of N ions. Where each float number is the thermal state nbar of the nth ion.  

                '''

                if len(args) != self.num_of_ions:
                        print("Number of arguments must be equal to the number of ions in the chain. \nLength of state = {}, whereas, number of ions = {}.".format(len(args), self.num_of_ions ) )
                        
                else:
                        args = [thermal_dm( self.ion_motional_hilbert_space_dim, arg ) for arg in args]

                        for i in range(len(args)):
                            self.Ions[i].initialize_ion_motional_density_operator( self.ion_motional_hilbert_space_dim, args[i] )


        @property
        def get_motional_state( self ):
            """Return the 'motional quantum state' of the ion chain as one state (could be pure or mixed):

            """
            return tensor([ ion.get_motional_state for ion in self.Ions ])


        @property
        def initial_state( self):
            """Get ion chain quantum state, starting with electronic states of all ions that are in coherent interaction with continuous/pulsed lasers.

            """
            if self.chain_electronic_states_initialized:
                return tensor( self.get_electronic_state, self.get_motional_state )
            else:
                return self.get_motional_state


        def set_zpositions( self, zpositions ):
                if len(zpositions) == self.num_of_ions:
                        for i in range(self.num_of_ions):
                                self.Ions[i].set_position( zpositions[i] )

                else:
                        print("Number of given ions don't match with number of elements in zpositions array.")


        def get_positions(self):
                
                return [ion.get_position() for ion in self.Ions]
                

        def set_couplings( self, omega_x, zpositions, potential='harmonic'):

            if potential == 'harmonic':
                if self.num_of_ions == 1:
                    self.harmonic_couplings = [[omega_x]]
                else:
                    self.harmonic_couplings = self.generate_omegax(self.num_of_ions, omega_x, zpositions, nearest_neighbor_coupling=0)


        
        def generate_omegax(self, N, omega_x, zpositions, nearest_neighbor_coupling=0): 

            couplings = self.generate_couplings(N, omega_x, zpositions, nearest_neighbor_coupling)
            local_radial_freqs = self.generate_local_radial_freqs(omega_x, couplings) 
            omegax = np.zeros((N, N))
            #  Construct the matrix of local radial frequencies and couplings   
            for i in range(N):
                for j in range(N):
                    if i == j:
                        omegax[i][i] = local_radial_freqs[i]
                    else:
                        omegax[i][j] = couplings[i][j]
            return omegax


        def get_couplings(self, potential='harmonic'):
    
            if potential == 'harmonic':
                return self.harmonic_couplings


        @staticmethod
        def generate_couplings(N, omega_x, zposition_arr = [], nearest_neighbor_coupling = 0, 
                               mass = 40 * 1.672621e-27):
            '''Return the matrix of couplings.
            Note that nearest_neighbor_coupling is used only when zposition_arr is empty.

            ''' 

            eps0 = 8.85419e-12
            echarge = 1.60218e-19
            if zposition_arr != []:
                k = echarge**2/(8*mass*omega_x*np.pi*eps0)

            elif nearest_neighbor_coupling != 0:      
                k = nearest_neighbor_coupling 
                zposition_arr = range(N)
            else:
                raise Exception("Either ion positions or the nearest neighbor coupling is missing!") 

            t = np.zeros((len(zposition_arr),len(zposition_arr)))
            for i in range(len(zposition_arr)):
                for j in range(len(zposition_arr)):
                    if i != j:
                        t[i][j] =  k / absolute(zposition_arr[i]-zposition_arr[j]) ** 3
            return t


        @staticmethod
        def generate_local_radial_freqs(omega_x, couplings):
                """Return the array of local radial frequencies

                """
                ion_numbers = range(len(couplings[0]))
                local_radial_freqs = [omega_x for i in ion_numbers]
                for i in ion_numbers:
                    for j in ion_numbers:
                        if j != i:
                            local_radial_freqs[i] -= couplings[i][j]
                return local_radial_freqs

