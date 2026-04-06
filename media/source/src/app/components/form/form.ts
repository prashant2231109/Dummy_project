import { Component ,EventEmitter , Output, OnInit ,Input} from '@angular/core';
import { SourceService } from '../../services/source';
import { CompanyModel, SourceModel } from '../../models/source';
import { FormsModule } from '@angular/forms';
import { CommonModule } from '@angular/common';
import { Router } from '@angular/router';
import { TypeaheadModule } from 'ngx-bootstrap/typeahead';
import { Observable, debounceTime, switchMap, map } from 'rxjs';

@Component({
  selector: 'app-form',
  imports: [FormsModule, CommonModule, TypeaheadModule],
  templateUrl: './form.html',
  styleUrl: './form.css',
})
export class FormComponent implements OnInit {

@Output() saved = new EventEmitter<void>();
@Output() close = new EventEmitter<void>();
@Input() source: any = null;

 formData = {
    id:null,
    name: '',
    url: '',
    tagged_companies: [] as number[]
  };

companies : any[] = [];


companyQuery = '';
selectedCompanies: any[] = [];



  constructor(private sourceService : SourceService , private router:Router){}

  ngOnInit(): void {
  this.loadCompanies();

  if (this.source) {
    this.formData = {
      id: this.source.id,
      name: this.source.name,
      url: this.source.url,
      tagged_companies: this.source.tagged_companies || []
    };
    this.selectedCompanies = this.source.tagged_companies_data || [];

   

    
  }
}



loadCompanies(): void {
  this.sourceService.getCompanies().subscribe({
    next: (res: any) => {
      this.companies = res.data ? res.data : res;

    },
    error: (err) => console.error('Error fetching companies:', err),
  });
}


  

  submitForm() {

    if (this.formData.id) {
      this.sourceService.updateSource(this.formData.id, this.formData).subscribe({
        next: () => this.saved.emit(),
        error: (err: any) => {
          console.error(err);
          alert('Failed to update story');
        }
      });
    } else{
    this.sourceService.addSource(this.formData).subscribe({
      next: (res: any) => {
        this.saved.emit(); 
        
      },
      error: (err: any) => {
        console.error(' Error adding source:', err)
      }
    });
  }

}

closeForm() {
    this.close.emit();
  }


onCompanySelected(company: any) {
  
  const exists = this.selectedCompanies.some(c => c.id === company.id);
  if (!exists) {
    this.selectedCompanies.push(company);
    this.syncTaggedCompanies();
  }

  this.companyQuery = '';
}

removeCompany(companyId: number) {
  this.selectedCompanies = this.selectedCompanies.filter(c => c.id !== companyId);
  this.syncTaggedCompanies();
}

private syncTaggedCompanies() {
  this.formData.tagged_companies = this.selectedCompanies.map(c => c.id);
}


}
