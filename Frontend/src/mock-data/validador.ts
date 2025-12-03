import type { ValidationStatus } from '../types';

export const mockPseudocode = `PROCEDURE busquedaLineal(A: array, x: elemento)
  n ← length(A)
  FOR i ← 0 TO n-1 DO
    IF A[i] = x THEN
      RETURN i
    END IF
  END FOR
  RETURN -1
END PROCEDURE`;

export const mockValidation: Record<string, ValidationStatus> = {
  lexica: 'valid',
  sintaxis: 'valid',
  estructuras: 'invalid'
};
