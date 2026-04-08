import { Component, ChangeDetectorRef, OnInit } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { CommonModule } from '@angular/common';
import { StoryService } from '../../services/story';
import { Form } from '../form/form';
import { Router } from '@angular/router';
import { PageChangedEvent } from 'ngx-bootstrap/pagination';
import { PaginationModule } from 'ngx-bootstrap/pagination';
import { BsModalService, BsModalRef } from 'ngx-bootstrap/modal';
import { StoryModel } from '../../models/story.model';

@Component({
  selector: 'app-list',
  standalone: true,
  imports: [FormsModule, CommonModule,  PaginationModule],
  templateUrl: './list.html',
  styleUrl: './list.css',
})
export class ListComponent implements OnInit {


modalRef?: BsModalRef;  
totalItems: number = 0;
currentPage : number = 1;
page: number = 1;
query: string = '';
stories: StoryModel[] = [];


constructor(
    private storyService: StoryService,
    private cdr: ChangeDetectorRef,
    private router: Router,
    private modalService: BsModalService
  ) {}
  
ngOnInit() {

this.loadStories();

}

openForm(story: StoryModel | null = null) {
  this.modalRef = this.modalService.show(Form, {
    initialState: {
      story: story
    },
    class: 'modal-lg'
  });

  this.modalRef.content.saved.subscribe(() => {
    this.onStoryAdded();  
  });
}


loadStories() {
    this.storyService.getStories(this.page, this.query).subscribe({
      next: (data: any) => {
        this.stories = data.results;
         this.totalItems = data.count;

        this.cdr.markForCheck();
      },
      error: (err:any) => console.error(err)
    });
  }


onSearch(): void {
   this.currentPage = 1;
  this.page = 1;
  this.loadStories();
}


onStoryAdded() {
    this.loadStories();   
}


deleteStory(id: number) {
    if (confirm('Are you sure you want to delete this source?')) {
      this.storyService.deleteStory(id).subscribe({
        next: () => {
          console.log('Deleted');
          this.loadStories();
        },
        error: (err:any) => console.error(err)
      });
    }
  }


pageChanged(event: PageChangedEvent): void {
    this.page = event.page;
    this.loadStories(); 
}


goToSource() {
    window.location.href = '/sources/new/';
}

}