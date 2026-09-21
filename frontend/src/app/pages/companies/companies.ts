import { HttpErrorResponse } from '@angular/common/http';
import { Component, inject, OnInit, signal } from '@angular/core';
import { FormBuilder, ReactiveFormsModule, Validators } from '@angular/forms';

import { Company } from '../../models/company';
import { getApiErrorMessage } from '../../utils/api-error';
import { CompanyApi, CompanyPayload } from '../../services/company-api';

@Component({
  selector: 'app-companies',
  imports: [ReactiveFormsModule],
  templateUrl: './companies.html',
  styleUrl: './companies.css',
})
export class Companies implements OnInit {
  private readonly companyApi = inject(CompanyApi);
  private readonly fb = inject(FormBuilder);

  readonly companies = signal<Company[]>([]);
  readonly errorMessage = signal('');
  readonly editingId = signal<number | null>(null);

  readonly form = this.fb.nonNullable.group({
    name: ['', Validators.required],
    website: [''],
    city: [''],
    career_url: [''],
    notes: [''],
  });

  readonly isLoading = signal(false);

  ngOnInit(): void {
    this.loadCompanies();
  }

  loadCompanies(): void {
    this.isLoading.set(true);
    this.errorMessage.set('');

    this.companyApi.getAll().subscribe({
      next: (companies) => {
        this.companies.set(companies);
        this.isLoading.set(false);
      },

      error: (error: HttpErrorResponse) => {
        this.errorMessage.set(
          getApiErrorMessage(error, 'Unternehmen konnten nicht geladen werden.'),
        );
        this.isLoading.set(false);
      },
    });
  }

  save(): void {
    if (this.form.invalid) {
      return;
    }

    const data: CompanyPayload = this.form.getRawValue();

    const editingId = this.editingId();

    if (editingId === null) {
      this.companyApi.create(data).subscribe({
        next: () => {
          this.resetForm();
          this.loadCompanies();
        },
        error: (error: HttpErrorResponse) => {
          this.errorMessage.set(
            getApiErrorMessage(error, 'Unternehmen konnte nicht erstellt werden.'),
          );
        },
      });

      return;
    }

    this.companyApi.update(editingId, data).subscribe({
      next: () => {
        this.resetForm();
        this.loadCompanies();
      },

      error: (error: HttpErrorResponse) => {
        this.errorMessage.set(
          getApiErrorMessage(error, 'Unternehmen konnte nicht aktualisiert werden.'),
        );
      },
    });
  }

  edit(company: Company): void {
    this.editingId.set(company.id);

    this.form.patchValue({
      name: company.name,
      website: company.website,
      city: company.city,
      career_url: company.career_url,
      notes: company.notes,
    });
  }

  delete(company: Company): void {
    const confirmed = window.confirm(`Unternehmen "${company.name}" wirklich löschen?`);

    if (!confirmed) {
      return;
    }

    this.companyApi.delete(company.id).subscribe({
      next: () => {
        this.loadCompanies();
      },

      error: (error: HttpErrorResponse) => {
        this.errorMessage.set(
          getApiErrorMessage(error, 'Unternehmen konnte nicht gelöscht werden.'),
        );
      },
    });
  }

  resetForm(): void {
    this.form.reset();
    this.editingId.set(null);
    this.errorMessage.set('');
  }
}
