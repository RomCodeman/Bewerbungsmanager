import { Component, inject, OnInit, signal } from '@angular/core';

import { Application } from '../../models/application';
import { ApplicationApi } from '../../services/application-api';


@Component({
  selector: 'app-applications',
  imports: [],
  templateUrl: './applications.html',
  styleUrl: './applications.css',
})
export class Applications implements OnInit {
  private readonly applicationApi = inject(ApplicationApi);

  readonly applications = signal<Application[]>([]);
  readonly errorMessage = signal('');

  ngOnInit(): void {
    this.applicationApi.getAll().subscribe({
      next: (applications) => {
        this.applications.set(applications);
      },
      error: () => {
        this.errorMessage.set(
          'Bewerbungen konnten nicht geladen werden.',
        );
      },
    });
  }
}