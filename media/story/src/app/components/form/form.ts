import { Component, EventEmitter, Output, Input, OnInit } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { CommonModule } from '@angular/common';

import { StoryService } from '../../services/story';



@Component({
  selector: 'app-form',
  standalone: true,
  imports: [CommonModule, FormsModule],
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
    source: 1,
    body_text: '',
    tagged_companies: []
  };

  companies: any[] = [];
  sources: any[] = [];

  constructor(
    private storyService: StoryService,
  
    // private sourceService: SourceService
  ) {}

  ngOnInit(): void {
    this.loadCompanies();
    if (this.story) {
      this.formData = {
        id: this.story.id,
        title: this.story.title,
        url: this.story.url,
        source: this.story.source,
        body_text: this.story.body_text,
        tagged_companies: this.story.tagged_companies || []
      };
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


  submitForm() {
    if (this.formData.id) {
      // Update existing story
      this.storyService.updateStory(this.formData.id, this.formData).subscribe({
        next: () => this.saved.emit(),
        error: (err: any) => {
          console.error(err);
          alert('Failed to update story');
        }
      });
    } else {
      // Create new story
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
}

