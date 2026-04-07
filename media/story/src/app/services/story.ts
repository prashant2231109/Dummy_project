import { Injectable } from '@angular/core';
import { HttpClient ,HttpParams} from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root',
})
export class StoryService {

apiUrl = 'http://127.0.0.1:8000/story/drf/viewsets/';
private SourceUrl = 'http://127.0.0.1:8000/source/drf/viewsets/';

constructor(private http: HttpClient) {}

// getStories(page: number = 1, query: string = ''): Observable<any> {
//     return this.http.get(
//       `${this.apiUrl}?page=${page}&q=${query}`,
//       { withCredentials: true }
//     );
//   }
// }

 getCompanies() {
  return this.http.get('http://127.0.0.1:8000/company/drf/list/', {
    withCredentials: true   
  });
}
  

 getStories(page: number = 1, query: string = ''): Observable<any> {
  return this.http.get<any>(
    `${this.apiUrl}?page=${page}&search=${query}`,
    { withCredentials: true }
  );
}


   addStory(data: any) {
    return this.http.post(this.apiUrl, data, {
      withCredentials: true
    });
  }



  updateStory(id: number, data: any) {
  return this.http.patch(
    `${this.apiUrl}${id}/`,   
    data,
    { withCredentials: true }
  );
}

deleteStory(id: number) {
    return this.http.delete(`${this.apiUrl}${id}/`, {
      withCredentials: true
    });
  }


getSources(page: number = 1, query: string = ''): Observable<any> {
  return this.http.get<any>(
    `${this.SourceUrl}?page=${page}&search=${query}`,
    { withCredentials: true }
  );
}  
}



