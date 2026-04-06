import { Component ,OnInit} from '@angular/core';
import { SourceModel } from '../../models/source';
import { SourceService } from '../../services/source';
import { ChangeDetectorRef } from '@angular/core';
import { FormComponent } from '../form/form';


@Component({
  selector: 'app-list',
  standalone: true,
  imports: [FormComponent],
  templateUrl: './list.html',
  styleUrl: './list.css',
})
export class ListComponents implements OnInit {

sources : SourceModel[] = [];
totalPages : number = 1;
page: number = 1;
showForm: boolean = false;
selectedSource: any = null;

constructor(private SourceService : SourceService ,
private cdr : ChangeDetectorRef
){}

ngOnInit(): void {
  this.getSources();
}

getSources(): void{
  this.SourceService.getSources(this.page).subscribe({
    next :(data) =>{
      console.log("this is data" ,data);

      this.sources = data.results || [];
      this.totalPages = Math.ceil(data.count / 10);
      console.log('total pages' , this.totalPages);
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

  nextPage() {
    if (this.page < this.totalPages) {
      this.page++;
      this.getSources();
    }
  }

  prevPage() {
    if (this.page > 1) {
      this.page--;
      this.getSources();
    }
  }
  goToStory() {
    window.location.href = '/stories/new/';
  }


  updateSource(source:any) {
    this.showForm = true;
    this.selectedSource = source;
}
}
