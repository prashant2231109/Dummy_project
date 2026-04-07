import { Routes } from '@angular/router';
import { ListComponents } from './components/list/list';
import { FormComponent } from './components/form/form';
export const routes: Routes = [
    {
    path: 'sources/new',
    component: ListComponents
    // component: FormComponent
  },
  {
    path: '',
    redirectTo: 'sources/new',
    pathMatch: 'full'
  },


];
