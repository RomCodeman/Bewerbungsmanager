import { Component, inject, OnInit, signal } from '@angular/core';

import { Company } from '../../models/company';
import { CompanyApi } from '../../services/company-api';


@Component({
  selector: 'app-companies',
  imports: [],
  templateUrl: './companies.html',
  styleUrl: './companies.css',
})
export class Companies implements OnInit {
  private readonly companyApi = inject(CompanyApi);

  readonly companies = signal<Company[]>([]);
  readonly errorMessage = signal('');

  ngOnInit(): void {
    this.companyApi.getAll().subscribe({
      next: (companies) => {
        this.companies.set(companies);
      },
      error: () => {
        this.errorMessage.set(
          'Unternehmen konnten nicht geladen werden.',
        );
      },
    });
  }
}