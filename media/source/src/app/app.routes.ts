import { Routes } from '@angular/router';
import { ListComponents } from './components/list/list';

export const routes: Routes = [
    {
    path: 'sources/new',
    component: ListComponents
  },
  {
    path: '',
    redirectTo: 'sources/new',
    pathMatch: 'full'
  }

];
