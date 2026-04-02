// import { Component, OnInit } from '@angular/core';
// import { StoryService } from '../../services/story';
// import { FormsModule } from '@angular/forms';
// import { ChangeDetectorRef } from '@angular/core';

// @Component({
//   selector: 'app-list',
//   imports: [FormsModule],
//   templateUrl: './list.html',
//   styleUrl: './list.css',
// })
// export class ListComponent implements OnInit {

//   stories: any[] = [];
//   page = 1;
//   totalPages = 1;
//   query = '';

//   constructor(private storyService: StoryService , private cdr:ChangeDetectorRef) {}

//   ngOnInit() {
//     this.loadStories();
//   }

//   loadStories() {
//     this.storyService.getStories(this.page, this.query).subscribe({
//       next: (data) => {
//         this.stories = data.results;
        

//         this.totalPages = Math.ceil(data.count / 10);

//         console.log('Stories:', this.stories);
//         console.log('Total Pages:', this.totalPages);
//         this.cdr.markForCheck();
//       },
//       error: (err) => {
//         console.error(err);
//       }
//     });
//   }


// nextPage() {
//   if (this.page < this.totalPages) {
//     this.page++;
//     this.loadStories();
//   }
// }

// prevPage() {
//   if (this.page > 1) {
//     this.page--;
//     this.loadStories();
//   }
// }

// search() {
//   this.page = 1;
//   this.loadStories();
// }



import { Component, ChangeDetectorRef, OnInit } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { CommonModule } from '@angular/common';
import { StoryService } from '../../services/story';
import { Subject, debounceTime, distinctUntilChanged } from 'rxjs';
import { Form } from '../form/form';
import { Router } from '@angular/router';

@Component({
  selector: 'app-list',
  standalone: true,
  imports: [FormsModule, CommonModule, Form],
  templateUrl: './list.html',
  styleUrl: './list.css',
})
export class ListComponent implements OnInit {

  page: number = 1;
  totalPages: number = 1;
  query: string = '';
  stories: any[] = [];
  showForm: boolean = false;
  selectedStory: any = null;

  private searchSubject = new Subject<string>();

  constructor(
    private storyService: StoryService,
    private cdr: ChangeDetectorRef,
    private router: Router
  ) {}
  

  ngOnInit() {

   
    this.searchSubject.pipe(
      debounceTime(400),
      distinctUntilChanged()
    ).subscribe((value) => {
      this.page = 1;
      this.loadStories();
    });

  
    this.loadStories();
  }

 
  onSearchChange(value: string) {
    this.searchSubject.next(value);
  }

  loadStories() {
    this.storyService.getStories(this.page, this.query).subscribe({
      next: (data: any) => {
        this.stories = data.results;
        this.totalPages = Math.ceil(data.count / 10);

        this.cdr.markForCheck();
      },
      error: (err:any) => console.error(err)
    });
  }


   onStoryAdded() {
    this.loadStories();   
    this.showForm = false;
    this.selectedStory = null;
  }

  editStory(story: any) {
    this.selectedStory = story;
    this.showForm = true;
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


  closeForm() {
    this.showForm = false;
    this.selectedStory = null;
  }

  nextPage() {
    if (this.page < this.totalPages) {
      this.page++;
      this.loadStories();
    }
  }

  prevPage() {
    if (this.page > 1) {
      this.page--;
      this.loadStories();
    }
  }


goToSource() {
  // this.router.navigate(['/source']);
    window.location.href = '/sources/new/';
}
}