import { HttpClient } from '@angular/common/http';
import { inject, Injectable } from '@angular/core';
import { Observable } from 'rxjs';

import { Company } from '../models/company';

export type CompanyPayload = Omit<Company, 'id' | 'created_at' | 'updated_at'>;

@Injectable({
  providedIn: 'root',
})
export class CompanyApi {
  private readonly http = inject(HttpClient);

  private readonly apiUrl = 'http://127.0.0.1:8000/api/companies/';

  getAll(): Observable<Company[]> {
    return this.http.get<Company[]>(this.apiUrl);
  }

  create(data: CompanyPayload): Observable<Company> {
    return this.http.post<Company>(this.apiUrl, data);
  }

  update(id: number, data: Partial<CompanyPayload>): Observable<Company> {
    return this.http.patch<Company>(`${this.apiUrl}${id}/`, data);
  }

  delete(id: number): Observable<void> {
    return this.http.delete<void>(`${this.apiUrl}${id}/`);
  }
}
