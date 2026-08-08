import { Routes } from '@angular/router';

export const routes: Routes = [
  {
    path: 'guest',
    loadComponent: () => import('./guest-form/guest-form').then((m) => m.GuestForm),
  },
  { path: '', redirectTo: 'guest', pathMatch: 'full' },
];
