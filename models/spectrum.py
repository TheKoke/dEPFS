from __future__ import annotations
import numpy


class Spectrum:
    def __init__(self, numbers: numpy.ndarray):
        self._numbers = numbers
        self._peaks: list[int] = []

    @property
    def numbers(self) -> numpy.ndarray:
        return self._numbers

    @property
    def peaks(self) -> list[int]:
        return self._peaks
    
    def copy(self) -> Spectrum:
        new = Spectrum(self._numbers.copy())
        for i in self._peaks:
            new.add_peak(i)
        return new
    
    def evaluate_point(self, x: float) -> int:
        return int(round(x))

    def add_peak(self, hypo: float | int) -> bool:
        if hypo < 0 or hypo >= len(self._numbers):
            return False
        
        self._peaks.append(self.evaluate_point(hypo))
        return True
    
    def delete_peak(self, hypo: float | int) -> bool:
        if hypo < 0 or hypo > len(self._numbers):
            return False
        
        try:
            index = self._peaks.index(self.evaluate_point(hypo))
        except:
            return False
        
        self._peaks.pop(index)
        return True


if __name__ == '__main__':
    pass
