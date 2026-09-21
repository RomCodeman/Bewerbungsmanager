import { Component, inject, OnInit, signal } from '@angular/core';

import { FormBuilder, ReactiveFormsModule, Validators } from '@angular/forms';

import { Application } from '../../models/application';
import { Company } from '../../models/company';

import { ApplicationApi, ApplicationPayload } from '../../services/application-api';

import { CompanyApi } from '../../services/company-api';

import { HttpErrorResponse } from '@angular/common/http';

@Component({
  selector: 'app-applications',
  imports: [ReactiveFormsModule],
  templateUrl: './applications.html',
  styleUrl: './applications.css',
})
export class Applications implements OnInit {
  private readonly applicationApi = inject(ApplicationApi);

  private readonly companyApi = inject(CompanyApi);

  private readonly fb = inject(FormBuilder);

  readonly applications = signal<Application[]>([]);

  readonly companies = signal<Company[]>([]);

  readonly editingId = signal<number | null>(null);

  readonly errorMessage = signal('');

  readonly statuses = [
    { value: 'PLANNED', label: 'Geplant' },
    { value: 'APPLIED', label: 'Beworben' },
    { value: 'INTERVIEW', label: 'Interview' },
    { value: 'ACCEPTED', label: 'Zusage' },
    { value: 'REJECTED', label: 'Absage' },
  ];

  readonly form = this.fb.group({
    company: [null as number | null, Validators.required],
    position: ['', Validators.required],
    status: ['PLANNED', Validators.required],
    application_date: [''],
    job_url: [''],
    contact_person: [''],
    contact_email: [''],
    next_action: [''],
    next_action_date: [''],
    notes: [''],
  });

  readonly isLoading = signal(false);

  ngOnInit(): void {
    this.loadApplications();
    this.loadCompanies();
  }

  loadApplications(): void {
    this.isLoading.set(true);
    this.errorMessage.set('');

    this.applicationApi.getAll().subscribe({
      next: (applications) => {
        this.applications.set(applications);
        this.isLoading.set(false);
      },
      error: () => {
        this.errorMessage.set('Bewerbungen konnten nicht geladen werden.');
        this.isLoading.set(false);
      },
    });
  }

  loadCompanies(): void {
    this.companyApi.getAll().subscribe({
      next: (companies) => {
        this.companies.set(companies);
      },
      error: () => {
        this.errorMessage.set('Unternehmen konnten nicht geladen werden.');
      },
    });
  }
  private buildPayload(): ApplicationPayload {
    const value = this.form.getRawValue();

    return {
      company: value.company!,
      position: value.position!,
      status: value.status!,
      application_date: value.application_date || null,
      job_url: value.job_url || '',
      contact_person: value.contact_person || '',
      contact_email: value.contact_email || '',
      next_action: value.next_action || '',
      next_action_date: value.next_action_date || null,
      notes: value.notes || '',
    };
  }

  save(): void {
    if (this.form.invalid) {
      return;
    }

    const data = this.buildPayload();
    const editingId = this.editingId();

    if (editingId === null) {
      this.applicationApi.create(data).subscribe({
        next: () => {
          this.resetForm();
          this.loadApplications();
        },
        error: (error: HttpErrorResponse) => {
          this.handleApiError(error);
        },
      });

      return;
    }

    this.applicationApi.update(editingId, data).subscribe({
      next: () => {
        this.resetForm();
        this.loadApplications();
      },
      error: () => {
        this.errorMessage.set('Bewerbung konnte nicht aktualisiert werden.');
      },
    });
  }

  edit(application: Application): void {
    this.editingId.set(application.id);

    this.form.patchValue({
      company: application.company,
      position: application.position,
      status: application.status,
      application_date: application.application_date ?? '',
      job_url: application.job_url,
      contact_person: application.contact_person,
      contact_email: application.contact_email,
      next_action: application.next_action,
      next_action_date: application.next_action_date ?? '',
      notes: application.notes,
    });
  }

  delete(application: Application): void {
    const confirmed = window.confirm(`Bewerbung "${application.position}" wirklich löschen?`);

    if (!confirmed) {
      return;
    }

    this.applicationApi.delete(application.id).subscribe({
      next: () => {
        this.loadApplications();
      },
      error: () => {
        this.errorMessage.set('Bewerbung konnte nicht gelöscht werden.');
      },
    });
  }

  resetForm(): void {
    this.form.reset({
      company: null,
      position: '',
      status: 'PLANNED',
      application_date: '',
      job_url: '',
      contact_person: '',
      contact_email: '',
      next_action: '',
      next_action_date: '',
      notes: '',
    });

    this.editingId.set(null);
    this.errorMessage.set('');
  }

  companyName(companyId: number): string {
    return this.companies().find((company) => company.id === companyId)?.name ?? 'Unbekannt';
  }

  private handleApiError(error: HttpErrorResponse): void {
    const applicationDateErrors = error.error?.application_date;

    if (Array.isArray(applicationDateErrors) && applicationDateErrors.length > 0) {
      this.errorMessage.set(applicationDateErrors[0]);
      return;
    }

    this.errorMessage.set('Die Aktion konnte nicht ausgeführt werden.');
  }
}
