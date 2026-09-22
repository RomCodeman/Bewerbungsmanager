import { HttpClient } from '@angular/common/http';
import { inject, Injectable } from '@angular/core';
import { Observable } from 'rxjs';

import { Application } from '../models/application';

import { API_BASE_URL } from '../config/api';

export type ApplicationPayload = Omit<
  Application,
  'id' | 'status_display' | 'created_at' | 'updated_at'
>;

@Injectable({
  providedIn: 'root',
})
export class ApplicationApi {
  private readonly http = inject(HttpClient);
  private readonly apiUrl = `${API_BASE_URL}/applications/`;

  getAll(): Observable<Application[]> {
    return this.http.get<Application[]>(this.apiUrl);
  }

  create(data: ApplicationPayload): Observable<Application> {
    return this.http.post<Application>(this.apiUrl, data);
  }

  update(id: number, data: Partial<ApplicationPayload>): Observable<Application> {
    return this.http.patch<Application>(`${this.apiUrl}${id}/`, data);
  }

  delete(id: number): Observable<void> {
    return this.http.delete<void>(`${this.apiUrl}${id}/`);
  }
}
