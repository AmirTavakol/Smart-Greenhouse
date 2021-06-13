import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Observable, of } from 'rxjs';
import { ICrops } from './crops';
import { catchError, map, tap } from 'rxjs/operators';
import { MessageService } from '../message.service';
@Injectable({
    providedIn: 'root'
  })
export class CropsService {

    private backendAPI = "http://80.210.98.95:1628";
    constructor(private http: HttpClient,
        private messageService: MessageService) { }

    /** Log a HeroService message with the MessageService */
    private log(message: string) {
        this.messageService.add(`CropsService: ${message}`);
    }

    private handleError<T>(operation = 'operation', result?: T) {
        return (error: any): Observable<T> => {
      
          // TODO: send the error to remote logging infrastructure
          console.error(error); // log to console instead
      
          // TODO: better job of transforming error for user consumption
          this.log(`${operation} failed: ${error.message}`);
      
          // Let the app keep running by returning an empty result.
          return of(result as T);
        };
      }

    //to get data
    getCropsData(): Observable<ICrops[]>{
        let crops = {};
        let url = this.backendAPI + "/getAllCropsForUI"; 
        return this.http.get<ICrops[]>(url).pipe(
            tap(_ => this.log('fetched crops')),
            catchError(this.handleError<ICrops[]>('getCropsData', []))
          );
        }
  
}
