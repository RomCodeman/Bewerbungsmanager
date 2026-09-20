import { Routes } from '@angular/router';

import { Applications } from './pages/applications/applications';
import { Companies } from './pages/companies/companies';
import { Dashboard } from './pages/dashboard/dashboard';

export const routes: Routes = [
  {
    path: '',
    redirectTo: 'dashboard',
    pathMatch: 'full',
  },
  {
    path: 'dashboard',
    component: Dashboard,
  },
  {
    path: 'companies',
    component: Companies,
  },
  {
    path: 'applications',
    component: Applications,
  },
  {
    path: '**',
    redirectTo: 'dashboard',
  },
];