import { Routes } from '@angular/router';
import { ListComponent } from './components/list/list';

export const routes: Routes = [

    {
    path: 'stories/new',
    component: ListComponent
  },
  {
    path: '',
    redirectTo: 'stories/new',
    pathMatch: 'full'
  }
    
];
