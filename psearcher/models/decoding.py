import struct
import numpy


# Physics area
BEAM_CHARGE    = 0
BEAM_NUCLON    = 1
TARGET_CHARGE  = 2
TARGET_NUCLON  = 3
BEAM_ENERGY    = 4
DETECTOR_ANGLE = 8
# Electronics area
E_DETECTOR_THICKNESS  = 12
E_DETECTOR_MADEOF     = 16
E_DETECTOR_RESOLUTION = 20
DE_DETECTOR_THICKNESS = 24
DE_DETECTOR_MADEOF    = 28
DE_DETECTOR_RESOLUTION = 32
# Cross-section valuable, details area
INTEGRATOR_COUNTS        = 36
CONGRUENCE               = 40
INTEGRATOR_CONSTANT      = 44
COLLIMATOR_RADIUS        = 48
TARGET_DETECTOR_DISTANCE = 52
# Matrix area
E_SIZE       = 56
DE_SIZE      = 58
MATRIX_START = 60
# Dynamic area, locuses and spectres
LOCUSES_START = lambda height, width: MATRIX_START + 4 * height * width


class Decoder:
    def __init__(self, path: str) -> None:
        self.buffer = open(path, 'rb').read()

    @property
    def matrix_sizes(self) -> tuple[int, int]:
        e_size = struct.unpack_from('H', self.buffer, E_SIZE)[0]
        de_size = struct.unpack_from('H', self.buffer, DE_SIZE)[0]

        return (e_size, de_size)

    def get_matrix(self) -> numpy.ndarray:
        e_size, de_size = self.matrix_sizes
        flat = [struct.unpack_from('I', self.buffer, MATRIX_START + 4 * i)[0] for i in range(e_size * de_size)]
        return numpy.array(flat).reshape(de_size, e_size)
    

if __name__ == '__main__':
    pass
