import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { SourceModel, StoryModel, StoryResponse , CompanyModel, StoryInput} from '../models/story.model';

@Injectable({
  providedIn: 'root',
})
export class StoryService {

private apiUrl = 'http://127.0.0.1:8000/story/drf/viewsets/';
private SourceUrl = 'http://127.0.0.1:8000/source/drf/viewsets/';
private companyUrl = 'http://127.0.0.1:8000/company/drf/list/';


constructor(private http: HttpClient) {}




getCompanies() {
  return this.http.get<CompanyModel[]>(this.companyUrl, {
    
  });
}
  

 getStories(page: number = 1, query: string = ''): Observable<StoryResponse> {
  return this.http.get<StoryResponse>(
    `${this.apiUrl}?page=${page}&search=${query}`,
    { withCredentials: true }
  );
}


  addStory(data: StoryInput) {
    return this.http.post(this.apiUrl, data, {
      withCredentials: true
    });
  }



updateStory(id: number, data: Partial<StoryInput>) {
  return this.http.patch(
    `${this.apiUrl}${id}/`,   
    data,
    { withCredentials: true }
  );
}

deleteStory(id: number): Observable<void>  {
    return this.http.delete<void>(`${this.apiUrl}${id}/`, {
      withCredentials: true
    });
  }


getSources(page: number = 1, query: string = ''): Observable<SourceModel> {
  return this.http.get<SourceModel>(
    `${this.SourceUrl}?page=${page}&search=${query}`,
    { withCredentials: true }
  );
}  
}



