import { Component ,OnInit} from '@angular/core';
import { SourceModel } from '../../models/source';
import { SourceService } from '../../services/source';
import { ChangeDetectorRef } from '@angular/core';
import { FormComponent } from '../form/form';
import { FormsModule } from '@angular/forms';
import { PageChangedEvent } from 'ngx-bootstrap/pagination';
import { PaginationModule } from 'ngx-bootstrap/pagination';

@Component({
  selector: 'app-list',
  standalone: true,
  imports: [FormComponent, FormsModule, PaginationModule],
  templateUrl: './list.html',
  styleUrl: './list.css',
})
export class ListComponents implements OnInit {

sources : SourceModel[] = [];
// totalPages : number = 1;
totalItems: number = 0;
currentPage: number = 1;
page: number = 1;
showForm: boolean = false;
selectedSource: any = null;

query: string = '';

constructor(private SourceService : SourceService ,
private cdr : ChangeDetectorRef
){}

ngOnInit(): void {
  this.getSources();
}

onSearch(): void {
   this.currentPage = 1;
  this.page = 1;
  this.getSources();
}

getSources(): void{
  this.SourceService.getSources(this.page, this.query ).subscribe({
    next :(data) =>{
      console.log("this is data" ,data);

      this.sources = data.results || [];
      this.totalItems = data.count;
      console.log('total pages' , this.totalItems);
      this.cdr.markForCheck();

    },
    error: (err) => {
        console.error('Error fetching sources:', err);
      }
  });
}


deleteSource(id:number) : void {
  this.SourceService.deleteSource(id).subscribe({
    next: () =>{
      console.log("source deleted");
      this.getSources()
    },
    error : (err) => {
      console.error('Error deleting source:', err);
    }
  });
}


onSourceAdded() {
    this.getSources();     
    this.showForm = false; 
  }


pageChanged(event: PageChangedEvent): void {
    this.page = event.page;

    this.getSources(); 
  }

goToStory() {
    window.location.href = '/stories/new/';
  }


updateSource(source:any) {
    this.showForm = true;
    this.selectedSource = source;
}
}
