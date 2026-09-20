import { HttpClient } from '@angular/common/http';
import { inject, Injectable } from '@angular/core';
import { Observable } from 'rxjs';

import { Application } from '../models/application';

export type ApplicationPayload = Omit<
  Application,
  'id' | 'status_display' | 'created_at' | 'updated_at'
>;

@Injectable({
  providedIn: 'root',
})
export class ApplicationApi {
  private readonly http = inject(HttpClient);

  private readonly apiUrl = 'http://127.0.0.1:8000/api/applications/';

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
