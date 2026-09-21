import { HttpErrorResponse } from '@angular/common/http';

export function getApiErrorMessage(error: HttpErrorResponse, fallback: string): string {
  if (error.status === 0) {
    return 'Backend ist nicht erreichbar.';
  }

  const detail = error.error?.detail;

  if (typeof detail === 'string') {
    return detail;
  }

  if (error.error && typeof error.error === 'object') {
    for (const value of Object.values(error.error)) {
      if (Array.isArray(value) && value.length > 0 && typeof value[0] === 'string') {
        return value[0];
      }
    }
  }

  if (error.status >= 500) {
    return 'Ein Serverfehler ist aufgetreten.';
  }

  return fallback;
}
