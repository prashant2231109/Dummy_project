import { Component, EventEmitter, Output, Input, OnInit } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { CommonModule } from '@angular/common';

import { StoryService } from '../../services/story';
import { TypeaheadModule } from 'ngx-bootstrap/typeahead';





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
  
  companies: any[] = [];
  sources: any[] = [];

companyQuery = '';
selectedCompanies: any[] = [];

  constructor(
    private storyService: StoryService,
  
    // private sourceService: SourceService
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


  submitForm() {
    if (this.formData.id) {
     
      this.storyService.updateStory(this.formData.id, this.formData).subscribe({
        next: () => this.saved.emit(),
        error: (err: any) => {
          console.error(err);
          alert('Failed to update story');
        }
      });
    } else {
      
      this.storyService.addStory(this.formData).subscribe({
        next: () => this.saved.emit(),
        error: (err: any) => {
          console.error(err);
          alert('Failed to add story');
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

