import { Component, inject, OnInit, signal } from '@angular/core';
import { HttpErrorResponse } from '@angular/common/http';

import { DashboardStats } from '../../models/dashboard-stats';
import { DashboardApi } from '../../services/dashboard-api';
import { getApiErrorMessage } from '../../utils/api-error';

@Component({
  imports: [],
  selector: 'app-dashboard',
  styleUrl: './dashboard.css',
  templateUrl: './dashboard.html',
})
export class Dashboard implements OnInit {
  private readonly dashboardApi = inject(DashboardApi);

  readonly stats = signal<DashboardStats | null>(null);

  readonly isLoading = signal(false);
  readonly errorMessage = signal('');

  ngOnInit(): void {
    this.loadStats();
  }

  loadStats(): void {
    this.isLoading.set(true);
    this.errorMessage.set('');

    this.dashboardApi.getStats().subscribe({
      next: (stats) => {
        this.stats.set(stats);
        this.isLoading.set(false);
      },

      error: (error: HttpErrorResponse) => {
        this.errorMessage.set(getApiErrorMessage(error, 'Dashboard konnte nicht geladen werden.'));

        this.isLoading.set(false);
      },
    });
  }
}
