import { Component } from '@angular/core';
import { SourceService } from '../../services/source';
import { CompanyModel, SourceModel } from '../../models/source';

@Component({
  selector: 'app-form',
  imports: [],
  templateUrl: './form.html',
  styleUrl: './form.css',
})
export class FormComponent {
 formData = {
    name: '',
    url: '',
    tagged_companies: []
  };

  companies : CompanyModel[] = [];

  constructor(private sourceService : SourceService){}

  ngonInit(): void {
    this.loadCompanies();
  }

  loadCompanies(): void {
    this.sourceService.getCompanies().subscribe({
      next: (data) => {
        this.companies = data.results || [];
      },
      error: (err) => {
        console.error('Error fetching companies:', err);
      }
    });
  }

  


}
