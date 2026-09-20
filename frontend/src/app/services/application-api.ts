import { HttpClient } from '@angular/common/http';
import { inject, Injectable } from '@angular/core';
import { Observable } from 'rxjs';

import { Application } from '../models/application';

@Injectable({
  providedIn: 'root',
})
export class ApplicationApi {
  private readonly http = inject(HttpClient);

  private readonly apiUrl = 'http://127.0.0.1:8000/api/applications/';

  getAll(): Observable<Application[]> {
    return this.http.get<Application[]>(this.apiUrl);
  }
}
