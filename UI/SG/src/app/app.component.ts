import { Component } from '@angular/core';

@Component({
  selector: 'app-root',
  template: `
  <div class='text-center text-dark'><h1>{{pageTitle}}</h1></div>
    
  <div>
    <router-outlet></router-outlet>
  </div>
  `
})

export class AppComponent {

  pageTitle: string = 'Smart Greenhouse';
  title: any;

  }








