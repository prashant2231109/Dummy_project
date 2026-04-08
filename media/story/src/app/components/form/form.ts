import { Component, EventEmitter, Output, Input, OnInit } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { CommonModule } from '@angular/common';

import { StoryService } from '../../services/story';
import { TypeaheadModule, TypeaheadMatch } from 'ngx-bootstrap/typeahead';
import { BsModalRef } from 'ngx-bootstrap/modal';
import { CompanyModel, SourceModel } from '../../models/story.model';

@Component({
  selector: 'app-form',
  standalone: true,
  imports: [CommonModule, FormsModule, TypeaheadModule],
  templateUrl: './form.html',
  styleUrls: ['./form.css']
})
export class Form implements OnInit {

  @Output() saved = new EventEmitter<void>();
  @Output() close = new EventEmitter<void>();
  @Input() story: any = null;

  formData = {
    id: null,
    title: '',
    url: '',
    source: null,
    body_text: '',
    tagged_companies: [] as number[]
  };


companies: CompanyModel[] = [];
sources: SourceModel[] = [];
selectedSource: SourceModel | null = null;
sourceSearchText: string = '';

companyQuery = '';
selectedCompanies: CompanyModel[] = [];

constructor(
    private storyService: StoryService,
    public bsModalRef: BsModalRef 
  ) {}

ngOnInit(): void {
    this.loadCompanies();
    this.loadSources();
    if (this.story) {
      this.formData = {
        id: this.story.id,
        title: this.story.title,
        url: this.story.url,
        source: this.story.source,
        body_text: this.story.body_text,
        tagged_companies: this.story.tagged_companies || []
      };
       this.selectedCompanies = this.story.tagged_companies_data || [];
       if (this.story.source_data) {
         this.selectedSource = this.story.source_data;
         this.sourceSearchText = this.story.source_data.name;
       }
    }
  }

loadCompanies() {
    this.storyService.getCompanies().subscribe({
      next: (res: any) => {
        this.companies = res.data ? res.data : res;
      },
      error: (err: any) => console.error(err)
    });
  }

loadSources() {
    this.storyService.getSources().subscribe({
      next: (res: any) => {
        this.sources = res.results ? res.results : (res.data ? res.data : res);
        console.log('Sources loaded:', this.sources)
      },
      error: (err: any) => console.error('Error loading sources:', err)
    });
  }

onSourceSelect(event: TypeaheadMatch) {
  const selected = event.item;
  this.formData.source = selected.id;
  this.sourceSearchText = selected.name; 
}

submitForm() {
  const request = this.formData.id
    ? this.storyService.updateStory(this.formData.id, this.formData)
    : this.storyService.addStory(this.formData);

  request.subscribe({
    next: () => {
      this.saved.emit();       
      this.bsModalRef.hide();   
    },
    error: (err: any) => {
      console.error(err);
      alert('Failed to save story');
    }
  });
}

closeForm() {
  this.bsModalRef.hide(); 
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

syncTaggedCompanies() {
  this.formData.tagged_companies = this.selectedCompanies.map(c => c.id);
}



}

