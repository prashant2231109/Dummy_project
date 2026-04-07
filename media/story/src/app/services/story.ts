import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable, of, throwError } from 'rxjs';
import { SourceModel, StoryModel, StoryResponse , CompanyModel, StoryInput} from '../models/story.model';
import { catchError } from 'rxjs';

@Injectable({
  providedIn: 'root',
})
export class StoryService {

private apiUrl = 'http://127.0.0.1:8000/story/drf/viewsets/';
private SourceUrl = 'http://127.0.0.1:8000/source/drf/viewsets/';
private companyUrl = 'http://127.0.0.1:8000/company/drf/list/';


constructor(private http: HttpClient) {}

private handleError<T>(operation = 'operation', result?: T, rethrow: boolean = false) {
  return (error: any): Observable<T> => {
    const errorMsg = error?.error?.message || error?.message || 'Unknown error';
    console.error(`${operation} failed: ${errorMsg}`);

   if (rethrow) {
      return throwError(() => error.error);
    }
    return of(result as T);
  };
}


getCompanies() :Observable<CompanyModel[]> {
    return this.http.get<CompanyModel[]>(this.companyUrl)
      .pipe(catchError(this.handleError('getCompanies', [])));
  }
  

getStories(page = 1, query = '') :Observable<StoryResponse>{
    return this.http.get<StoryResponse>(`${this.apiUrl}?page=${page}&search=${query}`)
      .pipe(catchError(this.handleError('getStories', {
        count: 0, 
        next: null, 
        previous: null,
        results: [] }))
      );
  }


addStory(data: StoryInput): Observable<StoryModel> {
    return this.http.post<StoryModel>(this.apiUrl, data)
      .pipe(catchError(this.handleError<StoryModel>('addStory', undefined as any, true))
    );
  }



updateStory(id: number, data: Partial<StoryInput>): Observable<StoryModel> {
    return this.http.patch<StoryModel>(`${this.apiUrl}${id}/`, data)
      .pipe(catchError(this.handleError<StoryModel>('updateStory', undefined as any, true))
    );
  }

deleteStory(id: number): Observable<void> {
    return this.http.delete<void>(`${this.apiUrl}${id}/`)
      .pipe(catchError(this.handleError<void>('deleteStory'))
    );
  }


getSources(page = 1, query = ''): Observable<SourceModel> {
    return this.http.get<SourceModel>(`${this.SourceUrl}?page=${page}&search=${query}`)
      .pipe(catchError(this.handleError<any>('getSources', { 
        count: 0, results: [] })
      ));
  }
}




