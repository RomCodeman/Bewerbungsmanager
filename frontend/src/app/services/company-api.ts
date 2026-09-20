import { HttpClient } from '@angular/common/http';
import { inject, Injectable } from '@angular/core';
import { Observable } from 'rxjs';

import { Company } from '../models/company';


@Injectable({
  providedIn: 'root',
})
export class CompanyApi {
  private readonly http = inject(HttpClient);

  private readonly apiUrl =
    'http://127.0.0.1:8000/api/companies/';

  getAll(): Observable<Company[]> {
    return this.http.get<Company[]>(this.apiUrl);
  }
}