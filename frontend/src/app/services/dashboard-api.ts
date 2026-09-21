import { HttpClient } from '@angular/common/http';
import { inject, Injectable } from '@angular/core';
import { Observable } from 'rxjs';

import { DashboardStats } from '../models/dashboard-stats';

import { API_BASE_URL } from '../config/api';

@Injectable({
  providedIn: 'root',
})
export class DashboardApi {
  private readonly http = inject(HttpClient);

  private readonly apiUrl = `${API_BASE_URL}/dashboard/`;

  getStats(): Observable<DashboardStats> {
    return this.http.get<DashboardStats>(this.apiUrl);
  }
}
